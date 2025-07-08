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
    print("=" * 60)
    print("Choose your trading mode:")
    print()


def print_menu():
    """Print the main menu."""
    print("📊 **CRYPTO TRADING** (CCXT Data)")
    print("   1. Crypto Backtest      - Historical analysis of all 37 crypto pairs")
    print("   2. Crypto Live Scanner  - Real-time scanning and alerts")
    print()
    print("📈 **STOCKS TRADING** (TradingView Data)")
    print("   3. Stocks Backtest      - Historical analysis of stocks")
    print("   4. Stocks Live Scanner  - Real-time stock scanning")
    print()
    print("🛠️  **UTILITIES**")
    print("   5. List Crypto Assets   - Show available crypto pairs")
    print("   6. List Exchanges       - Show supported exchanges")
    print()
    print("   0. Exit")
    print("=" * 60)


def run_script(script_name):
    """Run a specific script."""
    script_path = f"scripts/{script_name}"
    
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
            choice = input("Enter your choice (0-6): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                run_script("crypto_backtest.py")
            elif choice == "2":
                run_script("crypto_live_scanner.py")
            elif choice == "3":
                run_script("stocks_backtest.py")
            elif choice == "4":
                run_script("stocks_live_scanner.py")
            elif choice == "5":
                run_script("list_crypto_assets.py")
            elif choice == "6":
                run_script("list_ccxt_exchanges.py")
            else:
                print("❌ Invalid choice! Please enter 0-6.")
            
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
