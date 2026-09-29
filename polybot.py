#!/usr/bin/env python3
"""
Polyester Testnet bot — connect wallet, deposit ETH (Sepolia), social verify,
daily reward claim, and routine spot trading.

Usage:
  python3 polybot.py status
  python3 polybot.py claim
  python3 polybot.py terms
  python3 polybot.py social-status
  python3 polybot.py social-start twitter <handle>
  python3 polybot.py social-ready twitter
  python3 polybot.py deposit-address [chain_id]
  python3 polybot.py deposit-eth <amount_eth>
  python3 polybot.py trade [rounds]
  python3 polybot.py all

Env: PK (wallet private key), optional SEPOLIA_RPC, CDP_PORT
"""

import json
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

import cdp_browser as CB
from poly import Poly
from w3wallet import WalletBridge

ROOT = Path("/root/polyester-bot")
OUT = ROOT / "recon"
OUT.mkdir(exist_ok=True)

ETH_SEPOLIA = 2          # Polyester internal chain id for ethereum-sepolia
PROVIDER = {"twitter": 1, "discord": 2, "1": 1, "2": 2}
PROVIDER_NAME = {1: "TWITTER", 2: "DISCORD"}
METHOD = {"profile": 1, "channel": 2, "dm": 3, "1": 1, "2": 2, "3": 3}


def log(*a):
    print(*a, flush=True)


