#!/usr/bin/env python3
"""
Delta Exchange Demo Trading System
Complete backtest + realtime demo mode with all 29 KPIs
"""

import os
import sys
import json
import time
import math
import threading
from datetime import datetime, timedelta
from collections import defaultdict
import argparse

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

print("🎯 DELTA EXCHANGE DEMO TRADING SYSTEM")
print("="*70)
print("Backtest + Realtime Demo Mode with All 29 KPIs")
print("="*70)

class DeltaExchangeDemo:
    """Delta Exchange demo trading system."""
    
    EXCHANGE_INFO = {
        'name': 'Delta Exchange',
        'id': 'delta',
        'country': 'India',
        'website': 'https://www.delta.exchange',
        'api_docs': 'https://docs.delta.exchange',
        'status': 'Active - Demo Mode',
        'type': 'Cryptocurrency Derivatives Exchange',
        'features': ['Spot Trading', 'Futures', 'Options', 'Perpetual Swaps'],
        'demo_pairs': [
            'BTC/USDT', 'ETH/USDT', 'BTC/USD', 'ETH/USD',
            'ADA/USDT', 'DOT/USDT', 'SOL/USDT', 'MATIC/USDT'
        ],
        'timeframes': ['1m', '5m', '15m', '1h', '4h', '1d'],
        'demo_balance': 100000.0
    }
    
    @classmethod
    def display_info(cls):
        """Display Delta Exchange demo information."""
        info = cls.EXCHANGE_INFO
        print(f"\n📊 {info['name']} Demo System:")
        print(f"   🏢 Country: {info['country']}")
        print(f"   🌐 Website: {info['website']}")
        print(f"   📚 API Docs: {info['api_docs']}")
        print(f"   🎮 Status: {info['status']}")
        print(f"   🎯 Type: {info['type']}")
        print(f"   🔧 Features: {', '.join(info['features'])}")
        print(f"   📈 Demo Pairs: {', '.join(info['demo_pairs'][:6])}")
        print(f"   💰 Demo Balance: ${info['demo_balance']:,.2f}")

