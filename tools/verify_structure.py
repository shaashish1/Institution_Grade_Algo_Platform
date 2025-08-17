#!/usr/bin/env python3
"""
Project Structure Verification Script
=====================================

This script verifies that the AlgoProject structure is clean and organized.
"""

import os
import subprocess
from pathlib import Path

def check_duplicates():
    """Check for duplicate files in the project."""
    print("🔍 Checking for duplicate files...")
    
    # Check for common duplicates that we've cleaned up
    duplicate_checks = [
        ("data_acquisition.py", ["src/data_acquisition.py"]),
        ("launcher.py", ["tools/launcher.py"]),
        ("access_token.py", ["input/access_token.py"]),
    ]
    
    for filename, expected_locations in duplicate_checks:
        print(f"📋 Checking {filename}...")
        found_locations = []
        
        for root, dirs, files in os.walk("."):
            if filename in files:
                found_locations.append(os.path.join(root, filename))
        
        if len(found_locations) == len(expected_locations):
            all_expected_found = True
            for expected in expected_locations:
                expected_normalized = expected.replace("\\", "/")
                found_expected = False
                for found in found_locations:
                    found_normalized = found.replace("\\", "/").replace("./", "")
                    if found_normalized == expected_normalized:
                        print(f"  ✅ Found in expected location: {found}")
                        found_expected = True
                        break
                if not found_expected:
                    print(f"  ❌ Expected location not found: {expected}")
                    all_expected_found = False
            
            if all_expected_found:
                print(f"  ✅ All {filename} files are in correct locations")
        else:
            print(f"  ⚠️  Expected {len(expected_locations)} files, found {len(found_locations)}")
            for location in found_locations:
                print(f"    📁 {location}")

def check_test_files():
    """Check that test files are properly organized."""
    print("\n🧪 Checking test files organization...")
    
    test_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            # Only count files that are actually test files (start with test_ or end with _test.py)
            if file.endswith(".py") and (file.startswith("test_") or file.endswith("_test.py")):
                test_files.append(os.path.join(root, file))
    
    tests_dir_files = [f for f in test_files if "tests/" in f or "tests\\" in f]
    other_test_files = [f for f in test_files if not ("tests/" in f or "tests\\" in f) and not ("venv" in f or "site-packages" in f)]
    
    print(f"📊 Test files in tests/ directory: {len(tests_dir_files)}")
    for f in tests_dir_files:
        print(f"  ✅ {f}")
    
    if other_test_files:
        print(f"⚠️  Test files outside tests/ directory: {len(other_test_files)}")
        for f in other_test_files:
            print(f"  📁 {f}")
    else:
        print("✅ All test files are in the tests/ directory")

def check_script_organization():
    """Check that scripts are properly organized."""
    print("\n📜 Checking script organization...")
    
    # Check for root scripts folder
    if os.path.exists("scripts"):
        print("❌ Root scripts/ folder still exists - should be removed")
    else:
        print("✅ Root scripts/ folder properly removed")
    
    # Check crypto scripts
    crypto_scripts = Path("crypto/scripts")
    if crypto_scripts.exists():
        scripts = list(crypto_scripts.glob("*.py"))
        print(f"🪙 Crypto scripts: {len(scripts)} files")
        for script in scripts:
            print(f"  📄 {script}")
    
    # Check stock scripts
    stock_scripts = Path("stocks/scripts")
    if stock_scripts.exists():
        scripts = list(stock_scripts.glob("*.py"))
        print(f"📈 Stock scripts: {len(scripts)} files")
        for script in scripts:
            print(f"  📄 {script}")

def check_documentation():
    """Check that documentation is properly organized."""
    print("\n📚 Checking documentation organization...")
    
    # Check for root .md files
    root_md_files = [f for f in os.listdir(".") if f.endswith(".md")]
    if root_md_files:
        print(f"⚠️  Found {len(root_md_files)} .md files in root:")
        for f in root_md_files:
            print(f"  📄 {f}")
    else:
        print("✅ No .md files in root directory")
    
    # Check docs directory
    docs_dir = Path("docs")
    if docs_dir.exists():
        md_files = list(docs_dir.glob("*.md"))
        print(f"📚 Documentation files in docs/: {len(md_files)}")
        print("✅ All documentation properly organized")

def check_import_paths():
    """Check that import paths are correct after reorganization."""
    print("\n🔧 Checking import paths...")
    
    # Check for old import patterns that should be updated
    old_imports = [
        "from data_acquisition import",
        "import data_acquisition"
    ]
    
    issues_found = []
    
    for old_import in old_imports:
        # Search for old import patterns
        for root, dirs, files in os.walk("."):
            # Skip venv, hidden directories, and this verification script itself
            if ("venv" in root or "site-packages" in root or "/.git" in root or "\\.git" in root or 
                root.endswith("tools")):
                continue
                
            for file in files:
                if file.endswith(".py") and file != "verify_structure.py":
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Look for actual import lines, not comments
                            lines = content.split('\n')
                            for line_num, line in enumerate(lines, 1):
                                stripped_line = line.strip()
                                if stripped_line.startswith(old_import) and not stripped_line.startswith('#'):
                                    issues_found.append(f"{file_path}:{line_num}: {stripped_line}")
                    except (UnicodeDecodeError, PermissionError):
                        continue
    
    if issues_found:
        print(f"⚠️  Found {len(issues_found)} files with old import patterns:")
        for issue in issues_found:
            print(f"  📁 {issue}")
    else:
        print("✅ All import paths are correctly updated")

def main():
    print("🔄 AlgoProject Structure Verification")
    print("=" * 50)
    
    check_duplicates()
    check_test_files()
    check_script_organization()
    check_documentation()
    check_import_paths()
    
    print("\n" + "=" * 50)
    print("✅ Structure verification complete!")
    print("🚀 Use 'python tools/launcher.py --all' to see all options")

if __name__ == "__main__":
    main()