class Bot:
    def __init__(self, pk):
        self.wallet = WalletBridge(pk)
        self.pw = None
        self.browser = None
        self.ctx = None
        self.page = None
        self.poly = None

    # ---------- lifecycle ----------
    def open(self):
        CB.ensure_chrome()
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.connect_over_cdp(CB.CDP if hasattr(CB, "CDP") else f"http://127.0.0.1:{CB.PORT}")
        self.ctx = self.browser.contexts[0]
        page = None
        for pg in self.ctx.pages:
            if "polyester" in pg.url:
                page = pg
        self.page = page or self.ctx.pages[0]
        self.poly = Poly(self.page)
        self.wallet.bind(self.page)
        self.page.add_init_script(
            f"window.__WALLET_ADDRESS={json.dumps(self.wallet.address)};"
            f"window.__WALLET_CHAIN_HEX={json.dumps(self.wallet.chain_hex)};")
        self.page.add_init_script(CB.INJECT)
        self._inject()
        log(f"wallet {self.wallet.address} | page {self.page.url}")
        return self

    def _inject(self):
        try:
            self.page.evaluate(f"window.__WALLET_ADDRESS={json.dumps(self.wallet.address)};"
                               f"window.__WALLET_CHAIN_HEX={json.dumps(self.wallet.chain_hex)};")
            self.page.evaluate(CB.INJECT)
        except Exception as e:
            log("inject err", str(e)[:120])

    def close(self):
        try:
            if self.pw:
                self.pw.stop()
        except Exception:
            pass

    # ---------- auth ----------
    def logged_in(self):
        return bool(self.poly.token())

    def go(self, path, wait=5):
        self.page.goto(CB.BASE + path, wait_until="domcontentloaded", timeout=60000)
        t0 = time.time()
        while time.time() - t0 < 60:
            if "Just a moment" not in self.page.title():
                break
            time.sleep(2)
        time.sleep(wait)
        self._inject()

    def login(self):
        if self.logged_in():
            log("already logged in")
            return True
        self.go("/connect", 3)
        try:
            self.page.get_by_text("Continue with MetaMask", exact=False).first.click(timeout=20000)
            log("clicked MetaMask")
        except Exception as e:
            log("click err", str(e)[:100])
        for i in range(25):
            time.sleep(3)
            if self.logged_in() and "/connect" not in self.page.url:
                log("logged in ->", self.page.url)
                return True
            if "/connect" not in self.page.url and self.logged_in():
                return True
        log("login FAILED")
        return False

    # ---------- tasks ----------
    def accept_terms(self):
        r = self.poly.call("auth.v1.AuthService/AcceptTerms", {})
        log("AcceptTerms ->", r["status"], json.dumps(r["body"])[:200])
        return r

    def balances(self):
        r = self.poly.balances()
        return r["body"]

    def non_zero_balances(self):
        b = self.balances()
        out = []
        for x in (b.get("balances") or []):
            vals = {}
            for k in ("trading", "funding", "available", "reserved"):
                v = x.get(k) or {}
                if v:
                    vals[k] = v
            if vals:
                out.append({"assetId": x.get("assetId"), **vals})
        return out

    def claim_status(self):
        return self.poly.claim_status()["body"]

    def claim(self):
        st = self.claim_status()
        log("claim state:", st.get("state"), "reset:", st.get("resetAt"))
        if st.get("state") != "CLAIM_AVAILABLE":
            return st
        r = self.poly.claim()
        log("ClaimDailyReward ->", r["status"], json.dumps(r["body"])[:500])
        return r["body"]

    def social_status(self):
        out = {}
        for pid in (1, 2):
            r = self.poly.call("auth.v1.SocialVerificationService/GetSocialVerification", {"provider": pid})
            out[PROVIDER_NAME[pid]] = r
            log(PROVIDER_NAME[pid], "->", r["status"], json.dumps(r["body"])[:300])
        return out

    def social_start(self, provider, handle, method=1):
        r = self.poly.start_social(provider, method, handle)
        log("StartSocialVerification ->", r["status"], json.dumps(r["body"], indent=1)[:600])
        return r["body"]

    def set_profile_twitter(self, handle):
        r = self.poly.call("auth.v1.ProfileService/UpdateProfile", {"twitter": handle})
        log("UpdateProfile(twitter) ->", r["status"], json.dumps(r["body"])[:300])
        return r["body"]

    def x_verify_start(self, handle):
        """Step 1: register handle + get the challenge code to put in the X bio."""
        self.set_profile_twitter(handle)
        body = self.social_start(1, handle, 1)   # twitter, method=profile
        code = (body or {}).get("challengeCode") or ((body or {}).get("verification") or {}).get("challengeCode")
        log("X challenge code:", code)
        return code

    def x_verify_check(self, tries=10, delay=5):
        """Step 3 (after the code is in the bio): flip to ready and poll."""
        r = self.poly.social_ready(1)
        log("SocialVerificationReady(twitter) ->", r["status"], json.dumps(r["body"])[:300])
        for i in range(tries):
            time.sleep(delay)
            g = self.poly.social(1)
            v = (g["body"] or {}).get("verification") or {}
            log(f"  [{i}] status={v.get('status')} handle={v.get('handle')} err={v.get('lastError')}")
            if v.get("status") == "verified":
                return True
        return False

    def social_ready(self, provider):
        r = self.poly.social_ready(provider)
        log("SocialVerificationReady ->", r["status"], json.dumps(r["body"])[:500])
        return r["body"]

    def deposit_address(self, chain_id=ETH_SEPOLIA):
        r = self.poly.list_deposit_addresses(chain_id=chain_id)
        addrs = (r["body"] or {}).get("depositAddresses") or []
        if not addrs:
            r2 = self.poly.create_deposit_address(chain_id, 0)
            log("CreateDepositAddress ->", r2["status"], json.dumps(r2["body"])[:300])
            r = self.poly.list_deposit_addresses(chain_id=chain_id)
            addrs = (r["body"] or {}).get("depositAddresses") or []
        log("deposit addresses:", json.dumps(addrs)[:400])
        return addrs[0]["depositAddress"] if addrs else None

    def deposit_eth(self, amount_eth):
        addr = self.deposit_address(ETH_SEPOLIA)
        if not addr:
            log("no deposit address")
            return None
        bal = self.wallet.rpc("eth_getBalance", json.dumps([self.wallet.address, "latest"]))
        log(f"wallet {self.wallet.address} sepETH balance: {int(bal, 16)/1e18:.6f}")
        wei = int(float(amount_eth) * 1e18)
        tx = {"to": addr, "value": hex(wei)}
        txh = self.wallet.send_tx(tx)
        log("deposit tx:", txh)
        return txh

    # ---------- trading ----------
    def spot_config(self):
        return self.poly.spot_config()["body"]

    def pairs(self):
        return {p["symbol"]: p for p in self.spot_config().get("pairs", [])}

    def orders(self):
        return self.poly.open_orders()["body"], self.poly.order_history()["body"]

    def market_order(self, symbol="BTC-USDT", side="buy", quote_usd=20.0,
                     slippage_bps=500, qty_base=None):
        pairs = self.pairs()
        p = pairs.get(symbol)
        if not p:
            log("unknown symbol", symbol, "have:", list(pairs)[:20])
            return None
        ob = self.poly.call("orderbook.v1.OrderbookService/GetOrderBook",
                            {"symbolId": p["symbolId"], "depth": 2})["body"]
        ref_scale = 10 ** int(p.get("referencePriceScale") or 9)   # priceTicks -> price
        bids = ob.get("bids") or []
        asks = ob.get("asks") or []
        px = None
        if side == "buy" and asks:
            px = float(asks[0]["priceTicks"]) / ref_scale
        elif side == "sell" and bids:
            px = float(bids[0]["priceTicks"]) / ref_scale
        if not px:
            # fall back to last trade price
            tr = self.poly.call("marketdata.v1.MarketDataService/GetTrades",
                                {"symbolId": p["symbolId"], "limit": 1})["body"]
            log("no book level, trades:", json.dumps(tr)[:200])
            return None
        scale = p["baseQuantityScale"]
        step = float(p["stepSize"])
        min_qty = float(p.get("minQtyBase") or 0)
        min_notional = float(p.get("minNotionalQuote") or 0)
        if qty_base is not None:
            qty = qty_base
        else:
            qty = max(quote_usd / px, min_qty)
            if qty * px < min_notional:
                qty = min_notional / px
        # round to step (down for sells so we never exceed position)
        if step > 0:
            n = int(round(qty / step))
            qty = n * step
        if qty <= 0:
            log("qty rounds to 0, skip", symbol)
            return None
        base_qty_scaled = int(round(qty * (10 ** scale)))
        intent = {
            "symbolId": p["symbolId"],
            "side": 1 if side == "buy" else 2,
            "baseQtyScaled": str(base_qty_scaled),
            "marketIoc": {"maxSlippageBps": slippage_bps},
        }
        t0 = time.time()
        prev = self.poly.preview_order(intent)
        log("preview:", prev["status"], json.dumps(prev["body"])[:300])
        r = self.poly.create_order(intent)
        log("CreateOrder ->", r["status"], json.dumps(r["body"])[:400])
        body = r["body"] or {}
        if r["status"] != 200 or "orderId" not in body:
            return None
        order_id = body["orderId"]
        # resolve actual filled base qty from our trades
        filled = None
        for _ in range(3):
            time.sleep(1.5)
            filled = self._fill_qty(p["symbolId"], t0, side)
            if filled:
                break
        if not filled:
            filled = qty  # fall back to intended qty
        return {"orderId": order_id, "qty_base": filled, "price": px}

    def _fill_qty(self, symbol_id, t0, side):
        t = self.poly.trades()
        body = (t["body"] or {}) if isinstance(t, dict) else {}
        p = next((x for x in self.pairs().values()
                  if x["symbolId"] == symbol_id), {})
        scale = int(p.get("baseQuantityScale") or 0)
        want = "BUY" if side == "buy" else "SELL"
        best = 0.0
        for tr in (body.get("trades") or []):
            if str(tr.get("symbolId")) != str(symbol_id):
                continue
            if tr.get("side") != want:
                continue
            ts = int(tr.get("tsNs") or 0) / 1e9
            if ts < t0 - 5:
                continue
            # qtyScaled = qty * 10**baseQuantityScale -> convert back to raw base qty
            q = float(tr.get("qtyScaled") or 0) / (10 ** scale)
            if q > best:
                best = q
        return best or None

    # ---------- orchestrator ----------
    def run_all(self, deposit_eth=0.0, rounds=3):
        self.login()
        self.accept_terms()
        self.social_status()
        log("--- claim attempt")
        self.claim()
        log("--- deposit address")
        addr = self.deposit_address(ETH_SEPOLIA)
        log("ETH(Sepolia) deposit address:", addr)
        if deposit_eth and addr:
            self.deposit_eth(deposit_eth)
        log("--- balances")
        log(json.dumps(self.non_zero_balances(), indent=1)[:1500])


