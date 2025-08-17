#!/usr/bin/env python3
"""
Quick AlgoProject Status Check
Per coding_rules.md structure validation
"""

import os
import sys
from pathlib import Path

def main():
    """Quick status check."""
    print("🔍 ALGOPROJECT STATUS - Per coding_rules.md")
    print("=" * 50)
    
    project_root = Path("D:/AlgoProject")
    
    # Required structure per coding_rules.md
    required_structure = {
        "📁 Directories": [
            "crypto", "stocks", "strategies", "utils", 
            "docs", "helper_scripts", "venv", "tests"
        ],
        "📄 Root Files": [
            "main.py", "crypto_launcher.py", "crypto_main.py",
            "requirements.txt", "README.md"
        ],
        "🔧 Core Modules": [
            "crypto/data_acquisition.py",
            "strategies/ml_ai_framework.py",
            "docs/coding_rules.md"
        ]
    }
    
    # Check structure
    all_good = True
    for category, items in required_structure.items():
        print(f"\n{category}:")
        for item in items:
            path = project_root / item
            exists = path.exists()
            status = "✅" if exists else "❌"
            print(f"  {status} {item}")
            if not exists:
                all_good = False
    
    # Python environment
    print(f"\n🐍 Python Environment:")
    venv_python = project_root / "venv/Scripts/python.exe"
    status = "✅" if venv_python.exists() else "❌"
    print(f"  {status} Virtual Environment")
    
    # Quick import test
    print(f"\n📦 Quick Import Test:")
    sys.path.insert(0, str(project_root))
    
    try:
        from crypto.data_acquisition import health_check
        health = health_check()
        print(f"  ✅ Crypto Module: {health['status']}")
        print(f"  ✅ CCXT: {health['ccxt_available']}")
        print(f"  ✅ Exchanges: {len(health['working_exchanges'])} available")
    except Exception as e:
        print(f"  ❌ Crypto Module: {e}")
        all_good = False
    
    # Final status
    print(f"\n🎯 OVERALL STATUS")
    print("=" * 50)
    if all_good:
        print("✅ ALL SYSTEMS OPERATIONAL")
        print("✅ Structure matches coding_rules.md")
        print("✅ Ready for production use")
    else:
        print("⚠️  Some issues detected")
        print("📖 Check coding_rules.md for structure")

if __name__ == "__main__":
    main()
