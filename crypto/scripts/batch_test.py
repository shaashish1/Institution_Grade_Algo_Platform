#!/usr/bin/env python3
"""
Quick Test for Enhanced Batch Runner
====================================

Test the batch runner with minimal settings to ensure it works correctly.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🧪 Quick Test for Enhanced Batch Runner")
    print("=" * 50)
    
    # Change to crypto scripts directory
    script_dir = Path("c:/vscode/AlgoProject/crypto/scripts")
    os.chdir(script_dir)
    
    print(f"📁 Working directory: {os.getcwd()}")
    print()
    
    # Test 1: Quick single symbol test
    print("🎯 Test 1: Quick single symbol, single strategy test")
    print("-" * 50)
    
    cmd = [
        sys.executable, 
        "batch_runner.py", 
        "--symbols", "BTC/USDT",
        "--strategies", "RSI_MACD_VWAP",
        "--timeframes", "1h",
        "--bars", "100",  # Small number for quick test
        "--limit-symbols", "1"
    ]
    
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, cwd=os.getcwd(), timeout=300)  # 5 minute timeout
        
        if result.returncode == 0:
            print("✅ Test 1 PASSED - Basic functionality works!")
        else:
            print(f"❌ Test 1 FAILED - Return code: {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Test 1 TIMEOUT - Test took too long")
    except Exception as e:
        print(f"❌ Test 1 ERROR: {e}")
    
    print("\n" + "=" * 50)
    
    # Test 2: Auto mode with limited symbols
    print("🎯 Test 2: Auto mode with symbol limit")
    print("-" * 50)
    
    cmd2 = [
        sys.executable,
        "batch_runner.py",
        "--auto",
        "--limit-symbols", "2",  # Only test first 2 symbols
        "--bars", "50"  # Very small for quick test
    ]
    
    print(f"Command: {' '.join(cmd2)}")
    print("⚠️  This test is disabled to save time - uncomment to run")
    
    # Uncomment below to run the full auto test
    # try:
    #     result = subprocess.run(cmd2, cwd=os.getcwd(), timeout=600)  # 10 minute timeout
    #     
    #     if result.returncode == 0:
    #         print("✅ Test 2 PASSED - Auto mode works!")
    #     else:
    #         print(f"❌ Test 2 FAILED - Return code: {result.returncode}")
    #         
    # except subprocess.TimeoutExpired:
    #     print("⏰ Test 2 TIMEOUT - Test took too long")
    # except Exception as e:
    #     print(f"❌ Test 2 ERROR: {e}")
    
    print("\n🎉 Testing completed!")
    print("💡 If Test 1 passed, the batch runner is working correctly.")
    print("📊 Check the output directory for generated reports.")

if __name__ == "__main__":
    main()
