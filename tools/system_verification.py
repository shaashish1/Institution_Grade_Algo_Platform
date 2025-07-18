#!/usr/bin/env python3
"""
AlgoProject System Verification Script
Comprehensive testing of all components and configurations
"""

import os
import sys
import importlib.util
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_section(title):
    print(f"\n📋 {title}")
    print("-" * 40)

def test_imports():
    """Test all critical module imports"""
    print_section("Testing Module Imports")
    
    # Add project root to path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(project_root / 'strategies'))
    sys.path.insert(0, str(project_root / 'tools'))
    
    import_tests = [
        # Core strategies
        ("strategies.VWAPSigma2Strategy", "VWAPSigma2Strategy"),
        ("strategies.ml_ai_framework", "MLAITradingFramework"),
        ("strategies.market_inefficiency_strategy", "MarketInefficiencyStrategy"),
        
        # Core modules
        ("crypto.data_acquisition", "fetch_data"),
        ("stocks.data_acquisition", "fetch_data"),
        ("tools.technical_analysis", None),
        ("tools.scanner", None),
        
        # Data providers
        ("stocks.fyers_data_provider", "FyersDataProvider"),
    ]
    
    passed = 0
    total = len(import_tests)
    
    for module_name, class_name in import_tests:
        try:
            module = importlib.import_module(module_name)
            if class_name:
                getattr(module, class_name)
            print(f"✅ {module_name} - OK")
            passed += 1
        except ImportError as e:
            print(f"❌ {module_name} - FAILED: {e}")
        except AttributeError as e:
            print(f"⚠️  {module_name} - Class {class_name} not found: {e}")
    
    print(f"\n📊 Import Test Results: {passed}/{total} passed ({passed/total*100:.1f}%)")
    return passed == total

def test_file_structure():
    """Test if all required files and folders exist"""
    print_section("Testing File Structure")
    
    project_root = Path(__file__).parent.parent
    
    required_structure = {
        "📁 Folders": [
            "strategies",
            "crypto/input", 
            "crypto/scripts",
            "crypto/output",
            "crypto/logs",
            "crypto/tools",
            "stocks/input",
            "stocks/scripts", 
            "stocks/output",
            "stocks/logs",
            "stocks/fyers",
            "tests",
            "tools",
            "docs"
        ],
        "📄 Core Files": [
            "strategies/VWAPSigma2Strategy.py",
            "tools/data_acquisition.py",
            "crypto/input/crypto_assets.csv",
            "stocks/input/stocks_assets.csv",
            "stocks/fyers/access_token.py",
            "tools/launcher.py",
            "requirements.txt",
            "README.md"
        ],
        "📝 Documentation": [
            "docs/GETTING_STARTED.md",
            "docs/PROJECT_STRUCTURE.md"
        ]
    }
    
    all_passed = True
    
    for category, items in required_structure.items():
        print(f"\n{category}:")
        for item in items:
            path = project_root / item
            if path.exists():
                print(f"  ✅ {item}")
            else:
                print(f"  ❌ {item} - MISSING")
                all_passed = False
    
    return all_passed

def test_configurations():
    """Test configuration files"""
    print_section("Testing Configurations")
    
    project_root = Path(__file__).parent.parent
    
    config_files = [
        ("crypto/input/crypto_assets.csv", "Crypto assets list"),
        ("stocks/input/stocks_assets.csv", "Stock assets list"),
        ("stocks/fyers/access_token.py", "Fyers credentials"),
        ("requirements.txt", "Python dependencies")
    ]
    
    all_passed = True
    
    for file_path, description in config_files:
        path = project_root / file_path
        if path.exists():
            try:
                if file_path.endswith('.csv'):
                    # Test CSV file
                    with open(path, 'r') as f:
                        lines = len(f.readlines())
                    print(f"  ✅ {description}: {lines} lines")
                elif file_path.endswith('.py'):
                    # Test Python file
                    with open(path, 'r') as f:
                        content = f.read()
                    if len(content.strip()) > 0:
                        print(f"  ✅ {description}: {len(content)} characters")
                    else:
                        print(f"  ⚠️  {description}: Empty file")
                        all_passed = False
                else:
                    print(f"  ✅ {description}: Exists")
            except Exception as e:
                print(f"  ❌ {description}: Error reading - {e}")
                all_passed = False
        else:
            print(f"  ❌ {description}: Missing")
            all_passed = False
    
    return all_passed

