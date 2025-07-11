# AlgoProject - Advanced Crypto Trading Platform

A comprehensive algorithmic trading platform focused on cryptocurrency markets with advanced backtesting, live trading, and portfolio management capabilities.

================================================================================
🚀 AlgoProject - Crypto Trading Platform (Personal Laptop Edition)
================================================================================
� Crypto Trading: 100+ Exchanges via CCXT
⚡ Advanced Backtesting & Live Trading
🔧 Strategy Development & Optimization
🏠 Optimized for Personal Use (No Corporate Restrictions)
================================================================================

📋 QUICK START:
==================================================
• Setup everything:     setup.bat
• Launch crypto platform: python crypto_launcher.py
• Direct crypto trading: python crypto_main.py
• Full documentation:   PERSONAL_LAPTOP_SETUP.md

💡 TIP: Run setup.bat first for automated installation!

� NOTE: Stocks/Fyers disabled due to corporate firewall restrictions.
         Focus on crypto trading for unrestricted market access.

================================================================================
📚 Documentation: docs/ | 🔧 Setup: setup.bat | 💰 Happy Crypto Trading!
================================================================================

## 🏠 Personal Laptop Setup

This version is optimized for personal laptops with no network restrictions:

1. **Auto Setup**: Run `setup.bat` for complete automated installation
2. **Crypto Focus**: All crypto exchanges accessible via CCXT
3. **No Firewall Issues**: Bypass corporate network restrictions
4. **Full Features**: Backtesting, live trading, technical analysis

## 🚀 Crypto Trading Features

### Multi-Exchange Support
- **Binance, Coinbase Pro, Kraken, Bitfinex, KuCoin**
- **100+ exchanges** via CCXT library
- **Real-time data** and order execution
- **Paper trading** for risk-free testing

### Advanced Tools
```bash
# Launch crypto trading platform
python crypto_launcher.py

# Direct crypto trading
python crypto_main.py

# Crypto backtesting
python crypto_backtest.py
```

## Key Features

- **Multi-Asset Support**: Stocks (NSE/BSE via Fyers API) and Crypto (Multiple exchanges via CCXT)
- **Advanced Backtesting**: Comprehensive KPIs, strategy comparison, and detailed reporting
- **Live Trading**: Real-time scanning, signal generation, and portfolio management
- **Strategy Library**: Pre-built strategies with optimization capabilities
- **Risk Management**: Position sizing, stop-loss, and portfolio risk controls
- **Organized Structure**: Clean separation between crypto and stock modules

## Project Structure

```
AlgoProject/
├── launcher.py           # 🚀 Main launcher script
├── crypto/scripts/       # 🪙 Crypto trading scripts
│   ├── enhanced_crypto_backtest.py
│   ├── crypto_demo_live.py
│   ├── crypto_live_scanner.py
│   └── batch_runner.py
├── stocks/scripts/       # 📈 Stock trading scripts
│   ├── stocks_backtest.py
│   ├── stocks_demo_live.py
│   └── stocks_live_scanner.py
├── src/                 # 🔧 Core modules
│   ├── data_acquisition.py    # Unified data fetching
│   ├── src/strategies/        # Trading strategies (all strategies)
│   └── ...
├── docs/                # 📚 Documentation
├── input/               # 📊 Asset lists and configuration
├── output/              # 📈 Backtest results and reports
├── crypto/              # 🪙 Crypto-specific modules
├── stocks/              # 📈 Stock-specific modules
└── utils/               # 🛠️ Utility functions
```

## Core Modules

### Data Acquisition
- **Location**: `src/data_acquisition.py`
- **Purpose**: Unified data fetching for both crypto and stocks
- **Features**: 
  - Crypto: CCXT integration for multiple exchanges
  - Stocks: Fyers API for NSE/BSE data
  - Auto-detection of data source based on symbol format

### Trading Scripts
- **Crypto Scripts**: `crypto/scripts/` - All cryptocurrency-related functionality
- **Stock Scripts**: `stocks/scripts/` - All stock market-related functionality
- **No Root Scripts**: Removed duplicate/empty scripts from root directory

## Documentation

All documentation is available in the `/docs` directory:

- **Setup Guide**: `docs/SETUP_GUIDE.md`
- **API Configuration**: `docs/FYERS_SETUP.md`
- **Project Status**: `docs/PROJECT_STATUS.md`
- **Features Guide**: `docs/ENHANCED_CRYPTO_BACKTEST_FEATURES.md`

## Getting Started

```bash
# Initial setup
setup.bat

# Use launcher for easy access
python launcher.py --all

# Direct script execution examples:
# Crypto backtest
cd crypto/scripts && python enhanced_crypto_backtest.py --symbols BTC/USDT ETH/USDT --compare

# Stock backtest
cd stocks/scripts && python stocks_backtest.py --symbols RELIANCE TCS --compare

# Batch crypto testing
cd crypto/scripts && python batch_runner.py --symbols BTC/USDT ETH/USDT --strategies BB_RSI,MACD_Only
```

## Recent Updates

### ✅ Project Reorganization (July 2025)
- **Scripts Reorganization**: Moved all scripts to appropriate modules (`crypto/scripts/`, `stocks/scripts/`)
- **Data Acquisition**: Unified `data_acquisition.py` now located in `src/` directory
- **Documentation**: All `.md` files moved to `docs/` directory for better organization
- **Launcher**: New `launcher.py` script for easy access to all functionalities
- **Clean Structure**: Removed duplicate and empty files

### 🔧 Data Acquisition Module
- **Single Source**: Only one `data_acquisition.py` file located in `src/`
- **Unified Interface**: Handles both crypto (CCXT) and stock (Fyers API) data
- **Auto-Detection**: Automatically detects data source based on symbol format
- **Error Handling**: Robust error handling and timeout management

## Support

For detailed documentation, troubleshooting, and advanced configuration, please refer to the comprehensive guides in the `/docs` directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
