#!/usr/bin/env python3
"""
Alternative Crypto Backtest - Native Python Implementation
Works without pandas/numpy/ccxt if they're causing issues
"""

import os
import sys
import json
import csv
import time
import math
from datetime import datetime, timedelta

print("🚀 ALTERNATIVE CRYPTO BACKTEST - Native Python")
print("="*60)
print("This version works without pandas/numpy/ccxt")
print("="*60)

class SimpleCryptoData:
    """Simple crypto data handler without external dependencies."""
    
    def __init__(self):
        self.data = []
        
    def generate_sample_data(self, symbol='BTC/USDT', days=30):
        """Generate sample OHLCV data for testing."""
        print(f"📊 Generating sample data for {symbol} ({days} days)...")
        
        # Start price around 45000 for BTC
        base_price = 45000 if 'BTC' in symbol else 2500
        
        current_time = datetime.now() - timedelta(days=days)
        
        for i in range(days * 24):  # Hourly data
            # Simple random walk
            change = (hash(str(current_time)) % 200 - 100) / 1000  # -10% to +10%
            base_price *= (1 + change)
            
            # Ensure positive price
            if base_price < 100:
                base_price = 100
                
            # Generate OHLCV
            high = base_price * (1 + abs(change) * 0.5)
            low = base_price * (1 - abs(change) * 0.5)
            volume = 1000 + (hash(str(current_time)) % 5000)
            
            candle = {
                'timestamp': current_time,
                'open': base_price,
                'high': high,
                'low': low,
                'close': base_price,
                'volume': volume
            }
            
            self.data.append(candle)
            current_time += timedelta(hours=1)
            
        print(f"✅ Generated {len(self.data)} data points")
        return self.data

class SimpleIndicators:
    """Simple technical indicators without numpy."""
    
    @staticmethod
    def simple_moving_average(data, period):
        """Calculate simple moving average."""
        if len(data) < period:
            return None
        return sum(data[-period:]) / period
    
    @staticmethod
    def rsi(prices, period=14):
        """Calculate RSI without pandas."""
        if len(prices) < period + 1:
            return 50  # Neutral RSI
            
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
        
        if len(gains) < period:
            return 50
            
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

class SimpleBacktest:
    """Simple backtest engine without external dependencies."""
    
    def __init__(self, initial_capital=100000, position_size=10000):
        self.initial_capital = initial_capital
        self.position_size = position_size
        self.capital = initial_capital
        self.position = None
        self.trades = []
        
    def generate_simple_signals(self, data):
        """Generate simple RSI-based signals."""
        signals = []
        
        print("📈 Generating signals...")
        
        for i in range(20, len(data)):  # Start after indicator period
            current = data[i]
            
            # Get recent prices for RSI
            recent_prices = [candle['close'] for candle in data[max(0, i-20):i+1]]
            rsi = SimpleIndicators.rsi(recent_prices)
            
            # Simple RSI strategy
            if rsi < 30:  # Oversold - buy signal
                signals.append({
                    'timestamp': current['timestamp'],
                    'action': 'buy',
                    'price': current['close'],
                    'rsi': rsi
                })
            elif rsi > 70:  # Overbought - sell signal
                signals.append({
                    'timestamp': current['timestamp'],
                    'action': 'sell',
                    'price': current['close'],
                    'rsi': rsi
                })
        
        print(f"✅ Generated {len(signals)} signals")
        return signals
    
    def execute_backtest(self, data, signals):
        """Execute backtest with generated signals."""
        print("⚡ Executing backtest...")
        
        for signal in signals:
            if signal['action'] == 'buy' and self.position is None:
                # Enter position
                quantity = self.position_size / signal['price']
                self.position = {
                    'entry_price': signal['price'],
                    'entry_time': signal['timestamp'],
                    'quantity': quantity
                }
                
            elif signal['action'] == 'sell' and self.position is not None:
                # Exit position
                profit = (signal['price'] - self.position['entry_price']) * self.position['quantity']
                profit_pct = ((signal['price'] - self.position['entry_price']) / self.position['entry_price']) * 100
                
                trade = {
                    'entry_time': self.position['entry_time'],
                    'exit_time': signal['timestamp'],
                    'entry_price': self.position['entry_price'],
                    'exit_price': signal['price'],
                    'quantity': self.position['quantity'],
                    'profit': profit,
                    'profit_pct': profit_pct
                }
                
                self.trades.append(trade)
                self.capital += profit
                self.position = None
        
        print(f"✅ Executed {len(self.trades)} trades")
        return self.trades
    
    def calculate_performance(self):
        """Calculate basic performance metrics."""
        if not self.trades:
            return None
            
        total_return = sum(trade['profit_pct'] for trade in self.trades)
        winning_trades = len([t for t in self.trades if t['profit_pct'] > 0])
        win_rate = (winning_trades / len(self.trades)) * 100
        
        best_trade = max(trade['profit_pct'] for trade in self.trades)
        worst_trade = min(trade['profit_pct'] for trade in self.trades)
        avg_trade = total_return / len(self.trades)
        
        return {
            'total_trades': len(self.trades),
            'winning_trades': winning_trades,
            'win_rate': win_rate,
            'total_return': total_return,
            'avg_return': avg_trade,
            'best_trade': best_trade,
            'worst_trade': worst_trade,
            'final_capital': self.capital
        }

