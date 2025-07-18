#!/usr/bin/env python3
"""
Enhanced Stocks Backtest Scanner
Comprehensive backtesting with detailed KPIs, profitability analysis, and portfolio simulation.
Includes professional-grade performance metrics for trading strategy evaluation.
"""

import os
import sys
import yaml
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import warnings
warnings.filterwarnings('ignore')

# Add project path to sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stocks.data_acquisition import fetch_data
from tabulate import tabulate


class AdvancedPortfolioTracker:
    """Advanced portfolio tracker with comprehensive performance metrics."""
    
    def __init__(self, initial_capital=100000):  # Default to ₹1,00,000 for stocks
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.trades = []
        self.portfolio_history = []
        self.start_date = None
        self.end_date = None
        self.market_data = {}  # Store market data for buy & hold comparison
        
    def add_trade(self, symbol, entry_time, exit_time, side, entry_price, exit_price, 
                  position_size=10000):  # Default ₹10,000 per trade for stocks
        """Add a completed trade to the portfolio."""
        pnl_abs = (exit_price - entry_price) * (position_size / entry_price)
        pnl_pct = ((exit_price - entry_price) / entry_price) * 100
        
        trade = {
            'symbol': symbol,
            'entry_time': entry_time,
            'exit_time': exit_time,
            'side': side,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'position_size': position_size,
            'pnl_abs': pnl_abs,
            'pnl_pct': pnl_pct,
            'duration_hours': self._calculate_duration(entry_time, exit_time),
            'duration_days': self._calculate_duration(entry_time, exit_time) / 24,
            'trade_type': self._classify_trade(side)
        }
        
        self.trades.append(trade)
        self.current_capital += pnl_abs
        
        # Update start/end dates
        if self.start_date is None or entry_time < self.start_date:
            self.start_date = entry_time
        if self.end_date is None or exit_time > self.end_date:
            self.end_date = exit_time
            
        return trade
    
    def add_market_data(self, symbol, data):
        """Add market data for buy & hold comparison."""
        self.market_data[symbol] = data
    
    def _calculate_duration(self, entry_time, exit_time):
        """Calculate trade duration in hours."""
        try:
            if isinstance(entry_time, str):
                entry_time = pd.to_datetime(entry_time)
            if isinstance(exit_time, str):
                exit_time = pd.to_datetime(exit_time)
            return (exit_time - entry_time).total_seconds() / 3600
        except:
            return 0
    
    def _classify_trade(self, side):
        """Classify trade type based on exit reason."""
        if 'TP' in side:
            return 'Take Profit'
        elif 'SL' in side:
            return 'Stop Loss'
        elif 'EOD' in side:
            return 'End of Data'
        else:
            return 'Regular Exit'
    
    def _calculate_buy_hold_return(self):
        """Calculate buy & hold return for comparison."""
        if not self.market_data:
            return 0
        
        total_return = 0
        symbol_count = len(self.market_data)
        
        for symbol, data in self.market_data.items():
            if data is not None and len(data) > 1:
                start_price = data['close'].iloc[0]
                end_price = data['close'].iloc[-1]
                symbol_return = ((end_price - start_price) / start_price) * 100
                total_return += symbol_return
        
        return total_return / symbol_count if symbol_count > 0 else 0
    
    def _calculate_drawdowns(self, equity_curve):
        """Calculate drawdown metrics."""
        peak = equity_curve.expanding().max()
        drawdown = (equity_curve - peak) / peak * 100
        
        # Find drawdown periods
        drawdown_periods = []
        in_drawdown = False
        start_idx = None
        
        for i, dd in enumerate(drawdown):
            if dd < 0 and not in_drawdown:
                in_drawdown = True
                start_idx = i
            elif dd >= 0 and in_drawdown:
                in_drawdown = False
                if start_idx is not None:
                    drawdown_periods.append(i - start_idx)
        
        max_drawdown = drawdown.min()
        avg_drawdown = drawdown[drawdown < 0].mean() if len(drawdown[drawdown < 0]) > 0 else 0
        max_dd_duration = max(drawdown_periods) if drawdown_periods else 0
        avg_dd_duration = np.mean(drawdown_periods) if drawdown_periods else 0
        
        return max_drawdown, avg_drawdown, max_dd_duration, avg_dd_duration
    
    def _calculate_risk_metrics(self, returns, risk_free_rate=0.06):  # Higher risk-free rate for India
        """Calculate advanced risk metrics."""
        if len(returns) < 2:
            return 0, 0, 0, 0, 0, 0, 0
        
        # Annualized metrics (Indian market: ~250 trading days)
        trading_days = 250
        ann_return = returns.mean() * trading_days
        ann_volatility = returns.std() * np.sqrt(trading_days)
        
        # CAGR
        if self.start_date and self.end_date:
            years = (self.end_date - self.start_date).days / 365.25
            cagr = ((self.current_capital / self.initial_capital) ** (1/years) - 1) * 100 if years > 0 else 0
        else:
            cagr = 0
        
        # Sharpe Ratio
        excess_returns = returns - (risk_free_rate / trading_days)
        sharpe = excess_returns.mean() / returns.std() * np.sqrt(trading_days) if returns.std() > 0 else 0
        
        # Sortino Ratio (downside deviation)
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std() if len(downside_returns) > 0 else returns.std()
        sortino = excess_returns.mean() / downside_std * np.sqrt(trading_days) if downside_std > 0 else 0
        
        # Calmar Ratio (CAGR / Max Drawdown)
        equity_curve = pd.Series([self.initial_capital + sum([t['pnl_abs'] for t in self.trades[:i+1]]) 
                                 for i in range(len(self.trades))])
        max_dd, _, _, _ = self._calculate_drawdowns(equity_curve)
        calmar = abs(cagr / max_dd) if max_dd < 0 else 0
        
        # Alpha and Beta (simplified calculation vs market average)
        buy_hold_return = self._calculate_buy_hold_return()
        alpha = ann_return - buy_hold_return
        beta = 1.0  # Simplified - would need NIFTY correlation for accurate calculation
        
        return ann_return, ann_volatility, cagr, sharpe, sortino, calmar, alpha, beta
        
    
    def get_comprehensive_analytics(self):
        """Generate comprehensive portfolio analytics with all professional metrics."""
        if not self.trades:
            return {}
        
        df = pd.DataFrame(self.trades)
        
        # Create equity curve
        df['cumulative_pnl'] = df['pnl_abs'].cumsum()
        df['portfolio_value'] = self.initial_capital + df['cumulative_pnl']
        
        # Basic trade statistics
        total_trades = len(df)
        winning_trades = len(df[df['pnl_abs'] > 0])
        losing_trades = len(df[df['pnl_abs'] < 0])
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        # PnL calculations
        total_pnl = df['pnl_abs'].sum()
        total_return_pct = ((self.current_capital - self.initial_capital) / self.initial_capital) * 100
        
        # Trade performance
        avg_win_pct = df[df['pnl_pct'] > 0]['pnl_pct'].mean() if winning_trades > 0 else 0
        avg_loss_pct = df[df['pnl_pct'] < 0]['pnl_pct'].mean() if losing_trades > 0 else 0
        best_trade_pct = df['pnl_pct'].max() if len(df) > 0 else 0
        worst_trade_pct = df['pnl_pct'].min() if len(df) > 0 else 0
        avg_trade_pct = df['pnl_pct'].mean() if len(df) > 0 else 0
        
        # Trade durations
        max_trade_duration = df['duration_days'].max() if len(df) > 0 else 0
        avg_trade_duration = df['duration_days'].mean() if len(df) > 0 else 0
        
        # Profit factor and expectancy
        gross_profit = df[df['pnl_abs'] > 0]['pnl_abs'].sum() if winning_trades > 0 else 0
        gross_loss = abs(df[df['pnl_abs'] < 0]['pnl_abs'].sum()) if losing_trades > 0 else 1
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        expectancy = (win_rate/100 * avg_win_pct) + ((100-win_rate)/100 * avg_loss_pct)
        
        # Calculate equity peaks
        equity_curve = df['portfolio_value']
        equity_peak = equity_curve.max()
        
        # Drawdown calculations
        max_drawdown, avg_drawdown, max_dd_duration, avg_dd_duration = self._calculate_drawdowns(equity_curve)
        
        # Returns for risk calculations
        daily_returns = df['pnl_pct'] / 100  # Convert percentage to decimal
        
        # Risk metrics
        ann_return, ann_volatility, cagr, sharpe, sortino, calmar, alpha, beta = self._calculate_risk_metrics(daily_returns)
        
        # Duration calculations
        if self.start_date and self.end_date:
            duration_days = (self.end_date - self.start_date).days
            
            # Exposure time calculation (time in market vs total time)
            total_trade_days = df['duration_days'].sum()
            exposure_time_pct = (total_trade_days / duration_days * 100) if duration_days > 0 else 0
        else:
            duration_days = 0
            exposure_time_pct = 0
        
        # Buy & hold comparison
        buy_hold_return = self._calculate_buy_hold_return()
        
        return {
            # Basic Information
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else 'N/A',
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else 'N/A',
            'duration_days': duration_days,
            'exposure_time_pct': exposure_time_pct,
            
            # Portfolio Performance
            'equity_final': self.current_capital,
            'equity_peak': equity_peak,
            'total_return_pct': total_return_pct,
            'buy_hold_return_pct': buy_hold_return,
            'ann_return_pct': ann_return,
            'ann_volatility_pct': ann_volatility,
            'cagr_pct': cagr,
            
            # Risk Metrics
            'sharpe_ratio': sharpe,
            'sortino_ratio': sortino,
            'calmar_ratio': calmar,
            'alpha_pct': alpha,
            'beta': beta,
            'max_drawdown_pct': max_drawdown,
            'avg_drawdown_pct': avg_drawdown,
            'max_drawdown_duration': max_dd_duration,
            'avg_drawdown_duration': avg_dd_duration,
            
            # Trade Statistics
            'total_trades': total_trades,
            'win_rate_pct': win_rate,
            'best_trade_pct': best_trade_pct,
            'worst_trade_pct': worst_trade_pct,
            'avg_trade_pct': avg_trade_pct,
            'max_trade_duration': max_trade_duration,
            'avg_trade_duration': avg_trade_duration,
            'profit_factor': profit_factor,
            'expectancy_pct': expectancy,
            
            # Legacy fields for compatibility
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'total_pnl': total_pnl,
            'avg_win': avg_win_pct,
            'avg_loss': avg_loss_pct,
            'max_win': best_trade_pct,
            'max_loss': worst_trade_pct,
            'initial_capital': self.initial_capital,
            'final_capital': self.current_capital,
            'trade_types': df['trade_type'].value_counts().to_dict(),
            'trades_df': df
        }


