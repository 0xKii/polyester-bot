"""Multi-pair momentum/mean-reversion strategy for Polyester testnet.

Per cycle:
  - check held positions: TP +1.2% / SL -0.8% (exit at mid)
  - pick up to `picks` random USDT pairs; momentum on 5m candles:
      up-momentum  (> +0.25% vs SMA12)  -> trend buy, $100-$200 scaled by strength
      down-momentum (< -0.25%)          -> dip buy,   $100-$150 scaled by depth
      flat                              -> skip
  - max 6 concurrent base positions (gross capped at MAX_GROSS_NOTIONAL); every entry is >= $100 notional

Size is flexible but floored at MIN_NOTIONAL ($100): the stronger the signal the
larger the order, capped at MAX_NOTIONAL_MO / MAX_NOTIONAL_DIP.

State: recon/positions.json  {pair: {symbolId, qty, entry_px, entry_ts, pnl_closed, base_asset_id}}
"""
import json, time, random, sys
from pathlib import Path

STATE = Path(__file__).resolve().parent / "recon" / "positions.json"


def log(*a):
    print(*a, file=sys.stderr, flush=True)

# USDT-quoted pairs from GetSpotConfig
USDT_PAIRS = {
    "BTC-USDT": 1, "ETH-USDT": 2, "SOL-USDT": 3, "BNB-USDT": 4,
    "XRP-USDT": 5, "DOGE-USDT": 6, "LTC-USDT": 12, "BCH-USDT": 13,
    "TRX-USDT": 14, "AVAX-USDT": 15, "POL-USDT": 16, "ETC-USDT": 17,
    "HYPE-USDT": 18,
}

MIN_NOTIONAL = 100.0        # hard floor: no entry below this
MAX_NOTIONAL_MO = 200.0     # trend buy ceiling (strong momentum)
MAX_NOTIONAL_DIP = 150.0    # dip buy ceiling (deep drop)
MOM_FULL = 0.015            # |momentum| that reaches the ceiling (1.5%)
TP_PCT = 0.012
SL_PCT = -0.008
MOMENTUM_BAND = 0.0025
MAX_POS = 6
MAX_GROSS_NOTIONAL = 700.0  # keep total open exposure under the liquid quote balance


def size_for(mom):
    """Flexible notional, floored at MIN_NOTIONAL. |mom| 0.25% -> min, >=1.5% -> max."""
    scale = min(abs(mom) / MOM_FULL, 1.0)
    ceil = MAX_NOTIONAL_MO if mom > 0 else MAX_NOTIONAL_DIP
    n = MIN_NOTIONAL + (ceil - MIN_NOTIONAL) * scale
    return float(max(MIN_NOTIONAL, min(ceil, n)))


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {}


def save_state(st):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, indent=1))


def mid_price(poly, symbol_id):
    ob = poly.call("orderbook.v1.OrderbookService/GetOrderBook",
                   {"symbolId": symbol_id, "depth": 2})["body"] or {}
    bids = ob.get("bids") or []
    asks = ob.get("asks") or []
    if bids and asks:
        b, a = float(bids[0]["priceTicks"]), float(asks[0]["priceTicks"])
        return (b + a) / 2
    if bids:
        return float(bids[0]["priceTicks"])
    if asks:
        return float(asks[0]["priceTicks"])
    return None


def candles_5m(poly, symbol_id, limit=24):
    c = poly.call("marketdata.v1.MarketDataService/GetCandles",
                  {"symbolId": symbol_id, "timeframe": 3, "limit": limit})["body"] or {}
    out = []
    for k in c.get("candles", []):
        px = k.get("close")
        if px is None:
            continue
        out.append((int(k.get("tsSec") or 0), float(px)))
    out.sort(key=lambda x: x[0])  # oldest -> newest (API returns newest first)
    return [p for _, p in out]


def momentum(px):
    """close / SMA(12 of prior candles) - 1, over the given series (oldest->newest)."""
    if len(px) < 13:
        return 0.0
    window = px[-13:-1]
    sma = sum(window) / len(window)
    if sma <= 0:
        return 0.0
    return px[-1] / sma - 1.0


def run_cycle(bot, poly, pairs_cfg, picks=5):
    st = load_state()
    actions = []
    closed = []

    # --- exits: TP/SL on held positions ---
    for pair, pos in list(st.items()):
        sym_id = pos["symbolId"]
        p = pairs_cfg.get(pair)
        if not p:
            continue
        ref = 10 ** int(p.get("referencePriceScale") or 9)
        mid = mid_price(poly, sym_id)
        if mid is None:
            continue
        px = mid / ref
        entry = pos["entry_px"]
        pct = (px / entry - 1.0) * 100 if entry else 0.0
        if pct >= TP_PCT * 100 or pct <= SL_PCT * 100:
            r = bot.market_order(symbol=pair, side="sell", quote_usd=0,
                                 qty_base=pos.get("qty"), slippage_bps=1000)
            if r is not None:
                pnl = (px - entry) * pos.get("qty", 0)
                closed.append((pair, round(pct, 2), round(pnl, 2)))
                pos["pnl_closed"] = round(pos.get("pnl_closed", 0.0) + pnl, 4)
                del st[pair]
                actions.append(f"exit {pair} {pct:+.2f}%")
            time.sleep(2)
    if st:
        save_state(st)

    held = len(st)
    gross = sum((v.get("entry_px") or 0) * (v.get("qty") or 0) for v in st.values())
    # --- entries ---
    chosen = [p for p in random.sample(list(USDT_PAIRS), min(picks, len(USDT_PAIRS))) if p not in st]
    for pair in chosen:
        if held >= MAX_POS:
            break
        sym_id = USDT_PAIRS[pair]
        p = pairs_cfg.get(pair)
        if not p:
            continue
        ref = 10 ** int(p.get("referencePriceScale") or 9)
        px_series = candles_5m(poly, sym_id)
        if not px_series:
            continue
        mid = mid_price(poly, sym_id)
        if mid is None:
            continue
        px = mid / ref
        mom = momentum(px_series)
        if mom > MOMENTUM_BAND:
            notional, tag = size_for(mom), "mo"
        elif mom < -MOMENTUM_BAND:
            notional, tag = size_for(mom), "dip"
        else:
            continue  # flat -> skip
        if gross + notional > MAX_GROSS_NOTIONAL:
            log(f"skip {pair}: gross {gross:.0f} + {notional:.0f} > cap {MAX_GROSS_NOTIONAL:.0f}")
            continue
        r = bot.market_order(symbol=pair, side="buy", quote_usd=notional, slippage_bps=500)
        if r is not None:
            held += 1
            gross += notional
            st[pair] = {"symbolId": sym_id, "qty": r["qty_base"], "entry_px": px,
                        "entry_ts": time.time(), "tag": tag, "pnl_closed": 0.0,
                        "orderId": r.get("orderId")}
            save_state(st)
            actions.append(f"buy {pair} {notional:.0f}U qty={r['qty_base']:.6g} mom={mom*100:+.2f}% @{px:.2f}")
        time.sleep(2)

    # report
    open_pos = ", ".join(f"{k}({v.get('tag')})" for k, v in st.items()) or "-"
    tot_pnl = sum(v.get("pnl_closed", 0.0) for v in st.values()) + sum(c[2] for c in closed)
    log(f"strat | open=[{open_pos}] | closed={closed if closed else '-'} | actions={actions if actions else '-'} | cumPnL={tot_pnl:+.3f}")
    return {"actions": actions, "closed": closed}
