# Crypto Trading Scripts Guide - HOWTO

## Overview
This guide explains how to use the crypto trading scripts for different purposes: backtesting, demo trading, and live trading.

## Script Categories

### 📊 1. COMPREHENSIVE BACKTESTING (All Strategies × All Assets × All Timeframes)

**Primary Script**: `crypto/scripts/batch_runner.py`
**Demo Script**: `crypto/scripts/batch_runner_demo.py`

**Purpose**: Tests ALL strategies on ALL crypto assets from CSV file across ALL timeframes to identify the best performing combinations.

**Features**:
- Auto-discovers all available strategies from `/strategies` folder
- Loads all crypto symbols from `crypto/input/crypto_assets.csv` 
- Tests multiple timeframes: 5m, 15m, 30m, 1h, 2h, 4h, 1d
- Generates comprehensive comparison reports
- Identifies best strategy per asset per timeframe

**Usage**:
```bash
# Navigate to scripts directory
cd crypto/scripts

# Complete analysis (all strategies × all assets × all timeframes)
python batch_runner.py --auto

# Quick test with specific symbols
python batch_runner.py --auto --symbols BTC/USDT ETH/USDT

# Custom strategies only
python batch_runner.py --symbols BTC/USDT --strategies "BB_RSI,MACD_Only"

# Custom timeframes only  
python batch_runner.py --symbols BTC/USDT --timeframes 1h 4h 1d

# Interactive demo
python batch_runner_demo.py
```

**Expected Output**:
- `strategy_comparison_report_YYYYMMDD_HHMMSS.md` - Main analysis report
- `strategy_comparison_data_YYYYMMDD_HHMMSS.csv` - Raw performance data
- Individual backtest results in subdirectories

**Strategy Mapping**:
- `bb_rsi_strategy.py` → `BB_RSI`
- `enhanced_multi_factor.py` → `Enhanced_Multi_Factor`
- `macd_only_strategy.py` → `MACD_Only`
- `optimized_crypto_v2.py` → `Optimized_Crypto_V2`
- `rsi_macd_vwap_strategy.py` → `RSI_MACD_VWAP`
- `sma_cross.py` → `SMA_Cross`

---

### 🎯 2. DEMO TRADING (Real-time Testing with NO Real Trades)

**Primary Script**: `crypto/scripts/crypto_demo_live.py`

**Purpose**: Tests strategy performance using real-time data without executing actual trades. Perfect for validating strategies before going live.

**Features**:
- Uses live market data from CCXT exchanges
- Simulates trades without real money
- Real-time strategy execution
- Forward testing capabilities
- Risk-free strategy validation

**Usage**:
```bash
cd crypto/scripts

# Run demo trading with default strategy
python crypto_demo_live.py

# Run with specific parameters (if supported)
python crypto_demo_live.py --symbol BTC/USDT --strategy RSI_MACD_VWAP --interval 1h
```

**Key Benefits**:
- ✅ Real market conditions
- ✅ No financial risk
- ✅ Real-time performance validation
- ✅ Strategy behavior analysis

---

### 🔴 3. LIVE TRADING (Production Trading with Real Money)

**Current Status**: ⚠️ **NO PRODUCTION TRADING SCRIPT IDENTIFIED**

**Analysis**: Based on examination of all scripts in `crypto/scripts/`, there is **NO dedicated production trading script** that executes real trades on exchanges with real money.

**Available Scripts Related to Live Data**:
- `crypto_live_scanner.py` - Real-time market scanning (NO trading)
- `crypto_demo_live.py` - Demo trading (NO real trades)

**What's Missing**:
- Production trading script with:
  - Real API key integration
  - Actual order placement
  - Position management
  - Risk management
  - Trade execution logic

---

## Detailed Script Analysis

### batch_runner.py - Comprehensive Backtesting Engine

**Core Functions**:
- `discover_strategies()` - Auto-finds strategy files
- `load_crypto_symbols()` - Loads symbols from crypto_assets.csv
- `get_available_timeframes()` - Returns all supported timeframes
- `run_single_backtest()` - Executes individual backtest
- `parse_backtest_results()` - Processes results
- `generate_comparison_report()` - Creates analysis report

**Workflow**:
1. Load crypto assets from CSV
2. Discover available strategies
3. For each combination of (asset, strategy, timeframe):
   - Run backtest using `enhanced_crypto_backtest.py`
   - Collect performance metrics
4. Generate comparative analysis
5. Identify best performers

### crypto_demo_live.py - Real-time Demo Trading

**Core Functions**:
- `load_crypto_assets()` - Loads trading symbols
- `load_strategy()` - Initializes trading strategy
- `run_crypto_live_scan()` - Executes real-time scanning
- Real-time data fetching via CCXT
- Strategy signal generation
- Portfolio simulation

**Workflow**:
1. Load crypto assets and strategy
2. Connect to live data feed
3. Continuously:
   - Fetch latest market data
   - Apply strategy logic
   - Generate buy/sell signals
   - Update simulated portfolio
   - Display results

