# AlgoProject - Trading Platform Instructions

# AlgoProject - Trading Platform Instructions

## 🚀 **Quick Start - Simple & Easy!**

### **Easy Launcher (Recommended for Beginners)**
```bash
# Navigate to project directory
cd c:\vscode\AlgoProject

# Run the simple launcher menu
python scripts/launcher.py
```
The launcher provides an easy menu to choose any trading mode.

### **Direct Commands for Advanced Users**

#### **1. 🧪 Quick Test (Start Here!)**
```bash
# Test the system with 3 crypto symbols
python scripts/quick_test.py
```

#### **2. 💰 Crypto Trading (CCXT Data - All 37 Symbols)**
```bash
# Backtest all crypto pairs
python scripts/crypto_backtest.py

# Live scanning (real-time alerts)
python scripts/crypto_live_scanner.py
```

#### **3. 📈 Stock Trading (TradingView Data - Authenticated)**
```bash
# Backtest stocks
python scripts/stocks_backtest.py

# Live stock scanning
python scripts/stocks_live_scanner.py
```

#### **4. 🛠️ Utilities**
```bash
# List available crypto assets
python scripts/list_crypto_assets.py

# List supported exchanges
python scripts/list_ccxt_exchanges.py
```

## 📁 **New Simplified Structure**

### **Scripts (All Separate & Simple)**
- `launcher.py` - Easy menu launcher
- `quick_test.py` - Quick 3-symbol test
- `crypto_backtest.py` - Crypto historical analysis
- `crypto_live_scanner.py` - Real-time crypto alerts
- `stocks_backtest.py` - Stock historical analysis
- `stocks_live_scanner.py` - Real-time stock alerts
- `list_crypto_assets.py` - Show crypto pairs
- `list_ccxt_exchanges.py` - Show exchanges

### **Key Benefits of New Structure**
1. ✅ **Simple**: Each script does one thing well
2. ✅ **No Configuration Confusion**: No more yaml file mixing
3. ✅ **Crypto = CCXT**: All crypto always uses CCXT (fast, reliable)
4. ✅ **Stocks = TradingView**: All stocks use TradingView (with authentication)
5. ✅ **Bulk Processing**: Scans all symbols at once (not one-by-one)
6. ✅ **Professional Output**: Beautiful tables and progress indicators

## 🔑 **TradingView Authentication**

The stocks scripts now include TradingView authentication:
- **Username**: ashish.sharma14@gmail.com
- **Password**: BlockTrade5$1
- **Fallback**: If auth fails, uses anonymous mode (limited data)

## 📊 **Data Sources**

### **Crypto (CCXT)**
- ✅ Real-time data
- ✅ No login required
- ✅ Fast and reliable
- ✅ 37 USDT pairs supported

### **Stocks (TradingView)**
- ✅ Authenticated access
- ✅ More data availability
- ✅ Indian NSE stocks
- ✅ Handles timezone properly

## 📈 **Sample Output**

### Crypto Backtest
```
🚀 Crypto Backtest Scanner
================================================================================
🔍 Scanning 37 crypto symbols using CCXT (Kraken)
📊 Strategy: VWAPSigma2Strategy
================================================================================
📈 [ 1/37] Processing BTC/USDT... ✅ 3 signals
📈 [ 2/37] Processing ETH/USDT... ✅ 2 signals
...
✅ Backtest completed in 45.2s
📊 Total signals: 15
💰 Total trades: 8
```

### Live Scanner
```
🔴 LIVE Crypto Scanner
================================================================================
📅 2025-07-08 13:15:30 IST | 🔍 Scan #1
------------------------------------------------------------
🚨 LIVE SIGNALS DETECTED (2 signals)
╔══════════════════════╦══════════╦════════╦════════════╦══════════════╗
║ Time                 ║ Symbol   ║ Signal ║ Price      ║ Volume       ║
╠══════════════════════╬══════════╬════════╬════════════╬══════════════╣
║ 2025-07-08 13:15:30  ║ BTC/USDT ║ BUY    ║ $43250.45  ║ 1,234,567    ║
║ 2025-07-08 13:15:30  ║ ETH/USDT ║ SELL   ║ $2845.12   ║ 2,345,678    ║
╚══════════════════════╩══════════╩════════╩════════════╩══════════════╝
```
python -m venv venv

# Activate virtual environment
# For PowerShell:
venv\Scripts\Activate.ps1
# For Command Prompt:
venv\Scripts\activate.bat

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📊 **Main Trading Scripts**

### **1. Backtest Mode (Historical Analysis)**
```bash
# Run backtest with default config (all 37 USDT pairs)
python scripts/realtime_trader.py

# Run backtest with specific configurations
python scripts/realtime_trader.py --config config/config_test.yaml
python scripts/realtime_trader.py --config config/config_crypto.yaml
python scripts/realtime_trader.py --config config/config_stocks.yaml
```

### **2. Forward Testing Mode (Real-time Live Trading Simulation)**
```bash
# Run forward testing with default config
python scripts/realtime_trader.py --forward

# Run forward testing with specific configurations
python scripts/realtime_trader.py --config config/config_test.yaml --forward
python scripts/realtime_trader.py --config config/config_crypto.yaml --forward
```

---

## 🔧 **Utility Scripts**

### **3. List Available Exchanges**
```bash
python scripts/list_ccxt_exchanges.py
```

### **4. Update Crypto Asset List**
```bash
# Updates input/crypto_assets.csv with all available Kraken USDT pairs
python scripts/list_crypto_assets.py
```

### **5. Standalone Backtest Runner**
```bash
# If you have the separate backtest runner
python scripts/backtest_runner.py
python scripts/backtest_runner.py --config config/config_crypto.yaml
```

---

## 📂 **Project Structure**

