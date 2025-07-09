#!/usr/bin/env python3
"""
List available crypto assets from Kraken exchange
"""
import ccxt
import pandas as pd

def list_kraken_usdt_pairs():
    """List all USDT trading pairs available on Kraken."""
    try:
        exchange = ccxt.kraken()
        markets = exchange.load_markets()
        
        # Filter for USDT pairs only
        usdt_pairs = [symbol for symbol in markets.keys() if '/USDT' in symbol]
        usdt_pairs.sort()
        
        print(f"Found {len(usdt_pairs)} USDT pairs on Kraken:")
        print("-" * 40)
        for pair in usdt_pairs:
            print(pair)
        
        # Save to CSV
        df = pd.DataFrame({'symbol': usdt_pairs})
        output_file = 'input/crypto_assets.csv'
        df.to_csv(output_file, index=False)
        print(f"\n✅ Saved {len(usdt_pairs)} USDT pairs to {output_file}")
        
        return usdt_pairs
        
    except Exception as e:
        print(f"❌ Error fetching Kraken markets: {e}")
        return []

if __name__ == "__main__":
    list_kraken_usdt_pairs()
