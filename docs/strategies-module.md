# 🎯 Trading Strategies Framework

> **Advanced trading strategies for both cryptocurrency and stock markets using proven technical analysis methods**  
> Part of the [AlgoProject Enterprise Trading Platform](../README.md)

---

## 📋 **Available Strategies**

### **📊 Technical Analysis Strategies**

| **Strategy** | **Asset Class** | **Description** | **Key Indicators** |
|-------------|----------------|-----------------|-------------------|
| **SMA Cross** | Crypto + Stocks | Simple Moving Average crossover | SMA(10) vs SMA(30) |
| **VWAP Sigma-2** | Crypto + Stocks | Volume-Weighted Average Price with 2-sigma bands | VWAP, Volume, Price deviation |
| **52-Week Low** | Stocks | Value investing based on 52-week lows | Price levels, Support/Resistance |

---

## 🚀 **Strategy Details**

### **📈 SMA Cross Strategy (`sma_cross.py`)**

Simple Moving Average crossover strategy using backtrader framework.

```python
# Signal Logic:
- BUY:  SMA(10) crosses above SMA(30)
- SELL: SMA(10) crosses below SMA(30)

# Parameters:
- Fast SMA: 10 periods
- Slow SMA: 30 periods
- Signal: CrossOver indicator
```

**Best For**: Trending markets, medium-term trades

### **📊 VWAP Sigma-2 Strategy (`VWAPSigma2Strategy.py`)**

Volume-Weighted Average Price with 2-sigma deviation bands.

```python
# Signal Logic:
- BUY:  Price touches VWAP - 2σ (oversold)
- SELL: Price touches VWAP + 2σ (overbought)

# Parameters:
- VWAP calculation with volume weighting
- 2-sigma bands for entry/exit
- Mean reversion approach
```

**Best For**: Range-bound markets, intraday trading

### **💎 52-Week Low Strategy (`FiftyTwoWeekLowStrategy.py`)**

Value investing strategy targeting stocks near 52-week lows.

```python
# Signal Logic:
- BUY:  Stock near 52-week low with volume confirmation
- SELL: Target profit or stop-loss levels

# Parameters:
- 52-week lookback period
- Volume confirmation
- Risk management rules
```

**Best For**: Long-term value investing, stock markets

---

## 🔧 **Usage Examples**

### **📊 In Backtesting**

```python
# Import strategy
from src.strategies.sma_cross import SmaCross

# Add to backtest
cerebro.addstrategy(SmaCross)

# Run backtest
cerebro.run()
```

### **🎮 In Live Trading**

```python
# Import strategy
from src.strategies.VWAPSigma2Strategy import VWAPSigma2Strategy

# Apply to live data
strategy = VWAPSigma2Strategy()
signal = strategy.generate_signal(current_data)
```

### **📈 In Crypto Scripts**

```python
# Use in crypto_demo_live.py
from src.strategies.sma_cross import SmaCross

# Apply to crypto pairs
for symbol in crypto_symbols:
    strategy_result = apply_strategy(SmaCross, symbol)
```

### **📊 In Stock Scripts**

```python
# Use in stocks_demo_live.py
from src.strategies.FiftyTwoWeekLowStrategy import FiftyTwoWeekLowStrategy

# Apply to NSE stocks
for symbol in nse_stocks:
    strategy_result = apply_strategy(FiftyTwoWeekLowStrategy, symbol)
```

---

## 🛠️ **Creating New Strategies**

### **🎯 Strategy Template**

```python
import backtrader as bt

class MyCustomStrategy(bt.Strategy):
    # Parameters
    params = (
        ('period', 14),
        ('threshold', 0.02),
    )
    
    def __init__(self):
        # Initialize indicators
        self.sma = bt.ind.SMA(period=self.params.period)
        self.rsi = bt.ind.RSI(period=14)
    
    def next(self):
        # Strategy logic
        if self.rsi < 30:  # Oversold
            self.buy()
        elif self.rsi > 70:  # Overbought
            self.sell()
    
    def log(self, txt, dt=None):
        # Logging function
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}: {txt}')
```

### **📊 Integration Steps**

1. **Create Strategy File**
   ```python
   # Save as src/strategies/my_strategy.py
   ```

2. **Test Strategy**
   ```python
   # Add to backtest scripts
   python stocks/scripts/stocks_backtest.py
   ```

3. **Deploy Strategy**
   ```python
   # Use in live demo
   python stocks/scripts/stocks_demo_live.py
   ```

---

## 📊 **Performance Metrics**