def load_stock_assets():
    """Load stock assets from CSV file."""
    assets_file = "stocks/input/stocks_assets.csv"
    if not os.path.exists(assets_file):
        print(f"❌ Error: {assets_file} not found!")
        return []
    
    df = pd.read_csv(assets_file)
    return df['symbol'].tolist()


def load_strategy():
    """Load the trading strategy."""
    sys.path.append('strategies')
    from strategies.VWAPSigma2Strategy import VWAPSigma2Strategy
    return VWAPSigma2Strategy()


def get_backtest_period():
    """Get the backtesting period information."""
    # Default to last 30 days of data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    return start_date, end_date


def run_stocks_backtest():
    """Run comprehensive backtest on all stock assets."""
    # Initialize
    ist = pytz.timezone('Asia/Kolkata')
    start_time = datetime.now(ist)
    start_date, end_date = get_backtest_period()
    
    print("🚀 Enhanced Stocks Backtest Scanner")
    print("=" * 100)
    
    # Load assets and strategy
    symbols = load_stock_assets()
    if not symbols:
        return
    
    strategy = load_strategy()
    portfolio = AdvancedPortfolioTracker(initial_capital=100000)  # ₹1,00,000 starting capital
    
    print(f"📊 Strategy: VWAPSigma2Strategy")
    print(f"💰 Initial Capital: ₹{portfolio.initial_capital:,.2f}")
    print(f"📅 Backtest Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"🔍 Scanning {len(symbols)} stock symbols using TradingView (NSE)")
    print(f"⏱️  Position Size: ₹10,000 per trade")
    print("=" * 100)
    
    all_results = []
    failed_symbols = []
    
    for i, symbol in enumerate(symbols, 1):
        try:
            print(f"📈 [{i:2d}/{len(symbols)}] Processing {symbol}...", end=" ")
            
            # Fetch data with proper timeframe for strategy
            data = fetch_data(
                symbol=symbol,
                exchange="NSE",
                interval="1h",  # 1-hour candles for better signal quality
                bars=720,  # ~30 days of hourly data
                data_source="tvdatafeed"
            )
            
            if data is None or len(data) < 50:
                print("❌ Insufficient data")
                failed_symbols.append(symbol)
                continue
            
            # Ensure datetime column
            if 'timestamp' in data.columns:
                data['datetime'] = pd.to_datetime(data['timestamp'])
            elif 'datetime' not in data.columns:
                data['datetime'] = pd.to_datetime(data.index)
            
            # Apply strategy backtest
            trades_df = strategy.backtest(data)
            
            if not trades_df.empty:
                trade_count = len(trades_df)
                
                # Process each trade and add to portfolio
                total_pnl = 0
                winning_trades = 0
                
                for _, trade in trades_df.iterrows():
                    portfolio_trade = portfolio.add_trade(
                        symbol=symbol,
                        entry_time=trade.get('entry_time'),
                        exit_time=trade.get('exit_time'),
                        side=trade.get('side', 'BUY'),
                        entry_price=trade.get('entry_price'),
                        exit_price=trade.get('exit_price'),
                        position_size=10000  # ₹10,000 per trade
                    )
                    
                    total_pnl += portfolio_trade['pnl_abs']
                    if portfolio_trade['pnl_abs'] > 0:
                        winning_trades += 1
                    
                    # Store result for summary
                    result = {
                        'timestamp': trade.get('entry_time'),
                        'symbol': symbol,
                        'signal': 'BUY',  # Strategy only goes long
                        'entry_price': trade.get('entry_price'),
                        'exit_price': trade.get('exit_price'),
                        'pnl_abs': portfolio_trade['pnl_abs'],
                        'pnl_pct': portfolio_trade['pnl_pct'],
                        'side': trade.get('side')
                    }
                    all_results.append(result)
                
                # Add market data for buy & hold comparison
                portfolio.add_market_data(symbol, data)
                
                win_rate = (winning_trades / trade_count) * 100
                print(f"✅ {trade_count} trades | P&L: ₹{total_pnl:.2f} | Win Rate: {win_rate:.1f}%")
            else:
                print("⚪ No trades")
                
        except Exception as e:
            print(f"❌ Error: {str(e)[:50]}...")
            failed_symbols.append(symbol)
    
    # Calculate final performance
    end_time = datetime.now(ist)
    duration = (end_time - start_time).total_seconds()
    
    print("=" * 100)
    print(f"✅ Backtest completed in {duration:.1f}s")
    
    if failed_symbols:
        print(f"⚠️  Failed symbols ({len(failed_symbols)}): {', '.join(failed_symbols[:5])}")
        if len(failed_symbols) > 5:
            print(f"   ... and {len(failed_symbols) - 5} more")
    
    # Save and display comprehensive results
    analytics = portfolio.get_comprehensive_analytics()
    save_enhanced_results(all_results, analytics)
    display_comprehensive_summary(analytics)


def save_enhanced_results(results, analytics):
    """Save enhanced results to CSV files."""
    os.makedirs("stocks/output", exist_ok=True)
    
    # Save individual trade results
    if results:
        df_results = pd.DataFrame(results)
        results_file = "stocks/output/stocks_backtest_detailed.csv"
        df_results.to_csv(results_file, index=False)
        print(f"💾 Detailed results saved to {results_file}")
    
    # Save portfolio analytics
    if analytics and 'trades_df' in analytics:
        trades_file = "stocks/output/stocks_backtest_trades.csv"
        analytics['trades_df'].to_csv(trades_file, index=False)
        print(f"💾 Trade history saved to {trades_file}")
    
    # Save comprehensive summary analytics
    if analytics:
        summary_file = "stocks/output/stocks_backtest_summary.csv"
        summary_data = {
            'Metric': [
                'Start Date', 'End Date', 'Duration (Days)', 'Exposure Time (%)',
                'Equity Final (₹)', 'Equity Peak (₹)', 'Return (%)', 'Buy & Hold Return (%)',
                'Return (Ann.) (%)', 'Volatility (Ann.) (%)', 'CAGR (%)', 'Sharpe Ratio',
                'Sortino Ratio', 'Calmar Ratio', 'Alpha (%)', 'Beta', 'Max. Drawdown (%)',
                'Avg. Drawdown (%)', 'Max. Drawdown Duration', 'Avg. Drawdown Duration',
                '# Trades', 'Win Rate (%)', 'Best Trade (%)', 'Worst Trade (%)',
                'Avg. Trade (%)', 'Max. Trade Duration', 'Avg. Trade Duration',
                'Profit Factor', 'Expectancy (%)'
            ],
            'Value': [
                analytics.get('start_date', 'N/A'),
                analytics.get('end_date', 'N/A'),
                analytics.get('duration_days', 0),
                round(analytics.get('exposure_time_pct', 0), 2),
                round(analytics.get('equity_final', 0), 2),
                round(analytics.get('equity_peak', 0), 2),
                round(analytics.get('total_return_pct', 0), 2),
                round(analytics.get('buy_hold_return_pct', 0), 2),
                round(analytics.get('ann_return_pct', 0), 2),
                round(analytics.get('ann_volatility_pct', 0), 2),
                round(analytics.get('cagr_pct', 0), 2),
                round(analytics.get('sharpe_ratio', 0), 3),
                round(analytics.get('sortino_ratio', 0), 3),
                round(analytics.get('calmar_ratio', 0), 3),
                round(analytics.get('alpha_pct', 0), 2),
                round(analytics.get('beta', 0), 3),
                round(analytics.get('max_drawdown_pct', 0), 2),
                round(analytics.get('avg_drawdown_pct', 0), 2),
                round(analytics.get('max_drawdown_duration', 0), 1),
                round(analytics.get('avg_drawdown_duration', 0), 1),
                analytics.get('total_trades', 0),
                round(analytics.get('win_rate_pct', 0), 2),
                round(analytics.get('best_trade_pct', 0), 2),
                round(analytics.get('worst_trade_pct', 0), 2),
                round(analytics.get('avg_trade_pct', 0), 2),
                round(analytics.get('max_trade_duration', 0), 2),
                round(analytics.get('avg_trade_duration', 0), 2),
                round(analytics.get('profit_factor', 0), 2),
                round(analytics.get('expectancy_pct', 0), 2)
            ]
        }
        pd.DataFrame(summary_data).to_csv(summary_file, index=False)
        print(f"💾 Comprehensive summary saved to {summary_file}")


def display_comprehensive_summary(analytics):
    """Display comprehensive backtest summary with all professional trading metrics."""
    if not analytics or analytics.get('total_trades', 0) == 0:
        print("\n⚠️  No trades executed in backtest period.")
        print("\n💡 **Possible Reasons:**")
        print("   • Strategy conditions too strict for current market")
        print("   • Insufficient data history")
        print("   • Market conditions don't match strategy requirements")
        print("\n🔧 **Suggestions:**")
        print("   • Try different time periods")
        print("   • Adjust strategy parameters")
        print("   • Check symbol data quality")
        return

    print(f"\n📊 **COMPREHENSIVE BACKTEST PERFORMANCE REPORT**")
    print("=" * 90)
    
    # Period & Duration Information
    print(f"\n📅 **BACKTEST PERIOD & DURATION**")
    print("-" * 50)
    period_data = [
        ["Start Date", analytics.get('start_date', 'N/A')],
        ["End Date", analytics.get('end_date', 'N/A')],
        ["Duration (Days)", f"{analytics.get('duration_days', 0):,.0f}"],
        ["Exposure Time", f"{analytics.get('exposure_time_pct', 0):.2f}%"]
    ]
    print(tabulate(period_data, headers=['Metric', 'Value'], tablefmt='grid'))
    
    # Portfolio Performance
    print(f"\n💰 **PORTFOLIO PERFORMANCE**")
    print("-" * 50)
    performance_data = [
        ["Equity Final", f"₹{analytics.get('equity_final', 0):,.2f}"],
        ["Equity Peak", f"₹{analytics.get('equity_peak', 0):,.2f}"],
        ["Return", f"{analytics.get('total_return_pct', 0):+.2f}%"],
        ["Buy & Hold Return", f"{analytics.get('buy_hold_return_pct', 0):+.2f}%"],
        ["Return (Annualized)", f"{analytics.get('ann_return_pct', 0):+.2f}%"],
        ["Volatility (Annualized)", f"{analytics.get('ann_volatility_pct', 0):.2f}%"],
        ["CAGR", f"{analytics.get('cagr_pct', 0):+.2f}%"]
    ]
    print(tabulate(performance_data, headers=['Metric', 'Value'], tablefmt='grid'))
    
    # Risk & Reward Ratios
    print(f"\n⚖️  **RISK & REWARD RATIOS**")
    print("-" * 50)
    ratio_data = [
        ["Sharpe Ratio", f"{analytics.get('sharpe_ratio', 0):.3f}"],
        ["Sortino Ratio", f"{analytics.get('sortino_ratio', 0):.3f}"],
        ["Calmar Ratio", f"{analytics.get('calmar_ratio', 0):.3f}"],
        ["Alpha", f"{analytics.get('alpha_pct', 0):+.2f}%"],
        ["Beta", f"{analytics.get('beta', 0):.3f}"]
    ]
    print(tabulate(ratio_data, headers=['Metric', 'Value'], tablefmt='grid'))
    
    # Drawdown Analysis
    print(f"\n📉 **DRAWDOWN ANALYSIS**")
    print("-" * 50)
    dd_data = [
        ["Max. Drawdown", f"{analytics.get('max_drawdown_pct', 0):.2f}%"],
        ["Avg. Drawdown", f"{analytics.get('avg_drawdown_pct', 0):.2f}%"],
        ["Max. Drawdown Duration", f"{analytics.get('max_drawdown_duration', 0):.1f} periods"],
        ["Avg. Drawdown Duration", f"{analytics.get('avg_drawdown_duration', 0):.1f} periods"]
    ]
    print(tabulate(dd_data, headers=['Metric', 'Value'], tablefmt='grid'))
    
    # Trade Statistics
    print(f"\n📈 **TRADE STATISTICS**")
    print("-" * 50)
    trade_data = [
        ["# Trades", f"{analytics.get('total_trades', 0):,}"],
        ["Win Rate", f"{analytics.get('win_rate_pct', 0):.2f}%"],
        ["Best Trade", f"{analytics.get('best_trade_pct', 0):+.2f}%"],
        ["Worst Trade", f"{analytics.get('worst_trade_pct', 0):+.2f}%"],
        ["Avg. Trade", f"{analytics.get('avg_trade_pct', 0):+.2f}%"],
        ["Max. Trade Duration", f"{analytics.get('max_trade_duration', 0):.2f} days"],
        ["Avg. Trade Duration", f"{analytics.get('avg_trade_duration', 0):.2f} days"],
        ["Profit Factor", f"{analytics.get('profit_factor', 0):.2f}"],
        ["Expectancy", f"{analytics.get('expectancy_pct', 0):+.2f}%"]
    ]
    print(tabulate(trade_data, headers=['Metric', 'Value'], tablefmt='grid'))
    
    # Strategy Assessment & Recommendation
    print(f"\n🎯 **STRATEGY ASSESSMENT & RECOMMENDATION**")
    print("-" * 60)
    
    # Scoring criteria
    is_profitable = analytics.get('total_return_pct', 0) > 0
    good_sharpe = analytics.get('sharpe_ratio', 0) >= 1.0
    good_win_rate = analytics.get('win_rate_pct', 0) >= 45
    good_profit_factor = analytics.get('profit_factor', 0) >= 1.5
    acceptable_drawdown = analytics.get('max_drawdown_pct', 0) >= -20
    positive_expectancy = analytics.get('expectancy_pct', 0) > 0
    
    assessment_score = sum([
        is_profitable, good_sharpe, good_win_rate, 
        good_profit_factor, acceptable_drawdown, positive_expectancy
    ])
    
    # Recommendation logic
    if assessment_score >= 5:
        recommendation = "✅ HIGHLY RECOMMENDED for live trading"
        risk_level = "🟢 LOW RISK"
        next_step = "Ready for live deployment with proper risk management"
    elif assessment_score >= 4:
        recommendation = "✅ RECOMMENDED for live trading"
        risk_level = "🟡 MODERATE RISK"
        next_step = "Consider paper trading first, then start with small position sizes"
    elif assessment_score >= 3:
        recommendation = "⚠️  CAUTION - Strategy shows promise but needs optimization"
        risk_level = "🟡 MODERATE RISK"
        next_step = "Optimize parameters and test on different market conditions"
    elif assessment_score >= 2:
        recommendation = "⚠️  NOT RECOMMENDED - Significant improvements needed"
        risk_level = "🔴 HIGH RISK"
        next_step = "Major strategy revision required before live trading"
    else:
        recommendation = "❌ STRONGLY NOT RECOMMENDED - High risk of losses"
        risk_level = "🔴 VERY HIGH RISK"
        next_step = "Complete strategy overhaul needed"
    
    assessment_data = [
        ["Profitability", "✅ Positive" if is_profitable else "❌ Negative"],
        ["Sharpe Ratio", "✅ Good (≥1.0)" if good_sharpe else f"⚠️  Poor ({analytics.get('sharpe_ratio', 0):.2f})"],
        ["Win Rate", "✅ Good (≥45%)" if good_win_rate else f"⚠️  Low ({analytics.get('win_rate_pct', 0):.1f}%)"],
        ["Profit Factor", "✅ Good (≥1.5)" if good_profit_factor else f"⚠️  Poor ({analytics.get('profit_factor', 0):.2f})"],
        ["Max Drawdown", "✅ Acceptable (≤20%)" if acceptable_drawdown else f"❌ High ({abs(analytics.get('max_drawdown_pct', 0)):.1f}%)"],
        ["Expectancy", "✅ Positive" if positive_expectancy else "❌ Negative"],
        ["Overall Score", f"⭐ {assessment_score}/6 stars"],
        ["Risk Level", risk_level],
        ["Recommendation", recommendation]
    ]
    print(tabulate(assessment_data, headers=['Criteria', 'Status'], tablefmt='grid'))
    
    # Detailed recommendations
    print(f"\n💡 **NEXT STEPS & RECOMMENDATIONS**")
    print("-" * 60)
    print(f"📋 Primary Action: {next_step}")
    print()
    
    if is_profitable and assessment_score >= 4:
        print("✅ **LIVE TRADING CHECKLIST:**")
        print("   • Start with 1-2% risk per trade")
        print("   • Implement strict stop-loss discipline")
        print("   • Monitor performance daily for first month")
        print("   • Keep detailed trading journal")
        print("   • Set maximum daily/monthly loss limits")
    elif assessment_score >= 2:
        print("🔧 **OPTIMIZATION SUGGESTIONS:**")
        print("   • Analyze losing trades for patterns")
        print("   • Consider adjusting entry/exit criteria")
        print("   • Test on different time periods")
        print("   • Evaluate market regime dependency")
        print("   • Consider position sizing optimization")
    else:
        print("⚠️  **STRATEGY REVISION NEEDED:**")
        print("   • Fundamental strategy logic may be flawed")
        print("   • Consider completely different approach")
        print("   • Extensive backtesting on various markets")
        print("   • Professional strategy development recommended")
    
    print(f"\n📊 **PERFORMANCE HIGHLIGHTS:**")
    print(f"   • Total Return: {analytics.get('total_return_pct', 0):+.2f}% vs Buy & Hold: {analytics.get('buy_hold_return_pct', 0):+.2f}%")
    print(f"   • Risk-Adjusted Return (Sharpe): {analytics.get('sharpe_ratio', 0):.2f}")
    print(f"   • Win Rate: {analytics.get('win_rate_pct', 0):.1f}% with {analytics.get('total_trades', 0)} trades")
    print(f"   • Maximum Loss Period: {abs(analytics.get('max_drawdown_pct', 0)):.1f}%")


if __name__ == "__main__":
    try:
        run_stocks_backtest()
    except KeyboardInterrupt:
        print("\n⚠️  Backtest interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        print(traceback.format_exc())
