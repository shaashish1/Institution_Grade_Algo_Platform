#!/usr/bin/env python3
"""
Advanced Crypto Symbol Management
Fetch and manage crypto trading pairs from any CCXT exchange with user selection.
"""

import os
import sys
import pandas as pd
from tabulate import tabulate

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def get_available_exchanges():
    """Get list of available CCXT exchanges."""
    exchanges = []
    
    # Popular crypto exchanges
    popular_exchanges = [
        'kraken', 'binance', 'coinbase', 'bybit', 'okx', 
        'kucoin', 'huobi', 'bitfinex', 'gemini', 'ftx'
    ]
    
    print("🔍 Checking available exchanges...")
    
    ccxt_lib = _ensure_ccxt()
    
    for exchange_id in popular_exchanges:
        try:
            exchange_class = getattr(ccxt_lib, exchange_id, None)
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
        ccxt_lib = _ensure_ccxt()
        exchange_class = getattr(ccxt_lib, exchange_id.lower())
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


def get_symbol_priority(symbol_data):
    """Get priority score for a symbol based on popularity and trading volume."""
    base = symbol_data['base']
    quote = symbol_data['quote']
    
    # Priority scoring system
    priority_score = 0
    
    # Quote currency priority (higher is better)
    quote_priority = {
        'USDT': 100,  # Most popular
        'USD': 95,
        'BUSD': 90,
        'USDC': 85,
        'BTC': 80,
        'ETH': 75,
        'EUR': 70,
        'GBP': 65,
        'JPY': 60,
        'BNB': 55,
    }
    priority_score += quote_priority.get(quote, 30)
    
    # Base currency priority (top cryptocurrencies)
    base_priority = {
        # Top 10 by market cap
        'BTC': 100, 'ETH': 95, 'BNB': 90, 'XRP': 85, 'ADA': 80,
        'DOGE': 75, 'SOL': 70, 'DOT': 65, 'AVAX': 60, 'SHIB': 55,
        
        # Top 20 by market cap
        'MATIC': 50, 'LTC': 48, 'UNI': 46, 'LINK': 44, 'ATOM': 42,
        'XLM': 40, 'ALGO': 38, 'VET': 36, 'FIL': 34, 'TRX': 32,
        
        # Popular DeFi tokens
        'AAVE': 30, 'COMP': 28, 'YFI': 26, 'SUSHI': 24, 'CRV': 22,
        
        # Popular meme coins
        'PEPE': 20, 'FLOKI': 18, 'BABYDOGE': 16,
        
        # Promising altcoins
        'NEAR': 25, 'LUNA': 23, 'FTM': 21, 'ONE': 19, 'HBAR': 17,
        'CAKE': 15, 'SAND': 13, 'MANA': 11, 'ENJ': 9, 'CHZ': 7,
    }
    priority_score += base_priority.get(base, 5)
    
    # Bonus for popular pairs
    popular_pairs = [
        'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT',
        'DOGE/USDT', 'SOL/USDT', 'DOT/USDT', 'AVAX/USDT', 'SHIB/USDT',
        'MATIC/USDT', 'LTC/USDT', 'UNI/USDT', 'LINK/USDT', 'ATOM/USDT',
        'BTC/USD', 'ETH/USD', 'BTC/EUR', 'ETH/EUR'
    ]
    if symbol_data['symbol'] in popular_pairs:
        priority_score += 20
    
    return priority_score


def sort_symbols_by_priority(symbol_groups):
    """Sort symbols by priority within each group."""
    sorted_groups = {}
    
    for quote, symbols in symbol_groups.items():
        # Calculate priority for each symbol
        symbols_with_priority = []
        for symbol_data in symbols:
            priority = get_symbol_priority(symbol_data)
            symbols_with_priority.append((symbol_data, priority))
        
        # Sort by priority (highest first)
        symbols_with_priority.sort(key=lambda x: x[1], reverse=True)
        
        # Extract sorted symbols
        sorted_groups[quote] = [symbol_data for symbol_data, _ in symbols_with_priority]
    
    return sorted_groups


