# AlgoProject - Advanced Crypto Trading Platform

A comprehensive algorithmic trading platform focused on cryptocurrency markets with advanced backtesting, live trading, and portfolio management capabilities.

## 🚀 Quick Start

### First Time Setup:
```powershell
# 1. Run setup (installs all dependencies)
.\setup.bat

# 2. Launch unified platform (recommended)
.\venv\Scripts\python.exe main.py
```

### Daily Usage - Choose Your Entry Point:

#### 🎯 **main.py** - Unified Platform Launcher (Recommended)
```powershell
.\venv\Scripts\python.exe main.py
```
- **Best for**: Complete platform access (crypto + stocks)
- **Features**: Project health checks, system management
- **Users**: All users wanting full platform capabilities

#### 🪙 **crypto_launcher.py** - Full Crypto Trading Platform
```powershell
.\venv\Scripts\python.exe crypto_launcher.py
```
- **Best for**: Active crypto traders
- **Features**: 10 interactive menu options, all crypto operations
- **Users**: Dedicated crypto trading with advanced tools

#### ⚡ **crypto_main.py** - Quick Health Check & Diagnostics
```powershell
.\venv\Scripts\python.exe crypto_main.py
```
- **Best for**: Quick system validation and troubleshooting
- **Features**: Fast startup, minimal dependencies, pure diagnostic
- **Users**: Developers, debugging, status checks

## 📋 Launcher Hierarchy & Dependencies

```
main.py (Unified Entry) 
    ↓ [calls]
crypto_launcher.py (Full Crypto Platform)
    ↓ [option 10 launches]
crypto_main.py (Health Check & Diagnostics)
```

### File Dependencies:
- **All launchers**: Use built-in Python modules only (`os`, `sys`, `json`, `datetime`)
- **No external packages**: Clean separation, fast startup
- **Optimal structure**: Each serves distinct users without redundancy

### When to Use Which:
- **🎯 main.py**: Daily platform access, project management
- **🪙 crypto_launcher.py**: Intensive crypto trading sessions  
- **⚡ crypto_main.py**: Quick checks, troubleshooting

## 📁 Project Structure

### Essential Core Files (Root Directory):
- ✅ `setup.bat` - Main setup script (run this first)
- ✅ `main.py` - **Unified platform launcher** (primary entry point)
- ✅ `crypto_launcher.py` - **Full crypto trading platform** (10 menu options)
- ✅ `crypto_main.py` - **Quick health check & diagnostics** (troubleshooting)
- ✅ `requirements.txt` - Python dependencies
- ✅ `README.md` - Main project documentation
- ✅ `LICENSE` - Project license
- ✅ `.gitignore` - Git configuration

### Launcher Usage Guide:
1. **🎯 main.py** → Complete platform access, project management
2. **🪙 crypto_launcher.py** → Advanced crypto trading with full menu system
3. **⚡ crypto_main.py** → Fast diagnostics and system validation

### Directories:
- ✅ `crypto/` - Crypto trading modules and data
- ✅ `stocks/` - Stock trading modules
- ✅ `strategies/` - Trading strategies
- ✅ `tools/` - Utility tools
- ✅ `utils/` - Common utilities
- ✅ `tests/` - Test files
- ✅ `docs/` - All documentation (.md files)
- ✅ `helper_scripts/` - Non-essential .bat files
- ✅ `venv/` - Python virtual environment

💡 TIP: Run setup.bat first for automated installation!

� NOTE: Stocks/Fyers disabled due to corporate firewall restrictions.
         Focus on crypto trading for unrestricted market access.

=====================================
📚 Documentation: docs/ | 🔧 Setup: setup.bat | 💰 Happy Crypto Trading!
=====================================

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
# 🎯 Unified Platform (Recommended Entry Point)
.\venv\Scripts\python.exe main.py

# 🪙 Full Crypto Trading Platform (10 Menu Options)
.\venv\Scripts\python.exe crypto_launcher.py

# ⚡ Quick Health Check & Diagnostics
.\venv\Scripts\python.exe crypto_main.py

