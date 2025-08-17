#!/usr/bin/env python3
"""
Backtest Runner - Universal Backtesting Tool
============================================

Universal backtest runner that can execute backtests for both crypto and stocks
with various strategies and configurations.
"""

import os
import sys
import argparse
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_crypto_backtest(symbols=None, strategy='VWAPSigma2Strategy', days=30):
    """Run crypto backtest with specified parameters."""
    print(f"🪙 Running crypto backtest...")
    print(f"   • Strategy: {strategy}")
    print(f"   • Symbols: {symbols or 'All available'}")
    print(f"   • Period: {days} days")
    
    try:
        # Import crypto backtest
        sys.path.append(str(project_root / 'crypto' / 'scripts'))
        from crypto_backtest import run_crypto_backtest as run_crypto
        
        # Run the backtest
        run_crypto()
        return True
    except Exception as e:
        print(f"❌ Crypto backtest failed: {e}")
        return False

def run_stock_backtest(symbols=None, strategy='VWAPSigma2Strategy', days=30):
    """Run stock backtest with specified parameters."""
    print(f"📈 Running stock backtest...")
    print(f"   • Strategy: {strategy}")
    print(f"   • Symbols: {symbols or 'All available'}")
    print(f"   • Period: {days} days")
    
    try:
        # Import stock backtest
        sys.path.append(str(project_root / 'stocks' / 'scripts'))
        from stocks_backtest import run_stocks_backtest as run_stocks
        
        # Run the backtest
        run_stocks()
        return True
    except Exception as e:
        print(f"❌ Stock backtest failed: {e}")
        return False

def run_comprehensive_backtest(crypto_symbols=None, stock_symbols=None, strategy='VWAPSigma2Strategy'):
    """Run comprehensive backtest on both crypto and stocks."""
    print("🔄 Running comprehensive backtest...")
    print("=" * 60)
    
    results = {
        'crypto': False,
        'stocks': False
    }
    
    # Run crypto backtest
    if crypto_symbols != False:  # Allow empty list but not False
        print("\n1️⃣ Crypto Backtesting Phase")
        print("-" * 30)
        results['crypto'] = run_crypto_backtest(crypto_symbols, strategy)
    
    # Run stock backtest
    if stock_symbols != False:  # Allow empty list but not False
        print("\n2️⃣ Stock Backtesting Phase")
        print("-" * 30)
        results['stocks'] = run_stock_backtest(stock_symbols, strategy)
    
    # Summary
    print("\n📊 Backtest Summary")
    print("=" * 30)
    print(f"Crypto: {'✅ Success' if results['crypto'] else '❌ Failed'}")
    print(f"Stocks: {'✅ Success' if results['stocks'] else '❌ Failed'}")
    
    return results

def main():
    """Main entry point for backtest runner."""
    parser = argparse.ArgumentParser(description='Universal Backtest Runner')
    parser.add_argument('--mode', choices=['crypto', 'stocks', 'both'], default='both',
                       help='Backtest mode (default: both)')
    parser.add_argument('--strategy', default='VWAPSigma2Strategy',
                       help='Strategy to test (default: VWAPSigma2Strategy)')
    parser.add_argument('--crypto-symbols', nargs='*',
                       help='Crypto symbols to test (e.g., BTC/USDT ETH/USDT)')
    parser.add_argument('--stock-symbols', nargs='*',
                       help='Stock symbols to test (e.g., RELIANCE TCS)')
    parser.add_argument('--days', type=int, default=30,
                       help='Number of days to backtest (default: 30)')
    
    args = parser.parse_args()
    
    print("🚀 AlgoProject Backtest Runner")
    print("=" * 50)
    print(f"Mode: {args.mode}")
    print(f"Strategy: {args.strategy}")
    print(f"Period: {args.days} days")
    print("=" * 50)
    
    if args.mode == 'crypto':
        run_crypto_backtest(args.crypto_symbols, args.strategy, args.days)
    elif args.mode == 'stocks':
        run_stock_backtest(args.stock_symbols, args.strategy, args.days)
    else:  # both
        crypto_symbols = args.crypto_symbols if args.crypto_symbols is not None else []
        stock_symbols = args.stock_symbols if args.stock_symbols is not None else []
        run_comprehensive_backtest(crypto_symbols, stock_symbols, args.strategy)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Backtest interrupted by user")
    except Exception as e:
        print(f"\n❌ Backtest runner failed: {e}")
        import traceback
        traceback.print_exc()
