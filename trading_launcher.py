#!/usr/bin/env python3
"""
Unified Trading Platform Launcher
=================================

Main launcher for both crypto and stock trading platforms.
Optimized for personal laptops with full functionality.
"""

import os
import sys
import json
from datetime import datetime

def print_banner():
    print("🚀 AlgoProject - Unified Trading Platform")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🏠 Personal Laptop Edition - Full Functionality!")
    print()
    print("💰 Crypto Trading: 100+ exchanges via CCXT")
    print("📈 Stock Trading: NSE/BSE via Fyers API")
    print("=" * 60)

def check_prerequisites():
    """Check if all required directories and files exist"""
    print("🔍 Checking prerequisites...")
    
    issues = []
    
    # Check directories
    required_dirs = ["crypto", "stocks", "tools", "strategies"]
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            issues.append(f"Missing directory: {dir_name}")
    
    # Check key files
    key_files = [
        "crypto/input/crypto_assets.csv",
        "stocks/input/stock_assets.csv",
        "crypto/input/config_crypto.yaml",
        "stocks/input/config_stocks.yaml",
        "tools/launcher.py"
    ]
    
    for file_path in key_files:
        if not os.path.exists(file_path):
            issues.append(f"Missing file: {file_path}")
    
    if issues:
        print("⚠️  Prerequisites issues found:")
        for issue in issues:
            print(f"   • {issue}")
        print("\n💡 Run setup_complete.bat to fix these issues")
        return False
    
    print("✅ All prerequisites met!")
    return True

def run_crypto_trading():
    """Launch crypto trading platform"""
    print("\n🚀 Launching Crypto Trading Platform...")
    if os.path.exists("crypto_launcher.py"):
        os.system("python crypto_launcher.py")
    else:
        print("❌ crypto_launcher.py not found!")
        print("💡 Please run setup_complete.bat first")

def run_stock_trading():
    """Launch stock trading platform"""
    print("\n📈 Launching Stock Trading Platform...")
    if os.path.exists("stock_launcher.py"):
        os.system("python stock_launcher.py")
    else:
        print("❌ stock_launcher.py not found!")
        print("💡 Creating minimal stock launcher...")
        create_stock_launcher()
        os.system("python stock_launcher.py")

def run_unified_launcher():
    """Run the unified tools launcher"""
    print("\n🔧 Launching Unified Tools...")
    if os.path.exists("tools/launcher.py"):
        os.chdir("tools")
        os.system("python launcher.py")
        os.chdir("..")
    else:
        print("❌ tools/launcher.py not found!")
        print("💡 Please run setup_complete.bat first")

