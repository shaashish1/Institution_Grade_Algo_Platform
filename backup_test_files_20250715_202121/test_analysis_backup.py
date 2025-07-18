#!/usr/bin/env python3
"""
Test Files Analysis and Backup Report
Creating backup and analysis of all existing test files before consolidation
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

def analyze_test_files():
    """Analyze all test files and create summary."""
    
    project_root = Path("D:/AlgoProject")
    helper_scripts = project_root / "helper_scripts"
    
    # Test files to analyze
    test_files = [
        "comprehensive_test.py",
        "comprehensive_test_suite.py", 
        "core_functionality_test.py",
        "crypto_file_test.py",
        "crypto_test_suite.py",
        "diagnostic_test.py",
        "quick_clean_test.py",
        "quick_clean_test_from_utils.py",
        "quick_crypto_test.py",
        "quick_test.py",
        "quick_test_from_utils.py",
        "simple_import_test.py",
        "test_advanced_strategies.py",
        "test_backtest.py",
        "test_comprehensive_validation.py",
        "test_limited_backtest.py",
        "test_runner.py"
    ]
    
    print("📋 TEST FILES ANALYSIS REPORT")
    print("=" * 60)
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Test Files Found: {len(test_files)}")
    
    # Categorize by functionality
    categories = {
        "🔧 Core Infrastructure Tests": [
            "core_functionality_test.py",
            "comprehensive_test_suite.py",
            "diagnostic_test.py",
            "system_validation.py"
        ],
        "🪙 Crypto-Specific Tests": [
            "crypto_file_test.py", 
            "crypto_test_suite.py",
            "quick_crypto_test.py"
        ],
        "⚡ Quick Validation Tests": [
            "quick_test.py",
            "quick_clean_test.py",
            "simple_import_test.py"
        ],
        "📊 Backtest & Strategy Tests": [
            "test_backtest.py",
            "test_advanced_strategies.py", 
            "test_limited_backtest.py"
        ],
        "🔄 Test Infrastructure": [
            "test_runner.py",
            "comprehensive_test.py",
            "test_comprehensive_validation.py"
        ],
        "📑 Duplicate/Legacy Files": [
            "quick_clean_test_from_utils.py",
            "quick_test_from_utils.py"
        ]
    }
    
    for category, files in categories.items():
        print(f"\n{category}")
        print("-" * 50)
        for file in files:
            file_path = helper_scripts / file
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  ✅ {file} ({size} bytes)")
            else:
                print(f"  ❌ {file} (missing)")
    
    return test_files

def create_backup():
    """Create backup of all test files."""
    
    project_root = Path("D:/AlgoProject")
    helper_scripts = project_root / "helper_scripts"
    
    # Create backup directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = project_root / f"backup_test_files_{timestamp}"
    backup_dir.mkdir(exist_ok=True)
    
    print(f"\n💾 CREATING BACKUP")
    print("=" * 60)
    print(f"Backup Location: {backup_dir}")
    
    backed_up = 0
    for file_path in helper_scripts.glob("*test*.py"):
        if file_path.is_file():
            backup_path = backup_dir / file_path.name
            shutil.copy2(file_path, backup_path)
            print(f"  ✅ Backed up: {file_path.name}")
            backed_up += 1
    
    print(f"\n📊 Backup Summary: {backed_up} files backed up")
    return backup_dir

def main():
    """Main analysis function."""
    print("🔍 ALGOPROJECT TEST FILES ANALYSIS")
    print("=" * 70)
    
    # Analyze current test files
    test_files = analyze_test_files()
    
    # Create backup
    backup_dir = create_backup()
    
    print(f"\n🎯 NEXT STEPS")
    print("=" * 60)
    print("1. Create crypto_app_testing.py - Comprehensive crypto testing")
    print("2. Create stocks_app_testing.py - Comprehensive stocks testing") 
    print("3. Remove duplicate and legacy test files")
    print("4. Remove unnecessary .bat files")
    print("5. Update all logging to helper_scripts/logs/")
    
    print(f"\n✅ ANALYSIS COMPLETE")
    print(f"📁 Backup created at: {backup_dir}")

if __name__ == "__main__":
    main()
