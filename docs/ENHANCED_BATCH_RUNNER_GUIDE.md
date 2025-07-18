# 🚀 Enhanced Batch Runner - Comprehensive Strategy Analysis

## 🎯 Overview

The Enhanced Batch Runner is a powerful tool that automatically tests **ALL available trading strategies** across **multiple timeframes** and generates comprehensive comparison reports to identify the best performing strategies.

## ✨ Key Features

### 🤖 **Auto-Discovery**
- Automatically finds all strategy files in the `strategies/` folder
- No need to manually specify strategy names
- Supports any new strategies you add

### ⏰ **Multi-Timeframe Analysis**
- Tests strategies on: **5m, 15m, 30m, 1h, 2h, 4h, 1d**
- Identifies which timeframe works best for each strategy
- Comprehensive performance comparison across all combinations

### 📊 **Comprehensive Reports**
- **Performance Rankings** - Sort by risk-adjusted returns
- **Best Strategy per Timeframe** - Optimal strategy for each time period
- **Best Timeframe per Strategy** - Optimal time period for each strategy
- **Top Performers** - By return, Sharpe ratio, win rate, low drawdown
- **Strategy Recommendations** - Conservative, aggressive, and balanced choices

### 📈 **Advanced Metrics**
- Total Return %
- Risk-Adjusted Return (Return/Drawdown ratio)
- Sharpe Ratio
- Maximum Drawdown %
- Win Rate %
- Total Trades

---

## 🚀 Quick Start

### **1. Auto Mode (Recommended)**
```bash
cd crypto/scripts
python batch_runner.py --auto --symbols BTC/USDT ETH/USDT
```
**What it does:**
- Tests ALL strategies on ALL timeframes
- Generates comprehensive comparison report
- Identifies best performers automatically

### **2. Quick Test (Single Symbol)**
```bash
python batch_runner.py --auto --symbols BTC/USDT
```
**What it does:**
- Faster testing with just BTC/USDT
- Still tests all strategies and timeframes
- Good for initial exploration

---

## 🛠️ Advanced Usage

### **Custom Strategies**
```bash
python batch_runner.py --symbols BTC/USDT ETH/USDT --strategies "BB RSI,MACD Only,RSI MACD VWAP"
```

### **Custom Timeframes**
```bash
python batch_runner.py --symbols BTC/USDT --timeframes 1h 4h 1d
```

### **Custom Parameters**
```bash
python batch_runner.py --auto --symbols BTC/USDT ETH/USDT LTC/USDT --capital 50000 --position 5000 --bars 1000
```

### **Different Exchange**
```bash
python batch_runner.py --auto --symbols BTC/USDT --exchange binance
```

---

## 📊 Output Files

### **📄 Main Report**
`strategy_comparison_report_YYYYMMDD_HHMMSS.md`
- Complete analysis with rankings and recommendations
- Best strategy identification
- Performance metrics summary

### **📈 Raw Data**
`strategy_comparison_data_YYYYMMDD_HHMMSS.csv`
- All test results in CSV format
- Suitable for further analysis in Excel/Python

### **📁 Individual Results**
- Each strategy/timeframe combination gets its own folder
- Detailed trade logs and performance files

---

## 🏆 Example Output Report

```markdown
# 📊 Comprehensive Strategy Performance Report

## 🏆 Overall Performance Rankings

| Strategy          | Timeframe | Total Return (%) | Max Drawdown (%) | Sharpe Ratio | Win Rate (%) | Risk-Adjusted Return |
|-------------------|-----------|------------------|------------------|--------------|--------------|---------------------|
| Enhanced Multi Factor | 4h       | 15.3            | 8.2              | 1.87         | 68.5         | 1.87                |
| RSI MACD VWAP    | 1h        | 12.8            | 7.1              | 1.80         | 64.2         | 1.80                |
| BB RSI           | 2h        | 11.5            | 6.8              | 1.69         | 61.3         | 1.69                |

## ⭐ Best Strategy per Timeframe

| Timeframe | Strategy              | Total Return (%) | Risk-Adjusted Return |
|-----------|-----------------------|------------------|---------------------|
| 5m        | MACD Only            | 8.3              | 1.23                |
| 15m       | BB RSI               | 9.1              | 1.34                |
| 30m       | RSI MACD VWAP        | 10.2             | 1.44                |
| 1h        | RSI MACD VWAP        | 12.8             | 1.80                |
| 2h        | BB RSI               | 11.5             | 1.69                |
| 4h        | Enhanced Multi Factor | 15.3             | 1.87                |
| 1d        | Optimized Crypto V2   | 14.1             | 1.76                |

## 💡 Strategy Recommendations

**🥇 Overall Best Strategy**: Enhanced Multi Factor on 4h timeframe
- Total Return: 15.3%
- Risk-Adjusted Return: 1.87
- Max Drawdown: 8.2%
- Win Rate: 68.5%

**🛡️ Conservative Choice**: BB RSI on 2h timeframe
- Low risk with 6.8% max drawdown
- Steady return: 11.5%

**🚀 Aggressive Choice**: Enhanced Multi Factor on 4h timeframe
- Highest return potential: 15.3%
- Max drawdown: 8.2%
```

