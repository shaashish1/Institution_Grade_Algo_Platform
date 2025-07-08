#!/usr/bin/env python3
"""
Stocks Backtest Scanner
Simple script to backtest stock trading strategies using TradingView data.
"""

import os
import sys
import pandas as pd
from datetime import datetime
import pytz

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_acquisition import fetch_data
from tabulate import tabulate


def load_stock_assets():
    """Load stock assets from CSV file."""
    assets_file = "input/stocks_assets.csv"
    if not os.path.exists(assets_file):
        print(f"❌ Error: {assets_file} not found!")
        return []
    
    df = pd.read_csv(assets_file)
    return df['symbol'].tolist()


def load_strategy():
    """Load the trading strategy."""
    sys.path.append('src/strategies')
    from VWAPSigma2Strategy import VWAPSigma2Strategy
    return VWAPSigma2Strategy()


def setup_tradingview():
    """Setup TradingView connection with authentication."""
    try:
        from tvDatafeed import TvDatafeed
        
        # Try with authentication first
        try:
            tv = TvDatafeed(
                username="ashish.sharma14@gmail.com",
                password="BlockTrade5$1"
            )
            print("✅ TradingView authenticated successfully")
            return tv
        except Exception as auth_error:
            print(f"⚠️  TradingView authentication failed: {auth_error}")
            print("🔄 Falling back to anonymous mode (limited data)")
            return TvDatafeed()
    
    except ImportError:
        print("❌ Error: TradingView library not installed!")
        return None


def run_stocks_backtest():
    """Run backtest on all stock assets."""
    print("🚀 Stocks Backtest Scanner")
    print("=" * 80)
    
    # Setup TradingView
    tv = setup_tradingview()
    if not tv:
        return
    
    # Load assets
    symbols = load_stock_assets()
    if not symbols:
        return
    
    print(f"🔍 Scanning {len(symbols)} stock symbols using TradingView (NSE)")
    print(f"📊 Strategy: VWAPSigma2Strategy")
    print("=" * 80)
    
    # Load strategy
    strategy = load_strategy()
    
    # Results storage
    all_results = []
    all_trades = []
    
    ist = pytz.timezone('Asia/Kolkata')
    start_time = datetime.now(ist)
    
    for i, symbol in enumerate(symbols, 1):
        try:
            print(f"📈 [{i:2d}/{len(symbols)}] Processing {symbol}...", end=" ")
            
            # Fetch data using TradingView
            data = fetch_data_tv(tv, symbol)
            
            if data is None or data.empty:
                print("❌ No data")
                continue
            
            # Apply strategy
            signals = strategy.generate_signals(data)
            if not signals.empty:
                signal_count = len(signals)
                print(f"✅ {signal_count} signals")
                
                # Store results
                for _, signal in signals.iterrows():
                    result = {
                        'timestamp': signal['timestamp'],
                        'symbol': symbol,
                        'signal': signal['signal'],
                        'price': signal['close'],
                        'volume': signal['volume']
                    }
                    all_results.append(result)
                    
                    if signal['signal'] in ['BUY', 'SELL']:
                        trade = result.copy()
                        trade['amount'] = 1000  # Default trading amount
                        all_trades.append(trade)
            else:
                print("⚪ No signals")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Calculate performance
    end_time = datetime.now(ist)
    duration = (end_time - start_time).total_seconds()
    
    print("=" * 80)
    print(f"✅ Backtest completed in {duration:.1f}s")
    print(f"📊 Total signals: {len(all_results)}")
    print(f"💰 Total trades: {len(all_trades)}")
    
    # Save results
    save_results(all_results, all_trades)
    
    # Display summary
    display_summary(all_results, all_trades)


def fetch_data_tv(tv, symbol):
    """Fetch data from TradingView with proper error handling."""
    try:
        from tvDatafeed import Interval
        
        # Fetch data
        data = tv.get_hist(
            symbol=symbol,
            exchange='NSE',
            interval=Interval.in_5_minute,
            n_bars=100
        )
        
        if data is None or data.empty:
            return None
        
        # Fix datetime issues by resetting index and converting
        data = data.reset_index()
        
        # Ensure proper column names
        if 'datetime' in data.columns:
            data['timestamp'] = data['datetime']
        elif data.index.name == 'datetime':
            data = data.reset_index()
            data['timestamp'] = data['datetime']
        
        # Convert timestamp to proper format
        if 'timestamp' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Ensure required columns exist
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            if col not in data.columns:
                print(f"❌ Missing column: {col}")
                return None
        
        return data
        
    except Exception as e:
        print(f"TradingView fetch error: {e}")
        return None


def save_results(results, trades):
    """Save results to CSV files."""
    os.makedirs("output", exist_ok=True)
    
    if results:
        df_results = pd.DataFrame(results)
        results_file = "output/scan_results_stocks.csv"
        df_results.to_csv(results_file, index=False)
        print(f"💾 Scan results saved to {results_file}")
    
    if trades:
        df_trades = pd.DataFrame(trades)
        trades_file = "output/backtest_trades_stocks.csv"
        df_trades.to_csv(trades_file, index=False)
        print(f"💾 Trade results saved to {trades_file}")


def display_summary(results, trades):
    """Display backtest summary."""
    if not results:
        print("\n⚠️  No signals generated in backtest.")
        return
    
    df_results = pd.DataFrame(results)
    
    # Signal summary
    signal_summary = df_results['signal'].value_counts().to_dict()
    
    print(f"\n📊 **BACKTEST SUMMARY**")
    print("=" * 50)
    
    summary_data = []
    for signal_type, count in signal_summary.items():
        summary_data.append([signal_type, count])
    
    print(tabulate(summary_data, headers=['Signal Type', 'Count'], tablefmt='grid'))
    
    # Top symbols with signals
    if len(df_results) > 0:
        top_symbols = df_results['symbol'].value_counts().head(10)
        print(f"\n🏆 **TOP SYMBOLS BY SIGNALS**")
        print("=" * 40)
        
        top_data = []
        for symbol, count in top_symbols.items():
            top_data.append([symbol, count])
        
        print(tabulate(top_data, headers=['Symbol', 'Signals'], tablefmt='grid'))


if __name__ == "__main__":
    try:
        run_stocks_backtest()
    except KeyboardInterrupt:
        print("\n⚠️  Backtest interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
