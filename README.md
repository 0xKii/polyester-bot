# Polyester Testnet Bot

Automates the [Polyester](https://testnet.polyester.com) testnet campaign for a single
wallet: SIWE login, daily reward claim, and varied multi-pair spot trading.

> Testnet/personal-use tool. Your private key stays in `.env` (gitignored) -- never commit it.

## What it does

- **Login** -- injects an EIP-1193 (MetaMask-compatible) provider and signs SIWE with a local PK.
- **Claim** -- daily "Testnet Daily Claims" paper-asset reward (UTC daily reset, needs verified social).
- **Social verify** -- registers an X/Discord handle and prints the challenge code for the bio
  (the code must be placed in the profile manually; the bot then polls until verified).
- **Trade** -- momentum / mean-reversion strategy across 13 USDT pairs with TP/SL and P&L tracking.

## Requirements

- Python 3.10+ -- `pip install -r requirements.txt` (playwright, requests, eth-account)
- Google Chrome running on an Xvfb display (default `:99`) with remote debugging on port `9333`.
  The bot **attaches over CDP** -- do **not** launch Chrome through Playwright, Cloudflare will not pass.

## Setup

```bash
cp .env.example .env      # then edit PK=0x<private_key>
pip install -r requirements.txt

# display + real Chrome with CDP
Xvfb :99 -screen 0 1920x1080x24 -ac &
DISPLAY=:99 google-chrome --remote-debugging-port=9333 --user-data-dir=./profile2 &
```

## Commands

```bash
python3 polybot.py status            # account id, claim state, social state, balances
python3 polybot.py login             # wallet connect + SIWE signature
python3 polybot.py claim             # daily reward claim
python3 polybot.py terms             # AcceptTerms (required before deposit address)
python3 polybot.py x-start <handle>  # register X handle, print challenge code
python3 polybot.py x-check           # poll verification after the code is in the bio
python3 polybot.py deposit-address   # get/create a deposit address (ETH Sepolia)
python3 polybot.py deposit-eth <amt> # send Sepolia ETH to the deposit address
python3 polybot.py trade [rounds]    # quick BTC-USDT alternating buy/sell (smoke test)

./trade_var.py [picks]               # one strategy cycle  (default: scan 6 pairs)
./daily.py claim [picks]             # daily routine: claim + one strategy cycle
```

## Strategy (`strat.py`)

Runs on the 13 USDT-quoted pairs. Each cycle:

1. **Exit** held positions at take-profit / stop-loss (exits at mid price).
2. **Rank** every USDT-quoted pair by 5-minute momentum vs SMA12:
   - `> +0.12%` -> trend buy, **$100-$200** scaled by momentum strength
   - `< -0.12%` -> dip buy, **$100-$150** scaled by drop depth
   - flat -> skip
3. **Enter** the strongest signals first, at most **4** new entries per cycle.
4. **Rotate**: when slots/notional are full, a position down >=0.5% is closed to make room
   for a signal >=0.8% (keeps capital working instead of idling for hours).
5. Max **10** concurrent positions; gross exposure capped at **$2200**.

Order size is flexible but **floored at $100** per entry: `MIN_NOTIONAL + (ceiling - MIN) * min(|mom| / 1.5%, 1)`
(see `size_for()` in `strat.py`). A weak 0.12% signal still buys $100; a >=1.5% signal buys the ceiling.

| Param | Value |
|---|---|
| Min notional (floor) | $100 |
| Max notional (trend buy) | $200 |
| Max notional (dip buy) | $150 |
| Max gross exposure | $2200 |
| Max positions | 10 |
| Max new entries / cycle | 4 |
| Rotation: min signal | +-0.8% |
| Rotation: weakest must be down | -0.5% |
| Take profit | +0.9% |
| Stop loss | -0.6% |
| Momentum band | +/-0.12% |

State is kept in `recon/positions.json` (gitignored).

## Scheduled runs (example)

`polyester_daily.sh` -- daily `claim` + strategy cycle (also acts as a heartbeat).
`polyester_trade.sh` -- hourly strategy cycle, **quiet unless something happened**
(empty stdout = nothing delivered; non-zero exit alerts).

Both wrappers load `PK` from `.env`.

## Layout

- `polybot.py` -- bot core: login, claim, social, orders, CLI
- `poly.py` -- ConnectRPC transport (in-page `fetch`, JSON encoding)
- `strat.py` -- multi-pair strategy + P&L / position state
- `trade_var.py` / `daily.py` -- drivers (one line to stdout, logs to stderr)
- `cdp_browser.py` -- real-Chrome launcher + CDP attach + Cloudflare challenge handling
- `w3wallet.py` -- signing bridge (`personal_sign`, EIP-712, raw tx)
- `wallet_provider.js` -- injected EIP-1193 provider
- `proto/API.md` -- decoded ConnectRPC API schemas

## Notes

- Auth token lives in the `polyester_auth_token` cookie; API calls are in-page `fetch`
  with `authorization: Bearer <token>`.
- All ints are scaled: `price = priceTicks / 10**referencePriceScale` (9),
  `qty = qtyScaled / 10**baseQuantityScale`.
- **Candles come newest-first** -- sort by timestamp before any momentum math.
- Daily claim is blocked until X or Discord is verified (`SOCIAL_VERIFICATION_REQUIRED`).
