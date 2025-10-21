# 🚀 AlgoProject - Getting Started Guide

Welcome to AlgoProject! This comprehensive guide will help you set up and start using the advanced trading strategy platform.

**🎉 October 2025 Update**: Now featuring Multi-Theme UI, Individual User Credentials, AI Strategy Engine, and Modern Web Interface!

## 📋 Prerequisites

### System Requirements
- **Node.js**: 18+ (for web interface)
- **Python**: 3.8+ (for API backend)
- **Operating System**: Windows 10/11, macOS, or Linux
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 3GB free space
- **Browser**: Modern web browser (Chrome, Firefox, Safari, Edge)

### Trading Accounts (Optional)
- **Fyers Account**: For Indian stock trading (NSE/BSE) - Individual user credentials supported
- **Cryptocurrency Exchange**: Binance/Kraken/KuCoin etc. - 9 exchanges supported with tiered authentication

## 🛠️ Installation & Setup

### Quick Start (Recommended)

#### Option 1: Full Stack Web Platform
```powershell
# 1. Clone repository
git clone <repository-url>
cd AlgoProject

# 2. Start backend API (Terminal 1)
cd api
pip install fastapi uvicorn ccxt fyers-apiv3 pandas pydantic
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 3. Start frontend (Terminal 2)
cd frontend
npm install
npm run dev

# 4. Open browser: http://localhost:3000
```

#### Option 2: Legacy Python Interface
```bash
# Traditional setup for CLI-based usage
git clone <repository-url>
cd AlgoProject

# Create virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run setup
setup.bat    # Windows
./setup.sh   # Linux/Mac
```

## 🔑 API Configuration

### Fyers API Setup (For Stocks)