---

## 📋 Available Strategies

The batch runner automatically discovers these strategies:

1. **BB RSI** - Bollinger Bands + RSI combination
2. **Enhanced Multi Factor** - Multi-factor quantitative model
3. **Fifty Two Week Low** - 52-week breakout strategy
4. **Institutional Flow** - Volume and institutional analysis
5. **MACD Only** - Pure MACD momentum strategy
6. **Market Inefficiency** - Arbitrage and inefficiency exploitation
7. **Optimized Crypto V2** - Crypto-specific optimized strategy
8. **RSI MACD VWAP** - Multi-indicator comprehensive strategy
9. **SMA Cross** - Simple moving average crossover
10. **Ultimate Profitable** - Ensemble strategy combination
11. **VWAP Sigma2** - Volume-weighted statistical strategy

---

## ⚙️ Command Line Options

```bash
python batch_runner.py [OPTIONS]

OPTIONS:
  --auto                    Auto mode: Test ALL strategies on ALL timeframes
  --symbols SYMBOLS         List of symbols (default: BTC/USDT ETH/USDT)
  --strategies STRATEGIES   Comma-separated strategy names
  --timeframes TIMEFRAMES   List of timeframes to test
  --bars BARS              Number of bars to fetch (default: 720)
  --capital CAPITAL        Initial capital (default: 100000)
  --position POSITION      Position size per trade (default: 10000)
  --exchange EXCHANGE      Exchange: binance|kraken|coinbase|bitfinex
  --output OUTPUT          Output directory (default: output)
  --legacy                 Use legacy single-test mode
```

---

## 🎯 Pro Tips

### **For Beginners:**
1. Start with: `python batch_runner.py --auto --symbols BTC/USDT`
2. Review the generated report carefully
3. Look for strategies with high risk-adjusted returns
4. Consider both return and drawdown

### **For Advanced Users:**
1. Test with multiple symbols for diversification insights
2. Experiment with different bar counts (--bars parameter)
3. Compare results across different exchanges
4. Use the CSV output for custom analysis

### **Performance Optimization:**
1. Use fewer symbols for faster testing during development
2. Reduce --bars for quicker preliminary tests
3. Focus on specific timeframes that match your trading style
4. Use --strategies to test only promising strategies

---

## 🚨 Important Notes

1. **Data Requirements**: Ensure you have good internet connection for data fetching
2. **Time Estimation**: Full auto mode can take 30-60 minutes depending on system
3. **Resource Usage**: Multiple parallel tests use significant CPU/memory
4. **Market Hours**: Some exchanges may have data limitations during certain hours

---

## 🔧 Troubleshooting

### **Common Issues:**

**"No data available"**
- Check internet connection
- Try different exchange (--exchange parameter)
- Verify symbol format (BTC/USDT not BTC-USDT)

**"Strategy not found"**
- Use exact strategy names from auto-discovery
- Check strategies folder for available files

**"Low performance results"**
- Try different timeframes
- Increase --bars for more data
- Check if market conditions were unusual during test period

---

## 📞 Support

For questions or issues:
1. Check the generated error logs in output directories
2. Review the comprehensive test results
3. Try with fewer symbols/strategies first
4. Ensure all dependencies are installed via requirements.txt

**Happy Strategy Testing! 🚀📈💰**
