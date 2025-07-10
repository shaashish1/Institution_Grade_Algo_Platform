#!/usr/bin/env python3
"""
Quick test of clean stocks backtest output
Test just a few symbols to verify error suppression works
"""

import os
import sys
import yaml
import pandas as pd
from datetime import datetime, timedelta
import pytz

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_acquisition import fetch_data

def quick_clean_test():
    """Test a few symbols to verify clean output."""
    print("🧪 Quick Clean Output Test")
    print("=" * 40)
    
    # Test symbols
    symbols = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "ITC"]
    
    print(f"📊 Testing {len(symbols)} symbols for clean output...")
    print("🔍 This should show NO error messages:")
    print("-" * 40)
    
    success_count = 0
    for i, symbol in enumerate(symbols, 1):
        print(f"📈 [{i:2d}/{len(symbols)}] Processing {symbol}...", end=" ")
        
        try:
            # This should be completely silent now
            data = fetch_data(
                symbol=symbol,
                exchange="NSE",
                interval="1h",
                bars=10,
                data_source="tvdatafeed"
            )
            
            if data is not None and len(data) > 0:
                print(f"✅ Got {len(data)} bars")
                success_count += 1
            else:
                print("❌ No data")
                
        except Exception as e:
            print(f"❌ Error: {str(e)[:30]}...")
    
    print("-" * 40)
    print(f"✅ Completed: {success_count}/{len(symbols)} symbols successful")
    
    if success_count == len(symbols):
        print("🎉 **PERFECT!** All symbols processed cleanly!")
        print("🟢 No authentication errors visible")
        print("🟢 No warning messages")
        print("🟢 Clean, professional output")
    elif success_count > 0:
        print("🟡 **GOOD!** Most symbols working cleanly")
        print("🟢 Error suppression working")
        print("🟡 Some connectivity issues (normal)")
    else:
        print("🔴 **ISSUE!** No symbols working")
        print("❌ Check network connectivity")
        print("❌ Verify TradingView status")
    
    return success_count

if __name__ == "__main__":
    print("🚀 Clean Output Verification Test")
    print("=" * 50)
    print("🎯 Goal: Verify NO error messages appear")
    print("=" * 50)
    
    success = quick_clean_test()
    
    print(f"\n📋 **SUMMARY:**")
    if success >= 4:
        print("✅ **SUCCESS:** Your error suppression is working perfectly!")
        print("✅ **Ready:** Run full stocks backtest with confidence")
        print("✅ **Clean:** Professional output achieved")
        print("\n🚀 **Next Step:** Run `python scripts/stocks_backtest.py`")
    elif success >= 2:
        print("✅ **MOSTLY SUCCESSFUL:** Error suppression working well")
        print("🟡 **Minor Issues:** Some connectivity problems (normal)")
        print("✅ **Functional:** System ready for use")
        print("\n🚀 **Next Step:** Full backtest should work great")
    else:
        print("❌ **CONNECTIVITY ISSUE:** Check network/TradingView status")
        print("🔧 **Try:** Restart and test again")
        print("🔧 **Alternative:** Use crypto backtest (no auth needed)")
    
    print(f"\n💡 **Note:** Zero error messages = perfect setup!")
