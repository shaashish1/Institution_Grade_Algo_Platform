#!/usr/bin/env python3
"""
Simplified Enhanced Crypto Backtest - Debug Version
Fixed version to avoid hanging and path issues
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import argparse
import time

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

print(f"🔧 Python path: {parent_dir}")

# Import required modules
try:
    from crypto.data_acquisition import fetch_data
    from crypto.tools.backtest_evaluator import BacktestEvaluator
    from strategies.rsi_macd_vwap_strategy import RSI_MACD_VWAP_Strategy
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class SimpleEnhancedCryptoBacktest:
    """Simplified version for testing and debugging"""

    def __init__(self, initial_capital=100000, position_size=10000, bars=720, interval='1h', exchange='kraken', strategy='RSI_MACD_VWAP'):
        self.initial_capital = initial_capital
        self.position_size = position_size
        self.bars = bars
        self.interval = interval
        self.exchange = exchange
        self.strategy = strategy

    def load_crypto_assets(self):
        """Load crypto assets from configuration."""
        try:
            assets_file = os.path.join(os.path.dirname(__file__), '..', 'input', 'crypto_assets.csv')
            if os.path.exists(assets_file):
                df = pd.read_csv(assets_file)
                assets = df['symbol'].tolist()
                print(f"✅ Loaded {len(assets)} crypto assets from {assets_file}")
                return assets[:5]  # Limit to first 5 for testing
            else:
                print(f"⚠️ crypto_assets.csv not found, using defaults")
                return ['BTC/USDT', 'ETH/USDT']
        except Exception as e:
            print(f"⚠️ Error loading crypto assets: {e}")
            return ['BTC/USDT', 'ETH/USDT']

    def calculate_indicators(self, data):
        """Calculate basic technical indicators."""
        try:
            # RSI
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['rsi'] = 100 - (100 / (1 + rs))

            # Simple MACD
            exp1 = data['close'].ewm(span=12).mean()
            exp2 = data['close'].ewm(span=26).mean()
            data['macd'] = exp1 - exp2
            data['macd_signal'] = data['macd'].ewm(span=9).mean()
            
            return data
        except Exception as e:
            print(f"❌ Error calculating indicators: {e}")
            return data

    def generate_simple_signals(self, data):
        """Generate simple RSI-based signals."""
        try:
            signals = []
            
            for i in range(20, len(data)):  # Skip first 20 bars for indicator calculation
                current = data.iloc[i]
                
                if pd.isna(current['rsi']) or pd.isna(current['macd']):
                    continue
                
                signal_type = 'hold'
                signal_strength = 1
                
                # Simple RSI signals
                if current['rsi'] < 30:  # Oversold
                    signal_type = 'buy'
                    signal_strength = 3
                elif current['rsi'] > 70:  # Overbought
                    signal_type = 'sell'
                    signal_strength = 3
                
                signals.append({
                    'timestamp': data.index[i],
                    'signal': signal_type,
                    'score': signal_strength,
                    'price': current['close'],
                    'rsi': current['rsi'],
                    'macd': current['macd']
                })
            
            return pd.DataFrame(signals)
        except Exception as e:
            print(f"❌ Error generating signals: {e}")
            return pd.DataFrame()

    def backtest_with_signals(self, data, signals, symbol):
        """Perform simple backtest."""
        try:
            if signals.empty:
                return None
            
            # Simple backtest logic
            position = None
            trades = []
            
            for _, signal in signals.iterrows():
                if signal['signal'] == 'buy' and position is None:
                    position = {
                        'entry_price': signal['price'],
                        'entry_time': signal['timestamp'],
                        'quantity': self.position_size / signal['price']
                    }
                elif signal['signal'] == 'sell' and position is not None:
                    profit = (signal['price'] - position['entry_price']) * position['quantity']
                    profit_percent = ((signal['price'] - position['entry_price']) / position['entry_price']) * 100
                    
                    trades.append({
                        'symbol': symbol,
                        'entry_time': position['entry_time'],
                        'exit_time': signal['timestamp'],
                        'entry_price': position['entry_price'],
                        'exit_price': signal['price'],
                        'profit_percent': profit_percent
                    })
                    position = None
            
            if not trades:
                return None
            
            # Calculate metrics
            trades_df = pd.DataFrame(trades)
            total_trades = len(trades)
            winning_trades = len(trades_df[trades_df['profit_percent'] > 0])
            win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
            total_return = trades_df['profit_percent'].sum()
            
            return {
                'symbol': symbol,
                'strategy': self.strategy,
                'timeframe': self.interval,
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'win_rate': win_rate,
                'total_return': total_return,
                'trades': trades
            }
        except Exception as e:
            print(f"❌ Error in backtest: {e}")
            return None

    def process_symbol(self, symbol):
        """Process a single symbol."""
        print(f"📊 Processing {symbol}...", end=" ")
        
        try:
            # Fetch data with timeout
            print("fetching data...", end=" ")
            data = fetch_data(
                symbol=symbol,
                bars=self.bars,
                interval=self.interval,
                exchange=self.exchange
            )
            
            if data is None or len(data) < 50:
                print("❌ insufficient data")
                return None
            
            print(f"got {len(data)} bars...", end=" ")
            
            # Calculate indicators
            data = self.calculate_indicators(data)
            
            # Generate signals
            signals = self.generate_simple_signals(data)
            
            if signals.empty:
                print("❌ no signals")
                return None
            
            # Run backtest
            result = self.backtest_with_signals(data, signals, symbol)
            
            if result is None:
                print("❌ no trades")
                return None
            
            print(f"✅ {result['total_trades']} trades, {result['win_rate']:.1f}% win rate")
            return result
            
        except Exception as e:
            print(f"❌ error: {e}")
            return None

    def run_backtest(self, symbols=None):
        """Run backtest on specified symbols."""
        if symbols is None:
            symbols = self.load_crypto_assets()
        
        print("🚀 Simple Enhanced Crypto Backtest")
        print("=" * 60)
        print(f"Strategy: {self.strategy}")
        print(f"Timeframe: {self.interval}")
        print(f"Bars: {self.bars}")
        print(f"Exchange: {self.exchange}")
        print(f"Testing {len(symbols)} symbols")
        print("=" * 60)
        
        results = []
        
        for symbol in symbols:
            try:
                result = self.process_symbol(symbol)
                if result:
                    results.append(result)
            except Exception as e:
                print(f"❌ Error processing {symbol}: {e}")
                continue
        
        if not results:
            print("❌ No results to analyze!")
            return
        
        # Generate summary
        print("\n" + "="*60)
        print("📈 SUMMARY")
        print("="*60)
        
        total_trades = sum(r['total_trades'] for r in results)
        avg_win_rate = np.mean([r['win_rate'] for r in results])
        avg_return = np.mean([r['total_return'] for r in results])
        
        print(f"Symbols processed: {len(results)}")
        print(f"Total trades: {total_trades}")
        print(f"Average win rate: {avg_win_rate:.2f}%")
        print(f"Average return: {avg_return:.2f}%")
        
        # Top performers
        sorted_results = sorted(results, key=lambda x: x['total_return'], reverse=True)
        print(f"\n🏆 Top 3 performers:")
        for i, result in enumerate(sorted_results[:3], 1):
            print(f"{i}. {result['symbol']}: {result['total_return']:.2f}% ({result['total_trades']} trades)")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Simple Enhanced Crypto Backtest')
    
    parser.add_argument('--symbols', '-s', nargs='+', help='Symbols to test')
    parser.add_argument('--capital', '-c', type=float, default=100000, help='Initial capital')
    parser.add_argument('--position', '-p', type=float, default=10000, help='Position size per trade')
    parser.add_argument('--bars', '-b', type=int, default=720, help='Number of bars to fetch')
    parser.add_argument('--interval', '-i', type=str, default='1h', help='Time interval')
    parser.add_argument('--exchange', '-e', type=str, default='kraken', help='Exchange')
    parser.add_argument('--strategy', '-st', type=str, default='RSI_MACD_VWAP', help='Strategy')
    
    args = parser.parse_args()
    
    print("🚀 Starting Simple Enhanced Crypto Backtest...")
    
    try:
        backtest = SimpleEnhancedCryptoBacktest(
            initial_capital=args.capital,
            position_size=args.position,
            bars=args.bars,
            interval=args.interval,
            exchange=args.exchange,
            strategy=args.strategy
        )
        
        backtest.run_backtest(args.symbols)
        print("\n✅ Backtest completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during backtest: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
