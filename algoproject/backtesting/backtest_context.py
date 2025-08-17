"""
Backtest Context
===============

Context object that provides backtesting environment for strategies.
"""

import pandas as pd
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict

from ..core.interfaces import MarketData, Signal, Position
from .portfolio import Portfolio


class BacktestContext:
    """Backtesting context for strategies"""
    
    def __init__(self, initial_capital: float = 100000.0, commission: float = 0.001):
        """Initialize backtest context
        
        Args:
            initial_capital: Starting capital for backtesting
            commission: Commission rate (as decimal, e.g., 0.001 = 0.1%)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.logger = logging.getLogger(__name__)
        
        # Portfolio management
        self.portfolio = Portfolio(initial_capital)
        
        # Current market data
        self.current_data: Dict[str, MarketData] = {}
        self.current_timestamp: Optional[datetime] = None
        
        # Historical data storage
        self.historical_data: Dict[str, List[MarketData]] = defaultdict(list)
        
        # Performance tracking
        self.equity_curve: List[Dict[str, Any]] = []
        self.trade_log: List[Dict[str, Any]] = []
        self.daily_returns: List[float] = []
        
        # Strategy state
        self.strategy_states: Dict[str, Any] = {}
        
        # Execution tracking
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_commission_paid = 0.0
        
    @property
    def portfolio_value(self) -> float:
        """Get current portfolio value"""
        return self.portfolio.get_total_value()
    
    @property
    def cash(self) -> float:
        """Get current cash balance"""
        return self.portfolio.cash
    
    @property
    def positions(self) -> Dict[str, Position]:
        """Get current positions"""
        return self.portfolio.positions
    
    def get_position(self, symbol: str) -> float:
        """Get position quantity for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Position quantity (positive for long, negative for short)
        """
        return self.portfolio.get_position_quantity(symbol)
    
    def get_position_value(self, symbol: str) -> float:
        """Get position value for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Current position value
        """
        return self.portfolio.get_position_value(symbol)
    
    def update_market_data(self, data: MarketData):
        """Update current market data
        
        Args:
            data: New market data
        """
        symbol = data.symbol
        self.current_data[symbol] = data
        self.current_timestamp = data.timestamp
        
        # Store historical data
        self.historical_data[symbol].append(data)
        
        # Update portfolio with current prices
        self.portfolio.update_market_price(symbol, data.close)
    
    def get_historical_data(self, symbol: str, periods: int = None) -> List[MarketData]:
        """Get historical data for a symbol
        
        Args:
            symbol: Trading symbol
            periods: Number of periods to return (None for all)
            
        Returns:
            List of historical MarketData objects
        """
        data = self.historical_data.get(symbol, [])
        if periods is not None:
            return data[-periods:]
        return data
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Current price or None if not available
        """
        if symbol in self.current_data:
            return self.current_data[symbol].close
        return None
    
    def execute_signal(self, signal: Signal) -> bool:
        """Execute a trading signal
        
        Args:
            signal: Trading signal to execute
            
        Returns:
            True if execution successful, False otherwise
        """
        try:
            symbol = signal.symbol
            action = signal.action.lower()
            quantity = abs(signal.quantity)
            price = signal.price or self.get_current_price(symbol)
            
            if price is None:
                self.logger.error(f"No price available for {symbol}")
                return False
            
            # Calculate commission
            trade_value = quantity * price
            commission = trade_value * self.commission
            
            success = False
            
            if action == 'buy':
                success = self.portfolio.buy(symbol, quantity, price, commission)
            elif action == 'sell':
                success = self.portfolio.sell(symbol, quantity, price, commission)
            
            if success:
                # Log the trade
                self._log_trade(signal, price, commission)
                self.total_commission_paid += commission
                self.total_trades += 1
                
                # Update performance tracking
                self._update_performance_tracking()
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error executing signal: {e}")
            return False
    
    def _log_trade(self, signal: Signal, executed_price: float, commission: float):
        """Log a trade for analysis
        
        Args:
            signal: Original trading signal
            executed_price: Actual execution price
            commission: Commission paid
        """
        trade_record = {
            'timestamp': self.current_timestamp,
            'symbol': signal.symbol,
            'action': signal.action,
            'quantity': signal.quantity,
            'signal_price': signal.price,
            'executed_price': executed_price,
            'commission': commission,
            'portfolio_value': self.portfolio_value,
            'cash': self.cash,
            'confidence': signal.confidence,
            'metadata': signal.metadata
        }
        
        self.trade_log.append(trade_record)
    
    def _update_performance_tracking(self):
        """Update performance tracking metrics"""
        # Record equity curve point
        equity_point = {
            'timestamp': self.current_timestamp,
            'portfolio_value': self.portfolio_value,
            'cash': self.cash,
            'positions_value': self.portfolio_value - self.cash,
            'total_trades': self.total_trades,
            'commission_paid': self.total_commission_paid
        }
        
        self.equity_curve.append(equity_point)
        
        # Calculate daily return if we have previous data
        if len(self.equity_curve) > 1:
            prev_value = self.equity_curve[-2]['portfolio_value']
            current_value = self.portfolio_value
            daily_return = (current_value - prev_value) / prev_value
            self.daily_returns.append(daily_return)
    
    def get_equity_curve_df(self) -> pd.DataFrame:
        """Get equity curve as DataFrame
        
        Returns:
            DataFrame with equity curve data
        """
        if not self.equity_curve:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.equity_curve)
        df.set_index('timestamp', inplace=True)
        return df
    
    def get_trade_log_df(self) -> pd.DataFrame:
        """Get trade log as DataFrame
        
        Returns:
            DataFrame with trade log data
        """
        if not self.trade_log:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.trade_log)
        df.set_index('timestamp', inplace=True)
        return df
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.equity_curve:
            return {}
        
        final_value = self.portfolio_value
        total_return = (final_value - self.initial_capital) / self.initial_capital
        
        # Calculate win rate
        winning_trades = 0
        losing_trades = 0
        
        for i in range(1, len(self.equity_curve)):
            prev_value = self.equity_curve[i-1]['portfolio_value']
            curr_value = self.equity_curve[i]['portfolio_value']
            
            if curr_value > prev_value:
                winning_trades += 1
            elif curr_value < prev_value:
                losing_trades += 1
        
        total_trades = winning_trades + losing_trades
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        return {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'total_return_pct': total_return * 100,
            'total_trades': self.total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'win_rate_pct': win_rate * 100,
            'total_commission': self.total_commission_paid,
            'commission_pct': (self.total_commission_paid / self.initial_capital) * 100
        }
    
    def reset(self):
        """Reset the backtest context"""
        self.portfolio = Portfolio(self.initial_capital)
        self.current_data.clear()
        self.current_timestamp = None
        self.historical_data.clear()
        self.equity_curve.clear()
        self.trade_log.clear()
        self.daily_returns.clear()
        self.strategy_states.clear()
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_commission_paid = 0.0
    
    def set_strategy_state(self, key: str, value: Any):
        """Set strategy-specific state
        
        Args:
            key: State key
            value: State value
        """
        self.strategy_states[key] = value
    
    def get_strategy_state(self, key: str, default: Any = None) -> Any:
        """Get strategy-specific state
        
        Args:
            key: State key
            default: Default value if key not found
            
        Returns:
            State value or default
        """
        return self.strategy_states.get(key, default)