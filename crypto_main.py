#!/usr/bin/env python3
"""
AlgoProject - Direct Crypto Trading Main Script
==============================================

Direct entry point for crypto trading functionality.
This is a simplified version of crypto_launcher.py for direct execution.
"""

import os
import sys
import json
from datetime import datetime

def main():
    """Main crypto trading entry point"""
    print("🚀 AlgoProject - Crypto Trading Main")
    print("=" * 40)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("crypto"):
        print("❌ Error: crypto folder not found!")
        print("💡 Make sure you're running this from the AlgoProject root directory")
        return
    
    print("🔍 Available Crypto Trading Options:")
    print("-" * 40)
    print("1. Use crypto_launcher.py for full interactive menu")
    print("2. Run crypto/scripts/ modules directly")
    print("3. Access trading_launcher.py for unified platform")
    print()
    
    # System health check
    print("🔧 Quick System Check:")
    print("-" * 20)
    
    try:
        import ccxt
        print(f"✅ CCXT library: OK (v{ccxt.__version__})")
    except ImportError:
        print("❌ CCXT library: Missing")
        print("💡 Run with virtual environment: .\\venv\\Scripts\\python.exe crypto_main.py")
        print("💡 Or use: .\\launch_crypto.bat")
    
    try:
        import pandas as pd
        print("✅ Pandas library: OK")
    except ImportError:
        print("❌ Pandas library: Missing")
    
    try:
        import numpy as np
        print("✅ NumPy library: OK")
    except ImportError:
        print("❌ NumPy library: Missing")
    
    # Check directories
    crypto_dirs = ["crypto/input", "crypto/output", "crypto/logs", "crypto/scripts"]
    for dir_path in crypto_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/: OK")
        else:
            print(f"❌ {dir_path}/: Missing")
    
    print()
    print("🚀 To start crypto trading:")
    print("   venv\\Scripts\\python.exe crypto_launcher.py")
    print()
    print("📊 To run a crypto backtest:")
    print("   venv\\Scripts\\python.exe crypto/scripts/enhanced_crypto_backtest.py")
    print()
    print("📈 For live trading:")
    print("   venv\\Scripts\\python.exe crypto/scripts/crypto_demo_live.py")
    print()

if __name__ == "__main__":
    main()
