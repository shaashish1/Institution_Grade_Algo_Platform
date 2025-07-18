#!/usr/bin/env python3
"""
Test Runner for D:\AlgoProject\tests\ directory
Runs all tests and validates they work correctly
"""

import os
import sys
import subprocess
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def run_test_file(test_file_path):
    """Run a single test file and capture results."""
    try:
        # Use the virtual environment Python
        venv_python = os.path.join(project_root, 'venv', 'Scripts', 'python.exe')
        
        print(f"🔍 Running {os.path.basename(test_file_path)}...")
        
        # Run the test with timeout
        result = subprocess.run(
            [venv_python, test_file_path],
            capture_output=True,
            text=True,
            timeout=120,  # 2 minute timeout
            cwd=project_root
        )
        
        if result.returncode == 0:
            print(f"✅ {os.path.basename(test_file_path)}: PASSED")
            if result.stdout:
                # Show last few lines of output
                lines = result.stdout.strip().split('\n')
                if len(lines) > 5:
                    print(f"   Output (last 3 lines):")
                    for line in lines[-3:]:
                        print(f"   {line}")
                else:
                    print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {os.path.basename(test_file_path)}: FAILED")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}...")
            if result.stdout:
                print(f"   Output: {result.stdout[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {os.path.basename(test_file_path)}: TIMEOUT (>2 minutes)")
        return False
    except Exception as e:
        print(f"❌ {os.path.basename(test_file_path)}: ERROR - {e}")
        return False

def main():
    """Run all tests in tests/ directory."""
    print("🧪 ALGOPROJECT TESTS VALIDATION")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Project Root: {project_root}")
    print("=" * 60)
    
    # Find all test files
    tests_dir = os.path.join(project_root, 'tests')
    
    if not os.path.exists(tests_dir):
        print("❌ Tests directory not found!")
        return False
    
    test_files = []
    for file_name in os.listdir(tests_dir):
        if file_name.endswith('.py') and file_name != '__init__.py':
            test_files.append(os.path.join(tests_dir, file_name))
    
    if not test_files:
        print("⚠️ No test files found in tests/ directory")
        return True
    
    print(f"📊 Found {len(test_files)} test files:")
    for test_file in test_files:
        print(f"   • {os.path.basename(test_file)}")
    
    print(f"\n🚀 RUNNING TESTS")
    print("-" * 40)
    
    # Run each test
    results = []
    for test_file in test_files:
        success = run_test_file(test_file)
        results.append((os.path.basename(test_file), success))
        print()  # Empty line between tests
    
    # Summary
    print(f"📋 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Overall Results:")
    print(f"   Total Tests: {total}")
    print(f"   Passed: {passed}")
    print(f"   Failed: {total - passed}")
    print(f"   Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED!")
        print("✅ All files in tests/ directory working correctly")
        print("✅ Using correct paths and project structure")
        return True
    else:
        print(f"\n⚠️ {total - passed} tests failed")
        print("🔧 Review the failures above")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
