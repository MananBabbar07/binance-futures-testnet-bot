# Binance Futures Testnet Trading Bot

> A CLI-based Python application for placing MARKET and LIMIT orders on Binance Futures Testnet (USDT-M).  
> Built for the **Primetrade.ai AI Agent Developer Assessment**.

---

## 📌 Overview

This application interacts with the Binance Futures Testnet API to place real orders in a simulated trading environment. The focus is on clean architecture, safe input handling, and reliable logging — not strategy logic.

**What it demonstrates:**
- Correct usage of the Binance Futures REST API via `python-binance`
- Separation of concerns across CLI, validation, API client, and order logic
- Handling of Binance's asynchronous order execution (acknowledgement ≠ final status)
- Structured, readable logging for debugging and auditability

---

## 🏗️ Project Structure

```
binance-futures-testnet-bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API client setup and connection
│   ├── orders.py          # Order placement and status verification
│   ├── validators.py      # Input validation logic
│   └── logging_config.py  # Log formatting and file handler setup
├── logs/                  # Runtime log files (auto-created, git-ignored)
├── sample_logs/           # Pre-captured logs for review
│   ├── market_order.log
│   └── limit_order.log
├── cli.py                 # CLI entry point (argparse)
├── .env.example           # Example environment variable file
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/binance-futures-testnet-bot.git
cd binance-futures-testnet-bot
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API credentials

Create a `.env` file in the project root:

```env
API_KEY=your_binance_testnet_api_key
API_SECRET=your_binance_testnet_api_secret
```

> **Get your Testnet credentials at:** [testnet.binancefuture.com](https://testnet.binancefuture.com)  
> Register → Log in → API Management → Generate Key

---

## ▶️ Usage

### MARKET Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### LIMIT Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 80000
```

### All Available Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--symbol` | ✅ | Trading pair (e.g., `BTCUSDT`) |
| `--side` | ✅ | `BUY` or `SELL` |
| `--type` | ✅ | `MARKET` or `LIMIT` |
| `--quantity` | ✅ | Order size (must be positive) |
| `--price` | LIMIT only | Limit price (required for LIMIT orders) |

---

## 🖥️ Sample Output

```
========================================
  ORDER SUMMARY
========================================
  Symbol   : BTCUSDT
  Side     : BUY
  Type     : MARKET
  Quantity : 0.001
========================================

✅ Order placed successfully.

  Order ID     : 3718937291
  Status       : FILLED
  Executed Qty : 0.001
  Avg Price    : 83412.50

Log saved to: logs/trading.log
```

---

## 🔄 How It Works

1. User runs `cli.py` with order parameters
2. `argparse` parses and surfaces all arguments
3. `validators.py` validates all inputs locally (before any API call)
4. `client.py` initializes the authenticated Binance Futures client
5. `orders.py` sends the order and logs the initial API response
6. A short delay (`time.sleep(1)`) allows the exchange to process the order
7. Order status is **re-fetched** using `futures_get_order()` for the true final state
8. Final result is printed to the terminal and written to the log file

> **Why re-fetch the order?**  
> Binance's API returns an acknowledgement immediately — not the final execution result. A MARKET order may show `NEW` in the first response and `FILLED` a moment later. Re-fetching is the correct way to confirm actual execution status.

---

## 📊 Order Behavior

| Order Type | Typical Final Status | Explanation |
|------------|---------------------|-------------|
| MARKET | `FILLED` | Executes immediately at best available price |
| LIMIT | `NEW` | Queued; only fills when market reaches the set price |

Both behaviors verified via logs and Binance Testnet UI.

---

## 📁 Logging

Logs are written to `logs/trading.log` and include three entries per order cycle:

| Log Entry | Contents |
|-----------|----------|
| **Request** | symbol, side, type, quantity, price |
| **Initial Response** | orderId, raw status from API |
| **Final Status** | re-fetched status, executedQty, avgPrice |

Sample logs for both order types are included in `sample_logs/`.

**Log format example:**
```
2025-07-10 14:22:01 INFO  Placing order: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.001}
2025-07-10 14:22:01 INFO  Initial response: {'orderId': 3718937291, 'status': 'NEW', ...}
2025-07-10 14:22:02 INFO  Final status: {'orderId': 3718937291, 'status': 'FILLED', 'executedQty': '0.001', 'avgPrice': '83412.5'}
```

---

## 🛡️ Validation & Error Handling

**Input validation (before API call):**
- `side` must be `BUY` or `SELL`
- `type` must be `MARKET` or `LIMIT`
- `quantity` must be a positive number
- `price` is required when `type` is `LIMIT`

**Runtime error handling:**
- Invalid trading symbol → caught and logged with message
- API authentication failure → clear error printed, full trace logged
- Network timeout or connection failure → exception caught, logged, user notified
- Unexpected API errors → logged with full response for debugging

---

## 🔐 Security

- API credentials stored in `.env` (never hardcoded)
- `.env` is listed in `.gitignore` — not committed to version control
- `.env.example` included to show expected format without exposing secrets

---

## ⚠️ Assumptions & Limitations

- Designed for **Binance Futures Testnet only** — not production-safe
- Testnet base URL used: `https://testnet.binancefuture.com`
- No trading strategy, risk management, or position tracking
- Quantity precision is not auto-adjusted for symbol lot size filters (manual input assumed correct)
- `time.sleep(1)` is a reasonable delay for testnet; production would use WebSocket order events

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| `python-binance` | Binance Futures API client |
| `argparse` | CLI input parsing |
| `python-dotenv` | Secure credential loading |
| `logging` | Structured log output to file |

---

## 🚀 Possible Improvements

- Stop-Limit / OCO order support
- Real-time price validation before limit order placement
- Retry logic with exponential backoff for transient API failures
- Interactive CLI mode (menu-driven prompts via `Typer` or `Rich`)
- WebSocket-based order status updates instead of polling
