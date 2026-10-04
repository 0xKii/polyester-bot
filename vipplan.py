"""VIP tier planning — how the bot sizes and paces itself to earn a fee tier.

Ki: chase VIP 1 first; if the balance grows enough for VIP 2, go for that too. So the
strategy can't use fixed notional constants any more: size follows the *portfolio* (claim
rewards keep topping it up) and the *volume gap* to the next tier.

Tier requirement is an AND of two 30-day numbers (from the Fee Schedule):
    VIP 1  $100K volume / $50K avg portfolio
    VIP 2  $500K / $100K
    VIP 3  $1M   / $250K
    VIP 4  $5M   / $500K

What this module does every cycle:
  - values the portfolio (trading + funding balances, `t*` variants priced off their base)
  - reads the turnover ledger (voltrack) for the 30d volume and the recent daily pace
  - picks the tier worth chasing (the first one not satisfied on BOTH bars)
  - derives order notional + gross cap from the *liquid stable* balance, and a pace
    multiplier that only ever pushes volume UP (never throttles below the base size)

Volume alone never moves the tier: the portfolio bar is the gate, so there is no point
farming sprints. This keeps the bot trading normally while the daily claims grow the balance.
"""
import json, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
LEDGER = BASE / "recon" / "volume.json"

TIERS = [  # (tier, 30d volume, avg portfolio)
    (1, 100_000.0, 50_000.0),
    (2, 500_000.0, 100_000.0),
    (3, 1_000_000.0, 250_000.0),
    (4, 5_000_000.0, 500_000.0),
]
VOL_BUFFER = 1.15        # aim 15% above the bar so a slow day doesn't drop us under it
NOTIONAL_LO = 300.0      # hard floor per entry
NOTIONAL_HI_BASE = 600.0  # base ceiling at the current balance
NOTIONAL_HI_MAX = 5_000.0
GROSS_MIN = 3_000.0
LIQUID_FRACTION = 0.10   # per-entry ceiling as a share of liquid stablecoin
GROSS_FRACTION = 0.80    # total open exposure vs liquid stablecoin
PACE_WINDOW = 7          # days used for the current trading pace

_deps_cache = {"ts": 0.0, "amap": None, "px": None}


def log(*a):
    print("vipplan |", *a, file=sys.stderr, flush=True)


def _u128(x):
    if isinstance(x, dict):
        return (int(x.get("hi", 0) or 0) * 2**64 + int(x.get("lo", 0) or 0)) / 1e18
    return float(x or 0)


def asset_map(bot):
    cfg = bot.spot_config() or {}
    return {int(a["ledgerId"]): a["asset"] for a in (cfg.get("assets") or []) if a.get("ledgerId") is not None}


def prices(bot):
    """{base: last price} for every *-USDT pair from ListMarketOverview."""
    mo = bot.poly.call("marketoverview.v1.MarketOverviewService/ListMarketOverview", {})["body"] or {}
    names = _names(bot)
    px = {}
    for m in (mo.get("markets") or []):
        name = names.get(m.get("symbolId"), "")
        if name.endswith("-USDT"):
            last = float(m.get("lastPriceTicks") or 0) / 1e9
            if last:
                px[name.split("-")[0]] = last
    return px


_symbol_names = {}


def _names(bot):
    global _symbol_names
    if not _symbol_names:
        _symbol_names = {p["symbolId"]: n for n, p in bot.pairs().items()}
    return _symbol_names


def equity(bot, amap=None, px=None):
    """Portfolio value in USDT: every balance (trading + funding), `t*` priced off its base."""
    amap = amap if amap is not None else asset_map(bot)
    px = px if px is not None else prices(bot)
    total = 0.0
    for b in ((bot.balances() or {}).get("balances") or []):
        amt = _u128(b.get("trading")) + _u128(b.get("funding"))
        if amt <= 0:
            continue
        sym = amap.get(b.get("assetId")) or ""
        price = 1.0 if sym in ("USDC", "USDT") else px.get(sym) or px.get(sym.lstrip("t") if sym.startswith("t") else sym)
        if price:
            total += amt * price
    return total


def liquid_stable(bot, amap=None):
    """USDT + USDC available to trade — what actually caps order size and exposure."""
    amap = amap if amap is not None else asset_map(bot)
    out = 0.0
    for b in ((bot.balances() or {}).get("balances") or []):
        if amap.get(b.get("assetId")) in ("USDC", "USDT"):
            out += _u128(b.get("trading")) + _u128(b.get("funding"))
    return out


def ledger_days():
    try:
        return (json.loads(LEDGER.read_text()).get("days") or {})
    except Exception:
        return {}


def volume_30d(days=30):
    d = ledger_days()
    return sum(list(d.values())[-days:])


def pace(window=PACE_WINDOW):
    vals = list(ledger_days().values())[-window:]
    return sum(vals) / len(vals) if vals else 0.0


def plan(bot, amap=None, px=None):
    amap = amap if amap is not None else asset_map(bot)
    px = px if px is not None else prices(bot)
    eq = equity(bot, amap, px)
    liq = liquid_stable(bot, amap)
    v30 = volume_30d()
    p = pace()

    chase = None
    for tier, vol, port in TIERS:
        if v30 >= vol and eq >= port:
            continue
        chase = (tier, vol, port)
        break
    if chase is None:
        chase = TIERS[-1]
    daily_target = chase[1] / 30.0 * VOL_BUFFER
    mult = min(2.0, max(1.0, daily_target / max(p, 1.0)))   # only ever pushes volume up

    hi_mo = min(NOTIONAL_HI_MAX, max(NOTIONAL_HI_BASE, LIQUID_FRACTION * liq * mult))
    hi_dip = max(NOTIONAL_LO, hi_mo * 0.75)
    gross_cap = max(GROSS_MIN, GROSS_FRACTION * liq)
    return {
        "equity": eq, "liquid": liq, "vol30": v30, "pace": p,
        "chase_tier": chase[0], "chase_vol": chase[1], "chase_port": chase[2],
        "daily_target": daily_target, "mult": mult,
        "notional_lo": NOTIONAL_LO, "notional_hi_mo": hi_mo, "notional_hi_dip": hi_dip,
        "gross_cap": gross_cap, "max_pos": 10,
    }


def line(p):
    """One-line progress report (stderr for trade runs, stdout for the daily heartbeat)."""
    done = "volume OK" if p["vol30"] >= p["chase_vol"] else f"volume {p['vol30']/p['chase_vol']*100:.0f}%"
    port_gap = max(0.0, p["chase_port"] - p["equity"])
    return (f"vip | chase VIP{p['chase_tier']} (${p['chase_vol']/1000:.0f}k vol / ${p['chase_port']/1000:.0f}k port) | "
            f"equity=${p['equity']:,.0f} (need ${port_gap:,.0f} more) | 30d vol ${p['vol30']:,.0f} [{done}] | "
            f"pace ${p['pace']:,.0f}/d vs target ${p['daily_target']:,.0f}/d (x{p['mult']:.2f}) | "
            f"size ${p['notional_lo']:.0f}-{p['notional_hi_mo']:.0f} | gross cap ${p['gross_cap']:,.0f}")
