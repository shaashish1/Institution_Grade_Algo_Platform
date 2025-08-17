#!/usr/bin/env python3
"""
CCXT Symbol Validator - AlgoProject
==================================

Test real CCXT exchanges (Kraken and Binance) to validate which symbols 
have actual data available. Filter for USDT pairs only.

This script will:
1. Connect to Kraken and Binance via CCXT
2. Fetch available markets/symbols
3. Filter for USDT pairs only
4. Test actual data availability for each symbol
5. Generate a validated list of working symbols
6. Update crypto_assets.csv with only working symbols

Author: AlgoProject Team
Date: July 15, 2025
"""

import os
import sys
import time
import logging
import pandas as pd
from datetime import datetime
import ccxt

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Setup logging
log_filename = f"ccxt_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logs_dir = os.path.join(project_root, 'helper_scripts', 'logs')
os.makedirs(logs_dir, exist_ok=True)
log_filepath = os.path.join(logs_dir, log_filename)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filepath, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("CCXTValidator")

class CCXTSymbolValidator:
    """CCXT Symbol Validator for crypto exchanges."""
    
    def __init__(self):
        """Initialize the validator."""
        self.exchanges = {}
        self.validated_symbols = []
        self.results = {}
        
        logger.info("=" * 80)
        logger.info("🔍 CCXT SYMBOL VALIDATOR INITIALIZED")
        logger.info("=" * 80)
        logger.info(f"📁 Project Root: {project_root}")
        logger.info(f"📝 Log File: {log_filepath}")
        logger.info("=" * 80)
    
    def initialize_exchanges(self):
        """Initialize CCXT exchanges."""
        logger.info("🔌 Initializing CCXT exchanges...")
        
        exchanges_config = {
            'kraken': {
                'class': ccxt.kraken,
                'params': {
                    'rateLimit': 1000,  # 1 second between requests
                    'enableRateLimit': True,
                    'sandbox': False
                }
            },
            'binance': {
                'class': ccxt.binance,
                'params': {
                    'rateLimit': 1200,  # 1.2 seconds between requests
                    'enableRateLimit': True,
                    'sandbox': False
                }
            }
        }
        
        for name, config in exchanges_config.items():
            try:
                logger.info(f"  🔄 Initializing {name}...")
                exchange = config['class'](config['params'])
                
                # Test connection
                markets = exchange.load_markets()
                logger.info(f"  ✅ {name}: Connected successfully ({len(markets)} markets)")
                self.exchanges[name] = exchange
                
            except Exception as e:
                logger.error(f"  ❌ {name}: Failed to initialize - {e}")
        
        logger.info(f"📊 Successfully initialized {len(self.exchanges)} exchanges")
        return len(self.exchanges) > 0
    
    def get_usdt_symbols(self, exchange_name):
        """Get USDT trading pairs from an exchange."""
        logger.info(f"💰 Getting USDT pairs from {exchange_name}...")
        
        if exchange_name not in self.exchanges:
            logger.error(f"❌ Exchange {exchange_name} not initialized")
            return []
        
        exchange = self.exchanges[exchange_name]
        usdt_symbols = []
        
        try:
            markets = exchange.markets
            
            for symbol, market in markets.items():
                # Filter for USDT pairs only
                if '/USDT' in symbol and market.get('active', True):
                    usdt_symbols.append(symbol)
            
            logger.info(f"  ✅ Found {len(usdt_symbols)} USDT pairs on {exchange_name}")
            
            # Show first 10 symbols as example
            if usdt_symbols:
                logger.info(f"  📋 Example symbols: {', '.join(usdt_symbols[:10])}")
                if len(usdt_symbols) > 10:
                    logger.info(f"  📋 ... and {len(usdt_symbols) - 10} more")
            
            return sorted(usdt_symbols)
            
        except Exception as e:
            logger.error(f"❌ Error getting USDT symbols from {exchange_name}: {e}")
            return []
    
    def test_symbol_data(self, exchange_name, symbol, max_retries=3):
        """Test if a symbol has actual data available."""
        if exchange_name not in self.exchanges:
            return False, "Exchange not available"
        
        exchange = self.exchanges[exchange_name]
        
        for attempt in range(max_retries):
            try:
                # Try to fetch recent OHLCV data
                ohlcv = exchange.fetch_ohlcv(symbol, '1h', limit=1)
                
                if ohlcv and len(ohlcv) > 0:
                    # Validate data structure
                    if len(ohlcv[0]) >= 5:  # [timestamp, open, high, low, close, volume]
                        latest_data = ohlcv[0]
                        close_price = latest_data[4]  # Close price
                        
                        if close_price and close_price > 0:
                            return True, f"${close_price:.6f}"
                        else:
                            return False, "Invalid price data"
                    else:
                        return False, "Invalid data structure"
                else:
                    return False, "No data returned"
                    
            except ccxt.NetworkError as e:
                logger.warning(f"  ⚠️ Network error for {symbol} (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait before retry
                continue
                
            except ccxt.BaseError as e:
                return False, f"CCXT error: {str(e)[:50]}"
                
            except Exception as e:
                return False, f"Error: {str(e)[:50]}"
        
        return False, "Max retries exceeded"
    
    def validate_exchange_symbols(self, exchange_name, limit=None):
        """Validate symbols for a specific exchange."""
        logger.info(f"🧪 Validating symbols for {exchange_name}...")
        
        # Get USDT symbols
        usdt_symbols = self.get_usdt_symbols(exchange_name)
        
        if not usdt_symbols:
            logger.error(f"❌ No USDT symbols found for {exchange_name}")
            return []
        
        # Limit for testing if specified
        if limit:
            usdt_symbols = usdt_symbols[:limit]
            logger.info(f"📊 Testing first {limit} symbols for {exchange_name}")
        
        validated = []
        failed = []
        
        logger.info(f"🚀 Testing {len(usdt_symbols)} symbols...")
        
        for i, symbol in enumerate(usdt_symbols, 1):
            logger.info(f"  🔄 [{i}/{len(usdt_symbols)}] Testing {symbol}...")
            
            success, message = self.test_symbol_data(exchange_name, symbol)
            
            if success:
                logger.info(f"    ✅ {symbol}: {message}")
                validated.append({
                    'symbol': symbol,
                    'exchange': exchange_name,
                    'status': 'SUCCESS',
                    'price': message,
                    'error': None
                })
            else:
                logger.warning(f"    ❌ {symbol}: {message}")
                failed.append({
                    'symbol': symbol,
                    'exchange': exchange_name,
                    'status': 'FAILED',
                    'price': None,
                    'error': message
                })
            
            # Rate limiting - small delay between requests
            time.sleep(0.5)
        
        logger.info(f"📊 {exchange_name} Results: ✅ {len(validated)} success, ❌ {len(failed)} failed")
        
        self.results[exchange_name] = {
            'validated': validated,
            'failed': failed,
            'success_rate': (len(validated) / len(usdt_symbols)) * 100 if usdt_symbols else 0
        }
        
        return validated
    
    def generate_report(self):
        """Generate comprehensive validation report."""
        logger.info("\n" + "=" * 80)
        logger.info("📋 CCXT SYMBOL VALIDATION REPORT")
        logger.info("=" * 80)
        
        all_validated = []
        total_tested = 0
        total_validated = 0
        
        for exchange_name, results in self.results.items():
            validated = results['validated']
            failed = results['failed']
            success_rate = results['success_rate']
            
            logger.info(f"\n🏢 {exchange_name.upper()} EXCHANGE:")
            logger.info(f"  📊 Total Tested: {len(validated) + len(failed)}")
            logger.info(f"  ✅ Validated: {len(validated)}")
            logger.info(f"  ❌ Failed: {len(failed)}")
            logger.info(f"  📈 Success Rate: {success_rate:.1f}%")
            
            # Show top 10 validated symbols
            if validated:
                logger.info(f"  🏆 Top Validated Symbols:")
                for symbol_data in validated[:10]:
                    logger.info(f"    💰 {symbol_data['symbol']}: {symbol_data['price']}")
                if len(validated) > 10:
                    logger.info(f"    📋 ... and {len(validated) - 10} more")
            
            all_validated.extend(validated)
            total_tested += len(validated) + len(failed)
            total_validated += len(validated)
        
        overall_success_rate = (total_validated / total_tested) * 100 if total_tested > 0 else 0
        
        logger.info(f"\n📊 OVERALL SUMMARY:")
        logger.info(f"  🎯 Total Symbols Tested: {total_tested}")
        logger.info(f"  ✅ Total Validated: {total_validated}")
        logger.info(f"  📈 Overall Success Rate: {overall_success_rate:.1f}%")
        logger.info(f"  🏢 Exchanges Tested: {len(self.results)}")
        
        return all_validated
    
    def save_validated_symbols(self, validated_symbols):
        """Save validated symbols to crypto_assets.csv."""
        if not validated_symbols:
            logger.warning("⚠️ No validated symbols to save")
            return False
        
        logger.info(f"💾 Saving {len(validated_symbols)} validated symbols...")
        
        # Create DataFrame
        df = pd.DataFrame(validated_symbols)
        
        # Add additional columns for crypto_assets.csv format
        df['base_currency'] = df['symbol'].apply(lambda x: x.split('/')[0])
        df['quote_currency'] = df['symbol'].apply(lambda x: x.split('/')[1])
        df['validated_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Reorder columns
        df = df[['symbol', 'base_currency', 'quote_currency', 'exchange', 'status', 'price', 'validated_date']]
        
        # Save to crypto assets file
        crypto_assets_path = os.path.join(project_root, 'crypto', 'input', 'crypto_assets.csv')
        
        try:
            # Backup existing file if it exists
            if os.path.exists(crypto_assets_path):
                backup_path = crypto_assets_path.replace('.csv', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
                os.rename(crypto_assets_path, backup_path)
                logger.info(f"📁 Backed up existing file to: {os.path.basename(backup_path)}")
            
            # Save new validated symbols
            df.to_csv(crypto_assets_path, index=False)
            logger.info(f"✅ Saved validated symbols to: crypto_assets.csv")
            
            # Also save detailed results
            results_path = os.path.join(project_root, 'helper_scripts', 'logs', f'validated_symbols_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
            df.to_csv(results_path, index=False)
            logger.info(f"✅ Detailed results saved to: {os.path.basename(results_path)}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving validated symbols: {e}")
            return False
    
    def run_validation(self, test_limit=None):
        """Run complete validation process."""
        logger.info("🚀 Starting CCXT Symbol Validation...")
        
        # Initialize exchanges
        if not self.initialize_exchanges():
            logger.error("❌ Failed to initialize any exchanges")
            return False
        
        # Validate symbols for each exchange
        all_validated = []
        
        for exchange_name in self.exchanges.keys():
            validated = self.validate_exchange_symbols(exchange_name, limit=test_limit)
            all_validated.extend(validated)
        
        # Generate report
        validated_symbols = self.generate_report()
        
        # Save results
        if validated_symbols:
            self.save_validated_symbols(validated_symbols)
        
        logger.info(f"\n📝 Detailed logs saved to: {log_filepath}")
        logger.info("=" * 80)
        
        return len(validated_symbols) > 0

def main():
    """Main function."""
    try:
        # Create validator
        validator = CCXTSymbolValidator()
        
        # Use default test limit for automated testing
        test_limit = 20  # Test first 20 symbols per exchange for better coverage
        
        logger.info(f"🔍 Running automated validation with {test_limit} symbols per exchange...")
        
        # Run validation
        success = validator.run_validation(test_limit=test_limit)
        
        if success:
            logger.info("🎉 Validation completed successfully!")
            return 0
        else:
            logger.error("❌ Validation failed")
            return 1
            
    except Exception as e:
        logger.error(f"💥 Critical error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
