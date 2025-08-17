#!/usr/bin/env python3
"""
Crypto Live Scanner
Real-time crypto trading scanner using CCXT data.
"""

import os
import sys
import time
import pandas as pd
from datetime import datetime
import pytz

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from crypto.data_acquisition import fetch_data
from tabulate import tabulate


def load_crypto_assets():
    """Load crypto assets from CSV file."""
    assets_file = "crypto/input/crypto_assets.csv"
    if not os.path.exists(assets_file):
        print(f"❌ Error: {assets_file} not found!")
        return []
    
    df = pd.read_csv(assets_file)
    return df['symbol'].tolist()


def load_strategy():
    """Load the trading strategy."""
    sys.path.append('src/strategies')
    from strategies.VWAPSigma2Strategy import VWAPSigma2Strategy
    return VWAPSigma2Strategy()


def run_crypto_live_scan():
    """Run live scanning on all crypto assets."""
    print("🔴 LIVE Crypto Scanner")
    print("=" * 80)
    
    # Load assets
    symbols = load_crypto_assets()
    if not symbols:
        return
    
    print(f"🔍 Live scanning {len(symbols)} crypto symbols using CCXT (Kraken)")
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
                    data = fetch_data(
                        symbol=symbol,
                        exchange="kraken",
                        interval="5m",
                        bars=20,  # Less data for faster scanning
                        data_source="ccxt",
                        fetch_timeout=10
                    )
                    
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
                            'Price': f"${data['close'].iloc[-1]:.4f}",
                            'Volume': f"{data['volume'].iloc[-1]:,.0f}"
                        })
                    
                    # Progress indicator
                    if i % 10 == 0 or i == len(symbols):
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
            
            print(f"\n⏱️  Next scan in 30 seconds...")
            time.sleep(30)  # Wait 30 seconds between scans
    
    except KeyboardInterrupt:
        print(f"\n\n✅ Live scanning stopped. Completed {scan_count} scans.")


def save_live_signals(signals):
    """Save live signals to CSV file."""
    if not signals:
        return
    
    os.makedirs("output", exist_ok=True)
    
    df = pd.DataFrame(signals)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/live_signals_crypto_{timestamp}.csv"
    
    df.to_csv(filename, index=False)
    print(f"💾 Live signals saved to {filename}")


if __name__ == "__main__":
    try:
        run_crypto_live_scan()
    except KeyboardInterrupt:
        print("\n⚠️  Live scanning interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
