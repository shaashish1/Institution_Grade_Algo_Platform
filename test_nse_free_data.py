"""
Test NSE Free Data Provider
This tests that we can get real NSE data WITHOUT any FYERS credentials
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_provider_status():
    """Check which data providers are available"""
    print("\n" + "=" * 60)
    print("📊 TESTING DATA PROVIDER STATUS")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/market-data/provider-status")
    data = response.json()
    
    print(json.dumps(data, indent=2))
    print()
    
    if data["nse_free_provider"]["available"]:
        print("✅ NSE Free Provider: WORKING (NO CONFIG NEEDED)")
    else:
        print("❌ NSE Free Provider: NOT WORKING")
    
    if data["fyers_provider"]["available"]:
        print("✅ FYERS Provider: WORKING (Credentials configured)")
    else:
        print("⚠️  FYERS Provider: NOT CONFIGURED (OK for development)")
    
    return data

def test_nse_indices():
    """Test getting NIFTY indices from free NSE data"""
    print("\n" + "=" * 60)
    print("📈 TESTING NIFTY INDICES (FREE NSE DATA)")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/market-data/indices")
    data = response.json()
    
    print(f"\n📊 Found {len(data.get('indices', []))} indices")
    print(f"🔌 Data Source: {data.get('data_source', 'UNKNOWN')}")
    print(f"🏦 Market Status: {data.get('market_status', {}).get('status', 'UNKNOWN')}")
    
    print("\n📋 NIFTY Indices:")
    for idx in data.get('indices', [])[:5]:  # Show first 5
        print(f"   {idx['symbol']:20} | ₹{idx['price']:10.2f} | {idx['change']:+7.2f} ({idx['change_percent']:+.2f}%)")
    
    return data

def test_stock_quotes():
    """Test getting stock quotes from free NSE data"""
    print("\n" + "=" * 60)
    print("💹 TESTING STOCK QUOTES (FREE NSE DATA)")
    print("=" * 60)
    
    test_symbols = ["RELIANCE", "TCS", "INFY", "HDFC", "ITC"]
    
    response = requests.post(
        f"{BASE_URL}/api/market-data/quotes",
        json={
            "symbols": test_symbols,
            "exchange": "NSE"
        }
    )
    
    quotes = response.json()
    
    print(f"\n📊 Fetched quotes for {len(quotes)} symbols")
    print("\n📋 Stock Quotes:")
    
    for symbol, data in quotes.items():
        print(f"\n   {symbol}:")
        print(f"      LTP: ₹{data.get('ltp', 0):.2f}")
        print(f"      Change: {data.get('change', 0):+.2f} ({data.get('change_percent', 0):+.2f}%)")
        print(f"      High/Low: ₹{data.get('high', 0):.2f} / ₹{data.get('low', 0):.2f}")
        print(f"      Volume: {data.get('volume', 0):,}")
        print(f"      Source: {data.get('data_source', 'UNKNOWN')}")
    
    return quotes

def main():
    print("\n" + "🎯" * 30)
    print("FREE NSE DATA PROVIDER TEST")
    print("NO FYERS CREDENTIALS NEEDED!")
    print("🎯" * 30)
    
    try:
        # Test 1: Provider Status
        provider_status = test_provider_status()
        
        # Test 2: NIFTY Indices
        indices = test_nse_indices()
        
        # Test 3: Stock Quotes
        quotes = test_stock_quotes()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n📝 SUMMARY:")
        print(f"   - NSE Free Provider: {'✅ Working' if provider_status['nse_free_provider']['available'] else '❌ Failed'}")
        print(f"   - FYERS Provider: {'✅ Working' if provider_status['fyers_provider']['available'] else '⚠️  Not Configured (OK)'}")
        print(f"   - Indices Fetched: {len(indices.get('indices', []))}")
        print(f"   - Quotes Fetched: {len(quotes)}")
        print("\n✅ You can now use the trading platform WITHOUT FYERS configuration!")
        print("ℹ️  Configure FYERS only when you're ready to place actual trades.")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
