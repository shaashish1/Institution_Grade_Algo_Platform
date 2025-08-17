"""
Chart Generator
===============

Generate charts and visualizations for backtest results.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
import base64
from io import BytesIO

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.figure import Figure
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.offline as pyo
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


class ChartGenerator:
    """Generate charts and visualizations for backtest results"""
    
    def __init__(self, use_plotly: bool = True):
        """Initialize chart generator
        
        Args:
            use_plotly: Use Plotly for interactive charts (fallback to matplotlib)
        """
        self.use_plotly = use_plotly and PLOTLY_AVAILABLE
        self.logger = logging.getLogger(__name__)
        
        if not MATPLOTLIB_AVAILABLE and not PLOTLY_AVAILABLE:
            self.logger.warning("Neither matplotlib nor plotly available. Charts will not be generated.")
        
        # Set style for matplotlib
        if MATPLOTLIB_AVAILABLE:
            plt.style.use('seaborn-v0_8' if hasattr(plt.style, 'seaborn-v0_8') else 'default')
    
    def generate_equity_curve(self, equity_curve: pd.DataFrame, 
                            benchmark_data: Optional[pd.DataFrame] = None,
                            title: str = "Equity Curve") -> Optional[str]:
        """Generate equity curve chart
        
        Args:
            equity_curve: DataFrame with portfolio values over time
            benchmark_data: Optional benchmark data for comparison
            title: Chart title
            
        Returns:
            Chart as HTML string or base64 encoded image
        """
        if equity_curve.empty or 'portfolio_value' not in equity_curve.columns:
            return None
        
        try:
            if self.use_plotly:
                return self._generate_equity_curve_plotly(equity_curve, benchmark_data, title)
            else:
                return self._generate_equity_curve_matplotlib(equity_curve, benchmark_data, title)
        except Exception as e:
            self.logger.error(f"Error generating equity curve: {e}")
            return None
    
    def generate_drawdown_chart(self, equity_curve: pd.DataFrame,
                              title: str = "Drawdown Chart") -> Optional[str]:
        """Generate drawdown chart
        
        Args:
            equity_curve: DataFrame with portfolio values over time
            title: Chart title
            
        Returns:
            Chart as HTML string or base64 encoded image
        """
        if equity_curve.empty or 'portfolio_value' not in equity_curve.columns:
            return None
        
        try:
            # Calculate drawdown
            values = equity_curve['portfolio_value']
            peak = values.expanding().max()
            drawdown = (values - peak) / peak * 100
            
            if self.use_plotly:
                return self._generate_drawdown_plotly(drawdown, title)
            else:
                return self._generate_drawdown_matplotlib(drawdown, title)
        except Exception as e:
            self.logger.error(f"Error generating drawdown chart: {e}")
            return None
    
    def generate_returns_distribution(self, equity_curve: pd.DataFrame,
                                    title: str = "Returns Distribution") -> Optional[str]:
        """Generate returns distribution histogram
        
        Args:
            equity_curve: DataFrame with portfolio values over time
            title: Chart title
            
        Returns:
            Chart as HTML string or base64 encoded image
        """
        if equity_curve.empty or 'portfolio_value' not in equity_curve.columns:
            return None
        
        try:
            returns = equity_curve['portfolio_value'].pct_change().dropna() * 100
            
            if self.use_plotly:
                return self._generate_returns_distribution_plotly(returns, title)
            else:
                return self._generate_returns_distribution_matplotlib(returns, title)
        except Exception as e:
            self.logger.error(f"Error generating returns distribution: {e}")
            return None
    
    def generate_monthly_returns_heatmap(self, equity_curve: pd.DataFrame,
                                       title: str = "Monthly Returns Heatmap") -> Optional[str]:
        """Generate monthly returns heatmap
        
        Args:
            equity_curve: DataFrame with portfolio values over time
            title: Chart title
            
        Returns:
            Chart as HTML string or base64 encoded image
        """
        if equity_curve.empty or 'portfolio_value' not in equity_curve.columns:
            return None
        
        try:
            # Calculate monthly returns
            monthly_returns = equity_curve['portfolio_value'].resample('M').apply(
                lambda x: (x.iloc[-1] / x.iloc[0] - 1) * 100 if len(x) > 0 else 0
            )
            
            # Create pivot table for heatmap
            monthly_returns.index = pd.to_datetime(monthly_returns.index)
            monthly_returns_df = pd.DataFrame({
                'Year': monthly_returns.index.year,
                'Month': monthly_returns.index.month,
                'Return': monthly_returns.values
            })
            
            pivot_table = monthly_returns_df.pivot(index='Year', columns='Month', values='Return')
            
            if self.use_plotly:
                return self._generate_monthly_heatmap_plotly(pivot_table, title)
            else:
                return self._generate_monthly_heatmap_matplotlib(pivot_table, title)
        except Exception as e:
            self.logger.error(f"Error generating monthly returns heatmap: {e}")
            return None
    
    def generate_performance_comparison(self, results_list: List[Dict[str, Any]],
                                      title: str = "Strategy Performance Comparison") -> Optional[str]:
        """Generate performance comparison chart
        
        Args:
            results_list: List of strategy results
            title: Chart title
            
        Returns:
            Chart as HTML string or base64 encoded image
        """
        if not results_list:
            return None
        
        try:
            # Extract comparison data
            comparison_data = []
            for result in results_list:
                if result.get('success', False):
                    metrics = result.get('metrics', {})
                    performance = result.get('performance', {})
                    
                    comparison_data.append({
                        'Strategy': result.get('strategy_name', 'Unknown'),
                        'Total Return %': performance.get('total_return_pct', 0),
                        'Sharpe Ratio': metrics.get('sharpe_ratio', 0),
                        'Max Drawdown %': abs(metrics.get('max_drawdown_pct', 0)),
                        'Win Rate %': metrics.get('win_rate_pct', 0)
                    })
            
            if not comparison_data:
                return None
            
            df = pd.DataFrame(comparison_data)
            
            if self.use_plotly:
                return self._generate_comparison_plotly(df, title)
            else:
                return self._generate_comparison_matplotlib(df, title)
        except Exception as e:
            self.logger.error(f"Error generating performance comparison: {e}")
            return None
    
    def _generate_equity_curve_plotly(self, equity_curve: pd.DataFrame,
                                    benchmark_data: Optional[pd.DataFrame],
                                    title: str) -> str:
        """Generate equity curve using Plotly"""
        fig = go.Figure()
        
        # Add equity curve
        fig.add_trace(go.Scatter(
            x=equity_curve.index,
            y=equity_curve['portfolio_value'],
            mode='lines',
            name='Portfolio Value',
            line=dict(color='blue', width=2)
        ))
        
        # Add benchmark if provided
        if benchmark_data is not None and not benchmark_data.empty:
            fig.add_trace(go.Scatter(
                x=benchmark_data.index,
                y=benchmark_data.iloc[:, 0],  # Assume first column is benchmark
                mode='lines',
                name='Benchmark',
                line=dict(color='red', width=1, dash='dash')
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Portfolio Value',
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def _generate_equity_curve_matplotlib(self, equity_curve: pd.DataFrame,
                                        benchmark_data: Optional[pd.DataFrame],
                                        title: str) -> str:
        """Generate equity curve using Matplotlib"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot equity curve
        ax.plot(equity_curve.index, equity_curve['portfolio_value'], 
                label='Portfolio Value', color='blue', linewidth=2)
        
        # Plot benchmark if provided
        if benchmark_data is not None and not benchmark_data.empty:
            ax.plot(benchmark_data.index, benchmark_data.iloc[:, 0],
                   label='Benchmark', color='red', linestyle='--', alpha=0.7)
        
        ax.set_title(title)
        ax.set_xlabel('Date')
        ax.set_ylabel('Portfolio Value')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f'<img src="data:image/png;base64,{image_base64}" style="max-width:100%;">'
    
    def _generate_drawdown_plotly(self, drawdown: pd.Series, title: str) -> str:
        """Generate drawdown chart using Plotly"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=drawdown.index,
            y=drawdown,
            mode='lines',
            fill='tonexty',
            name='Drawdown %',
            line=dict(color='red'),
            fillcolor='rgba(255, 0, 0, 0.3)'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Drawdown %',
            hovermode='x unified',
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def _generate_drawdown_matplotlib(self, drawdown: pd.Series, title: str) -> str:
        """Generate drawdown chart using Matplotlib"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.fill_between(drawdown.index, drawdown, 0, alpha=0.3, color='red')
        ax.plot(drawdown.index, drawdown, color='red', linewidth=1)
        
        ax.set_title(title)
        ax.set_xlabel('Date')
        ax.set_ylabel('Drawdown %')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f'<img src="data:image/png;base64,{image_base64}" style="max-width:100%;">'
    
    def _generate_returns_distribution_plotly(self, returns: pd.Series, title: str) -> str:
        """Generate returns distribution using Plotly"""
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=returns,
            nbinsx=50,
            name='Daily Returns %',
            opacity=0.7
        ))
        
        # Add normal distribution overlay
        mean_return = returns.mean()
        std_return = returns.std()
        x_range = np.linspace(returns.min(), returns.max(), 100)
        normal_dist = (1 / (std_return * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_range - mean_return) / std_return) ** 2)
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=normal_dist * len(returns) * (returns.max() - returns.min()) / 50,
            mode='lines',
            name='Normal Distribution',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Daily Returns %',
            yaxis_title='Frequency',
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def _generate_returns_distribution_matplotlib(self, returns: pd.Series, title: str) -> str:
        """Generate returns distribution using Matplotlib"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Histogram
        n, bins, patches = ax.hist(returns, bins=50, alpha=0.7, density=True, color='skyblue')
        
        # Normal distribution overlay
        mean_return = returns.mean()
        std_return = returns.std()
        x_range = np.linspace(returns.min(), returns.max(), 100)
        normal_dist = (1 / (std_return * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_range - mean_return) / std_return) ** 2)
        ax.plot(x_range, normal_dist, 'r--', label='Normal Distribution')
        
        ax.set_title(title)
        ax.set_xlabel('Daily Returns %')
        ax.set_ylabel('Density')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f'<img src="data:image/png;base64,{image_base64}" style="max-width:100%;">'
    
    def _generate_monthly_heatmap_plotly(self, pivot_table: pd.DataFrame, title: str) -> str:
        """Generate monthly returns heatmap using Plotly"""
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=[month_names[i-1] for i in pivot_table.columns],
            y=pivot_table.index,
            colorscale='RdYlGn',
            zmid=0,
            text=np.round(pivot_table.values, 2),
            texttemplate='%{text}%',
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Month',
            yaxis_title='Year',
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def _generate_monthly_heatmap_matplotlib(self, pivot_table: pd.DataFrame, title: str) -> str:
        """Generate monthly returns heatmap using Matplotlib"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Create heatmap
        im = ax.imshow(pivot_table.values, cmap='RdYlGn', aspect='auto', vmin=-10, vmax=10)
        
        # Set ticks and labels
        ax.set_xticks(range(len(pivot_table.columns)))
        ax.set_xticklabels([month_names[i-1] for i in pivot_table.columns])
        ax.set_yticks(range(len(pivot_table.index)))
        ax.set_yticklabels(pivot_table.index)
        
        # Add text annotations
        for i in range(len(pivot_table.index)):
            for j in range(len(pivot_table.columns)):
                value = pivot_table.iloc[i, j]
                if not np.isnan(value):
                    ax.text(j, i, f'{value:.1f}%', ha='center', va='center', fontsize=8)
        
        ax.set_title(title)
        plt.colorbar(im, ax=ax, label='Monthly Return %')
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f'<img src="data:image/png;base64,{image_base64}" style="max-width:100%;">'
    
    def _generate_comparison_plotly(self, df: pd.DataFrame, title: str) -> str:
        """Generate performance comparison using Plotly"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total Return %', 'Sharpe Ratio', 'Max Drawdown %', 'Win Rate %'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Total Return
        fig.add_trace(go.Bar(x=df['Strategy'], y=df['Total Return %'], name='Total Return %'), row=1, col=1)
        
        # Sharpe Ratio
        fig.add_trace(go.Bar(x=df['Strategy'], y=df['Sharpe Ratio'], name='Sharpe Ratio'), row=1, col=2)
        
        # Max Drawdown
        fig.add_trace(go.Bar(x=df['Strategy'], y=df['Max Drawdown %'], name='Max Drawdown %'), row=2, col=1)
        
        # Win Rate
        fig.add_trace(go.Bar(x=df['Strategy'], y=df['Win Rate %'], name='Win Rate %'), row=2, col=2)
        
        fig.update_layout(
            title_text=title,
            showlegend=False,
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn')
    
    def _generate_comparison_matplotlib(self, df: pd.DataFrame, title: str) -> str:
        """Generate performance comparison using Matplotlib"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Total Return
        axes[0, 0].bar(df['Strategy'], df['Total Return %'])
        axes[0, 0].set_title('Total Return %')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Sharpe Ratio
        axes[0, 1].bar(df['Strategy'], df['Sharpe Ratio'])
        axes[0, 1].set_title('Sharpe Ratio')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Max Drawdown
        axes[1, 0].bar(df['Strategy'], df['Max Drawdown %'])
        axes[1, 0].set_title('Max Drawdown %')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Win Rate
        axes[1, 1].bar(df['Strategy'], df['Win Rate %'])
        axes[1, 1].set_title('Win Rate %')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.suptitle(title)
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f'<img src="data:image/png;base64,{image_base64}" style="max-width:100%;">'