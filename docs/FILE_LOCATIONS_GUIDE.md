# 📁 AlgoProject File Locations Guide

## 🎯 **Complete File Structure Overview**

Based on your current AlgoProject setup, here's where all files are saved:

### 📊 **Trading Pair CSV Files**
**Location:** `d:\Institution_Grade_Algo_Platform\crypto\input\`

When you run `--save-pairs`, CSV files are created here:
```
d:\Institution_Grade_Algo_Platform\crypto\input\
├── delta_spot_usdt.csv         # Spot USDT pairs (BTC/USDT, ETH/USDT, etc.)
├── delta_spot_btc.csv          # Spot BTC pairs  
├── delta_spot_eth.csv          # Spot ETH pairs
├── delta_perpetual_usdt.csv    # Perpetual futures USDT
├── delta_futures_usdt.csv      # Futures contracts USDT
├── delta_futures_btc.csv       # Futures contracts BTC
├── delta_options_calls.csv     # Call options
├── delta_options_puts.csv      # Put options
├── delta_other_pairs.csv       # Other trading pairs
└── delta_pairs_summary.csv     # Master summary file
```

### 📈 **Backtest Results**
**Location:** `d:\Institution_Grade_Algo_Platform\crypto\output\`

Backtest results are saved here with timestamps:
```
d:\Institution_Grade_Algo_Platform\crypto\output\
├── multi_strategy_backtest_20250716_HHMMSS.csv   # Latest backtest results
├── multi_strategy_backtest_20250716_155409.csv   # Previous runs
├── multi_strategy_backtest_20250716_155922.csv
├── multi_strategy_backtest_20250716_160025.csv
└── ... (more timestamped files)
```

**Example backtest CSV content:**
```csv
Strategy,Symbol,Timeframe,Trades,Total_Profit_Pct,Profit_Factor,Win_Rate_Pct,Sharpe_Ratio,Max_Drawdown_Pct,Composite_Score
RSI_30_70,BTC/USDT,1h,15,12.50,1.85,66.7,1.42,8.30,75.2
RSI_25_75,ETH/USDT,4h,8,8.75,1.65,62.5,1.28,5.20,68.5
```

### 📝 **Log Files**
**Location:** `d:\Institution_Grade_Algo_Platform\crypto\logs\`

System logs and debug information:
```
d:\Institution_Grade_Algo_Platform\crypto\logs\
├── delta_backtest_YYYYMMDD.log    # Daily backtest logs
├── data_acquisition.log           # Data fetching logs
└── error_logs/                    # Error tracking
```

### 🔧 **Helper Scripts & Tests**
**Location:** `d:\Institution_Grade_Algo_Platform\helper_scripts\`

Test files and utilities:
```
d:\Institution_Grade_Algo_Platform\helper_scripts\
├── test_rate_limiting.py          # Rate limiting tests
├── test_ccxt_simple.py           # Basic CCXT tests
├── delta_pairs_fetcher.py        # Pair fetching utility
├── quick_delta_test.py           # Quick connection test
└── logs/                         # Helper script logs
```

### 📚 **Documentation**
**Location:** `d:\Institution_Grade_Algo_Platform\docs\`

All guides and documentation:
```
d:\Institution_Grade_Algo_Platform\docs\
├── DELTA_EXCHANGE_PAIRS_GUIDE.md     # Pair management guide
├── RATE_LIMITING_IMPLEMENTATION.md   # Rate limiting details
├── CRYPTO_README.md                  # Crypto module documentation
└── ... (other documentation files)
```

## 🎯 **File Creation Commands & Locations**

### 1. **Save Trading Pairs to CSV**
```bash
python crypto\scripts\delta_backtest_strategies.py --save-pairs
```
**Files Created:** `d:\Institution_Grade_Algo_Platform\crypto\input\delta_*.csv`

### 2. **Run Backtests (Results to CSV)**
```bash
python crypto\scripts\delta_backtest_strategies.py --symbols BTC/USDT ETH/USDT
```
**Files Created:** `d:\Institution_Grade_Algo_Platform\crypto\output\multi_strategy_backtest_*.csv`

### 3. **Interactive Pair Selection**
```bash
python crypto\scripts\delta_backtest_strategies.py --interactive
```
**Files Created:** Results go to `crypto\output\` with timestamp

### 4. **Load Specific Pair Types**
```bash
python crypto\scripts\delta_backtest_strategies.py --load-csv spot_usdt
```
**Files Used:** `d:\Institution_Grade_Algo_Platform\crypto\input\delta_spot_usdt.csv`

## 📊 **Current File Status Check**

### **Input Directory Status:**
```
d:\Institution_Grade_Algo_Platform\crypto\input\
├── crypto_assets.csv (existing)
└── [Delta CSV files will be created here]
```

### **Output Directory Status:**
```
d:\Institution_Grade_Algo_Platform\crypto\output\
├── [Multiple existing backtest files]
├── multi_strategy_backtest_*.csv (your Delta results)
└── backtest_results/ (subdirectory)
```

## 🔍 **File Naming Conventions**

### **Pair CSV Files:**
- Format: `delta_{category}.csv`
- Categories: `spot_usdt`, `futures_usdt`, `options_calls`, etc.

### **Backtest Results:**
- Format: `multi_strategy_backtest_{YYYYMMDD_HHMMSS}.csv`
- Example: `multi_strategy_backtest_20250716_143025.csv`

### **Summary Files:**
- `delta_pairs_summary.csv` - Overview of all pair categories
- Individual CSV files for each trading pair type

## 🎯 **Quick File Location Test**

To see exactly where your files are saved, run:

```bash
# 1. Save pairs and see input location
python crypto\scripts\delta_backtest_strategies.py --save-pairs

# 2. Run backtest and see output location  
python crypto\scripts\delta_backtest_strategies.py --symbols BTC/USDT --top 3

# 3. Check file locations
dir crypto\input\delta_*.csv
dir crypto\output\multi_strategy_*.csv
```

## 📁 **File Management Tips**

1. **Input Files** (`crypto\input\`) - Pair configurations, reusable
2. **Output Files** (`crypto\output\`) - Results, timestamped, accumulate over time
3. **Logs** (`crypto\logs\`) - Debug info, system monitoring
4. **Docs** (`docs\`) - Guides and documentation
5. **Helper Scripts** (`helper_scripts\`) - Testing utilities

## 🎉 **Summary**

- **Trading Pairs:** `d:\Institution_Grade_Algo_Platform\crypto\input\delta_*.csv`
- **Backtest Results:** `d:\Institution_Grade_Algo_Platform\crypto\output\multi_strategy_backtest_*.csv`  
- **Documentation:** `d:\Institution_Grade_Algo_Platform\docs\*.md`
- **Test Scripts:** `d:\Institution_Grade_Algo_Platform\helper_scripts\*.py`

All files are organized by function and include timestamps for easy tracking!
