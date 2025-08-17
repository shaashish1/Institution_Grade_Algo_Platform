"""
Performance Analyzer
===================

Advanced performance analysis for backtest results.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import math

from ...core.interfaces import MarketData


class PerformanceAnalyzer:
    """Advanced performance analysis for trading strategies"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def calculate_comprehensive_metrics(self, equity_curve: pd.DataFrame, 
                                      trade_log: pd.DataFrame,
                                      benchmark_returns: Optional[pd.Series] = None,
                                      risk_free_rate: float = 0.02) -> Dict[str, Any]:
        """Calculate comprehensive performance metrics
        
        Args:
            equity_curve: DataFrame with portfolio values over time
            trade_log: DataFrame with trade details
            benchmark_returns: Optional benchmark returns for comparison
            risk_free_rate: Risk-free rate for Sharpe ratio calculation
            
        Returns:
            Dictionary with comprehensive metrics
        """
        if equity_curve.empty:
            return {}
        
        try:
            metrics = {}
            
            # Basic return metrics
            metrics.update(self._calculate_return_metrics(equity_curve))
            
            # Risk metrics
            metrics.update(self._calculate_risk_metrics(equity_curve, risk_free_rate))
            
            # Drawdown metrics
            metrics.update(self._calculate_drawdown_metrics(equity_curve))
            
            # Trade metrics
            if not trade_log.empty:
                metrics.update(self._calculate_trade_metrics(trade_log))
            
            # Benchmark comparison
            if benchmark_returns is not None:
                metrics.update(self._calculate_benchmark_metrics(equity_curve, benchmark_returns))
            
            # Advanced metrics
            metrics.update(self._calculate_advanced_metrics(equity_curve))
            
            # Star rating
            metrics['star_rating'] = self._calculate_star_rating(metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating metrics: {e}")
            return {}
    
    def _calculate_return_metrics(self, equity_curve: pd.DataFrame) -> Dict[str, float]:
        """Calculate return-based metrics"""
        if 'portfolio_value' not in equity_curve.columns:
            return {}
        
        values = equity_curve['portfolio_value']
        returns = values.pct_change().dropna()
        
        initial_value = values.iloc[0]
        final_value = values.iloc[-1]
        
        # Time period calculations
        start_date = equity_curve.index[0]
        end_date = equity_curve.index[-1]
        total_days = (end_date - start_date).days
        years = total_days / 365.25
        
        # Basic returns
        total_return = (final_value - initial_value) / initial_value
        total_return_pct = total_return * 100
        
        # Annualized returns
        if years > 0:
            cagr = (final_value / initial_value) ** (1 / years) - 1
            cagr_pct = cagr * 100
        else:
            cagr = cagr_pct = 0
        
        # Average returns
        avg_daily_return = returns.mean()
        avg_monthly_return = avg_daily_return * 21  # Approximate trading days per month
        avg_annual_return = avg_daily_return * 252  # Trading days per year
        
        return {
            'total_return': total_return,
            'total_return_pct': total_return_pct,
            'cagr': cagr,
            'cagr_pct': cagr_pct,
            'avg_daily_return': avg_daily_return,
            'avg_monthly_return': avg_monthly_return,
            'avg_annual_return': avg_annual_return,
            'final_return_pct': total_return_pct
        }
    
    def _calculate_risk_metrics(self, equity_curve: pd.DataFrame, risk_free_rate: float) -> Dict[str, float]:
        """Calculate risk-based metrics"""
        if 'portfolio_value' not in equity_curve.columns:
            return {}
        
        values = equity_curve['portfolio_value']
        returns = values.pct_change().dropna()
        
        if len(returns) == 0:
            return {}
        
        # Volatility metrics
        daily_vol = returns.std()
        annual_vol = daily_vol * np.sqrt(252)
        
        # Sharpe ratio
        excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
        if daily_vol > 0:
            sharpe_ratio = excess_returns.mean() / daily_vol * np.sqrt(252)
        else:
            sharpe_ratio = 0
        
        # Sortino ratio (downside deviation)
        downside_returns = returns[returns < 0]
        if len(downside_returns) > 0:
            downside_deviation = downside_returns.std() * np.sqrt(252)
            if downside_deviation > 0:
                sortino_ratio = (returns.mean() * 252 - risk_free_rate) / downside_deviation
            else:
                sortino_ratio = 0
        else:
            sortino_ratio = float('inf')
        
        # Calmar ratio (CAGR / Max Drawdown)
        total_days = (equity_curve.index[-1] - equity_curve.index[0]).days
        years = total_days / 365.25
        if years > 0:
            cagr = (values.iloc[-1] / values.iloc[0]) ** (1 / years) - 1
        else:
            cagr = 0
        
        peak = values.expanding().max()
        drawdown = (values - peak) / peak
        max_drawdown = abs(drawdown.min())
        
        if max_drawdown > 0:
            calmar_ratio = cagr / max_drawdown
        else:
            calmar_ratio = float('inf')
        
        # Value at Risk (VaR)
        var_95 = np.percentile(returns, 5)
        var_99 = np.percentile(returns, 1)
        
        # Expected Shortfall (Conditional VaR)
        es_95 = returns[returns <= var_95].mean()
        es_99 = returns[returns <= var_99].mean()
        
        return {
            'volatility': annual_vol,
            'daily_volatility': daily_vol,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': sortino_ratio,
            'calmar_ratio': calmar_ratio,
            'var_95': var_95,
            'var_99': var_99,
            'expected_shortfall_95': es_95,
            'expected_shortfall_99': es_99
        }
    
    def _calculate_drawdown_metrics(self, equity_curve: pd.DataFrame) -> Dict[str, float]:
        """Calculate drawdown-based metrics"""
        if 'portfolio_value' not in equity_curve.columns:
            return {}
        
        values = equity_curve['portfolio_value']
        
        # Calculate drawdowns
        peak = values.expanding().max()
        drawdown = (values - peak) / peak
        
        # Maximum drawdown
        max_drawdown = abs(drawdown.min())
        max_drawdown_pct = max_drawdown * 100
        
        # Average drawdown
        negative_drawdowns = drawdown[drawdown < 0]
        if len(negative_drawdowns) > 0:
            avg_drawdown = abs(negative_drawdowns.mean())
            avg_drawdown_pct = avg_drawdown * 100
        else:
            avg_drawdown = avg_drawdown_pct = 0
        
        # Drawdown duration
        in_drawdown = drawdown < 0
        drawdown_periods = []
        current_period = 0
        
        for is_dd in in_drawdown:
            if is_dd:
                current_period += 1
            else:
                if current_period > 0:
                    drawdown_periods.append(current_period)
                    current_period = 0
        
        if current_period > 0:
            drawdown_periods.append(current_period)
        
        if drawdown_periods:
            max_drawdown_duration = max(drawdown_periods)
            avg_drawdown_duration = np.mean(drawdown_periods)
        else:
            max_drawdown_duration = avg_drawdown_duration = 0
        
        # Recovery factor
        total_return = (values.iloc[-1] - values.iloc[0]) / values.iloc[0]
        if max_drawdown > 0:
            recovery_factor = total_return / max_drawdown
        else:
            recovery_factor = float('inf')
        
        return {
            'max_drawdown': max_drawdown,
            'max_drawdown_pct': max_drawdown_pct,
            'avg_drawdown': avg_drawdown,
            'avg_drawdown_pct': avg_drawdown_pct,
            'max_drawdown_duration': max_drawdown_duration,
            'avg_drawdown_duration': avg_drawdown_duration,
            'recovery_factor': recovery_factor
        }
    
    def _calculate_trade_metrics(self, trade_log: pd.DataFrame) -> Dict[str, Any]:
        """Calculate trade-based metrics"""
        if trade_log.empty:
            return {}
        
        # Basic trade counts
        total_trades = len(trade_log)
        buy_trades = len(trade_log[trade_log['action'] == 'buy'])
        sell_trades = len(trade_log[trade_log['action'] == 'sell'])
        
        # Calculate trade returns (simplified - assumes paired buy/sell)
        trade_returns = []
        positions = {}
        
        for _, trade in trade_log.iterrows():
            symbol = trade['symbol']
            action = trade['action']
            quantity = trade['quantity']
            price = trade['executed_price']
            
            if action == 'buy':
                if symbol not in positions:
                    positions[symbol] = []
                positions[symbol].append({'quantity': quantity, 'price': price})
            
            elif action == 'sell' and symbol in positions:
                remaining_quantity = quantity
                trade_pnl = 0
                
                while remaining_quantity > 0 and positions[symbol]:
                    position = positions[symbol][0]
                    pos_quantity = position['quantity']
                    pos_price = position['price']
                    
                    if pos_quantity <= remaining_quantity:
                        # Close entire position
                        trade_pnl += pos_quantity * (price - pos_price)
                        remaining_quantity -= pos_quantity
                        positions[symbol].pop(0)
                    else:
                        # Partial close
                        trade_pnl += remaining_quantity * (price - pos_price)
                        positions[symbol][0]['quantity'] -= remaining_quantity
                        remaining_quantity = 0
                
                if trade_pnl != 0:
                    # Calculate return as percentage
                    cost_basis = quantity * price - trade_pnl
                    if cost_basis > 0:
                        trade_return = trade_pnl / cost_basis
                        trade_returns.append(trade_return)
        
        # Win/Loss analysis
        if trade_returns:
            winning_trades = [r for r in trade_returns if r > 0]
            losing_trades = [r for r in trade_returns if r < 0]
            
            win_count = len(winning_trades)
            loss_count = len(losing_trades)
            total_closed_trades = win_count + loss_count
            
            win_rate = win_count / total_closed_trades if total_closed_trades > 0 else 0
            win_rate_pct = win_rate * 100
            
            # Average trade metrics
            avg_trade_return = np.mean(trade_returns) if trade_returns else 0
            avg_trade_return_pct = avg_trade_return * 100
            
            avg_winning_trade = np.mean(winning_trades) if winning_trades else 0
            avg_losing_trade = np.mean(losing_trades) if losing_trades else 0
            
            # Profit factor
            gross_profit = sum(winning_trades) if winning_trades else 0
            gross_loss = abs(sum(losing_trades)) if losing_trades else 0
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
            
            # Expectancy
            expectancy = (win_rate * avg_winning_trade) - ((1 - win_rate) * abs(avg_losing_trade))
            expectancy_pct = expectancy * 100
            
        else:
            win_count = loss_count = total_closed_trades = 0
            win_rate = win_rate_pct = 0
            avg_trade_return = avg_trade_return_pct = 0
            avg_winning_trade = avg_losing_trade = 0
            profit_factor = 0
            expectancy = expectancy_pct = 0
        
        # Trade frequency
        if len(trade_log) > 1:
            time_diff = trade_log.index[-1] - trade_log.index[0]
            days = time_diff.days
            trades_per_day = total_trades / days if days > 0 else 0
            trades_per_month = trades_per_day * 30
        else:
            trades_per_day = trades_per_month = 0
        
        return {
            'total_trades': total_trades,
            'buy_trades': buy_trades,
            'sell_trades': sell_trades,
            'closed_trades': total_closed_trades,
            'winning_trades': win_count,
            'losing_trades': loss_count,
            'win_rate': win_rate,
            'win_rate_pct': win_rate_pct,
            'avg_trade_return': avg_trade_return,
            'avg_trade_return_pct': avg_trade_return_pct,
            'avg_winning_trade': avg_winning_trade,
            'avg_losing_trade': avg_losing_trade,
            'profit_factor': profit_factor,
            'expectancy': expectancy,
            'expectancy_pct': expectancy_pct,
            'trades_per_day': trades_per_day,
            'trades_per_month': trades_per_month
        }
    
    def _calculate_benchmark_metrics(self, equity_curve: pd.DataFrame, 
                                   benchmark_returns: pd.Series) -> Dict[str, float]:
        """Calculate benchmark comparison metrics"""
        if 'portfolio_value' not in equity_curve.columns:
            return {}
        
        values = equity_curve['portfolio_value']
        strategy_returns = values.pct_change().dropna()
        
        # Align returns with benchmark
        common_dates = strategy_returns.index.intersection(benchmark_returns.index)
        if len(common_dates) == 0:
            return {}
        
        aligned_strategy = strategy_returns.loc[common_dates]
        aligned_benchmark = benchmark_returns.loc[common_dates]
        
        # Alpha and Beta
        if len(aligned_strategy) > 1 and len(aligned_benchmark) > 1:
            covariance = np.cov(aligned_strategy, aligned_benchmark)[0, 1]
            benchmark_variance = np.var(aligned_benchmark)
            
            if benchmark_variance > 0:
                beta = covariance / benchmark_variance
                alpha = aligned_strategy.mean() - beta * aligned_benchmark.mean()
                alpha_annualized = alpha * 252
            else:
                beta = alpha = alpha_annualized = 0
        else:
            beta = alpha = alpha_annualized = 0
        
        # Information ratio
        excess_returns = aligned_strategy - aligned_benchmark
        if len(excess_returns) > 0 and excess_returns.std() > 0:
            information_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252)
        else:
            information_ratio = 0
        
        # Tracking error
        tracking_error = excess_returns.std() * np.sqrt(252) if len(excess_returns) > 0 else 0
        
        return {
            'alpha': alpha,
            'alpha_annualized': alpha_annualized,
            'beta': beta,
            'information_ratio': information_ratio,
            'tracking_error': tracking_error
        }
    
    def _calculate_advanced_metrics(self, equity_curve: pd.DataFrame) -> Dict[str, float]:
        """Calculate advanced performance metrics"""
        if 'portfolio_value' not in equity_curve.columns:
            return {}
        
        values = equity_curve['portfolio_value']
        returns = values.pct_change().dropna()
        
        if len(returns) == 0:
            return {}
        
        # Skewness and Kurtosis
        skewness = returns.skew()
        kurtosis = returns.kurtosis()
        
        # Tail ratio
        returns_sorted = returns.sort_values()
        n = len(returns_sorted)
        if n >= 20:  # Need sufficient data
            top_10_pct = returns_sorted.iloc[int(0.9 * n):].mean()
            bottom_10_pct = returns_sorted.iloc[:int(0.1 * n)].mean()
            tail_ratio = abs(top_10_pct / bottom_10_pct) if bottom_10_pct != 0 else 0
        else:
            tail_ratio = 0
        
        # Stability metrics
        rolling_returns = returns.rolling(window=21).mean()  # 21-day rolling average
        return_stability = 1 - (rolling_returns.std() / returns.std()) if returns.std() > 0 else 0
        
        # Consistency score (percentage of positive months)
        monthly_returns = returns.resample('M').apply(lambda x: (1 + x).prod() - 1)
        positive_months = (monthly_returns > 0).sum()
        total_months = len(monthly_returns)
        consistency_score = positive_months / total_months if total_months > 0 else 0
        
        return {
            'skewness': skewness,
            'kurtosis': kurtosis,
            'tail_ratio': tail_ratio,
            'return_stability': return_stability,
            'consistency_score': consistency_score,
            'positive_months': positive_months,
            'total_months': total_months
        }
    
    def _calculate_star_rating(self, metrics: Dict[str, Any]) -> int:
        """Calculate star rating (1-5 stars) based on key metrics
        
        Args:
            metrics: Dictionary of calculated metrics
            
        Returns:
            Star rating from 1 to 5
        """
        try:
            score = 0
            max_score = 0
            
            # Profit Factor (25% weight)
            profit_factor = metrics.get('profit_factor', 0)
            if profit_factor >= 2.0:
                score += 25
            elif profit_factor >= 1.5:
                score += 20
            elif profit_factor >= 1.2:
                score += 15
            elif profit_factor >= 1.0:
                score += 10
            max_score += 25
            
            # Sharpe Ratio (25% weight)
            sharpe_ratio = metrics.get('sharpe_ratio', 0)
            if sharpe_ratio >= 2.0:
                score += 25
            elif sharpe_ratio >= 1.5:
                score += 20
            elif sharpe_ratio >= 1.0:
                score += 15
            elif sharpe_ratio >= 0.5:
                score += 10
            max_score += 25
            
            # Win Rate (20% weight)
            win_rate_pct = metrics.get('win_rate_pct', 0)
            if win_rate_pct >= 70:
                score += 20
            elif win_rate_pct >= 60:
                score += 16
            elif win_rate_pct >= 50:
                score += 12
            elif win_rate_pct >= 40:
                score += 8
            max_score += 20
            
            # Max Drawdown (15% weight) - lower is better
            max_drawdown_pct = metrics.get('max_drawdown_pct', 100)
            if max_drawdown_pct <= 5:
                score += 15
            elif max_drawdown_pct <= 10:
                score += 12
            elif max_drawdown_pct <= 20:
                score += 9
            elif max_drawdown_pct <= 30:
                score += 6
            max_score += 15
            
            # Total Return (15% weight)
            total_return_pct = metrics.get('total_return_pct', 0)
            if total_return_pct >= 100:
                score += 15
            elif total_return_pct >= 50:
                score += 12
            elif total_return_pct >= 20:
                score += 9
            elif total_return_pct >= 10:
                score += 6
            elif total_return_pct > 0:
                score += 3
            max_score += 15
            
            # Calculate star rating
            if max_score > 0:
                percentage = (score / max_score) * 100
                if percentage >= 90:
                    return 5
                elif percentage >= 75:
                    return 4
                elif percentage >= 60:
                    return 3
                elif percentage >= 40:
                    return 2
                else:
                    return 1
            else:
                return 1
                
        except Exception as e:
            self.logger.error(f"Error calculating star rating: {e}")
            return 1
    
    def compare_strategies(self, results_list: List[Dict[str, Any]]) -> pd.DataFrame:
        """Compare multiple strategy results
        
        Args:
            results_list: List of strategy result dictionaries
            
        Returns:
            DataFrame with comparison metrics
        """
        comparison_data = []
        
        for result in results_list:
            if not result.get('success', False):
                continue
                
            strategy_name = result.get('strategy_name', 'Unknown')
            metrics = result.get('metrics', {})
            performance = result.get('performance', {})
            
            # Combine key metrics
            row = {
                'Strategy': strategy_name,
                'Total Return %': performance.get('total_return_pct', 0),
                'CAGR %': metrics.get('cagr_pct', 0),
                'Sharpe Ratio': metrics.get('sharpe_ratio', 0),
                'Max Drawdown %': metrics.get('max_drawdown_pct', 0),
                'Win Rate %': metrics.get('win_rate_pct', 0),
                'Profit Factor': metrics.get('profit_factor', 0),
                'Total Trades': metrics.get('total_trades', 0),
                'Star Rating': metrics.get('star_rating', 1)
            }
            
            comparison_data.append(row)
        
        if comparison_data:
            df = pd.DataFrame(comparison_data)
            # Sort by star rating and total return
            df = df.sort_values(['Star Rating', 'Total Return %'], ascending=[False, False])
            return df
        else:
            return pd.DataFrame()