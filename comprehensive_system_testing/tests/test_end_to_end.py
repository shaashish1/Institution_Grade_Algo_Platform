"""
End-to-End System Validation
============================

Comprehensive system test that validates the entire AlgoProject.
"""

import unittest
import tempfile
import os
import time
from pathlib import Path

from ..core.test_orchestrator import TestOrchestrator
from ..core.models import TestConfiguration, TestStatus, Severity
from ..reporting.report_generator import ReportGenerator


class TestEndToEndValidation(unittest.TestCase):
    """End-to-end system validation tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = TestConfiguration(
            auto_fix_enabled=True,
            parallel_execution=False,  # Disable for predictable testing
            timeout_seconds=60
        )
        self.orchestrator = TestOrchestrator(self.config)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_complete_project_structure(self):
        """Create a complete AlgoProject-like structure for testing"""
        base_path = Path(self.temp_dir)
        
        # Create main directories
        directories = [
            "crypto/input",
            "crypto/output", 
            "crypto/logs",
            "crypto/scripts",
            "stocks/input",
            "stocks/output",
            "stocks/logs",
            "stocks/fyers",
            "strategies",
            "tools",
            "utils",
            "docs",
            "helper_scripts"
        ]
        
        for directory in directories:
            (base_path / directory).mkdir(parents=True, exist_ok=True)
        
        # Create main entry points
        entry_points = {
            "main.py": '''#!/usr/bin/env python3
"""Main entry point for AlgoProject"""
import os
import sys

def main():
    print("AlgoProject - Trading Platform")
    return True

if __name__ == "__main__":
    main()
''',
            "crypto_launcher.py": '''#!/usr/bin/env python3
"""Crypto trading launcher"""
import os

def launch_crypto():
    print("Launching crypto trading")
    return True

if __name__ == "__main__":
    launch_crypto()
''',
            "crypto_main.py": '''#!/usr/bin/env python3
"""Direct crypto entry point"""

def crypto_main():
    print("Crypto main function")
    return True

if __name__ == "__main__":
    crypto_main()
'''
        }
        
        for filename, content in entry_points.items():
            with open(base_path / filename, 'w') as f:
                f.write(content)
        
        # Create module __init__.py files
        init_files = [
            "crypto/__init__.py",
            "stocks/__init__.py", 
            "strategies/__init__.py",
            "tools/__init__.py",
            "utils/__init__.py"
        ]
        
        for init_file in init_files:
            with open(base_path / init_file, 'w') as f:
                f.write(f'"""Module: {init_file.split("/")[0]}"""\n__version__ = "1.0.0"\n')
        
        # Create sample strategy files
        strategies = {
            "strategies/sma_cross.py": '''"""Simple Moving Average Crossover Strategy"""

class SMAStrategy:
    def __init__(self, short_window=10, long_window=30):
        self.short_window = short_window
        self.long_window = long_window
    
    def calculate_signals(self, data):
        """Calculate trading signals"""
        return {"signal": "buy", "confidence": 0.8}
    
    def get_parameters(self):
        """Get strategy parameters"""
        return {"short_window": self.short_window, "long_window": self.long_window}
''',
            "strategies/rsi_strategy.py": '''"""RSI Strategy"""

class RSIStrategy:
    def __init__(self, period=14, oversold=30, overbought=70):
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def calculate_signals(self, data):
        """Calculate RSI signals"""
        return {"signal": "hold", "rsi": 45}
    
    def get_parameters(self):
        """Get strategy parameters"""
        return {
            "period": self.period,
            "oversold": self.oversold,
            "overbought": self.overbought
        }
'''
        }
        
        for filename, content in strategies.items():
            with open(base_path / filename, 'w') as f:
                f.write(content)
        
        # Create crypto module files
        crypto_files = {
            "crypto/data_acquisition.py": '''"""Crypto data acquisition"""
import time

def fetch_data(symbol, timeframe="1h", limit=100):
    """Fetch crypto data"""
    return {"symbol": symbol, "data": []}

def health_check():
    """Health check for crypto module"""
    return {
        "status": "healthy",
        "ccxt_available": True,
        "working_exchanges": ["binance", "coinbase"]
    }

def get_available_exchanges():
    """Get available exchanges"""
    return ["binance", "coinbase", "kraken"]
''',
            "crypto/crypto_assets_manager.py": '''"""Crypto assets manager"""

class CryptoAssetsManager:
    def __init__(self):
        self.assets = []
    
    def load_assets(self, file_path):
        """Load crypto assets from file"""
        return True
    
    def validate_symbol(self, symbol):
        """Validate crypto symbol"""
        return symbol.upper() in ["BTC/USDT", "ETH/USDT", "ADA/USDT"]
'''
        }
        
        for filename, content in crypto_files.items():
            with open(base_path / filename, 'w') as f:
                f.write(content)
        
        # Create stock module files
        stock_files = {
            "stocks/data_acquisition.py": '''"""Stock data acquisition"""

def fetch_data(symbol, timeframe="1D", limit=100):
    """Fetch stock data"""
    return {"symbol": symbol, "data": []}

def health_check():
    """Health check for stock module"""
    return {
        "status": "healthy",
        "fyers_available": False,
        "yfinance_available": True
    }

def get_live_quote(symbol):
    """Get live stock quote"""
    return {"symbol": symbol, "price": 100.0, "change": 1.5}
''',
            "stocks/simple_fyers_provider.py": '''"""Simple Fyers provider"""

class SimpleFyersDataProvider:
    def __init__(self):
        self.connected = False
    
    def connect(self):
        """Connect to Fyers API"""
        self.connected = True
        return True
    
    def get_data(self, symbol):
        """Get stock data"""
        return {"symbol": symbol, "price": 150.0}

def fetch_nse_stock_data(symbol):
    """Fetch NSE stock data"""
    return {"symbol": symbol, "exchange": "NSE", "price": 200.0}
'''
        }
        
        for filename, content in stock_files.items():
            with open(base_path / filename, 'w') as f:
                f.write(content)
        
        # Create configuration files
        config_files = {
            "requirements.txt": '''# AlgoProject Requirements
pandas>=1.3.0
numpy>=1.21.0
requests>=2.31.0
pyyaml>=6.0
ccxt>=4.0.0
yfinance>=0.2.0
matplotlib>=3.5.0
''',
            "crypto/input/crypto_assets.csv": '''symbol,name,exchange,active
BTC/USDT,Bitcoin,binance,true
ETH/USDT,Ethereum,binance,true
ADA/USDT,Cardano,binance,true
''',
            "stocks/input/stocks_assets.csv": '''symbol,name,exchange,sector,active
NSE:SBIN-EQ,State Bank of India,NSE,Banking,true
NSE:RELIANCE-EQ,Reliance Industries,NSE,Energy,true
NSE:TCS-EQ,Tata Consultancy Services,NSE,IT,true
''',
            "crypto/input/config_crypto.yaml": '''# Crypto Configuration
exchanges:
  binance:
    sandbox: true
    rate_limit: true
  coinbase:
    sandbox: true

symbols:
  - BTC/USDT
  - ETH/USDT
  - ADA/USDT

timeframes:
  - 1m
  - 5m
  - 1h
  - 1d
''',
            "config.json": '''{
  "application": {
    "name": "AlgoProject",
    "version": "1.0.0",
    "debug": false
  },
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "algoproject"
  }
}
'''
        }
        
        for filename, content in config_files.items():
            with open(base_path / filename, 'w') as f:
                f.write(content)
        
        # Create some files with intentional issues for testing auto-fix
        problematic_files = {
            "test_file_with_issues.py": '''# File with various issues
import os,
from sys import *

def function_with_issues():
\tprint('Mixed quotes and tabs')   
\treturn True  

class TestClass:
    def method(self):
        my_list = [1, 2, 3,
        return my_list
'''
        }
        
        for filename, content in problematic_files.items():
            with open(base_path / filename, 'w') as f:
                f.write(content)
    
    def test_comprehensive_system_validation(self):
        """Test complete system validation"""
        # Create complete project structure
        self._create_complete_project_structure()
        
        # Run comprehensive test
        start_time = time.time()
        result = self.orchestrator.run_comprehensive_test(self.temp_dir)
        execution_time = time.time() - start_time
        
        # Validate results structure
        self.assertIn("results", result)
        self.assertIn("system_health", result)
        self.assertIn("execution_time", result)
        self.assertIn("report_files", result)
        
        # Check that we got test results
        results = result["results"]
        self.assertGreater(len(results), 0)
        
        # Verify different types of tests were run
        test_components = set(r.component for r in results)
        expected_components = {
            "syntax_validator",
            "import_tester", 
            "dependency_checker",
            "config_validator",
            "integration_tester"
        }
        
        # Should have results from multiple components
        self.assertGreater(len(test_components.intersection(expected_components)), 2)
        
        # Check system health calculation
        system_health = result["system_health"]
        if system_health:
            self.assertIsNotNone(system_health.overall_score)
            self.assertGreaterEqual(system_health.overall_score, 0)
            self.assertLessEqual(system_health.overall_score, 100)
        
        # Verify execution time is reasonable
        self.assertLess(execution_time, 300)  # Should complete within 5 minutes
        
        # Check that reports were generated
        report_files = result.get("report_files", {})
        self.assertIn("html", report_files)
        
        print(f"✅ Comprehensive test completed in {execution_time:.2f} seconds")
        print(f"📊 Total tests run: {len(results)}")
        print(f"🏥 System health score: {system_health.overall_score:.1f}/100" if system_health else "🏥 System health: Not calculated")
    
    def test_performance_benchmarking(self):
        """Test system performance and resource usage"""
        self._create_complete_project_structure()
        
        # Measure performance metrics
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        result = self.orchestrator.run_quick_test(self.temp_dir)
        end_time = time.time()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = final_memory - initial_memory
        execution_time = end_time - start_time
        
        # Performance assertions
        self.assertLess(execution_time, 60)  # Should complete within 1 minute for quick test
        self.assertLess(memory_used, 100)   # Should use less than 100MB additional memory
        
        # Check results quality
        results = result["results"]
        self.assertGreater(len(results), 0)
        
        print(f"⚡ Performance metrics:")
        print(f"   Execution time: {execution_time:.2f} seconds")
        print(f"   Memory usage: {memory_used:.1f} MB")
        print(f"   Tests per second: {len(results)/execution_time:.1f}")
    
    def test_error_handling_and_recovery(self):
        """Test system behavior with various error conditions"""
        # Create structure with some missing components
        base_path = Path(self.temp_dir)
        
        # Create minimal structure
        (base_path / "src").mkdir()
        
        # Create file with syntax errors
        with open(base_path / "broken_file.py", 'w') as f:
            f.write("def broken_function(\n    print('missing closing parenthesis')\n")
        
        # Create invalid JSON config
        with open(base_path / "invalid_config.json", 'w') as f:
            f.write('{"invalid": json: content}')
        
        # Run test and verify it handles errors gracefully
        result = self.orchestrator.run_comprehensive_test(self.temp_dir)
        
        # Should complete despite errors
        self.assertIn("results", result)
        
        # Should identify the issues
        results = result["results"]
        failed_tests = [r for r in results if r.status == TestStatus.FAIL]
        
        # Should have some failed tests due to the intentional errors
        self.assertGreater(len(failed_tests), 0)
        
        # System should still calculate health (even if low)
        system_health = result.get("system_health")
        if system_health:
            # Health score should be low due to errors
            self.assertLess(system_health.overall_score, 80)
        
        print(f"🛡️  Error handling test completed")
        print(f"   Failed tests detected: {len(failed_tests)}")
        print(f"   System remained stable: ✅")
    
    def test_auto_fix_integration(self):
        """Test auto-fix functionality in end-to-end scenario"""
        self._create_complete_project_structure()
        
        # Enable auto-fix
        config = TestConfiguration(auto_fix_enabled=True)
        orchestrator = TestOrchestrator(config)
        
        # Run comprehensive test with auto-fix
        result = orchestrator.run_comprehensive_test(self.temp_dir)
        
        results = result["results"]
        
        # Check for auto-fix results
        auto_fixed_results = [r for r in results if r.auto_fixed]
        
        if auto_fixed_results:
            print(f"🔧 Auto-fixes applied: {len(auto_fixed_results)}")
            for fix in auto_fixed_results[:3]:  # Show first 3
                print(f"   • {fix.component}: {fix.message}")
        
        # Verify that problematic file was fixed
        problematic_file = Path(self.temp_dir) / "test_file_with_issues.py"
        if problematic_file.exists():
            with open(problematic_file, 'r') as f:
                fixed_content = f.read()
            
            # Should have fixed some issues
            self.assertNotIn('\t', fixed_content)  # Tabs should be converted to spaces
    
    def test_report_generation_integration(self):
        """Test report generation in end-to-end scenario"""
        self._create_complete_project_structure()
        
        result = self.orchestrator.run_comprehensive_test(self.temp_dir)
        
        # Check that reports were generated
        report_files = result.get("report_files", {})
        
        # Should have multiple report formats
        self.assertIn("html", report_files)
        self.assertIn("json", report_files)
        
        # Verify report files exist
        for format_name, file_path in report_files.items():
            if file_path:
                self.assertTrue(os.path.exists(file_path), f"{format_name} report file should exist")
                
                # Check file is not empty
                file_size = os.path.getsize(file_path)
                self.assertGreater(file_size, 0, f"{format_name} report should not be empty")
        
        print(f"📊 Reports generated:")
        for format_name, file_path in report_files.items():
            if file_path:
                size_kb = os.path.getsize(file_path) / 1024
                print(f"   • {format_name.upper()}: {file_path} ({size_kb:.1f} KB)")
    
    def test_system_health_scoring(self):
        """Test system health scoring accuracy"""
        # Create project with known issues
        base_path = Path(self.temp_dir)
        
        # Create mix of good and bad files
        good_files = {
            "good_file.py": '''"""Well-written Python file"""

def clean_function():
    """A clean function with proper formatting"""
    result = "hello world"
    return result

class CleanClass:
    """A clean class"""
    
    def __init__(self):
        self.value = 42
    
    def get_value(self):
        return self.value
'''
        }
        
        bad_files = {
            "bad_file.py": '''# Poorly written file
import os,
from sys import *

def bad_function(
\tprint("syntax errors and bad formatting")   
\treturn None  

class BadClass:
    def method():  # Missing self parameter
        undefined_variable = some_undefined_var
        return undefined_variable
'''
        }
        
        # Create files
        for filename, content in good_files.items():
            with open(base_path / filename, 'w') as f:
                f.write(content)
        
        for filename, content in bad_files.items():
            with open(base_path / filename, 'w') as f:
                f.write(content)
        
        # Run test
        result = self.orchestrator.run_comprehensive_test(self.temp_dir)
        system_health = result.get("system_health")
        
        if system_health:
            # Should have calculated a reasonable health score
            self.assertGreaterEqual(system_health.overall_score, 0)
            self.assertLessEqual(system_health.overall_score, 100)
            
            # Should have component scores
            self.assertGreater(len(system_health.component_scores), 0)
            
            print(f"🏥 System Health Analysis:")
            print(f"   Overall Score: {system_health.overall_score:.1f}/100")
            print(f"   Critical Issues: {len(system_health.critical_issues)}")
            print(f"   Warnings: {len(system_health.warnings)}")
            print(f"   Trend: {system_health.trend.value}")


if __name__ == '__main__':
    unittest.main()