### **📈 Backtesting Results**

Strategies are tested against historical data with the following metrics:

- **Return %** - Total return percentage
- **Sharpe Ratio** - Risk-adjusted return
- **Max Drawdown** - Maximum loss from peak
- **Win Rate** - Percentage of profitable trades
- **Profit Factor** - Gross profit / Gross loss

### **🎯 Live Performance**

Real-time performance tracking includes:

- **P&L Tracking** - Profit and loss monitoring
- **Risk Metrics** - Position sizing and exposure
- **Signal Accuracy** - Buy/sell signal effectiveness
- **Execution Quality** - Slippage and timing

---

## 🔍 **Strategy Analysis**

### **📊 Technical Indicators**

Common indicators used across strategies:

- **Moving Averages** - SMA, EMA, VWAP
- **Oscillators** - RSI, MACD, Stochastic
- **Volume** - Volume confirmation, OBV
- **Price Action** - Support/Resistance, Breakouts

### **⚡ Market Conditions**

Strategy performance varies by market conditions:

- **Trending Markets** - SMA Cross, Breakout strategies
- **Range-Bound Markets** - VWAP Sigma-2, Mean reversion
- **Volatile Markets** - Volatility-based strategies
- **High Volume** - Volume-weighted strategies

---

## 🧪 **Testing Framework**

### **📋 Strategy Testing**

```python
# Test individual strategy
python -c "from src.strategies.sma_cross import SmaCross; print('Strategy loaded successfully')"

# Backtest validation
python stocks/scripts/stocks_backtest.py

# Live demo testing
python stocks/scripts/stocks_demo_live.py
```

### **📊 Performance Validation**

```python
# Compare strategies
python utils/strategy_comparison.py

# Risk analysis
python utils/risk_analysis.py

# Performance metrics
python utils/performance_metrics.py
```

---

## 🔧 **Advanced Features**

### **🎯 Multi-Asset Strategies**

Strategies can be applied to both crypto and stocks:

```python
# Universal strategy application
def apply_universal_strategy(strategy_class, asset_type):
    if asset_type == "crypto":
        return apply_to_crypto_pairs(strategy_class)
    elif asset_type == "stocks":
        return apply_to_stock_symbols(strategy_class)
```

### **📊 Portfolio Strategies**

Advanced portfolio management:

```python
# Portfolio optimization
from src.strategies.portfolio_optimizer import PortfolioOptimizer

# Risk parity
from src.strategies.risk_parity import RiskParityStrategy

# Mean reversion
from src.strategies.mean_reversion import MeanReversionStrategy
```

### **⚡ Real-time Adaptation**

Dynamic strategy parameters:

```python
# Adaptive parameters
strategy.update_parameters(market_volatility)

# Dynamic thresholds
strategy.adjust_thresholds(market_conditions)

# Real-time optimization
strategy.optimize_parameters(recent_performance)
```

---

## 📖 **Documentation**

- **📚 Main README** - `../README.md`
- **📊 Backtest Guide** - `../FYERS_ONLY_SETUP.md`
- **🧪 Testing** - `../tests/`
- **📈 Data Sources** - `../utils/`

---

## 🚀 **Next Steps**

1. **📊 Test Strategies** - Run backtests on historical data
2. **🎮 Demo Mode** - Test with live data, no real trades
3. **📈 Live Trading** - Deploy with real capital (with proper risk management)
4. **🔧 Customize** - Modify parameters for your risk tolerance
5. **📊 Monitor** - Track performance and adjust as needed

---

## 🔗 Related Documentation

- [**Main README**](../README.md) - Project overview and setup
- [**Crypto Module**](crypto-module.md) - Cryptocurrency trading
- [**Stocks Module**](stocks-module.md) - Indian equity trading
- [**Fyers Setup Guide**](FYERS_ONLY_SETUP.md) - Stock trading setup
- [**Documentation Index**](README.md) - All documentation

---

<div align="center">

### **🚀 Ready to Test Strategies?**

[![Main README](https://img.shields.io/badge/Main%20Project-🚀-brightgreen)](../README.md)
[![Crypto Module](https://img.shields.io/badge/Crypto%20Module-🪙-blue)](crypto-module.md)
[![Stocks Module](https://img.shields.io/badge/Stocks%20Module-📈-orange)](stocks-module.md)

**Part of the AlgoProject Enterprise Trading Platform**

</div>

---

> **⚠️ Risk Warning**: All strategies involve financial risk. Always test thoroughly in demo mode before live trading. Past performance does not guarantee future results.
