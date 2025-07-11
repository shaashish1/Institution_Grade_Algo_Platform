# 🏠 Personal Laptop Setup Guide

## 🎯 Quick Setup for Personal Laptop

This guide helps you transfer and setup AlgoProject on your personal laptop where there are no corporate firewall restrictions. Focus is on **crypto trading only** since Fyers/stocks require unrestricted network access.

---

## 📋 Prerequisites

### System Requirements
- **Python 3.8+** (Download from [python.org](https://www.python.org/downloads/))
- **Windows 10/11** (MacOS/Linux also supported)
- **4GB+ RAM** (8GB+ recommended)
- **2GB+ free disk space**
- **Stable internet connection** (for crypto APIs)

### During Python Installation
- ✅ **IMPORTANT**: Check "Add Python to PATH"
- ✅ Check "Install pip"
- ✅ Choose "Add Python to environment variables"

---

## 🚀 Installation Methods

### Method 1: Direct Git Clone (Recommended)
```bash
# Open Command Prompt or PowerShell
git clone https://github.com/yourusername/AlgoProject.git
cd AlgoProject
setup.bat
```

### Method 2: Download ZIP from GitHub
1. Go to GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract to desired location
4. Open Command Prompt in extracted folder
5. Run `setup.bat`

### Method 3: Transfer from Corporate Laptop
1. Copy entire AlgoProject folder to USB drive
2. Transfer to personal laptop
3. Open Command Prompt in AlgoProject folder
4. Run `setup.bat`

---

## 🔧 Automated Setup Process

### Run Setup Script
```bash
# Navigate to AlgoProject folder
cd AlgoProject

# Run the automated setup
setup.bat
```

### What the Setup Does:
1. ✅ Checks Python installation
2. ✅ Creates virtual environment
3. ✅ Installs crypto trading dependencies
4. ✅ Sets up project structure
5. ✅ Creates crypto-focused launcher
6. ✅ Launches crypto trading platform

---

## 💰 Crypto Trading Features

### Available Features:
- **🔍 Real-time Crypto Scanner** - Find trading opportunities
- **📊 Backtesting Engine** - Test strategies on historical data
- **🚀 Live Trading** - Execute trades on 100+ exchanges
- **📈 Technical Analysis** - Advanced charting and indicators
- **⚙️ Strategy Builder** - Create custom trading strategies

### Supported Exchanges:
- Binance
- Coinbase Pro
- Kraken
- Bitfinex
- KuCoin
- And 100+ more via CCXT

---

## 📁 Project Structure (Crypto Focus)

```
AlgoProject/
├── crypto/
│   ├── input/           # Crypto configuration files
│   ├── output/          # Trading results and reports
│   └── logs/            # Crypto trading logs
├── strategies/          # Trading strategies
├── tools/               # Utility scripts
├── crypto_launcher.py   # Main crypto launcher
├── crypto_main.py       # Crypto trading script
├── setup.bat           # Automated setup
└── requirements.txt     # Dependencies
```

---

## 🎮 Using the Platform

### Launch Methods:

#### Option 1: Crypto Launcher (Recommended)
```bash
python crypto_launcher.py
```

#### Option 2: Direct Crypto Script
```bash
python crypto_main.py
```

#### Option 3: Main Script with Crypto Flag
```bash
python main.py --crypto
```

### First Time Configuration:
1. Launch crypto platform
2. Choose "Configuration" from menu
3. Set up your preferred exchanges
4. Configure trading parameters
5. Start with paper trading

---

## 🔒 Security Best Practices

### API Key Management:
- **Never commit API keys to GitHub**
- Store in local config files only
- Use paper trading mode first
- Start with small amounts

### Safe Trading:
- Always test strategies in backtest mode
- Use stop-loss orders
- Start with demo/paper trading
- Monitor positions regularly

---

## 🛠️ Troubleshooting

### Common Issues:

#### Python Not Found
```bash
# Solution: Add Python to PATH
# Reinstall Python with "Add to PATH" checked
```

#### Package Installation Fails
```bash
# Solution: Upgrade pip and try again
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Import Errors
```bash
# Solution: Activate virtual environment
venv\Scripts\activate
pip install missing-package
```

#### Crypto API Errors
```bash
# Solution: Check internet connection
# Verify exchange is accessible
ping api.binance.com
```

### Network Test:
```bash
# Test crypto exchange connectivity
python -c "import ccxt; print(ccxt.binance().fetch_ticker('BTC/USDT'))"
```

---

## 📊 Getting Started with Crypto Trading

### Step 1: Run System Check
```bash
python crypto_launcher.py
# Choose option 8: System Health Check
```

### Step 2: Configure Exchanges
1. Edit `crypto/input/config_crypto.yaml`
2. Add your exchange API credentials
3. Set trading parameters

### Step 3: Paper Trading
1. Start with paper trading mode
2. Test your strategies risk-free
3. Monitor performance

### Step 4: Live Trading (When Ready)
1. Fund your exchange account
2. Switch to live trading mode
3. Start with small amounts
4. Monitor closely

---

## 📈 Example Configuration

### Basic Crypto Config:
```yaml
# crypto/input/config_crypto.yaml
exchanges:
  binance:
    api_key: "your_api_key"
    secret: "your_secret"
    sandbox: true  # Start with paper trading

trading:
  base_currency: "USDT"
  symbols: ["BTC/USDT", "ETH/USDT", "ADA/USDT"]
  max_position_size: 100  # USD
  
strategies:
  - name: "simple_ma"
    enabled: true
    parameters:
      fast_ma: 20
      slow_ma: 50
```

---

## 🆘 Support Resources

### Documentation:
- `docs/PROJECT_STRUCTURE.md` - Detailed project structure
- `docs/GETTING_STARTED.md` - Comprehensive guide
- `docs/strategies-module.md` - Strategy development

### Community:
- GitHub Issues for bug reports
- README.md for general help
- Code comments for technical details

### Online Resources:
- [CCXT Documentation](https://ccxt.readthedocs.io/) - Exchange integration
- [Pandas Documentation](https://pandas.pydata.org/) - Data analysis
- [TA-Lib Documentation](https://ta-lib.org/) - Technical analysis

---

## 🎉 Success Checklist

- ✅ Python 3.8+ installed with PATH
- ✅ AlgoProject folder downloaded/transferred
- ✅ setup.bat executed successfully
- ✅ Virtual environment created
- ✅ Dependencies installed
- ✅ Crypto launcher working
- ✅ System health check passed
- ✅ Configuration file setup
- ✅ Paper trading tested
- ✅ Ready for live trading

---

## 💡 Pro Tips

1. **Start Small**: Begin with paper trading and small amounts
2. **Diversify**: Don't put all funds in one strategy
3. **Monitor**: Keep track of performance and adjust
4. **Learn**: Study market patterns and improve strategies
5. **Backup**: Regularly backup your configuration and logs
6. **Update**: Keep the platform updated with latest features

---

**🏠 Perfect for Personal Use**: No corporate restrictions, full crypto market access, unlimited trading potential!
