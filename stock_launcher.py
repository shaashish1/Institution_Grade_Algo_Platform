#!/usr/bin/env python3
"""
Stock Trading Platform Launcher
==============================

Focused launcher for stock trading via Fyers API.
Optimized for personal laptops with full NSE/BSE access.
"""

import os
import sys
from datetime import datetime

def print_banner():
    print("📈 Stock Trading Platform - Fyers API")
    print("=" * 50)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🇮🇳 Indian Stock Market Trading (NSE/BSE)")
    print("🏠 Personal Laptop Edition - Full API Access!")
    print("=" * 50)

def check_stock_prerequisites():
    """Check if stock trading prerequisites are met"""
    print("🔍 Checking stock trading prerequisites...")
    
    issues = []
    
    # Check directories
    required_dirs = ["stocks", "stocks/input", "stocks/fyers", "stocks/scripts", "stocks/output"]
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            issues.append(f"Missing directory: {dir_name}")
    
    # Check key files
    key_files = [
        "stocks/input/stock_assets.csv",
        "stocks/input/config_stocks.yaml",
        "stocks/fyers/credentials.py"
    ]
    
    for file_path in key_files:
        if not os.path.exists(file_path):
            issues.append(f"Missing file: {file_path}")
    
    if issues:
        print("⚠️  Stock trading setup issues found:")
        for issue in issues:
            print(f"   • {issue}")
        print("\n💡 Run setup_complete.bat to fix these issues")
        return False
    
    print("✅ Stock trading prerequisites met!")
    return True

def run_stock_scanner():
    """Run stock scanning for trading opportunities"""
    print("\n🔍 Stock Scanner - Finding Trading Opportunities...")
    print("=" * 50)
    
    if os.path.exists("stocks/scripts/stock_scanner.py"):
        os.chdir("stocks/scripts")
        os.system("python stock_scanner.py")
        os.chdir("../..")
    else:
        print("📊 Using built-in scanner...")
        print("💡 Available scanners:")
        print("   • Live NSE Quotes: stocks/live_nse_quotes.py")
        print("   • Market Analysis: tools/comprehensive_test.py")
        
        choice = input("\nRun live NSE quotes? (y/n): ").lower()
        if choice == 'y':
            os.system("python stocks/live_nse_quotes.py")

def run_stock_backtest():
    """Run stock backtesting"""
    print("\n📊 Stock Backtesting...")
    print("=" * 30)
    
    if os.path.exists("stocks/scripts/stocks_backtest.py"):
        print("🚀 Running stocks backtest...")
        os.chdir("stocks/scripts")
        os.system("python stocks_backtest.py")
        os.chdir("../..")
    else:
        print("⚠️  stocks_backtest.py not found in stocks/scripts/")
        print("💡 Available backtest options:")
        print("   • Run: python tools/launcher.py --stocks")
        print("   • Or create custom backtest in stocks/scripts/")

def run_live_stock_trading():
    """Run live stock trading"""
    print("\n🚀 Live Stock Trading...")
    print("=" * 30)
    print("⚠️  IMPORTANT: This will execute REAL trades with REAL money!")
    print("🔐 Make sure your Fyers API credentials are correctly configured")
    
    confirm = input("\nContinue with live trading? (yes/no): ").lower()
    if confirm != "yes":
        print("❌ Live trading cancelled")
        return
    
    if os.path.exists("stocks/scripts/stocks_demo_live.py"):
        os.chdir("stocks/scripts")
        os.system("python stocks_demo_live.py")
        os.chdir("../..")
    else:
        print("⚠️  stocks_demo_live.py not found!")
        print("💡 Creating demo live trading script...")
        create_demo_live_script()

def create_demo_live_script():
    """Create a basic demo live trading script"""
    if not os.path.exists("stocks/scripts"):
        os.makedirs("stocks/scripts")
    
    script_content = '''#!/usr/bin/env python3
"""
Demo Live Stock Trading Script
=============================
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from datetime import datetime

def main():
    print("🚀 Stock Demo Live Trading")
    print("=" * 40)
    print(f"Started: {datetime.now()}")
    print()
    print("⚠️  This is a DEMO script")
    print("🔧 Integrate with your Fyers API here")
    print()
    print("📋 Next steps:")
    print("   1. Configure Fyers API credentials")
    print("   2. Implement your trading strategy")
    print("   3. Add risk management")
    print("   4. Test with paper trading first")
    print()
    print("💡 See stocks/README.md for detailed setup")

if __name__ == "__main__":
    main()
'''
    
    with open("stocks/scripts/stocks_demo_live.py", "w") as f:
        f.write(script_content)
    print("✅ Demo live trading script created!")

def configure_fyers_api():
    """Help configure Fyers API"""
    print("\n⚙️  Fyers API Configuration")
    print("=" * 35)
    
    print("📋 Configuration Steps:")
    print("1. 🔐 Credentials Setup:")
    print(f"   • Edit: stocks/fyers/credentials.py")
    print("   • Add your Fyers user ID and PIN")
    
    print("\n2. 🔑 API Token Generation:")
    if os.path.exists("stocks/fyers/generate_token.py"):
        print("   • Run: python stocks/fyers/generate_token.py")
        choice = input("\nRun token generation now? (y/n): ").lower()
        if choice == 'y':
            os.chdir("stocks/fyers")
            os.system("python generate_token.py")
            os.chdir("../..")
    else:
        print("   ⚠️  generate_token.py not found!")
        print("   💡 Check Fyers API documentation")
    
    print("\n3. 📊 Configuration File:")
    print(f"   • Edit: stocks/input/config_stocks.yaml")
    print("   • Update Fyers client ID and settings")
    
    print("\n4. 🧪 Test Connection:")
    print("   • Run system verification")
    choice = input("\nRun system verification? (y/n): ").lower()
    if choice == 'y':
        os.system("python tools/system_verification.py")