class RealtimeDemoTrader:
    """Realtime demo trading system."""
    
    def __init__(self, initial_balance=100000, position_size=10000):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.position_size = position_size
        self.active_positions = {}
        self.completed_trades = []
        self.is_running = False
        self.symbols = ['BTC/USDT', 'ETH/USDT', 'ADA/USDT']
        
    def generate_live_price(self, symbol, base_price=None):
        """Generate realistic live price simulation."""
        base_prices = {
            'BTC/USDT': 45000,
            'ETH/USDT': 2500,
            'ADA/USDT': 0.5,
            'DOT/USDT': 7.5,
            'SOL/USDT': 20,
            'MATIC/USDT': 0.8
        }
        
        if base_price is None:
            base_price = base_prices.get(symbol, 1000)
        
        # Simulate realistic price movement (-2% to +2%)
        current_time = datetime.now()
        change = (hash(str(current_time) + symbol) % 100 - 50) / 2500  # -2% to +2%
        new_price = base_price * (1 + change)
        
        return max(new_price, 0.01)  # Ensure positive price
    
    def calculate_rsi_live(self, symbol, prices):
        """Calculate RSI for live trading."""
        if len(prices) < 15:
            return 50
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        period = 14
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def check_trading_signals(self, symbol, current_price, price_history):
        """Check for trading signals in realtime."""
        if len(price_history) < 20:
            return None
        
        rsi = self.calculate_rsi_live(symbol, price_history)
        
        # Trading logic
        if rsi < 25 and symbol not in self.active_positions:
            return {
                'action': 'BUY',
                'symbol': symbol,
                'price': current_price,
                'rsi': rsi,
                'timestamp': datetime.now(),
                'reason': f'RSI Oversold ({rsi:.1f})'
            }
        elif rsi > 75 and symbol in self.active_positions:
            return {
                'action': 'SELL',
                'symbol': symbol,
                'price': current_price,
                'rsi': rsi,
                'timestamp': datetime.now(),
                'reason': f'RSI Overbought ({rsi:.1f})'
            }
        
        return None
    
    def execute_trade(self, signal):
        """Execute demo trade."""
        symbol = signal['symbol']
        action = signal['action']
        price = signal['price']
        timestamp = signal['timestamp']
        
        if action == 'BUY':
            quantity = self.position_size / price
            
            position = {
                'symbol': symbol,
                'entry_price': price,
                'entry_time': timestamp,
                'quantity': quantity,
                'entry_rsi': signal['rsi']
            }
            
            self.active_positions[symbol] = position
            
            print(f"\n🟢 BUY EXECUTED:")
            print(f"   📊 Symbol: {symbol}")
            print(f"   💰 Price: ${price:,.2f}")
            print(f"   📈 Quantity: {quantity:.6f}")
            print(f"   📊 RSI: {signal['rsi']:.1f}")
            print(f"   💡 Reason: {signal['reason']}")
            print(f"   ⏰ Time: {timestamp.strftime('%H:%M:%S')}")
            
        elif action == 'SELL' and symbol in self.active_positions:
            position = self.active_positions[symbol]
            
            profit = (price - position['entry_price']) * position['quantity']
            profit_pct = ((price - position['entry_price']) / position['entry_price']) * 100
            duration = timestamp - position['entry_time']
            
            trade = {
                'symbol': symbol,
                'entry_time': position['entry_time'],
                'exit_time': timestamp,
                'entry_price': position['entry_price'],
                'exit_price': price,
                'quantity': position['quantity'],
                'profit': profit,
                'profit_pct': profit_pct,
                'duration': duration,
                'entry_rsi': position['entry_rsi'],
                'exit_rsi': signal['rsi']
            }
            
            self.completed_trades.append(trade)
            self.current_balance += profit
            del self.active_positions[symbol]
            
            print(f"\n🔴 SELL EXECUTED:")
            print(f"   📊 Symbol: {symbol}")
            print(f"   💰 Price: ${price:,.2f}")
            print(f"   📈 Profit: ${profit:,.2f} ({profit_pct:+.2f}%)")
            print(f"   📊 Exit RSI: {signal['rsi']:.1f}")
            print(f"   💡 Reason: {signal['reason']}")
            print(f"   ⏱️ Duration: {str(duration).split('.')[0]}")
            print(f"   💰 New Balance: ${self.current_balance:,.2f}")
    
    def display_status(self):
        """Display current trading status."""
        print(f"\n📊 LIVE TRADING STATUS:")
        print(f"   💰 Balance: ${self.current_balance:,.2f}")
        print(f"   📈 P&L: ${self.current_balance - self.initial_balance:,.2f}")
        print(f"   🔄 Active Positions: {len(self.active_positions)}")
        print(f"   ✅ Completed Trades: {len(self.completed_trades)}")
        
        if self.active_positions:
            print(f"\n🎯 ACTIVE POSITIONS:")
            for symbol, pos in self.active_positions.items():
                duration = datetime.now() - pos['entry_time']
                print(f"   📊 {symbol}: ${pos['entry_price']:,.2f} | {str(duration).split('.')[0]}")
        
        if self.completed_trades:
            recent_trades = self.completed_trades[-3:]
            print(f"\n📋 RECENT TRADES:")
            for trade in recent_trades:
                print(f"   {trade['symbol']}: {trade['profit_pct']:+.2f}% | {str(trade['duration']).split('.')[0]}")
    
    def run_live_demo(self, duration_minutes=5):
        """Run live demo trading."""
        print(f"\n🚀 STARTING LIVE DEMO TRADING")
        print(f"Duration: {duration_minutes} minutes")
        print(f"Symbols: {', '.join(self.symbols)}")
        print("="*60)
        
        self.is_running = True
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        # Price history for each symbol
        price_histories = {symbol: [] for symbol in self.symbols}
        
        # Initialize with some history
        for symbol in self.symbols:
            for _ in range(20):
                price = self.generate_live_price(symbol)
                price_histories[symbol].append(price)
        
        cycle_count = 0
        
        try:
            while datetime.now() < end_time and self.is_running:
                cycle_count += 1
                
                for symbol in self.symbols:
                    # Generate new price
                    current_price = self.generate_live_price(symbol)
                    price_histories[symbol].append(current_price)
                    
                    # Keep only recent history
                    if len(price_histories[symbol]) > 50:
                        price_histories[symbol] = price_histories[symbol][-50:]
                    
                    # Check for signals
                    signal = self.check_trading_signals(symbol, current_price, price_histories[symbol])
                    
                    if signal:
                        self.execute_trade(signal)
                
                # Display status every 10 cycles
                if cycle_count % 10 == 0:
                    self.display_status()
                    
                    # Show live prices
                    print(f"\n💹 LIVE PRICES:")
                    for symbol in self.symbols:
                        current_price = price_histories[symbol][-1]
                        rsi = self.calculate_rsi_live(symbol, price_histories[symbol])
                        status = "🟢" if symbol in self.active_positions else "⚪"
                        print(f"   {status} {symbol}: ${current_price:,.2f} | RSI: {rsi:.1f}")
                
                time.sleep(2)  # 2-second intervals
                
        except KeyboardInterrupt:
            print("\n⚠️ Demo interrupted by user")
        
        self.is_running = False
        
        # Final summary
        self.display_final_summary()
    
    def display_final_summary(self):
        """Display final trading summary."""
        print(f"\n" + "="*60)
        print("🎯 DEMO TRADING COMPLETE")
        print("="*60)
        
        total_profit = self.current_balance - self.initial_balance
        total_return = (total_profit / self.initial_balance) * 100
        
        print(f"📊 FINAL RESULTS:")
        print(f"   💰 Starting Balance: ${self.initial_balance:,.2f}")
        print(f"   💰 Ending Balance: ${self.current_balance:,.2f}")
        print(f"   📈 Total Profit: ${total_profit:,.2f}")
        print(f"   📊 Total Return: {total_return:+.2f}%")
        print(f"   🔄 Total Trades: {len(self.completed_trades)}")
        print(f"   🎯 Active Positions: {len(self.active_positions)}")
        
        if self.completed_trades:
            winning_trades = [t for t in self.completed_trades if t['profit_pct'] > 0]
            win_rate = (len(winning_trades) / len(self.completed_trades)) * 100
            avg_profit = sum([t['profit_pct'] for t in self.completed_trades]) / len(self.completed_trades)
            
            print(f"   ✅ Win Rate: {win_rate:.1f}%")
            print(f"   📊 Average Trade: {avg_profit:+.2f}%")
            
            if winning_trades:
                best_trade = max([t['profit_pct'] for t in self.completed_trades])
                worst_trade = min([t['profit_pct'] for t in self.completed_trades])
                print(f"   🏆 Best Trade: {best_trade:+.2f}%")
                print(f"   📉 Worst Trade: {worst_trade:+.2f}%")

