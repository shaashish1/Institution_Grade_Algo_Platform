#!/usr/bin/env python3
"""
Minimal CCXT Test - Step by step debugging
"""

import sys
import time

print("🔧 Step 1: Testing Python import system...")
try:
    import pandas as pd
    print("✅ Pandas imported successfully")
except Exception as e:
    print(f"❌ Pandas import failed: {e}")

print("\n🔧 Step 2: Testing CCXT import...")
try:
    print("   Importing ccxt module...", end="")
    import ccxt
    print(" ✅ Success")
    
    print(f"   CCXT version: {ccxt.__version__}")
    print(f"   Exchanges available: {len(ccxt.exchanges)}")
    
except Exception as e:
    print(f" ❌ Failed: {e}")
    sys.exit(1)

print("\n🔧 Step 3: Testing basic ccxt functionality...")
try:
    print("   Getting exchange list...", end="")
    exchanges = ccxt.exchanges
    print(f" ✅ Got {len(exchanges)} exchanges")
    
    print("   Checking for popular exchanges...")
    popular = ['binance', 'kraken', 'coinbase']
    for exchange in popular:
        status = "✅" if exchange in exchanges else "❌"
        print(f"   {status} {exchange}")
        
except Exception as e:
    print(f" ❌ Failed: {e}")
    sys.exit(1)

print("\n🔧 Step 4: Testing exchange creation (without network)...")
try:
    print("   Creating Binance instance...", end="")
    binance = ccxt.binance()
    print(" ✅ Success")
    
    print("   Creating Kraken instance...", end="")
    kraken = ccxt.kraken()
    print(" ✅ Success")
    
except Exception as e:
    print(f" ❌ Failed: {e}")
    sys.exit(1)

print("\n🔧 Step 5: Testing network call with timeout...")
try:
    print("   Testing Binance ping (5 sec timeout)...", end="")
    binance = ccxt.binance({'timeout': 5000})  # 5 seconds
    
    # This is where it usually hangs
    result = binance.fetch_status()
    print(f" ✅ Success: {result}")
    
except Exception as e:
    print(f" ❌ Failed: {e}")

print("\n🔧 Step 6: Testing Delta Exchange...")
try:
    if 'delta' in ccxt.exchanges:
        print("   Delta found in exchanges")
        delta = ccxt.delta({'timeout': 5000})
        print("   Delta instance created")
    else:
        print("   ❌ Delta not found in CCXT")
        print(f"   Available exchanges starting with 'd': {[x for x in ccxt.exchanges if x.startswith('d')]}")
        
except Exception as e:
    print(f" ❌ Delta test failed: {e}")

print("\n✅ Minimal CCXT test completed")
print("If this hangs, the issue is in Step 5 (network calls)")