def main():
    pk = os.getenv("PK")
    if not pk:
        print("set PK env")
        sys.exit(1)
    bot = Bot(pk).open()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    try:
        if cmd == "status":
            bot.login()
            log(json.dumps(bot.poly.me()["body"], indent=1)[:500])
            log("claim:", json.dumps(bot.claim_status(), indent=1)[:700])
            bot.social_status()
            log("deposit addrs:", json.dumps(bot.poly.list_deposit_addresses()["body"])[:400])
            log("balances:", json.dumps(bot.non_zero_balances(), indent=1)[:1200])
        elif cmd == "login":
            bot.login()
        elif cmd == "terms":
            bot.accept_terms()
        elif cmd == "claim":
            bot.login()
            bot.claim()
            log("balances:", json.dumps(bot.non_zero_balances(), indent=1)[:1200])
        elif cmd == "social-status":
            bot.login()
            bot.social_status()
        elif cmd == "social-start":
            bot.login()
            prov = PROVIDER[sys.argv[2].lower()]
            handle = sys.argv[3] if len(sys.argv) > 3 else ""
            meth = METHOD[sys.argv[4].lower()] if len(sys.argv) > 4 else 1
            bot.social_start(prov, handle, meth)
        elif cmd == "social-ready":
            bot.login()
            bot.social_ready(PROVIDER[sys.argv[2].lower()])
        elif cmd == "x-start":
            bot.login()
            code = bot.x_verify_start(sys.argv[2])
            log("=" * 50)
            log(f"PUT THIS CODE IN THE X BIO of {sys.argv[2]}: {code}")
        elif cmd == "x-check":
            bot.login()
            log("verified:", bot.x_verify_check())
        elif cmd == "deposit-address":
            bot.login()
            cid = int(sys.argv[2]) if len(sys.argv) > 2 else ETH_SEPOLIA
            log("address:", bot.deposit_address(cid))
        elif cmd == "deposit-eth":
            bot.login()
            t = bot.deposit_eth(sys.argv[2] if len(sys.argv) > 2 else "0.01")
            log("tx:", t)
        elif cmd == "trade":
            bot.login()
            n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
            for i in range(n):
                side = "buy" if i % 2 == 0 else "sell"
                bot.market_order("BTC-USDT", side, 20.0)
                time.sleep(3)
        elif cmd == "all":
            amt = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
            bot.run_all(amt)
        else:
            log("unknown command", cmd)
    finally:
        bot.close()


if __name__ == "__main__":
    main()
