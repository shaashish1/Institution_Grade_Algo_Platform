#!/usr/bin/env python3
"""
Advanced Crypto Symbol Management
Fetch and manage crypto trading pairs from any CCXT exchange with user selection.
"""

import os
import sys
import pandas as pd
import ccxt
from tabulate import tabulate

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_available_exchanges():
    """Get list of available CCXT exchanges."""
    exchanges = []
    
    # Popular crypto exchanges
    popular_exchanges = [
        'kraken', 'binance', 'coinbase', 'bybit', 'okx', 
        'kucoin', 'huobi', 'bitfinex', 'gemini', 'ftx'
    ]
    
    print("🔍 Checking available exchanges...")
    
    for exchange_id in popular_exchanges:
        try:
            exchange_class = getattr(ccxt, exchange_id, None)
            if exchange_class:
                exchange = exchange_class()
                exchanges.append({
                    'id': exchange_id,
                    'name': exchange.name if hasattr(exchange, 'name') else exchange_id.title(),
                    'countries': exchange.countries if hasattr(exchange, 'countries') else ['Unknown']
                })
        except Exception:
            continue
    
    return exchanges


def fetch_symbols_from_exchange(exchange_id, quote_currencies=None):
    """Fetch trading symbols from a specific exchange."""
    if quote_currencies is None:
        quote_currencies = ['USDT', 'USD', 'EUR', 'BTC', 'ETH']
    
    try:
        # Initialize exchange
        exchange_class = getattr(ccxt, exchange_id.lower())
        exchange = exchange_class()
        
        print(f"🔄 Fetching symbols from {exchange.name}...")
        
        # Fetch markets
        markets = exchange.fetch_markets()
        
        # Group symbols by quote currency
        symbol_groups = {}
        for market in markets:
            if market['active'] and market['spot']:  # Only active spot markets
                symbol = market['symbol']
                base = market['base']
                quote = market['quote']
                
                if quote in quote_currencies:
                    if quote not in symbol_groups:
                        symbol_groups[quote] = []
                    
                    symbol_groups[quote].append({
                        'symbol': symbol,
                        'base': base,
                        'quote': quote,
                        'id': market['id']
                    })
        
        # Sort symbols within each group
        for quote in symbol_groups:
            symbol_groups[quote].sort(key=lambda x: x['base'])
        
        return symbol_groups
        
    except Exception as e:
        print(f"❌ Error fetching symbols from {exchange_id}: {e}")
        return {}


def display_symbol_groups(symbol_groups):
    """Display symbols grouped by quote currency with numbering."""
    print("\n📊 **AVAILABLE TRADING PAIRS**")
    print("=" * 80)
    
    symbol_index = {}
    current_number = 1
    
    for quote, symbols in symbol_groups.items():
        print(f"\n🪙 **{quote} Pairs** ({len(symbols)} pairs)")
        print("-" * 50)
        
        display_data = []
        for symbol_data in symbols:
            symbol_index[current_number] = symbol_data
            display_data.append([
                current_number,
                symbol_data['symbol'],
                symbol_data['base']
            ])
            current_number += 1
        
        # Display in chunks of 20 for readability
        chunk_size = 20
        for i in range(0, len(display_data), chunk_size):
            chunk = display_data[i:i+chunk_size]
            print(tabulate(chunk, headers=['#', 'Symbol', 'Base Currency'], tablefmt='grid'))
            if i + chunk_size < len(display_data):
                input("\nPress Enter to see more symbols...")
    
    return symbol_index


def get_user_selection(symbol_index):
    """Get user selection of symbols."""
    print(f"\n🎯 **SYMBOL SELECTION**")
    print("=" * 50)
    print("Choose symbols by entering numbers (e.g., 1,5,10-15,20)")
    print("Or type 'all' to select all symbols")
    print("Or type 'usdt' to select all USDT pairs")
    print("Or type 'top20' to select top 20 by market cap")
    
    while True:
        try:
            user_input = input("\nEnter your selection: ").strip().lower()
            
            if user_input == 'all':
                return list(symbol_index.values())
            elif user_input == 'usdt':
                return [s for s in symbol_index.values() if s['quote'] == 'USDT']
            elif user_input == 'top20':
                # Get top 20 USDT pairs (assuming they're ordered by popularity)
                usdt_pairs = [s for s in symbol_index.values() if s['quote'] == 'USDT']
                return usdt_pairs[:20]
            else:
                # Parse number ranges and individual numbers
                selected_symbols = []
                parts = user_input.split(',')
                
                for part in parts:
                    part = part.strip()
                    if '-' in part:
                        # Range like 10-15
                        start, end = map(int, part.split('-'))
                        for num in range(start, end + 1):
                            if num in symbol_index:
                                selected_symbols.append(symbol_index[num])
                    else:
                        # Individual number
                        num = int(part)
                        if num in symbol_index:
                            selected_symbols.append(symbol_index[num])
                
                if selected_symbols:
                    return selected_symbols
                else:
                    print("❌ No valid symbols selected. Please try again.")
        
        except ValueError:
            print("❌ Invalid input format. Please try again.")
        except KeyboardInterrupt:
            return []


