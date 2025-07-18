#!/usr/bin/env python3
"""
Quick data fetch test to isolate the hanging issue
"""

import os
import sys
import time

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

print(f"🔧 Testing data fetch from: {parent_dir}")

def test_ccxt_direct():
    """Test CCXT directly without our wrapper."""
    try:
        print("📊 Testing CCXT directly...")
        import ccxt
        
        # Use shorter timeout
        exchange = ccxt.kraken({
            'timeout': 5000,  # 5 seconds
            'enableRateLimit': True
        })
        
        print("📈 Fetching BTC/USDT...")
        data = exchange.fetch_ohlcv('BTC/USDT', '1h', limit=10)
        
        if data:
            print(f"✅ Got {len(data)} bars directly from CCXT")
            return True
        else:
            print("❌ No data from CCXT")
            return False
            
    except Exception as e:
        print(f"❌ CCXT error: {e}")
        return False

def test_our_wrapper():
    """Test our data acquisition wrapper."""
    try:
        print("📊 Testing our wrapper...")
        from crypto.data_acquisition import fetch_data
        
        print("📈 Fetching via wrapper...")
        data = fetch_data(
            symbol='BTC/USDT',
            bars=10,
            interval='1h',
            exchange='kraken',
            fetch_timeout=5
        )
        
        if data is not None and len(data) > 0:
            print(f"✅ Got {len(data)} bars from wrapper")
            return True
        else:
            print("❌ No data from wrapper")
            return False
            
    except Exception as e:
        print(f"❌ Wrapper error: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 ISOLATED DATA FETCH TEST")
    print("=" * 50)
    
    # Test 1: Direct CCXT
    print("\n1️⃣ Testing CCXT directly...")
    ccxt_works = test_ccxt_direct()
    
    # Test 2: Our wrapper
    print("\n2️⃣ Testing our wrapper...")
    wrapper_works = test_our_wrapper()
    
    print("\n" + "=" * 50)
    print("🎯 RESULTS:")
    print(f"CCXT Direct: {'✅ Works' if ccxt_works else '❌ Failed'}")
    print(f"Our Wrapper: {'✅ Works' if wrapper_works else '❌ Failed'}")
    
    if ccxt_works and not wrapper_works:
        print("🔍 Issue is in our wrapper code")
    elif not ccxt_works:
        print("🔍 Issue is with CCXT/network")
    else:
        print("🔍 Both work - issue might be elsewhere")

if __name__ == "__main__":
    main()
