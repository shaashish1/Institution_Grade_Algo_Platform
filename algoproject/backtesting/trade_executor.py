"""
Trade Executor
==============

Handles trade execution for backtesting and live trading.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

from ..core.interfaces import Signal, MarketData
from ..core.risk_manager import RiskManager
from .backtest_context import BacktestContext


class ExecutionMode(Enum):
    """Trade execution modes"""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(Enum):
    """Order status enumeration"""
    PENDING = "pending"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class Order:
    """Represents a trading order"""
    
    def __init__(self, order_id: str, symbol: str, action: str, quantity: float,
                 order_type: ExecutionMode, price: Optional[float] = None,
                 stop_price: Optional[float] = None, metadata: Optional[Dict] = None):
        self.order_id = order_id
        self.symbol = symbol
        self.action = action.lower()
        self.quantity = quantity
        self.order_type = order_type
        self.price = price
        self.stop_price = stop_price
        self.metadata = metadata or {}
        
        self.status = OrderStatus.PENDING
        self.filled_quantity = 0.0
        self.avg_fill_price = 0.0
        self.created_at = datetime.now()
        self.filled_at: Optional[datetime] = None
        self.commission = 0.0


class TradeExecutor:
    """Handles trade execution logic with integrated risk management"""
    
    def __init__(self, context: BacktestContext, slippage: float = 0.001, 
                 risk_manager: Optional[RiskManager] = None):
        """Initialize trade executor
        
        Args:
            context: Backtest context
            slippage: Slippage factor (as decimal)
            risk_manager: Risk manager instance (optional)
        """
        self.context = context
        self.slippage = slippage
        self.logger = logging.getLogger(__name__)
        
        # Risk management
        self.risk_manager = risk_manager or RiskManager()
        
        # Order management
        self.pending_orders: Dict[str, Order] = {}
        self.filled_orders: List[Order] = []
        self.order_counter = 0
        
        # Execution settings (fallback if no risk manager)
        self.max_position_size = 0.1  # Max 10% of portfolio per position
        self.max_total_exposure = 0.95  # Max 95% total exposure
    
    def execute_signal(self, signal: Signal) -> Optional[str]:
        """Execute a trading signal
        
        Args:
            signal: Trading signal to execute
            
        Returns:
            Order ID if order created, None otherwise
        """
        try:
            # Validate signal
            if not self._validate_signal(signal):
                return None
            
            # Create order
            order = self._create_order_from_signal(signal)
            
            # Execute order immediately for market orders in backtesting
            if order.order_type == ExecutionMode.MARKET:
                self._execute_market_order(order)
            else:
                # Add to pending orders for limit/stop orders
                self.pending_orders[order.order_id] = order
            
            return order.order_id
            
        except Exception as e:
            self.logger.error(f"Error executing signal: {e}")
            return None
    
    def process_market_data(self, data: MarketData):
        """Process market data and check pending orders
        
        Args:
            data: Market data update
        """
        symbol = data.symbol
        
        # Check pending orders for this symbol
        orders_to_remove = []
        
        for order_id, order in self.pending_orders.items():
            if order.symbol == symbol:
                if self._should_execute_order(order, data):
                    self._execute_order(order, data)
                    orders_to_remove.append(order_id)
        
        # Remove executed orders from pending
        for order_id in orders_to_remove:
            del self.pending_orders[order_id]
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel a pending order
        
        Args:
            order_id: Order ID to cancel
            
        Returns:
            True if order cancelled, False otherwise
        """
        if order_id in self.pending_orders:
            order = self.pending_orders[order_id]
            order.status = OrderStatus.CANCELLED
            del self.pending_orders[order_id]
            self.logger.info(f"Cancelled order {order_id}")
            return True
        
        return False
    
    def get_pending_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """Get pending orders
        
        Args:
            symbol: Filter by symbol (optional)
            
        Returns:
            List of pending orders
        """
        orders = list(self.pending_orders.values())
        
        if symbol:
            orders = [order for order in orders if order.symbol == symbol]
        
        return orders
    
    def get_filled_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """Get filled orders
        
        Args:
            symbol: Filter by symbol (optional)
            
        Returns:
            List of filled orders
        """
        orders = self.filled_orders.copy()
        
        if symbol:
            orders = [order for order in orders if order.symbol == symbol]
        
        return orders
    
    def _validate_signal(self, signal: Signal) -> bool:
        """Validate a trading signal using risk management
        
        Args:
            signal: Signal to validate
            
        Returns:
            True if signal is valid, False otherwise
        """
        try:
            # Use risk manager for validation if available
            if self.risk_manager:
                is_valid, reason, adjusted_quantity = self.risk_manager.validate_signal(
                    signal=signal,
                    portfolio_value=self.context.portfolio_value,
                    current_positions=self.context.positions,
                    market_data=self.context.current_data
                )
                
                if not is_valid:
                    self.logger.warning(f"Signal rejected by risk manager: {reason}")
                    return False
                
                # Update signal quantity if adjusted
                if adjusted_quantity != signal.quantity:
                    self.logger.info(f"Signal quantity adjusted by risk manager: {signal.quantity} -> {adjusted_quantity}")
                    signal.quantity = adjusted_quantity
                
                return True
            
            # Fallback validation if no risk manager
            return self._basic_signal_validation(signal)
            
        except Exception as e:
            self.logger.error(f"Error validating signal: {e}")
            return False
    
    def _basic_signal_validation(self, signal: Signal) -> bool:
        """Basic signal validation without risk manager"""
        # Check basic signal properties
        if not signal.symbol or not signal.action or signal.quantity <= 0:
            self.logger.error("Invalid signal: missing required fields")
            return False
        
        # Check if we have current market data
        if signal.symbol not in self.context.current_data:
            self.logger.error(f"No market data available for {signal.symbol}")
            return False
        
        # Check position size limits
        current_price = self.context.get_current_price(signal.symbol)
        if not current_price:
            self.logger.error(f"No current price for {signal.symbol}")
            return False
        
        position_value = signal.quantity * current_price
        max_position_value = self.context.portfolio_value * self.max_position_size
        
        if position_value > max_position_value:
            self.logger.warning(f"Position size too large: {position_value} > {max_position_value}")
            return False
        
        # Check total exposure
        total_positions_value = self.context.portfolio.get_total_positions_value()
        max_total_value = self.context.portfolio_value * self.max_total_exposure
        
        if signal.action.lower() == 'buy' and (total_positions_value + position_value) > max_total_value:
            self.logger.warning(f"Total exposure too high")
            return False
        
        return True
    
    def _create_order_from_signal(self, signal: Signal) -> Order:
        """Create an order from a trading signal
        
        Args:
            signal: Trading signal
            
        Returns:
            Order object
        """
        self.order_counter += 1
        order_id = f"ORDER_{self.order_counter:06d}"
        
        # Determine order type
        order_type = ExecutionMode.MARKET
        if signal.price and signal.price != self.context.get_current_price(signal.symbol):
            order_type = ExecutionMode.LIMIT
        
        return Order(
            order_id=order_id,
            symbol=signal.symbol,
            action=signal.action,
            quantity=signal.quantity,
            order_type=order_type,
            price=signal.price,
            metadata=signal.metadata
        )
    
    def _execute_market_order(self, order: Order):
        """Execute a market order immediately
        
        Args:
            order: Order to execute
        """
        current_price = self.context.get_current_price(order.symbol)
        if not current_price:
            order.status = OrderStatus.REJECTED
            return
        
        # Apply slippage
        if order.action == 'buy':
            execution_price = current_price * (1 + self.slippage)
        else:
            execution_price = current_price * (1 - self.slippage)
        
        # Create signal for execution
        execution_signal = Signal(
            symbol=order.symbol,
            action=order.action,
            quantity=order.quantity,
            price=execution_price,
            confidence=1.0,
            metadata=order.metadata
        )
        
        # Execute through context
        if self.context.execute_signal(execution_signal):
            order.status = OrderStatus.FILLED
            order.filled_quantity = order.quantity
            order.avg_fill_price = execution_price
            order.filled_at = datetime.now()
            order.commission = (order.quantity * execution_price) * self.context.commission
            
            self.filled_orders.append(order)
            self.logger.info(f"Executed market order {order.order_id}: {order.action} {order.quantity} {order.symbol} at {execution_price}")
        else:
            order.status = OrderStatus.REJECTED
            self.logger.error(f"Failed to execute market order {order.order_id}")
    
    def _should_execute_order(self, order: Order, data: MarketData) -> bool:
        """Check if an order should be executed based on market data
        
        Args:
            order: Order to check
            data: Current market data
            
        Returns:
            True if order should be executed, False otherwise
        """
        current_price = data.close
        
        if order.order_type == ExecutionMode.LIMIT:
            if order.action == 'buy' and current_price <= order.price:
                return True
            elif order.action == 'sell' and current_price >= order.price:
                return True
        
        elif order.order_type == ExecutionMode.STOP:
            if order.action == 'buy' and current_price >= order.stop_price:
                return True
            elif order.action == 'sell' and current_price <= order.stop_price:
                return True
        
        return False
    
    def _execute_order(self, order: Order, data: MarketData):
        """Execute a pending order
        
        Args:
            order: Order to execute
            data: Market data for execution
        """
        execution_price = order.price if order.order_type == ExecutionMode.LIMIT else data.close
        
        # Apply slippage for stop orders
        if order.order_type == ExecutionMode.STOP:
            if order.action == 'buy':
                execution_price = execution_price * (1 + self.slippage)
            else:
                execution_price = execution_price * (1 - self.slippage)
        
        # Create signal for execution
        execution_signal = Signal(
            symbol=order.symbol,
            action=order.action,
            quantity=order.quantity,
            price=execution_price,
            confidence=1.0,
            metadata=order.metadata
        )
        
        # Execute through context
        if self.context.execute_signal(execution_signal):
            order.status = OrderStatus.FILLED
            order.filled_quantity = order.quantity
            order.avg_fill_price = execution_price
            order.filled_at = datetime.now()
            order.commission = (order.quantity * execution_price) * self.context.commission
            
            self.filled_orders.append(order)
            self.logger.info(f"Executed {order.order_type.value} order {order.order_id}: {order.action} {order.quantity} {order.symbol} at {execution_price}")
        else:
            order.status = OrderStatus.REJECTED
            self.logger.error(f"Failed to execute order {order.order_id}")
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution summary statistics
        
        Returns:
            Dictionary with execution statistics
        """
        total_orders = len(self.filled_orders) + len(self.pending_orders)
        filled_orders = len(self.filled_orders)
        pending_orders = len(self.pending_orders)
        
        total_commission = sum(order.commission for order in self.filled_orders)
        
        return {
            'total_orders': total_orders,
            'filled_orders': filled_orders,
            'pending_orders': pending_orders,
            'fill_rate': filled_orders / total_orders if total_orders > 0 else 0,
            'total_commission': total_commission,
            'avg_commission_per_trade': total_commission / filled_orders if filled_orders > 0 else 0
        }