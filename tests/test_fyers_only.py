#!/usr/bin/env python3
"""
Simple test for Fyers data flow using existing credentials
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_acquisition import fetch_data, test_fyers_connection, get_live_quote

def main():
    print("🚀 Testing Fyers-Only Data Flow")
    print("=" * 50)
    
    # Test 1: Connection test
    print("\n1. Testing Fyers connection...")
    try:
        if test_fyers_connection():
            print("✅ Connection successful")
        else:
            print("❌ Connection failed")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # Test 2: Historical data
    print("\n2. Testing historical data...")
    try:
        data = fetch_data("RELIANCE", "NSE", "5m", 10, data_source="fyers")
        if not data.empty:
            print(f"✅ Historical data: {len(data)} bars")
            print(f"📅 Date range: {data['timestamp'].min()} to {data['timestamp'].max()}")
            print(f"💰 Latest close: ₹{data['close'].iloc[-1]:.2f}")
        else:
            print("❌ No historical data")
    except Exception as e:
        print(f"❌ Historical data error: {e}")
    
    # Test 3: Live quote
    print("\n3. Testing live quote...")
    try:
        quote = get_live_quote("RELIANCE", "NSE")
        if quote:
            print(f"✅ Live quote: ₹{quote['ltp']:.2f}")
        else:
            print("❌ No live quote")
    except Exception as e:
        print(f"❌ Live quote error: {e}")
    
    # Test 4: Multiple symbols
    print("\n4. Testing multiple symbols...")
    test_symbols = ["RELIANCE", "TCS", "INFY"]
    for symbol in test_symbols:
        try:
            data = fetch_data(symbol, "NSE", "5m", 5, data_source="fyers")
            if not data.empty:
                print(f"✅ {symbol}: ₹{data['close'].iloc[-1]:.2f}")
            else:
                print(f"❌ {symbol}: No data")
        except Exception as e:
            print(f"❌ {symbol}: {e}")
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    main()
