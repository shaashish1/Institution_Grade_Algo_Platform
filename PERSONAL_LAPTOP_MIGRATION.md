# AlgoProject - Personal Laptop Migration Guide

## 🚀 Complete Trading Platform Setup (Crypto + Stocks)

This guide will help you migrate AlgoProject to your personal laptop with **full functionality** for both cryptocurrency and stock trading.

## 📋 Quick Migration Checklist

### ✅ **Step 1: Download/Clone Project**
```bash
# Option 1: Clone from GitHub
git clone https://github.com/your-username/AlgoProject.git
cd AlgoProject

# Option 2: Download ZIP and extract
# Download from GitHub and extract to desired location
```

### ✅ **Step 2: Run Automated Setup** 
```bash
# Run the complete setup script (handles everything automatically)
setup_complete.bat
```

**What it does:**
- ✅ Checks and installs Python 3.8+ if missing
- ✅ Creates virtual environment
- ✅ Installs ALL crypto + stock trading dependencies  
- ✅ Creates complete project structure
- ✅ Generates input files for crypto and stock assets
- ✅ Creates configuration templates
- ✅ Sets up Fyers API credentials template
- ✅ Creates launcher scripts
- ✅ Verifies all prerequisites

### ✅ **Step 3: Quick Launch Options**

After setup, you have multiple ways to start:

```bash
# OPTION 1: Unified Platform (Both Crypto + Stocks)
start_trading_platform.bat

# OPTION 2: Crypto Trading Only  
start_crypto_trading.bat

# OPTION 3: Stock Trading Only
start_stock_trading.bat

# OPTION 4: Command Line
python trading_launcher.py
```

## 💰 Crypto Trading Configuration

### Ready Out-of-the-Box!
- ✅ **100+ exchanges** supported via CCXT
- ✅ **Popular trading pairs** pre-loaded
- ✅ **Paper trading** enabled by default

### Add Your API Keys:
1. Edit: `crypto/input/config_crypto.yaml`
2. Add your exchange API credentials:
```yaml
exchanges:
  binance:
    enabled: true
    sandbox: true  # Start with paper trading
    api_key: "your_api_key_here"
    secret: "your_secret_here"
```

## 📈 Stock Trading Configuration  

### For Fyers API (Indian Stocks):

1. **Fill Credentials**: Edit `stocks/fyers/credentials.py`
```python
user_name = "your_fyers_user_id"
pin1 = "1"  # Your PIN digits
pin2 = "2"
pin3 = "3" 
pin4 = "4"
client_id = "your_app_id-100"
secret_key = "your_app_secret_key"
totp_key = "your_totp_secret_key"
```

2. **Generate Token**: Run the token generation script
```bash
cd stocks/fyers
python generate_token.py
```

3. **Update Config**: Edit `stocks/input/config_stocks.yaml`
```yaml
fyers:
  enabled: true
  paper_trading: true  # Start with paper trading
  client_id: "your_fyers_client_id_here"
```

## 🏗️ Project Structure Created

```
AlgoProject/
├── crypto/                      # Crypto trading module
│   ├── input/
│   │   ├── crypto_assets.csv    # 15 popular crypto pairs
│   │   └── config_crypto.yaml   # Crypto configuration
│   ├── output/                  # Trading results
│   └── logs/                    # Trading logs
├── stocks/                      # Stock trading module  
│   ├── input/
│   │   ├── stock_assets.csv     # 15 popular Indian stocks
│   │   └── config_stocks.yaml   # Stock configuration
│   ├── fyers/
│   │   └── credentials.py       # Fyers API credentials
│   ├── output/                  # Trading results
│   └── logs/                    # Trading logs
├── tools/                       # Utilities and launchers
├── strategies/                  # Trading strategies
├── venv/                        # Python virtual environment
├── setup_complete.bat           # Complete setup script
├── trading_launcher.py          # Main launcher
├── crypto_launcher.py           # Crypto-focused launcher
├── stock_launcher.py            # Stock-focused launcher
├── start_trading_platform.bat   # Quick start (unified)
├── start_crypto_trading.bat     # Quick start (crypto)
└── start_stock_trading.bat      # Quick start (stocks)
```

## 📦 Dependencies Installed

### Crypto Trading:
- `ccxt` - 100+ crypto exchanges
- `websocket-client` - Real-time data
- `pandas, numpy` - Data analysis
- `matplotlib` - Charting

### Stock Trading:
- `fyers-apiv3` - Fyers API (if available)
- `tvdatafeed` - TradingView data
- `nsepython` - NSE data  
- `yfinance` - Yahoo Finance data
- `backtrader` - Backtesting framework

### Analysis & Utilities:
- `ta, pandas-ta` - Technical analysis
- `scipy, scikit-learn` - Statistics/ML
- `rich, colorama` - Beautiful output
- `pyyaml, python-dotenv` - Configuration

## 🎯 Usage Examples

### Crypto Trading:
```bash
# Start crypto platform
start_crypto_trading.bat

# Or command line
python crypto_launcher.py
```

**Features:**
- 🔍 Crypto scanner
- 📊 Backtesting
- 🚀 Live trading  
- 📈 Technical analysis

### Stock Trading:
```bash
# Start stock platform  
start_stock_trading.bat

# Or command line
python stock_launcher.py
```

**Features:**
- 🔍 Stock scanner
- 📊 Backtesting
- 🚀 Live trading
- 📈 Market analysis

### Unified Platform:
```bash
# Start complete platform
start_trading_platform.bat

# Or command line  
python trading_launcher.py
```

**Features:**
- 💰 Crypto trading
- 📈 Stock trading
- 🔧 System utilities
- 📊 Combined analysis

## ⚠️ Important Notes

### Security:
- ✅ Always start with **paper trading**
- ✅ Test strategies before live trading
- ✅ Use small amounts initially
- ✅ Keep API keys secure

### Prerequisites:
- ✅ Python 3.8+ (auto-installed by setup)
- ✅ Internet connection for API access
- ✅ Valid exchange/broker accounts
- ✅ API credentials configured

### Network Requirements:
- ✅ **Personal laptops**: Full functionality
- ✅ **Corporate networks**: May have restrictions
- ✅ **Crypto trading**: Usually works everywhere
- ✅ **Stock trading**: Requires API access

## 🔧 Troubleshooting

### Setup Issues:
```bash
# Re-run complete setup
setup_complete.bat

# Check system verification
python tools/system_verification.py

# Manual dependency install
pip install -r requirements.txt
```

### Launch Issues:
```bash
# Activate virtual environment manually
venv\Scripts\activate.bat

# Run launchers manually
python trading_launcher.py
python crypto_launcher.py  
python stock_launcher.py
```

### API Issues:
- Check credentials in config files
- Verify API keys are active
- Test with paper trading first
- Check exchange/broker status

## 📚 Additional Resources

- **Main Documentation**: `README.md`
- **Project Specifications**: `Project_Detailed_Specification.txt`
- **Crypto Guide**: `crypto/README.md`
- **Stock Guide**: `stocks/README.md`
- **Fyers Setup**: `docs/FYERS_SETUP.md`

## 🎉 Migration Complete!

Your AlgoProject is now ready for both crypto and stock trading on your personal laptop!

### Quick Start:
1. ✅ Run `setup_complete.bat`
2. ✅ Configure API credentials  
3. ✅ Launch with `start_trading_platform.bat`
4. ✅ Start with paper trading
5. ✅ Begin live trading when ready

**Happy Trading! 🚀📈💰**
