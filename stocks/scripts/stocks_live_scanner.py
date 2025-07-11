#!/usr/bin/env python3
"""
Stocks Live Scanner
Real-time stock trading scanner using TradingView data.
"""

import os
import sys
import time
import pandas as pd
from datetime import datetime
import pytz

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tabulate import tabulate


def load_stock_assets():
    """Load stock assets from CSV file."""
    assets_file = "stocks/input/stocks_assets.csv"
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


def run_stocks_live_scan():
    """Run live scanning on all stock assets."""
    print("🔴 LIVE Stocks Scanner")
    print("=" * 80)
    
    # Setup TradingView
    tv = setup_tradingview()
    if not tv:
        return
    
    # Load assets
    symbols = load_stock_assets()
    if not symbols:
        return
    
    print(f"🔍 Live scanning {len(symbols)} stock symbols using TradingView (NSE)")
    print(f"📊 Strategy: VWAPSigma2Strategy")
    print(f"🔄 Continuous scanning... Press Ctrl+C to stop")
    print("=" * 80)
    
    # Load strategy
    strategy = load_strategy()
    
    ist = pytz.timezone('Asia/Kolkata')
    scan_count = 0
    
    try:
        while True:
            scan_count += 1
            current_time = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n📅 {current_time} IST | 🔍 Scan #{scan_count}")
            print("-" * 60)
            
            live_signals = []
            
            for i, symbol in enumerate(symbols, 1):
                try:
                    # Fetch real-time data
                    data = fetch_data_tv(tv, symbol, bars=20)
                    
                    if data is None or data.empty:
                        continue
                    
                    # Apply strategy for real-time signal
                    signal = strategy.generate_signal(data)
                    
                    # Check for actionable signals
                    if signal and signal != "HOLD":
                        live_signals.append({
                            'Time': current_time,
                            'Symbol': symbol,
                            'Signal': signal.split('(')[0].strip(),  # Extract BUY/SELL part
                            'Price': f"₹{data['close'].iloc[-1]:.2f}",
                            'Volume': f"{data['volume'].iloc[-1]:,.0f}"
                        })
                    
                    # Progress indicator
                    if i % 5 == 0 or i == len(symbols):
                        progress = (i / len(symbols)) * 100
                        print(f"📊 Progress: {i}/{len(symbols)} ({progress:.0f}%)", end="\r")
                
                except Exception as e:
                    continue  # Skip errors in live mode
            
            # Display live signals
            if live_signals:
                print(f"\n🚨 **LIVE SIGNALS DETECTED** ({len(live_signals)} signals)")
                print(tabulate(live_signals, headers='keys', tablefmt='grid'))
                
                # Save live signals
                save_live_signals(live_signals)
            else:
                print(f"\n⚪ No live signals detected")
            
            print(f"\n⏱️  Next scan in 60 seconds...")
            time.sleep(60)  # Wait 60 seconds between scans (stocks are slower)
    
    except KeyboardInterrupt:
        print(f"\n\n✅ Live scanning stopped. Completed {scan_count} scans.")


def fetch_data_tv(tv, symbol, bars=100):
    """Fetch data from TradingView with proper error handling."""
    try:
        from tvDatafeed import Interval
        
        # Fetch data
        data = tv.get_hist(
            symbol=symbol,
            exchange='NSE',
            interval=Interval.in_5_minute,
            n_bars=bars
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
                return None
        
        return data
        
    except Exception as e:
        return None


def save_live_signals(signals):
    """Save live signals to CSV file."""
    if not signals:
        return
    
    os.makedirs("output", exist_ok=True)
    
    df = pd.DataFrame(signals)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/live_signals_stocks_{timestamp}.csv"
    
    df.to_csv(filename, index=False)
    print(f"💾 Live signals saved to {filename}")


if __name__ == "__main__":
    try:
        run_stocks_live_scan()
    except KeyboardInterrupt:
        print("\n⚠️  Live scanning interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