def get_priority_groups(symbol_groups):
    """Get symbols grouped by priority categories."""
    all_symbols = []
    for quote, symbols in symbol_groups.items():
        all_symbols.extend(symbols)
    
    # Calculate priorities and group
    priority_groups = {
        'top_tier': [],      # Priority >= 150
        'popular': [],       # Priority >= 100
        'standard': [],      # Priority >= 50
        'emerging': []       # Priority < 50
    }
    
    for symbol_data in all_symbols:
        priority = get_symbol_priority(symbol_data)
        
        if priority >= 150:
            priority_groups['top_tier'].append(symbol_data)
        elif priority >= 100:
            priority_groups['popular'].append(symbol_data)
        elif priority >= 50:
            priority_groups['standard'].append(symbol_data)
        else:
            priority_groups['emerging'].append(symbol_data)
    
    # Sort within each group
    for group in priority_groups.values():
        group.sort(key=lambda x: get_symbol_priority(x), reverse=True)
    
    return priority_groups


def display_priority_groups(priority_groups):
    """Display symbols grouped by priority with enhanced formatting."""
    print("\n📊 **TRADING PAIRS BY PRIORITY**")
    print("=" * 80)
    
    symbol_index = {}
    current_number = 1
    
    # Define group descriptions
    group_info = {
        'top_tier': ('🏆 **TOP TIER** (Most Popular)', 'grid'),
        'popular': ('⭐ **POPULAR** (High Volume)', 'grid'),
        'standard': ('📈 **STANDARD** (Good Liquidity)', 'simple'),
        'emerging': ('🚀 **EMERGING** (Growth Potential)', 'simple')
    }
    
    for group_name, symbols in priority_groups.items():
        if not symbols:
            continue
            
        group_title, table_format = group_info[group_name]
        print(f"\n{group_title} ({len(symbols)} pairs)")
        print("-" * 60)
        
        display_data = []
        for symbol_data in symbols:
            symbol_index[current_number] = symbol_data
            priority = get_symbol_priority(symbol_data)
            display_data.append([
                current_number,
                symbol_data['symbol'],
                symbol_data['base'],
                symbol_data['quote'],
                f"{priority}"
            ])
            current_number += 1
        
        # Display in chunks for readability
        chunk_size = 15 if group_name in ['top_tier', 'popular'] else 20
        for i in range(0, len(display_data), chunk_size):
            chunk = display_data[i:i+chunk_size]
            headers = ['#', 'Symbol', 'Base', 'Quote', 'Priority']
            print(tabulate(chunk, headers=headers, tablefmt=table_format))
            
            if i + chunk_size < len(display_data):
                print(f"\n... {len(display_data) - i - chunk_size} more pairs in this group")
                if input("Press Enter to see more or 'q' to skip: ").lower() == 'q':
                    break
    
    return symbol_index


def display_symbol_groups_traditional(symbol_groups):
    """Display symbols grouped by quote currency with numbering (traditional view)."""
    print("\n📊 **AVAILABLE TRADING PAIRS** (Traditional View)")
    print("=" * 80)
    
    symbol_index = {}
    current_number = 1
    
    # Sort quote currencies by preference
    quote_order = ['USDT', 'USD', 'BUSD', 'USDC', 'BTC', 'ETH', 'EUR', 'BNB']
    sorted_quotes = sorted(symbol_groups.keys(), 
                          key=lambda x: quote_order.index(x) if x in quote_order else 999)
    
    for quote in sorted_quotes:
        symbols = symbol_groups[quote]
        print(f"\n🪙 **{quote} Pairs** ({len(symbols)} pairs)")
        print("-" * 50)
        
        display_data = []
        for symbol_data in symbols:
            symbol_index[current_number] = symbol_data
            priority = get_symbol_priority(symbol_data)
            display_data.append([
                current_number,
                symbol_data['symbol'],
                symbol_data['base'],
                f"{priority}"
            ])
            current_number += 1
        
        # Display in chunks of 20 for readability
        chunk_size = 20
        for i in range(0, len(display_data), chunk_size):
            chunk = display_data[i:i+chunk_size]
            print(tabulate(chunk, headers=['#', 'Symbol', 'Base', 'Priority'], tablefmt='grid'))
            if i + chunk_size < len(display_data):
                if input("\nPress Enter to see more symbols or 'q' to skip: ").lower() == 'q':
                    break
    
    return symbol_index


