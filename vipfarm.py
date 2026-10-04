#!/usr/bin/env python3
"""Volume farming for the Polyester VIP tiers.

VIP 1 needs >= $100K 30-day volume AND >= $50K avg portfolio (VIP 2: $500K / $100K).
This module pushes turnover through market round-trips (buy -> sell the same base qty) on the
tightest, deepest USDT pair, and keeps a running ledger so progress is visible.

Usage:
  vipfarm.py probe [topN]              # measure spread + depth per pair, pick the farm pair
  vipfarm.py run [rounds] [notional] [pair]   # round-trips (default: 10 rounds, $500, auto pair)
"""
import json, os, sys, time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voltrack

STATE = Path(__file__).resolve().parent / "recon" / "volume.json"
TARGET_30D = float(os.getenv("VIP_TARGET_VOLUME", str(voltrack.TARGET_30D)))
CANDIDATE_PAIRS = ("BTC-USDT", "ETH-USDT", "SOL-USDT", "BNB-USDT", "ETH-USDC", "SOL-USDC")


def load_state():
    return voltrack.load()


def save_state(st):
    voltrack.save(st)


def probed(poly, pairs_cfg, names=CANDIDATE_PAIRS):
    """(pair, spread_bps, notional_within_30bps, mid) for each candidate."""
    out = []
    for name in names:
        p = pairs_cfg.get(name)
        if not p:
            continue
        ob = poly.call("orderbook.v1.OrderbookService/GetOrderBook",
                       {"symbolId": p["symbolId"], "depth": 5})["body"] or {}
        ref = 10 ** int(p.get("referencePriceScale") or 9)
        bscale = 10 ** int(p["baseQuantityScale"])
        bids, asks = ob.get("bids") or [], ob.get("asks") or []
        if not bids or not asks:
            continue
        bb = float(bids[0]["priceTicks"]) / ref
        ba = float(asks[0]["priceTicks"]) / ref
        mid = (bb + ba) / 2
        spread_bps = (ba - bb) / mid * 1e4
        def size_within(levels, tol=0.0030):
            return sum(float(lv["priceTicks"]) / ref * (int(lv["qtyScaled"]) / bscale)
                       for lv in levels if abs(float(lv["priceTicks"]) / ref / mid - 1) <= tol)
        out.append((name, spread_bps, size_within(bids), size_within(asks), mid))
        time.sleep(0.2)
    out.sort(key=lambda r: (r[1], -min(r[2], r[3])))
    return out


def cmd_probe(poly, pairs_cfg, topn=6):
    rows = probed(poly, pairs_cfg)
    print(f"{'pair':12s} {'spread':>8s} {'bids<=0.3%':>12s} {'asks<=0.3%':>12s}")
    for name, sp, b, a, mid in rows[:topn]:
        print(f"{name:12s} {sp:7.1f}b {b:12,.0f} {a:12,.0f}")
    if rows:
        total_bps = 0.0
        print(f"\ncheapest pair: {rows[0][0]} (spread {rows[0][1]:.1f} bps)")


def cmd_run(bot, poly, pairs_cfg, rounds=10, notional=500.0, pair=None):
    rows = probed(poly, pairs_cfg)
    if pair is None:
        pair = rows[0][0] if rows else "BTC-USDT"
    p = pairs_cfg.get(pair)
    if not p:
        print(f"unknown pair {pair}")
        return
    print(f"farming {pair}: {rounds} round-trips x ${notional:.0f}/leg "
          f"(target ${TARGET_30D:,.0f} — ledger fills automatically from every order)")
    made = 0
    start = time.time()
    for i in range(rounds):
        r = bot.market_order(symbol=pair, side="buy", quote_usd=notional, slippage_bps=800)
        if r is None:
            print(f"  round {i+1}: BUY failed, stopping")
            break
        qty = r["qty_base"]
        r2 = bot.market_order(symbol=pair, side="sell", quote_usd=0, qty_base=qty, slippage_bps=800)
        if r2 is None:
            print(f"  round {i+1}: SELL failed (holding {qty:g} {pair.split('-')[0]})")
        made += 1
        snap = voltrack.snapshot()
        print(f"  round {i+1}/{rounds}: turnover ${notional*2:,.0f} | today ${snap['today']:,.0f} | "
              f"30d ${snap['total']:,.0f} ({snap['pct']:.1f}%) | {time.time()-start:.0f}s")
        time.sleep(1.0)
    print(f"done: {made} rounds (~${made*notional*2:,.0f} turnover). {voltrack.line()}")


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "probe"
    if not os.environ.get("PK"):
        sys.exit("set PK env var (wallet private key), e.g. via .env")
    from polybot import Bot
    bot = Bot(os.environ["PK"]).open()
    if not bot.login():
        sys.exit("login failed")
    try:
        pairs_cfg = bot.pairs()
        if cmd == "probe":
            cmd_probe(bot.poly, pairs_cfg, int(args[1]) if len(args) > 1 else 6)
        elif cmd == "status":
            print(voltrack.line())
        elif cmd == "run":
            rounds = int(args[1]) if len(args) > 1 else 10
            notional = float(args[2]) if len(args) > 2 else 500.0
            pair = args[3] if len(args) > 3 else None
            cmd_run(bot, bot.poly, pairs_cfg, rounds, notional, pair)
        else:
            print(__doc__)
    finally:
        bot.close()


if __name__ == "__main__":
    main()