def run_backtest_mode():
    """Run comprehensive backtest mode."""
    from delta_exchange_backtest import DeltaBacktestEngine, display_comprehensive_results, save_results_to_json
    
    print("🔄 RUNNING BACKTEST MODE...")
    
    engine = DeltaBacktestEngine(
        initial_capital=100000,
        position_size=10000
    )
    
    results = engine.run_comprehensive_backtest()
    
    if results:
        display_comprehensive_results(results)
        save_results_to_json(results, "delta_backtest_results.json")
        return True
    return False

def run_demo_mode(duration=5):
    """Run realtime demo mode."""
    print("🎮 RUNNING DEMO MODE...")
    
    trader = RealtimeDemoTrader(
        initial_balance=100000,
        position_size=10000
    )
    
    trader.run_live_demo(duration_minutes=duration)

def main():
    """Main function for Delta Exchange demo system."""
    parser = argparse.ArgumentParser(description='Delta Exchange Demo Trading System')
    
    parser.add_argument(
        '--mode', '-m',
        choices=['backtest', 'demo', 'both'],
        default='both',
        help='Trading mode: backtest, demo, or both'
    )
    
    parser.add_argument(
        '--duration', '-d',
        type=int,
        default=5,
        help='Demo duration in minutes (default: 5)'
    )
    
    parser.add_argument(
        '--balance', '-b',
        type=float,
        default=100000,
        help='Initial balance (default: 100000)'
    )
    
    args = parser.parse_args()
    
    # Display system info
    DeltaExchangeDemo.display_info()
    
    if args.mode in ['backtest', 'both']:
        print("\n" + "="*70)
        print("🔄 BACKTEST MODE")
        print("="*70)
        
        success = run_backtest_mode()
        
        if not success:
            print("❌ Backtest failed")
            return 1
    
    if args.mode in ['demo', 'both']:
        print("\n" + "="*70)
        print("🎮 DEMO MODE")
        print("="*70)
        
        run_demo_mode(duration=args.duration)
    
    print(f"\n✅ Delta Exchange Demo System Complete!")
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️ System interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
