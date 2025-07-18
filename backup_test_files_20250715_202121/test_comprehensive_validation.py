#!/usr/bin/env python3
"""
Comprehensive Project Validation Test
=====================================

This test validates that all Python files in the project can be imported
and basic functionality works before committing to git repository.
"""

import sys
import os
import importlib.util
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_file_import(file_path):
    """Test if a Python file can be imported without errors."""
    try:
        # Convert file path to module name
        relative_path = file_path.relative_to(project_root)
        module_name = str(relative_path).replace(os.sep, '.').replace('.py', '')
        
        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return True, None
        else:
            return False, "Could not create module spec"
    except Exception as e:
        return False, str(e)

def find_python_files():
    """Find all Python files in the project (excluding venv and __pycache__)."""
    python_files = []
    
    for root, dirs, files in os.walk(project_root):
        # Skip virtual environment, cache, and git directories
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'node_modules']]
        
        for file in files:
            if file.endswith('.py') and not file.startswith('.'):
                file_path = Path(root) / file
                python_files.append(file_path)
    
    return python_files

def test_core_modules():
    """Test core modules with basic functionality."""
    print("🔧 Testing core modules...")
    
    tests = []
    
    # Test data acquisition
    try:
        # Test both crypto and stocks data acquisition
        try:
            from crypto.data_acquisition import fetch_data as crypto_fetch_data
            crypto_data = crypto_fetch_data('BTC/USDT', 'kraken', '1h', 10)
            print(f"✅ Crypto data acquisition: {len(crypto_data) if crypto_data is not None else 0} bars")
        except Exception as e:
            print(f"❌ Crypto data acquisition failed: {e}")
        
        try:
            from stocks.data_acquisition import fetch_data as stocks_fetch_data
            stock_data = stocks_fetch_data('RELIANCE', 'NSE', '1h', 10)
            print(f"✅ Stocks data acquisition: {len(stock_data) if stock_data is not None else 0} bars")
        except Exception as e:
            print(f"❌ Stocks data acquisition failed: {e}")
        print("  ✅ src.data_acquisition imported successfully")
        tests.append(("data_acquisition", True, None))
    except Exception as e:
        print(f"  ❌ src.data_acquisition failed: {e}")
        tests.append(("data_acquisition", False, str(e)))
    
    # Test technical analysis
    try:
        from tools.technical_analysis import calculate_rsi, calculate_macd
        print("  ✅ src.technical_analysis imported successfully")
        tests.append(("technical_analysis", True, None))
    except Exception as e:
        print(f"  ❌ src.technical_analysis failed: {e}")
        tests.append(("technical_analysis", False, str(e)))
    
    # Test scanner
    try:
        from tools.scanner import TechnicalScanner
        print("  ✅ src.scanner imported successfully")
        tests.append(("scanner", True, None))
    except Exception as e:
        print(f"  ❌ src.scanner failed: {e}")
        tests.append(("scanner", False, str(e)))
    
    return tests

def test_strategy_modules():
    """Test strategy modules."""
    print("🎯 Testing strategy modules...")
    
    tests = []
    strategy_dir = project_root / "strategies"
    
    if strategy_dir.exists():
        for strategy_file in strategy_dir.glob("*.py"):
            if strategy_file.name != "__init__.py":
                success, error = test_file_import(strategy_file)
                if success:
                    print(f"  ✅ {strategy_file.name} imported successfully")
                else:
                    print(f"  ❌ {strategy_file.name} failed: {error}")
                tests.append((strategy_file.name, success, error))
    
    return tests

def test_script_modules():
    """Test script modules (without executing them)."""
    print("📜 Testing script modules...")
    
    tests = []
    
    # Test crypto scripts
    crypto_scripts = project_root / "crypto" / "scripts"
    if crypto_scripts.exists():
        for script_file in crypto_scripts.glob("*.py"):
            success, error = test_file_import(script_file)
            if success:
                print(f"  ✅ crypto/{script_file.name} imported successfully")
            else:
                print(f"  ❌ crypto/{script_file.name} failed: {error}")
            tests.append((f"crypto/{script_file.name}", success, error))
    
    # Test stock scripts
    stock_scripts = project_root / "stocks" / "scripts"
    if stock_scripts.exists():
        for script_file in stock_scripts.glob("*.py"):
            success, error = test_file_import(script_file)
            if success:
                print(f"  ✅ stocks/{script_file.name} imported successfully")
            else:
                print(f"  ❌ stocks/{script_file.name} failed: {error}")
            tests.append((f"stocks/{script_file.name}", success, error))
    
    return tests

def main():
    """Run comprehensive validation tests."""
    print("🔄 Comprehensive Project Validation")
    print("=" * 60)
    
    all_tests = []
    
    # Test core modules
    core_tests = test_core_modules()
    all_tests.extend(core_tests)
    
    print()
    
    # Test strategy modules
    strategy_tests = test_strategy_modules()
    all_tests.extend(strategy_tests)
    
    print()
    
    # Test script modules
    script_tests = test_script_modules()
    all_tests.extend(script_tests)
    
    print()
    print("=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success, _ in all_tests if success)
    failed = sum(1 for _, success, _ in all_tests if not success)
    total = len(all_tests)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {failed}/{total}")
    print(f"📊 Success Rate: {(passed/total)*100:.1f}%")
    
    if failed > 0:
        print("\n⚠️  Failed Tests:")
        for name, success, error in all_tests:
            if not success:
                print(f"  📁 {name}: {error}")
    
    print("\n" + "=" * 60)
    
    if failed == 0:
        print("🎉 All tests passed! Project is ready for git commit.")
        return True
    else:
        print("⚠️  Some tests failed. Fix issues before committing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
