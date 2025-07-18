#!/usr/bin/env python3
"""
Enhanced Crypto Backtest - Quick Test
Test the enhanced backtest on a few popular crypto symbols
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from crypto.scripts.enhanced_crypto_backtest import EnhancedCryptoBacktest

def main():
    """Run quick test on popular crypto symbols."""
    
    print("🚀 Enhanced Crypto Backtest - Quick Test")
    print("=" * 80)
    
    # Initialize backtest
    backtest = EnhancedCryptoBacktest(
        initial_capital=100000,
        position_size=10000
    )
    
    # Test symbols
    test_symbols = ['BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'SOL/USDT', 'DOT/USDT']
    
    print(f"💰 Initial Capital: ${backtest.initial_capital:,.2f}")
    print(f"📊 Position Size: ${backtest.position_size:,.2f} per trade")
    print(f"🔍 Testing {len(test_symbols)} crypto symbols")
    print("=" * 80)
    
    successful_symbols = []
    failed_symbols = []
    
    for i, symbol in enumerate(test_symbols, 1):
        print(f"[{i:2d}/{len(test_symbols)}] ", end="")
        
        try:
            evaluator = backtest.run_symbol_backtest(symbol)
            if evaluator:
                successful_symbols.append(symbol)
                
                # Display basic results
                trades = evaluator.trades
                if trades:
                    total_pnl = sum(trade['pnl_dollars'] for trade in trades)
                    win_rate = len([t for t in trades if t['pnl_dollars'] > 0]) / len(trades) * 100
                    print(f"   💰 Total P&L: ${total_pnl:,.2f}, Win Rate: {win_rate:.1f}%")
                    
                    # Show a few sample trades
                    if len(trades) > 0:
                        print(f"   📋 Sample trades:")
                        for trade in trades[:3]:  # Show first 3 trades
                            color = "✅" if trade['pnl_dollars'] > 0 else "❌"
                            print(f"      {color} {trade['entry_time'].strftime('%Y-%m-%d %H:%M')} -> {trade['exit_time'].strftime('%Y-%m-%d %H:%M')}: ${trade['pnl_dollars']:,.2f} ({trade['pnl_percent']:.2f}%)")
                else:
                    print("   ⚠️  No trades")
            else:
                failed_symbols.append(symbol)
        except Exception as e:
            print(f"❌ Error: {e}")
            failed_symbols.append(symbol)
    
    print("=" * 80)
    print("📊 QUICK TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Successful: {len(successful_symbols)} symbols")
    print(f"❌ Failed: {len(failed_symbols)} symbols")
    
    if successful_symbols:
        print(f"✅ Successful symbols: {', '.join(successful_symbols)}")
    if failed_symbols:
        print(f"❌ Failed symbols: {', '.join(failed_symbols)}")
    
    print("=" * 80)
    print("🎉 Quick test completed!")
    print("📊 Check the output/ directory for detailed reports")

if __name__ == "__main__":
    main()
