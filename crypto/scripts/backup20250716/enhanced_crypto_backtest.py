#!/usr/bin/env python3
"""
Enhanced Crypto Backtest with Comprehensive KPIs
Integrates advanced BacktestEvaluator for professional-grade performance analysis
"""

import os
import sys
import yaml
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import warnings
import argparse
import time
import json
from collections import defaultdict
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import crypto-specific data acquisition (no stock dependencies)
from crypto.data_acquisition import fetch_data
from tabulate import tabulate
from crypto.tools.backtest_evaluator import BacktestEvaluator
from strategies.enhanced_multi_factor import EnhancedMultiFactorStrategy
from strategies.optimized_crypto_v2 import OptimizedCryptoStrategy
from strategies.bb_rsi_strategy import BB_RSI_Strategy
from strategies.macd_only_strategy import MACD_Only_Strategy
from strategies.rsi_macd_vwap_strategy import RSI_MACD_VWAP_Strategy

try:
    from colorama import Fore, Style, init
    COLORAMA_AVAILABLE = False  # Disabled for stability
except ImportError:
    COLORAMA_AVAILABLE = False


class EnhancedCryptoBacktest:
    """Enhanced crypto backtest with comprehensive KPIs and professional analysis"""

    def __init__(self, initial_capital=100000, position_size=10000, bars=720, interval='1h', exchange='kraken', strategy='RSI_MACD_VWAP', verbose=False):
        self.initial_capital = initial_capital
        self.position_size = position_size
        self.bars = bars
        self.interval = interval
        self.exchange = exchange
        self.strategy = strategy
        self.verbose = verbose
        self.evaluators = {}  # Store evaluator for each symbol
        self.ist = pytz.timezone('Asia/Kolkata')

    def load_crypto_assets(self):
        """Load crypto assets from configuration."""
        try:
            # Correct path to crypto_assets.csv
            assets_file = os.path.join(os.path.dirname(__file__), '..', 'input', 'crypto_assets.csv')
            if not os.path.exists(assets_file):
                # Default crypto assets
                print(f"WARNING: crypto_assets.csv not found at {assets_file}")
                return ['BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'DOT/USDT', 'SOL/USDT']

            df = pd.read_csv(assets_file)
            assets = df['symbol'].tolist()
            print(f"Loaded {len(assets)} crypto assets from {assets_file}")
            return assets
        except Exception as e:
            print(f"WARNING: Error loading crypto assets: {e}")
            return ['BTC/USDT', 'ETH/USDT']

    def load_strategy_config(self):
        """Load strategy configuration."""
        try:
            config_file = os.path.join(os.path.dirname(__file__), '..', 'input', 'config_crypto.yaml')
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            return config.get('strategy', {})
        except Exception as e:
            print(f"WARNING: Error loading strategy config: {e}")
            return {}

    def calculate_indicators(self, data):
        """Calculate technical indicators."""
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
        data['macd_histogram'] = data['macd'] - data['macd_signal']

        # VWAP
        typical_price = (data['high'] + data['low'] + data['close']) / 3
        data['vwap'] = (typical_price * data['volume']).cumsum() / data['volume'].cumsum()

        # Bollinger Bands
        data['bb_middle'] = data['close'].rolling(window=20).mean()
        bb_std = data['close'].rolling(window=20).std()
        data['bb_upper'] = data['bb_middle'] + (bb_std * 2)
        data['bb_lower'] = data['bb_middle'] - (bb_std * 2)

        return data

    def generate_signals_rsi_macd_vwap(self, data):
        """Generate signals using RSI, MACD, and VWAP strategy."""
        try:
            # Use the strategy from strategies folder
            strategy = RSI_MACD_VWAP_Strategy()
            signals_df = strategy.generate_signals(data)

            # Convert to expected format if not empty
            if not signals_df.empty:
                # Ensure all required columns exist
                if 'rsi' not in signals_df.columns:
                    signals_df['rsi'] = np.nan
                if 'macd' not in signals_df.columns:
                    signals_df['macd'] = np.nan
                if 'score' not in signals_df.columns:
                    signals_df['score'] = 3
                    
                # Ensure timestamp column exists
                if 'timestamp' not in signals_df.columns and signals_df.index.name != 'timestamp':
                    signals_df['timestamp'] = signals_df.index

                return signals_df
            else:
                return pd.DataFrame()

        except Exception as e:
            print(f"WARNING: Error generating RSI_MACD_VWAP signals: {e}")
            # Fallback to simple implementation
            return self.generate_simple_signals(data, 'RSI_MACD_VWAP')

    def generate_signals_sma_cross(self, data):
        """Generate signals using SMA crossover strategy."""
        try:
            # Calculate SMAs
            data['sma_fast'] = data['close'].rolling(window=10).mean()
            data['sma_slow'] = data['close'].rolling(window=30).mean()

            # Calculate RSI for additional confirmation
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['rsi'] = 100 - (100 / (1 + rs))

            signals = []

            # Generate signals with crossover detection
            for i in range(31, len(data)):  # Start after SMA calculation period
                current = data.iloc[i]
                prev = data.iloc[i-1]
                
                # Check for valid data
                if pd.isna(current['sma_fast']) or pd.isna(current['sma_slow']):
                    continue
                
                signal_strength = 0
                signal_type = 'hold'
                
                # Bullish crossover: fast SMA crosses above slow SMA
                if (current['sma_fast'] > current['sma_slow'] and 
                    prev['sma_fast'] <= prev['sma_slow']):
                    signal_type = 'buy'
                    signal_strength = 3  # Strong signal
                    
                    # Additional confirmation with RSI
                    if not pd.isna(current['rsi']) and current['rsi'] < 70:
                        signal_strength = 4  # Very strong signal
                
                # Bearish crossover: fast SMA crosses below slow SMA
                elif (current['sma_fast'] < current['sma_slow'] and 
                      prev['sma_fast'] >= prev['sma_slow']):
                    signal_type = 'sell'
                    signal_strength = 3  # Strong signal
                    
                    # Additional confirmation with RSI
                    if not pd.isna(current['rsi']) and current['rsi'] > 30:
                        signal_strength = 4  # Very strong signal

                signals.append({
                    'timestamp': data.index[i],
                    'signal': signal_type,
                    'score': signal_strength,
                    'price': current['close'],
                    'sma_fast': current['sma_fast'],
                    'sma_slow': current['sma_slow'],
                    'rsi': current['rsi'] if not pd.isna(current['rsi']) else 50,
                    'macd': np.nan
                })

            return pd.DataFrame(signals)

        except Exception as e:
            print(f"WARNING: Error generating SMA_Cross signals: {e}")
            return pd.DataFrame()

    def generate_signals_bb_rsi(self, data):
        """Generate signals using Bollinger Bands and RSI strategy."""
        try:
            # Use the strategy from strategies folder
            strategy = BB_RSI_Strategy()
            signals_df = strategy.generate_signals(data)

            # Convert to expected format if not empty
            if not signals_df.empty:
                # Ensure all required columns exist
                if 'rsi' not in signals_df.columns:
                    signals_df['rsi'] = np.nan
                if 'macd' not in signals_df.columns:
                    signals_df['macd'] = np.nan
                if 'score' not in signals_df.columns:
                    signals_df['score'] = 3
                    
                # Ensure timestamp column exists
                if 'timestamp' not in signals_df.columns and signals_df.index.name != 'timestamp':
                    signals_df['timestamp'] = signals_df.index

                return signals_df
            else:
                return pd.DataFrame()

        except Exception as e:
            print(f"WARNING: Error generating BB_RSI signals: {e}")
            # Fallback to simple implementation
            return self.generate_simple_signals(data, 'BB_RSI')

    def generate_signals_macd_only(self, data):
        """Generate signals using MACD only strategy."""
        try:
            # Use the strategy from strategies folder
            strategy = MACD_Only_Strategy()
            signals_df = strategy.generate_signals(data)

            # Convert to expected format if not empty
            if not signals_df.empty:
                # Ensure all required columns exist
                if 'rsi' not in signals_df.columns:
                    signals_df['rsi'] = np.nan
                if 'macd' not in signals_df.columns:
                    signals_df['macd'] = np.nan
                if 'score' not in signals_df.columns:
                    signals_df['score'] = 3
                    
                # Ensure timestamp column exists
                if 'timestamp' not in signals_df.columns and signals_df.index.name != 'timestamp':
                    signals_df['timestamp'] = signals_df.index

                return signals_df
            else:
                return pd.DataFrame()

        except Exception as e:
            print(f"WARNING: Error generating MACD_Only signals: {e}")
            # Fallback to simple implementation
            return self.generate_simple_signals(data, 'MACD_Only')

    def generate_signals_enhanced_multi_factor(self, data):
        """Generate signals using Enhanced Multi-Factor strategy."""
        try:
            # Use the strategy from strategies folder
            strategy = EnhancedMultiFactorStrategy()
            signals_df = strategy.generate_signals(data)

            # Convert to expected format if not empty
            if not signals_df.empty:
                # Ensure all required columns exist
                if 'rsi' not in signals_df.columns:
                    signals_df['rsi'] = np.nan
                if 'macd' not in signals_df.columns:
                    signals_df['macd'] = np.nan
                if 'score' not in signals_df.columns:
                    signals_df['score'] = 3
                    
                # Ensure timestamp column exists
                if 'timestamp' not in signals_df.columns and signals_df.index.name != 'timestamp':
                    signals_df['timestamp'] = signals_df.index

                return signals_df
            else:
                return pd.DataFrame()

        except Exception as e:
            print(f"WARNING: Error generating Enhanced_Multi_Factor signals: {e}")
            # Fallback to RSI_MACD_VWAP for multi-factor
            return self.generate_simple_signals(data, 'RSI_MACD_VWAP')

    def generate_signals_optimized_crypto_v2(self, data):
        """Generate signals using Optimized Crypto V2 strategy."""
        try:
            # Use the strategy from strategies folder
            strategy = OptimizedCryptoStrategy()
            signals_df = strategy.generate_signals(data)

            # Convert to expected format if not empty
            if not signals_df.empty:
                # Ensure all required columns exist
                if 'rsi' not in signals_df.columns:
                    signals_df['rsi'] = np.nan
                if 'macd' not in signals_df.columns:
                    signals_df['macd'] = np.nan
                if 'score' not in signals_df.columns:
                    signals_df['score'] = 3
                    
                # Ensure timestamp column exists
                if 'timestamp' not in signals_df.columns and signals_df.index.name != 'timestamp':
                    signals_df['timestamp'] = signals_df.index

                return signals_df
            else:
                return pd.DataFrame()

        except Exception as e:
            print(f"WARNING: Error generating Optimized_Crypto_V2 signals: {e}")
            # Fallback to RSI_MACD_VWAP for optimized crypto
            return self.generate_simple_signals(data, 'RSI_MACD_VWAP')

    def generate_simple_signals(self, data, strategy_name):
        """Fallback simple signal generation when strategy classes fail."""
        try:
            signals = []
            
            if strategy_name == 'RSI_MACD_VWAP':
                # Simple RSI + MACD + VWAP signals
                for i in range(50, len(data)):
                    current = data.iloc[i]
                    
                    if pd.isna(current['rsi']) or pd.isna(current['macd']) or pd.isna(current['vwap']):
                        continue
                        
                    # Buy signal: RSI oversold + MACD positive + Price below VWAP
                    if (current['rsi'] < 35 and current['macd'] > current['macd_signal'] and 
                        current['close'] < current['vwap']):
                        signals.append({
                            'timestamp': data.index[i],
                            'signal': 'buy',
                            'price': current['close'],
                            'rsi': current['rsi'],
                            'macd': current['macd'],
                            'score': 3
                        })
                    
                    # Sell signal: RSI overbought + MACD negative + Price above VWAP  
                    elif (current['rsi'] > 65 and current['macd'] < current['macd_signal'] and
                          current['close'] > current['vwap']):
                        signals.append({
                            'timestamp': data.index[i],
                            'signal': 'sell',
                            'price': current['close'],
                            'rsi': current['rsi'],
                            'macd': current['macd'],
                            'score': 3
                        })
                        
            elif strategy_name == 'BB_RSI':
                # Simple Bollinger Bands + RSI signals
                for i in range(30, len(data)):
                    current = data.iloc[i]
                    
                    if pd.isna(current['rsi']) or pd.isna(current['bb_lower']) or pd.isna(current['bb_upper']):
                        continue
                        
                    # Buy signal: Price at lower BB + RSI oversold
                    if current['close'] <= current['bb_lower'] and current['rsi'] < 30:
                        signals.append({
                            'timestamp': data.index[i],
                            'signal': 'buy',
                            'price': current['close'],
                            'rsi': current['rsi'],
                            'macd': np.nan,
                            'score': 3
                        })
                    
                    # Sell signal: Price at upper BB + RSI overbought
                    elif current['close'] >= current['bb_upper'] and current['rsi'] > 70:
                        signals.append({
                            'timestamp': data.index[i],
                            'signal': 'sell',
                            'price': current['close'],
                            'rsi': current['rsi'],
                            'macd': np.nan,
                            'score': 3
                        })
                        
            elif strategy_name == 'MACD_Only':
                # Simple MACD crossover signals
                for i in range(30, len(data)):
                    current = data.iloc[i]
                    prev = data.iloc[i-1]
                    
                    if pd.isna(current['macd']) or pd.isna(current['macd_signal']):
                        continue
                        
                    # Buy signal: MACD crosses above signal
                    if (current['macd'] > current['macd_signal'] and 
                        prev['macd'] <= prev['macd_signal']):
                        signals.append({
                            'timestamp': data.index[i],
                            'signal': 'buy',
                            'price': current['close'],
                            'rsi': np.nan,
                            'macd': current['macd'],
                            'score': 3
                        })
                    
                    # Sell signal: MACD crosses below signal
                    elif (current['macd'] < current['macd_signal'] and 
                          prev['macd'] >= prev['macd_signal']):
                        signals.append({
                            'timestamp': data.index[i],
                            'signal': 'sell',
                            'price': current['close'],
                            'rsi': np.nan,
                            'macd': current['macd'],
                            'score': 3
                        })
                        
            return pd.DataFrame(signals)
            
        except Exception as e:
            print(f"ERROR in simple signal generation: {e}")
            return pd.DataFrame()

    def process_symbol(self, symbol):
        """Process a single symbol and return analysis."""
        print(f"Processing {symbol}...", end=" ")
        
        try:
            # Fetch data with retry logic and timeout
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"fetching data (attempt {attempt + 1})...", end=" ")
                    data = fetch_data(
                        symbol=symbol, 
                        bars=self.bars, 
                        interval=self.interval,
                        exchange=self.exchange,
                        fetch_timeout=10  # 10 second timeout
                    )
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"retry...", end=" ")
                        time.sleep(1)  # Wait before retry
                        continue
                    else:
                        raise e
            
            if data is None or len(data) < 50:
                print("Insufficient data")
                return None
            
            print(f"got {len(data)} bars...", end=" ")
            
            # Calculate technical indicators
            print("calculating indicators...", end=" ")
            data = self.calculate_indicators(data)
            
            # Generate signals based on strategy
            print("generating signals...", end=" ")
            if self.strategy == 'RSI_MACD_VWAP':
                signals = self.generate_signals_rsi_macd_vwap(data)
            elif self.strategy == 'SMA_Cross':
                signals = self.generate_signals_sma_cross(data)
            elif self.strategy == 'BB_RSI':
                signals = self.generate_signals_bb_rsi(data)
            elif self.strategy == 'MACD_Only':
                signals = self.generate_signals_macd_only(data)
            elif self.strategy == 'Enhanced_Multi_Factor':
                signals = self.generate_signals_enhanced_multi_factor(data)
            elif self.strategy == 'Optimized_Crypto_V2':
                signals = self.generate_signals_optimized_crypto_v2(data)
            else:
                # Default to RSI_MACD_VWAP
                signals = self.generate_signals_rsi_macd_vwap(data)
            
            if signals.empty:
                print("No signals generated")
                return None
            
            print(f"got {len(signals)} signals...", end=" ")
            
            # Perform backtest
            print("running backtest...", end=" ")
            result = self.backtest_with_signals(data, signals, symbol)
            
            if result is None:
                print("No trades executed")
                return None
            
            print(f"Complete - {result['total_trades']} trades")
            return result
            
        except Exception as e:
            print(f"Error: {e}")
            return None

    def backtest_with_signals(self, data, signals, symbol):
        """Perform backtest using generated signals."""
        try:
            # Initialize evaluator
            evaluator = BacktestEvaluator(
                strategy_name=self.strategy,
                symbol=symbol,
                initial_capital=self.initial_capital
            )
            
            # Store evaluator for later use
            self.evaluators[symbol] = evaluator
            
            # Execute trades based on signals
            position = None
            trades = []
            
            for _, signal in signals.iterrows():
                current_price = signal['price']
                signal_type = signal['signal']
                timestamp = signal['timestamp']
                
                if signal_type == 'buy' and position is None:
                    # Enter long position
                    position = {
                        'type': 'long',
                        'entry_price': current_price,
                        'entry_time': timestamp,
                        'quantity': self.position_size / current_price
                    }
                    
                elif signal_type == 'sell' and position is not None:
                    # Exit position
                    if position['type'] == 'long':
                        profit = (current_price - position['entry_price']) * position['quantity']
                        profit_percent = ((current_price - position['entry_price']) / position['entry_price']) * 100
                        
                        trade = {
                            'symbol': symbol,
                            'entry_time': position['entry_time'],
                            'exit_time': timestamp,
                            'entry_price': position['entry_price'],
                            'exit_price': current_price,
                            'quantity': position['quantity'],
                            'profit': profit,
                            'profit_percent': profit_percent,
                            'type': position['type']
                        }
                        trades.append(trade)
                        
                        # Update evaluator with correct interface
                        evaluator.add_trade({
                            'entry_time': position['entry_time'],
                            'exit_time': timestamp,
                            'entry_price': position['entry_price'],
                            'exit_price': current_price,
                            'position_size': position['quantity'],
                            'trade_type': 'Long',
                            'pnl_dollars': profit,
                            'pnl_percent': profit_percent
                        })
                        
                        position = None
            
            if not trades:
                return None
            
            # Calculate performance metrics
            trades_df = pd.DataFrame(trades)
            
            total_trades = len(trades)
            winning_trades = len(trades_df[trades_df['profit_percent'] > 0])
            losing_trades = len(trades_df[trades_df['profit_percent'] < 0])
            
            win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
            total_return = trades_df['profit_percent'].sum()
            avg_return = trades_df['profit_percent'].mean()
            
            max_win = trades_df['profit_percent'].max()
            max_loss = trades_df['profit_percent'].min()
            
            # Get evaluator metrics
            evaluator_metrics = evaluator.get_performance_summary()
            
            result = {
                'symbol': symbol,
                'strategy': self.strategy,
                'timeframe': self.interval,
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': losing_trades,
                'win_rate': win_rate,
                'total_return': total_return,
                'avg_return': avg_return,
                'max_win': max_win,
                'max_loss': max_loss,
                'sharpe_ratio': evaluator_metrics.get('sharpe_ratio', 0),
                'max_drawdown': evaluator_metrics.get('max_drawdown_percent', 0),
                'trades': trades
            }
            
            return result
            
        except Exception as e:
            print(f"ERROR in backtest: {e}")
            return None

    def run_backtest(self, symbols=None):
        """Run backtest on specified symbols."""
        if symbols is None:
            symbols = self.load_crypto_assets()
        
        print("Enhanced Crypto Backtest with Comprehensive KPIs")
        print("=" * 80)
        print(f" Initial Capital: ${self.initial_capital:,.2f}")
        print(f" Position Size: ${self.position_size:,.2f} per trade")
        print(f" Scanning {len(symbols)} crypto symbols")
        print(f" Strategy: {self.strategy}")
        print(f" Timeframe: {self.interval}")
        print(f" Bars: {self.bars}")
        print(f" Exchange: {self.exchange}")
        print("=" * 80)
        
        results = []
        all_trades = []
        
        for symbol in symbols:
            try:
                result = self.process_symbol(symbol)
                if result:
                    results.append(result)
                    all_trades.extend(result['trades'])
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                continue
        
        if not results:
            print("No results to analyze!")
            return [], []  # Return empty lists instead of None
        
        # Generate summary
        self.generate_summary(results, all_trades)
        
        return results, all_trades

    def generate_summary(self, results, all_trades):
        """Generate comprehensive summary of backtest results."""
        print("\n" + "="*80)
        print("BACKTEST SUMMARY")
        print("="*80)
        
        total_symbols = len(results)
        total_trades = len(all_trades)
        
        if total_trades == 0:
            print("No trades executed!")
            return
        
        # Overall metrics
        all_returns = [trade['profit_percent'] for trade in all_trades]
        winning_trades = len([r for r in all_returns if r > 0])
        losing_trades = len([r for r in all_returns if r < 0])
        
        overall_win_rate = (winning_trades / total_trades) * 100
        total_return = sum(all_returns)
        avg_return = np.mean(all_returns)
        
        print(f"Symbols Analyzed: {total_symbols}")
        print(f"Total Trades: {total_trades}")
        print(f"Winning Trades: {winning_trades}")
        print(f"Losing Trades: {losing_trades}")
        print(f"Win Rate: {overall_win_rate:.2f}%")
        print(f"Total Return: {total_return:.2f}%")
        print(f"Average Return per Trade: {avg_return:.2f}%")
        print(f"Best Trade: {max(all_returns):.2f}%")
        print(f"Worst Trade: {min(all_returns):.2f}%")
        
        # Top performing symbols
        print("\nTOP 5 PERFORMING SYMBOLS:")
        sorted_results = sorted(results, key=lambda x: x['total_return'], reverse=True)[:5]
        for i, result in enumerate(sorted_results, 1):
            print(f"{i}. {result['symbol']}: {result['total_return']:.2f}% ({result['total_trades']} trades)")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Enhanced Crypto Backtest with Comprehensive KPIs')
    
    parser.add_argument(
        '--symbols', '-s',
        nargs='+',
        help='Symbols to test (default: auto-load from crypto_assets.csv)'
    )
    
    parser.add_argument(
        '--capital', '-c',
        type=float,
        help='Initial capital (default: 100000)',
        default=100000
    )
    
    parser.add_argument(
        '--position', '-p',
        type=float,
        help='Position size per trade (default: 10000)',
        default=10000
    )
    
    parser.add_argument(
        '--bars', '-b',
        type=int,
        help='Number of bars to fetch (default: 720)',
        default=720
    )
    
    parser.add_argument(
        '--interval', '-i',
        type=str,
        help='Time interval for data (default: 1h)',
        choices=['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d'],
        default='1h'
    )
    
    parser.add_argument(
        '--exchange', '-e',
        type=str,
        help='Exchange to use for data (default: kraken)',
        choices=['binance', 'kraken', 'coinbase', 'bitfinex'],
        default='kraken'
    )
    
    parser.add_argument(
        '--strategy', '-st',
        type=str,
        help='Strategy to use (default: RSI_MACD_VWAP)',
        choices=['RSI_MACD_VWAP', 'SMA_Cross', 'BB_RSI', 'MACD_Only', 'Enhanced_Multi_Factor', 'Optimized_Crypto_V2'],
        default='RSI_MACD_VWAP'
    )
    
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Enable comprehensive strategy comparison mode (tests all strategies across all timeframes)'
    )
    
    parser.add_argument(
        '--timeframes', '-tf',
        nargs='+',
        help='Timeframes to test (default: 1h 4h 1d)',
        choices=['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d'],
        default=['1h', '4h', '1d']
    )
    
    parser.add_argument(
        '--strategies', '-sts',
        nargs='+',
        help='Strategies to test (default: all strategies)',
        choices=['RSI_MACD_VWAP', 'SMA_Cross', 'BB_RSI', 'MACD_Only', 'Enhanced_Multi_Factor', 'Optimized_Crypto_V2'],
        default=['RSI_MACD_VWAP', 'SMA_Cross', 'BB_RSI', 'MACD_Only', 'Enhanced_Multi_Factor', 'Optimized_Crypto_V2']
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output directory for results (default: crypto/output)',
        default='crypto/output'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def main():
    """Main function to run the enhanced crypto backtest."""
    args = parse_arguments()

    print("Enhanced Crypto Backtest with Comprehensive KPIs")
    print("=" * 80)

    # Check if comprehensive comparison mode is requested
    if args.compare:
        print("🚀 COMPREHENSIVE STRATEGY COMPARISON MODE")
        print("=" * 80)
        
        # Initialize comprehensive runner
        runner = ComprehensiveBacktestRunner(
            initial_capital=args.capital,
            position_size=args.position,
            bars=args.bars,
            exchange=args.exchange
        )
        
        # Use specific symbols if provided
        if args.symbols:
            crypto_symbols = args.symbols
            print(f" Using specific symbols: {', '.join(crypto_symbols)}")
        else:
            crypto_symbols = None  # Will auto-load in runner
            
        print(f" Initial Capital: ${args.capital:,.2f}")
        print(f" Position Size: ${args.position:,.2f} per trade")
        print(f" Strategies: {', '.join(args.strategies)}")
        print(f" Timeframes: {', '.join(args.timeframes)}")
        print(f" Exchange: {args.exchange}")
        print(f" Bars per test: {args.bars}")
        print("=" * 80)
        
        try:
            # Run comprehensive backtest
            results = runner.run_comprehensive_backtest(
                symbols=crypto_symbols,
                strategies=args.strategies,
                timeframes=args.timeframes
            )
            
            if results:
                # Generate comprehensive summary
                summary_df = runner.generate_comprehensive_summary()
                print("\n✅ Comprehensive backtest completed successfully!")
                return 0
            else:
                print("\n❌ No successful backtests completed.")
                return 1
                
        except Exception as e:
            print(f"\n❌ Error during comprehensive backtest: {e}")
            return 1
    
    else:
        # Single strategy mode (original functionality)
        backtest = EnhancedCryptoBacktest(
            initial_capital=args.capital,
            position_size=args.position,
            bars=args.bars,
            interval=args.interval,
            exchange=args.exchange,
            strategy=args.strategy,
            verbose=args.verbose
        )

        # Use specific symbols if provided
        if args.symbols:
            crypto_symbols = args.symbols
            print(f" Using specific symbols: {', '.join(crypto_symbols)}")
        else:
            crypto_symbols = backtest.load_crypto_assets()

        print(f" Initial Capital: ${backtest.initial_capital:,.2f}")
        print(f" Position Size: ${backtest.position_size:,.2f} per trade")
        print(f" Scanning {len(crypto_symbols)} crypto symbols")
        print(f" Strategy: {backtest.strategy}")
        print(f" Timeframe: {backtest.interval}")
        print(f" Exchange: {backtest.exchange}")
        print("=" * 80)

        try:
            # Run backtest
            results, trades = backtest.run_backtest(crypto_symbols)
            
            if results:
                print("\nBacktest completed successfully!")
                
                # Save results if output directory specified
                if args.output and args.output != 'output':
                    os.makedirs(args.output, exist_ok=True)
                    
                    # Save summary
                    summary_data = []
                    for result in results:
                        summary_data.append({
                            'symbol': result['symbol'],
                            'strategy': result['strategy'],
                            'timeframe': result['timeframe'],
                            'total_trades': result['total_trades'],
                            'win_rate': result['win_rate'],
                            'total_return': result['total_return'],
                            'avg_return': result['avg_return']
                        })
                    
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_csv(os.path.join(args.output, 'summary.csv'), index=False)
                    
                    # Save trades
                    trades_df = pd.DataFrame(trades)
                    trades_df.to_csv(os.path.join(args.output, 'trades.csv'), index=False)
                    
                    print(f"Results saved to: {args.output}")
                    
                return 0
            else:
                print("No successful backtests completed.")
                return 1
                
        except Exception as e:
            print(f"Error during backtest execution: {e}")
            return 1


# Add comprehensive strategy and timeframe definitions
AVAILABLE_STRATEGIES = [
    'RSI_MACD_VWAP',
    'SMA_Cross', 
    'BB_RSI',
    'MACD_Only',
    'Enhanced_Multi_Factor',
    'Optimized_Crypto_V2'
]

AVAILABLE_TIMEFRAMES = ['1h', '4h', '1d']  # Focus on main timeframes


class ComprehensiveBacktestRunner:
    """Comprehensive backtest runner for multiple strategies and timeframes."""
    
    def __init__(self, initial_capital=100000, position_size=10000, bars=720, exchange='kraken'):
        self.initial_capital = initial_capital
        self.position_size = position_size 
        self.bars = bars
        self.exchange = exchange
        self.results = []
        
    def run_comprehensive_backtest(self, symbols=None, strategies=None, timeframes=None):
        """Run backtest across all combinations of symbols, strategies, and timeframes."""
        if symbols is None:
            # Load from crypto_assets.csv 
            backtest = EnhancedCryptoBacktest()
            symbols = backtest.load_crypto_assets()
            
        if strategies is None:
            strategies = AVAILABLE_STRATEGIES
            
        if timeframes is None:
            timeframes = AVAILABLE_TIMEFRAMES
            
        print("="*100)
        print("COMPREHENSIVE CRYPTO BACKTEST ANALYSIS")
        print("="*100)
        print(f"Testing {len(symbols)} symbols × {len(strategies)} strategies × {len(timeframes)} timeframes")
        print(f"Total combinations: {len(symbols) * len(strategies) * len(timeframes)}")
        print("="*100)
        
        total_tests = len(symbols) * len(strategies) * len(timeframes)
        completed_tests = 0
        
        for symbol in symbols:
            for strategy in strategies:
                for timeframe in timeframes:
                    completed_tests += 1
                    print(f"\n[{completed_tests}/{total_tests}] Testing {symbol} | {strategy} | {timeframe}")
                    
                    try:
                        # Initialize backtest for this combination
                        backtest = EnhancedCryptoBacktest(
                            initial_capital=self.initial_capital,
                            position_size=self.position_size,
                            bars=self.bars,
                            interval=timeframe,
                            exchange=self.exchange,
                            strategy=strategy
                        )
                        
                        # Run single symbol backtest
                        result = backtest.process_symbol(symbol)
                        
                        if result:
                            # Add metadata
                            result['test_id'] = completed_tests
                            result['timestamp'] = datetime.now()
                            self.results.append(result)
                        else:
                            print(f"   ❌ No result for {symbol} | {strategy} | {timeframe}")
                            
                        # Rate limiting to avoid exchange limits
                        time.sleep(0.1)
                        
                    except Exception as e:
                        print(f"   ❌ Error: {e}")
                        continue
                        
        print(f"\n✅ Completed {completed_tests} tests with {len(self.results)} successful results")
        return self.results
        
    def generate_comprehensive_summary(self):
        """Generate comprehensive analysis of all backtest results."""
        if not self.results:
            print("No results to analyze!")
            return
            
        print("\n" + "="*100)
        print("COMPREHENSIVE BACKTEST SUMMARY")
        print("="*100)
        
        # Convert results to DataFrame for easy analysis
        df = pd.DataFrame(self.results)
        
        # Overall statistics
        total_tests = len(df)
        total_trades = df['total_trades'].sum()
        avg_win_rate = df['win_rate'].mean()
        avg_return = df['total_return'].mean()
        
        print(f"\n📊 OVERALL STATISTICS:")
        print(f"   • Total tests completed: {total_tests}")
        print(f"   • Total trades executed: {total_trades}")
        print(f"   • Average win rate: {avg_win_rate:.2f}%")
        print(f"   • Average total return: {avg_return:.2f}%")
        
        # Top 10 best performing combinations
        print(f"\n🏆 TOP 10 BEST PERFORMING COMBINATIONS:")
        top_10 = df.nlargest(10, 'total_return')[['symbol', 'strategy', 'timeframe', 'total_return', 'win_rate', 'total_trades']]
        print(tabulate(top_10, headers=['Symbol', 'Strategy', 'Timeframe', 'Return%', 'Win Rate%', 'Trades'], 
                      tablefmt='grid', floatfmt='.2f'))
        
        # Best strategy per timeframe
        print(f"\n⏰ BEST STRATEGY PER TIMEFRAME:")
        timeframe_best = df.loc[df.groupby('timeframe')['total_return'].idxmax()]
        timeframe_summary = timeframe_best[['timeframe', 'strategy', 'symbol', 'total_return', 'win_rate']]
        print(tabulate(timeframe_summary, headers=['Timeframe', 'Best Strategy', 'Best Symbol', 'Return%', 'Win Rate%'], 
                      tablefmt='grid', floatfmt='.2f'))
        
        # Best strategy per symbol  
        print(f"\n💰 BEST STRATEGY PER SYMBOL:")
        symbol_best = df.loc[df.groupby('symbol')['total_return'].idxmax()]
        symbol_summary = symbol_best[['symbol', 'strategy', 'timeframe', 'total_return', 'win_rate']]
        print(tabulate(symbol_summary, headers=['Symbol', 'Best Strategy', 'Best Timeframe', 'Return%', 'Win Rate%'], 
                      tablefmt='grid', floatfmt='.2f'))
        
        # Strategy performance overview
        print(f"\n📈 STRATEGY PERFORMANCE OVERVIEW:")
        strategy_stats = df.groupby('strategy').agg({
            'total_return': ['mean', 'std', 'max', 'min'],
            'win_rate': 'mean',
            'total_trades': 'mean'
        }).round(2)
        strategy_stats.columns = ['Avg Return%', 'Return Std%', 'Max Return%', 'Min Return%', 'Avg Win Rate%', 'Avg Trades']
        print(tabulate(strategy_stats, headers=strategy_stats.columns, tablefmt='grid', floatfmt='.2f'))
        
        # Save detailed results
        self.save_results_to_files()
        
        return df
        
    def save_results_to_files(self):
        """Save comprehensive results to CSV and JSON files."""
        try:
            # Create output directory
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            # Save results as CSV
            df = pd.DataFrame(self.results)
            csv_path = os.path.join(output_dir, f'comprehensive_backtest_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
            df.to_csv(csv_path, index=False)
            
            # Save raw results as JSON for detailed analysis
            json_path = os.path.join(output_dir, f'comprehensive_backtest_raw_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            with open(json_path, 'w') as f:
                json.dump(self.results, f, indent=2, default=str)
                
            print(f"\n💾 Results saved to:")
            print(f"   📄 CSV: {csv_path}")
            print(f"   📄 JSON: {json_path}")
            
        except Exception as e:
            print(f"   ❌ Error saving results: {e}")


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
