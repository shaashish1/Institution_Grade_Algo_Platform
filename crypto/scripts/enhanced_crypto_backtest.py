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
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data_acquisition import fetch_data
from tabulate import tabulate
from src.backtest_evaluator import BacktestEvaluator
from src.strategies.enhanced_multi_factor import EnhancedMultiFactorStrategy
from src.strategies.optimized_crypto_v2 import OptimizedCryptoStrategy
from src.strategies.bb_rsi_strategy import BB_RSI_Strategy
from src.strategies.macd_only_strategy import MACD_Only_Strategy
from src.strategies.rsi_macd_vwap_strategy import RSI_MACD_VWAP_Strategy

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
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
            assets_file = os.path.join(os.path.dirname(__file__), '..', '..', 'input', 'crypto_assets.csv')
            if not os.path.exists(assets_file):
                # Default crypto assets
                return ['BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'DOT/USDT', 'SOL/USDT']
            
            df = pd.read_csv(assets_file)
            return df['symbol'].tolist()
        except Exception as e:
            print(f"⚠️  Error loading crypto assets: {e}")
            return ['BTC/USDT', 'ETH/USDT']
    
    def load_strategy_config(self):
        """Load strategy configuration."""
        try:
            config_file = os.path.join(os.path.dirname(__file__), '..', 'input', 'config_crypto.yaml')
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            return config.get('strategy', {})
        except Exception as e:
            print(f"⚠️  Error loading strategy config: {e}")
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
                    
                return signals_df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"⚠️  Error generating RSI_MACD_VWAP signals: {e}")
            return pd.DataFrame()
    
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
            
            for i in range(31, len(data)):  # Start after SMA calculation period
                current = data.iloc[i]
                prev = data.iloc[i-1]
                
                # Skip if any indicator is NaN
                if pd.isna(current['sma_fast']) or pd.isna(current['sma_slow']) or pd.isna(current['rsi']):
                    continue
                
                # Buy signal: Fast SMA crosses above slow SMA with RSI confirmation
                if (current['sma_fast'] > current['sma_slow'] and 
                    prev['sma_fast'] <= prev['sma_slow'] and 
                    current['rsi'] < 70):
                    signals.append({
                        'timestamp': current.name,
                        'signal': 'BUY',
                        'price': current['close'],
                        'rsi': current['rsi'],
                        'macd': np.nan,
                        'score': 3
                    })
                
                # Sell signal: Fast SMA crosses below slow SMA with RSI confirmation
                elif (current['sma_fast'] < current['sma_slow'] and 
                      prev['sma_fast'] >= prev['sma_slow'] and 
                      current['rsi'] > 30):
                    signals.append({
                        'timestamp': current.name,
                        'signal': 'SELL',
                        'price': current['close'],
                        'rsi': current['rsi'],
                        'macd': np.nan,
                        'score': 3
                    })
            
            return pd.DataFrame(signals)
        
        except Exception as e:
            print(f"⚠️  Error generating SMA_Cross signals: {e}")
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
                    
                return signals_df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"⚠️  Error generating BB_RSI signals: {e}")
            return pd.DataFrame()
    
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
                    
                return signals_df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"⚠️  Error generating MACD_Only signals: {e}")
            return pd.DataFrame()

    def generate_signals_enhanced_multi_factor(self, data):
        """Generate signals using Enhanced Multi-Factor strategy."""
        try:
            # Use the enhanced strategy from strategies folder
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
                    
                return signals_df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"⚠️  Error generating Enhanced_Multi_Factor signals: {e}")
            return pd.DataFrame()

    def generate_signals_optimized_crypto_v2(self, data):
        """Generate signals using Optimized Crypto V2 strategy."""
        try:
            # Use the optimized strategy from strategies folder
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
                    
                return signals_df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"⚠️  Error generating Optimized_Crypto_V2 signals: {e}")
            return pd.DataFrame()

    def simulate_trading(self, data, signals):
        """Simulate trading based on signals with stop-loss and take-profit."""
        if signals.empty:
            return []
        
        trades = []
        position = None
        stop_loss_pct = 0.05  # 5% stop loss
        take_profit_pct = 0.15  # 15% take profit
        
        # Convert data to list for easier iteration
        data_list = data.reset_index().to_dict('records')
        
        for _, signal in signals.iterrows():
            if signal['signal'] == 'BUY' and position is None:
                # Enter long position
                position = {
                    'entry_time': signal['timestamp'],
                    'entry_price': signal['price'],
                    'type': 'LONG',
                    'stop_loss': signal['price'] * (1 - stop_loss_pct),
                    'take_profit': signal['price'] * (1 + take_profit_pct)
                }
            
            elif signal['signal'] == 'SELL' and position is not None:
                # Exit long position
                trade = {
                    'entry_time': position['entry_time'],
                    'exit_time': signal['timestamp'],
                    'entry_price': position['entry_price'],
                    'exit_price': signal['price'],
                    'position_size': self.position_size,
                    'trade_type': 'Long',
                    'exit_reason': 'Signal'
                }
                
                # Calculate P&L
                pnl_dollars = (signal['price'] - position['entry_price']) * (self.position_size / position['entry_price'])
                pnl_percent = ((signal['price'] - position['entry_price']) / position['entry_price']) * 100
                
                trade['pnl_dollars'] = pnl_dollars
                trade['pnl_percent'] = pnl_percent
                
                trades.append(trade)
                position = None
        
        # Check for stop-loss and take-profit on remaining position
        if position is not None:
            # Find data points after position entry
            entry_idx = None
            for i, row in enumerate(data_list):
                if row['datetime'] == position['entry_time']:
                    entry_idx = i
                    break
            
            if entry_idx is not None:
                for i in range(entry_idx + 1, len(data_list)):
                    current_price = data_list[i]['close']
                    
                    # Check stop-loss
                    if current_price <= position['stop_loss']:
                        trade = {
                            'entry_time': position['entry_time'],
                            'exit_time': data_list[i]['datetime'],
                            'entry_price': position['entry_price'],
                            'exit_price': current_price,
                            'position_size': self.position_size,
                            'trade_type': 'Long',
                            'exit_reason': 'Stop Loss'
                        }
                        
                        pnl_dollars = (current_price - position['entry_price']) * (self.position_size / position['entry_price'])
                        pnl_percent = ((current_price - position['entry_price']) / position['entry_price']) * 100
                        
                        trade['pnl_dollars'] = pnl_dollars
                        trade['pnl_percent'] = pnl_percent
                        
                        trades.append(trade)
                        break
                    
                    # Check take-profit
                    elif current_price >= position['take_profit']:
                        trade = {
                            'entry_time': position['entry_time'],
                            'exit_time': data_list[i]['datetime'],
                            'entry_price': position['entry_price'],
                            'exit_price': current_price,
                            'position_size': self.position_size,
                            'trade_type': 'Long',
                            'exit_reason': 'Take Profit'
                        }
                        
                        pnl_dollars = (current_price - position['entry_price']) * (self.position_size / position['entry_price'])
                        pnl_percent = ((current_price - position['entry_price']) / position['entry_price']) * 100
                        
                        trade['pnl_dollars'] = pnl_dollars
                        trade['pnl_percent'] = pnl_percent
                        
                        trades.append(trade)
                        break
        
        return trades
    
    def run_symbol_backtest(self, symbol):
        """Run backtest for a single symbol."""
        print(f"📈 Processing {symbol}...", end=" ")
        
        try:
            # Fetch data
            data = fetch_data(
                symbol=symbol,
                exchange=self.exchange,
                interval=self.interval,
                bars=self.bars,
                data_source="ccxt"
            )
            
            if data is None or len(data) < 50:
                print("❌ Insufficient data")
                return None
            
            # Ensure datetime index
            if 'timestamp' in data.columns:
                data['datetime'] = pd.to_datetime(data['timestamp'])
                data.set_index('datetime', inplace=True)
            elif not isinstance(data.index, pd.DatetimeIndex):
                data.index = pd.to_datetime(data.index)
            
            # Generate signals
            signals = self.generate_signals(data)
            
            if signals.empty:
                print("⚠️  No signals generated")
                return None
            
            # Simulate trading
            trades = self.simulate_trading(data, signals)
            
            if not trades:
                print("⚠️  No trades executed")
                return None
            
            # Create evaluator
            evaluator = BacktestEvaluator(
                strategy_name=self.strategy,
                symbol=symbol,
                initial_capital=self.initial_capital
            )
            
            # Add trades to evaluator
            for trade in trades:
                evaluator.add_trade(trade)
            
            # Add equity curve points
            current_capital = self.initial_capital
            for i, trade in enumerate(trades):
                current_capital += trade['pnl_dollars']
                evaluator.add_equity_point(trade['exit_time'], current_capital)
            
            # Store evaluator
            self.evaluators[symbol] = evaluator
            
            print(f"✅ {len(trades)} trades executed")
            return evaluator
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def run_comprehensive_backtest(self, symbols=None):
        """Run comprehensive backtest on crypto assets."""
        print("🚀 Enhanced Crypto Backtest with Comprehensive KPIs")
        print("=" * 80)
        
        # Load assets if not provided
        if symbols is None:
            symbols = self.load_crypto_assets()
        if not symbols:
            print("❌ No symbols to process")
            return
        
        print(f"💰 Initial Capital: ${self.initial_capital:,.2f}")
        print(f"📊 Position Size: ${self.position_size:,.2f} per trade")
        print(f"🔍 Scanning {len(symbols)} crypto symbols")
        print("=" * 80)
        
        successful_backtests = []
        failed_symbols = []
        
        # Process each symbol
        for i, symbol in enumerate(symbols, 1):
            print(f"[{i:2d}/{len(symbols)}] ", end="")
            
            evaluator = self.run_symbol_backtest(symbol)
            
            if evaluator:
                successful_backtests.append(symbol)
            else:
                failed_symbols.append(symbol)
        
        # Display results
        print(f"\n{'='*80}")
        print(f"📊 BACKTEST SUMMARY")
        print(f"{'='*80}")
        print(f"✅ Successful: {len(successful_backtests)} symbols")
        print(f"❌ Failed: {len(failed_symbols)} symbols")
        
        if failed_symbols:
            print(f"⚠️  Failed symbols: {', '.join(failed_symbols)}")
        
        # Generate summary table for all successful symbols
        print(f"\n{'='*80}")
        print(f"🔍 STRATEGY PERFORMANCE SUMMARY")
        print(f"{'='*80}")
        
        # Create summary table
        if successful_backtests:
            self.display_strategy_summary_table(successful_backtests)
        
        # Generate portfolio summary
        self.generate_portfolio_summary(successful_backtests)
        
        # Generate best trade and strategy summary
        self.generate_best_trade_strategy_summary(successful_backtests)
        
        return successful_backtests
    
    def display_strategy_summary_table(self, successful_symbols):
        """Display comprehensive strategy performance table."""
        if not successful_symbols:
            return
        
        summary_data = []
        
        for symbol in successful_symbols:
            evaluator = self.evaluators[symbol]
            kpis = evaluator.calculate_comprehensive_kpis()
            
            if kpis:
                # Calculate additional metrics
                total_trades = len(evaluator.trades)
                winning_trades = sum(1 for trade in evaluator.trades if trade['pnl_dollars'] > 0)
                losing_trades = sum(1 for trade in evaluator.trades if trade['pnl_dollars'] < 0)
                
                # Get best and worst trades
                best_trade = max(evaluator.trades, key=lambda x: x['pnl_percent'])['pnl_percent'] if evaluator.trades else 0
                worst_trade = min(evaluator.trades, key=lambda x: x['pnl_percent'])['pnl_percent'] if evaluator.trades else 0
                
                # Calculate average trade duration
                avg_duration = sum(trade['duration_days'] for trade in evaluator.trades) / len(evaluator.trades) if evaluator.trades else 0
                
                summary_data.append([
                    symbol,
                    self.strategy,
                    total_trades,
                    winning_trades,
                    losing_trades,
                    f"{kpis['win_rate_pct']:.1f}%",
                    f"{kpis['total_return_pct']:+.2f}%",
                    f"{kpis['sharpe_ratio']:.2f}",
                    f"{kpis['max_drawdown_pct']:.2f}%",
                    f"{best_trade:+.2f}%",
                    f"{worst_trade:+.2f}%",
                    f"{avg_duration:.1f}d",
                    f"{kpis['profit_factor']:.2f}",
                    self.get_strategy_rating(kpis)
                ])
        
        # Sort by total return descending
        summary_data.sort(key=lambda x: float(x[6].replace('%', '').replace('+', '')), reverse=True)
        
        headers = [
            'Symbol', 'Strategy', 'Trades', 'Wins', 'Losses', 'Win Rate', 
            'Return', 'Sharpe', 'Max DD', 'Best Trade', 'Worst Trade', 
            'Avg Duration', 'Profit Factor', 'Rating'
        ]
        
        print(tabulate(summary_data, headers=headers, tablefmt='grid'))
        
        # Display detailed KPIs for each symbol
        self.display_detailed_kpis(successful_symbols)
        
        # Add strategy performance insights
        self.display_strategy_insights(summary_data)
    
    def get_strategy_rating(self, kpis):
        """Get strategy rating based on KPIs."""
        if not kpis:
            return "N/A"
        
        # Rating logic based on multiple factors
        score = 0
        
        # Profitability (40% weight)
        if kpis['total_return_pct'] > 15:
            score += 2
        elif kpis['total_return_pct'] > 5:
            score += 1.5
        elif kpis['total_return_pct'] > 0:
            score += 1
        
        # Sharpe ratio (30% weight)
        if kpis['sharpe_ratio'] > 2:
            score += 1.5
        elif kpis['sharpe_ratio'] > 1:
            score += 1
        elif kpis['sharpe_ratio'] > 0:
            score += 0.5
        
        # Win rate (20% weight)
        if kpis['win_rate_pct'] > 70:
            score += 1
        elif kpis['win_rate_pct'] > 50:
            score += 0.5
        
        # Max drawdown (10% weight)
        if kpis['max_drawdown_pct'] < 5:
            score += 0.5
        elif kpis['max_drawdown_pct'] < 15:
            score += 0.25
        
        # Convert to star rating
        if score >= 4:
            return "⭐⭐⭐⭐⭐"
        elif score >= 3:
            return "⭐⭐⭐⭐"
        elif score >= 2:
            return "⭐⭐⭐"
        elif score >= 1:
            return "⭐⭐"
        else:
            return "⭐"
    
    def display_strategy_insights(self, summary_data):
        """Display insights about strategy performance."""
        if not summary_data:
            return
        
        print(f"\n{'='*80}")
        print(f"📈 STRATEGY INSIGHTS - {self.strategy}")
        print(f"{'='*80}")
        
        # Calculate overall strategy metrics
        total_symbols = len(summary_data)
        profitable_symbols = sum(1 for row in summary_data if '+' in row[6])
        avg_return = sum(float(row[6].replace('%', '').replace('+', '')) for row in summary_data) / total_symbols
        
        best_performer = summary_data[0] if summary_data else None
        worst_performer = summary_data[-1] if summary_data else None
        
        print(f"📊 Strategy: {self.strategy}")
        print(f"🔍 Total Symbols Analyzed: {total_symbols}")
        print(f"✅ Profitable Symbols: {profitable_symbols} ({profitable_symbols/total_symbols*100:.1f}%)")
        print(f"📈 Average Return: {avg_return:+.2f}%")
        
        if best_performer:
            print(f"🏆 Best Performer: {best_performer[0]} ({best_performer[6]})")
        if worst_performer:
            print(f"📉 Worst Performer: {worst_performer[0]} ({worst_performer[6]})")
        
        # Strategy recommendation
        if avg_return > 5 and profitable_symbols/total_symbols > 0.6:
            recommendation = "🚀 EXCELLENT STRATEGY - Strong performance across multiple symbols"
            color = Fore.GREEN if COLORAMA_AVAILABLE else ""
        elif avg_return > 0 and profitable_symbols/total_symbols > 0.4:
            recommendation = "👍 GOOD STRATEGY - Decent performance, consider optimization"
            color = Fore.YELLOW if COLORAMA_AVAILABLE else ""
        else:
            recommendation = "❌ POOR STRATEGY - Needs significant improvement"
            color = Fore.RED if COLORAMA_AVAILABLE else ""
        
        print(f"\n{color}{recommendation}{Style.RESET_ALL if COLORAMA_AVAILABLE else ''}")

    def generate_portfolio_summary(self, successful_symbols):
        """Generate overall portfolio summary."""
        if not successful_symbols:
            return
        
        print(f"\n{'='*80}")
        print(f"🏦 PORTFOLIO SUMMARY")
        print(f"{'='*80}")
        
        total_trades = 0
        total_pnl = 0
        winning_symbols = 0
        
        portfolio_metrics = []
        
        for symbol in successful_symbols:
            evaluator = self.evaluators[symbol]
            kpis = evaluator.calculate_comprehensive_kpis()
            
            if kpis:
                total_trades += kpis['total_trades']
                symbol_pnl = kpis['equity_final'] - evaluator.initial_capital
                total_pnl += symbol_pnl
                
                if kpis['total_return_pct'] > 0:
                    winning_symbols += 1
                
                portfolio_metrics.append({
                    'Symbol': symbol,
                    'Trades': kpis['total_trades'],
                    'Win Rate': f"{kpis['win_rate_pct']:.1f}%",
                    'Total Return': f"{kpis['total_return_pct']:+.2f}%",
                    'CAGR': f"{kpis['cagr_pct']:+.2f}%",
                    'Sharpe Ratio': f"{kpis['sharpe_ratio']:.2f}",
                    'Sortino Ratio': f"{kpis['sortino_ratio']:.2f}",
                    'Max Drawdown': f"{kpis['max_drawdown_pct']:.2f}%",
                    'Profit Factor': f"{kpis['profit_factor']:.2f}" if kpis['profit_factor'] != float('inf') else "∞",
                    'Expectancy': f"{kpis['expectancy_pct']:+.2f}%"
                })
        
        # Display portfolio table
        if portfolio_metrics:
            print(tabulate(portfolio_metrics, headers='keys', tablefmt='grid'))
        
        # Portfolio summary
        portfolio_return = (total_pnl / (self.initial_capital * len(successful_symbols))) * 100
        symbol_win_rate = (winning_symbols / len(successful_symbols)) * 100
        
        print(f"\n💼 PORTFOLIO METRICS:")
        print(f"Total Symbols Analyzed: {len(successful_symbols)}")
        print(f"Total Trades Executed: {total_trades}")
        print(f"Portfolio Return: {portfolio_return:+.2f}%")
        print(f"Symbol Win Rate: {symbol_win_rate:.1f}%")
        
        # Overall recommendation
        if portfolio_return > 10 and symbol_win_rate > 60:
            recommendation = "🚀 STRONG PORTFOLIO - Consider live trading"
            color = Fore.GREEN if COLORAMA_AVAILABLE else ""
        elif portfolio_return > 0 and symbol_win_rate > 40:
            recommendation = "👍 DECENT PORTFOLIO - Optimize before live trading"
            color = Fore.YELLOW if COLORAMA_AVAILABLE else ""
        else:
            recommendation = "❌ WEAK PORTFOLIO - Strategy needs major revision"
            color = Fore.RED if COLORAMA_AVAILABLE else ""
        
        print(f"\n{color}{recommendation}{Style.RESET_ALL}")
        
        # Save portfolio summary
        self.save_portfolio_summary(portfolio_metrics, portfolio_return, symbol_win_rate, total_trades)
    
    def save_portfolio_summary(self, metrics, portfolio_return, symbol_win_rate, total_trades):
        """Save portfolio summary to file."""
        try:
            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(output_dir, f'crypto_portfolio_summary_{timestamp}.csv')
            
            # Create summary DataFrame
            summary_data = {
                'analysis_timestamp': [datetime.now()],
                'strategy_name': [self.strategy],
                'total_symbols': [len(metrics)],
                'portfolio_return_pct': [portfolio_return],
                'symbol_win_rate_pct': [symbol_win_rate],
                'total_trades': [total_trades],
                'initial_capital': [self.initial_capital],
                'position_size': [self.position_size],
                'interval': [self.interval],
                'bars': [self.bars],
                'exchange': [self.exchange]
            }
            
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_csv(filename, index=False)
            
            print(f"\n💾 Portfolio summary saved to: {filename}")
            
        except Exception as e:
            print(f"⚠️  Error saving portfolio summary: {e}")
    
    def generate_best_trade_strategy_summary(self, successful_symbols):
        """Generate comprehensive summary table showing best trades and strategy performance."""
        if not successful_symbols:
            return
        
        print(f"\n{'='*80}")
        print(f"🏆 BEST TRADE & STRATEGY SUMMARY")
        print(f"{'='*80}")
        
        # Find best trades across all symbols
        all_trades = []
        best_symbol_performance = []
        
        for symbol in successful_symbols:
            evaluator = self.evaluators[symbol]
            kpis = evaluator.calculate_comprehensive_kpis()
            
            if kpis and evaluator.trades:
                # Track all trades for best trade analysis
                for trade in evaluator.trades:
                    trade_info = {
                        'symbol': symbol,
                        'strategy': self.strategy,
                        'timeframe': self.interval,
                        'entry_time': trade['entry_time'],
                        'exit_time': trade['exit_time'],
                        'entry_price': trade['entry_price'],
                        'exit_price': trade['exit_price'],
                        'pnl_percent': trade['pnl_percent'],
                        'pnl_dollars': trade['pnl_dollars'],
                        'duration_days': trade['duration_days'],
                        'trade_type': trade['trade_type'],
                        'exit_reason': trade.get('exit_reason', 'Signal')
                    }
                    all_trades.append(trade_info)
                
                # Track symbol performance for best strategy analysis
                symbol_perf = {
                    'symbol': symbol,
                    'strategy': self.strategy,
                    'timeframe': self.interval,
                    'total_return_pct': kpis['total_return_pct'],
                    'sharpe_ratio': kpis['sharpe_ratio'],
                    'win_rate_pct': kpis['win_rate_pct'],
                    'total_trades': kpis['total_trades'],
                    'profit_factor': kpis['profit_factor'],
                    'max_drawdown_pct': kpis['max_drawdown_pct'],
                    'cagr_pct': kpis['cagr_pct'],
                    'duration_days': kpis['duration_days']
                }
                best_symbol_performance.append(symbol_perf)
        
        # Find top 5 best trades by percentage return
        if all_trades:
            best_trades = sorted(all_trades, key=lambda x: x['pnl_percent'], reverse=True)[:5]
            
            print(f"\n🎯 TOP 5 BEST TRADES:")
            print("-" * 80)
            
            best_trades_data = []
            for i, trade in enumerate(best_trades, 1):
                color = ""
                reset = ""
                if COLORAMA_AVAILABLE:
                    if trade['pnl_percent'] > 10:
                        color = Fore.GREEN
                        reset = Style.RESET_ALL
                    elif trade['pnl_percent'] > 5:
                        color = Fore.YELLOW
                        reset = Style.RESET_ALL
                
                best_trades_data.append([
                    f"#{i}",
                    trade['symbol'],
                    trade['strategy'],
                    trade['timeframe'],
                    trade['entry_time'].strftime('%Y-%m-%d %H:%M'),
                    trade['exit_time'].strftime('%Y-%m-%d %H:%M'),
                    f"${trade['entry_price']:.4f}",
                    f"${trade['exit_price']:.4f}",
                    f"{color}{trade['pnl_percent']:+.2f}%{reset}",
                    f"{color}${trade['pnl_dollars']:+,.2f}{reset}",
                    f"{trade['duration_days']:.1f}d",
                    trade['exit_reason']
                ])
            
            headers = [
                'Rank', 'Symbol', 'Strategy', 'Timeframe', 'Entry Time', 'Exit Time',
                'Entry Price', 'Exit Price', 'Return (%)', 'P&L ($)', 'Duration', 'Exit Reason'
            ]
            
            print(tabulate(best_trades_data, headers=headers, tablefmt='grid'))
        
        # Find top 5 best performing symbols by total return
        if best_symbol_performance:
            best_symbols = sorted(best_symbol_performance, key=lambda x: x['total_return_pct'], reverse=True)[:5]
            
            print(f"\n🏅 TOP 5 BEST PERFORMING SYMBOLS:")
            print("-" * 80)
            
            best_symbols_data = []
            for i, perf in enumerate(best_symbols, 1):
                color = ""
                reset = ""
                if COLORAMA_AVAILABLE:
                    if perf['total_return_pct'] > 5:
                        color = Fore.GREEN
                        reset = Style.RESET_ALL
                    elif perf['total_return_pct'] > 0:
                        color = Fore.YELLOW
                        reset = Style.RESET_ALL
                    else:
                        color = Fore.RED
                        reset = Style.RESET_ALL
                
                profit_factor_str = "∞" if perf['profit_factor'] == float('inf') else f"{perf['profit_factor']:.2f}"
                
                best_symbols_data.append([
                    f"#{i}",
                    perf['symbol'],
                    perf['strategy'],
                    perf['timeframe'],
                    f"{color}{perf['total_return_pct']:+.2f}%{reset}",
                    f"{perf['cagr_pct']:+.2f}%",
                    f"{perf['sharpe_ratio']:.2f}",
                    f"{perf['win_rate_pct']:.1f}%",
                    perf['total_trades'],
                    profit_factor_str,
                    f"{perf['max_drawdown_pct']:.2f}%",
                    f"{perf['duration_days']:.0f}d"
                ])
            
            headers = [
                'Rank', 'Symbol', 'Strategy', 'Timeframe', 'Total Return', 'CAGR',
                'Sharpe', 'Win Rate', 'Trades', 'Profit Factor', 'Max DD', 'Duration'
            ]
            
            print(tabulate(best_symbols_data, headers=headers, tablefmt='grid'))
        
        # Overall best trade and strategy insights
        if all_trades and best_symbol_performance:
            overall_best_trade = max(all_trades, key=lambda x: x['pnl_percent'])
            overall_best_symbol = max(best_symbol_performance, key=lambda x: x['total_return_pct'])
            
            print(f"\n🏆 OVERALL BEST PERFORMANCE:")
            print("-" * 80)
            
            # Best single trade
            print(f"💎 BEST SINGLE TRADE:")
            print(f"   Symbol: {overall_best_trade['symbol']}")
            print(f"   Strategy: {overall_best_trade['strategy']}")
            print(f"   Timeframe: {overall_best_trade['timeframe']}")
            print(f"   Return: {overall_best_trade['pnl_percent']:+.2f}%")
            print(f"   P&L: ${overall_best_trade['pnl_dollars']:+,.2f}")
            print(f"   Duration: {overall_best_trade['duration_days']:.1f} days")
            print(f"   Entry: {overall_best_trade['entry_time'].strftime('%Y-%m-%d %H:%M')} @ ${overall_best_trade['entry_price']:.4f}")
            print(f"   Exit: {overall_best_trade['exit_time'].strftime('%Y-%m-%d %H:%M')} @ ${overall_best_trade['exit_price']:.4f}")
            
            # Best symbol performance
            print(f"\n🥇 BEST SYMBOL PERFORMANCE:")
            print(f"   Symbol: {overall_best_symbol['symbol']}")
            print(f"   Strategy: {overall_best_symbol['strategy']}")
            print(f"   Timeframe: {overall_best_symbol['timeframe']}")
            print(f"   Total Return: {overall_best_symbol['total_return_pct']:+.2f}%")
            print(f"   CAGR: {overall_best_symbol['cagr_pct']:+.2f}%")
            print(f"   Sharpe Ratio: {overall_best_symbol['sharpe_ratio']:.2f}")
            print(f"   Win Rate: {overall_best_symbol['win_rate_pct']:.1f}%")
            print(f"   Total Trades: {overall_best_symbol['total_trades']}")
            print(f"   Analysis Period: {overall_best_symbol['duration_days']:.0f} days")
            
            # Timeframe analysis
            timeframe_performance = {}
            for perf in best_symbol_performance:
                tf = perf['timeframe']
                if tf not in timeframe_performance:
                    timeframe_performance[tf] = {
                        'symbols': 0,
                        'avg_return': 0,
                        'avg_sharpe': 0,
                        'total_trades': 0
                    }
                
                timeframe_performance[tf]['symbols'] += 1
                timeframe_performance[tf]['avg_return'] += perf['total_return_pct']
                timeframe_performance[tf]['avg_sharpe'] += perf['sharpe_ratio'] if not np.isnan(perf['sharpe_ratio']) else 0
                timeframe_performance[tf]['total_trades'] += perf['total_trades']
            
            # Calculate averages
            for tf in timeframe_performance:
                tf_data = timeframe_performance[tf]
                tf_data['avg_return'] = tf_data['avg_return'] / tf_data['symbols']
                tf_data['avg_sharpe'] = tf_data['avg_sharpe'] / tf_data['symbols']
            
            print(f"\n⏰ TIMEFRAME ANALYSIS:")
            print(f"   Current Timeframe: {self.interval}")
            print(f"   Symbols Analyzed: {len(successful_symbols)}")
            print(f"   Average Return: {sum(p['total_return_pct'] for p in best_symbol_performance) / len(best_symbol_performance):+.2f}%")
            print(f"   Total Trades: {sum(p['total_trades'] for p in best_symbol_performance)}")
            
            # Strategy recommendation for this timeframe
            avg_return = sum(p['total_return_pct'] for p in best_symbol_performance) / len(best_symbol_performance)
            profitable_symbols = sum(1 for p in best_symbol_performance if p['total_return_pct'] > 0)
            success_rate = (profitable_symbols / len(best_symbol_performance)) * 100
            
            print(f"\n💡 STRATEGY RECOMMENDATION:")
            if avg_return > 5 and success_rate > 60:
                recommendation = f"🚀 EXCELLENT: {self.strategy} strategy works very well on {self.interval} timeframe"
                color = Fore.GREEN if COLORAMA_AVAILABLE else ""
            elif avg_return > 0 and success_rate > 40:
                recommendation = f"👍 GOOD: {self.strategy} strategy shows promise on {self.interval} timeframe, consider optimization"
                color = Fore.YELLOW if COLORAMA_AVAILABLE else ""
            else:
                recommendation = f"❌ POOR: {self.strategy} strategy needs improvement on {self.interval} timeframe"
                color = Fore.RED if COLORAMA_AVAILABLE else ""
            
            print(f"   {color}{recommendation}{Style.RESET_ALL if COLORAMA_AVAILABLE else ''}")
            
            # Save best performance summary
            self.save_best_performance_summary(overall_best_trade, overall_best_symbol, best_trades[:3], best_symbols[:3])

    def save_best_performance_summary(self, best_trade, best_symbol, top_trades, top_symbols):
        """Save best performance summary to file."""
        try:
            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(output_dir, f'best_performance_summary_{timestamp}.csv')
            
            # Create summary data
            summary_data = []
            
            # Best single trade
            summary_data.append({
                'Category': 'Best Single Trade',
                'Symbol': best_trade['symbol'],
                'Strategy': best_trade['strategy'],
                'Timeframe': best_trade['timeframe'],
                'Return_Percent': best_trade['pnl_percent'],
                'PnL_Dollars': best_trade['pnl_dollars'],
                'Duration_Days': best_trade['duration_days'],
                'Entry_Time': best_trade['entry_time'],
                'Exit_Time': best_trade['exit_time'],
                'Entry_Price': best_trade['entry_price'],
                'Exit_Price': best_trade['exit_price']
            })
            
            # Best symbol performance
            summary_data.append({
                'Category': 'Best Symbol Performance',
                'Symbol': best_symbol['symbol'],
                'Strategy': best_symbol['strategy'],
                'Timeframe': best_symbol['timeframe'],
                'Return_Percent': best_symbol['total_return_pct'],
                'PnL_Dollars': np.nan,
                'Duration_Days': best_symbol['duration_days'],
                'Entry_Time': np.nan,
                'Exit_Time': np.nan,
                'Entry_Price': np.nan,
                'Exit_Price': np.nan
            })
            
            # Top trades
            for i, trade in enumerate(top_trades, 1):
                summary_data.append({
                    'Category': f'Top Trade #{i}',
                    'Symbol': trade['symbol'],
                    'Strategy': trade['strategy'],
                    'Timeframe': trade['timeframe'],
                    'Return_Percent': trade['pnl_percent'],
                    'PnL_Dollars': trade['pnl_dollars'],
                    'Duration_Days': trade['duration_days'],
                    'Entry_Time': trade['entry_time'],
                    'Exit_Time': trade['exit_time'],
                    'Entry_Price': trade['entry_price'],
                    'Exit_Price': trade['exit_price']
                })
            
            # Top symbols
            for i, symbol in enumerate(top_symbols, 1):
                summary_data.append({
                    'Category': f'Top Symbol #{i}',
                    'Symbol': symbol['symbol'],
                    'Strategy': symbol['strategy'],
                    'Timeframe': symbol['timeframe'],
                    'Return_Percent': symbol['total_return_pct'],
                    'PnL_Dollars': np.nan,
                    'Duration_Days': symbol['duration_days'],
                    'Entry_Time': np.nan,
                    'Exit_Time': np.nan,
                    'Entry_Price': np.nan,
                    'Exit_Price': np.nan
                })
            
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_csv(filename, index=False)
            
            print(f"\n💾 Best performance summary saved to: {filename}")
            
        except Exception as e:
            print(f"⚠️  Error saving best performance summary: {e}")
    
    def generate_signals(self, data):
        """Generate trading signals using the selected strategy."""
        if self.strategy == 'RSI_MACD_VWAP':
            return self.generate_signals_rsi_macd_vwap(data)
        elif self.strategy == 'SMA_Cross':
            return self.generate_signals_sma_cross(data)
        elif self.strategy == 'BB_RSI':
            return self.generate_signals_bb_rsi(data)
        elif self.strategy == 'MACD_Only':
            return self.generate_signals_macd_only(data)
        elif self.strategy == 'Enhanced_Multi_Factor':
            return self.generate_signals_enhanced_multi_factor(data)
        elif self.strategy == 'Optimized_Crypto_V2':
            return self.generate_signals_optimized_crypto_v2(data)
        else:
            print(f"⚠️  Unknown strategy: {self.strategy}, using default RSI_MACD_VWAP")
            return self.generate_signals_rsi_macd_vwap(data)

    def run_strategy_comparison(self, symbols=None):
        """Run comparison of all available strategies."""
        if symbols is None:
            symbols = self.load_crypto_assets()
        
        # Limit symbols for comparison to avoid overwhelming output
        if len(symbols) > 10:
            symbols = symbols[:10]
            print(f"⚠️  Strategy comparison limited to first 10 symbols for performance")
        
        print(f"\n{'='*80}")
        print(f"🔄 STRATEGY COMPARISON MODE")
        print(f"{'='*80}")
        
        strategies = ['RSI_MACD_VWAP', 'SMA_Cross', 'BB_RSI', 'MACD_Only', 'Enhanced_Multi_Factor', 'Optimized_Crypto_V2']
        strategy_results = {}
        
        for strategy in strategies:
            print(f"\n🧪 Testing Strategy: {strategy}")
            print("-" * 50)
            
            # Create a new backtest instance for this strategy
            strategy_backtest = EnhancedCryptoBacktest(
                initial_capital=self.initial_capital,
                position_size=self.position_size,
                bars=self.bars,
                interval=self.interval,
                exchange=self.exchange,
                strategy=strategy,
                verbose=self.verbose
            )
            
            # Run backtest for this strategy
            successful_symbols = []
            for symbol in symbols:
                evaluator = strategy_backtest.run_symbol_backtest(symbol)
                if evaluator:
                    successful_symbols.append(symbol)
            
            # Store results
            strategy_results[strategy] = {
                'successful_symbols': successful_symbols,
                'evaluators': strategy_backtest.evaluators
            }
            
            # Display per-strategy summary table
            if successful_symbols:
                self.display_per_strategy_summary(strategy, successful_symbols, strategy_backtest.evaluators)
        
        # Display comparison results
        self.display_strategy_comparison_results(strategy_results, symbols)
        
        # Generate best trade and strategy summary across all strategies
        self.generate_strategy_comparison_summary(strategy_results)
        
        return strategy_results
    
    def display_strategy_comparison_results(self, strategy_results, symbols):
        """Display strategy comparison results with transposed table."""
        print(f"\n{'='*80}")
        print(f"📊 STRATEGY COMPARISON RESULTS")
        print(f"{'='*80}")
        
        # Create comparison data
        comparison_data = {}
        strategy_names = []
        
        for strategy, results in strategy_results.items():
            strategy_names.append(strategy)
            successful_symbols = results['successful_symbols']
            evaluators = results['evaluators']
            
            if not successful_symbols:
                comparison_data[strategy] = {
                    'Successful': 0,
                    'Total Trades': 0,
                    'Success Rate': "0.0%",
                    'Avg Return': "0.00%",
                    'Avg Sharpe': "0.00",
                    'Avg Max DD': "0.00%",
                    'Rating': "⭐"
                }
                continue
            
            # Calculate aggregate metrics
            total_trades = 0
            total_pnl = 0
            total_return = 0
            sharpe_ratios = []
            max_drawdowns = []
            win_rates = []
            
            for symbol in successful_symbols:
                evaluator = evaluators[symbol]
                kpis = evaluator.calculate_comprehensive_kpis()
                
                if kpis:
                    total_trades += kpis['total_trades']
                    total_pnl += kpis['equity_final'] - evaluator.initial_capital
                    total_return += kpis['total_return_pct']
                    
                    if not np.isnan(kpis['sharpe_ratio']):
                        sharpe_ratios.append(kpis['sharpe_ratio'])
                    if not np.isnan(kpis['max_drawdown_pct']):
                        max_drawdowns.append(kpis['max_drawdown_pct'])
                    if not np.isnan(kpis['win_rate_pct']):
                        win_rates.append(kpis['win_rate_pct'])
            
            # Calculate averages
            avg_return = total_return / len(successful_symbols) if successful_symbols else 0
            avg_sharpe = np.mean(sharpe_ratios) if sharpe_ratios else 0
            avg_max_dd = np.mean(max_drawdowns) if max_drawdowns else 0
            avg_win_rate = np.mean(win_rates) if win_rates else 0
            
            # Success rate
            success_rate = (len(successful_symbols) / len(symbols)) * 100
            
            # Get strategy rating
            rating = self.get_strategy_comparison_rating(avg_return, avg_sharpe, avg_win_rate, success_rate)
            
            comparison_data[strategy] = {
                'Successful': len(successful_symbols),
                'Total Trades': total_trades,
                'Success Rate': f"{success_rate:.1f}%",
                'Avg Return': f"{avg_return:+.2f}%",
                'Avg Sharpe': f"{avg_sharpe:.2f}",
                'Avg Max DD': f"{avg_max_dd:.2f}%",
                'Rating': rating
            }
        
        # Sort strategies by average return
        sorted_strategies = sorted(strategy_names, 
                                 key=lambda x: float(comparison_data[x]['Avg Return'].replace('%', '').replace('+', '')), 
                                 reverse=True)
        
        # Create transposed table data
        metrics = ['Successful', 'Total Trades', 'Success Rate', 'Avg Return', 'Avg Sharpe', 'Avg Max DD', 'Rating']
        transposed_data = []
        
        for metric in metrics:
            row = [metric]
            for strategy in sorted_strategies:
                row.append(comparison_data[strategy][metric])
            transposed_data.append(row)
        
        # Create headers with strategy names
        headers = ['Metric'] + sorted_strategies
        
        print(tabulate(transposed_data, headers=headers, tablefmt='grid'))
        
        # Strategy recommendations
        if sorted_strategies:
            best_strategy = sorted_strategies[0]
            worst_strategy = sorted_strategies[-1]
            
            print(f"\n🏆 BEST STRATEGY: {best_strategy}")
            print(f"   📈 Average Return: {comparison_data[best_strategy]['Avg Return']}")
            print(f"   ⭐ Rating: {comparison_data[best_strategy]['Rating']}")
            print(f"   ✅ Success Rate: {comparison_data[best_strategy]['Success Rate']}")
            
            print(f"\n📉 WORST STRATEGY: {worst_strategy}")
            print(f"   📈 Average Return: {comparison_data[worst_strategy]['Avg Return']}")
            print(f"   ⭐ Rating: {comparison_data[worst_strategy]['Rating']}")
            print(f"   ✅ Success Rate: {comparison_data[worst_strategy]['Success Rate']}")
            
            # Overall recommendation
            best_return = float(comparison_data[best_strategy]['Avg Return'].replace('%', '').replace('+', ''))
            if best_return > 5:
                recommendation = f"🚀 RECOMMENDATION: Use {best_strategy} strategy for live trading"
                color = Fore.GREEN if COLORAMA_AVAILABLE else ""
            elif best_return > 0:
                recommendation = f"⚠️  RECOMMENDATION: {best_strategy} shows promise but needs optimization"
                color = Fore.YELLOW if COLORAMA_AVAILABLE else ""
            else:
                recommendation = "❌ RECOMMENDATION: All strategies show poor performance - major revision needed"
                color = Fore.RED if COLORAMA_AVAILABLE else ""
            
            print(f"\n{color}{recommendation}{Style.RESET_ALL}")
            
            # Display strategy details
            print(f"\n{'='*80}")
            print(f"📋 STRATEGY DETAILS")
            print(f"{'='*80}")
            
            for strategy in sorted_strategies:
                print(f"\n🔍 {strategy}:")
                print(f"   📊 Successful Symbols: {comparison_data[strategy]['Successful']}")
                print(f"   🔄 Total Trades: {comparison_data[strategy]['Total Trades']}")
                print(f"   💹 Average Return: {comparison_data[strategy]['Avg Return']}")
                print(f"   📈 Sharpe Ratio: {comparison_data[strategy]['Avg Sharpe']}")
                print(f"   📉 Max Drawdown: {comparison_data[strategy]['Avg Max DD']}")
                print(f"   ⭐ Rating: {comparison_data[strategy]['Rating']}")
    
    def get_strategy_comparison_rating(self, avg_return, avg_sharpe, avg_win_rate, success_rate):
        """Get strategy rating for comparison."""
        score = 0
        
        # Return score (40%)
        if avg_return > 10:
            score += 2
        elif avg_return > 5:
            score += 1.5
        elif avg_return > 0:
            score += 1
        
        # Sharpe ratio (30%)
        if avg_sharpe > 2:
            score += 1.5
        elif avg_sharpe > 1:
            score += 1
        elif avg_sharpe > 0:
            score += 0.5
        
        # Win rate (20%)
        if avg_win_rate > 70:
            score += 1
        elif avg_win_rate > 50:
            score += 0.5
        
        # Success rate (10%)
        if success_rate > 80:
            score += 0.5
        elif success_rate > 60:
            score += 0.25
        
        # Convert to star rating
        if score >= 4:
            return "⭐⭐⭐⭐⭐"
        elif score >= 3:
            return "⭐⭐⭐⭐"
        elif score >= 2:
            return "⭐⭐⭐"
        elif score >= 1:
            return "⭐⭐"
        else:
            return "⭐"
    
    def display_per_strategy_summary(self, strategy_name, successful_symbols, evaluators):
        """Display summary table for a single strategy showing KPIs for all tested symbols."""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}STRATEGY SUMMARY: {strategy_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        # Define metrics to display
        metrics = [
            'Total Return (%)',
            'Sharpe Ratio',
            'Max Drawdown (%)',
            'Total Trades',
            'Win Rate (%)',
            'Profit Factor'
        ]
        
        # Create header
        header = f"{'Symbol':<15}"
        for metric in metrics:
            header += f"{metric:<18}"
        print(header)
        print("-" * len(header))
        
        # Display each symbol's metrics
        for symbol in successful_symbols:
            if symbol in evaluators:
                evaluator = evaluators[symbol]
                kpis = evaluator.calculate_comprehensive_kpis()
                row = f"{symbol:<15}"
                
                # Total Return
                total_return = kpis.get('total_return_pct', 0.0)
                row += f"{total_return:.2f}%{'':<10}"
                
                # Sharpe Ratio
                sharpe = kpis.get('sharpe_ratio', 0.0)
                row += f"{sharpe:.3f}{'':<13}"
                
                # Max Drawdown
                max_dd = kpis.get('max_drawdown_pct', 0.0)
                row += f"{max_dd:.2f}%{'':<10}"
                
                # Total Trades
                total_trades = kpis.get('total_trades', 0)
                row += f"{total_trades:<18}"
                
                # Win Rate
                win_rate = kpis.get('win_rate_pct', 0.0)
                row += f"{win_rate:.1f}%{'':<12}"
                
                # Profit Factor
                profit_factor = kpis.get('profit_factor', 0.0)
                if profit_factor == float('inf'):
                    row += f"∞{'':<17}"
                else:
                    row += f"{profit_factor:.3f}{'':<13}"
                
                print(row)
        
        print("\n")
    
    def display_detailed_kpis(self, successful_symbols):
        """Display detailed KPIs for each symbol."""
        print(f"\n{'='*80}")
        print(f"📊 COMPREHENSIVE STRATEGY KPIs")
        print(f"{'='*80}")
        
        for symbol in successful_symbols:
            evaluator = self.evaluators[symbol]
            kpis = evaluator.calculate_comprehensive_kpis()
            
            if kpis:
                print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}📈 {symbol} - {self.strategy} Strategy{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
                
                # Time & Duration Metrics
                print(f"\n🕐 TIME & DURATION:")
                print(f"   Start Date: {kpis['start_date'].strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   End Date: {kpis['end_date'].strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Duration: {kpis['duration_days']:.0f} days")
                print(f"   Exposure Time: {kpis['exposure_time_pct']:.1f}%")
                
                # Equity & Returns
                print(f"\n💰 EQUITY & RETURNS:")
                print(f"   Equity Final: ${kpis['equity_final']:,.2f}")
                print(f"   Equity Peak: ${kpis['equity_peak']:,.2f}")
                print(f"   Total Return: {kpis['total_return_pct']:+.2f}%")
                print(f"   Buy & Hold Return: {kpis['buy_hold_return_pct']:+.2f}%")
                print(f"   CAGR: {kpis['cagr_pct']:+.2f}%")
                print(f"   Annualized Return: {kpis['annualized_return_pct']:+.2f}%")
                
                # Risk Metrics
                print(f"\n⚠️  RISK METRICS:")
                print(f"   Volatility (Ann.): {kpis['annualized_volatility_pct']:.2f}%")
                print(f"   Sharpe Ratio: {kpis['sharpe_ratio']:.3f}")
                print(f"   Sortino Ratio: {kpis['sortino_ratio']:.3f}")
                print(f"   Calmar Ratio: {kpis['calmar_ratio']:.3f}")
                print(f"   Alpha: {kpis['alpha_pct']:+.2f}%")
                print(f"   Beta: {kpis['beta']:.3f}")
                
                # Drawdown Metrics
                print(f"\n📉 DRAWDOWN METRICS:")
                print(f"   Max Drawdown: {kpis['max_drawdown_pct']:.2f}%")
                print(f"   Avg Drawdown: {kpis['avg_drawdown_pct']:.2f}%")
                print(f"   Max Drawdown Duration: {kpis['max_drawdown_duration']:.0f} days")
                print(f"   Avg Drawdown Duration: {kpis['avg_drawdown_duration']:.0f} days")
                
                # Trade Statistics
                print(f"\n📊 TRADE STATISTICS:")
                print(f"   Total Trades: {kpis['total_trades']}")
                print(f"   Win Rate: {kpis['win_rate_pct']:.1f}%")
                print(f"   Best Trade: {kpis['best_trade_pct']:+.2f}%")
                print(f"   Worst Trade: {kpis['worst_trade_pct']:+.2f}%")
                print(f"   Average Trade: {kpis['avg_trade_pct']:+.2f}%")
                print(f"   Max Trade Duration: {kpis['max_trade_duration']:.1f} days")
                print(f"   Avg Trade Duration: {kpis['avg_trade_duration']:.1f} days")
                
                # Performance Metrics
                print(f"\n🎯 PERFORMANCE METRICS:")
                profit_factor_str = "∞" if kpis['profit_factor'] == float('inf') else f"{kpis['profit_factor']:.3f}"
                print(f"   Profit Factor: {profit_factor_str}")
                print(f"   Expectancy: {kpis['expectancy_pct']:+.2f}%")
                
                # Strategy Rating
                rating = self.get_strategy_rating(kpis)
                print(f"   Strategy Rating: {rating}")
                
                # Display trade log for this symbol
                self.display_trade_log(symbol, evaluator)
    
    def display_trade_log(self, symbol, evaluator):
        """Display detailed trade log for a symbol."""
        if not evaluator.trades:
            print(f"\n📋 No trades executed for {symbol}")
            return
        
        print(f"\n📋 TRADE LOG - {symbol}")
        print("-" * 80)
        
        # Prepare trade log data
        trade_log_data = []
        for trade in evaluator.trades:
            # Format duration
            duration_str = f"{trade['duration_days']:.1f}d"
            
            # Color coding for P&L
            pnl_dollars_str = f"${trade['pnl_dollars']:+,.2f}"
            pnl_percent_str = f"{trade['pnl_percent']:+.2f}%"
            
            if COLORAMA_AVAILABLE:
                if trade['pnl_dollars'] > 0:
                    pnl_dollars_str = f"{Fore.GREEN}{pnl_dollars_str}{Style.RESET_ALL}"
                    pnl_percent_str = f"{Fore.GREEN}{pnl_percent_str}{Style.RESET_ALL}"
                elif trade['pnl_dollars'] < 0:
                    pnl_dollars_str = f"{Fore.RED}{pnl_dollars_str}{Style.RESET_ALL}"
                    pnl_percent_str = f"{Fore.RED}{pnl_percent_str}{Style.RESET_ALL}"
                else:
                    pnl_dollars_str = f"{Fore.YELLOW}{pnl_dollars_str}{Style.RESET_ALL}"
                    pnl_percent_str = f"{Fore.YELLOW}{pnl_percent_str}{Style.RESET_ALL}"
            
            trade_log_data.append([
                trade['trade_id'],
                trade['symbol'],
                trade['entry_time'].strftime('%Y-%m-%d %H:%M'),
                trade['exit_time'].strftime('%Y-%m-%d %H:%M'),
                f"${trade['entry_price']:.4f}",
                f"${trade['exit_price']:.4f}",
                f"${trade['position_size']:,.0f}",
                pnl_dollars_str,
                pnl_percent_str,
                duration_str,
                trade['trade_type'],
                trade['outcome'],
                trade.get('exit_reason', 'Signal')
            ])
        
        headers = [
            'ID', 'Symbol', 'Entry Time', 'Exit Time', 'Entry Price', 'Exit Price',
            'Position Size', 'P&L ($)', 'P&L (%)', 'Duration', 'Type', 'Outcome', 'Exit Reason'
        ]
        
        print(tabulate(trade_log_data, headers=headers, tablefmt='grid'))
        
        # Trade summary for this symbol
        winning_trades = sum(1 for trade in evaluator.trades if trade['pnl_dollars'] > 0)
        losing_trades = sum(1 for trade in evaluator.trades if trade['pnl_dollars'] < 0)
        total_pnl = sum(trade['pnl_dollars'] for trade in evaluator.trades)
        
        print(f"\n📊 TRADE SUMMARY - {symbol}:")
        print(f"   Total Trades: {len(evaluator.trades)}")
        print(f"   Winning Trades: {winning_trades} ({winning_trades/len(evaluator.trades)*100:.1f}%)")
        print(f"   Losing Trades: {losing_trades} ({losing_trades/len(evaluator.trades)*100:.1f}%)")
        print(f"   Total P&L: ${total_pnl:+,.2f}")

    def generate_strategy_comparison_summary(self, strategy_results):
        """Generate comprehensive summary across all strategies in comparison mode."""
        print(f"\n{'='*80}")
        print(f"🏆 STRATEGY COMPARISON SUMMARY")
        print(f"{'='*80}")
        
        # Aggregate all trades from all strategies
        all_trades = []
        all_strategy_performances = []
        
        for strategy, results in strategy_results.items():
            successful_symbols = results['successful_symbols']
            evaluators = results['evaluators']
            
            if not successful_symbols:
                continue
            
            # Calculate strategy aggregate performance
            total_trades = 0
            total_return = 0
            sharpe_ratios = []
            win_rates = []
            
            for symbol in successful_symbols:
                evaluator = evaluators[symbol]
                kpis = evaluator.calculate_comprehensive_kpis()
                
                if kpis and evaluator.trades:
                    # Track all trades for best trade analysis
                    for trade in evaluator.trades:
                        trade_info = {
                            'symbol': symbol,
                            'strategy': strategy,
                            'timeframe': self.interval,
                            'entry_time': trade['entry_time'],
                            'exit_time': trade['exit_time'],
                            'entry_price': trade['entry_price'],
                            'exit_price': trade['exit_price'],
                            'pnl_percent': trade['pnl_percent'],
                            'pnl_dollars': trade['pnl_dollars'],
                            'duration_days': trade['duration_days'],
                            'trade_type': trade['trade_type'],
                            'exit_reason': trade.get('exit_reason', 'Signal')
                        }
                        all_trades.append(trade_info)
                    
                    # Aggregate metrics
                    total_trades += kpis['total_trades']
                    total_return += kpis['total_return_pct']
                    
                    if not np.isnan(kpis['sharpe_ratio']):
                        sharpe_ratios.append(kpis['sharpe_ratio'])
                    if not np.isnan(kpis['win_rate_pct']):
                        win_rates.append(kpis['win_rate_pct'])
            
            # Calculate strategy averages
            if successful_symbols:
                avg_return = total_return / len(successful_symbols)
                avg_sharpe = np.mean(sharpe_ratios) if sharpe_ratios else 0
                avg_win_rate = np.mean(win_rates) if win_rates else 0
                
                strategy_perf = {
                    'strategy': strategy,
                    'timeframe': self.interval,
                    'symbols_count': len(successful_symbols),
                    'total_trades': total_trades,
                    'avg_return_pct': avg_return,
                    'avg_sharpe': avg_sharpe,
                    'avg_win_rate': avg_win_rate,
                    'success_rate': len(successful_symbols) / len(strategy_results) * 100
                }
                all_strategy_performances.append(strategy_perf)
        
        # Find top 5 best trades across all strategies
        if all_trades:
            best_trades = sorted(all_trades, key=lambda x: x['pnl_percent'], reverse=True)[:5]
            
            print(f"\n🎯 TOP 5 BEST TRADES ACROSS ALL STRATEGIES:")
            print("-" * 80)
            
            best_trades_data = []
            for i, trade in enumerate(best_trades, 1):
                color = ""
                reset = ""
                if COLORAMA_AVAILABLE:
                    if trade['pnl_percent'] > 10:
                        color = Fore.GREEN
                        reset = Style.RESET_ALL
                    elif trade['pnl_percent'] > 5:
                        color = Fore.YELLOW
                        reset = Style.RESET_ALL
                
                best_trades_data.append([
                    f"#{i}",
                    trade['symbol'],
                    trade['strategy'],
                    trade['timeframe'],
                    trade['entry_time'].strftime('%Y-%m-%d %H:%M'),
                    trade['exit_time'].strftime('%Y-%m-%d %H:%M'),
                    f"${trade['entry_price']:.4f}",
                    f"${trade['exit_price']:.4f}",
                    f"{color}{trade['pnl_percent']:+.2f}%{reset}",
                    f"{color}${trade['pnl_dollars']:+,.2f}{reset}",
                    f"{trade['duration_days']:.1f}d",
                    trade['exit_reason']
                ])
            
            headers = [
                'Rank', 'Symbol', 'Strategy', 'Timeframe', 'Entry Time', 'Exit Time',
                'Entry Price', 'Exit Price', 'Return (%)', 'P&L ($)', 'Duration', 'Exit Reason'
            ]
            
            print(tabulate(best_trades_data, headers=headers, tablefmt='grid'))
        
        # Find best performing strategies
        if all_strategy_performances:
            best_strategies = sorted(all_strategy_performances, key=lambda x: x['avg_return_pct'], reverse=True)
            
            print(f"\n🏅 STRATEGY PERFORMANCE RANKING:")
            print("-" * 80)
            
            strategy_ranking_data = []
            for i, perf in enumerate(best_strategies, 1):
                color = ""
                reset = ""
                if COLORAMA_AVAILABLE:
                    if perf['avg_return_pct'] > 1:
                        color = Fore.GREEN
                        reset = Style.RESET_ALL
                    elif perf['avg_return_pct'] > 0:
                        color = Fore.YELLOW
                        reset = Style.RESET_ALL
                    else:
                        color = Fore.RED
                        reset = Style.RESET_ALL
                
                strategy_ranking_data.append([
                    f"#{i}",
                    perf['strategy'],
                    perf['timeframe'],
                    f"{color}{perf['avg_return_pct']:+.2f}%{reset}",
                    f"{perf['avg_sharpe']:.2f}",
                    f"{perf['avg_win_rate']:.1f}%",
                    perf['total_trades'],
                    perf['symbols_count'],
                    f"{perf['success_rate']:.1f}%"
                ])
            
            headers = [
                'Rank', 'Strategy', 'Timeframe', 'Avg Return', 'Avg Sharpe',
                'Avg Win Rate', 'Total Trades', 'Symbols', 'Success Rate'
            ]
            
            print(tabulate(strategy_ranking_data, headers=headers, tablefmt='grid'))
        
        # Overall insights
        if all_trades and all_strategy_performances:
            overall_best_trade = max(all_trades, key=lambda x: x['pnl_percent'])
            overall_best_strategy = max(all_strategy_performances, key=lambda x: x['avg_return_pct'])
            
            print(f"\n🏆 OVERALL BEST PERFORMANCE ACROSS ALL STRATEGIES:")
            print("-" * 80)
            
            # Best single trade across all strategies
            print(f"💎 BEST SINGLE TRADE (ANY STRATEGY):")
            print(f"   Symbol: {overall_best_trade['symbol']}")
            print(f"   Strategy: {overall_best_trade['strategy']}")
            print(f"   Timeframe: {overall_best_trade['timeframe']}")
            print(f"   Return: {overall_best_trade['pnl_percent']:+.2f}%")
            print(f"   P&L: ${overall_best_trade['pnl_dollars']:+,.2f}")
            print(f"   Duration: {overall_best_trade['duration_days']:.1f} days")
            print(f"   Entry: {overall_best_trade['entry_time'].strftime('%Y-%m-%d %H:%M')} @ ${overall_best_trade['entry_price']:.4f}")
            print(f"   Exit: {overall_best_trade['exit_time'].strftime('%Y-%m-%d %H:%M')} @ ${overall_best_trade['exit_price']:.4f}")
            
            # Best strategy performance
            print(f"\n🥇 BEST STRATEGY PERFORMANCE:")
            print(f"   Strategy: {overall_best_strategy['strategy']}")
            print(f"   Timeframe: {overall_best_strategy['timeframe']}")
            print(f"   Average Return: {overall_best_strategy['avg_return_pct']:+.2f}%")
            print(f"   Average Sharpe: {overall_best_strategy['avg_sharpe']:.2f}")
            print(f"   Average Win Rate: {overall_best_strategy['avg_win_rate']:.1f}%")
            print(f"   Total Trades: {overall_best_strategy['total_trades']}")
            print(f"   Symbols Analyzed: {overall_best_strategy['symbols_count']}")
            print(f"   Success Rate: {overall_best_strategy['success_rate']:.1f}%")
            
            # Strategy recommendation
            print(f"\n💡 STRATEGY RECOMMENDATION:")
            if overall_best_strategy['avg_return_pct'] > 5 and overall_best_strategy['success_rate'] > 60:
                recommendation = f"🚀 EXCELLENT: {overall_best_strategy['strategy']} strategy is highly recommended for {self.interval} timeframe"
                color = Fore.GREEN if COLORAMA_AVAILABLE else ""
            elif overall_best_strategy['avg_return_pct'] > 0 and overall_best_strategy['success_rate'] > 40:
                recommendation = f"👍 GOOD: {overall_best_strategy['strategy']} strategy shows promise for {self.interval} timeframe"
                color = Fore.YELLOW if COLORAMA_AVAILABLE else ""
            else:
                recommendation = f"⚠️  CAUTION: Consider optimizing {overall_best_strategy['strategy']} strategy for {self.interval} timeframe"
                color = Fore.RED if COLORAMA_AVAILABLE else ""
            
            print(f"   {color}{recommendation}{Style.RESET_ALL if COLORAMA_AVAILABLE else ''}")
            
            # Summary statistics
            total_strategies_tested = len(all_strategy_performances)
            profitable_strategies = sum(1 for s in all_strategy_performances if s['avg_return_pct'] > 0)
            total_trades_all = sum(s['total_trades'] for s in all_strategy_performances)
            
            print(f"\n📊 COMPARISON SUMMARY:")
            print(f"   Strategies Tested: {total_strategies_tested}")
            print(f"   Profitable Strategies: {profitable_strategies} ({profitable_strategies/total_strategies_tested*100:.1f}%)")
            print(f"   Total Trades Executed: {total_trades_all}")
            print(f"   Best Trade Return: {overall_best_trade['pnl_percent']:+.2f}%")
            print(f"   Best Strategy Average: {overall_best_strategy['avg_return_pct']:+.2f}%")
            
            # Save comparison summary
            self.save_strategy_comparison_summary(overall_best_trade, overall_best_strategy, 
                                                 best_trades[:3], best_strategies[:3])

    def save_strategy_comparison_summary(self, best_trade, best_strategy, top_trades, top_strategies):
        """Save strategy comparison summary to file."""
        try:
            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(output_dir, f'strategy_comparison_summary_{timestamp}.csv')
            
            # Create summary data
            summary_data = []
            
            # Best single trade across all strategies
            summary_data.append({
                'Category': 'Best Single Trade (All Strategies)',
                'Strategy': best_trade['strategy'],
                'Symbol': best_trade['symbol'],
                'Timeframe': best_trade['timeframe'],
                'Return_Percent': best_trade['pnl_percent'],
                'PnL_Dollars': best_trade['pnl_dollars'],
                'Duration_Days': best_trade['duration_days'],
                'Entry_Time': best_trade['entry_time'],
                'Exit_Time': best_trade['exit_time'],
                'Entry_Price': best_trade['entry_price'],
                'Exit_Price': best_trade['exit_price'],
                'Win_Rate': np.nan,
                'Total_Trades': np.nan,
                'Symbols_Count': np.nan,
                'Success_Rate': np.nan
            })
            
            # Best strategy performance
            summary_data.append({
                'Category': 'Best Strategy Performance',
                'Strategy': best_strategy['strategy'],
                'Symbol': 'AGGREGATE',
                'Timeframe': best_strategy['timeframe'],
                'Return_Percent': best_strategy['avg_return_pct'],
                'PnL_Dollars': np.nan,
                'Duration_Days': np.nan,
                'Entry_Time': np.nan,
                'Exit_Time': np.nan,
                'Entry_Price': np.nan,
                'Exit_Price': np.nan,
                'Win_Rate': best_strategy['avg_win_rate'],
                'Total_Trades': best_strategy['total_trades'],
                'Symbols_Count': best_strategy['symbols_count'],
                'Success_Rate': best_strategy['success_rate']
            })
            
            # Top trades
            for i, trade in enumerate(top_trades, 1):
                summary_data.append({
                    'Category': f'Top Trade #{i} (All Strategies)',
                    'Strategy': trade['strategy'],
                    'Symbol': trade['symbol'],
                    'Timeframe': trade['timeframe'],
                    'Return_Percent': trade['pnl_percent'],
                    'PnL_Dollars': trade['pnl_dollars'],
                    'Duration_Days': trade['duration_days'],
                    'Entry_Time': trade['entry_time'],
                    'Exit_Time': trade['exit_time'],
                    'Entry_Price': trade['entry_price'],
                    'Exit_Price': trade['exit_price'],
                    'Win_Rate': np.nan,
                    'Total_Trades': np.nan,
                    'Symbols_Count': np.nan,
                    'Success_Rate': np.nan
                })
            
            # Top strategies
            for i, strategy in enumerate(top_strategies, 1):
                summary_data.append({
                    'Category': f'Top Strategy #{i}',
                    'Strategy': strategy['strategy'],
                    'Symbol': 'AGGREGATE',
                    'Timeframe': strategy['timeframe'],
                    'Return_Percent': strategy['avg_return_pct'],
                    'PnL_Dollars': np.nan,
                    'Duration_Days': np.nan,
                    'Entry_Time': np.nan,
                    'Exit_Time': np.nan,
                    'Entry_Price': np.nan,
                    'Exit_Price': np.nan,
                    'Win_Rate': strategy['avg_win_rate'],
                    'Total_Trades': strategy['total_trades'],
                    'Symbols_Count': strategy['symbols_count'],
                    'Success_Rate': strategy['success_rate']
                })
            
            # Save to CSV
            df = pd.DataFrame(summary_data)
            df.to_csv(filename, index=False)
            
            print(f"💾 Strategy comparison summary saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving strategy comparison summary: {e}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Enhanced Crypto Backtest with Comprehensive KPIs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python enhanced_crypto_backtest.py                           # Run on all symbols
  python enhanced_crypto_backtest.py --symbols BTC/USDT ETH/USDT  # Run on specific symbols
  python enhanced_crypto_backtest.py --capital 50000 --position 5000  # Custom capital and position
  python enhanced_crypto_backtest.py --bars 1440 --interval 4h       # Use 4h bars, 1440 periods
  python enhanced_crypto_backtest.py --exchange binance              # Use Binance exchange
        '''
    )
    
    parser.add_argument(
        '--symbols', '-s',
        nargs='+',
        help='Specific symbols to backtest (e.g., BTC/USDT ETH/USDT)',
        default=None
    )
    
    parser.add_argument(
        '--capital', '-c',
        type=float,
        help='Initial capital for backtest (default: 100000)',
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
        choices=['1m', '5m', '15m', '30m', '1h', '4h', '1d'],
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
        help='Enable strategy comparison mode'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output directory for results (default: output)',
        default='output'
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
    
    print(f"{Fore.CYAN}🚀 Enhanced Crypto Backtest with Comprehensive KPIs{Style.RESET_ALL}")
    print("=" * 80)
    
    # Initialize backtest with CLI arguments
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
        print(f"{Fore.YELLOW}🎯 Using specific symbols: {', '.join(crypto_symbols)}{Style.RESET_ALL}")
    else:
        crypto_symbols = backtest.load_crypto_assets()
    
    print(f"💰 Initial Capital: ${backtest.initial_capital:,.2f}")
    print(f"📊 Position Size: ${backtest.position_size:,.2f} per trade")
    print(f"🔍 Scanning {len(crypto_symbols)} crypto symbols")
    print(f"📈 Strategy: {args.strategy}")
    print(f"📊 Exchange: {args.exchange}")
    print(f"⏰ Interval: {args.interval} | Bars: {args.bars}")
    
    if args.compare:
        print(f"{Fore.MAGENTA}🔄 Strategy Comparison Mode Enabled{Style.RESET_ALL}")
        print("=" * 80)
        backtest.run_strategy_comparison(crypto_symbols)
        return
        
    print("=" * 80)
    
    # Run the backtest
    successful_symbols = backtest.run_comprehensive_backtest(crypto_symbols)
    
    print(f"\n{Fore.GREEN}🎉 Backtest completed successfully!{Style.RESET_ALL}")
    print(f"📊 Check the {args.output}/ directory for detailed reports")
    print(f"🔍 {len(successful_symbols)} symbols analyzed with full KPIs")


if __name__ == "__main__":
    main()
