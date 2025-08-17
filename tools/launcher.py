#!/usr/bin/env python3
"""
AlgoProject Launcher Script
===========================

Main launcher for the AlgoProject trading platform.
Provides easy access to all crypto and stock trading functionalities.
"""

import os
import sys
import argparse
from pathlib import Path

def print_banner():
    print("=" * 80)
    print("🚀 AlgoProject - Advanced Trading Strategy Platform")
    print("=" * 80)
    print("📊 Multi-Asset Trading: Crypto + Stocks")
    print("⚡ Advanced Backtesting & Live Trading")
    print("🔧 Strategy Development & Optimization")
    print("=" * 80)

def show_crypto_options():
    print("\n🪙 CRYPTO TRADING OPTIONS:")
    print("=" * 50)
    print("1. Enhanced Crypto Backtest")
    print("   → cd crypto/scripts && python enhanced_crypto_backtest.py")
    print("   → Example: python enhanced_crypto_backtest.py --symbols BTC/USDT ETH/USDT --compare")
    print()
    print("2. Crypto Demo Live Trading")
    print("   → cd crypto/scripts && python crypto_demo_live.py")
    print()
    print("3. Crypto Live Scanner")
    print("   → cd crypto/scripts && python crypto_live_scanner.py")
    print()
    print("4. Batch Runner (Multiple Strategies)")
    print("   → cd crypto/scripts && python batch_runner.py")
    print("   → Example: python batch_runner.py --symbols BTC/USDT ETH/USDT --strategies BB_RSI,MACD_Only")

def show_stock_options():
    print("\n📈 STOCK TRADING OPTIONS:")
    print("=" * 50)
    print("1. Stock Backtest")
    print("   → cd stocks/scripts && python stocks_backtest.py")
    print("   → Example: python stocks_backtest.py --symbols RELIANCE TCS")
    print()
    print("2. Stock Demo Live Trading")
    print("   → cd stocks/scripts && python stocks_demo_live.py")
    print()
    print("3. Stock Live Scanner")
    print("   → cd stocks/scripts && python stocks_live_scanner.py")

def show_setup_options():
    print("\n⚙️ SETUP & CONFIGURATION:")
    print("=" * 50)
    print("1. Initial Setup")
    print("   → Run: setup.bat")
    print()
    print("2. API Configuration")
    print("   → Fyers API (Stocks): docs/FYERS_SETUP.md")
    print("   → CCXT (Crypto): Automatic configuration")
    print()
    print("3. Documentation")
    print("   → All guides available in: docs/")

def main():
    parser = argparse.ArgumentParser(
        description="AlgoProject Launcher - Access all trading functionalities",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--crypto", action="store_true", help="Show crypto trading options")
    parser.add_argument("--stocks", action="store_true", help="Show stock trading options")
    parser.add_argument("--setup", action="store_true", help="Show setup and configuration options")
    parser.add_argument("--all", action="store_true", help="Show all available options")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.crypto or args.all:
        show_crypto_options()
    
    if args.stocks or args.all:
        show_stock_options()
    
    if args.setup or args.all:
        show_setup_options()
    
    if not any([args.crypto, args.stocks, args.setup, args.all]):
        print("\n📋 QUICK START:")
        print("=" * 50)
        print("• For crypto trading: python launcher.py --crypto")
        print("• For stock trading:  python launcher.py --stocks")
        print("• For setup help:     python launcher.py --setup")
        print("• For all options:    python launcher.py --all")
        print()
        print("💡 TIP: Start with setup.bat if this is your first time!")
    
    print("\n" + "=" * 80)
    print("📚 Documentation: docs/ | 🔧 Setup: setup.bat | 🎯 Happy Trading!")
    print("=" * 80)

if __name__ == "__main__":
    main()
