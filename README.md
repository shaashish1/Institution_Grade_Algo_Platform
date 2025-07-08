# How to Start the Project

1. **Open a terminal in your project directory:**
   ```
   cd c:\vscode\AlgoProject
   ```

2. **(Optional but recommended) Create and activate a virtual environment:**
   ```
   python -m venv venv
   ```
   - **If you see a "running scripts is disabled" error when activating:**
     - Open PowerShell as Administrator and run:
       ```
       Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
       ```
     - Then activate the environment:
       ```
       venv\Scripts\Activate.ps1
       ```
   - Or, in Command Prompt (cmd), use:
     ```
     venv\Scripts\activate.bat
     ```

3. **Install all dependencies:**
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run your main script or entry point.**  
   (Replace `main.py` with your actual entry script if different.)
   ```
   python main.py
   ```

5. **If you use Jupyter notebooks:**
   ```
   jupyter notebook
   ```

**Next steps after installing requirements:**
- Make sure your virtual environment is activated.
- Run your main Python script (for example, `python main.py`) to start your application.
- If your project uses Jupyter notebooks, launch them with `jupyter notebook`.
- Follow any project-specific instructions or documentation for configuration or usage.

**If you encounter errors:**  
- Check the terminal output for missing files or misconfigurations.
- Ensure all environment variables or config files are set as needed.
- Review the README or project docs for additional setup steps.
- **If you see `ModuleNotFoundError: No module named 'yaml'`, run:**
  ```
  pip install pyyaml
  ```
  or add `pyyaml` to your `requirements.txt` and run:
  ```
  pip install -r requirements.txt
  ```

## Project Requirements

### 1. Data Fetching
- Fetch historical and/or real-time data for a list of symbols (stocks, crypto, etc.) using `tvdatafeed` or 'ccxt' or other data sources.
- Display the fetched data (e.g., print head/tail, show summary, or plot).

### 2. Price Scanning & Strategy
- Scan the current/latest price for each symbol.
- Apply a trading strategy (e.g., SMA crossover, RSI, or custom logic) to determine entry/exit signals.
- Print or log the trade signals (buy/sell/hold) for each symbol.

### 3. Trading Workflow (main.py)
- The `main.py` file should:
  1. Read a list of symbols (from a config, list, or user input).
  2. Fetch data for each symbol.
  3. Scan the latest price and apply the chosen strategy.
  4. Display or log the results (signals, prices, etc.).
  5. (Optional) Run in a loop for live monitoring or backtesting.

### 4. Extensibility
- Allow easy switching or addition of strategies.
- Allow configuration of symbols, intervals, and strategy parameters.

---

## Algo Trading Platform Requirements

### Overview
Build an algorithmic trading platform that:
- Scans and records real-time data for selected crypto and stock assets.
- Applies user-selected strategies to generate trade signals.
- Supports modular strategies and configurable asset lists.
- Sends trade triggers to the specified exchange.

### Key Features

#### 1. Asset Input Files
- Maintain two input files:
  - `crypto_assets.csv` — List of crypto symbols to track.
  - `stock_assets.csv` — List of stock symbols to track.
- Only assets listed in these files will be scanned and processed.

#### 2. Real-Time Data Collection
- Continuously fetch and record real-time price data for all tracked assets.
- Store historical and real-time data for analysis and backtesting.

#### 3. Strategy Management
- Strategies are implemented as separate Python files in the `src/strategies/` folder.
- The platform can dynamically select and apply any strategy from this folder.
- Example strategies:
  - `VWAPSigma2Strategy.py` — Enters trade when price crosses VWAP ± 2 standard deviations.
  - `FiftyTwoWeekLowStrategy.py` — Enters trade when price hits a new 52-week low.

#### 4. Configuration File
- A config file (e.g., `config.yaml` or `config.json`) defines:
  - Which asset list to use (`crypto` or `stocks`).
  - Which strategy to apply (by filename/class).
  - Exchange(s) to send trade triggers to.
  - Other parameters (interval, thresholds, etc.).

