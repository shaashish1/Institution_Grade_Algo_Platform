#!/usr/bin/env python3
"""
Delta Exchange Trading Pairs - Direct CCXT Integration
Simple test to fetch and display real Delta Exchange trading pairs.
"""

def main():
    print("🎯 DELTA EXCHANGE TRADING PAIRS FETCHER")
    print("=" * 50)
    
    try:
        print("1. Testing CCXT import...")
        import ccxt
        print(f"   ✅ CCXT version: {ccxt.__version__}")
        
        print("2. Testing Delta Exchange availability...")
        if 'delta' not in ccxt.exchanges:
            print("   ❌ Delta Exchange not found in CCXT")
            return False
        
        print("   ✅ Delta Exchange found in CCXT")
        
        print("3. Creating Delta Exchange instance...")
        delta = ccxt.delta({
            'enableRateLimit': True,
            'timeout': 20000,
        })
        
        print(f"   ✅ Delta instance created: {delta.id}")
        
        print("4. Loading markets...")
        markets = delta.load_markets()
        
        print(f"   ✅ Loaded {len(markets)} total markets")
        
        # Filter USDT pairs
        usdt_pairs = []
        for symbol, market in markets.items():
            if 'USDT' in symbol and market.get('active', False):
                usdt_pairs.append(symbol)
        
        print(f"   ✅ Found {len(usdt_pairs)} active USDT pairs")
        
        # Display top pairs
        print(f"\n🔥 TOP 20 DELTA EXCHANGE USDT PAIRS:")
        print("-" * 40)
        
        for i, pair in enumerate(usdt_pairs[:20], 1):
            market = markets[pair]
            base = market.get('base', '')
            quote = market.get('quote', '')
            print(f"   {i:2d}. {pair:<15} ({base}/{quote})")
        
        if len(usdt_pairs) > 20:
            print(f"   ... and {len(usdt_pairs) - 20} more pairs")
        
        print(f"\n💡 These pairs can be used in delta_backtest_strategies.py")
        print(f"💡 Run: python crypto\\scripts\\delta_backtest_strategies.py --symbols {' '.join(usdt_pairs[:5])}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   💡 Install CCXT: pip install ccxt")
        return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print(f"   ❌ Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print(f"\n⚠️  Delta Exchange connection failed")
        print(f"🔄 Fallback pairs will be used for backtesting:")
        
        fallback = [
            'BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'SOL/USDT', 'MATIC/USDT',
            'DOT/USDT', 'LTC/USDT', 'XRP/USDT', 'LINK/USDT', 'AVAX/USDT'
        ]
        
        for i, pair in enumerate(fallback, 1):
            print(f"   {i:2d}. {pair}")
    
    print(f"\n✅ Ready for backtesting!")
