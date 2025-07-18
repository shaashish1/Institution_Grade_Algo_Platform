#!/usr/bin/env python3
"""
Quick Crypto Module Test
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_ccxt():
    """Test CCXT import and basic functionality."""
    try:
        import ccxt
        print(f"✅ CCXT imported successfully - Version: {ccxt.__version__}")
        
        # Test exchange creation
        exchange = ccxt.kraken()
        print(f"✅ Exchange created: {exchange.id}")
        
        return True
    except Exception as e:
        print(f"❌ CCXT test failed: {e}")
        return False

def test_crypto_data_acquisition():
    """Test crypto data acquisition module."""
    try:
        from crypto.data_acquisition import health_check
        print("✅ crypto.data_acquisition imported successfully")
        
        # Run health check
        health = health_check()
        print(f"✅ Health check completed: {health['status']}")
        print(f"   CCXT Available: {health['ccxt_available']}")
        print(f"   Working Exchanges: {len(health['working_exchanges'])}")
        
        return True
    except Exception as e:
        print(f"❌ Crypto data acquisition test failed: {e}")
        return False

def test_sample_data_fetch():
    """Test fetching sample data."""
    try:
        from crypto.data_acquisition import fetch_data
        print("✅ fetch_data imported successfully")
        
        # Try to fetch small sample
        data = fetch_data('BTC/USDT', 'kraken', '1h', 5)
        if data is not None and len(data) > 0:
            print(f"✅ Sample data fetched: {len(data)} bars")
            print(f"   Latest timestamp: {data.index[-1]}")
            print(f"   Price range: ${data['close'].min():.2f} - ${data['close'].max():.2f}")
            return True
        else:
            print("❌ No data returned")
            return False
            
    except Exception as e:
        print(f"❌ Sample data fetch failed: {e}")
        return False

def main():
    """Run all quick tests."""
    print("🚀 QUICK CRYPTO MODULE TEST")
    print("=" * 50)
    
    tests = [
        ("CCXT Library", test_ccxt),
        ("Crypto Data Acquisition", test_crypto_data_acquisition),
        ("Sample Data Fetch", test_sample_data_fetch)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}:")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
        
    print(f"\n📊 SUMMARY:")
    print("=" * 50)
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall: {successful}/{total} tests passed")
    
    if successful == total:
        print("🎉 All tests passed! Crypto module is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the details above.")

if __name__ == "__main__":
    main()
