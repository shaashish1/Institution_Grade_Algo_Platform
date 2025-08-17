#!/usr/bin/env python3
"""
MACD Only Strategy
Pure MACD crossover strategy with histogram confirmation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class MACD_Only_Strategy:
    """
    MACD-only strategy that focuses on:
    - MACD line crossing above/below signal line
    - Histogram confirmation for signal strength
    - Simple but reliable trend-following approach
    """
    
    def __init__(self, 
                 macd_fast: int = 12,
                 macd_slow: int = 26,
                 macd_signal: int = 9,
                 histogram_threshold: float = 0.0):
        
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.histogram_threshold = histogram_threshold
        
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate MACD indicators."""
        data = df.copy()
        
        # MACD calculation
        exp1 = data['close'].ewm(span=self.macd_fast).mean()
        exp2 = data['close'].ewm(span=self.macd_slow).mean()
        data['macd'] = exp1 - exp2
        data['macd_signal'] = data['macd'].ewm(span=self.macd_signal).mean()
        data['macd_histogram'] = data['macd'] - data['macd_signal']
        
        return data
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals using MACD only."""
        data = self.calculate_indicators(df)
        signals = []
        
        # Start after MACD calculation period
        start_idx = self.macd_slow + self.macd_signal
        
        for i in range(start_idx, len(data)):
            current = data.iloc[i]
            prev = data.iloc[i-1] if i > 0 else current
            
            # Skip if any indicator is NaN
            if pd.isna(current['macd']) or pd.isna(current['macd_signal']):
                continue
            
            # Buy signal: MACD crosses above signal line
            if (current['macd'] > current['macd_signal'] and 
                prev['macd'] <= prev['macd_signal']):
                
                # Calculate signal strength based on histogram
                signal_strength = min(abs(current['macd_histogram']) * 1000, 5)
                
                signals.append({
                    'timestamp': current.name,
                    'signal': 'BUY',
                    'price': current['close'],
                    'rsi': np.nan,
                    'macd': current['macd'],
                    'score': 3,
                    'histogram': current['macd_histogram'],
                    'signal_strength': signal_strength
                })
            
            # Sell signal: MACD crosses below signal line
            elif (current['macd'] < current['macd_signal'] and 
                  prev['macd'] >= prev['macd_signal']):
                
                # Calculate signal strength based on histogram
                signal_strength = min(abs(current['macd_histogram']) * 1000, 5)
                
                signals.append({
                    'timestamp': current.name,
                    'signal': 'SELL',
                    'price': current['close'],
                    'rsi': np.nan,
                    'macd': current['macd'],
                    'score': 3,
                    'histogram': current['macd_histogram'],
                    'signal_strength': signal_strength
                })
        
        return pd.DataFrame(signals)
    
    def get_strategy_name(self) -> str:
        """Return strategy name."""
        return "MACD_Only"
    
    def get_strategy_description(self) -> str:
        """Return strategy description."""
        return """
        MACD Only Strategy:
        - Buy when MACD line crosses above signal line
        - Sell when MACD line crosses below signal line
        - Uses histogram for signal strength confirmation
        - Pure trend-following approach
        - Works well in trending markets
        """