def test_script_execution():
    """Test if main scripts can be executed"""
    print_section("Testing Script Execution Readiness")
    
    project_root = Path(__file__).parent.parent
    
    scripts_to_test = [
        ("tests/diagnostic_test.py", "Diagnostic test"),
        ("tools/launcher.py", "Main launcher"),
        ("crypto/scripts/crypto_backtest.py", "Crypto backtest"),
        ("stocks/scripts/stocks_backtest.py", "Stock backtest"),
    ]
    
    all_passed = True
    
    for script_path, description in scripts_to_test:
        path = project_root / script_path
        if path.exists():
            # Check if script has proper shebang or main block
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            has_main = '__main__' in content
            has_functions = 'def ' in content
            has_imports = 'import ' in content
            
            # For diagnostic test, just check if it has imports and prints
            if script_path == "tests/diagnostic_test.py":
                if has_imports and 'print(' in content:
                    print(f"  ✅ {description}: Ready to execute")
                else:
                    print(f"  ⚠️  {description}: May have execution issues")
                    all_passed = False
            elif has_main and has_functions:
                print(f"  ✅ {description}: Ready to execute")
            else:
                print(f"  ⚠️  {description}: May have execution issues")
                all_passed = False
        else:
            print(f"  ❌ {description}: Missing")
            all_passed = False
    
    return all_passed

def generate_summary():
    """Generate summary and recommendations"""
    print_section("System Summary & Recommendations")
    
    # Run all tests
    import_ok = test_imports()
    structure_ok = test_file_structure()
    config_ok = test_configurations()
    script_ok = test_script_execution()
    
    total_score = sum([import_ok, structure_ok, config_ok, script_ok])
    
    print(f"\n📊 Overall System Health: {total_score}/4 components passed")
    
    if total_score == 4:
        print("\n🎉 EXCELLENT! System is fully ready for use")
        print("✅ All components verified successfully")
        print("\n🚀 Next Steps:")
        print("   1. Run: python tools/launcher.py")
        print("   2. Try crypto backtesting")
        print("   3. Configure Fyers credentials for stocks")
        print("   4. Read docs/GETTING_STARTED.md for detailed instructions")
        
    elif total_score >= 3:
        print("\n✅ GOOD! System is mostly ready")
        print("⚠️  Minor issues detected - see details above")
        print("\n🔧 Recommended Actions:")
        print("   1. Fix any missing files")
        print("   2. Test individual components")
        print("   3. Check docs/TROUBLESHOOTING.md")
        
    elif total_score >= 2:
        print("\n⚠️  CAUTION! System has significant issues")
        print("❌ Multiple components need attention")
        print("\n🔧 Required Actions:")
        print("   1. Fix all missing files")
        print("   2. Reinstall dependencies: pip install -r requirements.txt")
        print("   3. Check project structure")
        
    else:
        print("\n❌ CRITICAL! System not ready for use")
        print("🚨 Major components missing or broken")
        print("\n🆘 Emergency Actions:")
        print("   1. Verify project download/clone")
        print("   2. Run setup.bat (Windows) or setup.sh (Linux/Mac)")
        print("   3. Check Python environment")
        print("   4. Reinstall all dependencies")

def main():
    """Main verification function"""
    print_header("AlgoProject System Verification")
    print("🔍 Comprehensive testing of all components")
    print("⏱️  This may take a few moments...")
    
    try:
        # Test all components
        test_imports()
        test_file_structure() 
        test_configurations()
        test_script_execution()
        
        # Generate summary
        generate_summary()
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR during verification: {e}")
        print("🆘 Please check your Python environment and project setup")
        
    print(f"\n{'='*60}")
    print("🏁 Verification Complete")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
