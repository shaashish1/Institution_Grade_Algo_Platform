"""
Backtest Engine
===============

Core backtesting engine for AlgoProject.
"""

import pandas as pd
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

from ..core.interfaces import MarketData, Signal
from ..strategies.base_strategy import BaseStrategy
from ..data.data_loader import DataLoader
from .backtest_context import BacktestContext
from .trade_executor import TradeExecutor


class BacktestEngine:
    """Core backtesting engine"""
    
    def __init__(self, data_loader: DataLoader, initial_capital: float = 100000.0,
                 commission: float = 0.001, slippage: float = 0.001):
        """Initialize backtest engine
        
        Args:
            data_loader: Data loader for historical data
            initial_capital: Starting capital
            commission: Commission rate (as decimal)
            slippage: Slippage factor (as decimal)
        """
        self.data_loader = data_loader
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.logger = logging.getLogger(__name__)
        
        # Backtest state
        self.context: Optional[BacktestContext] = None
        self.executor: Optional[TradeExecutor] = None
        self.strategy: Optional[BaseStrategy] = None
        
        # Results storage
        self.results: Dict[str, Any] = {}
        self.is_running = False
        
    def run_backtest(self, strategy: BaseStrategy, symbols: List[str], 
                    start_date: datetime, end_date: datetime,
                    timeframe: str = '1d') -> Dict[str, Any]:
        """Run a single backtest
        
        Args:
            strategy: Trading strategy to test
            symbols: List of symbols to trade
            start_date: Start date for backtest
            end_date: End date for backtest
            timeframe: Data timeframe
            
        Returns:
            Dictionary with backtest results
        """
        try:
            self.logger.info(f"Starting backtest: {strategy.name} on {symbols}")
            self.is_running = True
            
            # Initialize backtest components
            self.context = BacktestContext(self.initial_capital, self.commission)
            self.executor = TradeExecutor(self.context, self.slippage)
            self.strategy = strategy
            
            # Initialize strategy with context
            strategy.initialize(self.context)
            
            # Load historical data for all symbols
            historical_data = self._load_historical_data(symbols, start_date, end_date, timeframe)
            
            if not historical_data:
                raise ValueError("No historical data loaded")
            
            # Run the backtest
            self._execute_backtest(historical_data)
            
            # Calculate results
            results = self._calculate_results()
            
            self.logger.info(f"Backtest completed: {strategy.name}")
            return results
            
        except Exception as e:
            self.logger.error(f"Backtest failed: {e}")
            raise
        finally:
            self.is_running = False
    
    def run_matrix_backtest(self, strategies: List[BaseStrategy], symbols: List[str],
                          start_date: datetime, end_date: datetime,
                          timeframe: str = '1d', max_workers: int = 4) -> Dict[str, Dict[str, Any]]:
        """Run matrix backtest (multiple strategies on multiple symbols)
        
        Args:
            strategies: List of trading strategies
            symbols: List of symbols to trade
            start_date: Start date for backtest
            end_date: End date for backtest
            timeframe: Data timeframe
            max_workers: Maximum number of parallel workers
            
        Returns:
            Dictionary with results for each strategy-symbol combination
        """
        try:
            self.logger.info(f"Starting matrix backtest: {len(strategies)} strategies on {len(symbols)} symbols")
            
            results = {}
            
            # Create all combinations
            combinations = []
            for strategy in strategies:
                for symbol in symbols:
                    combinations.append((strategy, [symbol], start_date, end_date, timeframe))
            
            # Run backtests in parallel
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                
                for strategy, symbol_list, start, end, tf in combinations:
                    future = executor.submit(self._run_single_backtest, strategy, symbol_list, start, end, tf)
                    futures.append((future, strategy.name, symbol_list[0]))
                
                # Collect results
                for future, strategy_name, symbol in futures:
                    try:
                        result = future.result()
                        key = f"{strategy_name}_{symbol}"
                        results[key] = result
                        self.logger.info(f"Completed: {key}")
                    except Exception as e:
                        self.logger.error(f"Failed: {strategy_name}_{symbol} - {e}")
                        results[f"{strategy_name}_{symbol}"] = {"error": str(e)}
            
            self.logger.info(f"Matrix backtest completed: {len(results)} results")
            return results
            
        except Exception as e:
            self.logger.error(f"Matrix backtest failed: {e}")
            raise
    
    def _run_single_backtest(self, strategy: BaseStrategy, symbols: List[str],
                           start_date: datetime, end_date: datetime, timeframe: str) -> Dict[str, Any]:
        """Run a single backtest (used for parallel execution)
        
        Args:
            strategy: Trading strategy
            symbols: List of symbols
            start_date: Start date
            end_date: End date
            timeframe: Data timeframe
            
        Returns:
            Backtest results
        """
        # Create new instances for thread safety
        context = BacktestContext(self.initial_capital, self.commission)
        executor = TradeExecutor(context, self.slippage)
        
        # Clone strategy to avoid state conflicts
        strategy_copy = strategy.__class__(strategy.name, strategy.parameters.copy())
        strategy_copy.initialize(context)
        
        # Load historical data
        historical_data = self._load_historical_data(symbols, start_date, end_date, timeframe)
        
        if not historical_data:
            raise ValueError("No historical data loaded")
        
        # Execute backtest
        self._execute_backtest_with_context(historical_data, strategy_copy, context, executor)
        
        # Calculate and return results
        return self._calculate_results_with_context(context, executor, strategy_copy)
    
    def _load_historical_data(self, symbols: List[str], start_date: datetime,
                            end_date: datetime, timeframe: str) -> Dict[str, pd.DataFrame]:
        """Load historical data for symbols
        
        Args:
            symbols: List of symbols
            start_date: Start date
            end_date: End date
            timeframe: Data timeframe
            
        Returns:
            Dictionary mapping symbols to DataFrames
        """
        historical_data = {}
        
        for symbol in symbols:
            try:
                df = self.data_loader.get_historical_data(
                    symbol=symbol,
                    timeframe=timeframe,
                    start_date=start_date,
                    end_date=end_date,
                    limit=10000
                )
                
                if not df.empty:
                    historical_data[symbol] = df
                    self.logger.info(f"Loaded {len(df)} bars for {symbol}")
                else:
                    self.logger.warning(f"No data loaded for {symbol}")
                    
            except Exception as e:
                self.logger.error(f"Error loading data for {symbol}: {e}")
        
        return historical_data
    
    def _execute_backtest(self, historical_data: Dict[str, pd.DataFrame]):
        """Execute the backtest with loaded data
        
        Args:
            historical_data: Historical data for all symbols
        """
        self._execute_backtest_with_context(historical_data, self.strategy, self.context, self.executor)
    
    def _execute_backtest_with_context(self, historical_data: Dict[str, pd.DataFrame],
                                     strategy: BaseStrategy, context: BacktestContext,
                                     executor: TradeExecutor):
        """Execute backtest with specific context
        
        Args:
            historical_data: Historical data
            strategy: Trading strategy
            context: Backtest context
            executor: Trade executor
        """
        # Create unified timeline
        all_timestamps = set()
        for df in historical_data.values():
            all_timestamps.update(df.index)
        
        sorted_timestamps = sorted(all_timestamps)
        
        self.logger.info(f"Processing {len(sorted_timestamps)} time periods")
        
        # Process each timestamp
        for i, timestamp in enumerate(sorted_timestamps):
            # Update market data for all symbols at this timestamp
            for symbol, df in historical_data.items():
                if timestamp in df.index:
                    row = df.loc[timestamp]
                    
                    market_data = MarketData(
                        symbol=symbol,
                        timestamp=timestamp,
                        open=row['open'],
                        high=row['high'],
                        low=row['low'],
                        close=row['close'],
                        volume=row['volume'],
                        exchange="backtest"
                    )
                    
                    # Update context with new data
                    context.update_market_data(market_data)
                    
                    # Process market data through executor
                    executor.process_market_data(market_data)
            
            # Generate signals from strategy
            try:
                signals = []
                for symbol in historical_data.keys():
                    if symbol in context.current_data:
                        symbol_signals = strategy.next(context.current_data[symbol])
                        if symbol_signals:
                            signals.extend(symbol_signals)
                
                # Execute signals
                for signal in signals:
                    executor.execute_signal(signal)
                    
            except Exception as e:
                self.logger.error(f"Error processing timestamp {timestamp}: {e}")
            
            # Log progress periodically
            if i % 1000 == 0 and i > 0:
                progress = (i / len(sorted_timestamps)) * 100
                self.logger.info(f"Progress: {progress:.1f}% ({i}/{len(sorted_timestamps)})")
        
        self.logger.info("Backtest execution completed")
    
    def _calculate_results(self) -> Dict[str, Any]:
        """Calculate backtest results
        
        Returns:
            Dictionary with comprehensive results
        """
        return self._calculate_results_with_context(self.context, self.executor, self.strategy)
    
    def _calculate_results_with_context(self, context: BacktestContext, 
                                      executor: TradeExecutor, strategy: BaseStrategy) -> Dict[str, Any]:
        """Calculate results with specific context
        
        Args:
            context: Backtest context
            executor: Trade executor
            strategy: Trading strategy
            
        Returns:
            Dictionary with results
        """
        # Get basic performance summary
        performance = context.get_performance_summary()
        
        # Get execution summary
        execution = executor.get_execution_summary()
        
        # Get equity curve and trade log
        equity_curve = context.get_equity_curve_df()
        trade_log = context.get_trade_log_df()
        
        # Calculate additional metrics
        additional_metrics = self._calculate_additional_metrics(equity_curve, trade_log)
        
        # Combine all results
        results = {
            'strategy_name': strategy.name,
            'strategy_parameters': strategy.parameters,
            'performance': performance,
            'execution': execution,
            'metrics': additional_metrics,
            'equity_curve': equity_curve.to_dict('records') if not equity_curve.empty else [],
            'trade_log': trade_log.to_dict('records') if not trade_log.empty else [],
            'final_portfolio': context.portfolio.get_portfolio_summary()
        }
        
        return results
    
    def _calculate_additional_metrics(self, equity_curve: pd.DataFrame, 
                                    trade_log: pd.DataFrame) -> Dict[str, float]:
        """Calculate additional performance metrics
        
        Args:
            equity_curve: Equity curve DataFrame
            trade_log: Trade log DataFrame
            
        Returns:
            Dictionary with additional metrics
        """
        metrics = {}
        
        if equity_curve.empty:
            return metrics
        
        try:
            # Calculate returns
            returns = equity_curve['portfolio_value'].pct_change().dropna()
            
            if len(returns) > 0:
                # Basic return metrics
                metrics['total_return'] = (equity_curve['portfolio_value'].iloc[-1] / equity_curve['portfolio_value'].iloc[0]) - 1
                metrics['annualized_return'] = (1 + metrics['total_return']) ** (252 / len(returns)) - 1
                metrics['volatility'] = returns.std() * (252 ** 0.5)
                
                # Risk metrics
                if metrics['volatility'] > 0:
                    metrics['sharpe_ratio'] = metrics['annualized_return'] / metrics['volatility']
                else:
                    metrics['sharpe_ratio'] = 0
                
                # Drawdown metrics
                peak = equity_curve['portfolio_value'].expanding().max()
                drawdown = (equity_curve['portfolio_value'] - peak) / peak
                metrics['max_drawdown'] = drawdown.min()
                metrics['avg_drawdown'] = drawdown[drawdown < 0].mean() if len(drawdown[drawdown < 0]) > 0 else 0
                
                # Trade metrics
                if not trade_log.empty:
                    # Calculate trade returns
                    buy_trades = trade_log[trade_log['action'] == 'buy']
                    sell_trades = trade_log[trade_log['action'] == 'sell']
                    
                    if len(buy_trades) > 0 and len(sell_trades) > 0:
                        metrics['avg_trade_duration'] = (sell_trades['timestamp'].mean() - buy_trades['timestamp'].mean()).total_seconds() / 3600  # hours
                        metrics['profit_factor'] = abs(returns[returns > 0].sum()) / abs(returns[returns < 0].sum()) if len(returns[returns < 0]) > 0 else float('inf')
                
        except Exception as e:
            self.logger.error(f"Error calculating additional metrics: {e}")
        
        return metrics
    
    def get_results(self) -> Dict[str, Any]:
        """Get the latest backtest results
        
        Returns:
            Dictionary with results
        """
        return self.results
    
    def is_backtest_running(self) -> bool:
        """Check if backtest is currently running
        
        Returns:
            True if running, False otherwise
        """
        return self.is_running
    
    def stop_backtest(self):
        """Stop the current backtest"""
        self.is_running = False
        self.logger.info("Backtest stop requested")