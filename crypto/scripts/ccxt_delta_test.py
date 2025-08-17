#!/usr/bin/env python3
"""
Comprehensive CCXT and Delta Exchange Test
Tests CCXT installation, available exchanges, and specifically Delta Exchange
"""

import sys
import time
from datetime import datetime

def test_ccxt_installation():
    """Test CCXT installation and basic functionality."""
    try:
        print("🔧 Testing CCXT installation...")
        import ccxt
        print(f"✅ CCXT Version: {ccxt.__version__}")
        print(f"✅ Available exchanges: {len(ccxt.exchanges)}")
        
        # Check if delta is available
        if 'delta' in ccxt.exchanges:
            print("✅ Delta Exchange is available in CCXT")
        else:
            print("❌ Delta Exchange NOT found in CCXT")
            print("Available exchanges with 'delta' in name:", [x for x in ccxt.exchanges if 'delta' in x.lower()])
        
        return True
    except ImportError as e:
        print(f"❌ CCXT not installed: {e}")
        return False
    except Exception as e:
        print(f"❌ CCXT error: {e}")
        return False

def test_popular_exchanges():
    """Test connection to popular exchanges."""
    try:
        import ccxt
        
        # Test popular exchanges with short timeouts
        test_exchanges = ['binance', 'kraken', 'coinbase', 'bitfinex']
        
        print("\n📊 Testing popular exchanges...")
        working_exchanges = []
        
        for exchange_name in test_exchanges:
            if exchange_name not in ccxt.exchanges:
                print(f"❌ {exchange_name}: Not available")
                continue
                
            try:
                print(f"🔄 Testing {exchange_name}...", end=" ")
                
                # Create exchange instance with short timeout
                exchange_class = getattr(ccxt, exchange_name)
                exchange = exchange_class({
                    'timeout': 3000,  # 3 seconds
                    'enableRateLimit': True,
                    'sandbox': False
                })
                
                # Test basic connection
                markets = exchange.load_markets()
                
                if markets and len(markets) > 0:
                    print(f"✅ {len(markets)} markets")
                    working_exchanges.append(exchange_name)
                else:
                    print("❌ No markets")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}")
                continue
        
        print(f"\n✅ Working exchanges: {working_exchanges}")
        return working_exchanges
        
    except Exception as e:
        print(f"❌ Error testing exchanges: {e}")
        return []

def test_delta_exchange():
    """Test Delta Exchange specifically."""
    try:
        import ccxt
        
        print("\n🎯 Testing Delta Exchange specifically...")
        
        # Check if delta is in the list
        if 'delta' not in ccxt.exchanges:
            print("❌ Delta Exchange not found in CCXT exchanges list")
            
            # Look for similar exchanges
            delta_like = [x for x in ccxt.exchanges if 'delta' in x.lower()]
            if delta_like:
                print(f"📍 Found similar exchanges: {delta_like}")
            else:
                print("📍 No exchanges with 'delta' in name found")
            return False
        
        try:
            print("🔄 Creating Delta Exchange instance...", end=" ")
            
            # Create delta exchange instance
            delta = ccxt.delta({
                'timeout': 5000,  # 5 seconds
                'enableRateLimit': True,
                'sandbox': False
            })
            
            print("✅ Instance created")
            
            # Test loading markets
            print("🔄 Loading Delta markets...", end=" ")
            markets = delta.load_markets()
            
            if markets:
                print(f"✅ {len(markets)} markets loaded")
                
                # Show some popular symbols
                symbols = list(markets.keys())[:10]
                print(f"📊 Sample symbols: {symbols}")
                
                # Test fetching OHLCV data
                print("🔄 Testing data fetch...", end=" ")
                
                # Try to find a popular symbol
                test_symbols = ['BTC/USDT', 'ETH/USDT', 'BTC/USD']
                for symbol in test_symbols:
                    if symbol in markets:
                        try:
                            ohlcv = delta.fetch_ohlcv(symbol, '1h', limit=5)
                            if ohlcv and len(ohlcv) > 0:
                                print(f"✅ Got {len(ohlcv)} bars for {symbol}")
                                return True
                        except Exception as e:
                            print(f"❌ Data fetch error for {symbol}: {str(e)[:30]}")
                            continue
                
                print("❌ No data could be fetched")
                return False
            else:
                print("❌ No markets loaded")
                return False
                
        except Exception as e:
            print(f"❌ Delta Exchange error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error in Delta test: {e}")
        return False

