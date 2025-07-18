"""
Demo Trading Engine
==================

Simulated trading engine using live data feeds for paper trading.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
import time
from dataclasses import dataclass, field
from enum import Enum

from ..core.interfaces import Signal, MarketData, Position, ITradingEngine
from ..core.risk_manager import RiskManager
from ..strategies.base_strategy import BaseStrategy
from ..data.data_loader import DataLoader
from ..data.streaming.stream_manager import StreamManager
from ..backtesting.portfolio import Portfolio


class DemoOrderStatus(Enum):
    """Demo order status"""
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class DemoOrder:
    """Demo trading order"""
    order_id: str
    symbol: str
    action: str
    quantity: float
    order_type: str
    price: Optional[float] = None
    stop_price: Optional[float] = None
    status: DemoOrderStatus = DemoOrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    filled_at: Optional[datetime] = None
    filled_price: Optional[float] = None
    commission: float = 0.0


class DemoTradingEngine(ITradingEngine):
    """Demo trading engine with simulated execution"""
    
    def __init__(self, data_loader: DataLoader, stream_manager: StreamManager,
                 initial_capital: float = 100000.0, commission: float = 0.001,
                 slippage: float = 0.0005):
        """Initialize demo trading engine
        
        Args:
            data_loader: Data loader for historical data
            stream_manager: Stream manager for live data
            initial_capital: Starting capital
            commission: Commission rate
            slippage: Slippage factor
        """
        self.data_loader = data_loader
        self.stream_manager = stream_manager
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.logger = logging.getLogger(__name__)
        
        # Trading state
        self.is_running = False
        self.start_time: Optional[datetime] = None
        
        # Portfolio and risk management
        self.portfolio = Portfolio(initial_capital)
        self.risk_manager = RiskManager()
        
        # Strategy management
        self.strategies: Dict[str, BaseStrategy] = {}
        self.active_strategies: List[str] = []
        
        # Order management
        self.orders: Dict[str, DemoOrder] = {}
        self.order_counter = 0
        
        # Market data
        self.current_data: Dict[str, MarketData] = {}
        self.subscribed_symbols: set = set()
        
        # Performance tracking
        self.trades_executed = 0
        self.total_pnl = 0.0
        self.daily_pnl = 0.0
        self.peak_value = initial_capital
        self.current_drawdown = 0.0
        
        # Callbacks
        self.on_trade_callback: Optional[Callable] = None
        self.on_order_callback: Optional[Callable] = None
        self.on_performance_callback: Optional[Callable] = None
        
    async def start(self) -> None:
        """Start the demo trading engine"""
        try:
            if self.is_running:
                self.logger.warning("Demo trading engine already running")
                return
            
            self.logger.info("Starting demo trading engine...")
            self.is_running = True
            self.start_time = datetime.now()
            
            # Start stream manager
            await self.stream_manager.start()
            
            # Subscribe to market data events
            self.stream_manager.add_subscriber("data", self._handle_market_data)
            self.stream_manager.add_subscriber("status", self._handle_stream_status)
            
            # Start main trading loop
            asyncio.create_task(self._trading_loop())
            
            self.logger.info("Demo trading engine started successfully")
            
        except Exception as e:
            self.logger.error(f"Error starting demo trading engine: {e}")
            self.is_running = False
            raise
    
    async def stop(self) -> None:
        """Stop the demo trading engine"""
        try:
            self.logger.info("Stopping demo trading engine...")
            self.is_running = False
            
            # Cancel all pending orders
            for order in self.orders.values():
                if order.status == DemoOrderStatus.PENDING:
                    order.status = DemoOrderStatus.CANCELLED
            
            # Stop stream manager
            await self.stream_manager.stop()
            
            self.logger.info("Demo trading engine stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping demo trading engine: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current engine status"""
        return {
            'is_running': self.is_running,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'portfolio_value': self.portfolio.get_total_value(),
            'cash': self.portfolio.cash,
            'positions': len(self.portfolio.positions),
            'active_strategies': len(self.active_strategies),
            'subscribed_symbols': len(self.subscribed_symbols),
            'total_trades': self.trades_executed,
            'total_pnl': self.total_pnl,
            'current_drawdown': self.current_drawdown,
            'pending_orders': len([o for o in self.orders.values() if o.status == DemoOrderStatus.PENDING])
        }
    
    def add_strategy(self, strategy: BaseStrategy, symbols: List[str]) -> bool:
        """Add a trading strategy
        
        Args:
            strategy: Strategy instance
            symbols: Symbols to trade with this strategy
            
        Returns:
            True if strategy added successfully
        """
        try:
            strategy_id = f"{strategy.name}_{len(self.strategies)}"
            
            # Initialize strategy
            context = self._create_strategy_context()
            strategy.initialize(context)
            
            # Store strategy
            self.strategies[strategy_id] = strategy
            
            # Subscribe to symbols
            for symbol in symbols:
                if symbol not in self.subscribed_symbols:
                    asyncio.create_task(self.stream_manager.subscribe_symbol(symbol))
                    self.subscribed_symbols.add(symbol)
            
            self.logger.info(f"Added strategy: {strategy_id} for symbols: {symbols}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding strategy: {e}")
            return False
    
    def activate_strategy(self, strategy_name: str) -> bool:
        """Activate a strategy for trading
        
        Args:
            strategy_name: Name of strategy to activate
            
        Returns:
            True if strategy activated
        """
        if strategy_name in self.strategies and strategy_name not in self.active_strategies:
            self.active_strategies.append(strategy_name)
            self.logger.info(f"Activated strategy: {strategy_name}")
            return True
        return False
    
    def deactivate_strategy(self, strategy_name: str) -> bool:
        """Deactivate a strategy
        
        Args:
            strategy_name: Name of strategy to deactivate
            
        Returns:
            True if strategy deactivated
        """
        if strategy_name in self.active_strategies:
            self.active_strategies.remove(strategy_name)
            self.logger.info(f"Deactivated strategy: {strategy_name}")
            return True
        return False
    
    async def place_order(self, symbol: str, action: str, quantity: float,
                         order_type: str = "market", price: Optional[float] = None,
                         stop_price: Optional[float] = None) -> str:
        """Place a demo trading order
        
        Args:
            symbol: Trading symbol
            action: Order action (buy/sell)
            quantity: Order quantity
            order_type: Order type (market/limit/stop)
            price: Limit price (for limit orders)
            stop_price: Stop price (for stop orders)
            
        Returns:
            Order ID
        """
        try:
            self.order_counter += 1
            order_id = f"DEMO_{self.order_counter:06d}"
            
            order = DemoOrder(
                order_id=order_id,
                symbol=symbol,
                action=action.lower(),
                quantity=quantity,
                order_type=order_type.lower(),
                price=price,
                stop_price=stop_price
            )
            
            # Validate order
            if not self._validate_order(order):
                order.status = DemoOrderStatus.REJECTED
                self.orders[order_id] = order
                return order_id
            
            # Store order
            self.orders[order_id] = order
            
            # Execute immediately if market order
            if order_type.lower() == "market":
                await self._execute_order(order)
            
            # Notify callback
            if self.on_order_callback:
                self.on_order_callback(order)
            
            return order_id
            
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")
            return ""
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel a pending order
        
        Args:
            order_id: Order ID to cancel
            
        Returns:
            True if order cancelled
        """
        if order_id in self.orders:
            order = self.orders[order_id]
            if order.status == DemoOrderStatus.PENDING:
                order.status = DemoOrderStatus.CANCELLED
                self.logger.info(f"Cancelled order: {order_id}")
                return True
        return False
    
    def get_orders(self, status: Optional[DemoOrderStatus] = None) -> List[DemoOrder]:
        """Get orders by status
        
        Args:
            status: Filter by order status (optional)
            
        Returns:
            List of orders
        """
        orders = list(self.orders.values())
        if status:
            orders = [o for o in orders if o.status == status]
        return orders
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary"""
        portfolio_summary = self.portfolio.get_portfolio_summary()
        
        # Add demo-specific metrics
        portfolio_summary.update({
            'initial_capital': self.initial_capital,
            'total_trades': self.trades_executed,
            'daily_pnl': self.daily_pnl,
            'peak_value': self.peak_value,
            'current_drawdown': self.current_drawdown,
            'active_strategies': len(self.active_strategies),
            'subscribed_symbols': len(self.subscribed_symbols)
        })
        
        return portfolio_summary
    
    async def _trading_loop(self):
        """Main trading loop"""
        try:
            while self.is_running:
                # Process pending orders
                await self._process_pending_orders()
                
                # Update performance metrics
                self._update_performance_metrics()
                
                # Sleep for a short interval
                await asyncio.sleep(1.0)
                
        except Exception as e:
            self.logger.error(f"Error in trading loop: {e}")
    
    async def _handle_market_data(self, data: MarketData):
        """Handle incoming market data"""
        try:
            # Update current data
            self.current_data[data.symbol] = data
            
            # Update portfolio with current prices
            self.portfolio.update_market_price(data.symbol, data.close)
            
            # Process strategies
            for strategy_name in self.active_strategies:
                if strategy_name in self.strategies:
                    strategy = self.strategies[strategy_name]
                    
                    # Generate signals
                    signals = strategy.next(data)
                    
                    # Execute signals
                    for signal in signals:
                        await self._execute_signal(signal)
            
        except Exception as e:
            self.logger.error(f"Error handling market data: {e}")
    
    async def _handle_stream_status(self, status_data: Dict[str, Any]):
        """Handle stream status changes"""
        self.logger.info(f"Stream status update: {status_data}")
    
    async def _execute_signal(self, signal: Signal):
        """Execute a trading signal"""
        try:
            # Validate signal with risk manager
            is_valid, reason, adjusted_quantity = self.risk_manager.validate_signal(
                signal=signal,
                portfolio_value=self.portfolio.get_total_value(),
                current_positions=self.portfolio.positions,
                market_data=self.current_data
            )
            
            if not is_valid:
                self.logger.warning(f"Signal rejected: {reason}")
                return
            
            # Place order with adjusted quantity
            await self.place_order(
                symbol=signal.symbol,
                action=signal.action,
                quantity=adjusted_quantity,
                order_type="market"
            )
            
        except Exception as e:
            self.logger.error(f"Error executing signal: {e}")
    
    def _validate_order(self, order: DemoOrder) -> bool:
        """Validate an order"""
        try:
            # Check if we have market data
            if order.symbol not in self.current_data:
                self.logger.error(f"No market data for {order.symbol}")
                return False
            
            current_price = self.current_data[order.symbol].close
            
            # Check if we have enough cash for buy orders
            if order.action == "buy":
                required_cash = order.quantity * current_price * (1 + self.commission)
                if required_cash > self.portfolio.cash:
                    self.logger.error(f"Insufficient cash: need {required_cash}, have {self.portfolio.cash}")
                    return False
            
            # Check if we have enough shares for sell orders
            elif order.action == "sell":
                current_position = self.portfolio.get_position_quantity(order.symbol)
                if order.quantity > current_position:
                    self.logger.error(f"Insufficient shares: need {order.quantity}, have {current_position}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating order: {e}")
            return False
    
    async def _execute_order(self, order: DemoOrder):
        """Execute an order"""
        try:
            if order.symbol not in self.current_data:
                order.status = DemoOrderStatus.REJECTED
                return
            
            current_price = self.current_data[order.symbol].close
            
            # Apply slippage
            if order.action == "buy":
                execution_price = current_price * (1 + self.slippage)
            else:
                execution_price = current_price * (1 - self.slippage)
            
            # Calculate commission
            commission = order.quantity * execution_price * self.commission
            
            # Execute trade
            if order.action == "buy":
                success = self.portfolio.buy(order.symbol, order.quantity, execution_price, commission)
            else:
                success = self.portfolio.sell(order.symbol, order.quantity, execution_price, commission)
            
            if success:
                order.status = DemoOrderStatus.FILLED
                order.filled_at = datetime.now()
                order.filled_price = execution_price
                order.commission = commission
                
                self.trades_executed += 1
                
                # Notify callback
                if self.on_trade_callback:
                    self.on_trade_callback(order)
                
                self.logger.info(f"Executed order {order.order_id}: {order.action} {order.quantity} {order.symbol} at {execution_price}")
            else:
                order.status = DemoOrderStatus.REJECTED
                self.logger.error(f"Failed to execute order {order.order_id}")
            
        except Exception as e:
            self.logger.error(f"Error executing order: {e}")
            order.status = DemoOrderStatus.REJECTED
    
    async def _process_pending_orders(self):
        """Process pending limit and stop orders"""
        try:
            for order in list(self.orders.values()):
                if order.status != DemoOrderStatus.PENDING:
                    continue
                
                if order.symbol not in self.current_data:
                    continue
                
                current_price = self.current_data[order.symbol].close
                should_execute = False
                
                # Check limit orders
                if order.order_type == "limit":
                    if order.action == "buy" and current_price <= order.price:
                        should_execute = True
                    elif order.action == "sell" and current_price >= order.price:
                        should_execute = True
                
                # Check stop orders
                elif order.order_type == "stop":
                    if order.action == "buy" and current_price >= order.stop_price:
                        should_execute = True
                    elif order.action == "sell" and current_price <= order.stop_price:
                        should_execute = True
                
                if should_execute:
                    await self._execute_order(order)
            
        except Exception as e:
            self.logger.error(f"Error processing pending orders: {e}")
    
    def _create_strategy_context(self):
        """Create strategy context"""
        return {
            'portfolio_value': self.portfolio.get_total_value(),
            'cash_balance': self.portfolio.cash,
            'positions': {symbol: pos.quantity for symbol, pos in self.portfolio.positions.items()},
            'market_data': self.current_data,
            'config': {}
        }
    
    def _update_performance_metrics(self):
        """Update performance tracking metrics"""
        try:
            current_value = self.portfolio.get_total_value()
            
            # Update peak value and drawdown
            if current_value > self.peak_value:
                self.peak_value = current_value
                self.current_drawdown = 0.0
            else:
                self.current_drawdown = (self.peak_value - current_value) / self.peak_value
            
            # Update total P&L
            self.total_pnl = current_value - self.initial_capital
            
            # Notify performance callback
            if self.on_performance_callback:
                self.on_performance_callback({
                    'portfolio_value': current_value,
                    'total_pnl': self.total_pnl,
                    'current_drawdown': self.current_drawdown,
                    'trades_executed': self.trades_executed
                })
            
        except Exception as e:
            self.logger.error(f"Error updating performance metrics: {e}")
    
    def set_callbacks(self, on_trade: Optional[Callable] = None,
                     on_order: Optional[Callable] = None,
                     on_performance: Optional[Callable] = None):
        """Set callback functions
        
        Args:
            on_trade: Callback for trade execution
            on_order: Callback for order updates
            on_performance: Callback for performance updates
        """
        self.on_trade_callback = on_trade
        self.on_order_callback = on_order
        self.on_performance_callback = on_performance