1. **Get Fyers Credentials**:
   - Login to [Fyers Developer Portal](https://api-portal.fyers.in/)
   - Create a new app and get `client_id`
   - Generate access token

2. **Configure Credentials**:
   ```bash
   # Navigate to Fyers directory
   cd stocks/fyers
   
   # Edit access_token.py
   # Add your credentials:
   client_id = "YOUR_FYERS_CLIENT_ID"
   access_token = "YOUR_FYERS_ACCESS_TOKEN"
   ```

3. **Generate Token** (if needed):
   ```bash
   python stocks/fyers/generate_token.py
   ```

### Crypto Exchange Setup (Optional)

For cryptocurrency trading, no API keys are required for basic backtesting as we use public data.

## 🎯 Quick Start Examples

### 1. Run Crypto Backtesting
```bash
# Navigate to project root
cd AlgoProject

# Run crypto backtest
python crypto/scripts/crypto_backtest.py
```

**Expected Output**:
```
🚀 Enhanced Crypto Backtest Scanner
================================================
📊 Strategy: VWAPSigma2Strategy
💰 Initial Capital: $10,000.00
📅 Backtest Period: 2024-12-12 to 2025-01-11
🔍 Scanning 20 crypto symbols using CCXT (Kraken)
⚡ Position Size: $1,000 per trade
================================================
📈 [01/20] Processing BTC/USDT... ✅ 5 trades | P&L: $245.67 | Win Rate: 60.0%
📈 [02/20] Processing ETH/USDT... ✅ 3 trades | P&L: $123.45 | Win Rate: 66.7%
...
✅ Backtest completed in 45.2s
💾 Results saved to output/crypto_backtest_detailed.csv
```

### 2. Run Stock Backtesting
```bash
# Run stock backtest
python stocks/scripts/stocks_backtest.py
```

**Expected Output**:
```
🚀 NSE/BSE Stock Backtest Scanner
================================================
📊 Strategy: VWAPSigma2Strategy
💰 Initial Capital: ₹100,000
📅 Backtest Period: 2024-12-12 to 2025-01-11
🔍 Scanning 50 NSE stocks using Fyers API
⚡ Position Size: ₹10,000 per trade
================================================
📈 [01/50] Processing RELIANCE... ✅ 7 trades | P&L: ₹2,456 | Win Rate: 71.4%
📈 [02/50] Processing TCS... ✅ 4 trades | P&L: ₹1,234 | Win Rate: 75.0%
...
✅ Backtest completed in 125.3s
💾 Results saved to output/stocks_backtest_detailed.csv
```

### 3. Use Interactive Launcher
```bash
# Launch main menu
python tools/launcher.py
```

**Interactive Menu**:
```
🚀 AlgoProject - Advanced Trading Strategy Platform
================================================
📊 Multi-Asset Trading: Crypto + Stocks
⚡ Advanced Backtesting & Live Trading

Please select an option:
[1] 🔸 Crypto Backtesting
[2] 📈 Stock Backtesting  
[3] 🔴 Live Trading (Demo)
[4] 🔍 Market Scanner
[5] 🧪 Strategy Validation
[6] 📊 Performance Reports
[0] ❌ Exit

Enter your choice (0-6): 
```

## 📊 Understanding the Output

### Backtest Results Structure
```
output/
├── crypto_backtest_detailed.csv     # Individual trade details
├── crypto_backtest_trades.csv       # Trade history with timestamps
├── crypto_backtest_summary.csv      # Performance metrics summary
├── stocks_backtest_detailed.csv     # Stock trade details
└── stocks_backtest_summary.csv      # Stock performance summary
```

### Key Performance Metrics

#### Portfolio Performance
- **Equity Final**: Final portfolio value
- **Return (%)**: Total return percentage
- **CAGR (%)**: Compound Annual Growth Rate
- **Sharpe Ratio**: Risk-adjusted return measure
- **Max Drawdown (%)**: Maximum loss from peak

#### Trade Statistics  
- **Win Rate (%)**: Percentage of profitable trades
- **Profit Factor**: Ratio of gross profit to gross loss
- **Avg Trade (%)**: Average trade return
- **Total Trades**: Number of trades executed

### Sample Performance Report
```
📊 COMPREHENSIVE BACKTEST PERFORMANCE REPORT
================================================

📅 BACKTEST PERIOD & DURATION
┌─────────────────┬──────────────┐
│ Metric          │ Value        │
├─────────────────┼──────────────┤
│ Start Date      │ 2024-12-12   │
│ End Date        │ 2025-01-11   │
│ Duration (Days) │ 30           │
│ Exposure Time   │ 45.67%       │
└─────────────────┴──────────────┘

💰 PORTFOLIO PERFORMANCE  
┌──────────────────────┬──────────────┐
│ Metric               │ Value        │
├──────────────────────┼──────────────┤
│ Equity Final         │ $12,456.78   │
│ Return               │ +24.57%      │
│ CAGR                 │ +298.84%     │
│ Sharpe Ratio         │ 1.845        │
│ Max. Drawdown        │ -8.23%       │
└──────────────────────┴──────────────┘

📈 TRADE STATISTICS
┌──────────────────────┬──────────────┐
│ Metric               │ Value        │
├──────────────────────┼──────────────┤
│ # Trades             │ 45           │
│ Win Rate             │ 66.67%       │
│ Best Trade           │ +8.45%       │
│ Worst Trade          │ -3.21%       │
│ Profit Factor        │ 2.34         │
└──────────────────────┴──────────────┘

🎯 STRATEGY ASSESSMENT & RECOMMENDATION
┌──────────────────┬─────────────────────────┐
│ Criteria         │ Status                  │
├──────────────────┼─────────────────────────┤
│ Profitability    │ ✅ Positive            │
│ Sharpe Ratio     │ ✅ Good (≥1.0)         │
│ Win Rate         │ ✅ Good (≥45%)         │
│ Profit Factor    │ ✅ Good (≥1.5)         │
│ Max Drawdown     │ ✅ Acceptable (≤20%)   │
│ Overall Score    │ ⭐ 5/6 stars           │
│ Risk Level       │ 🟢 LOW RISK            │
│ Recommendation   │ ✅ HIGHLY RECOMMENDED  │
└──────────────────┴─────────────────────────┘
```

## 🔧 Common Configuration Tasks

### 1. Modify Trading Symbols

**For Crypto**:
```bash
# Edit crypto assets file
nano crypto/input/crypto_assets.csv

# Add new symbols:
BTC/USDT,binance,true
ETH/USDT,binance,true  
ADA/USDT,binance,true
SOL/USDT,binance,true
```

**For Stocks**:
```bash
# Edit stock assets file
nano stocks/input/stocks_assets.csv

# Add new symbols:
RELIANCE.NS,NSE,true
TCS.NS,NSE,true
INFY.NS,NSE,true
HDFCBANK.NS,NSE,true
```

### 2. Adjust Strategy Parameters

```bash
# Edit strategy file
nano src/strategies/VWAPSigma2Strategy.py

# Modify parameters:
self.lookback_period = 20        # VWAP calculation period
self.sigma_multiplier = 2.0      # Deviation threshold
self.stop_loss_pct = 3.0         # Stop loss percentage
self.take_profit_pct = 6.0       # Take profit percentage
```

### 3. Change Backtesting Period

```bash
# Edit backtest script
nano crypto/scripts/crypto_backtest.py

# Modify date range:
start_date = end_date - timedelta(days=60)  # 60 days instead of 30
```

## 🧪 Testing Your Setup

### 1. Run Diagnostic Tests
```bash
python tests/diagnostic_test.py
```

**Expected Output**:
```
Testing module imports...
✅ MLAITradingFramework imported successfully
✅ MarketInefficiencyStrategy imported successfully
✅ AdvancedStrategyHub imported successfully
✅ All critical modules loaded successfully
```

### 2. Validate All Strategies
```bash
python validate_strategies.py
```

### 3. Quick Functionality Test
```bash
python tests/quick_test.py
```

## 📚 Next Steps

### 1. Learn Strategy Development
- Read `docs/STRATEGIES_GUIDE.md`
- Explore existing strategies in `src/strategies/`
- Create custom strategies

### 2. Optimize Performance
- Analyze backtest results
- Adjust strategy parameters
- Test different time periods

### 3. Live Trading (Advanced)
- Start with demo trading
- Implement risk management
- Monitor performance closely

## 🆘 Troubleshooting

### Common Issues & Solutions

#### Import Errors
```bash
# Error: ModuleNotFoundError
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### Fyers API Issues
```bash
# Error: Fyers authentication failed
# Solution: Check credentials in stocks/fyers/access_token.py
# Regenerate token if expired
python stocks/fyers/generate_token.py
```

#### Data Fetching Problems
```bash
# Error: No data returned
# Solution: Check internet connection and symbol format
# Verify exchange availability
```

#### Memory Issues
```bash
# Error: Out of memory during backtesting
# Solution: Reduce number of symbols or timeframe
# Process in smaller batches
```

### Getting Help

1. **Check Documentation**: Review all files in `docs/` folder
2. **Run Diagnostics**: Use `tests/diagnostic_test.py` 
3. **Validate Setup**: Run `validate_strategies.py`
4. **Check Logs**: Review files in `logs/` folder

## 🎉 Success Indicators

You're ready to start trading when you see:

✅ All dependencies installed successfully  
✅ Virtual environment activated  
✅ API credentials configured  
✅ Diagnostic tests pass  
✅ Sample backtest runs successfully  
✅ Output files generated correctly  

**Happy Trading! 🚀📈**

---

**Last Updated**: 2025-01-11  
**Version**: 1.0  
**Support**: Check docs/TROUBLESHOOTING.md for common issues