def test_simple_data_fetch():
    """Test simple data fetching from working exchanges."""
    try:
        import ccxt
        
        print("\n📈 Testing simple data fetch...")
        
        # Try the most reliable exchanges
        reliable_exchanges = ['binance', 'kraken']
        
        for exchange_name in reliable_exchanges:
            if exchange_name not in ccxt.exchanges:
                continue
                
            try:
                print(f"🔄 Testing {exchange_name}...", end=" ")
                
                exchange_class = getattr(ccxt, exchange_name)
                exchange = exchange_class({
                    'timeout': 5000,  # 5 seconds
                    'enableRateLimit': True
                })
                
                # Quick test with BTC/USDT
                ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h', limit=5)
                
                if ohlcv and len(ohlcv) > 0:
                    print(f"✅ Got {len(ohlcv)} bars from {exchange_name}")
                    latest_price = ohlcv[-1][4]  # Close price
                    print(f"   📊 Latest BTC/USDT close: ${latest_price:,.2f}")
                    return True
                else:
                    print(f"❌ No data from {exchange_name}")
                    
            except Exception as e:
                print(f"❌ {exchange_name} error: {str(e)[:50]}")
                continue
        
        return False
        
    except Exception as e:
        print(f"❌ Error in simple data fetch: {e}")
        return False

def test_network_connectivity():
    """Test basic network connectivity."""
    try:
        print("\n🌐 Testing network connectivity...")
        
        import urllib.request
        import socket
        
        # Test basic internet connectivity
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            print("✅ Internet connectivity: OK")
        except Exception:
            print("❌ Internet connectivity: FAILED")
            return False
        
        # Test HTTPS connectivity to popular exchanges
        test_urls = [
            'https://api.binance.com/api/v3/ping',
            'https://api.kraken.com/0/public/SystemStatus'
        ]
        
        for url in test_urls:
            try:
                response = urllib.request.urlopen(url, timeout=5)
                if response.getcode() == 200:
                    print(f"✅ {url}: OK")
                else:
                    print(f"❌ {url}: HTTP {response.getcode()}")
            except Exception as e:
                print(f"❌ {url}: {str(e)[:50]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Network test error: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 COMPREHENSIVE CCXT & DELTA EXCHANGE TEST")
    print("="*60)
    print(f"Timestamp: {datetime.now()}")
    print("="*60)
    
    # Test 1: CCXT Installation
    ccxt_ok = test_ccxt_installation()
    
    if not ccxt_ok:
        print("\n❌ CCXT installation failed - aborting tests")
        return
    
    # Test 2: Network connectivity
    network_ok = test_network_connectivity()
    
    # Test 3: Popular exchanges
    working_exchanges = test_popular_exchanges()
    
    # Test 4: Delta Exchange specifically
    delta_ok = test_delta_exchange()
    
    # Test 5: Simple data fetch
    data_ok = test_simple_data_fetch()
    
    # Summary
    print("\n" + "="*60)
    print("🎯 TEST SUMMARY")
    print("="*60)
    print(f"CCXT Installation: {'✅ OK' if ccxt_ok else '❌ FAILED'}")
    print(f"Network Connectivity: {'✅ OK' if network_ok else '❌ FAILED'}")
    print(f"Working Exchanges: {len(working_exchanges)} ({', '.join(working_exchanges)})")
    print(f"Delta Exchange: {'✅ OK' if delta_ok else '❌ FAILED'}")
    print(f"Data Fetching: {'✅ OK' if data_ok else '❌ FAILED'}")
    
    if data_ok:
        print("\n✅ CCXT is working - issue might be elsewhere")
    elif not network_ok:
        print("\n❌ Network connectivity issues detected")
    elif not working_exchanges:
        print("\n❌ No exchanges working - possible firewall/proxy issue")
    else:
        print("\n⚠️ Mixed results - check specific exchange configurations")
    
    print("="*60)

if __name__ == "__main__":
    main()
