#!/usr/bin/env python3
"""
Delta Exchange Symbol Fetcher
🎯 Fetch and organize all Delta Exchange trading pairs into CSV files
📊 Creates organized input files for backtesting system
💾 Saves pairs by category: spot, futures, options, perpetuals
"""

import os
import sys
import time
import argparse
from datetime import datetime

# Add crypto module to path for data acquisition
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import CCXT for Delta Exchange
try:
    import ccxt
    CCXT_AVAILABLE = True
    print("✅ CCXT library available for Delta Exchange integration")
except ImportError as e:
    CCXT_AVAILABLE = False
    print(f"❌ CCXT library not available: {e}")
    print("💡 Install with: pip install ccxt")
    sys.exit(1)

print("🎯 DELTA EXCHANGE SYMBOL FETCHER")
print("="*60)
print("📊 Fetch All Trading Pairs | Organize by Category")
print("💾 Create CSV Input Files for Backtesting")
print("="*60)

class DeltaExchangeSymbolFetcher:
    """Delta Exchange symbol fetching and organization."""
    
    def __init__(self):
        self.exchange = None
        self.available_pairs = []
        self.initialized = False
        
    def initialize(self):
        """Initialize Delta Exchange connection using CCXT."""
        try:
            print("🔗 Connecting to Delta Exchange via CCXT...")
            
            # Initialize Delta Exchange with comprehensive rate limiting
            self.exchange = ccxt.delta({
                'sandbox': False,  # Set to True for testing
                'enableRateLimit': True,  # Enable automatic rate limiting
                'rateLimit': 1200,  # Minimum delay between requests in milliseconds
                'timeout': 30000,  # 30 seconds timeout
                'headers': {
                    'User-Agent': 'AlgoProject/1.0 CCXT'
                },
                'options': {
                    'adjustForTimeDifference': True,  # Adjust for server time difference
                    'recvWindow': 60000,  # Receive window for requests
                }
            })
            
            print("📊 Loading Delta Exchange markets...")
            
            # Load markets with rate limiting
            markets = self.exchange.load_markets()
            
            # Extract trading pairs
            self.available_pairs = list(markets.keys())
            
            # Filter for active pairs only
            active_pairs = [pair for pair in self.available_pairs if markets[pair]['active']]
            
            self.initialized = True
            
            print(f"✅ Delta Exchange connected successfully with rate limiting!")
            print(f"📊 Found {len(self.available_pairs)} total pairs")
            print(f"🔥 Found {len(active_pairs)} active pairs")
            print(f"⏱️  Rate limit: {self.exchange.rateLimit}ms between requests")
            
            # Store market info for later use
            self.markets = markets
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to Delta Exchange: {e}")
            print("💡 Check internet connection and CCXT installation")
            return False
    
    def get_symbol_info(self, symbol):
        """Get detailed symbol information."""
        try:
            if self.exchange and self.initialized and symbol in self.markets:
                market = self.markets[symbol]
                return {
                    'symbol': symbol,
                    'base': market['base'],
                    'quote': market['quote'],
                    'active': market['active'],
                    'type': market['type'],
                    'spot': market.get('spot', True),
                    'future': market.get('future', False),
                    'option': market.get('option', False),
                    'swap': market.get('swap', False),
                    'precision': market.get('precision', {}),
                    'limits': market.get('limits', {})
                }
            return None
        except Exception as e:
            print(f"⚠️  Error getting symbol info for {symbol}: {e}")
            return None
    
    def categorize_pairs(self):
        """Categorize all trading pairs by type and quote currency."""
        if not self.initialized:
            print("❌ Delta Exchange not initialized")
            return {}
        
        print(f"📊 Categorizing {len(self.available_pairs)} pairs...")
        
        categories = {
            'spot_usdt': [],
            'spot_btc': [],
            'spot_eth': [],
            'futures_usdt': [],
            'futures_btc': [],
            'options_calls': [],
            'options_puts': [],
            'perpetual_usdt': [],
            'perpetual_btc': [],
            'other_pairs': []
        }
        
        for pair in self.available_pairs:
            # Get market info for accurate categorization
            market_info = self.markets.get(pair, {})
            
            # Skip inactive pairs
            if not market_info.get('active', False):
                continue
            
            # Categorize by market type and quote currency
            if '-PERP' in pair or market_info.get('swap', False):
                if 'USDT' in pair:
                    categories['perpetual_usdt'].append(pair)
                elif 'BTC' in pair:
                    categories['perpetual_btc'].append(pair)
                else:
                    categories['other_pairs'].append(pair)
            elif market_info.get('future', False) or '-FUT' in pair or 'FUTURES' in pair:
                if 'USDT' in pair:
                    categories['futures_usdt'].append(pair)
                elif 'BTC' in pair:
                    categories['futures_btc'].append(pair)
                else:
                    categories['other_pairs'].append(pair)
            elif market_info.get('option', False) or '-C-' in pair or '-P-' in pair:
                if '-C-' in pair or 'CALL' in pair:
                    categories['options_calls'].append(pair)
                elif '-P-' in pair or 'PUT' in pair:
                    categories['options_puts'].append(pair)
                else:
                    categories['other_pairs'].append(pair)
            elif market_info.get('spot', True):
                if 'USDT' in pair:
                    categories['spot_usdt'].append(pair)
                elif 'BTC' in pair and 'USDT' not in pair:
                    categories['spot_btc'].append(pair)
                elif 'ETH' in pair and 'USDT' not in pair and 'BTC' not in pair:
                    categories['spot_eth'].append(pair)
                else:
                    categories['other_pairs'].append(pair)
            else:
                categories['other_pairs'].append(pair)
        
        # Print categorization summary
        print(f"\n📋 CATEGORIZATION SUMMARY:")
        for category, pairs in categories.items():
            if pairs:
                print(f"   {category.replace('_', ' ').title():<20}: {len(pairs):>3} pairs")
        
        return categories
    
    def save_pairs_to_csv(self, output_dir=None):
        """Save categorized pairs to organized CSV files."""
        if not self.initialized:
            print("❌ Cannot save pairs - Delta Exchange not connected")
            return False
        
        # Set output directory
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'input')
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"💾 Saving pairs to CSV files in: {output_dir}")
        
        # Categorize pairs
        categories = self.categorize_pairs()
        
        if not any(categories.values()):
            print("❌ No pairs to save")
            return False
        
        saved_files = []
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save each category to separate CSV files
        for category, pair_list in categories.items():
            if not pair_list:
                continue
                
            filename = f"delta_{category}.csv"
            filepath = os.path.join(output_dir, filename)
            
            print(f"📄 Creating {filename} with {len(pair_list)} pairs...")
            
            # Create CSV content with comprehensive metadata
            csv_content = [
                'Symbol,Base,Quote,Market_Type,Active,Spot,Future,Option,Swap,Description,Generated'
            ]
            
            for pair in sorted(pair_list):
                # Get detailed symbol info
                symbol_info = self.get_symbol_info(pair)
                
                if symbol_info:
                    base = symbol_info.get('base', 'UNKNOWN')
                    quote = symbol_info.get('quote', 'UNKNOWN')
                    market_type = 'SPOT'
                    
                    # Determine market type
                    if symbol_info.get('swap', False) or '-PERP' in pair:
                        market_type = 'PERPETUAL'
                    elif symbol_info.get('future', False) or '-FUT' in pair:
                        market_type = 'FUTURES'
                    elif symbol_info.get('option', False) or '-C-' in pair or '-P-' in pair:
                        market_type = 'OPTION'
                    
                    active = 'YES' if symbol_info.get('active', True) else 'NO'
                    spot = 'YES' if symbol_info.get('spot', True) else 'NO'
                    future = 'YES' if symbol_info.get('future', False) else 'NO'
                    option = 'YES' if symbol_info.get('option', False) else 'NO'
                    swap = 'YES' if symbol_info.get('swap', False) else 'NO'
                    
                    description = f"{base}/{quote} {market_type}"
                else:
                    # Fallback info parsing
                    parts = pair.split('/')
                    base = parts[0] if len(parts) > 0 else 'UNKNOWN'
                    quote = parts[1] if len(parts) > 1 else 'UNKNOWN'
                    
                    market_type = 'SPOT'
                    if '-PERP' in pair:
                        market_type = 'PERPETUAL'
                    elif '-FUT' in pair or 'FUTURES' in pair:
                        market_type = 'FUTURES'
                    elif '-C-' in pair or '-P-' in pair:
                        market_type = 'OPTION'
                    
                    active = 'YES'
                    spot = 'YES' if market_type == 'SPOT' else 'NO'
                    future = 'YES' if market_type == 'FUTURES' else 'NO'
                    option = 'YES' if market_type == 'OPTION' else 'NO'
                    swap = 'YES' if market_type == 'PERPETUAL' else 'NO'
                    
                    description = f"{base}/{quote} {market_type}"
                
                # Add to CSV
                csv_line = f"{pair},{base},{quote},{market_type},{active},{spot},{future},{option},{swap},{description},{timestamp}"
                csv_content.append(csv_line)
            
            # Write to file
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(csv_content))
                
                saved_files.append((filename, len(pair_list)))
                print(f"✅ Saved {len(pair_list)} pairs to {filename}")
                
            except Exception as e:
                print(f"❌ Error saving {filename}: {e}")
        
        # Create master summary file
        if saved_files:
            summary_file = os.path.join(output_dir, "delta_pairs_summary.csv")
            summary_content = [
                'Category,Filename,Pair_Count,Description,Generated'
            ]
            
            for filename, count in saved_files:
                category = filename.replace('delta_', '').replace('.csv', '')
                description = f"Delta Exchange {category.replace('_', ' ').title()} Trading Pairs"
                summary_content.append(f"{category},{filename},{count},{description},{timestamp}")
            
            # Add totals row
            total_pairs = sum([count for _, count in saved_files])
            summary_content.append(f"TOTAL,ALL_FILES,{total_pairs},All Delta Exchange Trading Pairs,{timestamp}")
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(summary_content))
            
            print(f"\n💾 EXPORT COMPLETED SUCCESSFULLY!")
            print("="*60)
            
            print(f"📁 Output Directory: {output_dir}")
            print(f"📋 Files Created:")
            for filename, count in saved_files:
                print(f"   📄 {filename:<25} - {count:>3} pairs")
            
            print(f"\n📊 Summary:")
            print(f"   📋 Summary file: delta_pairs_summary.csv")
            print(f"   🎯 Total pairs exported: {total_pairs}")
            print(f"   📅 Generated: {timestamp}")
            
            return True
        else:
            print("❌ No files were saved")
            return False
    
    def display_pair_counts(self):
        """Display pair counts by category."""
        if not self.initialized:
            print("❌ Delta Exchange not initialized")
            return
        
        categories = self.categorize_pairs()
        
        print(f"\n📊 DELTA EXCHANGE PAIR COUNTS")
        print("="*50)
        
        total_pairs = 0
        for category, pairs in categories.items():
            if pairs:
                count = len(pairs)
                total_pairs += count
                category_name = category.replace('_', ' ').title()
                print(f"{category_name:<20}: {count:>3} pairs")
        
        print("-" * 50)
        print(f"{'Total Active Pairs':<20}: {total_pairs:>3}")
        
        # Show top pairs from each major category
        major_categories = ['spot_usdt', 'perpetual_usdt', 'futures_usdt', 'options_calls']
        
        for category in major_categories:
            if category in categories and categories[category]:
                pairs = categories[category][:5]  # Top 5
                category_name = category.replace('_', ' ').title()
                print(f"\n🔥 Top {category_name} Pairs:")
                for i, pair in enumerate(pairs, 1):
                    print(f"   {i}. {pair}")
                if len(categories[category]) > 5:
                    print(f"   ... and {len(categories[category]) - 5} more")

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Delta Exchange Symbol Fetcher - Create organized CSV input files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python delta_fetch_symbols.py                    # Fetch and save all pairs
  python delta_fetch_symbols.py --display          # Show pair counts only
  python delta_fetch_symbols.py --output custom/   # Save to custom directory
  python delta_fetch_symbols.py --test             # Test connection only
        """
    )
    
    parser.add_argument('--output', '-o', type=str, 
                       help='Output directory for CSV files (default: ../input)')
    parser.add_argument('--display', '-d', action='store_true',
                       help='Display pair counts without saving files')
    parser.add_argument('--test', '-t', action='store_true',
                       help='Test Delta Exchange connection only')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output with detailed progress')
    
    args = parser.parse_args()
    
    # Initialize fetcher
    fetcher = DeltaExchangeSymbolFetcher()
    
    # Test connection
    print("🔄 Testing Delta Exchange connection...")
    if not fetcher.initialize():
        print("❌ Failed to connect to Delta Exchange")
        print("\n💡 TROUBLESHOOTING:")
        print("   • Check internet connection")
        print("   • Verify CCXT installation: pip install ccxt")
        print("   • Try again in a few minutes (rate limiting)")
        return False
    
    if args.test:
        print("✅ Connection test successful!")
        return True
    
    if args.display:
        fetcher.display_pair_counts()
        return True
    
    # Save pairs to CSV files
    success = fetcher.save_pairs_to_csv(args.output)
    
    if success:
        print("\n🎉 SUCCESS! Delta Exchange pairs saved to CSV files")
        print("\n💡 NEXT STEPS:")
        print("   • Use files in backtesting: --load-csv spot_usdt")
        print("   • Check summary file: delta_pairs_summary.csv")
        print("   • Run backtests with: python delta_backtest_strategies.py")
        
        # Show usage examples
        input_dir = args.output or os.path.join(os.path.dirname(__file__), '..', 'input')
        print(f"\n📋 USAGE EXAMPLES:")
        print(f"   python delta_backtest_strategies.py --load-csv spot_usdt")
        print(f"   python delta_backtest_strategies.py --load-csv perpetual_usdt")
        print(f"   python delta_backtest_strategies.py --interactive")
        
        return True
    else:
        print("❌ Failed to save pairs")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Please report this issue if it persists")
        sys.exit(1)
