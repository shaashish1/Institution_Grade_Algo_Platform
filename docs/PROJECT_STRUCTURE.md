# AlgoProject - Complete Folder Structure & File Documentation

## 📁 Project Overview
AlgoProject is a comprehensive trading strategy platform supporting both cryptocurrency and stock trading with advanced backtesting capabilities, live trading, and portfolio management.

## 🗂️ Complete Folder Structure

```
AlgoProject/
├── 📁 crypto/                          # Cryptocurrency trading module
│   ├── 📁 input/                       # Crypto input data files and configs
│   │   ├── crypto_assets.csv           # List of crypto symbols to trade
│   │   ├── crypto_assets_detailed.csv  # Detailed crypto asset information
│   │   ├── crypto_assets_test.csv      # Test crypto assets for development
│   │   ├── config_crypto.yaml          # Main crypto configuration
│   │   └── config_test.yaml            # Test configuration
│   ├── 📁 scripts/                     # Crypto-specific scripts
│   │   ├── crypto_backtest.py          # Main crypto backtesting engine
│   │   ├── crypto_demo_live.py         # Live crypto trading demo
│   │   ├── crypto_live_scanner.py      # Real-time crypto market scanner
│   │   ├── enhanced_crypto_backtest.py # Advanced crypto backtesting
│   │   ├── batch_runner.py             # Batch crypto testing runner
│   │   └── batch_test_output/          # Batch test results
│   ├── 📁 output/                      # Crypto output files and results
│   │   ├── backtest_results/           # Crypto backtest result files
│   │   └── trade_logs/                 # Crypto trade execution logs
│   ├── 📁 logs/                        # Crypto log files
│   ├── 📁 tools/                       # Crypto-specific tools
│   │   └── backtest_evaluator.py       # Advanced crypto backtest evaluator
│   ├── crypto_symbol_manager.py        # Crypto symbol management
│   └── list_crypto_assets.py           # Crypto asset listing utility
│
├── 📁 stocks/                          # Stock trading module
│   ├── 📁 input/                       # Stock input data files and configs
│   │   ├── stocks_assets.csv           # List of stock symbols to trade
│   │   └── config_stocks.yaml          # Stock-specific configurations
│   ├── 📁 scripts/                     # Stock-specific scripts
│   │   ├── stocks_backtest.py          # Main stock backtesting engine
│   │   ├── stocks_demo_live.py         # Live stock trading demo
│   │   └── stocks_live_scanner.py      # Real-time stock market scanner
│   ├── 📁 fyers/                       # Fyers API integration
│   │   ├── access_token.py             # 🔑 Fyers API credentials
│   │   ├── credentials.py              # Fyers credential management
│   │   └── generate_token.py           # Fyers token generation utility
│   ├── 📁 output/                      # Stock output files and results
│   │   ├── backtest_results/           # Stock backtest result files
│   │   └── trade_logs/                 # Stock trade execution logs
│   ├── 📁 logs/                        # Stock log files
│   ├── fyers_data_provider.py          # Main Fyers data provider
│   └── live_nse_quotes.py              # Live NSE quote fetcher
│
├── 📁 strategies/                      # 🎯 Trading strategies (shared by crypto & stocks)
│   ├── VWAPSigma2Strategy.py           # VWAP-based sigma strategy
│   ├── ml_ai_framework.py              # Machine learning framework
│   ├── market_inefficiency_strategy.py # Market inefficiency strategy
│   ├── advanced_strategy_hub.py        # Advanced strategy collection
│   ├── bb_rsi_strategy.py              # Bollinger Bands + RSI strategy
│   ├── enhanced_multi_factor.py        # Multi-factor enhanced strategy
│   ├── institutional_flow_strategy.py  # Institutional flow strategy
│   ├── macd_only_strategy.py           # MACD-only strategy
│   ├── optimized_crypto_v2.py          # Optimized crypto strategy v2
│   ├── rsi_macd_vwap_strategy.py       # RSI+MACD+VWAP combination
│   ├── sma_cross.py                    # Simple moving average crossover
│   ├── ultimate_profitable_strategy.py # Ultimate profitable strategy
│   ├── FiftyTwoWeekLowStrategy.py      # 52-week low strategy
│   └── README.md                       # Strategy documentation
│
├── 📁 tests/                           # Test files and utilities
│   ├── test_main.py                    # Main test suite
│   ├── test_backtest.py                # Backtest testing
│   ├── diagnostic_test.py              # System diagnostic tests
│   ├── quick_test.py                   # Quick functionality tests
│   └── test_limited_backtest.py        # Limited backtest tests
│
├── 📁 tools/                           # Utility tools and common modules
│   ├── launcher.py                     # 🚀 Main project launcher
│   ├── backtest_runner.py              # General backtest runner
│   ├── realtime_trader.py              # Real-time trading utility
│   └── verify_structure.py             # Project structure verifier
│
├── 📁 tools/                           # Utility tools and common modules
│   ├── launcher.py                     # Main project launcher
│   ├── realtime_trader.py              # Real-time trading utilities
│   ├── backtest_runner.py              # Backtest execution runner
│   ├── system_verification.py          # System health checker
│   ├── data_acquisition.py             # Data fetching and management (common)
│   ├── technical_analysis.py           # Technical analysis indicators (common)
│   ├── scanner.py                      # Market scanning utilities (common)
│   └── verify_structure.py             # Project structure validator
│
├── 📁 docs/                            # 📚 Documentation
│   ├── GETTING_STARTED.md              # Getting started guide
│   ├── PROJECT_STRUCTURE.md            # This file
│   ├── STRATEGIES_GUIDE.md             # Trading strategies guide
│   ├── API_DOCUMENTATION.md            # API documentation
│   └── TROUBLESHOOTING.md              # Common issues and solutions
│
├── 📁 venv/                            # Python virtual environment
├── 📁 .vscode/                         # VS Code configuration
├── 📁 .git/                            # Git repository data
│
├── README.md                           # Main project README
├── requirements.txt                    # Python dependencies
├── setup.bat                           # Windows setup script
├── setup.sh                            # Linux/Mac setup script
├── .gitignore                          # Git ignore rules
└── validate_strategies.py              # Strategy validation script
```

