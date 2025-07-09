# 🪙 Cryptocurrency Trading Module

> **Complete documentation for cryptocurrency trading using CCXT library**  
> Part of the [AlgoProject Enterprise Trading Platform](../README.md)

## Overview
This module handles cryptocurrency trading using CCXT library to connect with multiple exchanges. No API keys required for demo trading with real market data.

## 🚀 Features

### **Supported Exchanges**
- Binance
- Kraken  
- Coinbase Pro
- KuCoin
- Bitfinex
- Huobi
- OKX
- Gate.io
- Bybit

### **Trading Pairs**
- **900+ Crypto Pairs** across all exchanges
- **Major Assets**: BTC, ETH, ADA, DOT, LINK, etc.
- **Fiat Pairs**: USD, EUR, GBP, USDT, USDC
- **Cross Trading**: All major cryptocurrency pairs

## 📁 Directory Structure

```
crypto/
├── scripts/                    # Crypto trading scripts
│   ├── crypto_demo_live.py     # Live demo with real prices
│   ├── crypto_backtest.py      # Historical backtesting
│   └── crypto_live_scanner.py  # Real-time opportunity scanner
└── crypto_symbol_manager.py    # Crypto symbol management utility
```

### **Related Files**
- `input/crypto_assets.csv` - 900+ trading pairs
- `input/crypto_assets_test.csv` - Test trading pairs
- `config/config_crypto.yaml` - Crypto-specific configuration
- `output/` - Trading results and logs

## 🚀 Quick Start

### **1. Live Demo Trading**
```bash
# Navigate to project root
cd AlgoProject

# Run live crypto demo
python crypto/scripts/crypto_demo_live.py
```

**Features:**
- ✅ Real-time price data from exchanges
- ✅ Virtual portfolio with $10,000 starting balance
- ✅ No actual trades executed (100% safe)
- ✅ VWAP Sigma-2 strategy implementation
- ✅ Real-time P&L tracking

### **2. Backtesting**
```bash
# Run crypto backtesting
python crypto/scripts/crypto_backtest.py
```

**Features:**
- ✅ Historical data analysis
- ✅ Strategy performance metrics
- ✅ Risk-adjusted returns
- ✅ Drawdown analysis

### **3. Live Scanner**
```bash
# Run real-time opportunity scanner
python crypto/scripts/crypto_live_scanner.py
```

**Features:**
- ✅ Real-time opportunity detection
- ✅ Multi-exchange scanning
- ✅ Signal generation and alerts
- ✅ Technical analysis indicators

## 📊 Configuration

### **Crypto Assets**
The file `input/crypto_assets.csv` contains all supported trading pairs:

```csv
symbol,exchange,base,quote,active
BTC/USDT,binance,BTC,USDT,true
ETH/USDT,binance,ETH,USDT,true
BTC/USD,kraken,BTC,USD,true
ETH/EUR,kraken,ETH,EUR,true
...
```

### **Exchange Selection**
Modify the exchange in scripts:

```python
# In crypto_demo_live.py
EXCHANGE = "kraken"  # Change to: binance, coinbase, kucoin, etc.
```

## 🔧 Technical Details

### **Data Provider**
- **Library**: CCXT (CryptoCurrency eXchange Trading Library)
- **Data Type**: Real-time and historical OHLCV
- **Latency**: <100ms for most exchanges
- **Rate Limits**: Automatically handled

### **Supported Timeframes**
- `1m`, `5m`, `15m`, `30m` - Minute intervals
- `1h`, `2h`, `4h`, `6h`, `12h` - Hour intervals
- `1d`, `3d`, `1w` - Daily/Weekly intervals

### **Data Structure**
```python
# DataFrame columns
['timestamp', 'open', 'high', 'low', 'close', 'volume']

# Example data
timestamp                open     high     low      close    volume
2025-01-09 10:30:00     43250.5  43280.0  43200.1  43265.8  1250.5
```

## 🛡️ Security & Risk Management

### **Demo Mode Safety**
- ✅ **No Real Trading**: All operations are simulated
- ✅ **Virtual Portfolio**: No actual money at risk
- ✅ **Real Data**: Uses live exchange data for accuracy
- ✅ **Paper Trading**: Perfect for strategy testing

### **Live Trading (Future)**
When ready for live trading:
1. Add exchange API credentials
2. Enable live trading mode
3. Start with small amounts
4. Implement proper risk management

## 📈 Performance Examples

### **Expected Output (Demo Trading)**
```
🔴 LIVE Crypto Demo - Forward Testing Mode
==============================================================================
⚠️  DEMO MODE: Uses real-time exchange data but NO ACTUAL TRADES
📊 Perfect for testing strategy performance before going live!
==============================================================================
🔍 Demo trading 900+ crypto symbols across 9 exchanges
📊 Strategy: VWAPSigma2Strategy
💰 Virtual Portfolio: $10,000 starting balance
🔄 Continuous demo... Press Ctrl+C to stop
==============================================================================

📊 Portfolio Performance:
┌─────────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Symbol          │ Position    │ Entry Price │ Current     │ P&L         │
├─────────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ BTC/USDT        │ LONG        │ $43,250.50  │ $43,465.20  │ +$214.70    │
│ ETH/USDT        │ SHORT       │ $2,850.30   │ $2,840.15   │ +$10.15     │
└─────────────────┴─────────────┴─────────────┴─────────────┴─────────────┘

💰 Total Portfolio Value: $10,224.85 (+2.25%)
📈 Total Trades: 12 | 🟢 Profitable: 8 | 🔴 Losses: 4
⚡ Success Rate: 66.7% | 📊 Avg Profit: $28.73
```

## 🔧 Advanced Configuration

### **Custom Exchanges**
Add new exchanges by modifying the exchange list:

```python
# In crypto/scripts/crypto_demo_live.py
SUPPORTED_EXCHANGES = [
    'binance', 'kraken', 'coinbase', 'kucoin', 
    'bitfinex', 'huobi', 'okx', 'gateio', 'bybit'
]
```

### **Strategy Parameters**
Modify strategy parameters in the scripts:

```python
# VWAP Sigma-2 Strategy settings
VWAP_PERIOD = 20        # VWAP calculation period
SIGMA_MULTIPLIER = 2.0  # Standard deviation multiplier
MIN_VOLUME = 1000       # Minimum volume filter
```

## 📚 Additional Resources

- **CCXT Documentation**: [https://ccxt.trade](https://ccxt.trade)
- **Exchange APIs**: Each exchange has specific API documentation

---

## 🔗 Related Documentation

- [**Main README**](../README.md) - Project overview and setup
- [**Stocks Module**](stocks-module.md) - Indian equity trading
- [**Strategies Module**](strategies-module.md) - Trading strategies
- [**Fyers Setup Guide**](FYERS_ONLY_SETUP.md) - Stock trading setup
- [**Documentation Index**](README.md) - All documentation

---

<div align="center">

### **🚀 Ready to Trade Crypto?**

[![Main README](https://img.shields.io/badge/Main%20Project-🚀-brightgreen)](../README.md)
[![Stocks Module](https://img.shields.io/badge/Stocks%20Module-📈-blue)](stocks-module.md)
[![Strategies](https://img.shields.io/badge/Strategies-📊-orange)](strategies-module.md)

**Part of the AlgoProject Enterprise Trading Platform**

</div>
- **Strategy Development**: See `src/strategies/` for custom strategies
- **Technical Analysis**: See `src/technical_analysis.py` for indicators

## ⚠️ Disclaimer

Cryptocurrency trading involves substantial risk of loss and is not suitable for every investor. Past performance does not guarantee future results. This module is for educational and testing purposes only.
