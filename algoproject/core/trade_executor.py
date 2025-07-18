"""
Trade Executor
==============

Handles order placement, management, and execution tracking.
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import logging

from .interfaces import Signal


class OrderStatus(Enum):
    PENDING = "pending"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class Order:
    """Represents a trading order"""
    
    def __init__(self, symbol: str, side: str, quantity: float, 
                 order_type: OrderType = OrderType.MARKET, price: float = None,
                 stop_price: float = None, time_in_force: str = "GTC"):
        self.id = str(uuid.uuid4())
        self.symbol = symbol
        self.side = side  # 'buy' or 'sell'
        self.quantity = quantity
        self.order_type = order_type
        self.price = price
        self.stop_price = stop_price
        self.time_in_force = time_in_force
        self.status = OrderStatus.PENDING
        self.filled_quantity = 0.0
        self.avg_fill_price = 0.0
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.fills = []
        self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert order to dictionary"""
        return {
            'id': self.id,
            'symbol': self.symbol,
            'side': self.side,
            'quantity': self.quantity,
            'order_type': self.order_type.value,
            'price': self.price,
            'stop_price': self.stop_price,
            'time_in_force': self.time_in_force,
            'status': self.status.value,
            'filled_quantity': self.filled_quantity,
            'avg_fill_price': self.avg_fill_price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'fills': self.fills,
            'metadata': self.metadata
        }


