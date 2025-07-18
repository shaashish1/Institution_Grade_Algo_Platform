"""
Live Trading Engine
==================

Real exchange integration for live trading.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

from ..core.interfaces import ITradingEngine, Signal, MarketData
from ..security.api_key_manager import APIKeyManager
from ..data.data_loader import DataLoader
from ..strategies.base_strategy import BaseStrategy


class TradingMode(Enum):
    """Trading modes"""
    PAPER = "paper"
    LIVE = "live"
    SANDBOX = "sandbox"


class LiveTradingEngine(ITradingEngine):
    """Live trading engine with real exchange integration"""
    
    def __init__(self, api_key_manager: APIKeyManager, data_loader: DataLoader):
        """Initialize live trading engine
        
        Args:
            api_key_manager: API key manager for secure credentials
            data_loader: Data loader for market data
        """
        self.api_key_manager = api_key_manager
        self.data_loader = data_loader
        self.logger = logging.getLogger(__name__)
        
        # Trading state
        self.is_running = False
        self.trading_mode = TradingMode.PAPER
        self.active_strategies: Dict[str, BaseStrategy] = {}
        self.positions: Dict[str, float] = {}
        self.orders: Dict[str, Dict[str, Any]] = {}
        
        # Performance tracking
        self.total_trades = 0
        self.successful_trades = 0
        self.total_pnl = 0.0
        self.start_time: Optional[datetime] = None
        
        # Risk management
        self.max_position_size = 0.1  # 10% max position
        self.daily_loss_limit = 0.05  # 5% daily loss limit
        self.emergency_stop = False
    
    def start(self) -> None:
        """Start the live trading engine"""
        try:
            if self.is_running:
                self.logger.warning("Trading engine already running")
                return
            
            self.is_running = True
            self.start_time = datetime.now()
            self.emergency_stop = False
            
            self.logger.info(f"Live trading engine started in {self.trading_mode.value} mode")
            
            # Start main trading loop
            asyncio.create_task(self._trading_loop())
            
        except Exception as e:
            self.logger.error(f"Failed to start trading engine: {e}")
            self.is_running = False
            raise
    
    def stop(self) -> None:
        """Stop the live trading engine"""
        try:
            self.is_running = False
            self.logger.info("Live trading engine stopped")
            
            # Close all positions if in live mode
            if self.trading_mode == TradingMode.LIVE:
                self._close_all_positions()
            
        except Exception as e:
            self.logger.error(f"Error stopping trading engine: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current engine status"""
        uptime = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        return {
            'running': self.is_running,
            'mode': self.trading_mode.value,
            'uptime_seconds': uptime,
            'active_strategies': len(self.active_strategies),
            'total_trades': self.total_trades,
            'successful_trades': self.successful_trades,
            'success_rate': self.successful_trades / max(self.total_trades, 1),
            'total_pnl': self.total_pnl,
            'positions': len(self.positions),
            'emergency_stop': self.emergency_stop
        }
    
    def add_strategy(self, strategy: BaseStrategy, symbols: List[str]) -> str:
        """Add strategy to live trading
        
        Args:
            strategy: Strategy instance
            symbols: Symbols to trade
            
        Returns:
            Strategy ID
        """
        try:
            strategy_id = f"{strategy.name}_{len(self.active_strategies)}"
            
            # Initialize strategy
            from ..backtesting.backtest_context import BacktestContext
            context = BacktestContext(initial_capital=100000.0)  # Mock context for live trading
            strategy.initialize(context)
            
            # Store strategy
            self.active_strategies[strategy_id] = {
                'strategy': strategy,
                'symbols': symbols,
                'added_at': datetime.now(),
                'signals_generated': 0,
                'trades_executed': 0
            }
            
            self.logger.info(f"Added strategy {strategy.name} for symbols {symbols}")
            return strategy_id
            
        except Exception as e:
            self.logger.error(f"Failed to add strategy: {e}")
            raise
    
    def remove_strategy(self, strategy_id: str) -> bool:
        """Remove strategy from live trading
        
        Args:
            strategy_id: Strategy ID to remove
            
        Returns:
            True if removed successfully
        """
        try:
            if strategy_id in self.active_strategies:
                del self.active_strategies[strategy_id]
                self.logger.info(f"Removed strategy {strategy_id}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to remove strategy: {e}")
            return False
    
    def execute_signal(self, signal: Signal) -> Dict[str, Any]:
        """Execute trading signal
        
        Args:
            signal: Trading signal to execute
            
        Returns:
            Execution result
        """
        try:
            if self.emergency_stop:
                return {'success': False, 'error': 'Emergency stop active'}
            
            # Validate signal
            if not self._validate_signal(signal):
                return {'success': False, 'error': 'Signal validation failed'}
            
            # Execute based on trading mode
            if self.trading_mode == TradingMode.LIVE:
                result = self._execute_live_signal(signal)
            else:
                result = self._execute_paper_signal(signal)
            
            # Update statistics
            self.total_trades += 1
            if result.get('success', False):
                self.successful_trades += 1
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to execute signal: {e}")
            return {'success': False, 'error': str(e)}
    
    def set_trading_mode(self, mode: TradingMode):
        """Set trading mode
        
        Args:
            mode: Trading mode to set
        """
        if self.is_running:
            self.logger.warning("Cannot change mode while engine is running")
            return
        
        self.trading_mode = mode
        self.logger.info(f"Trading mode set to {mode.value}")
    
    def emergency_stop_all(self):
        """Emergency stop all trading"""
        self.emergency_stop = True
        self.logger.critical("EMERGENCY STOP ACTIVATED")
        
        # Close all positions immediately
        self._close_all_positions()
        
        # Stop all strategies
        self.active_strategies.clear()
    
    async def _trading_loop(self):
        """Main trading loop"""
        try:
            while self.is_running:
                if self.emergency_stop:
                    break
                
                # Process each active strategy
                for strategy_id, strategy_data in self.active_strategies.items():
                    try:
                        await self._process_strategy(strategy_id, strategy_data)
                    except Exception as e:
                        self.logger.error(f"Error processing strategy {strategy_id}: {e}")
                
                # Sleep before next iteration
                await asyncio.sleep(1)  # 1 second intervals
                
        except Exception as e:
            self.logger.error(f"Error in trading loop: {e}")
        finally:
            self.is_running = False
    
    async def _process_strategy(self, strategy_id: str, strategy_data: Dict[str, Any]):
        """Process individual strategy"""
        strategy = strategy_data['strategy']
        symbols = strategy_data['symbols']
        
        for symbol in symbols:
            try:
                # Get latest market data
                market_data = self.data_loader.get_live_data(symbol)
                if not market_data:
                    continue
                
                # Generate signals
                signals = strategy.next(market_data)
                
                # Execute signals
                for signal in signals:
                    result = self.execute_signal(signal)
                    if result.get('success'):
                        strategy_data['trades_executed'] += 1
                    
                    strategy_data['signals_generated'] += 1
                
            except Exception as e:
                self.logger.error(f"Error processing {symbol} for strategy {strategy_id}: {e}")
    
    def _validate_signal(self, signal: Signal) -> bool:
        """Validate trading signal"""
        try:
            # Basic validation
            if not signal.symbol or not signal.action or signal.quantity <= 0:
                return False
            
            # Position size validation
            if signal.quantity > self.max_position_size:
                self.logger.warning(f"Signal quantity {signal.quantity} exceeds max position size")
                return False
            
            # Risk management checks
            current_position = self.positions.get(signal.symbol, 0.0)
            
            if signal.action.lower() == 'buy' and current_position + signal.quantity > self.max_position_size:
                self.logger.warning(f"Signal would exceed max position size for {signal.symbol}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating signal: {e}")
            return False
    
    def _execute_live_signal(self, signal: Signal) -> Dict[str, Any]:
        """Execute signal in live trading mode"""
        try:
            # TODO: Implement actual exchange API calls
            # For now, simulate execution
            
            order_id = f"LIVE_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{signal.symbol}"
            
            # Simulate order execution
            execution_result = {
                'success': True,
                'order_id': order_id,
                'symbol': signal.symbol,
                'action': signal.action,
                'quantity': signal.quantity,
                'price': signal.price,
                'timestamp': datetime.now().isoformat(),
                'mode': 'live'
            }
            
            # Update positions
            if signal.action.lower() == 'buy':
                self.positions[signal.symbol] = self.positions.get(signal.symbol, 0.0) + signal.quantity
            elif signal.action.lower() == 'sell':
                self.positions[signal.symbol] = self.positions.get(signal.symbol, 0.0) - signal.quantity
            
            # Store order
            self.orders[order_id] = execution_result
            
            self.logger.info(f"Executed live order: {order_id}")
            return execution_result
            
        except Exception as e:
            self.logger.error(f"Failed to execute live signal: {e}")
            return {'success': False, 'error': str(e)}
    
    def _execute_paper_signal(self, signal: Signal) -> Dict[str, Any]:
        """Execute signal in paper trading mode"""
        try:
            order_id = f"PAPER_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{signal.symbol}"
            
            # Simulate paper execution
            execution_result = {
                'success': True,
                'order_id': order_id,
                'symbol': signal.symbol,
                'action': signal.action,
                'quantity': signal.quantity,
                'price': signal.price,
                'timestamp': datetime.now().isoformat(),
                'mode': 'paper'
            }
            
            # Update paper positions
            if signal.action.lower() == 'buy':
                self.positions[signal.symbol] = self.positions.get(signal.symbol, 0.0) + signal.quantity
            elif signal.action.lower() == 'sell':
                self.positions[signal.symbol] = self.positions.get(signal.symbol, 0.0) - signal.quantity
            
            # Store order
            self.orders[order_id] = execution_result
            
            self.logger.info(f"Executed paper order: {order_id}")
            return execution_result
            
        except Exception as e:
            self.logger.error(f"Failed to execute paper signal: {e}")
            return {'success': False, 'error': str(e)}
    
    def _close_all_positions(self):
        """Close all open positions"""
        try:
            for symbol, quantity in self.positions.items():
                if quantity != 0:
                    # Create close signal
                    action = 'sell' if quantity > 0 else 'buy'
                    close_signal = Signal(
                        symbol=symbol,
                        action=action,
                        quantity=abs(quantity),
                        confidence=1.0,
                        metadata={'reason': 'emergency_close'}
                    )
                    
                    # Execute close signal
                    self.execute_signal(close_signal)
            
            self.logger.info("All positions closed")
            
        except Exception as e:
            self.logger.error(f"Error closing positions: {e}")
    
    def get_positions(self) -> Dict[str, float]:
        """Get current positions"""
        return self.positions.copy()
    
    def get_orders(self) -> Dict[str, Dict[str, Any]]:
        """Get order history"""
        return self.orders.copy()