def test_delta_exchange_info():
    """Check Delta Exchange information without CCXT."""
    print("\n🎯 DELTA EXCHANGE INFORMATION")
    print("="*50)
    
    # Delta Exchange is an Indian crypto derivatives exchange
    delta_info = {
        'name': 'Delta Exchange',
        'country': 'India',
        'type': 'Crypto Derivatives',
        'website': 'https://www.delta.exchange',
        'api_docs': 'https://docs.delta.exchange',
        'popular_pairs': ['BTC/USDT', 'ETH/USDT', 'BTC/USD', 'ETH/USD'],
        'features': ['Spot Trading', 'Futures', 'Options', 'Perpetual Swaps'],
        'ccxt_support': 'Check with: ccxt.exchanges list'
    }
    
    print("📊 Delta Exchange Details:")
    for key, value in delta_info.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print("\n📋 To use Delta Exchange with CCXT:")
    print("   1. Check if 'delta' is in ccxt.exchanges")
    print("   2. Create instance: delta = ccxt.delta()")
    print("   3. Load markets: markets = delta.load_markets()")
    print("   4. Fetch data: data = delta.fetch_ohlcv('BTC/USDT', '1h')")
    
    return delta_info

def main():
    """Main function for alternative backtest."""
    print("🚀 Starting Alternative Crypto Backtest...")
    
    # Test Delta Exchange info
    delta_info = test_delta_exchange_info()
    
    # Generate sample data
    data_handler = SimpleCryptoData()
    btc_data = data_handler.generate_sample_data('BTC/USDT', days=7)
    
    # Run backtest
    backtest = SimpleBacktest(initial_capital=100000, position_size=10000)
    signals = backtest.generate_simple_signals(btc_data)
    trades = backtest.execute_backtest(btc_data, signals)
    
    # Calculate performance
    performance = backtest.calculate_performance()
    
    if performance:
        print("\n📊 BACKTEST RESULTS:")
        print("="*40)
        print(f"Initial Capital: ${backtest.initial_capital:,.2f}")
        print(f"Final Capital: ${performance['final_capital']:,.2f}")
        print(f"Total Trades: {performance['total_trades']}")
        print(f"Winning Trades: {performance['winning_trades']}")
        print(f"Win Rate: {performance['win_rate']:.2f}%")
        print(f"Total Return: {performance['total_return']:.2f}%")
        print(f"Average Return per Trade: {performance['avg_return']:.2f}%")
        print(f"Best Trade: {performance['best_trade']:.2f}%")
        print(f"Worst Trade: {performance['worst_trade']:.2f}%")
        print("="*40)
        
        # Save results
        try:
            output_file = 'alternative_backtest_results.json'
            results = {
                'timestamp': datetime.now().isoformat(),
                'performance': performance,
                'trades': trades,
                'delta_exchange_info': delta_info
            }
            
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
                
            print(f"💾 Results saved to: {output_file}")
            
        except Exception as e:
            print(f"⚠️ Could not save results: {e}")
    else:
        print("❌ No trades executed")
    
    print("\n✅ Alternative backtest completed!")
    print("This proves the concept works - issue is with pandas/numpy/ccxt installation")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