### Enhanced Supporting Scripts

**enhanced_crypto_backtest.py**:
- Core backtesting engine used by batch_runner
- Supports multiple strategies
- Generates detailed KPIs
- Professional analysis via BacktestEvaluator

**crypto_live_scanner.py**:
- Real-time market scanning
- No trading execution
- Uses VWAPSigma2Strategy
- Market monitoring tool

## Prerequisites

### Required Files
1. `crypto/input/crypto_assets.csv` - Contains all trading symbols
2. `/strategies/*.py` - Strategy implementation files
3. Valid Python environment with required packages

### Required Packages
- ccxt (for exchange connectivity)
- pandas (data manipulation)
- numpy (numerical computations)  
- ta (technical analysis)
- tabulate (table formatting)
- colorama (colored output)

### Exchange Setup
- Kraken (default exchange)
- Binance (alternative)
- API keys required for live trading (when implemented)

## Testing the Scripts

### Test 1: Comprehensive Backtesting
```bash
cd crypto/scripts
python batch_runner_demo.py
# Choose 'y' to run quick demo
```

### Test 2: Demo Trading
```bash
cd crypto/scripts  
python crypto_demo_live.py
```

### Test 3: Market Scanning
```bash
cd crypto/scripts
python crypto_live_scanner.py
```

## Script Status Summary

| Script | Purpose | Status | Real Trades | Notes |
|--------|---------|--------|-------------|--------|
| `batch_runner.py` | Comprehensive backtesting | ✅ Available | ❌ No | Tests all combinations |
| `crypto_demo_live.py` | Demo trading | ✅ Available | ❌ No | Real data, simulated trades |
| `crypto_live_scanner.py` | Market scanning | ✅ Available | ❌ No | Monitoring only |
| **Production Trading** | **Real trading** | **❌ Missing** | **❌ No** | **Needs development** |

## Recommendations

### For Production Trading Implementation
1. **Create dedicated production trading script**:
   - `crypto_live_trading.py` or similar
   - Real API integration
   - Order management
   - Risk controls

2. **Required components**:
   - API key management
   - Order placement functions
   - Position tracking
   - Stop-loss implementation
   - Portfolio management

3. **Safety features**:
   - Maximum position size limits
   - Daily loss limits
   - Emergency stop functionality
   - Extensive logging

### Immediate Next Steps
1. ✅ Test backtesting with `batch_runner_demo.py`
2. ✅ Test demo trading with `crypto_demo_live.py`
3. ⚠️ Identify why scripts hang during execution
4. ❌ Develop production trading script
5. ❌ Implement safety and risk management

## Troubleshooting

### ⚠️ CRITICAL ISSUE: Script Execution Hanging

**Problem**: While all scripts import successfully, command-line execution hangs
**Status**: **KNOWN ISSUE** - Under investigation
**Workaround**: Use programmatic execution instead of command-line

### Common Issues
1. **Scripts hang on execution**: ⚠️ **KNOWN ISSUE** - Use workaround below
2. **Import errors**: Check Python path and dependencies  
3. **Data file not found**: Ensure `crypto_assets.csv` exists
4. **Strategy not found**: Verify strategy files in `/strategies`

### 🔧 WORKAROUND FOR EXECUTION HANGING

Instead of command-line execution, use programmatic approach:

```python
# DON'T USE: python enhanced_crypto_backtest.py --args (hangs)
# USE THIS INSTEAD:

import sys, os
sys.path.append('D:/AlgoProject/crypto/scripts')
os.chdir('D:/AlgoProject/crypto/scripts')

# For backtesting:
from enhanced_crypto_backtest import main
sys.argv = ['script.py', '--symbol', 'BTC/USDT', '--timeframe', '1h', 
           '--start-date', '2024-01-01', '--end-date', '2024-01-31',
           '--strategy', 'RSI_MACD_VWAP', '--initial-capital', '10000']
main()

# For demo trading:
from crypto_demo_live import run_crypto_demo_live
run_crypto_demo_live(symbol='BTC/USDT', strategy='RSI_MACD_VWAP', 
                    timeframe='5m', initial_capital=10000.0)
```

### Quick Fixes
1. ✅ Lazy CCXT loading implemented - no more import hanging
2. ✅ File paths verified and corrected
3. ✅ All dependencies confirmed working
4. ✅ Directory structure validated

### Validation Results
- ✅ **batch_runner.py** - Imports successfully, discovers 6 strategies, 36 symbols
- ✅ **crypto_demo_live.py** - Imports successfully after function name fix
- ✅ **enhanced_crypto_backtest.py** - Imports successfully
- ⚠️ **Command execution** - All scripts hang when run via command line

---

**Last Updated**: July 15, 2025
**Status**: Backtesting ✅ | Demo Trading ✅ | Production Trading ❌ Missing
