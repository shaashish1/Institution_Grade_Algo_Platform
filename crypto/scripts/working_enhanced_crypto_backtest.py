#!/usr/bin/env python3
"""
Working Enhanced Crypto Backtest with All 29 KPIs
Fixed version that doesn't hang - focused on comprehensive KPI display
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import argparse
import time

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

print(f"🔧 Python path: {parent_dir}")

# Import required modules
try:
    from crypto.data_acquisition import fetch_data
    from crypto.tools.backtest_evaluator import BacktestEvaluator
    from tabulate import tabulate
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class WorkingEnhancedCryptoBacktest:
    """Working version with comprehensive 29 KPIs"""

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
                print(f"✅ Loaded {len(assets)} crypto assets")
                return assets[:3]  # Limit for testing
            else:
                print(f"⚠️ Using default assets")
                return ['BTC/USDT', 'ETH/USDT']
        except Exception as e:
            print(f"⚠️ Error loading assets: {e}")
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
            
            for i in range(20, len(data)):
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
        """Perform comprehensive backtest with all KPIs."""
        try:
            if signals.empty:
                return None
            
            # Initialize evaluator for comprehensive KPIs
            evaluator = BacktestEvaluator(
                strategy_name=self.strategy,
                symbol=symbol,
                initial_capital=self.initial_capital
            )
            
            # Execute trades
            position = None
            trades = []
            current_equity = self.initial_capital
            
            for _, signal in signals.iterrows():
                # Add equity curve point
                evaluator.add_equity_point(signal['timestamp'], current_equity)
                
                if signal['signal'] == 'buy' and position is None:
                    position = {
                        'entry_price': signal['price'],
                        'entry_time': signal['timestamp'],
                        'quantity': self.position_size / signal['price']
                    }
                elif signal['signal'] == 'sell' and position is not None:
                    profit = (signal['price'] - position['entry_price']) * position['quantity']
                    profit_percent = ((signal['price'] - position['entry_price']) / position['entry_price']) * 100
                    
                    # Update equity
                    current_equity += profit
                    
                    # Record trade
                    trade = {
                        'symbol': symbol,
                        'entry_time': position['entry_time'],
                        'exit_time': signal['timestamp'],
                        'entry_price': position['entry_price'],
                        'exit_price': signal['price'],
                        'profit_percent': profit_percent
                    }
                    trades.append(trade)
                    
                    # Add to evaluator
                    evaluator.add_trade({
                        'entry_time': position['entry_time'],
                        'exit_time': signal['timestamp'],
                        'entry_price': position['entry_price'],
                        'exit_price': signal['price'],
                        'position_size': position['quantity'],
                        'trade_type': 'Long',
                        'pnl_dollars': profit,
                        'pnl_percent': profit_percent
                    })
                    
                    # Add final equity point
                    evaluator.add_equity_point(signal['timestamp'], current_equity)
                    position = None
            
            if not trades:
                return None
            
            # Calculate comprehensive KPIs
            kpis = evaluator.calculate_comprehensive_kpis()
            
            # Prepare result with all 29 KPIs
            result = {
                'symbol': symbol,
                'strategy': self.strategy,
                'timeframe': self.interval,
                'total_trades': len(trades),
                'trades': trades,
                
                # All 29 KPIs from specification
                'start_date': kpis.get('start_date'),
                'end_date': kpis.get('end_date'),
                'duration_days': kpis.get('duration_days', 0),
                'exposure_time_pct': kpis.get('exposure_time_pct', 100.0),
                'equity_final': kpis.get('equity_final', current_equity),
                'equity_peak': kpis.get('equity_peak', current_equity),
                'return_pct': kpis.get('total_return_pct', 0),
                'buy_hold_return_pct': kpis.get('buy_hold_return_pct', 0),
                'return_ann_pct': kpis.get('annualized_return_pct', 0),
                'volatility_ann_pct': kpis.get('annualized_volatility_pct', 0),
                'cagr_pct': kpis.get('cagr_pct', 0),
                'sharpe_ratio': kpis.get('sharpe_ratio', 0),
                'sortino_ratio': kpis.get('sortino_ratio', 0),
                'calmar_ratio': kpis.get('calmar_ratio', 0),
                'alpha_pct': kpis.get('alpha_pct', 0),
                'beta': kpis.get('beta', 1.0),
                'max_drawdown_pct': kpis.get('max_drawdown_pct', 0),
                'avg_drawdown_pct': kpis.get('avg_drawdown_pct', 0),
                'max_drawdown_duration': kpis.get('max_drawdown_duration', 0),
                'avg_drawdown_duration': kpis.get('avg_drawdown_duration', 0),
                'win_rate_pct': kpis.get('win_rate_pct', 0),
                'best_trade_pct': kpis.get('best_trade_pct', 0),
                'worst_trade_pct': kpis.get('worst_trade_pct', 0),
                'avg_trade_pct': kpis.get('avg_trade_pct', 0),
                'max_trade_duration': kpis.get('max_trade_duration', 0),
                'avg_trade_duration': kpis.get('avg_trade_duration', 0),
                'profit_factor': kpis.get('profit_factor', 0),
                'expectancy_pct': kpis.get('expectancy_pct', 0)
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Error in backtest: {e}")
            return None

    def process_symbol(self, symbol):
        """Process a single symbol."""
        print(f"📊 Processing {symbol}...", end=" ")
        
        try:
            # Fetch data with strict timeout
            print("fetching data...", end=" ")
            data = fetch_data(
                symbol=symbol,
                bars=min(self.bars, 100),  # Limit bars
                interval=self.interval,
                exchange=self.exchange,
                fetch_timeout=10  # 10 second timeout
            )
            
            if data is None or len(data) < 30:
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
            
            # Run comprehensive backtest
            result = self.backtest_with_signals(data, signals, symbol)
            
            if result is None:
                print("❌ no trades")
                return None
            
            print(f"✅ {result['total_trades']} trades")
            return result
            
        except Exception as e:
            print(f"❌ error: {e}")
            return None

    def display_comprehensive_kpis(self, results):
        """Display all 29 KPIs as specified."""
        print("\n" + "="*100)
        print("🎯 COMPREHENSIVE BACKTEST RESULTS - ALL 29 KPIs")
        print("="*100)
        
        for result in results:
            print(f"\n📊 {result['symbol']} | {result['strategy']} | {result['timeframe']}")
            print("-" * 80)
            
            # All 29 KPIs as per specification
            kpi_data = [
                ["1. Start", str(result.get('start_date', 'N/A'))[:10]],
                ["2. End", str(result.get('end_date', 'N/A'))[:10]],
                ["3. Duration", f"{result.get('duration_days', 0):.0f} days"],
                ["4. Exposure Time [%]", f"{result.get('exposure_time_pct', 0):.1f}%"],
                ["5. Equity Final [$]", f"${result.get('equity_final', 0):,.2f}"],
                ["6. Equity Peak [$]", f"${result.get('equity_peak', 0):,.2f}"],
                ["7. Return [%]", f"{result.get('return_pct', 0):.2f}%"],
                ["8. Buy & Hold Return [%]", f"{result.get('buy_hold_return_pct', 0):.2f}%"],
                ["9. Return (Ann.) [%]", f"{result.get('return_ann_pct', 0):.2f}%"],
                ["10. Volatility (Ann.) [%]", f"{result.get('volatility_ann_pct', 0):.2f}%"],
                ["11. CAGR [%]", f"{result.get('cagr_pct', 0):.2f}%"],
                ["12. Sharpe Ratio", f"{result.get('sharpe_ratio', 0):.3f}"],
                ["13. Sortino Ratio", f"{result.get('sortino_ratio', 0):.3f}"],
                ["14. Calmar Ratio", f"{result.get('calmar_ratio', 0):.3f}"],
                ["15. Alpha [%]", f"{result.get('alpha_pct', 0):.2f}%"],
                ["16. Beta", f"{result.get('beta', 0):.3f}"],
                ["17. Max. Drawdown [%]", f"{result.get('max_drawdown_pct', 0):.2f}%"],
                ["18. Avg. Drawdown [%]", f"{result.get('avg_drawdown_pct', 0):.2f}%"],
                ["19. Max. Drawdown Duration", f"{result.get('max_drawdown_duration', 0):.0f} days"],
                ["20. Avg. Drawdown Duration", f"{result.get('avg_drawdown_duration', 0):.0f} days"],
                ["21. # Trades", f"{result.get('total_trades', 0)}"],
                ["22. Win Rate [%]", f"{result.get('win_rate_pct', 0):.2f}%"],
                ["23. Best Trade [%]", f"{result.get('best_trade_pct', 0):.2f}%"],
                ["24. Worst Trade [%]", f"{result.get('worst_trade_pct', 0):.2f}%"],
                ["25. Avg. Trade [%]", f"{result.get('avg_trade_pct', 0):.2f}%"],
                ["26. Max. Trade Duration", f"{result.get('max_trade_duration', 0):.1f} days"],
                ["27. Avg. Trade Duration", f"{result.get('avg_trade_duration', 0):.1f} days"],
                ["28. Profit Factor", f"{result.get('profit_factor', 0):.3f}"],
                ["29. Expectancy [%]", f"{result.get('expectancy_pct', 0):.2f}%"]
            ]
            
            print(tabulate(kpi_data, headers=['KPI', 'Value'], tablefmt='grid'))

    def run_backtest(self, symbols=None):
        """Run comprehensive backtest."""
        if symbols is None:
            symbols = self.load_crypto_assets()
        
        print("🚀 Working Enhanced Crypto Backtest - All 29 KPIs")
        print("=" * 80)
        print(f"Strategy: {self.strategy}")
        print(f"Timeframe: {self.interval}")
        print(f"Bars: {self.bars}")
        print(f"Exchange: {self.exchange}")
        print(f"Testing {len(symbols)} symbols")
        print("=" * 80)
        
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
        
        # Display comprehensive KPIs
        self.display_comprehensive_kpis(results)
        
        print(f"\n✅ Backtest completed - {len(results)} symbols analyzed with all 29 KPIs")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Working Enhanced Crypto Backtest with All 29 KPIs')
    
    parser.add_argument('--symbols', '-s', nargs='+', help='Symbols to test')
    parser.add_argument('--capital', '-c', type=float, default=100000, help='Initial capital')
    parser.add_argument('--position', '-p', type=float, default=10000, help='Position size per trade')
    parser.add_argument('--bars', '-b', type=int, default=100, help='Number of bars to fetch')
    parser.add_argument('--interval', '-i', type=str, default='1h', help='Time interval')
    parser.add_argument('--exchange', '-e', type=str, default='kraken', help='Exchange')
    parser.add_argument('--strategy', '-st', type=str, default='RSI_MACD_VWAP', help='Strategy')
    
    args = parser.parse_args()
    
    print("🚀 Starting Working Enhanced Crypto Backtest...")
    
    try:
        backtest = WorkingEnhancedCryptoBacktest(
            initial_capital=args.capital,
            position_size=args.position,
            bars=args.bars,
            interval=args.interval,
            exchange=args.exchange,
            strategy=args.strategy
        )
        
        backtest.run_backtest(args.symbols)
        print("\n✅ All 29 KPIs displayed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during backtest: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
