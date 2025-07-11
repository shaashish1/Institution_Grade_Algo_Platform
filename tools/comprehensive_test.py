#!/usr/bin/env python3
"""
Comprehensive Project Testing Script
===================================

Tests all major components of the AlgoProject to ensure everything is working correctly.
"""

import os
import sys
import importlib
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent if __file__ else Path.cwd()
sys.path.insert(0, str(project_root))

def test_module_import(module_name, description=""):
    """Test if a module can be imported successfully."""
    try:
        module = importlib.import_module(module_name)
        print(f"✅ {module_name} - {description}")
        return True, module
    except Exception as e:
        print(f"❌ {module_name} - {description}: {str(e)}")
        return False, None

def test_function_availability(module, function_name):
    """Test if a function is available in a module."""
    try:
        func = getattr(module, function_name)
        if callable(func):
            print(f"  ├─ ✅ {function_name}() function available")
            return True
        else:
            print(f"  ├─ ❌ {function_name} exists but not callable")
            return False
    except AttributeError:
        print(f"  ├─ ❌ {function_name}() function not found")
        return False

def test_file_execution(script_path, description=""):
    """Test if a Python script can be compiled."""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            print(f"⚠️  {script_path} - {description}: Empty file")
            return False
        
        compile(content, script_path, 'exec')
        print(f"✅ {script_path} - {description}: Compiles successfully")
        return True
    except Exception as e:
        print(f"❌ {script_path} - {description}: {str(e)}")
        return False

def main():
    """Run comprehensive project testing."""
    print("🔍 AlgoProject Comprehensive Testing")
    print("=" * 60)
    
    # Test core modules
    print("\n📦 CORE MODULE IMPORTS")
    print("-" * 30)
    
    core_modules = [
        ("tools.data_acquisition", "Data fetching and management"),
        ("tools.technical_analysis", "Technical indicators"),
        ("tools.scanner", "Market scanning utilities"),
        ("strategies.VWAPSigma2Strategy", "Main trading strategy"),
        ("strategies.ml_ai_framework", "ML trading framework"),
        ("stocks.fyers_data_provider", "Stock data provider"),
    ]
    
    passed_imports = 0
    total_imports = len(core_modules)
    
    for module_name, description in core_modules:
        success, module = test_module_import(module_name, description)
        if success:
            passed_imports += 1
            
            # Test specific functions for key modules
            if module_name == "tools.data_acquisition":
                test_function_availability(module, "fetch_data")
            elif module_name == "tools.technical_analysis":
                test_function_availability(module, "calculate_rsi")
                test_function_availability(module, "calculate_macd")
            elif module_name == "strategies.VWAPSigma2Strategy":
                test_function_availability(module, "VWAPSigma2Strategy")
    
    print(f"\n📊 Import Results: {passed_imports}/{total_imports} ({(passed_imports/total_imports)*100:.1f}%)")
    
    # Test script compilation
    print("\n🔧 SCRIPT COMPILATION TESTS")
    print("-" * 30)
    
    script_tests = [
        ("tools/launcher.py", "Main launcher"),
        ("tools/backtest_runner.py", "Universal backtest runner"),
        ("tools/realtime_trader.py", "Real-time trading framework"),
        ("tools/system_verification.py", "System health checker"),
        ("crypto/scripts/crypto_demo_live.py", "Crypto demo trading"),
        ("crypto/scripts/crypto_backtest.py", "Crypto backtesting"),
        ("stocks/scripts/stocks_backtest.py", "Stock backtesting"),
        ("stocks/scripts/stocks_demo_live.py", "Stock demo trading"),
    ]
    
    passed_scripts = 0
    total_scripts = len(script_tests)
    
    for script_path, description in script_tests:
        if os.path.exists(script_path):
            success = test_file_execution(script_path, description)
            if success:
                passed_scripts += 1
        else:
            print(f"❌ {script_path} - {description}: File not found")
    
    print(f"\n📊 Script Results: {passed_scripts}/{total_scripts} ({(passed_scripts/total_scripts)*100:.1f}%)")
    
    # Test strategy files
    print("\n🎯 STRATEGY FILE TESTS")
    print("-" * 30)
    
    strategy_dir = "strategies"
    if os.path.exists(strategy_dir):
        strategy_files = [f for f in os.listdir(strategy_dir) if f.endswith('.py') and f != '__init__.py']
        passed_strategies = 0
        
        for strategy_file in strategy_files:
            strategy_path = os.path.join(strategy_dir, strategy_file)
            success = test_file_execution(strategy_path, f"Strategy: {strategy_file}")
            if success:
                passed_strategies += 1
        
        print(f"\n📊 Strategy Results: {passed_strategies}/{len(strategy_files)} ({(passed_strategies/len(strategy_files))*100:.1f}%)")
    else:
        print("❌ Strategies directory not found")
    
    # Overall summary
    print("\n📋 OVERALL SYSTEM HEALTH")
    print("=" * 40)
    
    total_tests = total_imports + total_scripts + len(strategy_files)
    total_passed = passed_imports + passed_scripts + passed_strategies
    overall_health = (total_passed / total_tests) * 100
    
    if overall_health >= 90:
        status = "🎉 EXCELLENT"
        color = "GREEN"
    elif overall_health >= 75:
        status = "✅ GOOD"
        color = "YELLOW"
    elif overall_health >= 50:
        status = "⚠️  NEEDS ATTENTION"
        color = "ORANGE"
    else:
        status = "❌ CRITICAL"
        color = "RED"
    
    print(f"Overall Health: {overall_health:.1f}% - {status}")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    
    if overall_health >= 75:
        print("\n🚀 SYSTEM READY FOR USE!")
        print("💡 Next steps:")
        print("   • Run: python tools/launcher.py")
        print("   • Try: python tools/backtest_runner.py --help")
        print("   • Test: python tools/realtime_trader.py --help")
    else:
        print("\n⚠️  SYSTEM NEEDS FIXES!")
        print("🔧 Recommended actions:")
        print("   • Check failed imports and fix missing dependencies")
        print("   • Verify file paths and project structure")
        print("   • Run: python tools/system_verification.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        traceback.print_exc()
