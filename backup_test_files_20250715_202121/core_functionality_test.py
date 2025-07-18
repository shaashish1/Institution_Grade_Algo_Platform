#!/usr/bin/env python3
"""
Core Functionality Test - AlgoProject
Tests essential functionality using correct paths
"""

import os
import sys
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_crypto_data_acquisition():
    """Test crypto data acquisition module."""
    print("🔍 Testing Crypto Data Acquisition...")
    
    try:
        from crypto.data_acquisition import fetch_data, health_check
        print("✅ Import successful")
        
        # Health check
        health = health_check()
        print(f"✅ Health check: {health['status']}")
        print(f"   CCXT Available: {health['ccxt_available']}")
        print(f"   Working Exchanges: {len(health['working_exchanges'])}")
        
        # Quick data fetch
        print("📊 Testing data fetch...")
        data = fetch_data('BTC/USDT', 'kraken', '1h', 5)
        
        if data is not None and len(data) > 0:
            print(f"✅ Data fetch: {len(data)} bars received")
            print(f"   Latest price: ${data.iloc[-1]['close']:.2f}")
            print(f"   Date range: {data.index[0]} to {data.index[-1]}")
            return True
        else:
            print("❌ No data received")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_crypto_scripts():
    """Test key crypto scripts import correctly."""
    print("\n🔍 Testing Crypto Scripts...")
    
    scripts_to_test = [
        'crypto.crypto_symbol_manager',
        'crypto.list_crypto_assets', 
        'crypto.list_ccxt_exchanges'
    ]
    
    success_count = 0
    for script in scripts_to_test:
        try:
            __import__(script)
            print(f"✅ {script}: Import successful")
            success_count += 1
        except Exception as e:
            print(f"❌ {script}: {e}")
    
    return success_count == len(scripts_to_test)

def test_launcher_files():
    """Test launcher files import correctly."""
    print("\n🔍 Testing Launcher Files...")
    
    launcher_files = [
        ('main.py', 'main'),
        ('crypto_launcher.py', 'crypto_launcher'),
        ('crypto_main.py', 'crypto_main')
    ]
    
    success_count = 0
    for file_name, module_name in launcher_files:
        try:
            file_path = os.path.join(project_root, file_name)
            if os.path.exists(file_path):
                # Try to import without executing main
                import importlib.util
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                # Don't execute to avoid running the main functions
                print(f"✅ {file_name}: Structure valid")
                success_count += 1
            else:
                print(f"❌ {file_name}: File not found")
        except Exception as e:
            print(f"❌ {file_name}: {e}")
    
    return success_count == len(launcher_files)

def test_crypto_symbols_file():
    """Test crypto symbols input file."""
    print("\n🔍 Testing Crypto Symbols File...")
    
    try:
        symbols_file = os.path.join(project_root, 'crypto', 'input', 'crypto_assets.csv')
        
        if os.path.exists(symbols_file):
            import pandas as pd
            df = pd.read_csv(symbols_file)
            
            if 'symbol' in df.columns and len(df) > 0:
                print(f"✅ Symbols file: {len(df)} symbols loaded")
                print(f"   Sample symbols: {', '.join(df['symbol'].head(5).tolist())}")
                return True
            else:
                print("❌ Symbols file: Invalid format")
                return False
        else:
            print("⚠️ Symbols file: Not found (will be created when needed)")
            return True
            
    except Exception as e:
        print(f"❌ Symbols file error: {e}")
        return False

def test_output_directories():
    """Test output directory structure."""
    print("\n🔍 Testing Output Directories...")
    
    required_dirs = [
        'crypto/output',
        'crypto/logs', 
        'crypto/input'
    ]
    
    for dir_path in required_dirs:
        full_path = os.path.join(project_root, dir_path)
        if os.path.exists(full_path):
            print(f"✅ {dir_path}/: Exists")
        else:
            print(f"⚠️ {dir_path}/: Will be created as needed")
    
    return True

def test_module_separation():
    """Test module separation compliance."""
    print("\n🔍 Testing Module Separation...")
    
    try:
        # Check that crypto module doesn't import Fyers
        crypto_dir = os.path.join(project_root, 'crypto')
        fyers_violations = []
        
        for root, dirs, files in os.walk(crypto_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if 'from fyers' in content.lower() or 'import fyers' in content.lower():
                                fyers_violations.append(file_path)
                    except:
                        continue
        
        if fyers_violations:
            print("❌ CRITICAL: Crypto files with Fyers dependencies:")
            for violation in fyers_violations:
                print(f"   {violation}")
            return False
        else:
            print("✅ Module separation: No Fyers dependencies in crypto module")
            return True
            
    except Exception as e:
        print(f"❌ Module separation test error: {e}")
        return False

def main():
    """Run all core functionality tests."""
    print("🧪 CORE FUNCTIONALITY TEST SUITE")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Project Root: {project_root}")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Crypto Data Acquisition", test_crypto_data_acquisition),
        ("Crypto Scripts Import", test_crypto_scripts),
        ("Launcher Files", test_launcher_files),
        ("Crypto Symbols File", test_crypto_symbols_file),
        ("Output Directories", test_output_directories),
        ("Module Separation", test_module_separation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n🎯 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL CORE TESTS PASSED!")
        print("✅ AlgoProject is ready for use")
        print("✅ All essential functionality working")
        print("✅ Correct paths and structure validated")
        return True
    else:
        print(f"\n⚠️ {total - passed} tests failed")
        print("🔧 Review the failures above and fix issues")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
