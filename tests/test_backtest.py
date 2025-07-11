#!/usr/bin/env python3
"""
Quick Crypto Backtest Test
Test backtest functionality with 3 symbols.
"""

import os
import sys
import pandas as pd
from datetime import datetime
import pytz

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.data_acquisition import fetch_data
from tabulate import tabulate


def load_strategy():
    """Load the trading strategy."""
    sys.path.append('src/strategies')
    from strategies.VWAPSigma2Strategy import VWAPSigma2Strategy
    return VWAPSigma2Strategy()


def run_quick_backtest():
    """Run a quick backtest with 3 popular crypto symbols."""
    print("🧪 Quick Crypto Backtest Test")
    print("=" * 60)
    
    # Test with 3 popular symbols
    test_symbols = ["BTC/USDT", "ETH/USDT", "ADA/USDT"]
    
    print(f"🔍 Backtesting {len(test_symbols)} crypto symbols using CCXT (Kraken)")
    print(f"📊 Strategy: VWAPSigma2Strategy")
    print("=" * 60)
    
    # Load strategy
    strategy = load_strategy()
    
    # Results storage
    all_trades = []
    
    ist = pytz.timezone('Asia/Kolkata')
    start_time = datetime.now(ist)
    
    for i, symbol in enumerate(test_symbols, 1):
        try:
            print(f"📈 [{i}/{len(test_symbols)}] Backtesting {symbol}...", end=" ")
            
            # Fetch data using CCXT
            data = fetch_data(
                symbol=symbol,
                exchange="kraken",
                interval="5m",
                bars=100,  # Good amount for backtest
                data_source="ccxt",
                fetch_timeout=15
            )
            
            if data is None or data.empty:
                print("❌ No data")
                continue
            
            # Add datetime column required by strategy
            if 'timestamp' in data.columns:
                data['datetime'] = data['timestamp']
            
            # Apply strategy backtest
            trades_df = strategy.backtest(data)
            if not trades_df.empty:
                trade_count = len(trades_df)
                print(f"✅ {trade_count} trades")
                
                # Store trades with symbol
                for _, trade in trades_df.iterrows():
                    trade_data = trade.to_dict()
                    trade_data['symbol'] = symbol
                    all_trades.append(trade_data)
            else:
                print("⚪ No trades")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Calculate performance
    end_time = datetime.now(ist)
    duration = (end_time - start_time).total_seconds()
    
    print("=" * 60)
    print(f"✅ Backtest completed in {duration:.1f}s")
    print(f"💰 Total trades: {len(all_trades)}")
    
    # Display trades
    if all_trades:
        display_trades(all_trades)
    else:
        print("\n⚠️  No trades generated in backtest.")


def display_trades(trades):
    """Display backtest trades."""
    print(f"\n📊 **BACKTEST TRADES** ({len(trades)} trades)")
    print("=" * 80)
    
    # Convert to display format
    display_data = []
    total_pnl = 0
    
    for trade in trades:
        pnl = trade.get('pnl_percentage', 0)
        total_pnl += pnl
        
        display_data.append([
            trade.get('symbol', ''),
            trade.get('action', ''),
            f"${trade.get('entry_price', 0):.4f}",
            f"${trade.get('exit_price', 0):.4f}",
            f"{pnl:.2f}%"
        ])
    
    print(tabulate(display_data, headers=['Symbol', 'Action', 'Entry', 'Exit', 'PnL%'], tablefmt='grid'))
    
    print(f"\n💰 **PERFORMANCE SUMMARY**")
    print(f"Total PnL: {total_pnl:.2f}%")
    print(f"Average PnL per trade: {total_pnl/len(trades):.2f}%")
    
    # Win/Loss ratio
    wins = sum(1 for trade in trades if trade.get('pnl_percentage', 0) > 0)
    losses = len(trades) - wins
    win_rate = (wins / len(trades)) * 100 if trades else 0
    
    print(f"Win Rate: {win_rate:.1f}% ({wins} wins, {losses} losses)")


if __name__ == "__main__":
    try:
        run_quick_backtest()
    except KeyboardInterrupt:
        print("\n⚠️  Backtest interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
