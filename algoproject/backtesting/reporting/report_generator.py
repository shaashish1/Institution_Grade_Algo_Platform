"""
Report Generator
================

Generate comprehensive reports for backtest results.
"""

import pandas as pd
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import os

from .performance_analyzer import PerformanceAnalyzer
from .chart_generator import ChartGenerator


class ReportGenerator:
    """Generate comprehensive backtest reports"""
    
    def __init__(self, use_interactive_charts: bool = True):
        """Initialize report generator
        
        Args:
            use_interactive_charts: Use interactive Plotly charts
        """
        self.logger = logging.getLogger(__name__)
        self.performance_analyzer = PerformanceAnalyzer()
        self.chart_generator = ChartGenerator(use_plotly=use_interactive_charts)
    
    def generate_single_strategy_report(self, backtest_result: Dict[str, Any],
                                      output_path: str = None,
                                      include_charts: bool = True) -> str:
        """Generate comprehensive report for a single strategy
        
        Args:
            backtest_result: Backtest result dictionary
            output_path: Output file path (optional)
            include_charts: Include charts in report
            
        Returns:
            HTML report string
        """
        try:
            if not backtest_result.get('success', False):
                return self._generate_error_report(backtest_result)
            
            # Extract data
            strategy_name = backtest_result.get('strategy_name', 'Unknown Strategy')
            equity_curve_data = backtest_result.get('equity_curve', [])
            trade_log_data = backtest_result.get('trade_log', [])
            performance = backtest_result.get('performance', {})
            metrics = backtest_result.get('metrics', {})
            
            # Convert to DataFrames
            equity_curve = pd.DataFrame(equity_curve_data)
            if not equity_curve.empty and 'timestamp' in equity_curve.columns:
                equity_curve['timestamp'] = pd.to_datetime(equity_curve['timestamp'])
                equity_curve.set_index('timestamp', inplace=True)
            
            trade_log = pd.DataFrame(trade_log_data)
            if not trade_log.empty and 'timestamp' in trade_log.columns:
                trade_log['timestamp'] = pd.to_datetime(trade_log['timestamp'])
                trade_log.set_index('timestamp', inplace=True)
            
            # Calculate comprehensive metrics
            comprehensive_metrics = self.performance_analyzer.calculate_comprehensive_metrics(
                equity_curve, trade_log
            )
            
            # Generate HTML report
            html_content = self._build_single_strategy_html(
                strategy_name, performance, comprehensive_metrics, 
                equity_curve, trade_log, include_charts
            )
            
            # Save to file if path provided
            if output_path:
                self._save_html_report(html_content, output_path)
            
            return html_content
            
        except Exception as e:
            self.logger.error(f"Error generating single strategy report: {e}")
            return self._generate_error_report({'error': str(e)})
    
    def generate_matrix_report(self, matrix_results: List[Dict[str, Any]],
                             output_path: str = None,
                             include_charts: bool = True) -> str:
        """Generate comprehensive report for matrix backtest results
        
        Args:
            matrix_results: List of backtest results
            output_path: Output file path (optional)
            include_charts: Include charts in report
            
        Returns:
            HTML report string
        """
        try:
            if not matrix_results:
                return self._generate_error_report({'error': 'No results provided'})
            
            # Filter successful results
            successful_results = [r for r in matrix_results if r.get('success', False)]
            
            if not successful_results:
                return self._generate_error_report({'error': 'No successful results'})
            
            # Generate comparison DataFrame
            comparison_df = self.performance_analyzer.compare_strategies(successful_results)
            
            # Calculate summary statistics
            summary_stats = self._calculate_matrix_summary(successful_results)
            
            # Generate HTML report
            html_content = self._build_matrix_html(
                successful_results, comparison_df, summary_stats, include_charts
            )
            
            # Save to file if path provided
            if output_path:
                self._save_html_report(html_content, output_path)
            
            return html_content
            
        except Exception as e:
            self.logger.error(f"Error generating matrix report: {e}")
            return self._generate_error_report({'error': str(e)})
    
    def export_results_csv(self, results: List[Dict[str, Any]], output_path: str):
        """Export results to CSV format
        
        Args:
            results: List of backtest results
            output_path: Output CSV file path
        """
        try:
            data = []
            
            for result in results:
                if not result.get('success', False):
                    continue
                
                performance = result.get('performance', {})
                metrics = result.get('metrics', {})
                
                row = {
                    'Strategy': result.get('strategy_name', 'Unknown'),
                    'Symbols': ','.join(result.get('symbols', [])),
                    'Success': result.get('success', False),
                    'Execution Time': result.get('execution_time', 0),
                    **performance,
                    **metrics
                }
                
                data.append(row)
            
            if data:
                df = pd.DataFrame(data)
                df.to_csv(output_path, index=False)
                self.logger.info(f"Results exported to CSV: {output_path}")
            else:
                self.logger.warning("No data to export")
                
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {e}")
            raise
    
    def export_results_json(self, results: List[Dict[str, Any]], output_path: str):
        """Export results to JSON format
        
        Args:
            results: List of backtest results
            output_path: Output JSON file path
        """
        try:
            # Convert datetime objects to strings for JSON serialization
            serializable_results = []
            for result in results:
                serializable_result = self._make_json_serializable(result.copy())
                serializable_results.append(serializable_result)
            
            with open(output_path, 'w') as f:
                json.dump(serializable_results, f, indent=2, default=str)
            
            self.logger.info(f"Results exported to JSON: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error exporting to JSON: {e}")
            raise
    
    def _build_single_strategy_html(self, strategy_name: str, performance: Dict[str, Any],
                                  metrics: Dict[str, Any], equity_curve: pd.DataFrame,
                                  trade_log: pd.DataFrame, include_charts: bool) -> str:
        """Build HTML content for single strategy report"""
        
        # Generate charts
        charts_html = ""
        if include_charts and not equity_curve.empty:
            equity_chart = self.chart_generator.generate_equity_curve(equity_curve, title=f"{strategy_name} - Equity Curve")
            drawdown_chart = self.chart_generator.generate_drawdown_chart(equity_curve, title=f"{strategy_name} - Drawdown")
            returns_dist = self.chart_generator.generate_returns_distribution(equity_curve, title=f"{strategy_name} - Returns Distribution")
            
            if equity_chart:
                charts_html += f'<div class="chart-container">{equity_chart}</div>'
            if drawdown_chart:
                charts_html += f'<div class="chart-container">{drawdown_chart}</div>'
            if returns_dist:
                charts_html += f'<div class="chart-container">{returns_dist}</div>'
        
        # Build performance table
        performance_table = self._build_performance_table(performance, metrics)
        
        # Build trade log table
        trade_table = self._build_trade_table(trade_log)
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Backtest Report - {strategy_name}</title>
            <style>
                {self._get_css_styles()}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Backtest Report</h1>
                    <h2>{strategy_name}</h2>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </header>
                
                <section class="summary">
                    <h3>Performance Summary</h3>
                    {performance_table}
                </section>
                
                {charts_html}
                
                <section class="trades">
                    <h3>Trade Log</h3>
                    {trade_table}
                </section>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def _build_matrix_html(self, results: List[Dict[str, Any]], comparison_df: pd.DataFrame,
                          summary_stats: Dict[str, Any], include_charts: bool) -> str:
        """Build HTML content for matrix report"""
        
        # Generate comparison chart
        charts_html = ""
        if include_charts and not comparison_df.empty:
            comparison_chart = self.chart_generator.generate_performance_comparison(
                results, title="Strategy Performance Comparison"
            )
            if comparison_chart:
                charts_html += f'<div class="chart-container">{comparison_chart}</div>'
        
        # Build comparison table
        comparison_table = self._build_comparison_table(comparison_df)
        
        # Build summary statistics
        summary_html = self._build_summary_stats(summary_stats)
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Matrix Backtest Report</title>
            <style>
                {self._get_css_styles()}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Matrix Backtest Report</h1>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </header>
                
                <section class="summary">
                    <h3>Summary Statistics</h3>
                    {summary_html}
                </section>
                
                {charts_html}
                
                <section class="comparison">
                    <h3>Strategy Comparison</h3>
                    {comparison_table}
                </section>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def _build_performance_table(self, performance: Dict[str, Any], metrics: Dict[str, Any]) -> str:
        """Build performance metrics table"""
        combined_metrics = {**performance, **metrics}
        
        # Key metrics to display
        key_metrics = [
            ('Total Return %', 'total_return_pct'),
            ('CAGR %', 'cagr_pct'),
            ('Sharpe Ratio', 'sharpe_ratio'),
            ('Sortino Ratio', 'sortino_ratio'),
            ('Max Drawdown %', 'max_drawdown_pct'),
            ('Win Rate %', 'win_rate_pct'),
            ('Profit Factor', 'profit_factor'),
            ('Total Trades', 'total_trades'),
            ('Star Rating', 'star_rating')
        ]
        
        table_rows = ""
        for display_name, key in key_metrics:
            value = combined_metrics.get(key, 'N/A')
            if isinstance(value, (int, float)) and value != 'N/A':
                if 'pct' in key or 'rate' in key:
                    formatted_value = f"{value:.2f}%"
                elif key == 'star_rating':
                    formatted_value = '★' * int(value) + '☆' * (5 - int(value))
                else:
                    formatted_value = f"{value:.2f}"
            else:
                formatted_value = str(value)
            
            table_rows += f"<tr><td>{display_name}</td><td>{formatted_value}</td></tr>"
        
        return f"""
        <table class="performance-table">
            <thead>
                <tr><th>Metric</th><th>Value</th></tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        """
    
    def _build_comparison_table(self, comparison_df: pd.DataFrame) -> str:
        """Build strategy comparison table"""
        if comparison_df.empty:
            return "<p>No comparison data available</p>"
        
        # Format the DataFrame for display
        formatted_df = comparison_df.copy()
        
        # Format numeric columns
        numeric_columns = ['Total Return %', 'CAGR %', 'Sharpe Ratio', 'Max Drawdown %', 'Win Rate %', 'Profit Factor']
        for col in numeric_columns:
            if col in formatted_df.columns:
                formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else 'N/A')
        
        # Format star rating
        if 'Star Rating' in formatted_df.columns:
            formatted_df['Star Rating'] = formatted_df['Star Rating'].apply(
                lambda x: '★' * int(x) + '☆' * (5 - int(x)) if pd.notnull(x) else 'N/A'
            )
        
        return formatted_df.to_html(classes='comparison-table', index=False, escape=False)
    
    def _build_trade_table(self, trade_log: pd.DataFrame) -> str:
        """Build trade log table"""
        if trade_log.empty:
            return "<p>No trades executed</p>"
        
        # Show only recent trades (last 20)
        recent_trades = trade_log.tail(20).copy()
        
        # Format columns
        if 'executed_price' in recent_trades.columns:
            recent_trades['executed_price'] = recent_trades['executed_price'].apply(lambda x: f"${x:.2f}")
        if 'quantity' in recent_trades.columns:
            recent_trades['quantity'] = recent_trades['quantity'].apply(lambda x: f"{x:.0f}")
        
        return recent_trades.to_html(classes='trade-table', index=True)
    
    def _build_summary_stats(self, summary_stats: Dict[str, Any]) -> str:
        """Build summary statistics HTML"""
        stats_html = "<div class='summary-stats'>"
        
        for key, value in summary_stats.items():
            if isinstance(value, (int, float)):
                formatted_value = f"{value:.2f}" if isinstance(value, float) else str(value)
            else:
                formatted_value = str(value)
            
            stats_html += f"<div class='stat-item'><strong>{key.replace('_', ' ').title()}:</strong> {formatted_value}</div>"
        
        stats_html += "</div>"
        return stats_html
    
    def _calculate_matrix_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics for matrix results"""
        if not results:
            return {}
        
        # Extract performance metrics
        returns = []
        sharpe_ratios = []
        win_rates = []
        
        for result in results:
            performance = result.get('performance', {})
            metrics = result.get('metrics', {})
            
            if 'total_return_pct' in performance:
                returns.append(performance['total_return_pct'])
            if 'sharpe_ratio' in metrics:
                sharpe_ratios.append(metrics['sharpe_ratio'])
            if 'win_rate_pct' in metrics:
                win_rates.append(metrics['win_rate_pct'])
        
        summary = {
            'Total Strategies': len(results),
            'Avg Total Return %': np.mean(returns) if returns else 0,
            'Best Total Return %': max(returns) if returns else 0,
            'Worst Total Return %': min(returns) if returns else 0,
            'Avg Sharpe Ratio': np.mean(sharpe_ratios) if sharpe_ratios else 0,
            'Best Sharpe Ratio': max(sharpe_ratios) if sharpe_ratios else 0,
            'Avg Win Rate %': np.mean(win_rates) if win_rates else 0
        }
        
        return summary
    
    def _get_css_styles(self) -> str:
        """Get CSS styles for HTML reports"""
        return """
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #eee;
            padding-bottom: 20px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        
        h2 {
            color: #666;
            margin-bottom: 5px;
        }
        
        h3 {
            color: #444;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }
        
        .performance-table, .comparison-table, .trade-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        .performance-table th, .comparison-table th, .trade-table th,
        .performance-table td, .comparison-table td, .trade-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        .performance-table th, .comparison-table th, .trade-table th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        .performance-table tr:nth-child(even), .comparison-table tr:nth-child(even), .trade-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        .chart-container {
            margin: 30px 0;
            text-align: center;
        }
        
        .summary-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-item {
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
        
        .error-message {
            color: #dc3545;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        """
    
    def _generate_error_report(self, error_data: Dict[str, Any]) -> str:
        """Generate error report HTML"""
        error_message = error_data.get('error_message', error_data.get('error', 'Unknown error'))
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Backtest Report - Error</title>
            <style>{self._get_css_styles()}</style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Backtest Report - Error</h1>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </header>
                
                <div class="error-message">
                    <h3>Error Occurred</h3>
                    <p>{error_message}</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _save_html_report(self, html_content: str, output_path: str):
        """Save HTML report to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Report saved to: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")
            raise
    
    def _make_json_serializable(self, obj):
        """Make object JSON serializable by converting datetime objects"""
        if isinstance(obj, dict):
            return {key: self._make_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        else:
            return obj