#!/usr/bin/env python3
"""
Basic System Validation Report
Checks if all key files and modules are in place and importable
"""

import sys
import os
from pathlib import Path

def validate_project_structure():
    """Validate the basic project structure is in place."""
    project_root = Path("D:/AlgoProject")
    
    print("🔍 PROJECT STRUCTURE VALIDATION")
    print("=" * 50)
    
    # Key directories that should exist (per coding_rules.md)
    required_dirs = [
        "crypto",
        "stocks", 
        "strategies",
        "utils",
        "docs",
        "helper_scripts",
        "venv"
    ]
    
    print("\n📁 Directory Structure:")
    all_dirs_exist = True
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        exists = dir_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {dir_name}")
        if not exists:
            all_dirs_exist = False
    
    # Key files that should exist (per coding_rules.md)
    key_files = [
        "crypto/data_acquisition.py",
        "strategies/ml_ai_framework.py", 
        "strategies/market_inefficiency_strategy.py",
        "strategies/advanced_strategy_hub.py",
        "tests/diagnostic_test.py",
        "helper_scripts/comprehensive_test_suite.py",
        "docs/coding_rules.md",
        "main.py",
        "crypto_launcher.py",
        "crypto_main.py"
    ]
    
    print("\n📄 Key Files:")
    all_files_exist = True
    for file_path in key_files:
        full_path = project_root / file_path
        exists = full_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
        if not exists:
            all_files_exist = False
    
    # Python environment check
    print("\n🐍 Python Environment:")
    venv_python = project_root / "venv/Scripts/python.exe"
    venv_exists = venv_python.exists()
    status = "✅" if venv_exists else "❌"
    print(f"  {status} Virtual Environment: {venv_python}")
    
    return all_dirs_exist and all_files_exist and venv_exists

def test_basic_imports():
    """Test if basic imports work without errors."""
    print("\n🔧 BASIC IMPORT TESTING")
    print("=" * 50)
    
    # Add project root to Python path
    sys.path.insert(0, "D:/AlgoProject")
    
    import_tests = [
        ("crypto.data_acquisition", "fetch_data"),
        ("strategies.ml_ai_framework", "MLAITradingFramework"),
        ("strategies.market_inefficiency_strategy", "MarketInefficiencyStrategy"),
        ("strategies.advanced_strategy_hub", "AdvancedStrategyHub")
    ]
    
    passed = 0
    total = len(import_tests)
    
    for module_name, class_name in import_tests:
        try:
            module = __import__(module_name, fromlist=[class_name])
            class_obj = getattr(module, class_name)
            print(f"  ✅ {module_name}.{class_name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {module_name}.{class_name}: {str(e)[:50]}...")
    
    print(f"\n📊 Import Results: {passed}/{total} passed")
    return passed == total

def main():
    """Run complete validation."""
    print("🚀 ALGOPROJECT SYSTEM VALIDATION")
    print("=" * 60)
    
    # Structure validation
    structure_ok = validate_project_structure()
    
    # Import validation  
    imports_ok = test_basic_imports()
    
    # Final summary
    print("\n🎯 VALIDATION SUMMARY")
    print("=" * 50)
    
    structure_status = "✅ PASS" if structure_ok else "❌ FAIL"
    imports_status = "✅ PASS" if imports_ok else "❌ FAIL"
    
    print(f"📁 Project Structure: {structure_status}")
    print(f"🔧 Module Imports: {imports_status}")
    
    if structure_ok and imports_ok:
        print("\n🎉 ALL SYSTEMS OPERATIONAL!")
        print("✅ Ready for production backtesting")
    else:
        print("\n⚠️  ISSUES DETECTED")
        print("❌ Some components need attention")

if __name__ == "__main__":
    main()
