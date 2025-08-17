#!/usr/bin/env python3
"""
Live NSE Quotes Utility
Real-time NSE stock price monitoring using nsepython.
"""

from nsepython import *
import time
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Nifty and Bank Nifty stock symbols (sample subset)
nifty50_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]
banknifty_stocks = ["AXISBANK", "KOTAKBANK", "SBIN", "BANKBARODA", "PNB"]

def fetch_live_data(symbols, category=""):
    """Fetch and display live NSE data for given symbols."""
    print("-" * 70)
    print(f"{'Symbol':<12}{'LTP':>10}{'% Change':>12}{'Volume':>12}")
    print("-" * 70)
    for symbol in symbols:
        try:
            data = nse_quote(symbol)
            ltp = data['priceInfo']['lastPrice']
            change = data['priceInfo']['pChange']
            volume = data['securityWiseDP']['quantityTraded']
            print(f"{symbol:<12}{ltp:>10,.2f}{change:>12,.2f}%{volume:>12,}")
        except Exception as e:
            print(f"{symbol:<12} Error: {e}")
    print("-" * 70)

def load_symbols_from_csv():
    """Load symbols from the stocks_assets.csv file if available."""
    try:
        import pandas as pd
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'stocks', 'input', 'stocks_assets.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            if 'symbol' in df.columns:
                return df['symbol'].tolist()[:20]  # Limit to first 20 for performance
    except:
        pass
    return nifty50_stocks  # Fallback to default list

def main():
    """Main function to run live NSE quotes."""
    print("🚀 Live NSE Quotes Monitor")
    print("=" * 70)
    
    # Try to load symbols from CSV, fallback to defaults
    symbols = load_symbols_from_csv()
    
    try:
        while True:
            print(f"\n📈 Live NSE Data ({len(symbols)} symbols)")
            fetch_live_data(symbols)
            print(f"\n🏦 Live Bank Nifty Data")
            fetch_live_data(banknifty_stocks)
            
            print(f"\n⏰ Refreshing in 10 seconds... (Press Ctrl+C to stop)")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print(f"\n\n✅ Live NSE quotes monitoring stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    while True:
        print("\n📈 Live Nifty 50 Data")
        fetch_live_data(nifty50_stocks)
        print("\n🏦 Live Bank Nifty Data")
        fetch_live_data(banknifty_stocks)
        time.sleep(10)  # wait 10 seconds before refreshing
