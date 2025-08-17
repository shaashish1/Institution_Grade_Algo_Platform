#!/usr/bin/env python3
"""
Minimal Delta Exchange CCXT Test
Tests only Delta Exchange without pandas dependencies
"""

import sys
import time
import json
from datetime import datetime

def test_ccxt_delta_only():
    """Test CCXT specifically for Delta Exchange."""
    print("🎯 MINIMAL DELTA EXCHANGE CCXT TEST")
    print("="*50)
    
    try:
        print("Step 1: Importing CCXT...", end=" ")
        import ccxt
        print("✅ Success")
        
        print(f"Step 2: CCXT Version: {ccxt.__version__}")
        
        print("Step 3: Checking Delta Exchange...", end=" ")
        if 'delta' in ccxt.exchanges:
            print("✅ Delta found in exchanges")
        else:
            print("❌ Delta NOT found")
            print(f"Available exchanges starting with 'd': {[x for x in ccxt.exchanges if x.startswith('d')]}")
            return False
        
        print("Step 4: Creating Delta instance...", end=" ")
        delta = ccxt.delta({
            'timeout': 3000,  # 3 seconds
            'enableRateLimit': True,
            'sandbox': False
        })
        print("✅ Success")
        
        print("Step 5: Loading markets (this might take time)...", end=" ")
        sys.stdout.flush()
        
        # This is the critical test
        markets = delta.load_markets()
        
        if markets:
            print(f"✅ Success - {len(markets)} markets loaded")
            
            # Show some popular symbols
            popular_symbols = []
            for symbol in ['BTC/USDT', 'ETH/USDT', 'BTC/USD', 'ETH/USD']:
                if symbol in markets:
                    popular_symbols.append(symbol)
            
            print(f"Popular symbols available: {popular_symbols}")
            
            if popular_symbols:
                test_symbol = popular_symbols[0]
                print(f"Step 6: Testing data fetch for {test_symbol}...", end=" ")
                
                try:
                    ohlcv = delta.fetch_ohlcv(test_symbol, '1h', limit=5)
                    if ohlcv and len(ohlcv) > 0:
                        print(f"✅ Success - {len(ohlcv)} candles")
                        
                        # Show sample data
                        latest = ohlcv[-1]
                        print(f"Latest {test_symbol}: ${latest[4]:,.2f}")
                        
                        return True
                    else:
                        print("❌ No data received")
                        return False
                        
                except Exception as e:
                    print(f"❌ Data fetch error: {str(e)[:50]}")
                    return False
            else:
                print("❌ No popular symbols found")
                return False
        else:
            print("❌ No markets loaded")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function."""
    success = test_ccxt_delta_only()
    
    print("\n" + "="*50)
    if success:
        print("✅ DELTA EXCHANGE CCXT TEST PASSED")
        print("Ready for production integration!")
    else:
        print("❌ DELTA EXCHANGE CCXT TEST FAILED")
        print("Continue with demo mode for now")
    print("="*50)
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted")
        sys.exit(1)