def get_user_selection(symbol_index, priority_groups=None):
    """Get user selection of symbols with enhanced options."""
    print(f"\n🎯 **SYMBOL SELECTION**")
    print("=" * 50)
    print("Choose symbols by entering numbers (e.g., 1,5,10-15,20)")
    print("Or use quick selection options:")
    print("  • 'all' - Select all symbols")
    print("  • 'usdt' - Select all USDT pairs")
    print("  • 'usd' - Select all USD pairs")
    print("  • 'top10' - Select top 10 by priority")
    print("  • 'top20' - Select top 20 by priority")
    print("  • 'top50' - Select top 50 by priority")
    print("  • 'toptier' - Select only top tier symbols")
    print("  • 'popular' - Select popular symbols")
    print("  • 'majors' - Select major cryptocurrencies (BTC, ETH, BNB, XRP, ADA)")
    print("  • 'defi' - Select DeFi tokens")
    print("  • 'meme' - Select meme coins")
    
    while True:
        try:
            user_input = input("\nEnter your selection: ").strip().lower()
            
            if user_input == 'all':
                return list(symbol_index.values())
            
            elif user_input == 'usdt':
                return [s for s in symbol_index.values() if s['quote'] == 'USDT']
            
            elif user_input == 'usd':
                return [s for s in symbol_index.values() if s['quote'] == 'USD']
            
            elif user_input in ['top10', 'top20', 'top50']:
                # Get top N symbols by priority
                all_symbols = list(symbol_index.values())
                all_symbols.sort(key=lambda x: get_symbol_priority(x), reverse=True)
                
                if user_input == 'top10':
                    return all_symbols[:10]
                elif user_input == 'top20':
                    return all_symbols[:20]
                elif user_input == 'top50':
                    return all_symbols[:50]
            
            elif user_input == 'toptier' and priority_groups:
                return priority_groups.get('top_tier', [])
            
            elif user_input == 'popular' and priority_groups:
                return priority_groups.get('popular', [])
            
            elif user_input == 'majors':
                major_coins = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'DOT', 'AVAX', 'MATIC']
                return [s for s in symbol_index.values() 
                       if s['base'] in major_coins and s['quote'] in ['USDT', 'USD']]
            
            elif user_input == 'defi':
                defi_coins = ['UNI', 'AAVE', 'COMP', 'YFI', 'SUSHI', 'CRV', 'CAKE', 'LINK']
                return [s for s in symbol_index.values() 
                       if s['base'] in defi_coins and s['quote'] in ['USDT', 'USD']]
            
            elif user_input == 'meme':
                meme_coins = ['DOGE', 'SHIB', 'PEPE', 'FLOKI', 'BABYDOGE']
                return [s for s in symbol_index.values() 
                       if s['base'] in meme_coins and s['quote'] in ['USDT', 'USD']]
            
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
    
    # Create DataFrame for detailed information (optional extended file)
    df_detailed = pd.DataFrame([{
        'symbol': symbol_data['symbol'],
        'base': symbol_data['base'],
        'quote': symbol_data['quote'],
        'exchange': exchange_id,
        'id': symbol_data['id'],
        'priority': get_symbol_priority(symbol_data)
    } for symbol_data in symbols])
    
    # Sort by priority (highest first)
    df_detailed = df_detailed.sort_values('priority', ascending=False)
    
    # Create simple DataFrame for backtest compatibility (only symbol column)
    df_simple = pd.DataFrame({
        'symbol': df_detailed['symbol'].tolist()
    })
    
    # Ensure input directory exists
    os.makedirs("crypto/input", exist_ok=True)
    
    # Save simple format for backtest compatibility
    filename = "crypto/input/crypto_assets.csv"
    df_simple.to_csv(filename, index=False)
    
    # Save detailed format for reference
    detailed_filename = "crypto/input/crypto_assets_detailed.csv"
    df_detailed.to_csv(detailed_filename, index=False)
    
    print(f"\n✅ Saved {len(symbols)} symbols to {filename}")
    print(f"📋 Detailed info saved to {detailed_filename}")
    
    # Display enhanced summary
    quote_summary = df_detailed['quote'].value_counts()
    print(f"\n📊 **SAVED SYMBOLS SUMMARY**")
    for quote, count in quote_summary.items():
        print(f"   {quote}: {count} pairs")
    
    # Priority distribution
    priority_stats = {
        'Top Tier (150+)': len(df_detailed[df_detailed['priority'] >= 150]),
        'Popular (100-149)': len(df_detailed[(df_detailed['priority'] >= 100) & (df_detailed['priority'] < 150)]),
        'Standard (50-99)': len(df_detailed[(df_detailed['priority'] >= 50) & (df_detailed['priority'] < 100)]),
        'Emerging (<50)': len(df_detailed[df_detailed['priority'] < 50])
    }
    
    print(f"\n🏆 **PRIORITY DISTRIBUTION**")
    for category, count in priority_stats.items():
        if count > 0:
            print(f"   {category}: {count} pairs")
    
    # Show top symbols
    print(f"\n📋 **TOP SELECTED SYMBOLS** (by priority)")
    top_symbols = df_detailed[['symbol', 'base', 'quote', 'priority']].head(10)
    print(tabulate(top_symbols.values, headers=['Symbol', 'Base', 'Quote', 'Priority'], tablefmt='grid'))