def create_stock_launcher():
    """Create a basic stock launcher if missing"""
    stock_launcher_content = '''#!/usr/bin/env python3
"""
Stock Trading Platform Launcher
==============================

Focused launcher for stock trading via Fyers API.
"""

import os
import sys
from datetime import datetime

def main():
    """Main stock trading platform launcher"""
    print("📈 Stock Trading Platform - Fyers API")
    print("=" * 50)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🇮🇳 Indian Stock Market Trading (NSE/BSE)")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("stocks"):
        print("❌ Error: stocks folder not found!")
        print("💡 Make sure you're running this from the AlgoProject root directory")
        return
    
    while True:
        print("\\n📈 Stock Trading Options:")
        print("=" * 30)
        print("1. 🔍 Stock Scanner - Find trading opportunities")
        print("2. 📊 Stock Backtest - Test strategies on historical data") 
        print("3. 🚀 Live Stock Trading - Execute real trades")
        print("4. 📈 Market Analysis - Technical analysis tools")
        print("5. ⚙️  Configuration - Setup Fyers API")
        print("6. 📋 Portfolio View - Check current positions")
        print("7. 📁 File Management - View logs and outputs")
        print("8. 🔧 System Health Check")
        print("9. 📖 Documentation")
        print("10. 🚪 Exit")
        
        choice = input("\\nEnter your choice (1-10): ").strip()
        
        if choice == "1":
            print("🔍 Stock Scanner - Coming Soon!")
            print("💡 Use tools/launcher.py for now")
        elif choice == "2":
            print("📊 Running Stock Backtest...")
            if os.path.exists("stocks/scripts"):
                os.chdir("stocks/scripts")
                os.system("python stocks_backtest.py")
                os.chdir("../..")
            else:
                print("❌ stocks/scripts not found!")
        elif choice == "3":
            print("🚀 Live Stock Trading...")
            print("⚠️  Make sure Fyers API is configured!")
            if os.path.exists("stocks/scripts"):
                os.chdir("stocks/scripts")
                os.system("python stocks_demo_live.py")
                os.chdir("../..")
            else:
                print("❌ stocks/scripts not found!")
        elif choice == "4":
            print("📈 Market Analysis - Coming Soon!")
        elif choice == "5":
            print("⚙️  Configuration...")
            print("📋 Fyers API Setup:")
            print("   1. Edit: stocks/fyers/credentials.py")
            print("   2. Run: stocks/fyers/generate_token.py")
            print("   3. Configure: stocks/input/config_stocks.yaml")
        elif choice == "6":
            print("📋 Portfolio View - Coming Soon!")
        elif choice == "7":
            print("📁 File Management...")
            print("   • Logs: stocks/logs/")
            print("   • Output: stocks/output/")
            print("   • Config: stocks/input/")
        elif choice == "8":
            print("🔧 System Health Check...")
            os.system("python tools/system_verification.py")
        elif choice == "9":
            print("📖 Documentation...")
            print("   • Main: README.md")
            print("   • Stocks: stocks/README.md")
            print("   • Setup: PERSONAL_LAPTOP_SETUP.md")
        elif choice == "10":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-10.")

if __name__ == "__main__":
    main()
'''
    
    with open("stock_launcher.py", "w") as f:
        f.write(stock_launcher_content)
    print("✅ stock_launcher.py created!")

def show_system_status():
    """Show current system status"""
    print("\n📊 System Status:")
    print("=" * 30)
    
    # Check Python environment
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("🔒 Virtual Environment: Active")
    else:
        print("⚠️  Virtual Environment: Not active")
    
    # Check key directories
    key_dirs = ["crypto", "stocks", "tools", "strategies", "venv"]
    for dir_name in key_dirs:
        status = "✅" if os.path.exists(dir_name) else "❌"
        print(f"{status} Directory: {dir_name}")

def main():
    """Main launcher function"""
    print_banner()
    
    if not check_prerequisites():
        print("\n🔧 Run setup_complete.bat to fix issues and try again!")
        return
    
    while True:
        print("\n🎯 Main Trading Platform Menu:")
        print("=" * 40)
        print("1. 💰 Crypto Trading Platform")
        print("2. 📈 Stock Trading Platform")
        print("3. 🔧 Unified Tools & Utilities")
        print("4. 📊 System Status")
        print("5. 🔍 Run System Verification")
        print("6. 📖 Show Documentation")
        print("7. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            run_crypto_trading()
        elif choice == "2":
            run_stock_trading()
        elif choice == "3":
            run_unified_launcher()
        elif choice == "4":
            show_system_status()
        elif choice == "5":
            print("\n🔍 Running System Verification...")
            os.system("python tools/system_verification.py")
        elif choice == "6":
            print("\n📖 Documentation:")
            print("   • README.md - Main project documentation")
            print("   • PERSONAL_LAPTOP_SETUP.md - Setup instructions")
            print("   • crypto/README.md - Crypto trading guide")
            print("   • stocks/README.md - Stock trading guide")
            print("   • docs/ - Additional documentation")
        elif choice == "7":
            print("👋 Thank you for using AlgoProject!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-7.")

if __name__ == "__main__":
    main()
