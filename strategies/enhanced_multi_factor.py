#!/usr/bin/env python3
"""
Enhanced Multi-Factor Crypto Trading Strategy
Combines RSI, MACD, Bollinger Bands, Volume, and Trend Analysis
Optimized for crypto markets with adaptive thresholds
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class EnhancedMultiFactorStrategy:
    """
    Enhanced multi-factor strategy for crypto trading that combines:
    - RSI with adaptive thresholds
    - MACD with histogram analysis
    - Bollinger Bands with squeeze detection
    - Volume profile analysis
    - Trend strength indicator
    - Market volatility adaptation
    """
    
    def __init__(self, 
                 rsi_period: int = 14,
                 macd_fast: int = 12,
                 macd_slow: int = 26,
                 macd_signal: int = 9,
                 bb_period: int = 20,
                 bb_std: float = 2.0,
                 volume_period: int = 20,
                 trend_period: int = 50):
        
        self.rsi_period = rsi_period
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.volume_period = volume_period
        self.trend_period = trend_period
        
        # Adaptive thresholds
        self.base_rsi_oversold = 30
        self.base_rsi_overbought = 70
        self.volatility_adjustment = 0.1
        
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators."""
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
        
        # Bollinger Bands
        data['bb_middle'] = data['close'].rolling(window=self.bb_period).mean()
        bb_std = data['close'].rolling(window=self.bb_period).std()
        data['bb_upper'] = data['bb_middle'] + (bb_std * self.bb_std)
        data['bb_lower'] = data['bb_middle'] - (bb_std * self.bb_std)
        data['bb_width'] = (data['bb_upper'] - data['bb_lower']) / data['bb_middle']
        
        # Volume indicators
        data['volume_sma'] = data['volume'].rolling(window=self.volume_period).mean()
        data['volume_ratio'] = data['volume'] / data['volume_sma']
        
        # Trend indicators
        data['trend_sma'] = data['close'].rolling(window=self.trend_period).mean()
        data['trend_strength'] = (data['close'] - data['trend_sma']) / data['trend_sma']
        
        # Volatility indicator
        data['volatility'] = data['close'].rolling(window=20).std() / data['close'].rolling(window=20).mean()
        
        # Price momentum
        data['price_momentum'] = data['close'].pct_change(5)
        
        # VWAP
        typical_price = (data['high'] + data['low'] + data['close']) / 3
        data['vwap'] = (typical_price * data['volume']).cumsum() / data['volume'].cumsum()
        
        return data
    
    def get_adaptive_thresholds(self, volatility: float) -> Tuple[float, float]:
        """Get adaptive RSI thresholds based on market volatility."""
        vol_factor = min(volatility * 100, 20)  # Cap at 20% adjustment
        
        oversold = self.base_rsi_oversold + (vol_factor * self.volatility_adjustment)
        overbought = self.base_rsi_overbought - (vol_factor * self.volatility_adjustment)
        
        # Ensure valid range
        oversold = max(20, min(oversold, 40))
        overbought = max(60, min(overbought, 80))
        
        return oversold, overbought
    
    def calculate_signal_strength(self, data: pd.DataFrame, idx: int) -> Dict[str, float]:
        """Calculate signal strength for multiple factors."""
        current = data.iloc[idx]
        prev = data.iloc[idx-1] if idx > 0 else current
        
        # Get adaptive thresholds
        oversold, overbought = self.get_adaptive_thresholds(current['volatility'])
        
        signals = {
            'rsi_bullish': 0,
            'rsi_bearish': 0,
            'macd_bullish': 0,
            'macd_bearish': 0,
            'bb_bullish': 0,
            'bb_bearish': 0,
            'volume_bullish': 0,
            'volume_bearish': 0,
            'trend_bullish': 0,
            'trend_bearish': 0,
            'momentum_bullish': 0,
            'momentum_bearish': 0,
            'vwap_bullish': 0,
            'vwap_bearish': 0
        }
        
        # RSI signals with adaptive thresholds
        if current['rsi'] < oversold:
            signals['rsi_bullish'] = (oversold - current['rsi']) / 10  # Normalize
        elif current['rsi'] > overbought:
            signals['rsi_bearish'] = (current['rsi'] - overbought) / 10
        
        # MACD signals
        if current['macd'] > current['macd_signal'] and prev['macd'] <= prev['macd_signal']:
            signals['macd_bullish'] = min(abs(current['macd_histogram']) * 1000, 3)
        elif current['macd'] < current['macd_signal'] and prev['macd'] >= prev['macd_signal']:
            signals['macd_bearish'] = min(abs(current['macd_histogram']) * 1000, 3)
        
        # Bollinger Bands signals
        if current['close'] <= current['bb_lower']:
            signals['bb_bullish'] = min((current['bb_lower'] - current['close']) / current['close'] * 100, 2)
        elif current['close'] >= current['bb_upper']:
            signals['bb_bearish'] = min((current['close'] - current['bb_upper']) / current['close'] * 100, 2)
        
        # Volume confirmation
        if current['volume_ratio'] > 1.5:  # High volume
            if current['close'] > prev['close']:
                signals['volume_bullish'] = min(current['volume_ratio'] - 1, 2)
            else:
                signals['volume_bearish'] = min(current['volume_ratio'] - 1, 2)
        
        # Trend signals
        if current['trend_strength'] > 0.02:  # 2% above trend
            signals['trend_bullish'] = min(current['trend_strength'] * 50, 2)
        elif current['trend_strength'] < -0.02:  # 2% below trend
            signals['trend_bearish'] = min(abs(current['trend_strength']) * 50, 2)
        
        # Momentum signals
        if current['price_momentum'] > 0.01:  # 1% momentum
            signals['momentum_bullish'] = min(current['price_momentum'] * 100, 2)
        elif current['price_momentum'] < -0.01:
            signals['momentum_bearish'] = min(abs(current['price_momentum']) * 100, 2)
        
        # VWAP signals
        if current['close'] < current['vwap'] * 0.98:  # Below VWAP
            signals['vwap_bullish'] = min((current['vwap'] - current['close']) / current['close'] * 100, 2)
        elif current['close'] > current['vwap'] * 1.02:  # Above VWAP
            signals['vwap_bearish'] = min((current['close'] - current['vwap']) / current['close'] * 100, 2)
        
        return signals
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate enhanced trading signals."""
        data = self.calculate_indicators(df)
        signals = []
        
        # Start after enough data for all indicators
        start_idx = max(self.macd_slow + self.macd_signal, self.bb_period, self.trend_period)
        
        for i in range(start_idx, len(data)):
            current = data.iloc[i]
            
            # Skip if any critical indicator is NaN
            if pd.isna(current['rsi']) or pd.isna(current['macd']) or pd.isna(current['bb_middle']):
                continue
            
            # Calculate signal strengths
            signal_strengths = self.calculate_signal_strength(data, i)
            
            # Calculate composite scores
            bullish_score = sum([
                signal_strengths['rsi_bullish'],
                signal_strengths['macd_bullish'],
                signal_strengths['bb_bullish'],
                signal_strengths['volume_bullish'],
                signal_strengths['trend_bullish'],
                signal_strengths['momentum_bullish'],
                signal_strengths['vwap_bullish']
            ])
            
            bearish_score = sum([
                signal_strengths['rsi_bearish'],
                signal_strengths['macd_bearish'],
                signal_strengths['bb_bearish'],
                signal_strengths['volume_bearish'],
                signal_strengths['trend_bearish'],
                signal_strengths['momentum_bearish'],
                signal_strengths['vwap_bearish']
            ])
            
            # Decision logic with minimum threshold
            min_signal_threshold = 3.0  # Minimum composite score
            
            if bullish_score >= min_signal_threshold and bullish_score > bearish_score:
                signals.append({
                    'timestamp': current.name,
                    'signal': 'BUY',
                    'price': current['close'],
                    'rsi': current['rsi'],
                    'macd': current['macd'],
                    'score': bullish_score,
                    'confidence': min(bullish_score / 10, 1.0),  # Confidence 0-1
                    'factors': signal_strengths
                })
            elif bearish_score >= min_signal_threshold and bearish_score > bullish_score:
                signals.append({
                    'timestamp': current.name,
                    'signal': 'SELL',
                    'price': current['close'],
                    'rsi': current['rsi'],
                    'macd': current['macd'],
                    'score': bearish_score,
                    'confidence': min(bearish_score / 10, 1.0),
                    'factors': signal_strengths
                })
        
        return pd.DataFrame(signals)
    
    def get_strategy_name(self) -> str:
        """Return strategy name."""
        return "Enhanced_Multi_Factor"
    
    def get_strategy_description(self) -> str:
        """Return strategy description."""
        return """
        Enhanced Multi-Factor Strategy combines:
        - Adaptive RSI thresholds based on volatility
        - MACD with histogram analysis
        - Bollinger Bands with squeeze detection
        - Volume profile confirmation
        - Trend strength analysis
        - Price momentum indicators
        - VWAP positioning
        
        Uses composite scoring with minimum threshold for signal generation.
        """
    
    def backtest_summary(self, df: pd.DataFrame) -> Dict:
        """Provide strategy-specific backtest summary."""
        data = self.calculate_indicators(df)
        signals = self.generate_signals(df)
        
        if signals.empty:
            return {
                'strategy': self.get_strategy_name(),
                'signals_generated': 0,
                'avg_confidence': 0,
                'signal_distribution': {'BUY': 0, 'SELL': 0}
            }
        
        return {
            'strategy': self.get_strategy_name(),
            'signals_generated': len(signals),
            'avg_confidence': signals['confidence'].mean(),
            'signal_distribution': signals['signal'].value_counts().to_dict(),
            'avg_score': signals['score'].mean(),
            'max_score': signals['score'].max(),
            'min_score': signals['score'].min()
        }