def update_config_file(exchange_id):
    """Update the config file with the selected exchange."""
    config_file = "crypto/input/config_crypto.yaml"
    
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
    
    # Sort symbols by priority
    sorted_symbol_groups = sort_symbols_by_priority(symbol_groups)
    
    # Create priority groups
    priority_groups = get_priority_groups(sorted_symbol_groups)
    
    # Display symbols by priority
    print(f"\n📊 Found {sum(len(symbols) for symbols in symbol_groups.values())} trading pairs")
    
    # Ask user for display preference
    print("\n🎨 **DISPLAY OPTIONS**")
    print("1. Priority-based grouping (Recommended)")
    print("2. Quote currency grouping (Traditional)")
    
    display_choice = input("\nChoose display option (1 or 2, default=1): ").strip()
    
    if display_choice == '2':
        # Traditional display by quote currency
        symbol_index = display_symbol_groups_traditional(sorted_symbol_groups)
        selected_symbols = get_user_selection(symbol_index)
    else:
        # Priority-based display
        symbol_index = display_priority_groups(priority_groups)
        selected_symbols = get_user_selection(symbol_index, priority_groups)
    
    if not selected_symbols:
        print("⚠️ No symbols selected. Exiting.")
        return
    
    # Step 4: Save symbols
    save_selected_symbols(selected_symbols, selected_exchange['id'])
    
    # Step 5: Update config
    update_config_file(selected_exchange['id'])
    
    print(f"\n🎉 **CRYPTO SYMBOL MANAGEMENT COMPLETE!**")
    print(f"📁 Symbols saved to: crypto/input/crypto_assets.csv")
    print(f"⚙️  Config updated: crypto/input/config_crypto.yaml")
    print(f"🚀 Ready to run: python scripts/crypto_backtest.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
