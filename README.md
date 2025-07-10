# AlgoProject - Advanced Trading Strategy Platform

A comprehensive algorithmic trading platform supporting both crypto and stock markets with advanced backtesting, live trading, and portfolio management capabilities.

================================================================================
🚀 AlgoProject - Advanced Trading Strategy Platform
================================================================================
📊 Multi-Asset Trading: Crypto + Stocks
⚡ Advanced Backtesting & Live Trading
🔧 Strategy Development & Optimization
================================================================================

📋 QUICK START:
==================================================
• For crypto trading: python launcher.py --crypto
• For stock trading:  python launcher.py --stocks
• For setup help:     python launcher.py --setup
• For all options:    python launcher.py --all

💡 TIP: Start with setup.bat if this is your first time!

================================================================================
📚 Documentation: docs/ | 🔧 Setup: setup.bat | 🎯 Happy Trading!
================================================================================

## Quick Start

1. **Setup Environment**: Run `setup.bat` or follow the setup guide in `docs/SETUP_GUIDE.md`
2. **Configure APIs**: Set up Fyers API for stocks and CCXT for crypto (see `docs/FYERS_SETUP.md`)
3. **Run Backtests**: Use the enhanced backtest scripts in `crypto/scripts/` and `stocks/scripts/`
4. **Live Trading**: Start with demo mode using the launcher script

## 🚀 Launcher Script

Use the new launcher script for easy access to all functionalities:

```bash
# Show all available options
python launcher.py --all

# Show crypto trading options
python launcher.py --crypto

# Show stock trading options  
python launcher.py --stocks

# Show setup and configuration help
python launcher.py --setup
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
│   ├── strategies/            # Trading strategies
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
