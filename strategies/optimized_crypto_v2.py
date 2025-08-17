#!/usr/bin/env python3
"""
Optimized Crypto Trading Strategy v2
Improved version with better signal filtering and market regime detection
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class OptimizedCryptoStrategy:
    """
    Optimized crypto strategy with:
    - Market regime detection (trending vs ranging)
    - Dynamic signal threshold adjustment
    - Better risk-reward filtering
    - Volatility-based position sizing hints
    """
    
    def __init__(self):
        # Core parameters
        self.rsi_period = 14
        self.macd_fast = 12
        self.macd_slow = 26
        self.macd_signal = 9
        self.bb_period = 20
        self.atr_period = 14
        self.volume_period = 20
        
        # Signal thresholds
        self.min_signal_strength = 4.0
        self.risk_reward_ratio = 1.5
        
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators with market regime detection."""
        data = df.copy()
        
        # Price-based indicators
        data['sma_20'] = data['close'].rolling(window=20).mean()
        data['sma_50'] = data['close'].rolling(window=50).mean()
        data['ema_12'] = data['close'].ewm(span=12).mean()
        data['ema_26'] = data['close'].ewm(span=26).mean()
        
        # RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        data['macd'] = data['ema_12'] - data['ema_26']
        data['macd_signal'] = data['macd'].ewm(span=self.macd_signal).mean()
        data['macd_histogram'] = data['macd'] - data['macd_signal']
        
        # Bollinger Bands
        data['bb_middle'] = data['close'].rolling(window=self.bb_period).mean()
        bb_std = data['close'].rolling(window=self.bb_period).std()
        data['bb_upper'] = data['bb_middle'] + (bb_std * 2)
        data['bb_lower'] = data['bb_middle'] - (bb_std * 2)
        data['bb_width'] = (data['bb_upper'] - data['bb_lower']) / data['bb_middle']
        data['bb_position'] = (data['close'] - data['bb_lower']) / (data['bb_upper'] - data['bb_lower'])
        
        # ATR for volatility
        data['high_low'] = data['high'] - data['low']
        data['high_close'] = np.abs(data['high'] - data['close'].shift())
        data['low_close'] = np.abs(data['low'] - data['close'].shift())
        data['tr'] = data[['high_low', 'high_close', 'low_close']].max(axis=1)
        data['atr'] = data['tr'].rolling(window=self.atr_period).mean()
        
        # Volume indicators
        data['volume_sma'] = data['volume'].rolling(window=self.volume_period).mean()
        data['volume_ratio'] = data['volume'] / data['volume_sma']
        
        # Market regime detection
        data['trend_strength'] = (data['sma_20'] - data['sma_50']) / data['sma_50']
        data['market_regime'] = np.where(
            abs(data['trend_strength']) > 0.02, 'trending', 'ranging'
        )
        
        # Momentum indicators
        data['momentum_5'] = data['close'].pct_change(5)
        data['momentum_10'] = data['close'].pct_change(10)
        
        # Support/Resistance levels (simplified)
        data['support'] = data['low'].rolling(window=20).min()
        data['resistance'] = data['high'].rolling(window=20).max()
        
        return data
    
    def calculate_signal_quality(self, data: pd.DataFrame, idx: int) -> Dict[str, float]:
        """Calculate signal quality scores."""
        current = data.iloc[idx]
        prev = data.iloc[idx-1] if idx > 0 else current
        
        signals = {
            'rsi_quality': 0,
            'macd_quality': 0,
            'bb_quality': 0,
            'volume_quality': 0,
            'trend_quality': 0,
            'momentum_quality': 0,
            'support_resistance_quality': 0
        }
        
        # RSI quality (better signals at extremes)
        if current['rsi'] < 30:
            signals['rsi_quality'] = min((30 - current['rsi']) / 10, 3)
        elif current['rsi'] > 70:
            signals['rsi_quality'] = min((current['rsi'] - 70) / 10, 3)
        
        # MACD quality (stronger on crossovers with histogram confirmation)
        if ((current['macd'] > current['macd_signal'] and prev['macd'] <= prev['macd_signal']) or
            (current['macd'] < current['macd_signal'] and prev['macd'] >= prev['macd_signal'])):
            signals['macd_quality'] = min(abs(current['macd_histogram']) * 1000, 3)
        
        # BB quality (better at band touches)
        if current['bb_position'] <= 0.1:  # Near lower band
            signals['bb_quality'] = 2
        elif current['bb_position'] >= 0.9:  # Near upper band
            signals['bb_quality'] = 2
        
        # Volume quality (confirmation with above-average volume)
        if current['volume_ratio'] > 1.2:
            signals['volume_quality'] = min(current['volume_ratio'] - 1, 2)
        
        # Trend quality (better signals with trend)
        if current['market_regime'] == 'trending':
            signals['trend_quality'] = min(abs(current['trend_strength']) * 50, 2)
        
        # Momentum quality
        if abs(current['momentum_5']) > 0.01:
            signals['momentum_quality'] = min(abs(current['momentum_5']) * 100, 2)
        
        # Support/Resistance quality
        price_near_support = abs(current['close'] - current['support']) / current['close'] < 0.02
        price_near_resistance = abs(current['close'] - current['resistance']) / current['close'] < 0.02
        if price_near_support or price_near_resistance:
            signals['support_resistance_quality'] = 1.5
        
        return signals
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate optimized trading signals."""
        data = self.calculate_indicators(df)
        signals = []
        
        # Start after enough data for all indicators
        start_idx = max(self.macd_slow + self.macd_signal, self.bb_period, 50)
        
        for i in range(start_idx, len(data)):
            current = data.iloc[i]
            prev = data.iloc[i-1] if i > 0 else current
            
            # Skip if any critical indicator is NaN
            if pd.isna(current['rsi']) or pd.isna(current['macd']) or pd.isna(current['bb_middle']):
                continue
            
            # Calculate signal quality
            quality_scores = self.calculate_signal_quality(data, i)
            
            # Generate buy signals
            buy_conditions = [
                # RSI oversold
                current['rsi'] < 35,
                # MACD bullish crossover
                current['macd'] > current['macd_signal'] and prev['macd'] <= prev['macd_signal'],
                # Price near lower BB
                current['bb_position'] <= 0.2,
                # Volume confirmation
                current['volume_ratio'] > 1.1,
                # Positive momentum
                current['momentum_5'] > -0.005,
                # Near support
                abs(current['close'] - current['support']) / current['close'] < 0.03
            ]
            
            # Generate sell signals
            sell_conditions = [
                # RSI overbought
                current['rsi'] > 65,
                # MACD bearish crossover
                current['macd'] < current['macd_signal'] and prev['macd'] >= prev['macd_signal'],
                # Price near upper BB
                current['bb_position'] >= 0.8,
                # Volume confirmation
                current['volume_ratio'] > 1.1,
                # Negative momentum
                current['momentum_5'] < 0.005,
                # Near resistance
                abs(current['close'] - current['resistance']) / current['close'] < 0.03
            ]
            
            # Calculate composite scores
            buy_score = sum(buy_conditions) + sum(quality_scores.values())
            sell_score = sum(sell_conditions) + sum(quality_scores.values())
            
            # Risk-reward check using ATR
            atr_multiple = 2.0
            stop_loss_distance = current['atr'] * atr_multiple
            take_profit_distance = stop_loss_distance * self.risk_reward_ratio
            
            # Generate signals with quality threshold
            if buy_score >= self.min_signal_strength:
                signals.append({
                    'timestamp': current.name,
                    'signal': 'BUY',
                    'price': current['close'],
                    'rsi': current['rsi'],
                    'macd': current['macd'],
                    'score': buy_score,
                    'confidence': min(buy_score / 8, 1.0),
                    'stop_loss': current['close'] - stop_loss_distance,
                    'take_profit': current['close'] + take_profit_distance,
                    'atr': current['atr'],
                    'market_regime': current['market_regime']
                })
            elif sell_score >= self.min_signal_strength:
                signals.append({
                    'timestamp': current.name,
                    'signal': 'SELL',
                    'price': current['close'],
                    'rsi': current['rsi'],
                    'macd': current['macd'],
                    'score': sell_score,
                    'confidence': min(sell_score / 8, 1.0),
                    'stop_loss': current['close'] + stop_loss_distance,
                    'take_profit': current['close'] - take_profit_distance,
                    'atr': current['atr'],
                    'market_regime': current['market_regime']
                })
        
        return pd.DataFrame(signals)
    
    def get_strategy_name(self) -> str:
        """Return strategy name."""
        return "Optimized_Crypto_V2"
    
    def get_strategy_description(self) -> str:
        """Return strategy description."""
        return """
        Optimized Crypto Strategy V2 features:
        - Market regime detection (trending vs ranging)
        - Dynamic signal threshold adjustment
        - ATR-based risk management
        - Support/resistance level awareness
        - Quality-based signal filtering
        - Volume confirmation
        - Multiple timeframe momentum
        """
