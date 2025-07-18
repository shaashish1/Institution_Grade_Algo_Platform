"""
SMA Crossover Strategy
=====================

Simple Moving Average crossover strategy for trend following.
"""

from typing import Dict, Any, List
import pandas as pd
from collections import deque

from ..base_strategy import BaseStrategy
from ...core.interfaces import Signal, MarketData


class SMACrossoverStrategy(BaseStrategy):
    """Simple Moving Average Crossover Strategy"""
    
    def __init__(self):
        super().__init__()
        self.price_history = deque(maxlen=200)  # Keep last 200 prices
        self.last_signal = None
    
    def _default_parameters(self) -> Dict[str, Any]:
        """Default parameters for SMA crossover"""
        return {
            'fast_period': 10,
            'slow_period': 20,
            'risk_per_trade': 0.02,
            'stop_loss_pct': 0.05,
            'take_profit_pct': 0.10
        }
    
    def _generate_signals(self, data: MarketData) -> List[Signal]:
        """Generate signals based on SMA crossover"""
        signals = []
        
        # Add current price to history
        self.price_history.append(data.close)
        
        # Need enough data for calculation
        if len(self.price_history) < self.parameters['slow_period']:
            return signals
        
        # Calculate SMAs
        prices = list(self.price_history)
        fast_sma = sum(prices[-self.parameters['fast_period']:]) / self.parameters['fast_period']
        slow_sma = sum(prices[-self.parameters['slow_period']:]) / self.parameters['slow_period']
        
        # Previous SMAs for crossover detection
        if len(self.price_history) >= self.parameters['slow_period'] + 1:
            prev_prices = prices[:-1]
            prev_fast_sma = sum(prev_prices[-self.parameters['fast_period']:]) / self.parameters['fast_period']
            prev_slow_sma = sum(prev_prices[-self.parameters['slow_period']:]) / self.parameters['slow_period']
            
            # Detect crossovers
            bullish_crossover = (fast_sma > slow_sma and prev_fast_sma <= prev_slow_sma)
            bearish_crossover = (fast_sma < slow_sma and prev_fast_sma >= prev_slow_sma)
            
            if bullish_crossover and self.last_signal != 'buy':
                # Generate buy signal
                position_size = self.get_position_size(data.symbol, data.close)
                if position_size > 0:
                    signal = self._create_signal(
                        symbol=data.symbol,
                        action='buy',
                        quantity=position_size,
                        price=data.close,
                        confidence=0.8,
                        metadata={
                            'fast_sma': fast_sma,
                            'slow_sma': slow_sma,
                            'crossover_type': 'bullish'
                        }
                    )
                    if signal:
                        signals.append(signal)
                        self.last_signal = 'buy'
            
            elif bearish_crossover and self.last_signal != 'sell':
                # Generate sell signal
                current_position = self.context.positions.get(data.symbol, 0)
                if current_position > 0:
                    signal = self._create_signal(
                        symbol=data.symbol,
                        action='sell',
                        quantity=current_position,
                        price=data.close,
                        confidence=0.8,
                        metadata={
                            'fast_sma': fast_sma,
                            'slow_sma': slow_sma,
                            'crossover_type': 'bearish'
                        }
                    )
                    if signal:
                        signals.append(signal)
                        self.last_signal = 'sell'
        
        return signals
    
    def _on_initialize(self) -> None:
        """Initialize strategy-specific data"""
        self.price_history.clear()
        self.last_signal = None
        self.logger.info(f"SMA Crossover initialized with fast={self.parameters['fast_period']}, slow={self.parameters['slow_period']}")