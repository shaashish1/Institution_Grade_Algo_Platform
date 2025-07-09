#!/usr/bin/env python3
"""
AlgoProject Launcher
Simple menu to choose which trading script to run.
"""

import os
import subprocess
import sys


def print_header():
    """Print the application header."""
    print("🚀 AlgoProject Trading Platform")
    print("=" * 70)
    print("Progressive Testing: Test → Backtest → Demo → Live")
    print("Choose your trading mode:")
    print()


def print_menu():
    """Print the main menu."""
    print("🧪 **TESTING & VALIDATION**")
    print("   1. Quick Test           - Test 3 crypto symbols (30 seconds)")
    print("   2. Detailed Test        - Detailed backtest test (1 minute)")
    print()
    print("📊 **BACKTEST (Historical Analysis)**")
    print("   3. Crypto Backtest      - All crypto pairs historical analysis")
    print("   4. Stocks Backtest      - Stock historical analysis")
    print()
    print("🔴 **LIVE DEMO (Real Data, NO Real Trades)**")
    print("   5. Crypto Live Demo     - Real-time crypto demo trading")
    print("   6. Stocks Live Demo     - Real-time stock demo trading")
    print()
    print("⚡ **LIVE SCANNERS (Real-time Alerts)**")
    print("   7. Crypto Live Scanner  - Continuous crypto signal alerts")
    print("   8. Stocks Live Scanner  - Continuous stock signal alerts")
    print()
    print("🛠️  **SYMBOL MANAGEMENT**")
    print("   9. Crypto Symbol Manager - Fetch & select crypto pairs from exchanges")
    print("  10. Stock Symbol Manager  - Fetch & select stocks from NIFTY indices")
    print()
    print("🔧 **UTILITIES**")
    print("  11. List Crypto Assets   - Show current crypto pairs")
    print("  12. List Exchanges       - Show supported exchanges")
    print("  13. Live NSE Quotes      - Real-time NSE stock prices")
    print()
    print("   0. Exit")
    print("=" * 70)


def run_script(script_name, folder="scripts"):
    """Run a specific script."""
    script_path = f"{folder}/{script_name}"
    
    if not os.path.exists(script_path):
        print(f"❌ Error: {script_path} not found!")
        return
    
    print(f"🏃 Running {script_name}...")
    print("=" * 60)
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, script_path], cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"\n✅ {script_name} completed successfully!")
        else:
            print(f"\n❌ {script_name} exited with error code {result.returncode}")
    
    except KeyboardInterrupt:
        print(f"\n⚠️  {script_name} interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running {script_name}: {e}")


def main():
    """Main launcher function."""
    while True:
        print_header()
        print_menu()
        
        try:
            choice = input("Enter your choice (0-13): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                run_script("quick_test.py", "tests")
            elif choice == "2":
                run_script("test_backtest.py", "tests")
            elif choice == "3":
                run_script("crypto_backtest.py", "crypto/scripts")
            elif choice == "4":
                run_script("stocks_backtest.py", "stocks/scripts")
            elif choice == "5":
                run_script("crypto_demo_live.py", "crypto/scripts")
            elif choice == "6":
                run_script("stocks_demo_live.py", "stocks/scripts")
            elif choice == "7":
                run_script("crypto_live_scanner.py", "crypto/scripts")
            elif choice == "8":
                run_script("stocks_live_scanner.py", "stocks/scripts")
            elif choice == "9":
                print("📊 Crypto symbols are managed in input/crypto_assets.csv")
                print("💡 You can edit this file to add/remove crypto pairs")
                input("Press Enter to continue...")
                continue
            elif choice == "10":
                print("📈 Stock symbols are managed via Fyers API and stored in input/stocks_assets.csv")
                print("💡 You can manually edit this file to add/remove stock symbols")
                input("Press Enter to continue...")
                continue
            elif choice == "11":
                run_script("list_crypto_assets.py", "crypto")
            elif choice == "12":
                run_script("list_ccxt_exchanges.py", "crypto")
            elif choice == "13":
                run_script("live_nse_quotes.py", "stocks")
            else:
                print("❌ Invalid choice! Please enter 0-13.")
            
            if choice != "0":
                input("\nPress Enter to continue...")
                print("\n" * 2)  # Clear screen
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
