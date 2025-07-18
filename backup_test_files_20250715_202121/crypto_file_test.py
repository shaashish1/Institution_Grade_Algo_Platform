#!/usr/bin/env python3
"""
Crypto Module File-by-File Test
Tests each Python file in the crypto module for import safety and basic functionality
"""

import sys
import os
import importlib.util
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.getcwd())

class CryptoFileTester:
    """Test individual crypto module files."""
    
    def __init__(self):
        self.results = {}
        self.start_time = datetime.now()
    
    def test_file_import(self, file_path, module_name):
        """Test if a file can be imported safely."""
        try:
            # Load module specification
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None:
                return False, "Cannot create module spec"
            
            # Create and execute module
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            return True, "Import successful"
            
        except ImportError as e:
            if 'fyers' in str(e).lower():
                return False, f"❌ CRITICAL: Fyers dependency: {e}"
            return False, f"Import error: {e}"
        except Exception as e:
            return False, f"Execution error: {e}"
    
    def test_core_modules(self):
        """Test core crypto modules."""
        print("🔧 TESTING CORE MODULES")
        print("-" * 50)
        
        core_files = [
            ('crypto/data_acquisition.py', 'data_acquisition'),
            ('crypto/crypto_symbol_manager.py', 'crypto_symbol_manager'),
            ('crypto/list_crypto_assets.py', 'list_crypto_assets'),
            ('crypto/list_ccxt_exchanges.py', 'list_ccxt_exchanges')
        ]
        
        for file_path, module_name in core_files:
            if os.path.exists(file_path):
                print(f"Testing {module_name}...", end=" ")
                success, message = self.test_file_import(file_path, module_name)
                
                self.results[module_name] = {
                    'success': success,
                    'message': message,
                    'category': 'core'
                }
                
                if success:
                    print("✅ PASS")
                else:
                    print(f"❌ FAIL - {message}")
            else:
                print(f"⚠️ File not found: {file_path}")
    
    def test_script_modules(self):
        """Test crypto script modules."""
        print(f"\n📜 TESTING SCRIPT MODULES")
        print("-" * 50)
        
        script_dir = 'crypto/scripts'
        if os.path.exists(script_dir):
            script_files = [f for f in os.listdir(script_dir) if f.endswith('.py') and f != '__init__.py']
            
            # Filter production files (no test/demo in name)
            production_files = [f for f in script_files if not any(x in f.lower() for x in ['test', 'demo', 'temp'])]
            test_files = [f for f in script_files if any(x in f.lower() for x in ['test', 'demo'])]
            
            print(f"Found {len(production_files)} production scripts, {len(test_files)} test/demo scripts")
            
            # Test production files first
            for script_file in production_files:
                file_path = os.path.join(script_dir, script_file)
                module_name = script_file.replace('.py', '')
                
                print(f"Testing {module_name}...", end=" ")
                success, message = self.test_file_import(file_path, module_name)
                
                self.results[module_name] = {
                    'success': success,
                    'message': message,
                    'category': 'script'
                }
                
                if success:
                    print("✅ PASS")
                else:
                    print(f"❌ FAIL - {message}")
            
            # Test demo/test files
            print(f"\n🧪 Testing demo/test scripts:")
            for script_file in test_files:
                file_path = os.path.join(script_dir, script_file)
                module_name = script_file.replace('.py', '')
                
                print(f"Testing {module_name}...", end=" ")
                success, message = self.test_file_import(file_path, module_name)
                
                self.results[module_name] = {
                    'success': success,
                    'message': message,
                    'category': 'test'
                }
                
                if success:
                    print("✅ PASS")
                else:
                    print(f"❌ FAIL - {message}")
    
    def test_tool_modules(self):
        """Test crypto tool modules."""
        print(f"\n🛠️ TESTING TOOL MODULES")
        print("-" * 50)
        
        tools_dir = 'crypto/tools'
        if os.path.exists(tools_dir):
            tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.py') and f != '__init__.py']
            
            for tool_file in tool_files:
                file_path = os.path.join(tools_dir, tool_file)
                module_name = tool_file.replace('.py', '')
                
                print(f"Testing {module_name}...", end=" ")
                success, message = self.test_file_import(file_path, module_name)
                
                self.results[module_name] = {
                    'success': success,
                    'message': message,
                    'category': 'tool'
                }
                
                if success:
                    print("✅ PASS")
                else:
                    print(f"❌ FAIL - {message}")
        else:
            print("⚠️ Tools directory not found")
    
    def test_data_functionality(self):
        """Test actual data fetching functionality."""
        print(f"\n📊 TESTING DATA FUNCTIONALITY")
        print("-" * 50)
        
        try:
            from crypto.data_acquisition import fetch_data, health_check
            
            # Health check
            print("Running health check...", end=" ")
            health = health_check()
            if health['status'] == 'healthy':
                print("✅ HEALTHY")
                print(f"   CCXT Available: {health['ccxt_available']}")
                print(f"   Working Exchanges: {len(health['working_exchanges'])}")
            else:
                print("❌ UNHEALTHY")
            
            # Data fetch test
            print("Testing data fetch...", end=" ")
            data = fetch_data('BTC/USDT', 'kraken', '1h', 10)
            
            if data is not None and len(data) > 0:
                print(f"✅ SUCCESS ({len(data)} bars)")
                
                # Show sample data
                latest = data.iloc[-1]
                print(f"   Latest: {data.index[-1]} - Close: ${latest['close']:.2f}")
                
                return True
            else:
                print("❌ NO DATA")
                return False
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def generate_summary(self):
        """Generate test summary."""
        print(f"\n📋 TEST SUMMARY")
        print("=" * 60)
        
        # Count by category
        categories = {}
        for module, result in self.results.items():
            category = result['category']
            if category not in categories:
                categories[category] = {'total': 0, 'passed': 0}
            
            categories[category]['total'] += 1
            if result['success']:
                categories[category]['passed'] += 1
        
        # Display results
        total_files = len(self.results)
        total_passed = sum(1 for r in self.results.values() if r['success'])
        
        print(f"📊 Overall Results:")
        print(f"   Total Files: {total_files}")
        print(f"   Passed: {total_passed}")
        print(f"   Failed: {total_files - total_passed}")
        print(f"   Success Rate: {(total_passed/total_files)*100:.1f}%")
        
        print(f"\n📂 Results by Category:")
        for category, stats in categories.items():
            success_rate = (stats['passed'] / stats['total']) * 100
            print(f"   {category.title()}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
        
        # Show failures
        failed_modules = [(name, result) for name, result in self.results.items() if not result['success']]
        if failed_modules:
            print(f"\n❌ Failed Modules:")
            for name, result in failed_modules:
                print(f"   • {name}: {result['message'][:60]}")
        
        # Save detailed log
        elapsed = datetime.now() - self.start_time
        log_file = f"crypto/logs/file_test_results_{self.start_time.strftime('%Y%m%d_%H%M%S')}.log"
        
        # Ensure logs directory exists
        os.makedirs('crypto/logs', exist_ok=True)
        
        with open(log_file, 'w') as f:
            f.write(f"Crypto Module File Test Results\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Duration: {elapsed.total_seconds():.2f}s\n\n")
            
            for name, result in self.results.items():
                f.write(f"Module: {name}\n")
                f.write(f"Category: {result['category']}\n")
                f.write(f"Success: {result['success']}\n")
                f.write(f"Message: {result['message']}\n\n")
        
        print(f"\n💾 Detailed log saved: {log_file}")
        print(f"⏱️ Total test time: {elapsed.total_seconds():.2f} seconds")

def main():
    """Run file-by-file tests."""
    print("🚀 CRYPTO MODULE FILE-BY-FILE TEST")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tester = CryptoFileTester()
    
    # Run all tests
    tester.test_core_modules()
    tester.test_script_modules()
    tester.test_tool_modules()
    
    # Test actual functionality
    data_works = tester.test_data_functionality()
    
    # Generate summary
    tester.generate_summary()
    
    if data_works:
        print("\n🎉 SUCCESS: Crypto module is fully functional!")
    else:
        print("\n⚠️ WARNING: Some functionality issues detected")

if __name__ == "__main__":
    main()
