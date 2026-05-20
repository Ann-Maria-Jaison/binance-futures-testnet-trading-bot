# 🚀 Binance Futures Testnet Trading Bot

An enterprise-grade, highly structured, and production-ready Python Command Line Interface (CLI) application for placing orders on **Binance Futures Testnet (USDT-M)**. Designed with clean code architecture, absolute security practices, robust validations, and comprehensive dual-channel logging.

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [Project Structure](#-project-structure)
4. [Prerequisites](#-prerequisites)
5. [Setup & Configuration](#-setup--configuration)
6. [Command Usage & Examples](#-command-usage--examples)
7. [Logging Architecture](#-logging-architecture)
8. [Architecture & Design Decisions](#-architecture--design-decisions)
9. [Underlying Assumptions](#-underlying-assumptions)

---

## 🔍 Project Overview

This command line trading assistant allows algorithmic traders, developers, and researchers to place immediately executable or trigger-based orders on the **Binance Futures Testnet (USDT-M Margined Contracts)**.

By leveraging python-binance, proper exception structures, and absolute strict data verification schemas, the system guarantees that API calls are error-minimized and transparently traced through a high-fidelity logging framework.

---

## ✨ Key Features

- **Standard Order Types**:
  - `MARKET`: Instant order execution matching current liquidity.
  - `LIMIT`: Pending order placed at a precise price threshold utilizing a pre-configured `GTC` (Good Till Cancelled) execution instruction.
- **Bonus Trigger Order Type**:
  - `STOP_MARKET`: Automatically triggers a Market order the second prices touch a custom `--stopPrice`.
- **Bidirectional Support**: Supports both long entry/exit (`BUY`) and short entry/exit (`SELL`) sides.
- **Bulletproof Multi-Stage Validations**: Checks asset symbol lengths, valid trade directions, boundary constraints on amounts (`quantity > 0`), and dynamic condition validations (e.g., verifying that a limit price is present only when `LIMIT` is selected).
- **Dual-Channel Logging**: Seamlessly logs events to a localized rotating log file (`logs/trading.log`) and highlights executions in standard output.
- **Secure Configuration**: Uses `.env` standard files to manage sensitive API credentials, protecting production keys.

---

## 📂 Project Structure

The project has been structured precisely according to the required folder architecture:

```text
trading_bot/
│
├── bot/
│   ├── __init__.py           # Package initializer, exposing clean sub-module APIs
│   ├── client.py             # Credentials validation and Binance API Client bootstrap
│   ├── orders.py             # Futures order executor with explicit logging and error wrappers
│   ├── validators.py         # Type and boundary validator functions for all parameters
│   └── logging_config.py     # Stream/file rotating log engine configuration
│
├── logs/
│   └── trading.log           # Persisted log file (generated automatically on startup)
│
├── cli.py                    # Main executable entry point with argparse implementation
├── README.md                 # Project documentation and user manual
├── requirements.txt          # Explicit third-party Python package dependencies
├── .env.example              # Template configuration for environment secrets
└── .gitignore                # Optimized patterns to prevent caching, venvs, and logs from leaks
```

---

## ⚡ Prerequisites

To run this application, make sure your machine has:
- **Python 3.8 to 3.12** installed.
- Access to **Binance Futures Testnet API Keys**.
  - If you do not have keys, you can generate them by logging into [testnet.binancefuture.com](https://testnet.binancefuture.com) with a crypto wallet or a registered account.

---

## ⚙️ Setup & Configuration

Follow these step-by-step commands to get the trading bot ready on your system:

### 1. Clone or Move to Workspace
Open your terminal and navigate to the directory of the trading bot project:
```bash
cd c:/Users/Ann/Desktop/bot/trading_bot
```

### 2. Create and Activate Virtual Environment
It is highly recommended to use a virtual environment to avoid package conflicts:
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(On Linux/macOS, use: `source venv/bin/activate`)*

### 3. Install Dependencies
Install all required libraries using the pinned configurations:
```bash
pip install -r requirements.txt
```

### 4. Configure Your API Secrets
1. Copy the `.env.example` file and create a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open the newly created `.env` file in your preferred text editor and replace the placeholder text with your actual credentials:
   ```env
   BINANCE_API_KEY=your_actual_binance_testnet_api_key_here
   BINANCE_API_SECRET=your_actual_binance_testnet_api_secret_here
   ```

> [!WARNING]
> Never commit your `.env` file to public code repositories. The local `.gitignore` is pre-configured to keep this file locally contained on your machine.

---

## 🖥️ Command Usage & Examples

Verify that everything is set up correctly by calling the CLI help menu:
```bash
python cli.py --help
```

Below are exact production-ready CLI command templates for the three supported order types:

### 1. Market Order
Places an immediate long market order for `0.005 BTC`:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.005
```

### 2. Limit Order (Requires Price)
Places a limit short order for `0.02 ETH` at a designated entry target of `$3450.50`:
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.02 --price 3450.50
```

### 3. Stop Market Order (Requires stopPrice - Bonus Feature!)
Places a long stop-market trigger order for `0.1 SOL` with a trigger target of `$175.50`:
```bash
python cli.py --symbol SOLUSDT --side BUY --type STOP_MARKET --quantity 0.1 --stopPrice 175.50
```
*Note: You can also use the `--stop-price` format for maximum command convenience.*

---

## 📝 Logging Architecture

The bot uses the standard Python `logging` module configured with a dual-handler rotating engine defined inside [logging_config.py](file:///c:/Users/Ann/Desktop/bot/trading_bot/bot/logging_config.py).

### Visual Output Behavior
1. **Console Stream**: Displays clean runtime events, standard success alerts, validation markers, and execution steps.
2. **Rotating File log (`logs/trading.log`)**:
   - Stores long-term records up to **5MB** before seamlessly cycling (retaining up to 3 old archive backups).
   - Formats log entries with precise timestamp strings: `YYYY-MM-DD HH:MM:SS [LEVEL] name - message`.

### Example Log Entries
```text
2026-05-20 20:35:10 [INFO] root - Performing local parameter validations...
2026-05-20 20:35:10 [INFO] bot.validators - Local parameter validation passed.
2026-05-20 20:35:10 [INFO] bot.client - Initializing Binance Client connected to Futures Testnet...
2026-05-20 20:35:11 [INFO] bot.client - Binance Futures Testnet Client successfully connected and verified.
2026-05-20 20:35:11 [INFO] bot.orders - Sending Futures Order Request: symbol=BTCUSDT, side=BUY, type=LIMIT, quantity=0.005, price=65200.0, stopPrice=None
2026-05-20 20:35:12 [INFO] bot.orders - Order successfully placed! OrderID: 2849174028 | Status: NEW
```

---

## 🏛️ Architecture & Design Decisions

- **Strict Single-Responsibility Principle (SRP)**:
  - `cli.py` ONLY manages user argument parsing and CLI output presentation.
  - `client.py` ONLY handles loading environment configs and checking API server health.
  - `validators.py` ONLY handles parameter check boundaries and cleans inputs.
  - `orders.py` ONLY manages the API communication wrappers.
- **Fail-Safe Pre-Flight Validations**: Checks all parameters locally *prior* to reaching out over HTTP. This prevents unnecessary round-trip latency and avoids wasting API rate limits on simple typos or missing values.
- **Robust Exception Cascade**: Captures `BinanceAPIException` separately from general runtime/network connectivity exceptions. This allows the bot to output highly detailed diagnostic messages if the API complains about insufficient margins, bad leverage, or out-of-bounds prices.

---

## 🧠 Underlying Assumptions

1. **Testnet Mode Only**: The API client is strictly locked to `testnet=True` as a guardrail. This guarantees that your real capital will never be put at risk, even if you accidentally configure production API keys in the `.env` file.
2. **Leverage and Margins**: The bot assumes your Futures Testnet account has already set up the appropriate leverage configurations and has enough collateral margin (in Mock USDT) to cover the requested contract sizes.
3. **Symbol Suffixes**: Symbols are formatted to uppercase (e.g. `BTCUSDT`). The bot expects symbols that exist on the Binance USDT-M Futures markets.
4. **Time In Force**: LIMIT orders automatically set the `timeInForce` parameter to `GTC` (Good Till Cancelled), which is a common and standard default.