class TradeExecutor:
    """Handles trade execution and order management"""
    
    def __init__(self, risk_manager=None):
        self.logger = logging.getLogger(__name__)
        self.risk_manager = risk_manager
        self.orders: Dict[str, Order] = {}
        self.positions: Dict[str, float] = {}
        self.execution_handlers = {}
        self.order_callbacks = []
    
    def register_execution_handler(self, asset_type: str, handler):
        """Register execution handler for specific asset type"""
        self.execution_handlers[asset_type] = handler
        self.logger.info(f"Registered execution handler for {asset_type}")
    
    def add_order_callback(self, callback):
        """Add callback for order status updates"""
        self.order_callbacks.append(callback)
    
    def create_order_from_signal(self, signal: Signal, order_type: OrderType = OrderType.MARKET,
                                stop_loss: float = None, take_profit: float = None) -> Optional[Order]:
        """Create order from trading signal"""
        try:
            # Risk management check
            if self.risk_manager:
                if not self.risk_manager.validate_order(signal, self.positions):
                    self.logger.warning(f"Order rejected by risk manager: {signal.symbol}")
                    return None
            
            # Create main order
            order = Order(
                symbol=signal.symbol,
                side=signal.action,
                quantity=signal.quantity,
                order_type=order_type,
                price=signal.price
            )
            
            # Add metadata from signal
            order.metadata.update(signal.metadata or {})
            order.metadata['signal_confidence'] = signal.confidence
            order.metadata['signal_timestamp'] = signal.timestamp.isoformat() if signal.timestamp else None
            
            # Store order
            self.orders[order.id] = order
            
            self.logger.info(f"Created order {order.id}: {signal.action} {signal.quantity} {signal.symbol}")
            
            # Create stop loss and take profit orders if specified
            if stop_loss and signal.action == 'buy':
                self._create_stop_loss_order(order, stop_loss)
            elif stop_loss and signal.action == 'sell':
                self._create_stop_loss_order(order, stop_loss)
            
            if take_profit:
                self._create_take_profit_order(order, take_profit)
            
            return order
            
        except Exception as e:
            self.logger.error(f"Error creating order from signal: {e}")
            return None
    
    def submit_order(self, order: Order) -> bool:
        """Submit order for execution"""
        try:
            # Determine asset type from symbol
            asset_type = self._get_asset_type(order.symbol)
            
            if asset_type not in self.execution_handlers:
                self.logger.error(f"No execution handler for asset type: {asset_type}")
                order.status = OrderStatus.REJECTED
                self._notify_order_update(order)
                return False
            
            # Submit to appropriate handler
            handler = self.execution_handlers[asset_type]
            success = handler.submit_order(order)
            
            if success:
                self.logger.info(f"Order {order.id} submitted successfully")
            else:
                self.logger.error(f"Failed to submit order {order.id}")
                order.status = OrderStatus.REJECTED
                self._notify_order_update(order)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error submitting order {order.id}: {e}")
            order.status = OrderStatus.REJECTED
            self._notify_order_update(order)
            return False
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        if order_id not in self.orders:
            self.logger.error(f"Order {order_id} not found")
            return False
        
        order = self.orders[order_id]
        
        if order.status in [OrderStatus.FILLED, OrderStatus.CANCELLED]:
            self.logger.warning(f"Cannot cancel order {order_id} with status {order.status}")
            return False
        
        try:
            # Get appropriate handler
            asset_type = self._get_asset_type(order.symbol)
            if asset_type in self.execution_handlers:
                handler = self.execution_handlers[asset_type]
                success = handler.cancel_order(order)
                
                if success:
                    order.status = OrderStatus.CANCELLED
                    order.updated_at = datetime.now()
                    self._notify_order_update(order)
                    self.logger.info(f"Order {order_id} cancelled")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error cancelling order {order_id}: {e}")
            return False
    
    def update_order_status(self, order_id: str, status: OrderStatus, 
                           filled_quantity: float = 0, fill_price: float = 0,
                           fill_info: Dict = None):
        """Update order status (called by execution handlers)"""
        if order_id not in self.orders:
            self.logger.error(f"Order {order_id} not found for status update")
            return
        
        order = self.orders[order_id]
        order.status = status
        order.updated_at = datetime.now()
        
        if filled_quantity > 0:
            # Record fill
            fill = {
                'quantity': filled_quantity,
                'price': fill_price,
                'timestamp': datetime.now().isoformat(),
                'info': fill_info or {}
            }
            order.fills.append(fill)
            
            # Update filled quantity and average price
            total_filled = order.filled_quantity + filled_quantity
            if total_filled > 0:
                order.avg_fill_price = (
                    (order.avg_fill_price * order.filled_quantity + fill_price * filled_quantity) / total_filled
                )
            order.filled_quantity = total_filled
            
            # Update position
            if order.side == 'buy':
                self.positions[order.symbol] = self.positions.get(order.symbol, 0) + filled_quantity
            else:
                self.positions[order.symbol] = self.positions.get(order.symbol, 0) - filled_quantity
            
            self.logger.info(f"Order {order_id} filled: {filled_quantity} @ {fill_price}")
        
        self._notify_order_update(order)
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        return self.orders.get(order_id)
    
    def get_orders(self, symbol: str = None, status: OrderStatus = None) -> List[Order]:
        """Get orders with optional filtering"""
        orders = list(self.orders.values())
        
        if symbol:
            orders = [o for o in orders if o.symbol == symbol]
        
        if status:
            orders = [o for o in orders if o.status == status]
        
        return orders
    
    def get_position(self, symbol: str) -> float:
        """Get current position for symbol"""
        return self.positions.get(symbol, 0.0)
    
    def get_all_positions(self) -> Dict[str, float]:
        """Get all current positions"""
        return self.positions.copy()
    
    def _create_stop_loss_order(self, parent_order: Order, stop_loss_price: float):
        """Create stop loss order"""
        stop_side = 'sell' if parent_order.side == 'buy' else 'buy'
        
        stop_order = Order(
            symbol=parent_order.symbol,
            side=stop_side,
            quantity=parent_order.quantity,
            order_type=OrderType.STOP,
            stop_price=stop_loss_price
        )
        
        stop_order.metadata['parent_order_id'] = parent_order.id
        stop_order.metadata['order_purpose'] = 'stop_loss'
        
        self.orders[stop_order.id] = stop_order
        self.logger.info(f"Created stop loss order {stop_order.id} for {parent_order.id}")
    
    def _create_take_profit_order(self, parent_order: Order, take_profit_price: float):
        """Create take profit order"""
        tp_side = 'sell' if parent_order.side == 'buy' else 'buy'
        
        tp_order = Order(
            symbol=parent_order.symbol,
            side=tp_side,
            quantity=parent_order.quantity,
            order_type=OrderType.LIMIT,
            price=take_profit_price
        )
        
        tp_order.metadata['parent_order_id'] = parent_order.id
        tp_order.metadata['order_purpose'] = 'take_profit'
        
        self.orders[tp_order.id] = tp_order
        self.logger.info(f"Created take profit order {tp_order.id} for {parent_order.id}")
    
    def _get_asset_type(self, symbol: str) -> str:
        """Determine asset type from symbol"""
        # Simple heuristic - can be enhanced
        if any(crypto in symbol.upper() for crypto in ['BTC', 'ETH', 'USDT', 'USDC']):
            return 'crypto'
        else:
            return 'stocks'
    
    def _notify_order_update(self, order: Order):
        """Notify callbacks of order updates"""
        for callback in self.order_callbacks:
            try:
                callback(order)
            except Exception as e:
                self.logger.error(f"Error in order callback: {e}")
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution summary statistics"""
        total_orders = len(self.orders)
        filled_orders = len([o for o in self.orders.values() if o.status == OrderStatus.FILLED])
        pending_orders = len([o for o in self.orders.values() if o.status == OrderStatus.PENDING])
        cancelled_orders = len([o for o in self.orders.values() if o.status == OrderStatus.CANCELLED])
        
        return {
            'total_orders': total_orders,
            'filled_orders': filled_orders,
            'pending_orders': pending_orders,
            'cancelled_orders': cancelled_orders,
            'fill_rate': (filled_orders / total_orders * 100) if total_orders > 0 else 0,
            'active_positions': len([p for p in self.positions.values() if p != 0]),
            'total_position_value': sum(abs(p) for p in self.positions.values())
        }