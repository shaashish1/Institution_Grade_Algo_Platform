#!/usr/bin/env python3
"""
RSI, MACD, and VWAP Combined Strategy
Multi-factor approach combining RSI, MACD, and VWAP indicators
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class RSI_MACD_VWAP_Strategy:
    """
    RSI, MACD, and VWAP combined strategy that uses:
    - RSI for overbought/oversold conditions
    - MACD for trend confirmation
    - VWAP for price positioning
    - Requires at least 2 out of 3 conditions for signal generation
    """
    
    def __init__(self, 
                 rsi_period: int = 14,
                 rsi_oversold: float = 35,
                 rsi_overbought: float = 65,
                 macd_fast: int = 12,
                 macd_slow: int = 26,
                 macd_signal: int = 9,
                 vwap_tolerance: float = 0.02):
        
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.vwap_tolerance = vwap_tolerance
        
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate RSI, MACD, and VWAP indicators."""
        data = df.copy()
        
        # RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = data['close'].ewm(span=self.macd_fast).mean()
        exp2 = data['close'].ewm(span=self.macd_slow).mean()
        data['macd'] = exp1 - exp2
        data['macd_signal'] = data['macd'].ewm(span=self.macd_signal).mean()
        data['macd_histogram'] = data['macd'] - data['macd_signal']
        
        # VWAP
        typical_price = (data['high'] + data['low'] + data['close']) / 3
        data['vwap'] = (typical_price * data['volume']).cumsum() / data['volume'].cumsum()
        
        return data
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals using RSI, MACD, and VWAP."""
        data = self.calculate_indicators(df)
        signals = []
        
        # Start after MACD calculation period
        start_idx = self.macd_slow + self.macd_signal
        
        for i in range(start_idx, len(data)):
            current = data.iloc[i]
            prev = data.iloc[i-1] if i > 0 else current
            
            # Skip if any indicator is NaN
            if pd.isna(current['rsi']) or pd.isna(current['macd']) or pd.isna(current['vwap']):
                continue
            
            # Buy signal conditions (at least 2 out of 3 conditions)
            buy_conditions = [
                current['rsi'] < self.rsi_oversold,  # RSI oversold
                current['macd'] > current['macd_signal'] and prev['macd'] <= prev['macd_signal'],  # MACD bullish crossover
                current['close'] < current['vwap'] * (1 + self.vwap_tolerance)  # Price near or below VWAP
            ]
            
            # Sell signal conditions (at least 2 out of 3 conditions)
            sell_conditions = [
                current['rsi'] > self.rsi_overbought,  # RSI overbought
                current['macd'] < current['macd_signal'] and prev['macd'] >= prev['macd_signal'],  # MACD bearish crossover
                current['close'] > current['vwap'] * (1 - self.vwap_tolerance)  # Price near or above VWAP
            ]
            
            # Signal strength scoring
            buy_score = sum(buy_conditions)
            sell_score = sum(sell_conditions)
            
            # Generate signals based on score (at least 2 conditions must be met)
            if buy_score >= 2:
                signals.append({
                    'timestamp': current.name,
                    'signal': 'BUY',
                    'price': current['close'],
                    'rsi': current['rsi'],
                    'macd': current['macd'],
                    'score': buy_score,
                    'vwap_distance': (current['close'] - current['vwap']) / current['vwap'],
                    'conditions_met': buy_score
                })
            elif sell_score >= 2:
                signals.append({
                    'timestamp': current.name,
                    'signal': 'SELL',
                    'price': current['close'],
                    'rsi': current['rsi'],
                    'macd': current['macd'],
                    'score': sell_score,
                    'vwap_distance': (current['close'] - current['vwap']) / current['vwap'],
                    'conditions_met': sell_score
                })
        
        return pd.DataFrame(signals)
    
    def get_strategy_name(self) -> str:
        """Return strategy name."""
        return "RSI_MACD_VWAP"
    
    def get_strategy_description(self) -> str:
        """Return strategy description."""
        return """
        RSI, MACD, and VWAP Combined Strategy:
        - RSI for overbought/oversold conditions
        - MACD for trend confirmation via crossovers
        - VWAP for price positioning relative to average
        - Requires at least 2 out of 3 conditions for signal
        - Flexible approach that works in various market conditions
        """
