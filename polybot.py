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
CF_MAX_WAIT = 180        # seconds to let a rate-limited CF managed challenge settle


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
        self.cf_blocked = False

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
        """Navigate and wait for Cloudflare's managed challenge to clear.

        The challenge is sometimes rate-limited (`cf_chl_rc_ni`) and can take 60s+ to
        auto-settle; a plain 60s wait made `login()` click on the interstitial page and
        report a bogus 'FATAL login failed'. Wait up to CF_MAX_WAIT and expose the state
        via self.cf_blocked so callers can report something truthful.
        """
        self.cf_blocked = False
        self.page.goto(CB.BASE + path, wait_until="domcontentloaded", timeout=60000)
        t0 = time.time()
        while time.time() - t0 < CF_MAX_WAIT:
            title = self.page.title()
            if "Just a moment" not in title and "Attention Required" not in title:
                break
            time.sleep(3)
        else:
            self.cf_blocked = True
            log(f"cloudflare challenge still up after {CF_MAX_WAIT}s")
        time.sleep(wait)
        self._inject()

    def _click_login_button(self, label="Continue with MetaMask"):
        """Click a login button robustly: text locator -> button locator -> raw mouse click."""
        attempts = [
            lambda loc: loc.click(timeout=12000),
            lambda loc: loc.click(timeout=8000, force=True),
        ]
        for sel in (f'button:has-text("{label}")', f'a:has-text("{label}")',
                    f'text={label}'):
            loc = self.page.locator(sel)
            try:
                if loc.count() == 0:
                    continue
            except Exception:
                continue
            for att in attempts:
                try:
                    att(loc.first)
                    return True
                except Exception as e:
                    log(f"click {sel} failed: {str(e)[:80]}")
            bb = loc.first.bounding_box()
            if bb:
                self.page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
                return True
        return False

    def login(self):
        if self.logged_in():
            log("already logged in")
            return True
        self.go("/connect", 3)
        if getattr(self, "cf_blocked", False):
            # never reload an active challenge: wait the jitter out instead
            CB.pass_cf(self.page, 180, "-login")
            self._inject()
            if CB.is_challenge(self.page):
                log("login FAILED (cloudflare challenge)")
                return False
        clicked = self._click_login_button()
        log("clicked MetaMask" if clicked else "login button not found")
        for i in range(25):
            time.sleep(3)
            if self.logged_in() and "/connect" not in self.page.url:
                log("logged in ->", self.page.url)
                return True
            if "/connect" not in self.page.url and self.logged_in():
                return True
        if getattr(self, "cf_blocked", False):
            log("login FAILED (cloudflare challenge)")
        else:
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

    def stable_balances(self):
        """(USDT, USDC) available in the trading account -- the money entries can actually use."""
        bal = {"USDT": 0.0, "USDC": 0.0}
        for b in ((self.balances() or {}).get("balances") or []):
            s = {1: "USDT", 2: "USDC"}.get(b.get("assetId"))
            if not s:
                continue
            v = b.get("trading") or {}
            bal[s] += (int(v.get("hi", 0) or 0) * 2**64 + int(v.get("lo", 0) or 0)) / 1e18
        return bal["USDT"], bal["USDC"]

    def ensure_quote(self, min_usdt=500.0, target_usdt=1500.0, keep_usdc=200.0, min_rate=0.995):
        """Top the USDT quote balance up from idle USDC, so entries can actually fill.

        Only USDT pairs are traded, and claim rewards pay in USDC on alternate days -- without
        this swap the bot sits on a pile of USDC and errors out with INSUFFICIENT_FUNDS.
        USDC-USDT is base=USDC / quote=USDT, so selling base USDC buys the USDT we need.

        The book on USDC-USDT is thin and can sit well below par (seen: best bid 0.95, i.e. a 5%
        haircut on the whole swap), so bail out unless the top bid is at least `min_rate`."""
        usdt, usdc = self.stable_balances()
        if usdt >= min_usdt or usdc <= keep_usdc:
            return None
        want = min(target_usdt - usdt, usdc - keep_usdc)
        if want < 10:
            return None
        p = self.pairs().get("USDC-USDT")
        if not p:
            return None
        best_bid, room = self._band(self._levels(p, "sell"), "sell", 20)
        if best_bid is None or best_bid < min_rate or room < want:
            log(f"quote top-up skipped: best USDC/USDT bid {best_bid} (need >= {min_rate}), "
                f"${room:,.0f} available -- not paying a haircut to swap")
            return None
        log(f"quote top-up: USDT=${usdt:,.0f} USDC=${usdc:,.0f} -> swapping ${want:,.0f} USDC into USDT")
        r = self.market_order(symbol="USDC-USDT", side="sell", quote_usd=0, qty_base=want,
                              slippage_bps=20)
        if r:
            log(f"quote top-up done: {r['qty_base']:,.2f} USDC @ {r['price']:.5f} "
                f"(haircut {10000*(1-r['price']):.1f}bps)")
        return r

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
        try:
            from eth_utils import to_checksum_address
            to_addr = to_checksum_address(addr)      # eth_account rejects all-lowercase `to`
        except Exception:
            to_addr = addr
        tx = {"to": to_addr, "value": hex(wei)}
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

    # ---------- order book helpers: size to what the book can actually absorb ----------
    def _levels(self, p, side, depth=5):
        """[(price, qty_base)] for the side we would hit, best level first."""
        ob = self.poly.call("orderbook.v1.OrderbookService/GetOrderBook",
                            {"symbolId": p["symbolId"], "depth": depth})["body"] or {}
        ref = 10 ** int(p.get("referencePriceScale") or 9)
        scale = int(p.get("baseQuantityScale") or 0)
        raw = (ob.get("asks") if side == "buy" else ob.get("bids")) or []
        return [(float(lv["priceTicks"]) / ref, float(lv.get("qtyScaled") or 0) / (10 ** scale))
                for lv in raw if lv.get("priceTicks")]

    @staticmethod
    def _band(levels, side, band_bps):
        """(best price, notional fillable) inside a slippage band around the best level."""
        if not levels:
            return None, 0.0
        best = levels[0][0]
        limit = best * (1 + band_bps / 1e4) if side == "buy" else best * (1 - band_bps / 1e4)
        tot = 0.0
        for px, q in levels:
            if (side == "buy" and px > limit) or (side == "sell" and px < limit):
                break
            tot += px * q
        return best, tot

    def market_order(self, symbol="BTC-USDT", side="buy", quote_usd=100.0,
                     slippage_bps=None, qty_base=None):
        pairs = self.pairs()
        p = pairs.get(symbol)
        if not p:
            log("unknown symbol", symbol, "have:", list(pairs)[:20])
            return None
        levels = self._levels(p, side)
        band_narrow = float(os.environ.get("POLY_BAND_BPS", "40"))
        band_wide = float(os.environ.get("POLY_BAND_BPS_WIDE", "120"))
        min_entry = float(os.environ.get("POLY_MIN_ENTRY", "100"))
        px, room = self._band(levels, side, band_narrow)
        band_used = band_narrow
        if px is None:
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
            band_used = band_wide          # exits must get out; they are already exposed
        else:
            if room < min_entry:           # book can't absorb a full entry inside 40 bps
                _b2, room2 = self._band(levels, side, band_wide)
                if room2 >= min_entry:
                    room, band_used = room2, band_wide
                    log(f"thin book {symbol}: only ${room:,.0f} inside {band_wide:.0f}bps -> sizing down")
                else:
                    log(f"book too thin for {symbol}: ${room:,.0f}@{band_narrow:.0f}bps "
                        f"/ ${room2:,.0f}@{band_wide:.0f}bps vs min ${min_entry:.0f} -> skip")
                    return None
            qty = min(float(quote_usd), room) / px
            qty = max(qty, min_qty)
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
        slip = int(slippage_bps if slippage_bps is not None else band_used + 20)
        intent = {
            "symbolId": p["symbolId"],
            "side": 1 if side == "buy" else 2,
            "baseQtyScaled": str(base_qty_scaled),
            "marketIoc": {"maxSlippageBps": slip},
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
        # actual fill: sum EVERY trade of this order (an IOC walking a thin book fills in pieces)
        filled, avg_px = None, None
        for _ in range(3):
            time.sleep(1.5)
            filled, avg_px = self._fills(p["symbolId"], t0, side, order_id)
            if filled:
                break
        if not filled:
            filled, avg_px = qty, px   # fall back to the intended size and the book price
        try:                      # turnover ledger for the VIP 30d volume requirement
            import voltrack
            voltrack.add((avg_px or px) * filled, source="order")
        except Exception:
            pass
        return {"orderId": order_id, "qty_base": filled, "price": avg_px or px}

    def _fills(self, symbol_id, t0, side, order_id=None):
        """(total base qty, average price) across the fills of one order.

        An IOC walking a thin book produces several trade rows; keeping only the largest row
        under-reported the position (the rest stayed in the account as an untracked bag)."""
        t = self.poly.trades()
        body = (t["body"] or {}) if isinstance(t, dict) else {}
        p = next((x for x in self.pairs().values() if x["symbolId"] == symbol_id), {})
        scale = int(p.get("baseQuantityScale") or 0)
        ref = 10 ** int(p.get("referencePriceScale") or 9)
        want = "BUY" if side == "buy" else "SELL"
        qty_tot, notional = 0.0, 0.0
        for tr in (body.get("trades") or []):
            if str(tr.get("symbolId")) != str(symbol_id):
                continue
            if order_id is not None:
                oid = tr.get("orderId") if tr.get("orderId") is not None else tr.get("order_id")
                if str(oid) != str(order_id):
                    continue
            elif int(tr.get("tsNs") or 0) / 1e9 < t0 - 5:
                continue
            if str(tr.get("side") or "").upper() != want:
                continue
            q = float(tr.get("qtyScaled") or 0) / (10 ** scale)
            px = float(tr.get("priceTicks") or 0) / ref
            qty_tot += q
            notional += q * px
        if qty_tot <= 0:
            return None, None
        return qty_tot, notional / qty_tot

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