# Direct Script Access (Advanced Users)
.\venv\Scripts\python.exe crypto\scripts\enhanced_crypto_backtest.py
.\venv\Scripts\python.exe crypto\scripts\crypto_live_scanner.py
```

## 🎯 Launcher File Purposes

### **main.py** - Unified Platform Entry Point
- **Role**: Primary launcher for entire AlgoProject platform
- **Dependencies**: Built-in Python modules only (`os`, `sys`, `json`, `datetime`)
- **Features**: 
  - Unified access to crypto and stock trading systems
  - Project health checks and system information
  - Virtual environment detection and validation
  - Clean project management interface
- **Best For**: Daily platform access, beginners, complete functionality

### **crypto_launcher.py** - Advanced Crypto Trading Platform  
- **Role**: Full-featured crypto trading interface with 10 interactive options
- **Dependencies**: Built-in Python modules only
- **Features**:
  - Complete menu system for all crypto operations
  - Live trading, backtesting, portfolio analysis
  - Multi-exchange support (100+ via CCXT)
  - Advanced scanning and signal generation
- **Best For**: Active crypto traders, advanced features, intensive trading sessions

### **crypto_main.py** - Lightweight Diagnostics Tool
- **Role**: Quick health checker and troubleshooting utility  
- **Dependencies**: Built-in Python modules only
- **Features**:
  - Fast system validation and status checks
  - Virtual environment verification
  - Minimal startup time, pure diagnostic utility
  - Basic library import testing
- **Best For**: Developers, troubleshooting, quick system verification

## Key Features

- **Multi-Asset Support**: Stocks (NSE/BSE via Fyers API) and Crypto (Multiple exchanges via CCXT)
- **Advanced Backtesting**: Comprehensive KPIs, strategy comparison, and detailed reporting
- **Live Trading**: Real-time scanning, signal generation, and portfolio management
- **Strategy Library**: Pre-built strategies with optimization capabilities
- **Risk Management**: Position sizing, stop-loss, and portfolio risk controls
- **Organized Structure**: Clean separation between crypto and stock modules

## 📁 Project Structure & Launcher Hierarchy

```
AlgoProject/
├── 🎯 main.py                    # PRIMARY: Unified platform launcher
├── 🪙 crypto_launcher.py         # ADVANCED: Full crypto trading platform  
├── ⚡ crypto_main.py             # DIAGNOSTIC: Quick health check utility
├── setup.bat                     # Initial setup script
├── requirements.txt              # Python dependencies
├── README.md                     # This documentation
├── LICENSE & .gitignore          # Project configuration
├── 
├── crypto/                       # 🪙 Crypto trading modules
│   ├── data_acquisition.py       # CCXT only, no stock dependencies
│   ├── scripts/                  # Advanced crypto trading scripts
│   ├── output/                   # All trading results and reports
│   ├── logs/                     # Centralized logging
│   └── tools/                    # Crypto utilities
├── stocks/                       # 📈 Stock trading modules
│   ├── data_acquisition.py       # Fyers API + CCXT for mixed portfolios
│   └── scripts/                  # Stock trading scripts  
├── strategies/                   # 📊 Trading strategies
├── utils/                        # 🛠️ Common utilities
├── docs/                         # 📚 All documentation (.md files)
├── helper_scripts/               # � Non-essential .bat files
└── venv/                         # � Python virtual environment
```

### 🎯 Launcher Execution Flow:
```
main.py (entry) → crypto_launcher.py (platform) → crypto_main.py (diagnostic)
     ↓                    ↓                           ↓
Unified Access      Interactive Menu              Health Check
```

### 🔧 Module Separation:
- **Crypto Scripts**: Use `crypto/data_acquisition.py` (CCXT only, no Fyers dependency)
- **Stock Scripts**: Use `stocks/data_acquisition.py` (includes Fyers API for NSE/BSE)
- **Clean Dependencies**: Each module imports only what it needs
- **No Shared Tools**: Removed `tools/data_acquisition.py` for better separation

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

### 🚀 Recommended Launch Sequence:

```powershell
# 1. First time setup (run once)
.\setup.bat

# 2. Daily usage - choose your entry point:

# 🎯 RECOMMENDED: Unified platform access
.\venv\Scripts\python.exe main.py

# 🪙 ADVANCED: Full crypto trading platform
.\venv\Scripts\python.exe crypto_launcher.py  

# ⚡ DIAGNOSTIC: Quick system health check
.\venv\Scripts\python.exe crypto_main.py
```

### 🔧 Direct Script Execution (Advanced Users):
```powershell
# Crypto backtesting
.\venv\Scripts\python.exe crypto\scripts\enhanced_crypto_backtest.py --symbols BTC/USDT ETH/USDT --compare

# Live crypto scanning  
.\venv\Scripts\python.exe crypto\scripts\crypto_live_scanner.py

# Batch crypto testing
.\venv\Scripts\python.exe crypto\scripts\batch_runner.py --symbols BTC/USDT ETH/USDT --strategies BB_RSI,MACD_Only
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

## 🧹 Clean Project Organization

This project has been organized with a minimal, clean root directory structure:

### What's in Root Directory:
- **Only essential files** needed to run the platform
- **No clutter** - helper files moved to `helper_scripts/`
- **Clear structure** - documentation moved to `docs/`
- **Easy navigation** - everything has its place

### File Organization:
- 📁 **All .md files** → `docs/` (except main README.md)
- 📁 **Helper .bat files** → `helper_scripts/`
- 📁 **Utility scripts** → `docs/` or appropriate module directories
- 📁 **Logs** → `crypto/logs/` (centralized logging)
- 📁 **Outputs** → `crypto/output/` (all results in one place)

### Benefits:
- ✅ **Easy to find** what you need
- ✅ **Professional structure** for development
- ✅ **No confusion** about which files to use
- ✅ **Clean Git commits** with organized changes

## Support

For detailed documentation, troubleshooting, and advanced configuration, please refer to the comprehensive guides in the `/docs` directory.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
