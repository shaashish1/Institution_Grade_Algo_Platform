#!/usr/bin/env python3
"""
Crypto Trading Platform Launcher
===============================

Focused launcher for crypto trading - optimized for personal laptops
with no corporate firewall restrictions.
"""

import os
import sys
import json
from datetime import datetime

def main():
    """Main crypto trading platform launcher"""
    print("🚀 Crypto Trading Platform - Personal Laptop Edition")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🏠 Optimized for personal use - no corporate restrictions!")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("crypto"):
        print("❌ Error: crypto folder not found!")
        print("💡 Make sure you're running this from the AlgoProject root directory")
        return
    
    while True:
        print("\n💰 Crypto Trading Options:")
        print("=" * 30)
        print("1. 🔍 Crypto Scanner - Find trading opportunities")
        print("2. 📊 Crypto Backtest - Test strategies on historical data")
        print("3. 🚀 Live Crypto Trading - Execute real trades")
        print("4. 📈 Market Analysis - Technical analysis tools")
        print("5. ⚙️  Configuration - Setup exchanges and strategies")
        print("6. 📋 Portfolio View - Check current positions")
        print("7. 📁 File Management - View logs and outputs")
        print("8. 🔧 System Health Check")
        print("9. 📖 Documentation")
        print("10. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-10): ").strip()
        
        if choice == "1":
            run_crypto_scanner()
        elif choice == "2":
            run_crypto_backtest()
        elif choice == "3":
            run_live_trading()
        elif choice == "4":
            run_market_analysis()
        elif choice == "5":
            configure_platform()
        elif choice == "6":
            view_portfolio()
        elif choice == "7":
            manage_files()
        elif choice == "8":
            system_health_check()
        elif choice == "9":
            show_documentation()
        elif choice == "10":
            print("👋 Goodbye! Happy trading!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def run_crypto_scanner():
    """Run the crypto scanner"""
    print("\n🔍 Starting Crypto Scanner...")
    print("=" * 30)
    
    if os.path.exists("crypto_main.py"):
        print("🚀 Launching crypto_main.py...")
        os.system("python crypto_main.py")
    elif os.path.exists("main.py"):
        print("🚀 Launching main.py with crypto mode...")
        os.system("python main.py --crypto")
    elif os.path.exists("tools/scanner.py"):
        print("🚀 Launching scanner directly...")
        os.system("python tools/scanner.py")
    else:
        print("❌ Scanner not found. Please check your installation.")

def run_crypto_backtest():
    """Run crypto backtesting"""
    print("\n📊 Starting Crypto Backtest...")
    print("=" * 30)
    
    if os.path.exists("crypto_backtest.py"):
        print("🚀 Launching crypto_backtest.py...")
        os.system("python crypto_backtest.py")
    elif os.path.exists("tools/backtest_runner.py"):
        print("🚀 Launching backtest runner...")
        os.system("python tools/backtest_runner.py")
    else:
        print("❌ Backtest module not found. Please check your installation.")

def run_live_trading():
    """Run live crypto trading"""
    print("\n🚀 Starting Live Crypto Trading...")
    print("=" * 30)
    print("⚠️  WARNING: This will execute real trades with real money!")
    
    confirm = input("Are you sure you want to proceed? (yes/no): ").lower().strip()
    if confirm in ['yes', 'y']:
        if os.path.exists("demo_live_trade.py"):
            print("🚀 Launching demo_live_trade.py...")
            os.system("python demo_live_trade.py")
        elif os.path.exists("tools/realtime_trader.py"):
            print("🚀 Launching realtime trader...")
            os.system("python tools/realtime_trader.py")
        else:
            print("❌ Live trading module not found. Please check your installation.")
    else:
        print("✅ Live trading cancelled.")

def run_market_analysis():
    """Run market analysis tools"""
    print("\n📈 Market Analysis Tools...")
    print("=" * 30)
    
    if os.path.exists("tools/technical_analysis.py"):
        print("🚀 Launching technical analysis...")
        os.system("python tools/technical_analysis.py")
    else:
        print("❌ Technical analysis module not found. Please check your installation.")

def configure_platform():
    """Configure the crypto trading platform"""
    print("\n⚙️  Platform Configuration...")
    print("=" * 30)
    
    config_file = "crypto/input/config_crypto.yaml"
    if os.path.exists(config_file):
        print(f"📁 Config file: {config_file}")
        print("1. View current configuration")
        print("2. Edit configuration (manual)")
        print("3. Reset to defaults")
        print("4. Back to main menu")
        
        choice = input("Choose option (1-4): ").strip()
        
        if choice == "1":
            with open(config_file, 'r') as f:
                print("\n📋 Current Configuration:")
                print("-" * 40)
                print(f.read())
        elif choice == "2":
            print(f"📝 Please edit: {config_file}")
            print("💡 Use any text editor to modify the configuration")
        elif choice == "3":
            print("🔄 Reset to defaults would go here...")
            print("💡 Feature coming soon!")
    else:
        print(f"❌ Configuration file not found: {config_file}")
        print("💡 Run setup.bat to create default configuration")

def view_portfolio():
    """View current portfolio"""
    print("\n📋 Portfolio View...")
    print("=" * 30)
    print("💡 Portfolio tracking feature coming soon!")
    print("📁 Check crypto/output/ folder for trading logs")

def manage_files():
    """Manage files and outputs"""
    print("\n📁 File Management...")
    print("=" * 30)
    
    folders = [
        ("Crypto Logs", "crypto/logs"),
        ("Crypto Output", "crypto/output"),
        ("General Output", "output"),
        ("General Logs", "logs")
    ]
    
    for name, path in folders:
        if os.path.exists(path):
            files = os.listdir(path)
            print(f"📂 {name} ({path}): {len(files)} files")
            if files:
                for file in files[:3]:  # Show first 3 files
                    print(f"   • {file}")
                if len(files) > 3:
                    print(f"   ... and {len(files) - 3} more files")
        else:
            print(f"📂 {name} ({path}): Not found")

def system_health_check():
    """Check system health"""
    print("\n🔧 System Health Check...")
    print("=" * 30)
    
    # Check Python packages
    packages = ['ccxt', 'pandas', 'numpy', 'requests', 'yaml']
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}: OK")
        except ImportError:
            print(f"❌ {package}: Missing")
    
    # Check directories
    dirs = ['crypto', 'crypto/input', 'crypto/output', 'crypto/logs', 'tools', 'strategies']
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/: OK")
        else:
            print(f"❌ {dir_path}/: Missing")
    
    # Check key files
    files = ['crypto_main.py', 'main.py', 'requirements.txt']
    for file_path in files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}: OK")
        else:
            print(f"❌ {file_path}: Missing")

def show_documentation():
    """Show documentation"""
    print("\n📖 Documentation...")
    print("=" * 30)
    
    docs = [
        ("Main README", "README.md"),
        ("Project Structure", "docs/PROJECT_STRUCTURE.md"),
        ("Getting Started", "docs/GETTING_STARTED.md"),
        ("Strategies Guide", "docs/strategies-module.md")
    ]
    
    for name, path in docs:
        if os.path.exists(path):
            print(f"📄 {name}: {path}")
        else:
            print(f"📄 {name}: Not found ({path})")
    
    print("\n💡 Quick Tips:")
    print("• Focus on crypto trading - no network restrictions")
    print("• Check crypto/input/config_crypto.yaml for settings")
    print("• Results saved to crypto/output/ folder")
    print("• Logs available in crypto/logs/ folder")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Please check your installation and try again")
