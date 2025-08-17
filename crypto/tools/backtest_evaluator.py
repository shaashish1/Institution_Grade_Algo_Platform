"""
AlgoProject - Advanced Backtest Evaluator
Comprehensive performance analysis with detailed KPIs and trade logging
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
from typing import Dict, List, Tuple, Optional
import csv
import os
from pathlib import Path

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    print("⚠️  Colorama not available. Install with: pip install colorama")

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Rich not available. Install with: pip install rich")

from tabulate import tabulate


class BacktestEvaluator:
    """
    Comprehensive backtest evaluation with detailed KPIs and trade analysis
    """
    
    def __init__(self, strategy_name: str, symbol: str, initial_capital: float = 100000):
        self.strategy_name = strategy_name
        self.symbol = symbol
        self.initial_capital = initial_capital
        self.trades = []
        self.equity_curve = []
        self.drawdown_curve = []
        self.start_date = None
        self.end_date = None
        
        # Ensure output directory exists
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def add_trade(self, trade_data: Dict):
        """
        Add a trade to the evaluation
        
        Expected trade_data format:
        {
            'entry_time': datetime,
            'exit_time': datetime,
            'entry_price': float,
            'exit_price': float,
            'position_size': float,
            'trade_type': 'Long' or 'Short',
            'pnl_dollars': float,
            'pnl_percent': float
        }
        """
        trade_id = len(self.trades) + 1
        
        # Calculate trade duration
        duration = trade_data['exit_time'] - trade_data['entry_time']
        duration_days = duration.total_seconds() / (24 * 3600)
        
        # Determine trade outcome
        outcome = "Win" if trade_data['pnl_dollars'] > 0 else "Loss" if trade_data['pnl_dollars'] < 0 else "Breakeven"
        
        trade_record = {
            'trade_id': trade_id,
            'symbol': self.symbol,
            'entry_time': trade_data['entry_time'],
            'exit_time': trade_data['exit_time'],
            'entry_price': trade_data['entry_price'],
            'exit_price': trade_data['exit_price'],
            'position_size': trade_data['position_size'],
            'pnl_dollars': trade_data['pnl_dollars'],
            'pnl_percent': trade_data['pnl_percent'],
            'duration_days': duration_days,
            'trade_type': trade_data['trade_type'],
            'outcome': outcome,
            'strategy_name': self.strategy_name
        }
        
        self.trades.append(trade_record)
        
    def add_equity_point(self, timestamp: datetime, equity_value: float):
        """Add equity curve point"""
        self.equity_curve.append({
            'timestamp': timestamp,
            'equity': equity_value,
            'drawdown': self._calculate_drawdown(equity_value)
        })
        
    def _calculate_drawdown(self, current_equity: float) -> float:
        """Calculate current drawdown percentage"""
        if not self.equity_curve:
            return 0.0
            
        peak_equity = max([point['equity'] for point in self.equity_curve] + [current_equity])
        drawdown = (peak_equity - current_equity) / peak_equity * 100
        return drawdown
        
    def calculate_comprehensive_kpis(self) -> Dict:
        """Calculate all performance KPIs"""
        if not self.trades or not self.equity_curve:
            return {}
            
        # Basic info
        df_trades = pd.DataFrame(self.trades)
        df_equity = pd.DataFrame(self.equity_curve)
        
        self.start_date = df_trades['entry_time'].min()
        self.end_date = df_trades['exit_time'].max()
        duration = (self.end_date - self.start_date).days
        
        # Equity metrics
        equity_final = df_equity['equity'].iloc[-1]
        equity_peak = df_equity['equity'].max()
        
        # Returns
        total_return = (equity_final - self.initial_capital) / self.initial_capital * 100
        
        # Buy & Hold Return (simplified - using first and last prices)
        first_price = df_trades['entry_price'].iloc[0]
        last_price = df_trades['exit_price'].iloc[-1]
        buy_hold_return = (last_price - first_price) / first_price * 100
        
        # Annualized metrics
        years = duration / 365.25
        if years > 0:
            cagr = ((equity_final / self.initial_capital) ** (1/years) - 1) * 100
            annualized_return = cagr
        else:
            cagr = 0
            annualized_return = 0
            
        # Volatility (annualized)
        if len(df_equity) > 1:
            daily_returns = df_equity['equity'].pct_change().dropna()
            daily_volatility = daily_returns.std()
            annualized_volatility = daily_volatility * np.sqrt(252) * 100
        else:
            annualized_volatility = 0
            
        # Risk-adjusted ratios
        risk_free_rate = 2.0  # Assume 2% risk-free rate
        if annualized_volatility > 0:
            sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
        else:
            sharpe_ratio = 0
            
        # Sortino Ratio (downside deviation)
        if len(df_equity) > 1:
            negative_returns = daily_returns[daily_returns < 0]
            if len(negative_returns) > 0:
                downside_deviation = negative_returns.std() * np.sqrt(252) * 100
                sortino_ratio = (annualized_return - risk_free_rate) / downside_deviation if downside_deviation > 0 else 0
            else:
                sortino_ratio = float('inf')
        else:
            sortino_ratio = 0
            
        # Drawdown metrics
        max_drawdown = df_equity['drawdown'].max()
        avg_drawdown = df_equity['drawdown'].mean()
        
        # Calmar Ratio
        calmar_ratio = annualized_return / max_drawdown if max_drawdown > 0 else 0
        
        # Trade statistics
        total_trades = len(df_trades)
        winning_trades = len(df_trades[df_trades['outcome'] == 'Win'])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # P&L statistics
        best_trade = df_trades['pnl_percent'].max()
        worst_trade = df_trades['pnl_percent'].min()
        avg_trade = df_trades['pnl_percent'].mean()
        
        # Trade duration
        max_trade_duration = df_trades['duration_days'].max()
        avg_trade_duration = df_trades['duration_days'].mean()
        
        # Profit Factor
        gross_profit = df_trades[df_trades['pnl_dollars'] > 0]['pnl_dollars'].sum()
        gross_loss = abs(df_trades[df_trades['pnl_dollars'] < 0]['pnl_dollars'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Expectancy
        expectancy = avg_trade
        
        # Alpha and Beta (simplified - would need benchmark data for accurate calculation)
        alpha = annualized_return - risk_free_rate  # Simplified alpha
        beta = 1.0  # Simplified beta
        
        # Exposure time (simplified - assume always in market during trades)
        exposure_time = 100.0  # Placeholder
        
        # Drawdown duration (simplified)
        max_drawdown_duration = duration  # Placeholder
        avg_drawdown_duration = duration / 2  # Placeholder
        
        kpis = {
            'strategy_name': self.strategy_name,
            'symbol': self.symbol,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'duration_days': duration,
            'exposure_time_pct': exposure_time,
            'equity_final': equity_final,
            'equity_peak': equity_peak,
            'total_return_pct': total_return,
            'buy_hold_return_pct': buy_hold_return,
            'cagr_pct': cagr,
            'annualized_return_pct': annualized_return,
            'annualized_volatility_pct': annualized_volatility,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'calmar_ratio': calmar_ratio,
            'alpha_pct': alpha,
            'beta': beta,
            'max_drawdown_pct': max_drawdown,
            'avg_drawdown_pct': avg_drawdown,
            'max_drawdown_duration': max_drawdown_duration,
            'avg_drawdown_duration': avg_drawdown_duration,
            'total_trades': total_trades,
            'win_rate_pct': win_rate,
            'best_trade_pct': best_trade,
            'worst_trade_pct': worst_trade,
            'avg_trade_pct': avg_trade,
            'max_trade_duration': max_trade_duration,
            'avg_trade_duration': avg_trade_duration,
            'profit_factor': profit_factor,
            'expectancy_pct': expectancy
        }
        
        return kpis
        
    def display_trade_logs(self):
        """Display trade logs in terminal with colors"""
        if not self.trades:
            print("No trades to display")
            return
            
        print(f"\n{'='*80}")
        print(f"📊 DETAILED TRADE LOG - {self.strategy_name} | {self.symbol}")
        print(f"{'='*80}")
        
        # Prepare table data
        table_data = []
        for trade in self.trades:
            # Color coding for P&L
            pnl_color = ""
            if COLORAMA_AVAILABLE:
                if trade['pnl_dollars'] > 0:
                    pnl_color = Fore.GREEN
                elif trade['pnl_dollars'] < 0:
                    pnl_color = Fore.RED
                else:
                    pnl_color = Fore.YELLOW
                    
            table_data.append([
                trade['trade_id'],
                trade['symbol'],
                trade['entry_time'].strftime('%Y-%m-%d %H:%M'),
                trade['exit_time'].strftime('%Y-%m-%d %H:%M'),
                f"${trade['entry_price']:.4f}",
                f"${trade['exit_price']:.4f}",
                f"${trade['position_size']:.2f}",
                f"{pnl_color}${trade['pnl_dollars']:.2f}{Style.RESET_ALL if COLORAMA_AVAILABLE else ''}",
                f"{pnl_color}{trade['pnl_percent']:.2f}%{Style.RESET_ALL if COLORAMA_AVAILABLE else ''}",
                f"{trade['duration_days']:.1f}d",
                trade['trade_type'],
                trade['outcome']
            ])
            
        headers = [
            'ID', 'Symbol', 'Entry Time', 'Exit Time', 'Entry Price', 'Exit Price',
            'Position Size', 'P&L ($)', 'P&L (%)', 'Duration', 'Type', 'Outcome'
        ]
        
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        
    def display_kpi_summary(self, kpis: Dict):
        """Display KPI summary with colors"""
        if not kpis:
            print("No KPIs to display")
            return
            
        print(f"\n{'='*80}")
        print(f"📈 COMPREHENSIVE BACKTEST ANALYSIS - {self.strategy_name}")
        print(f"{'='*80}")
        
        # Basic Info
        print(f"\n📅 PERIOD ANALYSIS:")
        print(f"Start Date: {kpis['start_date'].strftime('%Y-%m-%d')}")
        print(f"End Date: {kpis['end_date'].strftime('%Y-%m-%d')}")
        print(f"Duration: {kpis['duration_days']} days")
        print(f"Exposure Time: {kpis['exposure_time_pct']:.1f}%")
        
        # Equity & Returns
        print(f"\n💰 EQUITY & RETURNS:")
        self._print_colored_metric("Equity Final", f"${kpis['equity_final']:,.2f}", kpis['equity_final'] > self.initial_capital)
        self._print_colored_metric("Equity Peak", f"${kpis['equity_peak']:,.2f}", True)
        self._print_colored_metric("Total Return", f"{kpis['total_return_pct']:.2f}%", kpis['total_return_pct'] > 0)
        self._print_colored_metric("Buy & Hold Return", f"{kpis['buy_hold_return_pct']:.2f}%", kpis['buy_hold_return_pct'] > 0)
        self._print_colored_metric("CAGR", f"{kpis['cagr_pct']:.2f}%", kpis['cagr_pct'] > 0)
        
        # Risk Metrics
        print(f"\n⚠️ RISK ANALYSIS:")
        self._print_colored_metric("Annualized Volatility", f"{kpis['annualized_volatility_pct']:.2f}%", kpis['annualized_volatility_pct'] < 20)
        self._print_colored_metric("Sharpe Ratio", f"{kpis['sharpe_ratio']:.2f}", kpis['sharpe_ratio'] > 1.0)
        self._print_colored_metric("Sortino Ratio", f"{kpis['sortino_ratio']:.2f}", kpis['sortino_ratio'] > 1.0)
        self._print_colored_metric("Calmar Ratio", f"{kpis['calmar_ratio']:.2f}", kpis['calmar_ratio'] > 1.0)
        
        # Drawdown
        print(f"\n📉 DRAWDOWN ANALYSIS:")
        self._print_colored_metric("Max Drawdown", f"{kpis['max_drawdown_pct']:.2f}%", kpis['max_drawdown_pct'] < 10, reverse=True)
        self._print_colored_metric("Avg Drawdown", f"{kpis['avg_drawdown_pct']:.2f}%", kpis['avg_drawdown_pct'] < 5, reverse=True)
        
        # Trade Statistics
        print(f"\n📊 TRADE STATISTICS:")
        print(f"Total Trades: {kpis['total_trades']}")
        self._print_colored_metric("Win Rate", f"{kpis['win_rate_pct']:.1f}%", kpis['win_rate_pct'] > 50)
        self._print_colored_metric("Best Trade", f"{kpis['best_trade_pct']:.2f}%", kpis['best_trade_pct'] > 0)
        self._print_colored_metric("Worst Trade", f"{kpis['worst_trade_pct']:.2f}%", kpis['worst_trade_pct'] > -5, reverse=True)
        self._print_colored_metric("Avg Trade", f"{kpis['avg_trade_pct']:.2f}%", kpis['avg_trade_pct'] > 0)
        self._print_colored_metric("Profit Factor", f"{kpis['profit_factor']:.2f}", kpis['profit_factor'] > 1.5)
        self._print_colored_metric("Expectancy", f"{kpis['expectancy_pct']:.2f}%", kpis['expectancy_pct'] > 0)
        
        # Strategy Assessment
        self._display_strategy_assessment(kpis)
        
    def _print_colored_metric(self, label: str, value: str, condition: bool, reverse: bool = False):
        """Print metric with color coding"""
        if not COLORAMA_AVAILABLE:
            print(f"{label}: {value}")
            return
            
        if reverse:
            condition = not condition
            
        if condition:
            color = Fore.GREEN
            symbol = "✅"
        else:
            color = Fore.RED
            symbol = "❌"
            
        print(f"{symbol} {label}: {color}{value}{Style.RESET_ALL}")
        
    def _display_strategy_assessment(self, kpis: Dict):
        """Display strategy assessment with star rating"""
        print(f"\n🏆 STRATEGY ASSESSMENT:")
        
        # Calculate score
        score = 0
        max_score = 8
        
        # Scoring criteria
        if kpis['total_return_pct'] > 0: score += 1
        if kpis['sharpe_ratio'] > 1.0: score += 1
        if kpis['win_rate_pct'] > 50: score += 1
        if kpis['max_drawdown_pct'] < 10: score += 1
        if kpis['profit_factor'] > 1.5: score += 1
        if kpis['expectancy_pct'] > 0: score += 1
        if kpis['calmar_ratio'] > 1.0: score += 1
        if kpis['cagr_pct'] > 10: score += 1
        
        # Star rating
        star_rating = min(5, max(1, int(score / max_score * 5)))
        stars = "⭐" * star_rating
        
        # Recommendation
        if score >= 7:
            recommendation = "🚀 STRONG BUY - Excellent Strategy"
            color = Fore.GREEN if COLORAMA_AVAILABLE else ""
        elif score >= 5:
            recommendation = "👍 BUY - Good Strategy"
            color = Fore.GREEN if COLORAMA_AVAILABLE else ""
        elif score >= 3:
            recommendation = "⚠️ HOLD - Average Strategy"
            color = Fore.YELLOW if COLORAMA_AVAILABLE else ""
        else:
            recommendation = "❌ AVOID - Poor Strategy"
            color = Fore.RED if COLORAMA_AVAILABLE else ""
            
        print(f"\n{stars} RATING: {star_rating}/5 stars")
        print(f"{color}{recommendation}{Style.RESET_ALL if COLORAMA_AVAILABLE else ''}")
        
        # Detailed assessment
        print(f"\n📋 DETAILED ASSESSMENT:")
        profitability = "✅ Profitable" if kpis['total_return_pct'] > 0 else "❌ Unprofitable"
        risk_level = "✅ Low Risk" if kpis['max_drawdown_pct'] < 10 else "⚠️ High Risk"
        consistency = "✅ Consistent" if kpis['win_rate_pct'] > 50 else "❌ Inconsistent"
        
        print(f"• Profitability: {profitability}")
        print(f"• Risk Level: {risk_level}")
        print(f"• Consistency: {consistency}")
        print(f"• Sharpe Ratio: {'✅ Good' if kpis['sharpe_ratio'] > 1.0 else '❌ Poor'}")
        
    def save_trade_logs(self):
        """Save detailed trade logs to CSV"""
        if not self.trades:
            return
            
        # Clean symbol name for filename
        clean_symbol = self.symbol.replace('/', '_').replace('\\', '_')
        filename = self.output_dir / f"crypto_backtest_trades_detailed_{clean_symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df = pd.DataFrame(self.trades)
        df.to_csv(filename, index=False)
        
        print(f"\n💾 Trade logs saved to: {filename}")
        
    def save_kpi_summary(self, kpis: Dict):
        """Save KPI summary to CSV"""
        if not kpis:
            return
            
        filename = self.output_dir / "crypto_backtest_summary.csv"
        
        # Add timestamp
        kpis['analysis_timestamp'] = datetime.now()
        
        # Convert to DataFrame
        df = pd.DataFrame([kpis])
        
        # Append to existing file or create new
        if filename.exists():
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, index=False)
            
        print(f"📊 KPI summary saved to: {filename}")
        
    def run_full_analysis(self):
        """Run complete analysis and generate all outputs"""
        print(f"\n🔍 Starting comprehensive analysis for {self.strategy_name} on {self.symbol}...")
        
        # Calculate KPIs
        kpis = self.calculate_comprehensive_kpis()
        
        if not kpis:
            print("❌ No data available for analysis")
            return
            
        # Display results
        self.display_trade_logs()
        self.display_kpi_summary(kpis)
        
        # Save results
        self.save_trade_logs()
        self.save_kpi_summary(kpis)
        
        print(f"\n✅ Analysis complete! Check the output/ directory for detailed reports.")
        
        return kpis


def demo_backtest_evaluator():
    """Demo function showing how to use the BacktestEvaluator"""
    
    # Create evaluator
    evaluator = BacktestEvaluator("RSI_MACD_Strategy", "BTC/USDT", 100000)
    
    # Add sample trades
    base_time = datetime.now() - timedelta(days=30)
    
    sample_trades = [
        {
            'entry_time': base_time + timedelta(days=1),
            'exit_time': base_time + timedelta(days=2),
            'entry_price': 45000,
            'exit_price': 46500,
            'position_size': 50000,
            'trade_type': 'Long',
            'pnl_dollars': 1666.67,
            'pnl_percent': 3.33
        },
        {
            'entry_time': base_time + timedelta(days=5),
            'exit_time': base_time + timedelta(days=7),
            'entry_price': 47000,
            'exit_price': 46000,
            'position_size': 50000,
            'trade_type': 'Long',
            'pnl_dollars': -1063.83,
            'pnl_percent': -2.13
        },
        {
            'entry_time': base_time + timedelta(days=10),
            'exit_time': base_time + timedelta(days=12),
            'entry_price': 46500,
            'exit_price': 48000,
            'position_size': 50000,
            'trade_type': 'Long',
            'pnl_dollars': 1612.90,
            'pnl_percent': 3.23
        }
    ]
    
    # Add trades to evaluator
    for trade in sample_trades:
        evaluator.add_trade(trade)
        
    # Add equity curve points
    equity_values = [100000, 101667, 100603, 102216]
    for i, equity in enumerate(equity_values):
        evaluator.add_equity_point(base_time + timedelta(days=i*3), equity)
        
    # Run full analysis
    evaluator.run_full_analysis()


if __name__ == "__main__":
    demo_backtest_evaluator()
