#!/usr/bin/env python3
"""
Bollinger Bands and RSI Strategy
Simple but effective strategy combining Bollinger Bands and RSI
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class BB_RSI_Strategy:
    """
    Bollinger Bands and RSI strategy that looks for:
    - RSI oversold/overbought conditions
    - Price touching Bollinger Band extremes
    - Confluence of both signals for higher probability trades
    """
    
    def __init__(self, 
                 bb_period: int = 20,
                 bb_std: float = 2.0,
                 rsi_period: int = 14,
                 rsi_oversold: float = 30,
                 rsi_overbought: float = 70):
        
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Bollinger Bands and RSI indicators."""
        data = df.copy()
        
        # Bollinger Bands
        data['bb_middle'] = data['close'].rolling(window=self.bb_period).mean()
        bb_std = data['close'].rolling(window=self.bb_period).std()
        data['bb_upper'] = data['bb_middle'] + (bb_std * self.bb_std)
        data['bb_lower'] = data['bb_middle'] - (bb_std * self.bb_std)
        
        # RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        return data
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals using Bollinger Bands and RSI."""
        data = self.calculate_indicators(df)
        signals = []
        
        # Start after indicator calculation period
        start_idx = max(self.bb_period, self.rsi_period)
        
        for i in range(start_idx, len(data)):
            current = data.iloc[i]
            
            # Skip if any indicator is NaN
            if pd.isna(current['bb_lower']) or pd.isna(current['bb_upper']) or pd.isna(current['rsi']):
                continue
            
            # Buy signal: Price touches lower BB and RSI oversold
            if (current['close'] <= current['bb_lower'] and current['rsi'] < self.rsi_oversold):
                signals.append({
                    'timestamp': current.name,
                    'signal': 'BUY',
                    'price': current['close'],
                    'rsi': current['rsi'],
                    'macd': np.nan,
                    'score': 3,
                    'bb_position': (current['close'] - current['bb_lower']) / (current['bb_upper'] - current['bb_lower']),
                    'signal_strength': 'Strong'
                })
            
            # Sell signal: Price touches upper BB and RSI overbought
            elif (current['close'] >= current['bb_upper'] and current['rsi'] > self.rsi_overbought):
                signals.append({
                    'timestamp': current.name,
                    'signal': 'SELL',
                    'price': current['close'],
                    'rsi': current['rsi'],
                    'macd': np.nan,
                    'score': 3,
                    'bb_position': (current['close'] - current['bb_lower']) / (current['bb_upper'] - current['bb_lower']),
                    'signal_strength': 'Strong'
                })
        
        return pd.DataFrame(signals)
    
    def get_strategy_name(self) -> str:
        """Return strategy name."""
        return "BB_RSI"
    
    def get_strategy_description(self) -> str:
        """Return strategy description."""
        return """
        Bollinger Bands and RSI Strategy:
        - Buy when price touches lower Bollinger Band AND RSI is oversold
        - Sell when price touches upper Bollinger Band AND RSI is overbought
        - Focuses on mean reversion at extreme price levels
        - Simple but effective for range-bound markets
        """
