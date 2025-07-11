#!/usr/bin/env python3
"""
Subprocess-compatible version of enhanced_crypto_backtest.py
Removes all unicode characters and colorama dependencies for batch runner compatibility
"""

import os
import sys
import warnings
import argparse
import pandas as pd
import numpy as np
import ccxt
import ta
from datetime import datetime, timedelta
import json
import time

# Disable warnings
warnings.filterwarnings('ignore')

class SubprocessSafeCryptoBacktest:
    """Subprocess-safe crypto backtest engine"""
    
    def __init__(self, initial_capital=100000, position_size=10000, bars=720, interval='1h', exchange='kraken', strategy='RSI_MACD_VWAP', verbose=False):
        self.initial_capital = initial_capital
        self.position_size = position_size
        self.bars = bars
        self.interval = interval
        self.exchange = exchange
        self.strategy = strategy
        self.verbose = verbose
        
        # Initialize exchange
        self.exchange_obj = getattr(ccxt, exchange)()
        
        # Results storage
        self.results = []
        self.trades = []
        
    def load_crypto_assets(self):
        """Load crypto assets from CSV file"""
        try:
            assets_path = os.path.join(os.path.dirname(__file__), '..', 'input', 'crypto_assets.csv')
            if os.path.exists(assets_path):
                df = pd.read_csv(assets_path)
                return df['symbol'].tolist()
            else:
                return ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
        except Exception as e:
            print(f"WARNING: Error loading crypto assets: {e}")
            return ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    
    def fetch_data(self, symbol, timeframe, limit):
        """Fetch OHLCV data for a symbol"""
        try:
            ohlcv = self.exchange_obj.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            if self.verbose:
                print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def generate_signals_rsi_macd_vwap(self, df):
        """Generate RSI+MACD+VWAP signals"""
        try:
            # RSI
            df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
            
            # MACD
            macd = ta.trend.MACD(df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_histogram'] = macd.macd_diff()
            
            # VWAP (simple approximation)
            df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
            df['vwap'] = (df['typical_price'] * df['volume']).cumsum() / df['volume'].cumsum()
            
            # Generate signals
            df['signal'] = 0
            
            # Buy signals: RSI oversold, MACD bullish, price below VWAP
            buy_condition = (df['rsi'] < 30) & (df['macd'] > df['macd_signal']) & (df['close'] < df['vwap'])
            df.loc[buy_condition, 'signal'] = 1
            
            # Sell signals: RSI overbought, MACD bearish, price above VWAP  
            sell_condition = (df['rsi'] > 70) & (df['macd'] < df['macd_signal']) & (df['close'] > df['vwap'])
            df.loc[sell_condition, 'signal'] = -1
            
            return df
        except Exception as e:
            print(f"WARNING: Error generating RSI_MACD_VWAP signals: {e}")
            return df
    
    def generate_signals_sma_cross(self, df):
        """Generate SMA Cross signals"""
        try:
            df['sma_fast'] = ta.trend.SMAIndicator(df['close'], window=10).sma()
            df['sma_slow'] = ta.trend.SMAIndicator(df['close'], window=20).sma()
            
            df['signal'] = 0
            
            # Buy when fast SMA crosses above slow SMA
            buy_condition = df['sma_fast'] > df['sma_slow']
            df.loc[buy_condition, 'signal'] = 1
            
            # Sell when fast SMA crosses below slow SMA
            sell_condition = df['sma_fast'] < df['sma_slow']
            df.loc[sell_condition, 'signal'] = -1
            
            return df
        except Exception as e:
            print(f"WARNING: Error generating SMA_Cross signals: {e}")
            return df
    
    def generate_signals_bb_rsi(self, df):
        """Generate Bollinger Bands + RSI signals"""
        try:
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df['close'])
            df['bb_upper'] = bb.bollinger_hband()
            df['bb_lower'] = bb.bollinger_lband()
            df['bb_middle'] = bb.bollinger_mavg()
            
            # RSI
            df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
            
            df['signal'] = 0
            
            # Buy signals: price below lower band and RSI oversold
            buy_condition = (df['close'] < df['bb_lower']) & (df['rsi'] < 30)
            df.loc[buy_condition, 'signal'] = 1
            
            # Sell signals: price above upper band and RSI overbought
            sell_condition = (df['close'] > df['bb_upper']) & (df['rsi'] > 70)
            df.loc[sell_condition, 'signal'] = -1
            
            return df
        except Exception as e:
            print(f"WARNING: Error generating BB_RSI signals: {e}")
            return df
    
    def generate_signals_macd_only(self, df):
        """Generate MACD Only signals"""
        try:
            macd = ta.trend.MACD(df['close'])
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_histogram'] = macd.macd_diff()
            
            df['signal'] = 0
            
            # Buy when MACD above signal line
            buy_condition = df['macd'] > df['macd_signal']
            df.loc[buy_condition, 'signal'] = 1
            
            # Sell when MACD below signal line
            sell_condition = df['macd'] < df['macd_signal']
            df.loc[sell_condition, 'signal'] = -1
            
            return df
        except Exception as e:
            print(f"WARNING: Error generating MACD_Only signals: {e}")
            return df
    
    def generate_signals_enhanced_multi_factor(self, df):
        """Generate Enhanced Multi-Factor signals"""
        try:
            # Multiple indicators
            df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
            df['ema_fast'] = ta.trend.EMAIndicator(df['close'], window=12).ema()
            df['ema_slow'] = ta.trend.EMAIndicator(df['close'], window=26).ema()
            df['adx'] = ta.trend.ADXIndicator(df['high'], df['low'], df['close']).adx()
            df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
            
            df['signal'] = 0
            
            # Buy signals: multiple conditions
            buy_condition = (df['rsi'] < 35) & (df['ema_fast'] > df['ema_slow']) & (df['adx'] > 25)
            df.loc[buy_condition, 'signal'] = 1
            
            # Sell signals: multiple conditions
            sell_condition = (df['rsi'] > 65) & (df['ema_fast'] < df['ema_slow']) & (df['adx'] > 25)
            df.loc[sell_condition, 'signal'] = -1
            
            return df
        except Exception as e:
            print(f"WARNING: Error generating Enhanced_Multi_Factor signals: {e}")
            return df
    
    def generate_signals_optimized_crypto_v2(self, df):
        """Generate Optimized Crypto V2 signals"""
        try:
            # Advanced indicators
            df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
            df['stoch'] = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close']).stoch()
            df['cci'] = ta.trend.CCIIndicator(df['high'], df['low'], df['close']).cci()
            df['williams_r'] = ta.momentum.WilliamsRIndicator(df['high'], df['low'], df['close']).williams_r()
            
            df['signal'] = 0
            
            # Buy signals: multiple oversold conditions
            buy_condition = (df['rsi'] < 30) & (df['stoch'] < 20) & (df['cci'] < -100)
            df.loc[buy_condition, 'signal'] = 1
            
            # Sell signals: multiple overbought conditions
            sell_condition = (df['rsi'] > 70) & (df['stoch'] > 80) & (df['cci'] > 100)
            df.loc[sell_condition, 'signal'] = -1
            
            return df
        except Exception as e:
            print(f"WARNING: Error generating Optimized_Crypto_V2 signals: {e}")
            return df
    
    def generate_signals(self, df, strategy):
        """Generate trading signals based on strategy"""
        if strategy == 'RSI_MACD_VWAP':
            return self.generate_signals_rsi_macd_vwap(df)
        elif strategy == 'SMA_Cross':
            return self.generate_signals_sma_cross(df)
        elif strategy == 'BB_RSI':
            return self.generate_signals_bb_rsi(df)
        elif strategy == 'MACD_Only':
            return self.generate_signals_macd_only(df)
        elif strategy == 'Enhanced_Multi_Factor':
            return self.generate_signals_enhanced_multi_factor(df)
        elif strategy == 'Optimized_Crypto_V2':
            return self.generate_signals_optimized_crypto_v2(df)
        else:
            return self.generate_signals_rsi_macd_vwap(df)
    
    def backtest_symbol(self, symbol):
        """Backtest a single symbol"""
        if self.verbose:
            print(f"Processing {symbol}...", end=" ")
        
        # Fetch data
        df = self.fetch_data(symbol, self.interval, self.bars)
        if df is None or len(df) < 50:
            if self.verbose:
                print("Insufficient data")
            return None
        
        # Generate signals
        df = self.generate_signals(df, self.strategy)
        
        if 'signal' not in df.columns or df['signal'].sum() == 0:
            if self.verbose:
                print("No signals generated")
            return None
        
        # Execute trades
        trades = self.execute_trades(df, symbol)
        
        if not trades:
            if self.verbose:
                print("No trades executed")
            return None
        
        # Calculate metrics
        result = self.calculate_metrics(trades, symbol)
        
        if self.verbose:
            print(f"Complete - {len(trades)} trades, {result['total_return']:.2f}% return")
        
        return result
    
    def execute_trades(self, df, symbol):
        """Execute trades based on signals"""
        trades = []
        position = None
        
        for i in range(1, len(df)):
            current_price = df.iloc[i]['close']
            signal = df.iloc[i]['signal']
            
            # Enter long position
            if signal == 1 and position is None:
                position = {
                    'type': 'long',
                    'entry_price': current_price,
                    'entry_time': df.index[i],
                    'symbol': symbol
                }
            
            # Enter short position
            elif signal == -1 and position is None:
                position = {
                    'type': 'short',
                    'entry_price': current_price,
                    'entry_time': df.index[i],
                    'symbol': symbol
                }
            
            # Exit position
            elif signal != 0 and position is not None:
                if position['type'] == 'long':
                    pnl = (current_price - position['entry_price']) / position['entry_price'] * 100
                else:
                    pnl = (position['entry_price'] - current_price) / position['entry_price'] * 100
                
                trade = {
                    'symbol': symbol,
                    'type': position['type'],
                    'entry_price': position['entry_price'],
                    'exit_price': current_price,
                    'entry_time': position['entry_time'],
                    'exit_time': df.index[i],
                    'pnl_percent': pnl,
                    'strategy': self.strategy
                }
                trades.append(trade)
                position = None
        
        return trades
    
    def calculate_metrics(self, trades, symbol):
        """Calculate performance metrics"""
        if not trades:
            return None
        
        pnl_list = [trade['pnl_percent'] for trade in trades]
        
        total_trades = len(trades)
        winning_trades = len([pnl for pnl in pnl_list if pnl > 0])
        losing_trades = len([pnl for pnl in pnl_list if pnl < 0])
        
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        total_return = sum(pnl_list)
        avg_return = np.mean(pnl_list)
        
        max_win = max(pnl_list) if pnl_list else 0
        max_loss = min(pnl_list) if pnl_list else 0
        
        return {
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
            'trades': trades
        }
    
    def run_backtest(self, symbols):
        """Run backtest on multiple symbols"""
        print(f"Starting backtest with {self.strategy} strategy")
        print(f"Timeframe: {self.interval}, Bars: {self.bars}")
        print(f"Exchange: {self.exchange}")
        print(f"Testing {len(symbols)} symbols...")
        print("-" * 50)
        
        all_results = []
        all_trades = []
        
        for symbol in symbols:
            try:
                result = self.backtest_symbol(symbol)
                if result:
                    all_results.append(result)
                    all_trades.extend(result['trades'])
            except Exception as e:
                print(f"Error with {symbol}: {e}")
                continue
        
        if not all_results:
            print("No results generated!")
            return None, None
        
        # Summary
        self.print_summary(all_results, all_trades)
        
        # Save results (pass output_dir if available)
        output_dir = getattr(self, 'output_dir', None)
        self.save_results(all_results, all_trades, output_dir)
        
        return all_results, all_trades
    
    def print_summary(self, results, trades):
        """Print backtest summary"""
        print("\n" + "="*60)
        print(f"BACKTEST SUMMARY - {self.strategy}")
        print("="*60)
        
        total_symbols = len(results)
        total_trades = len(trades)
        
        if total_trades == 0:
            print("No trades executed!")
            return
        
        # Overall metrics
        all_returns = [trade['pnl_percent'] for trade in trades]
        winning_trades = len([r for r in all_returns if r > 0])
        losing_trades = len([r for r in all_returns if r < 0])
        
        overall_win_rate = (winning_trades / total_trades) * 100
        total_return = sum(all_returns)
        avg_return = np.mean(all_returns)
        
        print(f"Symbols Tested: {total_symbols}")
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
        
        print("="*60)
    
    def save_results(self, results, trades, output_dir=None):
        """Save results to files"""
        if output_dir:
            # Use provided output directory (for batch runner)
            os.makedirs(output_dir, exist_ok=True)
        else:
            # Create own output directory
            output_dir = f"output_{self.strategy}_{self.interval}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(output_dir, exist_ok=True)
        
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
        summary_df.to_csv(os.path.join(output_dir, 'summary.csv'), index=False)
        
        # Save trades
        trades_df = pd.DataFrame(trades)
        trades_df.to_csv(os.path.join(output_dir, 'trades.csv'), index=False)
        
        print(f"\nResults saved to: {output_dir}")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Subprocess-Safe Crypto Backtest')
    
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
        '--output', '-o',
        type=str,
        help='Output directory for results',
        default=None
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()

def main():
    """Main function"""
    args = parse_arguments()
    
    print("Enhanced Crypto Backtest - Subprocess Safe")
    print("=" * 50)
    
    # Initialize backtest
    backtest = SubprocessSafeCryptoBacktest(
        initial_capital=args.capital,
        position_size=args.position,
        bars=args.bars,
        interval=args.interval,
        exchange=args.exchange,
        strategy=args.strategy,
        verbose=args.verbose
    )
    
    # Set output directory if provided
    if args.output:
        backtest.output_dir = args.output
    
    # Get symbols
    if args.symbols:
        symbols = args.symbols
        print(f"Using specific symbols: {', '.join(symbols)}")
    else:
        symbols = backtest.load_crypto_assets()
        print(f"Loaded {len(symbols)} symbols from crypto_assets.csv")
    
    # Run backtest
    try:
        results, trades = backtest.run_backtest(symbols)
        print("\nBacktest completed successfully!")
    except Exception as e:
        print(f"Error during backtest: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
