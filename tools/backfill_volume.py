#!/usr/bin/env python3
"""Rebuild the turnover ledger (recon/volume.json) from the exchange's own transfer history.

`voltrack.add()` records filled orders live, but the ledger only knows about orders placed
while the bot was running. The exchange keeps every fill as a TRADE_QUOTE transfer, so we can
rebuild the per-day turnover from scratch — the 30-day VIP volume number is then the truth,
not just what this process happened to see.

Usage:  /usr/bin/python3 tools/backfill_volume.py [--dry]
"""
import json, os, sys, time
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
os.chdir(BASE)
for line in (BASE / ".env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v.strip())

from polybot import Bot  # noqa: E402

VOL = BASE / "recon" / "volume.json"
DRY = "--dry" in sys.argv


def u128(x):
    if isinstance(x, dict):
        return (int(x.get("hi", 0) or 0) * 2**64 + int(x.get("lo", 0) or 0)) / 1e18
    return float(x or 0)


def code_name(c):
    if isinstance(c, dict):
        c = c.get("code", 0)
    if isinstance(c, str):
        return c
    return {1000: "DEPOSIT", 1010: "MAKER_FEE", 1011: "TAKER_FEE", 1030: "INTERNAL_TRANSFER",
            1031: "TRADE_BASE", 1032: "TRADE_QUOTE", 1041: "REBATE"}.get(int(c), str(c))


def main():
    bot = Bot(os.environ["PK"]).open()
    if not bot.login():
        sys.exit("login failed")
    poly = bot.poly

    turnover, orders = defaultdict(float), defaultdict(int)
    tok, pages = None, 0
    while pages < 25:
        req = {"subaccountId": "0", "limit": 200, "reversed": True}
        if tok:
            req["pageToken"] = tok
        r = poly.call("ledger.read.v1.LedgerReadService/ListTransfers", req)
        body = r["body"] or {}
        rows = body.get("transfers") or []
        if not rows:
            break
        for x in rows:
            if code_name(x.get("transferCode")) != "TRADE_QUOTE":
                continue
            ts = int(x.get("tsUs") or 0) / 1e6
            day = time.strftime("%Y-%m-%d", time.localtime(ts))
            turnover[day] += abs(u128(x.get("amountE18")))
            orders[day] += 1
        tok = body.get("nextPageToken")
        pages += 1
        if not tok:
            break
    bot.close()

    st = {"days": {d: round(v, 2) for d, v in sorted(turnover.items())},
          "total_turnover": round(sum(turnover.values()), 2),
          "total_orders": sum(orders.values()),
          "rounds": sum(orders.values())}
    print(json.dumps(st, indent=1))
    if DRY:
        print("(dry run, not written)")
        return
    VOL.parent.mkdir(parents=True, exist_ok=True)
    VOL.write_text(json.dumps(st, indent=1))
    print(f"wrote {VOL}")


if __name__ == "__main__":
    main()
