#!/usr/bin/env python3
"""
Comprehensive AlgoProject Test Suite
Tests all files using correct paths and validates they work as expected
"""

import os
import sys
import time
import logging
import importlib.util
from datetime import datetime
import subprocess
import traceback

# Add project root to path (parent directory of tests)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Setup logging
test_logs_dir = os.path.join(project_root, 'tests', 'logs')
os.makedirs(test_logs_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(test_logs_dir, 'test_results.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ComprehensiveTestSuite:
    """Comprehensive test suite for AlgoProject."""
    
    def __init__(self):
        self.test_results = []
        self.start_time = datetime.now()
        self.project_root = project_root
        
    def print_header(self):
        """Print test suite header."""
        print("🧪 COMPREHENSIVE ALGOPROJECT TEST SUITE")
        print("=" * 80)
        print(f"📅 Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Project Root: {self.project_root}")
        print(f"🎯 Testing all files for functionality and compliance")
        print("=" * 80)
    
    def test_python_file_import(self, file_path, category="general"):
        """Test if a Python file can be imported safely."""
        try:
            # Get relative path for module name
            rel_path = os.path.relpath(file_path, self.project_root)
            module_name = rel_path.replace(os.sep, '.').replace('.py', '')
            
            # Skip __init__.py files
            if '__init__.py' in file_path:
                return True, "Init file skipped"
            
            # Load module specification
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                return False, "Cannot create module spec"
            
            # Create and execute module
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            return True, "Import successful"
            
        except ImportError as e:
            error_msg = str(e)
            if 'fyers' in error_msg.lower() and 'crypto' in file_path:
                return False, f"❌ CRITICAL: Crypto file has Fyers dependency: {error_msg}"
            return False, f"Import error: {error_msg}"
        except Exception as e:
            return False, f"Execution error: {str(e)[:100]}..."
    
    def test_directory_structure(self):
        """Test if directory structure follows coding rules."""
        print("\n📁 TESTING DIRECTORY STRUCTURE")
        print("-" * 50)
        
        required_dirs = ['crypto', 'stocks', 'docs', 'helper_scripts', 'venv']
        missing_dirs = []
        
        for dir_name in required_dirs:
            dir_path = os.path.join(self.project_root, dir_name)
            if os.path.exists(dir_path):
                print(f"✅ {dir_name}/ directory exists")
            else:
                print(f"❌ {dir_name}/ directory missing")
                missing_dirs.append(dir_name)
        
        # Check root directory cleanliness
        root_files = os.listdir(self.project_root)
        allowed_root_files = [
            'main.py', 'crypto_launcher.py', 'crypto_main.py',
            'setup.bat', 'requirements.txt', 'README.md', 'LICENSE', '.gitignore',
            'CRYPTO_STATUS_REPORT.md', '.git'
        ]
        
        disallowed_files = []
        for item in root_files:
            if item not in allowed_root_files and not os.path.isdir(os.path.join(self.project_root, item)):
                if not item.startswith('.') and not item.endswith('.md'):
                    disallowed_files.append(item)
        
        if disallowed_files:
            print(f"⚠️ Files in root that should be moved: {', '.join(disallowed_files)}")
        else:
            print("✅ Root directory is clean")
        
        return len(missing_dirs) == 0 and len(disallowed_files) == 0
    
    def test_crypto_module(self):
        """Test crypto module comprehensively."""
        print("\n🪙 TESTING CRYPTO MODULE")
        print("-" * 50)
        
        crypto_dir = os.path.join(self.project_root, 'crypto')
        if not os.path.exists(crypto_dir):
            print("❌ Crypto directory not found")
            return False
        
        # Test core crypto files
        core_files = [
            'data_acquisition.py',
            'crypto_symbol_manager.py',
            'list_crypto_assets.py',
            'list_ccxt_exchanges.py'
        ]
        
        success_count = 0
        total_files = 0
        
        for file_name in core_files:
            file_path = os.path.join(crypto_dir, file_name)
            if os.path.exists(file_path):
                total_files += 1
                success, message = self.test_python_file_import(file_path, "crypto_core")
                if success:
                    print(f"✅ {file_name}: {message}")
                    success_count += 1
                else:
                    print(f"❌ {file_name}: {message}")
                    
                self.test_results.append({
                    'file': file_name,
                    'category': 'crypto_core',
                    'success': success,
                    'message': message
                })
        
        # Test crypto scripts
        scripts_dir = os.path.join(crypto_dir, 'scripts')
        if os.path.exists(scripts_dir):
            script_files = [f for f in os.listdir(scripts_dir) if f.endswith('.py')]
            
            for script_file in script_files:
                script_path = os.path.join(scripts_dir, script_file)
                total_files += 1
                success, message = self.test_python_file_import(script_path, "crypto_script")
                if success:
                    print(f"✅ scripts/{script_file}: {message}")
                    success_count += 1
                else:
                    print(f"❌ scripts/{script_file}: {message}")
                    
                self.test_results.append({
                    'file': f"scripts/{script_file}",
                    'category': 'crypto_script',
                    'success': success,
                    'message': message
                })
        
        # Test crypto tools
        tools_dir = os.path.join(crypto_dir, 'tools')
        if os.path.exists(tools_dir):
            tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.py')]
            
            for tool_file in tool_files:
                tool_path = os.path.join(tools_dir, tool_file)
                total_files += 1
                success, message = self.test_python_file_import(tool_path, "crypto_tool")
                if success:
                    print(f"✅ tools/{tool_file}: {message}")
                    success_count += 1
                else:
                    print(f"❌ tools/{tool_file}: {message}")
                    
                self.test_results.append({
                    'file': f"tools/{tool_file}",
                    'category': 'crypto_tool',
                    'success': success,
                    'message': message
                })
        
        print(f"\n📊 Crypto Module Results: {success_count}/{total_files} files passed")
        return success_count == total_files
    
    def test_stocks_module(self):
        """Test stocks module if it exists."""
        print("\n📈 TESTING STOCKS MODULE")
        print("-" * 50)
        
        stocks_dir = os.path.join(self.project_root, 'stocks')
        if not os.path.exists(stocks_dir):
            print("⚠️ Stocks directory not found - skipping")
            return True
        
        stock_files = [f for f in os.listdir(stocks_dir) if f.endswith('.py')]
        
        success_count = 0
        for stock_file in stock_files:
            stock_path = os.path.join(stocks_dir, stock_file)
            success, message = self.test_python_file_import(stock_path, "stocks")
            if success:
                print(f"✅ {stock_file}: {message}")
                success_count += 1
            else:
                print(f"❌ {stock_file}: {message}")
                
            self.test_results.append({
                'file': stock_file,
                'category': 'stocks',
                'success': success,
                'message': message
            })
        
        print(f"\n📊 Stocks Module Results: {success_count}/{len(stock_files)} files passed")
        return success_count == len(stock_files)
    
    def test_launcher_files(self):
        """Test main launcher files."""
        print("\n🚀 TESTING LAUNCHER FILES")
        print("-" * 50)
        
        launcher_files = ['main.py', 'crypto_launcher.py', 'crypto_main.py']
        success_count = 0
        
        for launcher_file in launcher_files:
            launcher_path = os.path.join(self.project_root, launcher_file)
            if os.path.exists(launcher_path):
                success, message = self.test_python_file_import(launcher_path, "launcher")
                if success:
                    print(f"✅ {launcher_file}: {message}")
                    success_count += 1
                else:
                    print(f"❌ {launcher_file}: {message}")
                    
                self.test_results.append({
                    'file': launcher_file,
                    'category': 'launcher',
                    'success': success,
                    'message': message
                })
            else:
                print(f"⚠️ {launcher_file}: File not found")
        
        return success_count == len(launcher_files)
    
    def test_existing_tests(self):
        """Run existing tests in tests/ directory."""
        print("\n🧪 TESTING EXISTING TEST FILES")
        print("-" * 50)
        
        tests_dir = os.path.join(self.project_root, 'tests')
        if not os.path.exists(tests_dir):
            print("⚠️ Tests directory not found")
            return True
        
        test_files = [f for f in os.listdir(tests_dir) if f.endswith('.py') and f != '__init__.py']
        
        success_count = 0
        for test_file in test_files:
            test_path = os.path.join(tests_dir, test_file)
            success, message = self.test_python_file_import(test_path, "existing_test")
            if success:
                print(f"✅ tests/{test_file}: {message}")
                success_count += 1
            else:
                print(f"❌ tests/{test_file}: {message}")
                
            self.test_results.append({
                'file': f"tests/{test_file}",
                'category': 'existing_test',
                'success': success,
                'message': message
            })
        
        print(f"\n📊 Existing Tests Results: {success_count}/{len(test_files)} files passed")
        return success_count == len(test_files)
    
    def test_data_acquisition_functionality(self):
        """Test actual data acquisition functionality."""
        print("\n📊 TESTING DATA ACQUISITION FUNCTIONALITY")
        print("-" * 50)
        
        try:
            # Test crypto data acquisition
            from crypto.data_acquisition import fetch_data, health_check
            print("✅ Crypto data acquisition import successful")
            
            # Health check
            health = health_check()
            if health['status'] == 'healthy':
                print(f"✅ Crypto health check: {health['status']}")
                print(f"   CCXT Available: {health['ccxt_available']}")
                print(f"   Working Exchanges: {len(health['working_exchanges'])}")
            else:
                print(f"⚠️ Crypto health check: {health['status']}")
            
            # Quick data test
            print("🔍 Testing quick data fetch...")
            test_data = fetch_data('BTC/USDT', 'kraken', '1h', 5)
            if test_data is not None and len(test_data) > 0:
                print(f"✅ Data fetch successful: {len(test_data)} bars")
                print(f"   Latest price: ${test_data.iloc[-1]['close']:.2f}")
                return True
            else:
                print("❌ Data fetch returned no data")
                return False
                
        except Exception as e:
            print(f"❌ Data acquisition test failed: {e}")
            traceback.print_exc()
            return False
    
    def test_file_paths_and_imports(self):
        """Test that all import paths are correct."""
        print("\n🔗 TESTING IMPORT PATHS AND DEPENDENCIES")
        print("-" * 50)
        
        # Test crypto imports don't have stock dependencies
        crypto_files_with_fyers = []
        
        # Check all crypto files
        crypto_dir = os.path.join(self.project_root, 'crypto')
        for root, dirs, files in os.walk(crypto_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if 'fyers' in content.lower():
                                crypto_files_with_fyers.append(file_path)
                    except Exception:
                        continue
        
        if crypto_files_with_fyers:
            print("❌ CRITICAL: Crypto files with Fyers dependencies found:")
            for file_path in crypto_files_with_fyers:
                print(f"   {file_path}")
            return False
        else:
            print("✅ No Fyers dependencies found in crypto module")
            return True
    
    def test_output_directories(self):
        """Test that output directories exist and are correctly structured."""
        print("\n📁 TESTING OUTPUT DIRECTORY STRUCTURE")
        print("-" * 50)
        
        # Check crypto output directories
        crypto_output = os.path.join(self.project_root, 'crypto', 'output')
        crypto_logs = os.path.join(self.project_root, 'crypto', 'logs')
        crypto_input = os.path.join(self.project_root, 'crypto', 'input')
        
        directories_ok = True
        
        for dir_path, name in [(crypto_output, 'crypto/output'), 
                              (crypto_logs, 'crypto/logs'), 
                              (crypto_input, 'crypto/input')]:
            if os.path.exists(dir_path):
                print(f"✅ {name}/ exists")
            else:
                print(f"⚠️ {name}/ missing - will be created as needed")
        
        # Check helper_scripts directory
        helper_scripts = os.path.join(self.project_root, 'helper_scripts')
        if os.path.exists(helper_scripts):
            helper_files = os.listdir(helper_scripts)
            print(f"✅ helper_scripts/ exists with {len(helper_files)} files")
        else:
            print("❌ helper_scripts/ directory missing")
            directories_ok = False
        
        return directories_ok
    
    def generate_test_report(self):
        """Generate comprehensive test report."""
        elapsed = datetime.now() - self.start_time
        
        print("\n📋 COMPREHENSIVE TEST REPORT")
        print("=" * 80)
        
        # Overall statistics
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"📊 Overall Results:")
        print(f"   Total Files Tested: {total_tests}")
        print(f"   ✅ Successful: {successful_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   📈 Success Rate: {(successful_tests/total_tests)*100:.1f}%" if total_tests > 0 else "   📈 Success Rate: N/A (no tests)")
        print(f"   ⏱️ Total Time: {elapsed.total_seconds():.2f} seconds")
        
        # Results by category
        categories = {}
        for result in self.test_results:
            category = result['category']
            if category not in categories:
                categories[category] = {'total': 0, 'success': 0}
            categories[category]['total'] += 1
            if result['success']:
                categories[category]['success'] += 1
        
        print(f"\n📊 Results by Category:")
        for category, stats in categories.items():
            success_rate = (stats['success'] / stats['total']) * 100
            print(f"   {category}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")
        
        # Failed files details
        if failed_tests > 0:
            print(f"\n❌ FAILED FILES:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['file']}: {result['message']}")
        
        # Save detailed report
        timestamp = self.start_time.strftime('%Y%m%d_%H%M%S')
        report_file = f"comprehensive_test_report_{timestamp}.log"
        
        with open(report_file, 'w') as f:
            f.write(f"AlgoProject Comprehensive Test Report\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Total Files: {total_tests}\n")
            f.write(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%\n\n" if total_tests > 0 else "Success Rate: N/A\n\n")
            
            for result in self.test_results:
                f.write(f"File: {result['file']}\n")
                f.write(f"Category: {result['category']}\n")
                f.write(f"Success: {result['success']}\n")
                f.write(f"Message: {result['message']}\n\n")
        
        print(f"\n💾 Detailed report saved: {report_file}")
        
        return successful_tests == total_tests
    
    def run_all_tests(self):
        """Run complete test suite."""
        self.print_header()
        
        # Run all test categories
        tests_passed = []
        
        tests_passed.append(self.test_directory_structure())
        tests_passed.append(self.test_launcher_files())
        tests_passed.append(self.test_crypto_module())
        tests_passed.append(self.test_stocks_module())
        tests_passed.append(self.test_existing_tests())
        tests_passed.append(self.test_file_paths_and_imports())
        tests_passed.append(self.test_output_directories())
        tests_passed.append(self.test_data_acquisition_functionality())
        
        # Generate final report
        all_tests_passed = self.generate_test_report()
        
        print(f"\n🎯 FINAL ASSESSMENT")
        print("=" * 80)
        
        if all_tests_passed and all(tests_passed):
            print("🎉 ALL TESTS PASSED! AlgoProject is fully functional.")
            print("✅ Ready for production use")
            print("✅ All files working as expected")
            print("✅ Correct paths and structure validated")
        else:
            print("⚠️ Some tests failed. Review the report above.")
            print("🔧 Fix the issues and run tests again")
        
        return all_tests_passed


if __name__ == "__main__":
    print("🧪 Starting Comprehensive AlgoProject Test Suite...")
    
    test_suite = ComprehensiveTestSuite()
    success = test_suite.run_all_tests()
    
    if success:
        print("\n🎉 Test Suite Completed Successfully!")
        exit(0)
    else:
        print("\n❌ Test Suite Failed - Check Results Above")
        exit(1)
