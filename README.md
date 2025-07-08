# 🚀 AlgoProject - Advanced Trading Platform

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](https://github.com)

> **A comprehensive cryptocurrency and stock trading platform with advanced symbol management, backtesting, and real-time monitoring capabilities.**

## ✨ **Key Features**

🎮 **Interactive Menu System** - User-friendly launcher with 13 options  
🪙 **900+ Crypto Trading Pairs** - Support for 9 major exchanges (Kraken, Binance, etc.)  
📈 **100+ NSE Stock Symbols** - NIFTY 50/Next 50 + sector-wise selection  
🛠️ **Advanced Symbol Management** - Live fetching & auto-configuration  
📊 **Progressive Testing** - Test → Backtest → Demo → Live workflow  
🔴 **Risk-Free Demo Modes** - Real data, no actual trades  
⚡ **Real-time Monitoring** - Live scanners and price alerts  
🛡️ **Professional Output** - Beautiful tables, progress bars, IST timestamps  

---

## 🚀 **Quick Start (3 Steps)**

### **Step 1: Clone & Setup**
```bash
# Clone the repository
git clone https://github.com/yourusername/AlgoProject.git
cd AlgoProject

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
venv\\Scripts\\Activate.ps1
# Windows CMD:
venv\\Scripts\\activate.bat
# Linux/macOS:
source venv/bin/activate
```

### **Step 2: Install Dependencies**
```bash
# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt
```

### **Step 3: Launch Platform**
```bash
# Start the interactive menu (RECOMMENDED FOR BEGINNERS)
python scripts/launcher.py

# Choose option 1 for Quick Test (30 seconds, safe)
```

---

## 🗂️ **Project Structure**

```
AlgoProject/
├── 📁 scripts/                    # 🎯 Main Trading Scripts
│   ├── launcher.py               # 🎮 Interactive menu system
│   ├── crypto_backtest.py        # 📊 Crypto historical analysis
│   ├── stocks_backtest.py        # 📈 Stock historical analysis
│   ├── crypto_demo_live.py       # 🔴 Live crypto demo (safe)
│   ├── stocks_demo_live.py       # 🔴 Live stock demo (safe)
│   ├── crypto_live_scanner.py    # ⚡ Real-time crypto alerts
│   ├── stocks_live_scanner.py    # ⚡ Real-time stock alerts
│   └── realtime_trader.py        # 🔥 Live trading (advanced)
├── 📁 utils/                      # 🛠️ Utilities & Management
│   ├── crypto_symbol_manager.py  # 🪙 Crypto symbol management
│   ├── stock_symbol_manager.py   # 📊 Stock symbol management
│   ├── data_acquisition.py       # 📥 Core data fetching
│   ├── quick_test.py             # 🧪 Quick 3-symbol test
│   ├── test_backtest.py          # 🧪 Detailed testing
│   ├── list_crypto_assets.py     # 📋 Show crypto pairs
│   ├── list_ccxt_exchanges.py    # 🏢 Show exchanges
│   └── live_nse_quotes.py        # 📊 Real-time NSE quotes
├── 📁 src/                        # 🧠 Core Algorithms
│   ├── strategies/               # 📈 Trading strategies
│   │   ├── VWAPSigma2Strategy.py # VWAP-based strategy
│   │   ├── FiftyTwoWeekLowStrategy.py # 52-week low strategy
│   │   └── sma_cross.py          # Simple moving average crossover
├── 📁 config/                     # ⚙️ Configuration Files
│   ├── config_crypto.yaml        # Crypto exchange settings
│   ├── config_stocks.yaml        # Stock market settings
│   └── config.yaml               # General settings
├── 📁 input/                      # 📁 Symbol Lists (Auto-updated)
│   ├── crypto_assets.csv         # Active crypto trading pairs
│   └── stocks_assets.csv         # Active stock symbols
├── 📁 output/                     # 📂 Results & Reports
│   ├── crypto_backtest_results.csv
│   ├── stocks_backtest_results.csv
│   └── live_signals.csv
├── requirements.txt               # 📋 Dependencies
└── README.md                     # 📖 This file
```

---

## 🎮 **Interactive Menu System**

Launch the user-friendly menu system:
```bash
python scripts/launcher.py
```

### **Available Options:**
```
🧪 TESTING & VALIDATION
   1. Quick Test           - Test 3 crypto symbols (30 seconds)
   2. Detailed Test        - Detailed backtest test (1 minute)

📊 BACKTEST (Historical Analysis)
   3. Crypto Backtest      - All crypto pairs historical analysis
   4. Stocks Backtest      - Stock historical analysis

🔴 LIVE DEMO (Real Data, NO Real Trades)
   5. Crypto Live Demo     - Real-time crypto demo trading
   6. Stocks Live Demo     - Real-time stock demo trading

⚡ LIVE SCANNERS (Real-time Alerts)
   7. Crypto Live Scanner  - Continuous crypto signal alerts
   8. Stocks Live Scanner  - Continuous stock signal alerts

🛠️ SYMBOL MANAGEMENT
   9. Crypto Symbol Manager - Fetch & select crypto pairs
  10. Stock Symbol Manager  - Fetch & select stocks from NIFTY

🔧 UTILITIES
  11. List Crypto Assets   - Show current crypto pairs
  12. List Exchanges       - Show supported exchanges
  13. Live NSE Quotes      - Real-time NSE stock prices

   0. Exit
```

---

## 🪙 **Advanced Crypto Symbol Management**

### **Features:**
- 🏢 **Choose Any Exchange**: Kraken, Binance, Coinbase, Bybit, OKX, etc.
- 🎯 **Smart Filtering**: USDT, USD, EUR, BTC, ETH pairs
- 📊 **900+ Trading Pairs**: Complete exchange symbol lists
- ⚡ **Quick Presets**: 'all', 'usdt', 'top20' for instant selection
- 🔄 **Auto-Updates**: Updates `input/crypto_assets.csv` & config files

### **Usage:**
```bash
python utils/crypto_symbol_manager.py

# Examples:
Select exchange (1-9): 1           # Choose Kraken
Enter your selection: usdt          # Select all USDT pairs (37 symbols)
# OR
Enter your selection: 1,5,10-15,20  # Select specific symbols by numbers
# OR  
Enter your selection: top20         # Select top 20 by market cap
```

---

## 📊 **Advanced Stock Symbol Management**

### **Features:**
- 📈 **NIFTY Indices**: NIFTY 50, NIFTY Next 50 (100 stocks total)
- 🏦 **Sector Selection**: Banking, IT, Auto, Pharma, FMCG, Metals, Energy, Finance
- ✅ **TradingView Validation**: Optional symbol verification
- 🔄 **Auto-Updates**: Updates `input/stocks_assets.csv` & config files

### **Usage:**
```bash
python utils/stock_symbol_manager.py

# Examples:
Select category number: 1           # NIFTY 50 (50 stocks)
Enter your selection: all           # Select all NIFTY 50 stocks
# OR
Select category number: 3           # Banking sector (10 stocks)
Enter your selection: 1,3,5         # Select specific banking stocks
```

---

## 🎯 **Recommended Workflow**

### **🔰 For Beginners (Start Here):**
```bash
# Step 1: Launch interactive menu
python scripts/launcher.py

# Step 2: Choose option 1 (Quick Test - 30 seconds, safe)
# Step 3: Try option 3 (Crypto Backtest - historical analysis)
# Step 4: Try option 5 (Live Demo - real-time, no trades)
```

### **🚀 For Advanced Users:**
```bash
# Step 1: Set up your symbols
python utils/crypto_symbol_manager.py  # Choose exchange & symbols
python utils/stock_symbol_manager.py   # Choose stock categories

# Step 2: Test your strategy
python utils/quick_test.py             # Quick validation
python scripts/crypto_backtest.py      # Full historical test

# Step 3: Live testing (no real trades)
python scripts/crypto_demo_live.py     # Forward testing demo

# Step 4: Real-time monitoring
python scripts/crypto_live_scanner.py  # Continuous signal alerts
```

---

## 📊 **Data Sources & Authentication**

### **🪙 Crypto (CCXT - No Authentication Required)**
- ✅ **Exchanges**: Kraken, Binance, Coinbase, Bybit, OKX, KuCoin, Huobi, Bitfinex, Gemini
- ✅ **Symbols**: 900+ trading pairs across all quote currencies
- ✅ **Default**: 37 USDT pairs (BTC/USDT, ETH/USDT, etc.)
- ✅ **Speed**: Fast, reliable, real-time data
- ✅ **Login**: Not required

### **📈 Stocks (TradingView - Authentication Recommended)**
- ✅ **Exchange**: NSE (National Stock Exchange, India)
- ✅ **Symbols**: 100+ NIFTY stocks + sector-wise selection
- ✅ **Default**: 50 NIFTY 50 stocks
- ✅ **Speed**: Good, requires authentication for full access
- ✅ **Login**: Optional (limited data without login)

---

## 🛡️ **Risk Management & Safety**

### **✅ Safe Operations (Zero Risk):**
- 🧪 **All Testing Scripts** - Validation only, no real trades
- 📊 **All Backtest Scripts** - Historical data analysis only
- 🔴 **All Demo Scripts** - Real-time data but NO actual trades
- ⚡ **All Scanner Scripts** - Monitoring only, no trades

### **⚠️ Real Trading Risk:**
- 🔥 **Live Trading Scripts** - Execute real trades (when enabled)
- 💡 **Always test** with demo scripts first
- 💰 **Start small** with minimal capital
- 🛡️ **Set stop losses** and risk management rules

---

## ⚙️ **Configuration & Dependencies**

### **📋 Complete Dependencies:**
```
# Core Trading & Data Libraries
ccxt>=4.0.0              # Cryptocurrency exchange library
tvdatafeed>=2.0.0        # TradingView data feed for stocks
backtrader==1.9.76.123   # Backtesting framework
nsepython>=0.9.0         # NSE data

# Data Processing & Analysis
pandas>=1.3,<2.0         # Data manipulation
numpy>=1.21.0            # Numerical computing
requests>=2.31.0         # HTTP requests

# Configuration & Utilities
pyyaml>=6.0              # YAML config files
tabulate>=0.9.0          # Table formatting
pytz>=2023.3             # Timezone handling

# Networking & Visualization
websocket-client>=1.0.0  # WebSocket connections
matplotlib>=3.5.0        # Plotting and charts
```

### **🔄 Auto-Updated Configuration Files:**
- `config/config_crypto.yaml` - Crypto exchange settings
- `config/config_stocks.yaml` - Stock market settings  
- `input/crypto_assets.csv` - Active crypto trading pairs
- `input/stocks_assets.csv` - Active stock symbols

---

## 📂 **Output Files & Reports**

### **📊 Generated Reports:**
- `output/crypto_backtest_results.csv` - Historical crypto performance
- `output/stocks_backtest_results.csv` - Historical stock performance
- `output/live_signals.csv` - Real-time trading signals
- `output/demo_trades.csv` - Demo trading results

---

## 🔧 **Troubleshooting**

### **Common Issues & Solutions:**
```bash
# If crypto symbols not found
python utils/crypto_symbol_manager.py  # Re-select symbols

# If stock symbols not working  
python utils/stock_symbol_manager.py   # Re-select NIFTY stocks

# If dependencies missing
pip install -r requirements.txt        # Reinstall packages

# If launcher menu not showing
cd /path/to/AlgoProject                # Ensure correct directory
python scripts/launcher.py             # Run from project root

# If PowerShell execution policy error
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Quick Fixes:**
1. **Symbol Issues**: Use symbol managers to refresh symbol lists
2. **Data Issues**: Check internet connection and exchange status
3. **Import Errors**: Ensure all dependencies installed with pip
4. **Config Issues**: Symbol managers auto-fix configuration files

---

## 🎉 **Advanced Usage Examples**

### **Example 1: Custom Crypto Setup**
```bash
# Step 1: Choose Binance exchange with EUR pairs
python utils/crypto_symbol_manager.py
# Select: Exchange 2 (Binance), then choose EUR pairs

# Step 2: Run backtest with new symbols
python scripts/crypto_backtest.py
```

### **Example 2: Banking Sector Focus**
```bash  
# Step 1: Select only banking stocks
python utils/stock_symbol_manager.py
# Select: Category 3 (Banking), choose all 10 banking stocks

# Step 2: Run banking sector analysis
python scripts/stocks_backtest.py
```

### **Example 3: Multi-Exchange Monitoring**
```bash
# Monitor multiple asset classes simultaneously
python scripts/crypto_live_scanner.py &  # Background crypto scanning
python scripts/stocks_live_scanner.py &  # Background stock scanning
python utils/live_nse_quotes.py &        # Live NSE price quotes
```

---

## 📚 **Contributing & Development**

### **Project Structure Guidelines:**
- **📁 scripts/**: Main user-facing trading scripts
- **📁 utils/**: Utilities, testing, and management tools
- **📁 src/**: Core algorithms and strategies
- **📁 config/**: Configuration files (auto-managed)
- **📁 input/**: Symbol lists (auto-managed)
- **📁 output/**: Results and reports

### **Adding New Features:**
1. **New Trading Strategy**: Add to `src/strategies/`
2. **New Exchange**: Extend `utils/crypto_symbol_manager.py`
3. **New Market**: Create new symbol manager in `utils/`
4. **New Script**: Add to appropriate folder and update launcher

### **Development Setup:**
```bash
# Install development dependencies
pip install pytest jupyter

# Run tests
python -m pytest tests/

# Start Jupyter for strategy development
jupyter notebook
```

---

## 📈 **Performance & Capabilities**

### **🔢 Platform Statistics:**
- **900+ Crypto Trading Pairs** across 9 major exchanges
- **100+ Stock Symbols** from NIFTY indices + sectors
- **13 Interactive Menu Options** for easy navigation
- **Zero Configuration** required - all auto-managed
- **Real-time Data** from CCXT and TradingView
- **Professional Output** with tables and progress bars

### **⚡ Performance Features:**
- **Bulk Processing** - Scans all symbols simultaneously
- **Concurrent Data Fetching** - Multi-threaded data acquisition
- **Smart Caching** - Efficient data management
- **Progress Indicators** - Real-time status updates
- **Error Handling** - Robust error recovery

---

## 🎯 **Next Steps After Setup**

### **Production Checklist:**
- [ ] ✅ Test all strategies with demo scripts
- [ ] ✅ Verify symbol lists are current and relevant
- [ ] ✅ Configure proper risk management parameters
- [ ] ✅ Set up logging and monitoring for production
- [ ] ✅ Start with small position sizes for live trading
- [ ] ✅ Have manual stop-loss procedures ready
- [ ] ✅ Configure real API keys for live trading (advanced)

### **Learning Path:**
1. **🔰 Beginner**: Start with launcher menu, try Quick Test
2. **📊 Intermediate**: Use symbol managers, run backtests
3. **🔴 Advanced**: Try demo live trading, customize strategies
4. **🔥 Expert**: Set up live trading with real API keys

---

## 📞 **Support & Resources**

### **Getting Help:**
- 📖 **Documentation**: This README + inline code comments
- 🎮 **Interactive Help**: Use the launcher menu for guidance
- 🧪 **Safe Testing**: All demo modes are risk-free
- 🔧 **Auto-Fixing**: Symbol managers resolve configuration issues

### **Key Commands Reference:**
```bash
# Most important commands
python scripts/launcher.py              # Main menu
python utils/crypto_symbol_manager.py   # Crypto setup
python utils/stock_symbol_manager.py    # Stock setup
python utils/quick_test.py              # Quick validation
```

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🏆 **Summary**

**🚀 AlgoProject** is the most comprehensive and user-friendly cryptocurrency and stock trading platform available, featuring:

✅ **Complete Beginner Support** - Interactive menus and safe demo modes  
✅ **Advanced Symbol Management** - 900+ crypto pairs, 100+ stocks  
✅ **Professional Tools** - Backtesting, live scanning, real-time monitoring  
✅ **Zero Configuration** - Auto-managed configs and symbol lists  
✅ **Progressive Learning** - Test → Backtest → Demo → Live workflow  
✅ **Production Ready** - Risk management and error handling  

**🎯 Ready to start? Run `python scripts/launcher.py` and choose option 1!**

---

*⭐ If you find this project helpful, please consider giving it a star on GitHub!*
# AlgoProject