#### 5. Trade Signal & Execution
- After applying the strategy, generate trade signals (buy/sell/hold).
- Send trade triggers to the configured exchange(s) (integration via API).

#### 6. Extensibility
- Easily add new strategies by dropping a new file in `src/strategies/`.
- Easily update asset lists by editing the input CSVs.
- Easily change configuration by editing the config file.

---

## Example Directory Structure

```
/AlgoProject
  /src
    /strategies
      VWAPSigma2Strategy.py
      FiftyTwoWeekLowStrategy.py
      ...
    ...
  crypto_assets.csv
  stock_assets.csv
  config.yaml
  main.py
  ...
```

---

## Example: VWAP Sigma 2 Strategy

- **Logic:** Enter a trade when price crosses above VWAP + 2*std (buy) or below VWAP - 2*std (sell).
- **File:** `src/strategies/VWAPSigma2Strategy.py`

## Example: 52 Week Low Strategy

- **Logic:** Enter a trade when price reaches a new 52-week low.
- **File:** `src/strategies/FiftyTwoWeekLowStrategy.py`

---

## Example config.yaml

```yaml
asset_type: crypto  # or 'stocks'
assets:
  crypto: crypto_assets.csv
  stocks: stock_assets.csv
strategy:
  file: VWAPSigma2Strategy.py
  class: VWAPSigma2Strategy
exchange: BINANCE
interval: in_1_hour
bars: 100
data_source: tvdatafeed
```

## Example crypto_assets.csv

```csv
symbol
BTCUSD
ETHUSD
BNBUSD
```

## Example stock_assets.csv

```csv
symbol
AAPL
MSFT
GOOGL
```

---

## How to Apply the VWAP Sigma 2 Strategy and Scan Stocks & Crypto

1. **Edit your `config.yaml` to select the VWAP Sigma 2 strategy and asset type:**
   ```yaml
   asset_type: crypto  # or 'stocks'
   assets:
     crypto: crypto_assets.csv
     stocks: stock_assets.csv
   strategy:
     file: VWAPSigma2Strategy.py
     class: VWAPSigma2Strategy
   exchange: KRAKEN
   interval: 1h  # For ccxt/Kraken, use '1h', '5m', etc.
   bars: 100
   data_source: ccxt  # Use 'ccxt' for Kraken/crypto, 'tvdatafeed' for stocks
   ```

2. **Make sure your asset CSVs are up to date:**
   - `crypto_assets.csv` for crypto symbols (e.g., `BTC/USD`)
   - `stock_assets.csv` for NSE stocks/ETFs (e.g., `RELIANCE`)

3. **Run the main script:**
   ```
   python main.py
   ```

4. **What happens:**
   - The script loads your config and asset list.
   - For each symbol, it fetches historical data from the selected exchange.
   - It applies the VWAP Sigma 2 strategy (from `src/strategies/VWAPSigma2Strategy.py`).
   - It prints the signal (BUY/SELL/HOLD) for each asset.

5. **To scan both stocks and crypto:**
   - Run once with `asset_type: crypto` and once with `asset_type: stocks` in your `config.yaml`.
   - Or, automate by looping over both types in your own script.

---

## How to Select Which Strategy to Apply

- The strategy to use for scanning is defined in your `config.yaml` file.
- You specify both the Python file and the class name of the strategy in the `strategy` section.

**Example:**
```yaml
strategy:
  file: VWAPSigma2Strategy.py
  class: VWAPSigma2Strategy
```
- To use a different strategy, change the `file` and `class` values to match the desired strategy in your `src/strategies/` folder.

**How it works:**
- When you run `python main.py`, the script reads the `config.yaml`, loads the specified strategy class from the given file, and applies it to each asset.

---

## Note on Kraken Error

- The error `kraken {"error":["EGeneral:Invalid arguments"]}` means some symbols in your `crypto_assets.csv` are not valid on Kraken.
- Make sure your symbols match Kraken's supported trading pairs (e.g., `BTC/USD`, `ETH/USD`).  
- Remove or correct any symbols that are not available on Kraken to avoid this error.

---

## How to Run a Backtest

