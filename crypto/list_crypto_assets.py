#!/usr/bin/env python3
"""
List available crypto assets from Kraken exchange
Quick USDT pair listing and CSV generation
"""

import pandas as pd
import os
from tabulate import tabulate

# Lazy import CCXT to avoid hanging on module load
ccxt = None

def _ensure_ccxt():
    """Ensure CCXT is imported when needed"""
    global ccxt
    if ccxt is None:
        try:
            import ccxt as _ccxt
            ccxt = _ccxt
            print("✅ CCXT imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import CCXT: {e}")
            raise
        except Exception as e:
            print(f"❌ Error importing CCXT: {e}")
            raise
    return ccxt

def get_symbol_priority(symbol):
    """Get priority score for a symbol based on popularity."""
    base = symbol.split('/')[0]
    
    # Base currency priority (simplified version)
    base_priority = {
        # Top cryptocurrencies
        'BTC': 100, 'ETH': 95, 'BNB': 90, 'XRP': 85, 'ADA': 80,
        'DOGE': 75, 'SOL': 70, 'DOT': 65, 'AVAX': 60, 'SHIB': 55,
        'MATIC': 50, 'LTC': 48, 'UNI': 46, 'LINK': 44, 'ATOM': 42,
        'XLM': 40, 'ALGO': 38, 'VET': 36, 'FIL': 34, 'TRX': 32,
        # DeFi tokens
        'AAVE': 30, 'COMP': 28, 'YFI': 26, 'SUSHI': 24, 'CRV': 22,
        # Meme coins
        'PEPE': 20, 'FLOKI': 18,
        # Others
        'NEAR': 25, 'FTM': 21, 'ONE': 19, 'HBAR': 17,
    }
    
    return base_priority.get(base, 5)

def list_kraken_usdt_pairs():
    """List all USDT trading pairs available on Kraken."""
    try:
        ccxt_lib = _ensure_ccxt()
        print("🔄 Connecting to Kraken...")
        
        # Initialize Kraken exchange
        kraken = ccxt_lib.kraken()
        
        # Fetch all markets
        markets = kraken.load_markets()
        
        # Filter for USDT pairs
        usdt_pairs = []
        for symbol, market in markets.items():
            if symbol.endswith('/USDT'):
                base = market['base']
                quote = market['quote']
                priority = get_symbol_priority(symbol)
                
                usdt_pairs.append({
                    'symbol': symbol,
                    'base': base,
                    'quote': quote,
                    'priority': priority,
                    'active': market.get('active', True)
                })
        
        # Sort by priority (highest first)
        usdt_pairs.sort(key=lambda x: x['priority'], reverse=True)
        
        print(f"✅ Found {len(usdt_pairs)} USDT pairs on Kraken")
        return usdt_pairs
        
    except Exception as e:
        print(f"❌ Error fetching Kraken data: {e}")
        return []

def save_to_csv(pairs, output_dir='input'):
    """Save pairs to CSV file."""
    if not pairs:
        print("❌ No pairs to save")
        return None
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create DataFrame
    df = pd.DataFrame(pairs)
    
    # Save main CSV
    output_file = os.path.join(output_dir, 'kraken_usdt_pairs.csv')
    df.to_csv(output_file, index=False)
    
    print(f"✅ Saved {len(pairs)} USDT pairs to {output_file}")
    return output_file

def display_pairs(pairs, limit=20):
    """Display pairs in a formatted table."""
    if not pairs:
        print("❌ No pairs to display")
        return
    
    # Prepare data for display
    display_data = []
    for i, pair in enumerate(pairs[:limit]):
        display_data.append([
            i+1,
            pair['symbol'],
            pair['base'],
            pair['priority'],
            '✅' if pair['active'] else '❌'
        ])
    
    headers = ['#', 'Symbol', 'Base Currency', 'Priority', 'Active']
    
    print(f"\n📊 **TOP {len(display_data)} KRAKEN USDT PAIRS**")
    print(tabulate(display_data, headers=headers, tablefmt='grid'))
    
    if len(pairs) > limit:
        print(f"\n... and {len(pairs) - limit} more pairs")

def main():
    """Main function to run the crypto asset lister."""
    print("🚀 **KRAKEN CRYPTO ASSET LISTER**")
    print("=" * 50)
    
    # List USDT pairs
    pairs = list_kraken_usdt_pairs()
    
    if pairs:
        # Display top pairs
        display_pairs(pairs, 20)
        
        # Save to CSV
        save_to_csv(pairs)
        
        print(f"\n✅ **SUMMARY**")
        print(f"   📈 Total USDT pairs found: {len(pairs)}")
        print(f"   💾 CSV files saved to 'input/' directory")
    else:
        print("❌ No pairs found")

if __name__ == "__main__":
    main()
