#!/usr/bin/env python3
"""
List available crypto assets from Kraken exchange
Si        print(f"✅ Saved {len(usdt_pairs)} USDT pairs to {output_file}")
        print(f"📋 Detailed info saved to {detailed_file}")
        
        # Show priority distribution
        priority_stats = {
            'Top Tier (80+)': len(df_detailed[df_detailed['priority'] >= 80]),
            'Popular (50-79)': len(df_detailed[(df_detailed['priority'] >= 50) & (df_detailed['priority'] < 80)]),
            'Standard (20-49)': len(df_detailed[(df_detailed['priority'] >= 20) & (df_detailed['priority'] < 50)]),
            'Emerging (<20)': len(df_detailed[df_detailed['priority'] < 20])
        }
        
        print(f"\n🏆 **PRIORITY DISTRIBUTION**")
        for category, count in priority_stats.items():
            if count > 0:
                print(f"   {category}: {count} pairs")
        
        return usdt_pairsuick USDT pair listing and CSV generation
"""
import ccxt
import pandas as pd
import os
from tabulate import tabulate

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
        print("🔄 Fetching USDT pairs from Kraken...")
        exchange = ccxt.kraken()
        markets = exchange.load_markets()
        
        # Filter for USDT pairs only
        usdt_pairs = [symbol for symbol in markets.keys() if '/USDT' in symbol]
        
        # Sort by priority (highest first)
        usdt_pairs_with_priority = [(symbol, get_symbol_priority(symbol)) for symbol in usdt_pairs]
        usdt_pairs_with_priority.sort(key=lambda x: x[1], reverse=True)
        usdt_pairs = [symbol for symbol, _ in usdt_pairs_with_priority]
        
        print(f"✅ Found {len(usdt_pairs)} USDT pairs on Kraken")
        
        # Display top pairs
        print(f"\n📊 **TOP USDT PAIRS BY PRIORITY**")
        print("-" * 50)
        
        display_data = []
        for i, (symbol, priority) in enumerate(usdt_pairs_with_priority[:20], 1):
            base = symbol.split('/')[0]
            display_data.append([i, symbol, base, priority])
        
        print(tabulate(display_data, headers=['#', 'Symbol', 'Base', 'Priority'], tablefmt='grid'))
        
        if len(usdt_pairs) > 20:
            print(f"\n... and {len(usdt_pairs) - 20} more pairs")
        
        # Ensure input directory exists
        os.makedirs("crypto/input", exist_ok=True)
        
        # Save simple format for backtest compatibility
        df_simple = pd.DataFrame({'symbol': usdt_pairs})
        output_file = 'crypto/input/crypto_assets.csv'
        df_simple.to_csv(output_file, index=False)
        
        # Save detailed format for reference
        df_detailed = pd.DataFrame([{
            'symbol': symbol,
            'base': symbol.split('/')[0],
            'quote': 'USDT',
            'exchange': 'kraken',
            'priority': priority
        } for symbol, priority in usdt_pairs_with_priority])
        
        detailed_file = 'crypto/input/crypto_assets_detailed.csv'
        df_detailed.to_csv(detailed_file, index=False)
        
        print(f"\n✅ Saved {len(usdt_pairs)} USDT pairs to {output_file}")
        print(f"📋 Detailed info saved to {detailed_file}")
        
        # Show priority distribution
        priority_stats = {
            'Top Tier (80+)': len(df_detailed[df_detailed['priority'] >= 80]),
            'Popular (50-79)': len(df_detailed[(df_detailed['priority'] >= 50) & (df_detailed['priority'] < 80)]),
            'Standard (20-49)': len(df_detailed[(df_detailed['priority'] >= 20) & (df_detailed['priority'] < 50)]),
            'Emerging (<20)': len(df_detailed[df_detailed['priority'] < 20])
        }
        
        print(f"\n🏆 **PRIORITY DISTRIBUTION**")
        for category, count in priority_stats.items():
            if count > 0:
                print(f"   {category}: {count} pairs")
        
        return usdt_pairs
        
    except Exception as e:
        print(f"❌ Error fetching Kraken markets: {e}")
        return []

def main():
    """Main function with enhanced output."""
    print("🚀 Kraken USDT Pairs Listing")
    print("=" * 40)
    
    pairs = list_kraken_usdt_pairs()
    
    if pairs:
        print(f"\n🎉 **LISTING COMPLETE!**")
        print(f"📁 Symbols saved to: crypto/input/crypto_assets.csv")
        print(f"📊 Detailed info: crypto/input/crypto_assets_detailed.csv")
        print(f"🚀 Ready to run: python scripts/crypto_backtest.py")
    else:
        print("\n❌ Failed to fetch symbols from Kraken")

if __name__ == "__main__":
    main()
