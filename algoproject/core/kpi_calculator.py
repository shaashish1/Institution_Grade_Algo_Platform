"""
KPI Calculator
=============

Comprehensive KPI calculations for trading performance analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any
import math
from datetime import datetime, timedelta


class KPICalculator:
    """Calculates 29+ trading performance KPIs"""
    
    def __init__(self):
        self.risk_free_rate = 0.02  # 2% annual risk-free rate
    
    def calculate_all_kpis(self, trades: List[Dict], equity_curve: List[float], 
                          initial_capital: float = 100000) -> Dict[str, float]:
        """Calculate all KPIs from trades and equity curve"""
        if not trades or not equity_curve:
            return self._empty_kpis()
        
        trades_df = pd.DataFrame(trades)
        equity_series = pd.Series(equity_curve)
        
        kpis = {}
        
        # Basic metrics
        kpis.update(self._calculate_basic_metrics(trades_df, equity_series, initial_capital))
        
        # Return metrics
        kpis.update(self._calculate_return_metrics(equity_series, initial_capital))
        
        # Risk metrics
        kpis.update(self._calculate_risk_metrics(equity_series, trades_df))
        
        # Trade metrics
        kpis.update(self._calculate_trade_metrics(trades_df))
        
        # Drawdown metrics
        kpis.update(self._calculate_drawdown_metrics(equity_series))
        
        # Duration metrics
        kpis.update(self._calculate_duration_metrics(trades_df))
        
        # Advanced metrics
        kpis.update(self._calculate_advanced_metrics(equity_series, trades_df))
        
        return kpis
    
    def _calculate_basic_metrics(self, trades_df: pd.DataFrame, equity_series: pd.Series, 
                               initial_capital: float) -> Dict[str, float]:
        """Calculate basic trading metrics"""
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'initial_capital': initial_capital,
            'final_capital': equity_series.iloc[-1] if len(equity_series) > 0 else initial_capital
        }
    
    def _calculate_return_metrics(self, equity_series: pd.Series, initial_capital: float) -> Dict[str, float]:
        """Calculate return-based metrics"""
        if len(equity_series) == 0:
            return {}
        
        final_value = equity_series.iloc[-1]
        total_return = (final_value - initial_capital) / initial_capital
        
        # Calculate returns
        returns = equity_series.pct_change().dropna()
        
        # Annualized return (assuming daily data)
        days = len(equity_series)
        years = days / 252  # Trading days per year
        cagr = (final_value / initial_capital) ** (1/years) - 1 if years > 0 else 0
        
        return {
            'total_return_pct': total_return * 100,
            'final_return_pct': total_return * 100,
            'cagr_pct': cagr * 100,
            'annualized_return_pct': cagr * 100
        }
    
    def _calculate_risk_metrics(self, equity_series: pd.Series, trades_df: pd.DataFrame) -> Dict[str, float]:
        """Calculate risk-based metrics"""
        if len(equity_series) < 2:
            return {}
        
        returns = equity_series.pct_change().dropna()
        
        if len(returns) == 0:
            return {}
        
        # Volatility
        volatility = returns.std() * np.sqrt(252)  # Annualized
        
        # Sharpe Ratio
        excess_returns = returns.mean() * 252 - self.risk_free_rate
        sharpe_ratio = excess_returns / volatility if volatility > 0 else 0
        
        # Sortino Ratio (downside deviation)
        downside_returns = returns[returns < 0]
        downside_deviation = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0
        sortino_ratio = excess_returns / downside_deviation if downside_deviation > 0 else 0
        
        # Calmar Ratio (return/max drawdown)
        max_dd = self._calculate_max_drawdown(equity_series)
        calmar_ratio = (returns.mean() * 252) / abs(max_dd) if max_dd != 0 else 0
        
        return {
            'volatility_pct': volatility * 100,
            'annualized_volatility_pct': volatility * 100,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'calmar_ratio': calmar_ratio
        }
    
    def _calculate_trade_metrics(self, trades_df: pd.DataFrame) -> Dict[str, float]:
        """Calculate trade-specific metrics"""
        if len(trades_df) == 0:
            return {}
        
        pnl_series = trades_df['pnl']
        winning_trades = pnl_series[pnl_series > 0]
        losing_trades = pnl_series[pnl_series < 0]
        
        # Win rate
        win_rate = len(winning_trades) / len(trades_df) * 100
        
        # Average trade
        avg_trade = pnl_series.mean()
        avg_trade_pct = (avg_trade / trades_df['price'].mean()) * 100 if 'price' in trades_df.columns else 0
        
        # Average winning/losing trade
        avg_win = winning_trades.mean() if len(winning_trades) > 0 else 0
        avg_loss = losing_trades.mean() if len(losing_trades) > 0 else 0
        
        # Profit factor
        gross_profit = winning_trades.sum() if len(winning_trades) > 0 else 0
        gross_loss = abs(losing_trades.sum()) if len(losing_trades) > 0 else 0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf') if gross_profit > 0 else 0
        
        # Expectancy
        expectancy = (win_rate/100 * avg_win) + ((100-win_rate)/100 * avg_loss)
        expectancy_pct = expectancy / trades_df['price'].mean() * 100 if 'price' in trades_df.columns else 0
        
        # Best and worst trades
        best_trade = pnl_series.max()
        worst_trade = pnl_series.min()
        best_trade_pct = (best_trade / trades_df['price'].mean()) * 100 if 'price' in trades_df.columns else 0
        worst_trade_pct = (worst_trade / trades_df['price'].mean()) * 100 if 'price' in trades_df.columns else 0
        
        return {
            'win_rate_pct': win_rate,
            'avg_trade': avg_trade,
            'avg_trade_pct': avg_trade_pct,
            'avg_winning_trade': avg_win,
            'avg_losing_trade': avg_loss,
            'profit_factor': profit_factor,
            'expectancy': expectancy,
            'expectancy_pct': expectancy_pct,
            'best_trade': best_trade,
            'worst_trade': worst_trade,
            'best_trade_pct': best_trade_pct,
            'worst_trade_pct': worst_trade_pct,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss
        }
    
    def _calculate_drawdown_metrics(self, equity_series: pd.Series) -> Dict[str, float]:
        """Calculate drawdown metrics"""
        if len(equity_series) < 2:
            return {}
        
        # Calculate running maximum
        running_max = equity_series.expanding().max()
        drawdown = (equity_series - running_max) / running_max
        
        max_drawdown = drawdown.min()
        avg_drawdown = drawdown[drawdown < 0].mean() if len(drawdown[drawdown < 0]) > 0 else 0
        
        # Drawdown duration
        drawdown_periods = []
        in_drawdown = False
        start_idx = 0
        
        for i, dd in enumerate(drawdown):
            if dd < 0 and not in_drawdown:
                in_drawdown = True
                start_idx = i
            elif dd >= 0 and in_drawdown:
                in_drawdown = False
                drawdown_periods.append(i - start_idx)
        
        max_drawdown_duration = max(drawdown_periods) if drawdown_periods else 0
        avg_drawdown_duration = np.mean(drawdown_periods) if drawdown_periods else 0
        
        return {
            'max_drawdown_pct': max_drawdown * 100,
            'avg_drawdown_pct': avg_drawdown * 100,
            'max_drawdown_duration': max_drawdown_duration,
            'avg_drawdown_duration': avg_drawdown_duration
        }
    
    def _calculate_duration_metrics(self, trades_df: pd.DataFrame) -> Dict[str, float]:
        """Calculate trade duration metrics"""
        if 'entry_time' not in trades_df.columns or 'exit_time' not in trades_df.columns:
            return {}
        
        # Convert to datetime if needed
        entry_times = pd.to_datetime(trades_df['entry_time'])
        exit_times = pd.to_datetime(trades_df['exit_time'])
        
        durations = (exit_times - entry_times).dt.total_seconds() / 3600  # Hours
        
        return {
            'avg_trade_duration_hours': durations.mean(),
            'max_trade_duration_hours': durations.max(),
            'min_trade_duration_hours': durations.min()
        }
    
    def _calculate_advanced_metrics(self, equity_series: pd.Series, trades_df: pd.DataFrame) -> Dict[str, float]:
        """Calculate advanced performance metrics"""
        if len(equity_series) < 2:
            return {}
        
        returns = equity_series.pct_change().dropna()
        
        # Information Ratio (if benchmark available)
        # For now, using market return as 0
        information_ratio = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
        
        # Recovery Factor
        max_dd = abs(self._calculate_max_drawdown(equity_series))
        total_return = (equity_series.iloc[-1] - equity_series.iloc[0]) / equity_series.iloc[0]
        recovery_factor = total_return / max_dd if max_dd > 0 else 0
        
        # Consecutive wins/losses
        if len(trades_df) > 0:
            pnl_signs = np.sign(trades_df['pnl'])
            consecutive_wins = self._max_consecutive(pnl_signs, 1)
            consecutive_losses = self._max_consecutive(pnl_signs, -1)
        else:
            consecutive_wins = 0
            consecutive_losses = 0
        
        return {
            'information_ratio': information_ratio,
            'recovery_factor': recovery_factor,
            'max_consecutive_wins': consecutive_wins,
            'max_consecutive_losses': consecutive_losses
        }
    
    def _calculate_max_drawdown(self, equity_series: pd.Series) -> float:
        """Calculate maximum drawdown"""
        running_max = equity_series.expanding().max()
        drawdown = (equity_series - running_max) / running_max
        return drawdown.min()
    
    def _max_consecutive(self, series: pd.Series, value: int) -> int:
        """Calculate maximum consecutive occurrences of a value"""
        max_count = 0
        current_count = 0
        
        for val in series:
            if val == value:
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 0
        
        return max_count
    
    def calculate_star_rating(self, profit_factor: float, sharpe_ratio: float) -> str:
        """Calculate star rating based on performance thresholds"""
        if profit_factor >= 1.5 and sharpe_ratio >= 1.5:
            return "⭐⭐⭐⭐⭐"
        elif profit_factor >= 1.2 and sharpe_ratio >= 1.0:
            return "⭐⭐⭐⭐"
        elif profit_factor >= 1.0 and sharpe_ratio >= 0.5:
            return "⭐⭐⭐"
        elif profit_factor >= 0.8:
            return "⭐⭐"
        elif profit_factor >= 0.5:
            return "⭐"
        else:
            return "❌"
    
    def _empty_kpis(self) -> Dict[str, float]:
        """Return empty KPIs structure"""
        return {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate_pct': 0,
            'profit_factor': 0,
            'sharpe_ratio': 0,
            'total_return_pct': 0,
            'max_drawdown_pct': 0
        }