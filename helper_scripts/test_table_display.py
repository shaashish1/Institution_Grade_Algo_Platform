#!/usr/bin/env python3
"""
Quick test to check crypto price bars tabular display
Tests all symbols from crypto/input/crypto_assets.csv
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Try to import tabulate for better table formatting
try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
    print("✅ Tabulate available for enhanced formatting")
except ImportError:
    TABULATE_AVAILABLE = False
    print("⚠️ Tabulate not available, using pandas formatting")

def test_crypto_data_display():
    """Test crypto data acquisition and tabular display."""
    print("\n🚀 Testing Crypto Data Acquisition & Tabular Display")
    print("=" * 60)
    
    try:
        # Import crypto data acquisition
        from crypto.data_acquisition import fetch_data, health_check
        print("✅ Crypto data acquisition module imported")
        
        # Health check
        print("\n🔍 Running health check...")
        health = health_check()
        print(f"📊 Health Status: {health['status']}")
        print(f"📊 CCXT Available: {health['ccxt_available']}")
        print(f"📊 Working Exchanges: {len(health['working_exchanges'])}")
        
        if not health['ccxt_available']:
            print("❌ CCXT not available")
            return False
        
        if len(health['working_exchanges']) == 0:
            print("❌ No working exchanges found")
            return False
        
        # Read symbols from crypto_assets.csv
        print("\n📂 Loading symbols from crypto_assets.csv...")
        try:
            crypto_assets_path = os.path.join(project_root, 'crypto', 'input', 'crypto_assets.csv')
            if os.path.exists(crypto_assets_path):
                crypto_df = pd.read_csv(crypto_assets_path)
                test_symbols = crypto_df['symbol'].tolist()
                print(f"✅ Loaded {len(test_symbols)} symbols from crypto_assets.csv")
                print(f"📊 Symbols: {', '.join(test_symbols[:5])}{'...' if len(test_symbols) > 5 else ''}")
            else:
                print(f"❌ Crypto assets file not found at: {crypto_assets_path}")
                print("🔄 Falling back to default BTC/USDT")
                test_symbols = ['BTC/USDT']
        except Exception as e:
            print(f"❌ Error reading crypto_assets.csv: {e}")
            print("🔄 Falling back to default BTC/USDT")
            test_symbols = ['BTC/USDT']
        
        # Test data fetching with enhanced display - simplified to 1 bar
        print(f"\n📊 Testing data fetch with tabular display ({len(test_symbols)} symbols, 1 bar each)...")
        
        # Configure pandas display options for better table formatting
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 20)
        pd.set_option('display.float_format', '{:.2f}'.format)
        
        # Track results
        successful_fetches = 0
        failed_fetches = 0
        successful_symbols = []
        
        for i, symbol in enumerate(test_symbols, 1):
            # Use the first working exchange
            exchange = health['working_exchanges'][0] if health['working_exchanges'] else 'kraken'
            print(f"\n🔄 [{i}/{len(test_symbols)}] Fetching {symbol} from {exchange} (last 1 bar)...")
            
            try:
                data = fetch_data(symbol, exchange, '1h', 1)  # Only fetch 1 bar
                if data is not None and len(data) > 0:
                    latest_price = data.iloc[-1]['close']
                    print(f"  ✅ Success: {len(data)} bars, latest: ${latest_price:.2f}")
                    successful_fetches += 1
                    successful_symbols.append(symbol)
                    
                    # Only display detailed table for first few symbols to avoid clutter
                    if i <= 3:  # Show detailed display for first 3 symbols only
                        # Display crypto price bars in tabular format
                        print(f"\n📊 {symbol} Latest Price Data from {exchange.upper()}:")
                        print("=" * 80)
                        
                        # Prepare data for display
                        display_data = data.copy()
                        if 'timestamp' in display_data.columns:
                            display_data['timestamp'] = pd.to_datetime(display_data['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
                        
                        # Use tabulate for better formatting if available
                        if TABULATE_AVAILABLE:
                            print("🎨 Using tabulate for enhanced formatting...")
                            table_str = tabulate(
                                display_data,
                                headers=display_data.columns,
                                tablefmt='grid',
                                floatfmt='.2f',
                                numalign='right',
                                stralign='center'
                            )
                        else:
                            print("📋 Using pandas formatting...")
                            # Fallback to pandas formatting
                            table_str = display_data.to_string(
                                index=False,
                                float_format='{:.2f}'.format,
                                col_space=12,
                                justify='center'
                            )
                        
                        # Display the table
                        print(table_str)
                        print("=" * 80)
                        
                        # Display summary for the single row
                        print(f"\n📈 {symbol} Current Data Summary:")
                        print(f"  💰 Current Price: ${latest_price:.2f}")
                        print(f"  📊 High: ${display_data['high'].iloc[0]:.2f}")
                        print(f"  📉 Low: ${display_data['low'].iloc[0]:.2f}")
                        print(f"  📊 Volume: {display_data['volume'].iloc[0]:,.0f}")
                        print(f"  📊 Spread: ${(display_data['high'].iloc[0] - display_data['low'].iloc[0]):.2f}")
                    else:
                        # Just show basic info for remaining symbols
                        print(f"  💰 Price: ${latest_price:.2f}")
                        
                else:
                    print(f"  ⚠️ No data returned for {symbol} from {exchange}")
                    failed_fetches += 1
            except Exception as e:
                print(f"  ❌ Error fetching {symbol} from {exchange}: {e}")
                failed_fetches += 1
        
        # Display summary
        print(f"\n📊 TEST SUMMARY:")
        print("=" * 50)
        print(f"✅ Successful fetches: {successful_fetches}/{len(test_symbols)}")
        print(f"❌ Failed fetches: {failed_fetches}/{len(test_symbols)}")
        if successful_symbols:
            print(f"🎯 Success rate: {(successful_fetches/len(test_symbols)*100):.1f}%")
            print(f"✅ Working symbols: {', '.join(successful_symbols[:10])}{'...' if len(successful_symbols) > 10 else ''}")
        
        return successful_fetches > 0
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_crypto_data_display()
    if success:
        print("\n🎉 Tabular display test completed successfully!")
    else:
        print("\n❌ Tabular display test failed!")
