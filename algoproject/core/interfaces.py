"""
Core Interfaces
==============

Base interfaces and abstract classes for the AlgoProject platform.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd


@dataclass
class MarketData:
    """Market data structure"""
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    exchange: str


@dataclass
class Signal:
    """Trading signal structure"""
    symbol: str
    action: str  # 'BUY', 'SELL', 'HOLD'
    quantity: float
    price: Optional[float] = None
    timestamp: Optional[datetime] = None
    confidence: float = 1.0
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class Position:
    """Position structure"""
    symbol: str
    quantity: float
    avg_price: float
    market_price: float
    timestamp: datetime


@dataclass
class TradingContext:
    """Trading context for strategy execution"""
    portfolio_value: float
    cash_balance: float
    positions: Dict[str, float]
    market_data: Dict[str, MarketData]
    config: Dict[str, Any]


class IStrategy(ABC):
    """Base interface for all trading strategies"""
    
    @abstractmethod
    def initialize(self, context: TradingContext) -> None:
        """Initialize the strategy with trading context"""
        pass
    
    @abstractmethod
    def next(self, data: MarketData) -> List[Signal]:
        """Process new market data and generate signals"""
        pass
    
    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """Get strategy parameters"""
        pass
    
    @abstractmethod
    def set_parameters(self, params: Dict[str, Any]) -> None:
        """Set strategy parameters"""
        pass


class IDataProvider(ABC):
    """Base interface for data providers"""
    
    @abstractmethod
    def get_historical_data(self, symbol: str, timeframe: str, bars: int) -> pd.DataFrame:
        """Get historical market data"""
        pass
    
    @abstractmethod
    def get_live_data(self, symbol: str) -> MarketData:
        """Get live market data"""
        pass
    
    @abstractmethod
    def get_available_symbols(self, exchange: str) -> List[str]:
        """Get available trading symbols for an exchange"""
        pass


class ITradingEngine(ABC):
    """Base interface for trading engines"""
    
    @abstractmethod
    def start(self) -> None:
        """Start the trading engine"""
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """Stop the trading engine"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current engine status"""
        pass


class IExecutor(ABC):
    """Base interface for trade execution"""
    
    @abstractmethod
    def execute_signal(self, signal: Signal) -> Dict[str, Any]:
        """Execute a trading signal"""
        pass
    
    @abstractmethod
    def get_positions(self) -> Dict[str, float]:
        """Get current positions"""
        pass
    
    @abstractmethod
    def get_balance(self) -> float:
        """Get current cash balance"""
        pass