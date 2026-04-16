# Binance Futures Testnet Trading Bot

> A CLI-based Python application for placing MARKET and LIMIT orders on Binance Futures Testnet (USDT-M). Built to demonstrate clean architecture, input validation, async-aware order handling, and structured logging.

---

## 📌 Overview

This project simulates real trading interactions against Binance's Futures Testnet API. It is **not** a strategy bot — it is an engineering demonstration focused on:

- Correct API interaction patterns
- Modular, maintainable code structure
- Handling asynchronous order execution behavior
- Traceability through structured logging

---

## ⚙️ Features

- Place **MARKET** and **LIMIT** orders via CLI
- Supports **BUY** and **SELL** sides
- Input validation before any API call is made
- Logs API request, initial response, and re-fetched order status
- Post-order status verification to handle Binance's async execution model

---

## 🏗️ Project Structure

```
binance-futures-testnet-bot/
├── bot/
│   ├── client.py          # Binance API connection setup
│   ├── orders.py          # Order execution logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging configuration
├── logs/                  # Runtime logs (git-ignored)
├── sample_logs/           # Pre-captured logs for review
├── cli.py                 # CLI entry point
├── requirements.txt
└── README.md
```

- **`bot/`** — All core logic, cleanly separated by responsibility
- **`logs/`** — Generated at runtime; not committed to version control
- **`sample_logs/`** — Included for evaluation; contains real MARKET and LIMIT order outputs

---

## 🚀 Setup

**1. Clone the repository**

```bash
git clone https://github.com/your-username/binance-futures-testnet-bot.git
cd binance-futures-testnet-bot
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Create a `.env` file in the project root**

```env
API_KEY=your_binance_testnet_key
API_SECRET=your_binance_testnet_secret
```

> Get your Testnet API keys from [testnet.binancefuture.com](https://testnet.binancefuture.com)

---

## ▶️ Usage

**MARKET Order**

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**LIMIT Order**

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 80000
```

---

## 🔄 How It Works

1. User runs a CLI command with order parameters
2. `argparse` parses the inputs
3. `validators.py` validates symbol, side, type, quantity, and price
4. Order request is sent to Binance Futures API via `orders.py`
5. Initial API response is received and logged
6. A `time.sleep(1)` delay is applied to allow execution time
7. Order status is re-fetched using `futures_get_order()`
8. Final status is logged and printed to the terminal

---

## 🔥 Key Design Decisions

**Modular architecture**
Each concern — API connection, order logic, validation, logging — lives in its own module. This makes the codebase easy to extend without side effects.

**Validation before API calls**
All inputs are validated locally before any network request is made. This prevents unnecessary API calls and surfaces errors early with clear messages.

**Post-order status re-fetch**
Binance's API returns an *acknowledgement*, not a final execution result. A raw response does not tell you if the order was actually filled. To handle this correctly, the bot waits briefly and then re-fetches the order using `futures_get_order()` — giving an accurate final status (`FILLED` or `NEW`).

> This is the most important engineering decision in the project. Many implementations skip this step and incorrectly treat the acknowledgement as confirmation.

**Structured logging**
Every order cycle logs three things: the outgoing request, the initial API response, and the re-fetched status. This makes debugging straightforward and provides a full audit trail.

---

## 📊 Order Behavior

| Order Type | Expected Status | Reason |
|------------|-----------------|--------|
| MARKET | `FILLED` | Executes immediately at best available price |
| LIMIT | `NEW` | Queued; only fills when market reaches the specified price |

Both behaviors were verified through logs and the Binance Testnet UI.

---

## 📁 Logging

- Runtime logs are written to `logs/trading.log`
- Each log entry includes:
  - Outgoing request parameters
  - Initial API response
  - Re-fetched order status (`executedQty`, `avgPrice`, `status`)
- Sample logs for both MARKET and LIMIT orders are in `sample_logs/`

---

## 🛡️ Error Handling

The bot handles the following failure cases:

- Invalid order side (not `BUY` or `SELL`)
- Invalid order type (not `MARKET` or `LIMIT`)
- Non-positive quantity
- Missing price on LIMIT orders
- API errors (invalid symbol, insufficient balance, etc.)
- Network connectivity issues

---

## 🔐 Security

- API keys are stored in a `.env` file and loaded via `python-dotenv`
- `.env` is listed in `.gitignore` and never committed
- No secrets are hardcoded anywhere in the source

---

## ⚠️ Limitations

- Testnet only — not configured for live trading
- No trading strategy or signal logic
- No position tracking or portfolio management
- No risk management (stop-loss, take-profit, etc.)

---

## 🚀 Possible Improvements

- Support for Stop-Limit and OCO orders
- Real-time price validation before order placement
- Retry mechanism for transient API failures
- Web UI or dashboard for order monitoring

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core language |
| `python-binance` | Binance API interaction |
| `argparse` | CLI input parsing |
| `python-dotenv` | Secure API key management |
| `logging` | Structured log output |
