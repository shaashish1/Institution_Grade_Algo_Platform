"""
Base Strategy Class
==================

Abstract base class for all trading strategies in AlgoProject.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd

from ..core.interfaces import IStrategy, MarketData, Signal, TradingContext


class BaseStrategy(IStrategy):
    """Base class for all trading strategies"""
    
    def __init__(self, name: str, parameters: Dict[str, Any] = None):
        self.name = name
        self.parameters = parameters or {}
        self.is_initialized = False
        self.context = None
        self.positions = {}
        self.signals_history = []
        
    def initialize(self, context: TradingContext) -> None:
        """Initialize strategy with trading context"""
        self.context = context
        self.positions = context.positions.copy()
        self.is_initialized = True
        self._on_initialize()
    
    def _on_initialize(self):
        """Override this method for custom initialization logic"""
        pass
    
    @abstractmethod
    def next(self, data: MarketData) -> List[Signal]:
        """Process new market data and generate signals"""
        pass
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get strategy parameters"""
        return self.parameters.copy()
    
    def set_parameters(self, params: Dict[str, Any]) -> None:
        """Set strategy parameters"""
        self.parameters.update(params)
    
    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Get specific parameter value"""
        return self.parameters.get(key, default)
    
    def set_parameter(self, key: str, value: Any) -> None:
        """Set specific parameter value"""
        self.parameters[key] = value
    
    def create_signal(self, symbol: str, action: str, quantity: float, 
                     price: Optional[float] = None, confidence: float = 1.0,
                     metadata: Dict[str, Any] = None) -> Signal:
        """Create a trading signal"""
        signal = Signal(
            symbol=symbol,
            action=action,
            quantity=quantity,
            price=price,
            timestamp=datetime.now(),
            confidence=confidence,
            metadata=metadata or {}
        )
        
        self.signals_history.append(signal)
        return signal
    
    def get_position(self, symbol: str) -> float:
        """Get current position for symbol"""
        return self.positions.get(symbol, 0.0)
    
    def update_position(self, symbol: str, quantity: float):
        """Update position for symbol"""
        self.positions[symbol] = self.positions.get(symbol, 0.0) + quantity
    
    def calculate_position_size(self, symbol: str, price: float, risk_amount: float) -> float:
        """Calculate position size based on risk amount"""
        if price <= 0:
            return 0.0
        
        # Simple position sizing - can be overridden by strategies
        stop_loss_pct = self.get_parameter('stop_loss_pct', 0.05)
        if stop_loss_pct <= 0:
            return 0.0
        
        risk_per_share = price * stop_loss_pct
        position_size = risk_amount / risk_per_share
        
        return max(0.0, position_size)
    
    def should_enter_position(self, symbol: str, action: str) -> bool:
        """Check if should enter new position"""
        current_position = self.get_position(symbol)
        
        if action == 'buy' and current_position >= 0:
            return True
        elif action == 'sell' and current_position <= 0:
            return True
        
        return False
    
    def should_exit_position(self, symbol: str, action: str) -> bool:
        """Check if should exit existing position"""
        current_position = self.get_position(symbol)
        
        if action == 'sell' and current_position > 0:
            return True
        elif action == 'buy' and current_position < 0:
            return True
        
        return False
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """Get strategy information"""
        return {
            'name': self.name,
            'parameters': self.parameters,
            'is_initialized': self.is_initialized,
            'positions': self.positions,
            'signals_count': len(self.signals_history)
        }
    
    def reset(self):
        """Reset strategy state"""
        self.positions.clear()
        self.signals_history.clear()
        self.is_initialized = False
        self.context = None
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __repr__(self) -> str:
        return self.__str__()