1. **Run your main script as usual:**
   ```
   python main.py
   ```
   - This will scan all assets, apply the strategy, and save the latest scan results to `scan_results_crypto.csv` or `scan_results_stocks.csv`.
   - It will also save all backtest trades to `backtest_trades_crypto.csv` or `backtest_trades_stocks.csv`.

2. **Review the backtest results:**
   - Open the generated `backtest_trades_crypto.csv` (or `backtest_trades_stocks.csv`) in Excel or any CSV viewer.
   - Each row shows a simulated trade: entry/exit time, side, entry/exit price, and profit/loss (`pnl`).
   - You can sum the `pnl` column to see total profit/loss for the period.

3. **(Optional) Run a backtest manually in a notebook or script:**
   ```python
   import pandas as pd
   from src.strategies.VWAPSigma2Strategy import VWAPSigma2Strategy

   # Load historical data for a symbol (ensure it has columns: open, high, low, close, volume, timestamp)
   df = pd.read_csv("your_historical_data.csv")
   # Convert timestamp to IST if needed
   df["datetime_ist"] = pd.to_datetime(df["timestamp"], unit="ms" if df["timestamp"].max() > 1e12 else "s").dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")

   strat = VWAPSigma2Strategy()
   trades = strat.backtest(df)
   trades.to_csv("backtest_trades_manual.csv", index=False)
   print(trades)
   print("Total P/L:", trades["pnl"].sum())
   ```

**Tip:**  
- To backtest stocks, set `asset_type: stocks` and `exchange: NSE` in `config.yaml`, then run `python main.py`.

## Backtest Timeframe and Logic

### What timeframe did the backtest happen?
- The backtest was performed on **5-minute (5m) timeframe** data.
- This is set by the `interval: 5m` value in your `config.yaml` and used in `main.py` for fetching OHLCV data from Kraken.
- Each trade entry and exit in `backtest_trades_crypto.csv` corresponds to a 5-minute bar.

### What is the logic for the backtest?
- The backtest simulates following the VWAP Sigma 2 strategy with **take profit and stop loss** over the historical data.
- For each bar:
  - **Buy:** If price crosses above VWAP-2σ (from below) with volume at least 2x the rolling average, enter a long position.
  - **Take Profit:** If price rises 6.28% above entry, close the position.
  - **Stop Loss:** If price falls 3.14% below entry, close the position.
  - At the end of the data, any open position is closed at the last available price.
- Each trade is recorded with entry/exit time, side (BUY_TP, BUY_SL, BUY_EOD), entry/exit price, and profit/loss (`pnl`).
- The results are saved to `backtest_trades_crypto.csv` (or `backtest_trades_stocks.csv` for stocks).

## FAQ: Backtest and Live Trading

### Why is the backtest not showing trades from the configured start date?
- The backtest only generates trades if the strategy's entry condition is met after the `start_date`.
- If your data fetch (`bars`) is too small, or the exchange does not provide enough history, your DataFrame may only cover recent days.
- **Check:**  
  - Your `bars` value in `config.yaml` (e.g., `bars: 9000` for ~1 month of 5m bars).
  - The actual earliest date in your DataFrame:  
    ```python
    print(df["datetime_ist"].min(), df["datetime_ist"].max())
    ```
  - If the earliest date is after your `start_date`, increase `bars` or check the exchange's data limits.

### What does `side = BUY_EOD` mean?
- `BUY_EOD` means the strategy entered a long position but did not hit take profit or stop loss before the end of the data ("End Of Data").
- The open position is closed at the last available price in the dataset.
- The actual **buy** happens when the strategy condition is met (`BUY (VWAP -2σ reversal + 2x volume)`), and the position is closed by TP, SL, or EOD.

### How much historical data are we getting?
- Controlled by the `bars` parameter in `config.yaml`.
- For 5-minute bars:  
  - `bars: 9000` ≈ 31 days (12 bars/hour × 24 × 31 ≈ 9000).
- Actual data returned may be less if the exchange limits history or the symbol is newly listed.

### How to do a backtest?
1. Set `start_date` and `bars` in `config.yaml` for your desired period.
2. Run:
   ```
   python main.py
   ```