```
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
├── input/
│   ├── crypto_assets.csv       # 37 USDT trading pairs
│   └── stocks_assets.csv       # Stock symbols
├── output/
│   ├── scan_results_*.csv      # Market scan results
│   └── backtest_trades_*.csv   # Backtest trade logs
├── src/
│   └── strategies/             # Trading strategies
│       ├── VWAPSigma2Strategy.py
│       ├── FiftyTwoWeekLowStrategy.py
│       └── sma_cross.py
└── venv/                       # Python virtual environment
```

---

## 🎯 **Most Common Use Cases**

### **Quick Test Run (10 symbols):**
```bash
cd AlgoProject
python scripts/realtime_trader.py --config config/config_test.yaml
```

### **Live Forward Testing (Real-time):**
```bash
cd AlgoProject
python scripts/realtime_trader.py --config config/config_test.yaml --forward
```

### **Full Backtest (All 37 USDT Pairs):**
```bash
cd AlgoProject
python scripts/realtime_trader.py --config config/config_crypto.yaml
```

---

## 📈 **Expected Output Format**

Both backtest and forward modes display:

### **Real-time Progress:**
```
🔍 Scanning crypto assets: 37 symbols
📊 Strategy: VWAPSigma2Strategy | Exchange: kraken | Data: ccxt
📅 2025-07-08 14:30:15 IST | 🔍 Processing 37 symbols...
✅ Data fetched in 9.1s | Processing signals...
🎯 BTC/USDT: BUY (VWAP -2σ breakout) | Price: 108191
```

### **Professional Trade Tables:**
```
====================================================================================================
📊 BACKTEST SUMMARY / 📈 OPEN POSITIONS
====================================================================================================
+----+----------+--------+--------------+---------------+-----------------+----------+------------------+
|    |  Symbol  |  Side  |  Entry_Time  |   Entry_Price |   Current_Price |  Amount  |  Unrealized_PnL  |
+====+==========+========+==============+===============+=================+==========+==================+
|  0 | BTC/USDT |  LONG  |    14:30     |     108191    |       108350    |  $1000   |      $1.47       |
|  1 | ETH/USDT |  LONG  |    14:32     |       2534    |         2540    |  $1000   |      $2.37       |
+----+----------+--------+--------------+---------------+-----------------+----------+------------------+
```

### **PnL Summary:**
```
====================================================================================================
💰 PnL SUMMARY:
====================================================================================================
Realized PnL:        $     25.43
Unrealized PnL:      $      3.84
Total PnL:           $     29.27
Total Trades:               12
Win Rate:               75.0%
====================================================================================================
```

---

## ⚙️ **Configuration Files**

### **config_test.yaml** - Quick testing with 37 symbols
```yaml
asset_type: crypto
assets:
  crypto: input/crypto_assets.csv
interval: "5m"
bars: 100
trading_amount: 1000
exchange: "kraken"
strategy:
  file: VWAPSigma2Strategy.py
  class: VWAPSigma2Strategy
```

### **config_crypto.yaml** - Full crypto trading
```yaml
asset_type: crypto
assets:
  crypto: input/crypto_assets.csv
interval: "5m"
bars: 100
trading_amount: 1000
exchange: "kraken"
strategy:
  file: VWAPSigma2Strategy.py
  class: VWAPSigma2Strategy
```

---

## 🔑 **Key Features**

- **📊 Professional Display**: Beautiful tabular format with IST timestamps
- **🔄 Unified Asset Management**: Single `crypto_assets.csv` for all 37 USDT pairs
- **⚡ Smart Trade Management**: One trade per symbol, strategy-based entry/exit
- **🕐 IST Timestamps**: All times displayed in Indian Standard Time
- **💰 Real-time PnL Tracking**: Live unrealized PnL calculation and total summary
- **🎯 Signal Intelligence**: Only shows relevant signals, ignores HOLD states
- **📈 Performance Metrics**: Data fetch timing and scan efficiency tracking

---

## 🛠️ **Troubleshooting**

### **Common Issues:**

1. **ModuleNotFoundError:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Permission Error (PowerShell):**
   ```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Kraken API Errors:**
   - Ensure symbols in `crypto_assets.csv` are valid Kraken pairs
   - Check network connectivity

4. **Data Fetch Timeouts:**
   - Increase `fetch_timeout` in config files
   - Check exchange status

---

## 📋 **Available Strategies**

Located in `src/strategies/`:
- **VWAPSigma2Strategy.py** - VWAP ±2σ breakout strategy
- **FiftyTwoWeekLowStrategy.py** - 52-week low reversal strategy
- **sma_cross.py** - Simple Moving Average crossover

### **Adding New Strategies:**
1. Create new `.py` file in `src/strategies/`
2. Implement `generate_signal()` and `backtest()` methods
3. Update config file to reference new strategy

---

## 🔄 **Continuous Operation**

### **For Long-running Forward Tests:**
```bash
# Forward testing will run continuously with scan intervals
python scripts/realtime_trader.py --config config/config_test.yaml --forward
# Press Ctrl+C to stop
```

### **Scan Frequency:**
- Configured by `sleep_between_symbols` in config files
- Default: 60 seconds between scans for all symbols

---

## 📊 **Output Files**

All results saved to `output/` directory:
- `scan_results_crypto.csv` - Market scan results
- `backtest_trades_crypto.csv` - Historical backtest trades
- `scan_results_crypto_test.csv` - Test scan results

---

## 🎯 **Production Tips**

1. **Start with test config** for initial validation
2. **Monitor PnL closely** during forward testing
3. **Review backtest results** before live trading
4. **Keep asset lists updated** using utility scripts
5. **Use appropriate timeframes** for your strategy

---

**Happy Trading! 🚀📈**
