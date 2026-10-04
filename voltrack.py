"""Turnover ledger for the VIP volume requirement.

Every filled order (strategy or farm) adds its quote notional here, so the 30-day volume
requirement is tracked from real trading activity instead of a synthetic counter.

State: recon/volume.json (gitignored) — cumulative turnover per day + lifetime + source split.
"""
import json, time
from pathlib import Path

STATE = Path(__file__).resolve().parent / "recon" / "volume.json"
TARGET_30D = 100000.0     # VIP 1: >= $100K 30-day volume


def _today():
    return time.strftime("%Y-%m-%d")


def load():
    if STATE.exists():
        try:
            st = json.loads(STATE.read_text())
        except Exception:
            st = {}
    else:
        st = {}
    st.setdefault("days", {})
    st.setdefault("total_turnover", 0.0)
    st.setdefault("rounds", 0)
    st.setdefault("sources", {})
    return st


def save(st):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, indent=1))


def add(usd, source="order", rounds=0):
    """Record quote notional of a filled order. Never raises — tracking must not break trading."""
    try:
        usd = float(usd)
        if usd <= 0:
            return None
        st = load()
        st["days"][_today()] = st["days"].get(_today(), 0.0) + usd
        st["total_turnover"] = st.get("total_turnover", 0.0) + usd
        st["rounds"] = st.get("rounds", 0) + rounds
        st["sources"][source] = st["sources"].get(source, 0.0) + usd
        st["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        save(st)
        return st
    except Exception:
        return None


def snapshot():
    st = load()
    today = st["days"].get(_today(), 0.0)
    total = st.get("total_turnover", 0.0)
    return {"today": today, "total": total, "target": TARGET_30D,
            "pct": total / TARGET_30D * 100 if TARGET_30D else 0.0,
            "sources": st.get("sources", {}), "rounds": st.get("rounds", 0)}


def line():
    s = snapshot()
    return (f"volume | today=${s['today']:,.0f} | 30d=${s['total']:,.0f} "
            f"({s['pct']:.1f}% of ${s['target']:,.0f}) | sources={s['sources']}")
