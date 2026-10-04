#!/usr/bin/env python3
"""Variety + P&L-aware trading driver.
Usage: trade_var.py [picks]   (picks = candidate pairs to scan per cycle, default 6)
Intermediate logs -> stderr; one summary line -> stdout (cron-friendly).
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if not os.environ.get("PK"):
    sys.exit("set PK env var (wallet private key), e.g. via .env")

import polybot
polybot.log = lambda *a: print(*a, file=sys.stderr, flush=True)
from polybot import Bot
from poly import Poly
import strat

# argv[1] is accepted for backwards compatibility only: the cycle now scans every USDT pair
# and ranks candidates by signal strength, so a "picks" count is meaningless.
picks = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None


def main():
    bot = Bot(os.environ["PK"]).open()
    if not bot.login():
        why = "cloudflare challenge" if getattr(bot, "cf_blocked", False) else "login failed"
        print(f"polyester-trade | FATAL {why}", file=sys.stderr)
        sys.exit(1)
    poly = bot.poly
    pairs_cfg = bot.pairs()

    before = time.time()
    res = strat.run_cycle(bot, poly, pairs_cfg)
    acts = res.get("actions") or []
    closed = res.get("closed") or []

    # cumulative P&L across all closed positions
    st = strat.load_state()
    open_pos = [k for k in st]
    cum_pnl = sum(v.get("pnl_closed", 0.0) for v in st.values())
    # estimate open P&L
    opnl = 0.0
    for pair, pos in st.items():
        p = pairs_cfg.get(pair)
        if not p:
            continue
        ref = 10 ** int(p.get("referencePriceScale") or 9)
        mid = strat.mid_price(poly, pos["symbolId"])
        if not mid:
            continue
        px = mid / ref
        opnl += (px - pos.get("entry_px", px)) * pos.get("qty", 0)
    print(f"polyester-trade | open={len(open_pos)}[{','.join(open_pos)}] | "
          f"cumPnL={cum_pnl:+.3f} openPnL={opnl:+.3f} totPnL={cum_pnl+opnl:+.3f} | "
          f"acts={len(acts)} closed={len(closed)}")
    for a in acts:
        print(f"  - {a}")
    bot.close()


if __name__ == "__main__":
    main()