def view_portfolio():
    """View current portfolio and positions"""
    print("\n📋 Portfolio View")
    print("=" * 25)
    
    print("💡 Portfolio features:")
    print("   • Current positions")
    print("   • P&L analysis") 
    print("   • Risk metrics")
    print("   • Trade history")
    print()
    print("⚠️  Portfolio viewer not yet implemented")
    print("🔧 This feature is coming soon!")
    print()
    print("📊 Available alternatives:")
    print("   • Check Fyers web platform")
    print("   • View stocks/output/ for trade logs")
    print("   • Run system verification for status")

def manage_files():
    """File management and viewing"""
    print("\n📁 File Management")
    print("=" * 25)
    
    print("📂 Key directories:")
    print("   • stocks/logs/ - Trading logs")
    print("   • stocks/output/ - Results and analysis")
    print("   • stocks/input/ - Configuration files")
    print("   • stocks/fyers/ - API credentials")
    
    print("\n📋 Recent files:")
    dirs_to_check = ["stocks/logs", "stocks/output"]
    for dir_path in dirs_to_check:
        if os.path.exists(dir_path):
            files = os.listdir(dir_path)
            if files:
                print(f"\n{dir_path}:")
                for file in files[-5:]:  # Show last 5 files
                    print(f"   • {file}")
            else:
                print(f"\n{dir_path}: (empty)")
        else:
            print(f"\n{dir_path}: (not found)")

def run_system_health():
    """Run system health check"""
    print("\n🔧 System Health Check")
    print("=" * 30)
    
    if os.path.exists("tools/system_verification.py"):
        print("🚀 Running comprehensive system verification...")
        os.system("python tools/system_verification.py")
    else:
        print("⚠️  system_verification.py not found!")
        print("💡 Basic health check:")
        
        # Check Python
        print(f"🐍 Python: {sys.version.split()[0]}")
        
        # Check key directories
        for dir_name in ["stocks", "stocks/input", "stocks/fyers"]:
            status = "✅" if os.path.exists(dir_name) else "❌"
            print(f"{status} {dir_name}")

def show_documentation():
    """Show documentation and help"""
    print("\n📖 Documentation & Help")
    print("=" * 30)
    
    print("📚 Available documentation:")
    docs = [
        ("README.md", "Main project documentation"),
        ("PERSONAL_LAPTOP_SETUP.md", "Setup instructions"),
        ("stocks/README.md", "Stock trading guide"),
        ("docs/FYERS_SETUP.md", "Fyers API setup"),
        ("Project_Detailed_Specification.txt", "Technical specifications")
    ]
    
    for doc_file, description in docs:
        status = "✅" if os.path.exists(doc_file) else "❌"
        print(f"{status} {doc_file} - {description}")
    
    print("\n🌐 Online resources:")
    print("   • Fyers API Docs: https://fyers.in/api-documentation/")
    print("   • Python Trading: https://github.com/pmorissette/backtrader")
    print("   • Technical Analysis: https://github.com/twopirllc/pandas-ta")

def main():
    """Main stock trading launcher"""
    print_banner()
    
    # Check if we're in the right directory
    if not os.path.exists("stocks"):
        print("❌ Error: stocks folder not found!")
        print("💡 Make sure you're running this from the AlgoProject root directory")
        return
    
    # Check prerequisites
    if not check_stock_prerequisites():
        print("\n🔧 Run setup_complete.bat to fix issues and try again!")
        input("\nPress Enter to continue anyway...")
    
    while True:
        print("\n📈 Stock Trading Options:")
        print("=" * 35)
        print("1. 🔍 Stock Scanner - Find trading opportunities")
        print("2. 📊 Stock Backtest - Test strategies on historical data") 
        print("3. 🚀 Live Stock Trading - Execute real trades")
        print("4. 📈 Market Analysis - View live market data")
        print("5. ⚙️  Configure Fyers API - Setup credentials")
        print("6. 📋 Portfolio View - Check current positions")
        print("7. 📁 File Management - View logs and outputs")
        print("8. 🔧 System Health Check - Verify setup")
        print("9. 📖 Documentation - Help and guides")
        print("10. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-10): ").strip()
        
        if choice == "1":
            run_stock_scanner()
        elif choice == "2":
            run_stock_backtest()
        elif choice == "3":
            run_live_stock_trading()
        elif choice == "4":
            print("📈 Running market analysis...")
            run_stock_scanner()  # For now, use scanner for market analysis
        elif choice == "5":
            configure_fyers_api()
        elif choice == "6":
            view_portfolio()
        elif choice == "7":
            manage_files()
        elif choice == "8":
            run_system_health()
        elif choice == "9":
            show_documentation()
        elif choice == "10":
            print("👋 Thank you for using Stock Trading Platform!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-10.")

if __name__ == "__main__":
    main()
