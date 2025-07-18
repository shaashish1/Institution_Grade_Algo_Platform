"""
Backtest Engine
==============

Comprehensive backtesting engine for trading strategies.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path

class BacktestEngine:
    """Main backtesting engine"""
    
    def __init__(self):
        self.results_dir = Path("reports/backtests")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.current_backtest = None
        self.backtest_history = []
    
    def quick_backtest_wizard(self):
        """Quick backtest setup wizard"""
        print("\n🚀 Quick Backtest Wizard")
        print("=" * 25)
        
        try:
            # Get user inputs
            print("Let's set up a quick backtest!")
            
            # Asset selection
            asset_type = input("Asset type (crypto/stock) [crypto]: ").strip().lower() or "crypto"
            
            if asset_type == "crypto":
                symbol = input("Crypto symbol [BTC/USDT]: ").strip().upper() or "BTC/USDT"
            else:
                symbol = input("Stock symbol [NSE:SBIN-EQ]: ").strip().upper() or "NSE:SBIN-EQ"
            
            # Strategy selection
            print("\nAvailable strategies:")
            print("1. SMA Crossover")
            print("2. RSI Mean Reversion")
            print("3. MACD Signal")
            print("4. Bollinger Bands")
            
            strategy_choice = input("Select strategy (1-4) [1]: ").strip() or "1"
            strategy_map = {
                "1": "sma_crossover",
                "2": "rsi_mean_reversion", 
                "3": "macd_signal",
                "4": "bollinger_bands"
            }
            strategy = strategy_map.get(strategy_choice, "sma_crossover")
            
            # Timeframe
            timeframe = input("Timeframe (1h/4h/1d) [1h]: ").strip() or "1h"
            
            # Period
            days = input("Backtest period in days [30]: ").strip()
            try:
                days = int(days) if days else 30
            except:
                days = 30
            
            # Initial capital
            capital = input("Initial capital [10000]: ").strip()
            try:
                capital = float(capital) if capital else 10000.0
            except:
                capital = 10000.0
            
            print(f"\n🔄 Running backtest...")
            print(f"   Asset: {symbol}")
            print(f"   Strategy: {strategy.replace('_', ' ').title()}")
            print(f"   Timeframe: {timeframe}")
            print(f"   Period: {days} days")
            print(f"   Capital: ${capital:,.2f}")
            
            # Run the backtest
            results = self.run_backtest(
                symbol=symbol,
                strategy=strategy,
                timeframe=timeframe,
                days=days,
                initial_capital=capital,
                asset_type=asset_type
            )
            
            if results:
                self.display_backtest_results(results)
            
        except Exception as e:
            print(f"❌ Error in quick backtest: {e}")
    
    def run_backtest(self, symbol: str, strategy: str, timeframe: str = '1h', 
                     days: int = 30, initial_capital: float = 10000.0, 
                     asset_type: str = 'crypto') -> Optional[Dict]:
        """Run a backtest with specified parameters"""
        try:
            # Generate or fetch historical data
            data = self.get_historical_data(symbol, timeframe, days, asset_type)
            if data is None or data.empty:
                print(f"❌ No data available for {symbol}")
                return None
            
            # Apply strategy
            signals = self.apply_strategy(data, strategy)
            if signals is None:
                print(f"❌ Strategy {strategy} failed")
                return None
            
            # Calculate returns
            portfolio = self.calculate_portfolio_performance(data, signals, initial_capital)
            
            # Calculate metrics
            metrics = self.calculate_performance_metrics(portfolio, data)
            
            # Create results
            results = {
                'symbol': symbol,
                'strategy': strategy,
                'timeframe': timeframe,
                'days': days,
                'initial_capital': initial_capital,
                'asset_type': asset_type,
                'start_date': data.index[0].strftime('%Y-%m-%d'),
                'end_date': data.index[-1].strftime('%Y-%m-%d'),
                'data': data,
                'signals': signals,
                'portfolio': portfolio,
                'metrics': metrics,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save results
            self.save_backtest_results(results)
            self.current_backtest = results
            
            return results
            
        except Exception as e:
            print(f"❌ Backtest error: {e}")
            return None
    
    def get_historical_data(self, symbol: str, timeframe: str, days: int, asset_type: str) -> Optional[pd.DataFrame]:
        """Get historical data for backtesting"""
        try:
            if asset_type == 'crypto':
                return self.get_crypto_data(symbol, timeframe, days)
            else:
                return self.get_stock_data(symbol, timeframe, days)
        except Exception as e:
            print(f"❌ Error getting historical data: {e}")
            return None
    
    def get_crypto_data(self, symbol: str, timeframe: str, days: int) -> Optional[pd.DataFrame]:
        """Get crypto historical data"""
        try:
            # Try to get real data from crypto trader
            from ..crypto.crypto_trader import CryptoTrader
            
            trader = CryptoTrader()
            
            # Calculate limit based on timeframe
            if timeframe == '1h':
                limit = days * 24
            elif timeframe == '4h':
                limit = days * 6
            elif timeframe == '1d':
                limit = days
            else:
                limit = days * 24
            
            df = trader.get_historical_data(symbol, timeframe, limit)
            
            if df is not None and not df.empty:
                return df
            else:
                # Generate synthetic data as fallback
                return self.generate_synthetic_data(symbol, days, timeframe)
                
        except Exception as e:
            print(f"⚠️  Using synthetic data for {symbol}: {e}")
            return self.generate_synthetic_data(symbol, days, timeframe)
    
    def get_stock_data(self, symbol: str, timeframe: str, days: int) -> Optional[pd.DataFrame]:
        """Get stock historical data"""
        try:
            # Try to get real stock data
            import yfinance as yf
            
            # Convert symbol format if needed
            ticker_symbol = symbol.replace('NSE:', '').replace('-EQ', '.NS')
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            ticker = yf.Ticker(ticker_symbol)
            df = ticker.history(start=start_date, end=end_date, interval='1h' if timeframe == '1h' else '1d')
            
            if not df.empty:
                # Rename columns to match our format
                df.columns = [col.lower() for col in df.columns]
                return df
            else:
                return self.generate_synthetic_data(symbol, days, timeframe)
                
        except Exception as e:
            print(f"⚠️  Using synthetic data for {symbol}: {e}")
            return self.generate_synthetic_data(symbol, days, timeframe)
    
    def generate_synthetic_data(self, symbol: str, days: int, timeframe: str) -> pd.DataFrame:
        """Generate synthetic price data for backtesting"""
        try:
            # Calculate number of periods
            if timeframe == '1h':
                periods = days * 24
                freq = 'H'
            elif timeframe == '4h':
                periods = days * 6
                freq = '4H'
            elif timeframe == '1d':
                periods = days
                freq = 'D'
            else:
                periods = days * 24
                freq = 'H'
            
            # Create date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            dates = pd.date_range(start=start_date, end=end_date, periods=periods)
            
            # Generate realistic price data using geometric Brownian motion
            np.random.seed(42)  # For reproducible results
            
            # Starting price based on symbol
            if 'BTC' in symbol:
                start_price = 45000
            elif 'ETH' in symbol:
                start_price = 3000
            elif 'SBIN' in symbol:
                start_price = 500
            else:
                start_price = 100
            
            # Parameters for price simulation
            mu = 0.0001  # drift
            sigma = 0.02  # volatility
            
            # Generate price series
            returns = np.random.normal(mu, sigma, periods)
            price_series = [start_price]
            
            for i in range(1, periods):
                price = price_series[-1] * (1 + returns[i])
                price_series.append(max(price, start_price * 0.1))  # Prevent negative prices
            
            # Create OHLCV data
            df = pd.DataFrame(index=dates)
            df['close'] = price_series
            
            # Generate OHLC from close prices
            df['open'] = df['close'].shift(1).fillna(df['close'].iloc[0])
            df['high'] = df[['open', 'close']].max(axis=1) * (1 + np.random.uniform(0, 0.01, len(df)))
            df['low'] = df[['open', 'close']].min(axis=1) * (1 - np.random.uniform(0, 0.01, len(df)))
            df['volume'] = np.random.uniform(1000, 10000, len(df))
            
            return df
            
        except Exception as e:
            print(f"❌ Error generating synthetic data: {e}")
            return pd.DataFrame()
    
    def apply_strategy(self, data: pd.DataFrame, strategy: str) -> Optional[pd.DataFrame]:
        """Apply trading strategy to generate signals"""
        try:
            df = data.copy()
            
            if strategy == 'sma_crossover':
                return self.sma_crossover_strategy(df)
            elif strategy == 'rsi_mean_reversion':
                return self.rsi_mean_reversion_strategy(df)
            elif strategy == 'macd_signal':
                return self.macd_signal_strategy(df)
            elif strategy == 'bollinger_bands':
                return self.bollinger_bands_strategy(df)
            else:
                print(f"❌ Unknown strategy: {strategy}")
                return None
                
        except Exception as e:
            print(f"❌ Error applying strategy: {e}")
            return None
    
    def sma_crossover_strategy(self, df: pd.DataFrame) -> pd.DataFrame:
        """Simple Moving Average Crossover Strategy"""
        # Calculate SMAs
        df['sma_short'] = df['close'].rolling(window=10).mean()
        df['sma_long'] = df['close'].rolling(window=30).mean()
        
        # Generate signals
        df['signal'] = 0
        df['signal'][df['sma_short'] > df['sma_long']] = 1  # Buy signal
        df['signal'][df['sma_short'] < df['sma_long']] = -1  # Sell signal
        
        # Generate positions (1 for long, 0 for no position, -1 for short)
        df['position'] = df['signal'].diff()
        
        return df
    
    def rsi_mean_reversion_strategy(self, df: pd.DataFrame) -> pd.DataFrame:
        """RSI Mean Reversion Strategy"""
        # Calculate RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Generate signals
        df['signal'] = 0
        df['signal'][df['rsi'] < 30] = 1  # Buy when oversold
        df['signal'][df['rsi'] > 70] = -1  # Sell when overbought
        
        df['position'] = df['signal'].diff()
        
        return df
    
    def macd_signal_strategy(self, df: pd.DataFrame) -> pd.DataFrame:
        """MACD Signal Strategy"""
        # Calculate MACD
        exp1 = df['close'].ewm(span=12).mean()
        exp2 = df['close'].ewm(span=26).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # Generate signals
        df['signal'] = 0
        df['signal'][df['macd'] > df['macd_signal']] = 1  # Buy signal
        df['signal'][df['macd'] < df['macd_signal']] = -1  # Sell signal
        
        df['position'] = df['signal'].diff()
        
        return df
    
    def bollinger_bands_strategy(self, df: pd.DataFrame) -> pd.DataFrame:
        """Bollinger Bands Strategy"""
        # Calculate Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        # Generate signals
        df['signal'] = 0
        df['signal'][df['close'] < df['bb_lower']] = 1  # Buy when price below lower band
        df['signal'][df['close'] > df['bb_upper']] = -1  # Sell when price above upper band
        
        df['position'] = df['signal'].diff()
        
        return df
    
    def calculate_portfolio_performance(self, data: pd.DataFrame, signals: pd.DataFrame, initial_capital: float) -> pd.DataFrame:
        """Calculate portfolio performance"""
        try:
            df = signals.copy()
            
            # Initialize portfolio
            df['holdings'] = 0.0
            df['cash'] = initial_capital
            df['total'] = initial_capital
            df['returns'] = 0.0
            
            current_cash = initial_capital
            current_holdings = 0.0
            
            for i in range(1, len(df)):
                if pd.isna(df['position'].iloc[i]):
                    continue
                
                # Check for buy signal
                if df['position'].iloc[i] > 0 and current_cash > 0:
                    # Buy with all available cash
                    shares_to_buy = current_cash / df['close'].iloc[i]
                    current_holdings += shares_to_buy
                    current_cash = 0
                
                # Check for sell signal
                elif df['position'].iloc[i] < 0 and current_holdings > 0:
                    # Sell all holdings
                    current_cash += current_holdings * df['close'].iloc[i]
                    current_holdings = 0
                
                # Update portfolio values
                df.loc[df.index[i], 'holdings'] = current_holdings
                df.loc[df.index[i], 'cash'] = current_cash
                df.loc[df.index[i], 'total'] = current_cash + (current_holdings * df['close'].iloc[i])
            
            # Calculate returns
            df['returns'] = df['total'].pct_change()
            df['cumulative_returns'] = (1 + df['returns']).cumprod()
            
            return df
            
        except Exception as e:
            print(f"❌ Error calculating portfolio performance: {e}")
            return pd.DataFrame()
    
    def calculate_performance_metrics(self, portfolio: pd.DataFrame, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate performance metrics"""
        try:
            if portfolio.empty:
                return {}
            
            # Basic metrics
            initial_value = portfolio['total'].iloc[0]
            final_value = portfolio['total'].iloc[-1]
            total_return = (final_value - initial_value) / initial_value
            
            # Calculate buy and hold return
            buy_hold_return = (data['close'].iloc[-1] - data['close'].iloc[0]) / data['close'].iloc[0]
            
            # Risk metrics
            returns = portfolio['returns'].dropna()
            if len(returns) > 0:
                volatility = returns.std() * np.sqrt(252)  # Annualized
                sharpe_ratio = (returns.mean() * 252) / volatility if volatility > 0 else 0
                
                # Maximum drawdown
                cumulative = portfolio['cumulative_returns'].fillna(1)
                running_max = cumulative.expanding().max()
                drawdown = (cumulative - running_max) / running_max
                max_drawdown = drawdown.min()
            else:
                volatility = 0
                sharpe_ratio = 0
                max_drawdown = 0
            
            # Trade statistics
            positions = portfolio['position'].dropna()
            num_trades = len(positions[positions != 0])
            
            metrics = {
                'Initial Capital': f"${initial_value:,.2f}",
                'Final Value': f"${final_value:,.2f}",
                'Total Return': f"{total_return:.2%}",
                'Buy & Hold Return': f"{buy_hold_return:.2%}",
                'Excess Return': f"{total_return - buy_hold_return:.2%}",
                'Volatility (Annual)': f"{volatility:.2%}",
                'Sharpe Ratio': f"{sharpe_ratio:.2f}",
                'Maximum Drawdown': f"{max_drawdown:.2%}",
                'Number of Trades': num_trades,
                'Win Rate': 'N/A'  # Would need individual trade analysis
            }
            
            return metrics
            
        except Exception as e:
            print(f"❌ Error calculating metrics: {e}")
            return {}
    
    def display_backtest_results(self, results: Dict):
        """Display backtest results"""
        try:
            print(f"\n📊 Backtest Results for {results['symbol']}")
            print("=" * 50)
            
            print(f"Strategy: {results['strategy'].replace('_', ' ').title()}")
            print(f"Period: {results['start_date']} to {results['end_date']}")
            print(f"Timeframe: {results['timeframe']}")
            print()
            
            print("📈 Performance Metrics:")
            print("-" * 25)
            for metric, value in results['metrics'].items():
                print(f"{metric:20}: {value}")
            
            # Ask if user wants to see chart
            show_chart = input("\nShow performance chart? (y/n) [y]: ").strip().lower()
            if show_chart != 'n':
                self.plot_backtest_results(results)
                
        except Exception as e:
            print(f"❌ Error displaying results: {e}")
    
    def plot_backtest_results(self, results: Dict):
        """Plot backtest results"""
        try:
            data = results['data']
            portfolio = results['portfolio']
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=(f"{results['symbol']} Price & Signals", "Portfolio Value"),
                row_heights=[0.7, 0.3]
            )
            
            # Add price chart
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data['close'],
                    mode='lines',
                    name='Price',
                    line=dict(color='blue')
                ),
                row=1, col=1
            )
            
            # Add buy signals
            buy_signals = portfolio[portfolio['position'] > 0]
            if not buy_signals.empty:
                fig.add_trace(
                    go.Scatter(
                        x=buy_signals.index,
                        y=buy_signals['close'],
                        mode='markers',
                        name='Buy Signal',
                        marker=dict(color='green', size=10, symbol='triangle-up')
                    ),
                    row=1, col=1
                )
            
            # Add sell signals
            sell_signals = portfolio[portfolio['position'] < 0]
            if not sell_signals.empty:
                fig.add_trace(
                    go.Scatter(
                        x=sell_signals.index,
                        y=sell_signals['close'],
                        mode='markers',
                        name='Sell Signal',
                        marker=dict(color='red', size=10, symbol='triangle-down')
                    ),
                    row=1, col=1
                )
            
            # Add portfolio value
            fig.add_trace(
                go.Scatter(
                    x=portfolio.index,
                    y=portfolio['total'],
                    mode='lines',
                    name='Portfolio Value',
                    line=dict(color='purple')
                ),
                row=2, col=1
            )
            
            # Update layout
            fig.update_layout(
                title=f"Backtest Results: {results['symbol']} - {results['strategy'].replace('_', ' ').title()}",
                height=800,
                showlegend=True
            )
            
            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="Price", row=1, col=1)
            fig.update_yaxes(title_text="Portfolio Value ($)", row=2, col=1)
            
            fig.show()
            
        except Exception as e:
            print(f"❌ Error plotting results: {e}")
    
    def save_backtest_results(self, results: Dict):
        """Save backtest results to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"backtest_{results['symbol'].replace('/', '_')}_{results['strategy']}_{timestamp}.json"
            filepath = self.results_dir / filename
            
            # Prepare results for JSON serialization
            json_results = results.copy()
            json_results.pop('data', None)  # Remove DataFrame objects
            json_results.pop('signals', None)
            json_results.pop('portfolio', None)
            
            with open(filepath, 'w') as f:
                json.dump(json_results, f, indent=2, default=str)
            
            # Add to history
            self.backtest_history.append({
                'filename': filename,
                'symbol': results['symbol'],
                'strategy': results['strategy'],
                'timestamp': results['timestamp'],
                'metrics': results['metrics']
            })
            
            print(f"✅ Results saved to: {filepath}")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def advanced_backtest_setup(self):
        """Advanced backtest setup with more options"""
        print("\n🔧 Advanced Backtest Setup")
        print("=" * 30)
        print("💡 Advanced features coming soon!")
        print("   • Custom strategy parameters")
        print("   • Multiple asset backtesting")
        print("   • Risk management rules")
        print("   • Transaction costs")
        print("   • Slippage modeling")
    
    def view_results(self):
        """View previous backtest results"""
        print("\n📊 Backtest Results")
        print("=" * 20)
        
        if not self.backtest_history:
            print("No backtest results found.")
            return
        
        print("Recent backtests:")
        for i, result in enumerate(self.backtest_history[-10:], 1):
            print(f"{i:2d}. {result['symbol']} - {result['strategy']} ({result['timestamp'][:10]})")
    
    def compare_strategies(self):
        """Compare multiple strategies"""
        print("\n📊 Strategy Comparison")
        print("=" * 25)
        print("💡 Strategy comparison coming soon!")
        print("   • Side-by-side performance metrics")
        print("   • Risk-adjusted returns")
        print("   • Correlation analysis")
    
    def show_backtest_history(self):
        """Show backtest history"""
        print("\n📋 Backtest History")
        print("=" * 20)
        
        if not self.backtest_history:
            print("No backtest history available.")
            return
        
        print(f"Total backtests run: {len(self.backtest_history)}")
        print("\nRecent backtests:")
        
        for result in self.backtest_history[-5:]:
            print(f"\n📊 {result['symbol']} - {result['strategy']}")
            print(f"   Date: {result['timestamp'][:10]}")
            if 'Total Return' in result['metrics']:
                print(f"   Return: {result['metrics']['Total Return']}")
            if 'Sharpe Ratio' in result['metrics']:
                print(f"   Sharpe: {result['metrics']['Sharpe Ratio']}")