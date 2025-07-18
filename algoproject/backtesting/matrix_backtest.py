"""
Matrix Backtesting System
========================

Advanced matrix backtesting with parallel processing and result aggregation.
"""

import pandas as pd
import logging
from typing import Dict, List, Any, Optional, Tuple, Callable
from datetime import datetime
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import itertools

from ..strategies.base_strategy import BaseStrategy
from ..data.data_loader import DataLoader
from .backtest_engine import BacktestEngine


@dataclass
class BacktestJob:
    """Represents a single backtest job"""
    job_id: str
    strategy_name: str
    strategy_class: type
    strategy_params: Dict[str, Any]
    symbols: List[str]
    start_date: datetime
    end_date: datetime
    timeframe: str
    initial_capital: float
    commission: float
    slippage: float


@dataclass
class BacktestResult:
    """Represents a backtest result"""
    job_id: str
    strategy_name: str
    symbols: List[str]
    success: bool
    error_message: Optional[str]
    execution_time: float
    results: Optional[Dict[str, Any]]


class MatrixBacktestEngine:
    """Advanced matrix backtesting engine with parallel processing"""
    
    def __init__(self, data_loader: DataLoader, max_workers: Optional[int] = None):
        """Initialize matrix backtest engine
        
        Args:
            data_loader: Data loader for historical data
            max_workers: Maximum number of parallel workers (None for auto-detect)
        """
        self.data_loader = data_loader
        self.max_workers = max_workers or 4
        self.logger = logging.getLogger(__name__)
        
        # Job management
        self.jobs: List[BacktestJob] = []
        self.results: List[BacktestResult] = []
        self.progress_callback: Optional[Callable] = None
        
        # Status tracking
        self.is_running = False
        self.completed_jobs = 0
        self.total_jobs = 0
        self.start_time: Optional[datetime] = None
    
    def add_strategy_symbol_combinations(self, strategies: List[Tuple[type, Dict[str, Any]]], 
                                       symbols: List[str], start_date: datetime, 
                                       end_date: datetime, timeframe: str = '1d',
                                       initial_capital: float = 100000.0,
                                       commission: float = 0.001, slippage: float = 0.001):
        """Add strategy-symbol combinations to the job queue
        
        Args:
            strategies: List of (strategy_class, parameters) tuples
            symbols: List of symbols to test
            start_date: Start date for backtests
            end_date: End date for backtests
            timeframe: Data timeframe
            initial_capital: Initial capital for each backtest
            commission: Commission rate
            slippage: Slippage factor
        """
        job_counter = len(self.jobs)
        
        for strategy_class, params in strategies:
            strategy_name = params.get('name', strategy_class.__name__)
            
            for symbol in symbols:
                job_counter += 1
                job_id = f"JOB_{job_counter:06d}"
                
                job = BacktestJob(
                    job_id=job_id,
                    strategy_name=strategy_name,
                    strategy_class=strategy_class,
                    strategy_params=params,
                    symbols=[symbol],
                    start_date=start_date,
                    end_date=end_date,
                    timeframe=timeframe,
                    initial_capital=initial_capital,
                    commission=commission,
                    slippage=slippage
                )
                
                self.jobs.append(job)
        
        self.logger.info(f"Added {len(strategies) * len(symbols)} jobs to queue")
    
    def add_parameter_sweep(self, strategy_class: type, param_ranges: Dict[str, List[Any]],
                           symbols: List[str], start_date: datetime, end_date: datetime,
                           timeframe: str = '1d', initial_capital: float = 100000.0,
                           commission: float = 0.001, slippage: float = 0.001):
        """Add parameter sweep jobs
        
        Args:
            strategy_class: Strategy class to test
            param_ranges: Dictionary of parameter names to lists of values
            symbols: List of symbols to test
            start_date: Start date for backtests
            end_date: End date for backtests
            timeframe: Data timeframe
            initial_capital: Initial capital
            commission: Commission rate
            slippage: Slippage factor
        """
        job_counter = len(self.jobs)
        
        # Generate all parameter combinations
        param_combinations = self._generate_param_combinations(param_ranges)
        
        for params in param_combinations:
            for symbol in symbols:
                job_counter += 1
                job_id = f"SWEEP_{job_counter:06d}"
                
                job = BacktestJob(
                    job_id=job_id,
                    strategy_name=f"{strategy_class.__name__}_{job_counter}",
                    strategy_class=strategy_class,
                    strategy_params=params,
                    symbols=[symbol],
                    start_date=start_date,
                    end_date=end_date,
                    timeframe=timeframe,
                    initial_capital=initial_capital,
                    commission=commission,
                    slippage=slippage
                )
                
                self.jobs.append(job)
        
        self.logger.info(f"Added {len(param_combinations) * len(symbols)} parameter sweep jobs")
    
    def run_matrix_backtest(self) -> List[BacktestResult]:
        """Run all queued backtest jobs
        
        Returns:
            List of backtest results
        """
        if not self.jobs:
            self.logger.warning("No jobs in queue")
            return []
        
        try:
            self.is_running = True
            self.start_time = datetime.now()
            self.total_jobs = len(self.jobs)
            self.completed_jobs = 0
            self.results.clear()
            
            self.logger.info(f"Starting matrix backtest with {self.total_jobs} jobs using {self.max_workers} workers")
            
            results = self._run_with_threads()
            self.results = results
            
            # Calculate summary statistics
            successful_jobs = [r for r in results if r.success]
            failed_jobs = [r for r in results if not r.success]
            
            total_time = (datetime.now() - self.start_time).total_seconds()
            avg_time_per_job = sum(r.execution_time for r in results) / len(results) if results else 0
            
            self.logger.info(f"Matrix backtest completed:")
            self.logger.info(f"  Total jobs: {len(results)}")
            self.logger.info(f"  Successful: {len(successful_jobs)}")
            self.logger.info(f"  Failed: {len(failed_jobs)}")
            self.logger.info(f"  Total time: {total_time:.2f}s")
            self.logger.info(f"  Avg time per job: {avg_time_per_job:.2f}s")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Matrix backtest failed: {e}")
            raise
        finally:
            self.is_running = False
    
    def _run_with_threads(self) -> List[BacktestResult]:
        """Run backtests using thread pool
        
        Returns:
            List of backtest results
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_job = {
                executor.submit(self._execute_single_job, job): job 
                for job in self.jobs
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_job):
                job = future_to_job[future]
                
                try:
                    result = future.result()
                    results.append(result)
                    self.completed_jobs += 1
                    
                    # Report progress
                    self._report_progress(result)
                    
                except Exception as e:
                    self.logger.error(f"Job {job.job_id} failed: {e}")
                    error_result = BacktestResult(
                        job_id=job.job_id,
                        strategy_name=job.strategy_name,
                        symbols=job.symbols,
                        success=False,
                        error_message=str(e),
                        execution_time=0.0,
                        results=None
                    )
                    results.append(error_result)
                    self.completed_jobs += 1
        
        return results
    
    def _execute_single_job(self, job: BacktestJob) -> BacktestResult:
        """Execute a single backtest job
        
        Args:
            job: Backtest job to execute
            
        Returns:
            Backtest result
        """
        start_time = time.time()
        
        try:
            # Create strategy instance
            strategy = job.strategy_class(job.strategy_name, job.strategy_params)
            
            # Create backtest engine
            engine = BacktestEngine(
                data_loader=self.data_loader,
                initial_capital=job.initial_capital,
                commission=job.commission,
                slippage=job.slippage
            )
            
            # Run backtest
            results = engine.run_backtest(
                strategy=strategy,
                symbols=job.symbols,
                start_date=job.start_date,
                end_date=job.end_date,
                timeframe=job.timeframe
            )
            
            execution_time = time.time() - start_time
            
            return BacktestResult(
                job_id=job.job_id,
                strategy_name=job.strategy_name,
                symbols=job.symbols,
                success=True,
                error_message=None,
                execution_time=execution_time,
                results=results
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            return BacktestResult(
                job_id=job.job_id,
                strategy_name=job.strategy_name,
                symbols=job.symbols,
                success=False,
                error_message=str(e),
                execution_time=execution_time,
                results=None
            )
    
    def _report_progress(self, result: BacktestResult):
        """Report progress of backtest execution
        
        Args:
            result: Completed backtest result
        """
        progress = (self.completed_jobs / self.total_jobs) * 100
        elapsed_time = (datetime.now() - self.start_time).total_seconds()
        
        if self.completed_jobs > 0:
            avg_time_per_job = elapsed_time / self.completed_jobs
            estimated_remaining = avg_time_per_job * (self.total_jobs - self.completed_jobs)
        else:
            estimated_remaining = 0
        
        status = "SUCCESS" if result.success else "FAILED"
        
        self.logger.info(f"Progress: {progress:.1f}% ({self.completed_jobs}/{self.total_jobs}) - "
                        f"{result.job_id} [{status}] - "
                        f"Time: {result.execution_time:.2f}s - "
                        f"ETA: {estimated_remaining:.0f}s")
        
        # Call progress callback if provided
        if self.progress_callback:
            try:
                self.progress_callback({
                    'completed': self.completed_jobs,
                    'total': self.total_jobs,
                    'progress': progress,
                    'elapsed_time': elapsed_time,
                    'estimated_remaining': estimated_remaining,
                    'last_result': result
                })
            except Exception as e:
                self.logger.error(f"Error in progress callback: {e}")
    
    def _generate_param_combinations(self, param_ranges: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        """Generate all parameter combinations
        
        Args:
            param_ranges: Dictionary of parameter ranges
            
        Returns:
            List of parameter combinations
        """
        keys = list(param_ranges.keys())
        values = list(param_ranges.values())
        
        combinations = []
        for combination in itertools.product(*values):
            param_dict = dict(zip(keys, combination))
            combinations.append(param_dict)
        
        return combinations
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get summary of all backtest results
        
        Returns:
            Dictionary with results summary
        """
        if not self.results:
            return {}
        
        successful_results = [r for r in self.results if r.success and r.results]
        
        if not successful_results:
            return {"error": "No successful results"}
        
        # Extract performance metrics
        performance_data = []
        for result in successful_results:
            if result.results and 'performance' in result.results:
                perf = result.results['performance']
                perf['strategy_name'] = result.strategy_name
                perf['symbols'] = result.symbols
                perf['job_id'] = result.job_id
                performance_data.append(perf)
        
        if not performance_data:
            return {"error": "No performance data available"}
        
        # Create summary DataFrame
        df = pd.DataFrame(performance_data)
        
        # Calculate summary statistics
        summary = {
            'total_backtests': len(self.results),
            'successful_backtests': len(successful_results),
            'failed_backtests': len(self.results) - len(successful_results),
            'strategies_tested': len(set(r.strategy_name for r in self.results)),
            'symbols_tested': len(set(symbol for r in self.results for symbol in r.symbols)),
            'performance_summary': {
                'avg_total_return': df['total_return_pct'].mean() if 'total_return_pct' in df.columns else 0,
                'best_total_return': df['total_return_pct'].max() if 'total_return_pct' in df.columns else 0,
                'worst_total_return': df['total_return_pct'].min() if 'total_return_pct' in df.columns else 0,
                'avg_win_rate': df['win_rate_pct'].mean() if 'win_rate_pct' in df.columns else 0,
                'best_win_rate': df['win_rate_pct'].max() if 'win_rate_pct' in df.columns else 0,
                'avg_total_trades': df['total_trades'].mean() if 'total_trades' in df.columns else 0
            }
        }
        
        # Add top performers
        if 'total_return_pct' in df.columns:
            top_performers = df.nlargest(5, 'total_return_pct')[['strategy_name', 'symbols', 'total_return_pct', 'win_rate_pct']].to_dict('records')
            summary['top_performers'] = top_performers
        
        return summary
    
    def export_results(self, filepath: str, format: str = 'json'):
        """Export results to file
        
        Args:
            filepath: Output file path
            format: Export format ('json', 'csv', 'excel')
        """
        if not self.results:
            self.logger.warning("No results to export")
            return
        
        try:
            if format.lower() == 'json':
                # Convert results to JSON-serializable format
                export_data = []
                for result in self.results:
                    result_dict = {
                        'job_id': result.job_id,
                        'strategy_name': result.strategy_name,
                        'symbols': result.symbols,
                        'success': result.success,
                        'error_message': result.error_message,
                        'execution_time': result.execution_time,
                        'results': result.results
                    }
                    # Convert datetime objects to strings
                    if result_dict['results']:
                        self._convert_datetimes_to_strings(result_dict['results'])
                    export_data.append(result_dict)
                
                with open(filepath, 'w') as f:
                    json.dump(export_data, f, indent=2, default=str)
            
            elif format.lower() == 'csv':
                # Create DataFrame with key metrics
                data = []
                for result in self.results:
                    if result.success and result.results:
                        perf = result.results.get('performance', {})
                        row = {
                            'job_id': result.job_id,
                            'strategy_name': result.strategy_name,
                            'symbols': ','.join(result.symbols),
                            'success': result.success,
                            'execution_time': result.execution_time,
                            **perf
                        }
                        data.append(row)
                
                df = pd.DataFrame(data)
                df.to_csv(filepath, index=False)
            
            self.logger.info(f"Results exported to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error exporting results: {e}")
            raise
    
    def _convert_datetimes_to_strings(self, obj):
        """Recursively convert datetime objects to strings for JSON serialization"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self._convert_datetimes_to_strings(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                obj[i] = self._convert_datetimes_to_strings(item)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return obj
    
    def set_progress_callback(self, callback: Callable):
        """Set progress callback function
        
        Args:
            callback: Function to call with progress updates
        """
        self.progress_callback = callback
    
    def clear_jobs(self):
        """Clear all jobs from the queue"""
        self.jobs.clear()
        self.logger.info("Job queue cleared")
    
    def get_job_count(self) -> int:
        """Get number of jobs in queue
        
        Returns:
            Number of jobs
        """
        return len(self.jobs)
    
    def is_backtest_running(self) -> bool:
        """Check if matrix backtest is running
        
        Returns:
            True if running, False otherwise
        """
        return self.is_running