## 📋 File Descriptions & Usage Examples

### 🎯 Core Trading Strategies (`src/strategies/`)

#### `VWAPSigma2Strategy.py`
**Purpose**: VWAP-based trading strategy using statistical deviations
**Usage**: 
```python
from strategies.VWAPSigma2Strategy import VWAPSigma2Strategy
strategy = VWAPSigma2Strategy()
signals = strategy.generate_signals(data)
```

#### `ml_ai_framework.py`
**Purpose**: Machine learning and AI-based trading framework
**Features**: Neural networks, feature engineering, model training
**Usage**:
```python
from strategies.ml_ai_framework import MLAITradingFramework
ml_strategy = MLAITradingFramework()
ml_strategy.train_model(historical_data)
```

### 💰 Cryptocurrency Module (`crypto/`)

#### `crypto/scripts/crypto_backtest.py`
**Purpose**: Advanced cryptocurrency backtesting engine
**Features**: Portfolio tracking, risk metrics, performance analysis
**Usage**:
```bash
python crypto/scripts/crypto_backtest.py
```
**Output**: Comprehensive backtest reports with KPIs

#### `crypto/scripts/crypto_live_scanner.py`
**Purpose**: Real-time cryptocurrency market scanning
**Features**: Live price monitoring, signal detection, alerts
**Usage**:
```bash
python crypto/scripts/crypto_live_scanner.py
```

#### `crypto/input/crypto_assets.csv`
**Purpose**: List of cryptocurrency symbols for trading
**Format**:
```csv
symbol,exchange,active
BTC/USDT,binance,true
ETH/USDT,binance,true
```

### 📈 Stock Trading Module (`stocks/`)

#### `stocks/scripts/stocks_backtest.py`
**Purpose**: NSE/BSE stock backtesting using Fyers API
**Features**: Indian equity market analysis, Fyers integration
**Usage**:
```bash
python stocks/scripts/stocks_backtest.py
```

#### `stocks/fyers/access_token.py`
**Purpose**: Fyers API authentication credentials
**Content**:
```python
client_id = "YOUR_FYERS_CLIENT_ID"
access_token = "YOUR_FYERS_ACCESS_TOKEN"
```

#### `stocks/fyers_data_provider.py`
**Purpose**: Primary data provider for Indian stocks via Fyers API
**Features**: Historical data, live quotes, NSE/BSE data
**Usage**:
```python
from stocks.fyers_data_provider import fetch_nse_stock_data
data = fetch_nse_stock_data("RELIANCE", bars=100, interval="5m")
```

### 🛠️ Tools & Utilities (`tools/`)

#### `tools/launcher.py`
**Purpose**: Main project launcher with interactive menu
**Features**: Easy access to all functionalities
**Usage**:
```bash
python tools/launcher.py
```
**Menu Options**:
- Crypto backtesting
- Stock backtesting  
- Live trading
- Strategy validation

### 🧪 Testing (`tests/`)

#### `tests/diagnostic_test.py`
**Purpose**: System diagnostic and module loading tests
**Features**: Import validation, configuration checks
**Usage**:
```bash
python tests/diagnostic_test.py
```

## 🚀 Quick Start Commands

### Setup Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Run setup script
./setup.bat  # Windows
./setup.sh   # Linux/Mac
```

### Run Crypto Backtesting
```bash
python crypto/scripts/crypto_backtest.py
```

### Run Stock Backtesting
```bash
python stocks/scripts/stocks_backtest.py
```

### Launch Interactive Menu
```bash
python tools/launcher.py
```

### Validate All Strategies
```bash
python validate_strategies.py
```

## 📊 Input/Output Structure

### Input Files
- `crypto/input/crypto_assets.csv` - Crypto trading symbols
- `stocks/input/stocks_assets.csv` - Stock trading symbols  
- `crypto/input/*.yaml` - Crypto configuration files
- `stocks/input/*.yaml` - Stock configuration files

### Output Files
- `crypto/output/backtest_results/` - Crypto backtest performance reports
- `crypto/output/trade_logs/` - Crypto trade execution records
- `stocks/output/backtest_results/` - Stock backtest performance reports  
- `stocks/output/trade_logs/` - Stock trade execution records
- `crypto/logs/` - Crypto application and error logs
- `stocks/logs/` - Stock application and error logs

## 🔧 Configuration

### Main Crypto Config (`crypto/input/config_crypto.yaml`)
```yaml
trading:
  initial_capital: 10000
  risk_per_trade: 0.02
  max_positions: 5

data_sources:
  crypto: "ccxt"
  stocks: "fyers"
```

### Crypto Config (`crypto/input/config_crypto.yaml`)
```yaml
exchanges:
  primary: "binance"
  backup: "kraken"

timeframes:
  default: "1h"
  available: ["1m", "5m", "15m", "1h", "4h", "1d"]
```

---

**Last Updated**: 2025-01-11  
**Status**: ✅ Complete and Organized  
**Next Steps**: Follow GETTING_STARTED.md for setup instructions
