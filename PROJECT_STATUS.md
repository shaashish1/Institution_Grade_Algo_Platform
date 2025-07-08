# AlgoProject - Cryptocurrency & Stock Trading Platform

## Project Structure

```
AlgoProject/
├── config.yaml                  # Main configuration file
├── config_crypto.yaml          # Crypto-specific configuration
├── config_stocks.yaml          # Stocks-specific configuration
├── config_test.yaml            # Test configuration (10 USDT pairs)
├── requirements.txt             # Python dependencies
├── README.md                   # Project documentation
├── PROJECT_STATUS.md           # Current project status
├── 
├── # Core Trading Scripts
├── realtime_trader.py          # Real-time scanning and forward testing
├── backtest_runner.py          # Standalone backtesting with KPIs
├── 
├── # Utilities
├── list_ccxt_exchanges.py      # List all supported CCXT exchanges
├── list_crypto_assets.py       # Crypto asset listing utility
├── 
├── # Source Code
├── src/
│   ├── strategies/             # Trading strategies
│   │   ├── VWAPSigma2Strategy.py
│   │   ├── FiftyTwoWeekLowStrategy.py
│   │   └── sma_cross.py
│   ├── data_acquisition.py     # Data fetching utilities
│   ├── scanner.py             # Market scanning utilities
│   ├── technical_analysis.py  # Technical analysis helpers
│   └── web_scraper.py         # Web scraping utilities
├── 
├── # Data & Configuration
├── input/
│   ├── crypto_assets.csv      # All 37 USDT pairs from Kraken
│   ├── crypto_assets_test.csv # Test subset (10 pairs)
│   └── stocks_assets.csv      # List of stock symbols to trade
├── output/                    # Generated reports and scan results
│   ├── scan_results_*.csv     # Market scan results
│   └── backtest_trades_*.csv  # Backtest trade logs
├── 
├── # Dependencies & Environment
├── venv/                      # Python virtual environment
├── libs/                      # Local library dependencies
└── tests/                     # Test files
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Backtest
```bash
# Run backtest with default config (37 USDT pairs)
python scripts/realtime_trader.py

# Run backtest with specific config
python scripts/realtime_trader.py --config config/config_crypto.yaml
```

### 3. Run Forward Testing (Real-time)
```bash
# Run continuous forward testing with live price updates
python scripts/realtime_trader.py --config config/config_test.yaml --forward
```

## Enhanced Features

1. **📊 Professional Trade Display**: Beautiful tabular format with proper alignment
2. **🔄 Unified Asset Management**: Single `crypto_assets.csv` for all 37 USDT pairs
3. **⚡ Smart Trade Management**: One trade per symbol, strategy-based entry/exit
4. **🕐 IST Timestamps**: All times displayed in Indian Standard Time
5. **💰 Real-time PnL Tracking**: Live unrealized PnL calculation and total summary
6. **🎯 Signal Intelligence**: Only shows relevant signals, ignores HOLD states
7. **📈 Performance Metrics**: Data fetch timing and scan efficiency tracking

## Configuration

Edit `config.yaml` or create exchange-specific configs:

```yaml
asset_type: crypto
exchange: "kraken"
strategy:
  file: VWAPSigma2Strategy.py
  class: VWAPSigma2Strategy
interval: "5m"
bars: 100
trading_amount: 1000
```

## Strategy Development

Create new strategies in `src/strategies/` following the pattern:

```python
class MyStrategy:
    def generate_signal(self, df):
        # Return "BUY", "SELL", or "HOLD"
        pass
    
    def backtest(self, df):
        # Return DataFrame of trades
        pass
```

## Dependencies Resolved

- ✅ `backtest_runner.py` - Fixed import errors
- ✅ `realtime_trader.py` - Fixed import errors  
- ✅ `websocket-client` - Added to requirements
- ✅ `matplotlib` - Added for visualization
- ✅ Removed redundant/broken files
- ✅ **Updated crypto_assets.csv** - Now contains all 37 USDT pairs from Kraken
- ✅ **Cleaned project structure** - Organized files into proper folders
- ✅ **Output folder structure** - All results now go to output/ directory

## Project Cleanup Completed

**Files Moved:**
- All CSV results → `output/` folder
- Asset lists → `input/` folder  

**Files Removed:**
- Duplicate `tvdatafeed/` folder
- Old `algo_env/` virtual environment
- Setup scripts and old database files
- Duplicate asset CSV files

**Updated Configurations:**
- All config files now point to `output/` for results
- Clean separation of input data and output results

## Available Trading Pairs

The system now supports all **37 USDT trading pairs** available on Kraken:
- Major coins: BTC/USDT, ETH/USDT, XRP/USDT, ADA/USDT, SOL/USDT
- DeFi tokens: LINK/USDT, AVAX/USDT, DOT/USDT, ATOM/USDT
- Meme coins: DOGE/USDT, SHIB/USDT, FARTCOIN/USDT
- New tokens: AI16Z/USDT, TRUMP/USDT, MELANIA/USDT, VIRTUAL/USDT
- Stablecoins: USDC/USDT, DAI/USDT, EURR/USDT
- And 18 more pairs for comprehensive market coverage

## Next Steps

1. Test backtesting: `python backtest_runner.py`
2. Test real-time scanning: `python realtime_trader.py`
3. Configure exchanges and API credentials
4. Develop custom strategies
5. Run forward tests with `--forward` flag
