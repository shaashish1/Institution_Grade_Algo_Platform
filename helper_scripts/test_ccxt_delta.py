#!/usr/bin/env python3
"""
Test CCXT Delta Exchange Support
"""

try:
    import ccxt
    print("✅ CCXT imported successfully")
    print(f"📊 CCXT version: {ccxt.__version__}")
    
    # List all exchanges
    exchanges = ccxt.exchanges
    print(f"\n📈 Total exchanges: {len(exchanges)}")
    
    # Check for Delta Exchange
    delta_variants = [ex for ex in exchanges if 'delta' in ex.lower()]
    print(f"\n🔍 Delta-related exchanges: {delta_variants}")
    
    # Check specifically for Delta Exchange
    if 'delta' in exchanges:
        print("✅ Delta Exchange found in CCXT!")
        
        # Try to initialize
        try:
            delta = ccxt.delta()
            print("✅ Delta Exchange initialized successfully")
            
            # Try to load markets (requires internet)
            try:
                markets = delta.load_markets()
                print(f"✅ Loaded {len(markets)} markets from Delta Exchange")
                
                # Show some USDT pairs
                usdt_pairs = [pair for pair in markets.keys() if 'USDT' in pair][:10]
                print(f"💰 Sample USDT pairs: {usdt_pairs}")
                
            except Exception as e:
                print(f"⚠️  Could not load markets: {e}")
                
        except Exception as e:
            print(f"❌ Could not initialize Delta Exchange: {e}")
    else:
        print("❌ Delta Exchange not found in CCXT")
        print("💡 Available exchanges with 'delta' in name:", delta_variants)
        
        # Show some popular exchanges
        popular = ['binance', 'kraken', 'coinbase', 'bybit', 'okx']
        available_popular = [ex for ex in popular if ex in exchanges]
        print(f"🔥 Popular available exchanges: {available_popular}")

except ImportError as e:
    print(f"❌ Could not import CCXT: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
