#!/usr/bin/env python3
"""Daily Polyester routine: optional claim + trading rounds.
Usage: daily.py [claim] [rounds]
  - 'claim' arg: attempt daily claim (only fires if CLAIM_AVAILABLE)
  - rounds: trading rounds (default 3)
Exit 0 on success. Intermediate logs -> stderr; one summary line -> stdout (for cron).
"""
import os, sys, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if not os.environ.get("PK"):
    sys.exit("set PK env var (wallet private key), e.g. via .env")

# route all intermediate logs to stderr so stdout carries only the final summary
import polybot
polybot.log = lambda *a: print(*a, file=sys.stderr, flush=True)

from polybot import Bot, ETH_SEPOLIA
from poly import Poly

args = [a for a in sys.argv[1:]]
want_claim = "claim" in args
args = [a for a in args if a != "claim"]
rounds = int(args[0]) if args else 3


def main():
    bot = Bot(os.environ["PK"]).open()
    if not bot.login():
        why = "cloudflare challenge" if getattr(bot, "cf_blocked", False) else "login failed"
        print(f"polyester-daily | FATAL {why}", file=sys.stderr)
        sys.exit(1)

    claim_state = "n/a"
    if want_claim:
        st = bot.claim_status()
        claim_state = st.get("state")
        if claim_state == "CLAIM_AVAILABLE":
            bot.claim()
        else:
            polybot.log(f"claim skipped: {claim_state}")

    # varied multi-pair strategy cycle (momentum/dip entries + TP/SL exits)
    import strat
    pairs_cfg = bot.pairs()
    try:
        bot.ensure_quote()        # claim pays USDC on alternate days; entries need USDT
    except Exception as e:
        polybot.log("ensure_quote failed:", repr(e))
    res = strat.run_cycle(bot, bot.poly, pairs_cfg)
    st = bot.claim_status()
    bal = bot.non_zero_balances()
    assets = sorted({b.get("assetId") for b in bal})
    print(f"polyester-daily | acct={bot.wallet.address[:6]}..{bot.wallet.address[-4:]} | "
          f"claim={st.get('state')} reset={st.get('resetAt')} | "
          f"actions={res['actions'] if res['actions'] else '-'} closed={res['closed'] if res['closed'] else '-'} | "
          f"assets={assets}")
    try:
        import voltrack
        print(voltrack.line())
        import vipplan
        print(vipplan.line(vipplan.plan(bot)))
    except Exception:
        pass
    bot.close()


if __name__ == "__main__":
    main()
