#!/usr/bin/env python3
"""
Run a limited stocks backtest to verify clean output
Test the first 10 symbols only for verification
"""

import os
import sys
import signal
import time
from multiprocessing import Process

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_limited_backtest():
    """Run backtest on limited symbols for testing."""
    # Temporarily modify the stocks file to test only first 10 symbols
    import pandas as pd
    
    # Read current symbols
    stocks_file = "input/stocks_assets.csv"
    if os.path.exists(stocks_file):
        df = pd.read_csv(stocks_file)
        original_symbols = df.copy()
        
        # Limit to first 10 symbols for testing
        df_limited = df.head(10)
        df_limited.to_csv(stocks_file, index=False)
        
        print("🧪 Running Limited Stocks Backtest (10 symbols)")
        print("=" * 60)
        print("🎯 Goal: Verify clean output with no error messages")
        print("=" * 60)
        
        try:
            # Run the backtest
            from scripts import stocks_backtest
            stocks_backtest.run_stocks_backtest()
            
        except KeyboardInterrupt:
            print("\n⚠️  Test interrupted")
        except Exception as e:
            print(f"\n❌ Error during test: {e}")
        finally:
            # Restore original symbols
            original_symbols.to_csv(stocks_file, index=False)
            print(f"\n✅ Original symbol list restored")

if __name__ == "__main__":
    print("🚀 Limited Clean Backtest Test")
    print("=" * 50)
    
    try:
        run_limited_backtest()
    except KeyboardInterrupt:
        print("\n👋 Test stopped by user")
    
    print("\n📋 **Analysis Complete**")
    print("🎯 If you saw clean output above, your setup is perfect!")
    print("🚀 Ready for full backtest: `python scripts/stocks_backtest.py`")
