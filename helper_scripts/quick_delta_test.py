#!/usr/bin/env python3
"""
Simple Delta Exchange CCXT test with timeouts and fallbacks.
"""

import sys
import time

def quick_ccxt_test():
    """Quick CCXT test with timeout handling."""
    
    print("🔗 Quick CCXT Delta Exchange Test")
    print("=" * 40)
    
    try:
        # Test basic import
        print("1. Testing CCXT import...")
        import ccxt
        print(f"   ✅ CCXT version: {ccxt.__version__}")
        
        # Check Delta availability  
        print("2. Checking Delta availability...")
        available = 'delta' in ccxt.exchanges
        print(f"   {'✅' if available else '❌'} Delta in exchanges: {available}")
        
        if not available:
            print(f"   📋 Total exchanges available: {len(ccxt.exchanges)}")
            # Show a few exchange names
            sample_exchanges = list(ccxt.exchanges)[:10]
            print(f"   📋 Sample exchanges: {', '.join(sample_exchanges)}")
            return False
        
        # Try creating instance (no network call yet)
        print("3. Creating Delta instance...")
        delta = ccxt.delta({
            'enableRateLimit': True,
            'timeout': 10000,  # Short timeout
        })
        print(f"   ✅ Delta instance: {delta.id}")
        
        # Test if we can access basic properties
        print("4. Testing basic properties...")
        print(f"   📊 Has markets: {hasattr(delta, 'markets')}")
        print(f"   🌐 API URL: {getattr(delta, 'urls', {}).get('api', 'N/A')}")
        
        print("\n🎉 Basic CCXT Delta test passed!")
        print("💡 Delta Exchange is available via CCXT")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   💡 Try: pip install ccxt")
        return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_fallback_pairs():
    """Show fallback pairs that will be used."""
    print("\n📋 Fallback Trading Pairs:")
    print("-" * 30)
    
    fallback_pairs = [
        'BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'SOL/USDT', 'MATIC/USDT',
        'DOT/USDT', 'LTC/USDT', 'XRP/USDT', 'LINK/USDT', 'AVAX/USDT',
        'ALGO/USDT', 'ATOM/USDT', 'FTM/USDT', 'NEAR/USDT', 'ICP/USDT'
    ]
    
    for i, pair in enumerate(fallback_pairs, 1):
        print(f"   {i:2d}. {pair}")
    
    print(f"\n💡 These {len(fallback_pairs)} pairs will be used for backtesting")

if __name__ == "__main__":
    success = quick_ccxt_test()
    
    if not success:
        print("\n⚠️  CCXT Delta connection not available")
        print("🔄 Will use simulated data for backtesting")
        test_fallback_pairs()
    
    print(f"\nTest completed in {time.time():.1f} seconds")
