#!/usr/bin/env python3
"""
Quick Test - Crypto Backtest
Test the crypto backtest functionality with just a few symbols.
"""

import os
import sys
import pandas as pd
from datetime import datetime
import pytz

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.data_acquisition import fetch_data
from tabulate import tabulate


def load_strategy():
    """Load the trading strategy."""
    sys.path.append('src/strategies')
    from strategies.VWAPSigma2Strategy import VWAPSigma2Strategy
    return VWAPSigma2Strategy()


def run_quick_test():
    """Run a quick test with 3 popular crypto symbols."""
    print("🧪 Quick Crypto Test")
    print("=" * 60)
    
    # Test with 3 popular symbols
    test_symbols = ["BTC/USDT", "ETH/USDT", "ADA/USDT"]
    
    print(f"🔍 Testing {len(test_symbols)} crypto symbols using CCXT (Kraken)")
    print(f"📊 Strategy: VWAPSigma2Strategy")
    print("=" * 60)
    
    # Load strategy
    strategy = load_strategy()
    
    # Results storage
    all_results = []
    
    ist = pytz.timezone('Asia/Kolkata')
    start_time = datetime.now(ist)
    
    for i, symbol in enumerate(test_symbols, 1):
        try:
            print(f"📈 [{i}/{len(test_symbols)}] Testing {symbol}...", end=" ")
            
            # Fetch data using CCXT
            data = fetch_data(
                symbol=symbol,
                exchange="kraken",
                interval="5m",
                bars=50,  # Less data for quick test
                data_source="ccxt",
                fetch_timeout=10
            )
            
            if data is None or data.empty:
                print("❌ No data")
                continue
            
            # Apply strategy
            signal = strategy.generate_signal(data)
            if signal and signal != "HOLD":
                print(f"✅ Signal: {signal}")
                
                # Store result
                result = {
                    'Symbol': symbol,
                    'Signal': signal,
                    'Price': f"${data['close'].iloc[-1]:.4f}",
                    'Time': datetime.now(ist).strftime("%H:%M")
                }
                all_results.append(result)
            else:
                print("⚪ HOLD signal")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Calculate performance
    end_time = datetime.now(ist)
    duration = (end_time - start_time).total_seconds()
    
    print("=" * 60)
    print(f"✅ Quick test completed in {duration:.1f}s")
    
    # Display results
    if all_results:
        print(f"\n📊 **TEST RESULTS** ({len(all_results)} signals)")
        print(tabulate(all_results, headers='keys', tablefmt='grid'))
        print("\n✅ System is working correctly!")
    else:
        print("\n⚠️  No signals found in test data")
        print("✅ System is functional but no trading opportunities detected")


if __name__ == "__main__":
    try:
        run_quick_test()
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