3. The script will:
   - Fetch historical data.
   - Filter data from `start_date`.
   - Apply the strategy and run the backtest.
   - Save results to `backtest_trades_crypto.csv` (or `backtest_trades_stocks.csv`).

### How to run live trades?
- **This codebase currently only scans and backtests.**
- To run live trades:
  1. Integrate with exchange APIs (e.g., `ccxt` for Kraken, Binance, etc.).
  2. On each new bar, fetch the latest data, apply the strategy, and if a signal is generated, send an order via the exchange API.
  3. You must handle authentication, order management, and error handling.
- **Warning:** Live trading requires careful testing and risk management.  
- For a starting point, see the `ccxt` documentation for placing orders:  
  https://docs.ccxt.com/en/latest/manual.html#creating-orders


### DEMO - How this works:

This script fetches only the latest bars (no history), simulates live trading using your strategy, and records trades.
It prints and saves all demo trades to demo_live_trades.csv.
You can adjust symbol, timeframe, window, trading_amount, and demo_iterations as needed.
No real orders are placed; this is a dry-run simulation for live trading performance.

## How to Configure Git in VSCode

1. **Install Git:**
   - Download and install Git from [https://git-scm.com/downloads](https://git-scm.com/downloads).

2. **Open VSCode and your project folder.**

3. **Initialize a Git repository (if not already):**
   - Open the VSCode terminal (`Ctrl+``).
   - Run:
     ```
     git init
     ```

4. **Set your Git user info (first time only):**
   ```
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

5. **Stage and commit your files:**
   ```
   git add .
   git commit -m "Initial commit"
   ```

6. **(Optional) Connect to a remote repository (e.g., GitHub):**
   ```
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin master
   ```

7. **Use the Source Control panel in VSCode:**
   - Click the Source Control icon on the sidebar (or press `Ctrl+Shift+G`).
   - You can stage, commit, and push changes using the VSCode UI.

**Tip:**  
- Add files/folders to `.gitignore` to exclude them from version control (e.g., `venv/`, `.env`, `*.pyc`).

## Troubleshooting: 'git' is not recognized

- This error means Git is **not installed** or not added to your system's PATH.
- **To fix:**
  1. Download and install Git from [https://git-scm.com/downloads](https://git-scm.com/downloads).
  2. During installation, make sure to select the option to "Add Git to PATH".
  3. After installation, restart VSCode and your terminal.
  4. Run `git --version` in the terminal to verify Git is available.

- Now you can use all Git commands in VSCode and the terminal.

## Configuration

All parameters for demo/live trading are now in `config.yaml`.  
**Edit this file to change trading symbols, strategy, exchange, scan interval, and more.**

Example:
```yaml
crypto_assets_file: "crypto_assets.csv"   # CSV file with symbols to scan
timeframe: "5m"                           # Bar interval for OHLCV data
window: 30                                # Number of bars to fetch
trading_amount: 1000                      # USD value per trade
demo_iterations: 10                       # Number of scan cycles (set high for continuous)
sleep_seconds: 300                        # Seconds between scans
exchange: "kraken"                        # Exchange name for ccxt
strategy_file: "VWAPSigma2Strategy.py"    # Strategy file (in src/strategies/)
strategy_class: "VWAPSigma2Strategy"      # Strategy class name
display_live_pnl: true                    # Show live PnL for open trades
log_trades_to_csv: true                   # Save trades to CSV at end
trades_csv_file: "demo_live_trades.csv"   # Output CSV file for trades
```

**To change trading behavior, just edit `config.yaml` and restart the script.**

## Orderbook Columns Explained

- **symbol**: Trading pair (e.g., BTC/USD)
- **side**: LONG or SHORT (currently only LONG is supported)
- **entry_time**: When the trade was opened
- **entry_price**: Price at which the trade was opened
- **quantity**: Number of units bought (calculated as trading_amount / entry_price)
- **exit_time**: When the trade was closed (empty if still open)
- **exit_price**: Price at which the trade was closed (empty if still open)
- **pnl**: Profit/loss per unit (only filled when trade is closed)
- **pnl_usd**: Total profit/loss in USD (only filled when trade is closed)
- **live_pnl_usd**: *Unrealized* profit/loss in USD for open trades, calculated using the latest price (shows how the trade is performing right now)
- **trade_action**: "OPEN" or "CLOSE"

> **Why do we need `live_pnl_usd` and not just `pnl`?**  
> `pnl` and `pnl_usd` are only filled when a trade is closed (i.e., both entry and exit prices are known).  
> `live_pnl_usd` is calculated for open trades using the current/latest price, so you can monitor the real-time performance of your open positions.

# Project Structure

```
/AlgoProject
  /input
    crypto_assets.csv
    stocks_assets.csv
  /output
    scan_results_crypto.csv
    backtest_trades_crypto.csv
    scan_results_stocks.csv
    backtest_trades_stocks.csv
  /src
    /strategies
      VWAPSigma2Strategy.py
      ...
  config_crypto.yaml
  config_stocks.yaml
  crypto_backtest.py
  stocks_backtest.py
  # ...other scripts...
```

- **input/**: All input asset lists (crypto, stocks)
- **output/**: All output files (scan results, backtest trades, logs, future db files)
- **src/strategies/**: All trading strategies
- **config_crypto.yaml**: Config for crypto trading/backtest
- **config_stocks.yaml**: Config for stocks trading/backtest
- **crypto_backtest.py**: Crypto backtest/demo/live script
- **stocks_backtest.py**: Stocks backtest/demo/live script

## Usage

- For crypto backtest:
  ```
  python crypto_backtest.py --config config_crypto.yaml
  ```
- For stocks backtest:
  ```
  python stocks_backtest.py --config config_stocks.yaml
  ```

- Edit the config files to set trading parameters, input/output files, and (for live trading) exchange keys.

---
Here are the complete commands to run all the Python files in the AlgoProject:

🚀 Main Trading Scripts
1. Backtest Mode (Historical Analysis)

# Run backtest with default config (all 37 USDT pairs)
python scripts/realtime_trader.py

# Run backtest with specific config
python scripts/realtime_trader.py --config config/config_test.yaml
python scripts/realtime_trader.py --config config/config_crypto.yaml
python scripts/realtime_trader.py --config config/config_stocks.yaml

2. Forward Testing Mode (Real-time Live Trading Simulation)

# Run forward testing with default config
python scripts/realtime_trader.py --forward

# Run forward testing with specific config
python scripts/realtime_trader.py --config config/config_test.yaml --forward
python scripts/realtime_trader.py --config config/config_crypto.yaml --forward

🔧 Utility Scripts
3. List Available Exchanges

python scripts/list_ccxt_exchanges.py

4. Update Crypto Asset List

# Updates input/crypto_assets.csv with all available Kraken USDT pairs
python scripts/list_crypto_assets.py

5. Standalone Backtest Runner

# If you have the separate backtest runner
python scripts/backtest_runner.py
python scripts/backtest_runner.py --config config/config_crypto.yaml

📂 File Structure Reference

AlgoProject/
├── scripts/
│   ├── realtime_trader.py      # Main trading script (backtest + forward)
│   ├── backtest_runner.py      # Standalone backtest runner
│   ├── list_ccxt_exchanges.py  # List supported exchanges
│   └── list_crypto_assets.py   # Update crypto asset list
├── config/
│   ├── config.yaml             # Default configuration
│   ├── config_test.yaml        # Test configuration
│   ├── config_crypto.yaml      # Crypto-specific config
│   └── config_stocks.yaml      # Stocks-specific config
└── input/
    ├── crypto_assets.csv       # 37 USDT trading pairs
    └── stocks_assets.csv       # Stock symbols

🎯 Most Common Commands
Quick Test Run:

cd AlgoProject
python scripts/realtime_trader.py --config config/config_test.yaml

Live Forward Testing:

cd AlgoProject
python scripts/realtime_trader.py --config config/config_test.yaml --forward

Full Backtest (All 37 Pairs):

cd AlgoProject
python scripts/realtime_trader.py --config config/config_crypto.yaml