def save_selected_symbols(symbols, exchange_id):
    """Save selected symbols to crypto_assets.csv."""
    if not symbols:
        print("⚠️ No symbols to save.")
        return
    
    # Create DataFrame
    df_data = []
    for symbol_data in symbols:
        df_data.append({
            'symbol': symbol_data['symbol'],
            'base': symbol_data['base'],
            'quote': symbol_data['quote'],
            'exchange': exchange_id,
            'id': symbol_data['id']
        })
    
    df = pd.DataFrame(df_data)
    
    # Ensure input directory exists
    os.makedirs("input", exist_ok=True)
    
    # Save to CSV
    filename = "input/crypto_assets.csv"
    df.to_csv(filename, index=False)
    
    print(f"\n✅ Saved {len(symbols)} symbols to {filename}")
    
    # Display summary
    quote_summary = df['quote'].value_counts()
    print(f"\n📊 **SAVED SYMBOLS SUMMARY**")
    for quote, count in quote_summary.items():
        print(f"   {quote}: {count} pairs")
    
    # Show first few symbols as confirmation
    print(f"\n📋 **SAMPLE SYMBOLS** (first 10)")
    sample_symbols = df[['symbol', 'base', 'quote']].head(10)
    print(tabulate(sample_symbols.values, headers=['Symbol', 'Base', 'Quote'], tablefmt='grid'))


def update_config_file(exchange_id):
    """Update the config file with the selected exchange."""
    config_file = "config/config_crypto.yaml"
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                content = f.read()
            
            # Update exchange
            if 'exchange:' in content:
                import re
                content = re.sub(r'exchange:\s*"[^"]*"', f'exchange: "{exchange_id}"', content)
            else:
                content += f'\nexchange: "{exchange_id}"\n'
            
            with open(config_file, 'w') as f:
                f.write(content)
            
            print(f"✅ Updated {config_file} with exchange: {exchange_id}")
        
        except Exception as e:
            print(f"⚠️ Could not update config file: {e}")


def main():
    """Main function for crypto symbol management."""
    print("🚀 Advanced Crypto Symbol Management")
    print("=" * 60)
    
    # Step 1: Select exchange
    exchanges = get_available_exchanges()
    
    if not exchanges:
        print("❌ No exchanges available!")
        return
    
    print(f"\n🏢 **AVAILABLE EXCHANGES** ({len(exchanges)} exchanges)")
    exchange_data = []
    for i, exchange in enumerate(exchanges, 1):
        countries = ', '.join(exchange['countries'][:2])  # Show first 2 countries
        exchange_data.append([i, exchange['name'], exchange['id'], countries])
    
    print(tabulate(exchange_data, headers=['#', 'Name', 'ID', 'Countries'], tablefmt='grid'))
    
    # Get exchange selection
    while True:
        try:
            choice = int(input(f"\nSelect exchange (1-{len(exchanges)}): "))
            if 1 <= choice <= len(exchanges):
                selected_exchange = exchanges[choice - 1]
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(exchanges)}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return
    
    print(f"\n✅ Selected: {selected_exchange['name']} ({selected_exchange['id']})")
    
    # Step 2: Fetch symbols
    symbol_groups = fetch_symbols_from_exchange(selected_exchange['id'])
    
    if not symbol_groups:
        print("❌ Could not fetch symbols from this exchange.")
        return
    
    # Step 3: Display and select symbols
    symbol_index = display_symbol_groups(symbol_groups)
    selected_symbols = get_user_selection(symbol_index)
    
    if not selected_symbols:
        print("⚠️ No symbols selected. Exiting.")
        return
    
    # Step 4: Save symbols
    save_selected_symbols(selected_symbols, selected_exchange['id'])
    
    # Step 5: Update config
    update_config_file(selected_exchange['id'])
    
    print(f"\n🎉 **CRYPTO SYMBOL MANAGEMENT COMPLETE!**")
    print(f"📁 Symbols saved to: input/crypto_assets.csv")
    print(f"⚙️  Config updated: config/config_crypto.yaml")
    print(f"🚀 Ready to run: python scripts/crypto_backtest.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
