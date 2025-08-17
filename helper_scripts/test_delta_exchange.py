#!/usr/bin/env python3
"""
Test Delta Exchange connectivity via CCXT.
Quick validation script to ensure Delta Exchange pairs can be fetched.
"""

def test_delta_exchange():
    """Test Delta Exchange connection and pair fetching."""
    
    print("🔗 Testing Delta Exchange via CCXT...")
    print("="*50)
    
    try:
        # Test CCXT import
        import ccxt
        print(f"✅ CCXT imported successfully (version: {ccxt.__version__})")
        
        # Check if Delta is available
        if 'delta' in ccxt.exchanges:
            print("✅ Delta Exchange is available in CCXT")
        else:
            print("❌ Delta Exchange not found in CCXT exchanges")
            print(f"Available exchanges: {len(ccxt.exchanges)} total")
            return False
        
        # Initialize Delta Exchange
        print("\n🔌 Initializing Delta Exchange connection...")
        delta = ccxt.delta({
            'sandbox': False,
            'enableRateLimit': True,
            'timeout': 30000,
        })
        
        print(f"✅ Delta Exchange instance created: {delta.id}")
        
        # Load markets
        print("\n📊 Loading Delta Exchange markets...")
        markets = delta.load_markets()
        
        print(f"✅ Loaded {len(markets)} markets from Delta Exchange")
        
        # Extract USDT pairs
        usdt_pairs = [symbol for symbol in markets.keys() if 'USDT' in symbol and markets[symbol]['active']]
        
        print(f"✅ Found {len(usdt_pairs)} active USDT pairs")
        
        # Show top 10 pairs
        print(f"\n🔥 Top 10 USDT pairs:")
        for i, pair in enumerate(usdt_pairs[:10], 1):
            market = markets[pair]
            print(f"   {i:2d}. {pair:15s} - {market.get('info', {}).get('description', 'N/A')}")
        
        # Test fetching data for BTC/USDT
        if 'BTC/USDT' in usdt_pairs:
            print(f"\n📈 Testing data fetch for BTC/USDT...")
            try:
                ohlcv = delta.fetch_ohlcv('BTC/USDT', '1h', limit=10)
                print(f"✅ Successfully fetched {len(ohlcv)} OHLCV bars for BTC/USDT")
                
                # Show latest candle
                if ohlcv:
                    latest = ohlcv[-1]
                    timestamp, open_p, high, low, close, volume = latest
                    from datetime import datetime
                    dt = datetime.fromtimestamp(timestamp / 1000)
                    print(f"   Latest: {dt} | O:{open_p} H:{high} L:{low} C:{close} V:{volume}")
                
            except Exception as e:
                print(f"❌ Failed to fetch OHLCV data: {e}")
        
        print(f"\n🎉 Delta Exchange test completed successfully!")
        print(f"💡 Ready to use {len(usdt_pairs)} pairs for backtesting")
        
        return True
        
    except ImportError:
        print("❌ CCXT library not installed")
        print("💡 Install with: pip install ccxt")
        return False
        
    except Exception as e:
        print(f"❌ Error testing Delta Exchange: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_delta_exchange()
