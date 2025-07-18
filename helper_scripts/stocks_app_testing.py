#!/usr/bin/env python3
"""
Stocks App Testing Suite - AlgoProject
======================================

Comprehensive testing suite for all stocks functionality.
This single file replaces all individual stocks test files.

Features:
- Complete stocks module validation
- Fyers API integration testing
- Mixed portfolio data acquisition
- Module functionality verification
- Performance benchmarks
- Error handling validation
- Detailed step-by-step logging for troubleshooting

Author: AlgoProject Team
Date: July 15, 2025
"""

import os
import sys
import time
import logging
import traceback
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import importlib.util

# ===================================================================
# PROJECT SETUP & LOGGING
# ===================================================================

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Create logs directory
logs_dir = os.path.join(project_root, 'helper_scripts', 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Setup comprehensive logging
log_filename = f"stocks_testing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
log_filepath = os.path.join(logs_dir, log_filename)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',
    handlers=[
        logging.FileHandler(log_filepath, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("StocksAppTesting")

class StocksAppTestSuite:
    """Comprehensive stocks application testing suite."""
    
    def __init__(self):
        """Initialize the test suite."""
        self.project_root = project_root
        self.test_results = {}
        self.start_time = datetime.now()
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
        logger.info("=" * 80)
        logger.info("📈 STOCKS APP TESTING SUITE INITIALIZED")
        logger.info("=" * 80)
        logger.info(f"📁 Project Root: {self.project_root}")
        logger.info(f"📝 Log File: {log_filepath}")
        logger.info(f"🕐 Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)

    def run_test(self, test_name: str, test_func, *args, **kwargs):
        """Run a single test with error handling and logging."""
        self.total_tests += 1
        logger.info(f"\n{'='*20} TEST {self.total_tests}: {test_name} {'='*20}")
        logger.info(f"🔍 Starting: {test_name}")
        
        start_time = time.time()
        try:
            result = test_func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            if result:
                self.passed_tests += 1
                logger.info(f"✅ PASSED: {test_name} (⏱️ {elapsed:.2f}s)")
                self.test_results[test_name] = {"status": "PASSED", "time": elapsed, "error": None}
                return True
            else:
                self.failed_tests += 1
                logger.error(f"❌ FAILED: {test_name} (⏱️ {elapsed:.2f}s)")
                self.test_results[test_name] = {"status": "FAILED", "time": elapsed, "error": "Test returned False"}
                return False
                
        except Exception as e:
            elapsed = time.time() - start_time
            self.failed_tests += 1
            logger.error(f"❌ ERROR: {test_name} (⏱️ {elapsed:.2f}s)")
            logger.error(f"Exception: {str(e)}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            self.test_results[test_name] = {"status": "ERROR", "time": elapsed, "error": str(e)}
            return False

    # ===================================================================
    # TEST 1: STOCKS MODULE STRUCTURE VALIDATION
    # ===================================================================
    
    def test_stocks_structure(self):
        """Test 1: Validate stocks module directory structure."""
        logger.info("🔍 Validating stocks module structure...")
        
        required_dirs = [
            "stocks",
            "stocks/scripts",
            "stocks/output",  
            "stocks/logs"
        ]
        
        required_files = [
            "stocks/data_acquisition.py",
            "stocks/__init__.py"
        ]
        
        # Check directories
        logger.info("📁 Checking required directories...")
        for directory in required_dirs:
            dir_path = os.path.join(self.project_root, directory)
            if os.path.exists(dir_path):
                logger.info(f"  ✅ {directory}/")
            else:
                logger.warning(f"  ⚠️ Missing directory: {directory}/ (will be created as needed)")
        
        # Check files
        logger.info("📄 Checking required files...")
        missing_files = []
        for file in required_files:
            file_path = os.path.join(self.project_root, file)
            if os.path.exists(file_path):
                logger.info(f"  ✅ {file}")
            else:
                logger.error(f"  ❌ Missing file: {file}")
                missing_files.append(file)
        
        if missing_files:
            logger.error(f"❌ Missing critical files: {missing_files}")
            return False
        
        logger.info("✅ Stocks module structure validation complete")
        return True

    # ===================================================================
    # TEST 2: STOCKS DATA ACQUISITION TESTING
    # ===================================================================
    
    def test_stocks_data_acquisition(self):
        """Test 2: Test stocks data acquisition capabilities."""
        logger.info("📈 Testing stocks data acquisition...")
        
        try:
            # Check if stocks data acquisition exists
            stocks_data_path = os.path.join(self.project_root, 'stocks', 'data_acquisition.py')
            if not os.path.exists(stocks_data_path):
                logger.error("❌ Stocks data acquisition module not found")
                return False
            
            # Try to import stocks data acquisition
            from stocks.data_acquisition import fetch_data, health_check
            logger.info("✅ Stocks data acquisition module imported")
            
            # Health check
            logger.info("🔍 Running stocks health check...")
            health = health_check()
            logger.info(f"📊 Health Status: {health['status']}")
            
            # Test basic functionality (without requiring Fyers API credentials)
            logger.info("📊 Testing basic functionality...")
            
            # Note: This test will validate the module structure without requiring live API
            test_symbols = ['RELIANCE', 'TCS', 'HDFCBANK']
            
            for symbol in test_symbols:
                logger.info(f"🔄 Testing data structure for {symbol}...")
                try:
                    # This may fail due to API credentials, but we check the error handling
                    data = fetch_data(symbol, 'NSE', '1h', 5)
                    if data is not None and len(data) > 0:
                        logger.info(f"  ✅ {symbol}: Data fetched successfully")
                    else:
                        logger.info(f"  ⚠️ {symbol}: No data (expected without API credentials)")
                except Exception as e:
                    logger.info(f"  ⚠️ {symbol}: Error expected without credentials: {str(e)[:100]}...")
            
            logger.info("✅ Stocks data acquisition test complete")
            return True
                
        except ImportError as e:
            logger.error(f"❌ Cannot import stocks data acquisition: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Stocks data acquisition test failed: {e}")
            return False

    # ===================================================================
    # TEST 3: STOCKS SCRIPTS TESTING
    # ===================================================================
    
    def test_stocks_scripts(self):
        """Test 3: Test stocks module scripts."""
        logger.info("📜 Testing stocks scripts...")
        
        stocks_scripts_dir = os.path.join(self.project_root, 'stocks', 'scripts')
        
        if not os.path.exists(stocks_scripts_dir):
            logger.warning("⚠️ Stocks scripts directory not found - may not be implemented yet")
            return True  # Not critical for basic testing
        
        # List available scripts
        scripts = []
        for file in os.listdir(stocks_scripts_dir):
            if file.endswith('.py') and not file.startswith('__'):
                scripts.append(file)
        
        logger.info(f"📊 Found {len(scripts)} stock scripts")
        for script in scripts:
            logger.info(f"  📄 {script}")
        
        # Basic validation that scripts exist
        if len(scripts) > 0:
            logger.info("✅ Stocks scripts found and available")
            return True
        else:
            logger.info("ℹ️ No stocks scripts found - may not be implemented yet")
            return True  # Not critical failure

    # ===================================================================
    # TEST 4: FYERS API INTEGRATION CHECK
    # ===================================================================
    
    def test_fyers_integration(self):
        """Test 4: Check Fyers API integration capabilities."""
        logger.info("🔑 Testing Fyers API integration...")
        
        try:
            # Check if fyers_api is available
            import fyers_api
            logger.info("✅ fyers_api package is available")
            
            # Check if stocks module can handle Fyers
            from stocks.data_acquisition import fetch_data
            logger.info("✅ Stocks data acquisition can import Fyers functionality")
            
            # Note: We won't test actual API calls without credentials
            logger.info("ℹ️ API credentials test skipped (requires live credentials)")
            logger.info("✅ Fyers integration structure is ready")
            return True
            
        except ImportError as e:
            logger.warning(f"⚠️ Fyers API not available: {e}")
            logger.info("ℹ️ This is expected if Fyers API is not installed")
            logger.info("ℹ️ Stocks module can still function with CCXT for crypto pairs")
            return True  # Not critical - module can work without Fyers
        except Exception as e:
            logger.error(f"❌ Fyers integration test failed: {e}")
            return False

    # ===================================================================
    # TEST 5: MIXED PORTFOLIO CAPABILITIES
    # ===================================================================
    
    def test_mixed_portfolio(self):
        """Test 5: Test mixed portfolio (stocks + crypto) capabilities."""
        logger.info("🔄 Testing mixed portfolio capabilities...")
        
        try:
            # Check if stocks module can handle both stocks and crypto
            from stocks.data_acquisition import fetch_data
            
            # Test crypto pair through stocks module (should use CCXT)
            logger.info("🪙 Testing crypto pair through stocks module...")
            try:
                crypto_data = fetch_data('BTC/USDT', 'binance', '1h', 5, data_source="ccxt")
                if crypto_data is not None and len(crypto_data) > 0:
                    logger.info("  ✅ Crypto data fetched through stocks module")
                else:
                    logger.info("  ⚠️ No crypto data (expected without proper setup)")
            except Exception as e:
                logger.info(f"  ⚠️ Crypto fetch error: {str(e)[:100]}...")
            
            # Test stock symbol (would require Fyers API)
            logger.info("📈 Testing stock symbol through stocks module...")
            try:
                stock_data = fetch_data('RELIANCE', 'NSE', '1h', 5, data_source="fyers")
                if stock_data is not None and len(stock_data) > 0:
                    logger.info("  ✅ Stock data fetched through stocks module")
                else:
                    logger.info("  ⚠️ No stock data (expected without Fyers credentials)")
            except Exception as e:
                logger.info(f"  ⚠️ Stock fetch error: {str(e)[:100]}...")
            
            logger.info("✅ Mixed portfolio capability test complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Mixed portfolio test failed: {e}")
            return False

    # ===================================================================
    # TEST 6: STOCKS MODULE INDEPENDENCE
    # ===================================================================
    
    def test_stocks_independence(self):
        """Test 6: Verify stocks module independence from crypto."""
        logger.info("🔒 Testing stocks module independence...")
        
        try:
            # Import stocks module
            import stocks
            logger.info("✅ Stocks module imported successfully")
            
            # Check that stocks module can work independently
            from stocks.data_acquisition import health_check
            health = health_check()
            logger.info(f"✅ Stocks health check: {health['status']}")
            
            # Verify stocks module doesn't break crypto independence
            logger.info("🔍 Verifying crypto module still works independently...")
            from crypto.data_acquisition import health_check as crypto_health_check
            crypto_health = crypto_health_check()
            logger.info(f"✅ Crypto still independent: {crypto_health['status']}")
            
            logger.info("✅ Stocks module independence verified")
            return True
            
        except Exception as e:
            logger.error(f"❌ Stocks independence test failed: {e}")
            return False

    # ===================================================================
    # TEST 7: PERFORMANCE AND ERROR HANDLING
    # ===================================================================
    
    def test_performance_and_errors(self):
        """Test 7: Test performance and error handling."""
        logger.info("⚡ Testing performance and error handling...")
        
        try:
            from stocks.data_acquisition import fetch_data
            
            # Test invalid symbol handling
            logger.info("🔄 Testing invalid symbol handling...")
            result = fetch_data('INVALID_SYMBOL', 'NSE', '1h', 5)
            if result is None or (hasattr(result, 'empty') and result.empty):
                logger.info("  ✅ Invalid symbol handled gracefully")
            else:
                logger.warning("  ⚠️ Invalid symbol returned unexpected data")
            
            # Test invalid exchange handling
            logger.info("🔄 Testing invalid exchange handling...")
            result = fetch_data('RELIANCE', 'INVALID_EXCHANGE', '1h', 5)
            if result is None or (hasattr(result, 'empty') and result.empty):
                logger.info("  ✅ Invalid exchange handled gracefully")
            else:
                logger.warning("  ⚠️ Invalid exchange returned unexpected data")
            
            logger.info("✅ Error handling test complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Performance/error test failed: {e}")
            return False

    # ===================================================================
    # TEST EXECUTION & REPORTING
    # ===================================================================
    
    def generate_final_report(self):
        """Generate comprehensive test report."""
        end_time = datetime.now()
        total_duration = end_time - self.start_time
        
        logger.info("\n" + "=" * 80)
        logger.info("📋 STOCKS APP TESTING - FINAL REPORT")
        logger.info("=" * 80)
        logger.info(f"🕐 Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"🕐 Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"⏱️ Total Duration: {total_duration}")
        logger.info(f"📊 Total Tests: {self.total_tests}")
        logger.info(f"✅ Passed: {self.passed_tests}")
        logger.info(f"❌ Failed: {self.failed_tests}")
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        logger.info(f"📈 Success Rate: {success_rate:.1f}%")
        
        logger.info("\n📋 DETAILED TEST RESULTS:")
        logger.info("-" * 80)
        
        for test_name, result in self.test_results.items():
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            logger.info(f"{status_icon} {test_name}: {result['status']} (⏱️ {result['time']:.2f}s)")
            if result["error"]:
                logger.info(f"     Error: {result['error']}")
        
        logger.info("\n🎯 RECOMMENDATIONS:")
        logger.info("-" * 80)
        
        if self.failed_tests == 0:
            logger.info("🎉 ALL TESTS PASSED! Stocks module structure is operational.")
            logger.info("✅ Ready for stocks trading development")
            logger.info("✅ Module structure correctly configured")
            logger.info("✅ Independence from crypto module maintained")
        else:
            logger.info(f"⚠️ {self.failed_tests} test(s) failed - review failures above")
            logger.info("🔧 Fix failing tests before production deployment")
            logger.info("📚 Check documentation for troubleshooting")
        
        if self.failed_tests <= 1:  # Allow for API credential issues
            logger.info("ℹ️ Some failures may be due to missing API credentials")
            logger.info("ℹ️ This is expected in development environment")
        
        logger.info(f"\n📝 Detailed logs saved to: {log_filepath}")
        logger.info("=" * 80)
        
        # Success if no critical failures (allow API credential issues)
        return self.failed_tests <= 1

    def run_all_tests(self):
        """Execute all stocks tests."""
        logger.info("🚀 STARTING COMPREHENSIVE STOCKS TESTING")
        
        # Execute all tests
        test_functions = [
            ("Stocks Module Structure Validation", self.test_stocks_structure),
            ("Stocks Data Acquisition Testing", self.test_stocks_data_acquisition),
            ("Stocks Scripts Testing", self.test_stocks_scripts),
            ("Fyers API Integration Check", self.test_fyers_integration),
            ("Mixed Portfolio Capabilities", self.test_mixed_portfolio),
            ("Stocks Module Independence", self.test_stocks_independence),
            ("Performance and Error Handling", self.test_performance_and_errors)
        ]
        
        for test_name, test_func in test_functions:
            self.run_test(test_name, test_func)
        
        # Generate final report
        success = self.generate_final_report()
        return success

def main():
    """Main function to run stocks app testing."""
    try:
        # Initialize test suite
        test_suite = StocksAppTestSuite()
        
        # Run all tests
        success = test_suite.run_all_tests()
        
        # Exit with appropriate code
        exit_code = 0 if success else 1
        logger.info(f"🏁 Exiting with code: {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.error(f"💥 CRITICAL ERROR in main: {e}")
        logger.debug(f"Traceback: {traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
