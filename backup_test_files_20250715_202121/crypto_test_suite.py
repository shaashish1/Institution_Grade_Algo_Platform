#!/usr/bin/env python3
"""
Crypto Module Comprehensive Test Suite
Tests all .py files in crypto module and analyzes data availability
"""

import os
import sys
import time
import logging
import importlib.util
from datetime import datetime, timedelta
import pandas as pd

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crypto/logs/crypto_test_suite.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CryptoTestSuite:
    """Comprehensive test suite for crypto module."""
    
    def __init__(self):
        self.test_results = []
        self.data_analysis = {}
        self.start_time = datetime.now()
        
        # Ensure log directory exists
        os.makedirs('crypto/logs', exist_ok=True)
        
    def print_header(self):
        """Print professional test suite header."""
        print("🚀 CRYPTO MODULE COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        print(f"📅 Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Testing all Python files in crypto module")
        print(f"📊 Analyzing data availability for backtesting")
        print("=" * 80)
        
    def test_import_safety(self, file_path):
        """Test if a Python file can be imported safely."""
        try:
            # Get module name from file path
            module_name = os.path.basename(file_path).replace('.py', '')
            
            # Load module specification
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                return False, "Cannot create module spec"
                
            # Create module
            module = importlib.util.module_from_spec(spec)
            
            # Execute module (this tests imports)
            spec.loader.exec_module(module)
            
            return True, "Import successful"
            
        except ImportError as e:
            if 'fyers' in str(e).lower():
                return False, f"❌ CRITICAL: Fyers dependency found: {e}"
            return False, f"Import error: {e}"
        except Exception as e:
            return False, f"Execution error: {e}"
    
    def test_data_acquisition(self):
        """Test crypto data acquisition module."""
        print("\n📊 TESTING DATA ACQUISITION MODULE")
        print("-" * 50)
        
        try:
            from crypto.data_acquisition import fetch_data, health_check
            
            # Health check first
            health = health_check()
            logger.info(f"🏥 Health check status: {health['status']}")
            print(f"✅ Health check: {health['status']}")
            print(f"   CCXT Available: {health['ccxt_available']}")
            print(f"   Working Exchanges: {health['working_exchanges']}")
            
            return True, health
            
        except Exception as e:
            logger.error(f"❌ Data acquisition test failed: {e}")
            return False, str(e)
    
    def analyze_data_availability(self):
        """Analyze data availability for different timeframes."""
        print("\n📈 ANALYZING DATA AVAILABILITY")
        print("-" * 50)
        
        try:
            from crypto.data_acquisition import fetch_data
            
            test_symbol = 'BTC/USDT'
            test_exchange = 'kraken'
            timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
            
            for timeframe in timeframes:
                print(f"🔍 Testing {timeframe} timeframe...")
                start_time = time.time()
                
                # Test different bar counts
                for bars in [24, 100, 500, 1000]:
                    try:
                        data = fetch_data(
                            symbol=test_symbol,
                            exchange=test_exchange, 
                            interval=timeframe,
                            bars=bars
                        )
                        
                        if data is not None and len(data) > 0:
                            # Calculate date range
                            oldest_date = data.index.min()
                            newest_date = data.index.max()
                            actual_bars = len(data)
                            
                            # Calculate how recent the data is
                            now = datetime.now()
                            minutes_old = (now - newest_date.to_pydatetime().replace(tzinfo=None)).total_seconds() / 60
                            
                            self.data_analysis[f"{timeframe}_{bars}"] = {
                                'timeframe': timeframe,
                                'requested_bars': bars,
                                'actual_bars': actual_bars,
                                'oldest_date': oldest_date,
                                'newest_date': newest_date,
                                'minutes_old': minutes_old,
                                'date_range_days': (newest_date - oldest_date).days
                            }
                            
                            print(f"   📊 {bars} bars: {actual_bars} received, "
                                  f"range: {oldest_date.strftime('%Y-%m-%d %H:%M')} to "
                                  f"{newest_date.strftime('%Y-%m-%d %H:%M')} "
                                  f"({minutes_old:.1f} min old)")
                            
                            break  # Success, move to next timeframe
                            
                    except Exception as e:
                        logger.warning(f"⚠️  Failed to fetch {bars} bars for {timeframe}: {e}")
                        continue
                
                elapsed = time.time() - start_time
                print(f"   ⏱️  Test completed in {elapsed:.2f}s")
                
        except Exception as e:
            logger.error(f"❌ Data availability analysis failed: {e}")
            print(f"❌ Data availability analysis failed: {e}")
    
    def test_crypto_scripts(self):
        """Test all crypto script files."""
        print("\n🧪 TESTING CRYPTO SCRIPT FILES")
        print("-" * 50)
        
        script_dir = 'crypto/scripts'
        script_files = [f for f in os.listdir(script_dir) if f.endswith('.py')]
        
        # Filter out test files (following coding rules)
        production_files = [f for f in script_files if not any(x in f.lower() for x in ['test', 'demo', 'temp'])]
        
        for script_file in production_files:
            file_path = os.path.join(script_dir, script_file)
            print(f"🔍 Testing {script_file}...")
            
            success, message = self.test_import_safety(file_path)
            
            result = {
                'file': script_file,
                'path': file_path,
                'success': success,
                'message': message,
                'timestamp': datetime.now()
            }
            
            self.test_results.append(result)
            
            if success:
                print(f"   ✅ {message}")
                logger.info(f"✅ {script_file}: {message}")
            else:
                print(f"   ❌ {message}")
                logger.error(f"❌ {script_file}: {message}")
    
    def test_crypto_tools(self):
        """Test crypto tools and utilities."""
        print("\n🔧 TESTING CRYPTO TOOLS")
        print("-" * 50)
        
        tools_dir = 'crypto/tools'
        if os.path.exists(tools_dir):
            tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.py')]
            
            for tool_file in tool_files:
                file_path = os.path.join(tools_dir, tool_file)
                print(f"🔍 Testing {tool_file}...")
                
                success, message = self.test_import_safety(file_path)
                
                if success:
                    print(f"   ✅ {message}")
                    logger.info(f"✅ {tool_file}: {message}")
                else:
                    print(f"   ❌ {message}")
                    logger.error(f"❌ {tool_file}: {message}")
        else:
            print("⚠️  Tools directory not found")
    
    def test_crypto_utilities(self):
        """Test crypto utility files."""
        print("\n🛠️ TESTING CRYPTO UTILITIES")
        print("-" * 50)
        
        crypto_dir = 'crypto'
        util_files = [f for f in os.listdir(crypto_dir) 
                     if f.endswith('.py') and f not in ['__init__.py', 'data_acquisition.py']]
        
        for util_file in util_files:
            file_path = os.path.join(crypto_dir, util_file)
            print(f"🔍 Testing {util_file}...")
            
            success, message = self.test_import_safety(file_path)
            
            if success:
                print(f"   ✅ {message}")
                logger.info(f"✅ {util_file}: {message}")
            else:
                print(f"   ❌ {message}")
                logger.error(f"❌ {util_file}: {message}")
    
    def generate_data_report(self):
        """Generate detailed data availability report."""
        print("\n📋 DATA AVAILABILITY REPORT")
        print("=" * 80)
        
        if not self.data_analysis:
            print("❌ No data analysis available")
            return
        
        print("🕐 TIMEFRAME ANALYSIS:")
        print("-" * 50)
        
        timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
        
        for tf in timeframes:
            tf_data = [v for k, v in self.data_analysis.items() if k.startswith(tf + '_')]
            if tf_data:
                data = tf_data[0]  # Take first successful result
                
                print(f"📊 {tf.upper()} Timeframe:")
                print(f"   📈 Bars Available: {data['actual_bars']}")
                print(f"   📅 Date Range: {data['date_range_days']} days")
                print(f"   🕐 Latest Data: {data['minutes_old']:.1f} minutes old")
                print(f"   📆 From: {data['oldest_date'].strftime('%Y-%m-%d %H:%M UTC')}")
                print(f"   📆 To: {data['newest_date'].strftime('%Y-%m-%d %H:%M UTC')}")
                
                # Calculate coverage
                if tf == '1m':
                    expected_per_day = 1440  # 24*60
                elif tf == '5m':
                    expected_per_day = 288   # 24*12
                elif tf == '15m':
                    expected_per_day = 96    # 24*4
                elif tf == '30m':
                    expected_per_day = 48    # 24*2
                elif tf == '1h':
                    expected_per_day = 24    # 24
                elif tf == '4h':
                    expected_per_day = 6     # 24/4
                else:  # 1d
                    expected_per_day = 1
                
                expected_total = expected_per_day * data['date_range_days']
                coverage = (data['actual_bars'] / expected_total) * 100 if expected_total > 0 else 0
                
                print(f"   📊 Data Coverage: {coverage:.1f}%")
                print()
        
        # Data freshness analysis
        print("🕐 DATA FRESHNESS ANALYSIS:")
        print("-" * 50)
        
        latest_data = min([v['minutes_old'] for v in self.data_analysis.values() if 'minutes_old' in v])
        
        if latest_data < 5:
            print("✅ EXCELLENT: Data is very fresh (< 5 minutes old)")
        elif latest_data < 15:
            print("✅ GOOD: Data is reasonably fresh (< 15 minutes old)")
        elif latest_data < 60:
            print("⚠️  FAIR: Data is somewhat old (< 1 hour old)")
        else:
            print("❌ POOR: Data is quite old (> 1 hour old)")
        
        print(f"🕐 Latest data is {latest_data:.1f} minutes old")
        
        # Backtesting recommendations
        print("\n💡 BACKTESTING RECOMMENDATIONS:")
        print("-" * 50)
        print("📊 For reliable backtesting:")
        print("   • 1m/5m: Good for short-term strategies (< 30 days)")
        print("   • 15m/30m: Good for medium-term strategies (< 90 days)")
        print("   • 1h/4h: Good for long-term strategies (< 1 year)")
        print("   • 1d: Good for very long-term strategies (> 1 year)")
        print("\n⚡ For quick testing: Use 1h with 100-500 bars")
        print("📈 For comprehensive testing: Use 1h with 1000+ bars")
    
    def generate_summary(self):
        """Generate test summary."""
        elapsed = datetime.now() - self.start_time
        
        print("\n🎯 TEST SUITE SUMMARY")
        print("=" * 80)
        
        total_files = len(self.test_results)
        successful_files = len([r for r in self.test_results if r['success']])
        failed_files = total_files - successful_files
        
        print(f"📊 Total Files Tested: {total_files}")
        print(f"✅ Successful: {successful_files}")
        print(f"❌ Failed: {failed_files}")
        print(f"📈 Success Rate: {(successful_files/total_files)*100:.1f}%" if total_files > 0 else "N/A")
        print(f"⏱️  Total Time: {elapsed.total_seconds():.2f} seconds")
        
        if failed_files > 0:
            print(f"\n❌ FAILED FILES:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['file']}: {result['message']}")
        
        # Save detailed log
        log_file = f"crypto/logs/test_suite_results_{self.start_time.strftime('%Y%m%d_%H%M%S')}.log"
        with open(log_file, 'w') as f:
            f.write(f"Crypto Module Test Suite Results\n")
            f.write(f"Generated: {datetime.now()}\n\n")
            
            for result in self.test_results:
                f.write(f"File: {result['file']}\n")
                f.write(f"Success: {result['success']}\n")
                f.write(f"Message: {result['message']}\n")
                f.write(f"Timestamp: {result['timestamp']}\n\n")
        
        print(f"\n💾 Detailed results saved to: {log_file}")
    
    def run_all_tests(self):
        """Run complete test suite."""
        self.print_header()
        
        # Test core data acquisition
        data_success, data_info = self.test_data_acquisition()
        
        if data_success:
            # Analyze data availability
            self.analyze_data_availability()
        
        # Test all crypto files
        self.test_crypto_scripts()
        self.test_crypto_tools()
        self.test_crypto_utilities()
        
        # Generate reports
        self.generate_data_report()
        self.generate_summary()


if __name__ == "__main__":
    # Run comprehensive test suite
    test_suite = CryptoTestSuite()
    test_suite.run_all_tests()
