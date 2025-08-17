"""
Technical Scanner Module
Core scanning and signal detection functionality
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from tools.technical_analysis import (
    calculate_rsi, calculate_macd, calculate_bollinger_bands,
    calculate_vwap, calculate_sma, calculate_ema, calculate_stochastic, calculate_atr
)


class TechnicalScanner:
    """
    Technical analysis scanner for detecting trading opportunities
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the technical scanner
        
        Args:
            config: Scanner configuration dictionary
        """
        self.config = config or {
            'rsi_oversold': 30,
            'rsi_overbought': 70,
            'macd_signal_threshold': 0.001,
            'bb_deviation_threshold': 0.02,
            'volume_threshold': 1.5
        }
        
        self.signals = []
        self.results = {}
    
    def scan_rsi_signals(self, data: pd.DataFrame) -> List[Dict]:
        """
        Scan for RSI-based signals
        
        Args:
            data: OHLCV data
            
        Returns:
            List of RSI signals
        """
        signals = []
        
        if 'close' not in data.columns:
            return signals
            
        rsi = calculate_rsi(data['close'])
        
        # Find oversold conditions
        oversold_mask = rsi < self.config['rsi_oversold']
        overbought_mask = rsi > self.config['rsi_overbought']
        
        # Generate signals
        for i in range(len(data)):
            if oversold_mask.iloc[i]:
                signals.append({
                    'timestamp': data.index[i],
                    'type': 'RSI_OVERSOLD',
                    'value': rsi.iloc[i],
                    'signal': 'BUY',
                    'strength': 'STRONG' if rsi.iloc[i] < 20 else 'MEDIUM'
                })
            elif overbought_mask.iloc[i]:
                signals.append({
                    'timestamp': data.index[i],
                    'type': 'RSI_OVERBOUGHT',
                    'value': rsi.iloc[i],
                    'signal': 'SELL',
                    'strength': 'STRONG' if rsi.iloc[i] > 80 else 'MEDIUM'
                })
        
        return signals
    
    def scan_macd_signals(self, data: pd.DataFrame) -> List[Dict]:
        """
        Scan for MACD-based signals
        
        Args:
            data: OHLCV data
            
        Returns:
            List of MACD signals
        """
        signals = []
        
        if 'close' not in data.columns:
            return signals
            
        macd = calculate_macd(data['close'])
        
        # Find crossover signals
        macd_line = macd['macd']
        signal_line = macd['signal']
        
        # Bullish crossover (MACD crosses above signal)
        for i in range(1, len(data)):
            if (macd_line.iloc[i] > signal_line.iloc[i] and 
                macd_line.iloc[i-1] <= signal_line.iloc[i-1]):
                signals.append({
                    'timestamp': data.index[i],
                    'type': 'MACD_BULLISH_CROSSOVER',
                    'value': macd_line.iloc[i] - signal_line.iloc[i],
                    'signal': 'BUY',
                    'strength': 'MEDIUM'
                })
            # Bearish crossover (MACD crosses below signal)
            elif (macd_line.iloc[i] < signal_line.iloc[i] and 
                  macd_line.iloc[i-1] >= signal_line.iloc[i-1]):
                signals.append({
                    'timestamp': data.index[i],
                    'type': 'MACD_BEARISH_CROSSOVER',
                    'value': macd_line.iloc[i] - signal_line.iloc[i],
                    'signal': 'SELL',
                    'strength': 'MEDIUM'
                })
        
        return signals
    
    def scan_bollinger_bands_signals(self, data: pd.DataFrame) -> List[Dict]:
        """
        Scan for Bollinger Bands signals
        
        Args:
            data: OHLCV data
            
        Returns:
            List of Bollinger Bands signals
        """
        signals = []
        
        if 'close' not in data.columns:
            return signals
            
        bb = calculate_bollinger_bands(data['close'])
        
        # Find squeeze and expansion signals
        for i in range(len(data)):
            close_price = data['close'].iloc[i]
            upper_band = bb['upper'].iloc[i]
            lower_band = bb['lower'].iloc[i]
            
            # Band squeeze (price near lower band)
            if close_price <= lower_band * (1 + self.config['bb_deviation_threshold']):
                signals.append({
                    'timestamp': data.index[i],
                    'type': 'BB_LOWER_TOUCH',
                    'value': (close_price - lower_band) / lower_band,
                    'signal': 'BUY',
                    'strength': 'MEDIUM'
                })
            # Band expansion (price near upper band)
            elif close_price >= upper_band * (1 - self.config['bb_deviation_threshold']):
                signals.append({
                    'timestamp': data.index[i],
                    'type': 'BB_UPPER_TOUCH',
                    'value': (close_price - upper_band) / upper_band,
                    'signal': 'SELL',
                    'strength': 'MEDIUM'
                })
        
        return signals
    
    def scan_volume_signals(self, data: pd.DataFrame) -> List[Dict]:
        """
        Scan for volume-based signals
        
        Args:
            data: OHLCV data
            
        Returns:
            List of volume signals
        """
        signals = []
        
        if 'volume' not in data.columns:
            return signals
            
        # Calculate volume moving average
        volume_sma = calculate_sma(data['volume'], 20)
        
        # Find volume spikes
        for i in range(len(data)):
            current_volume = data['volume'].iloc[i]
            avg_volume = volume_sma.iloc[i]
            
            if pd.notna(avg_volume) and current_volume > avg_volume * self.config['volume_threshold']:
                signals.append({
                    'timestamp': data.index[i],
                    'type': 'VOLUME_SPIKE',
                    'value': current_volume / avg_volume,
                    'signal': 'WATCH',
                    'strength': 'HIGH' if current_volume > avg_volume * 2 else 'MEDIUM'
                })
        
        return signals
    
    def scan_comprehensive(self, data: pd.DataFrame, symbol: str = "") -> Dict:
        """
        Perform comprehensive technical analysis scan
        
        Args:
            data: OHLCV data
            symbol: Trading symbol (optional)
            
        Returns:
            Dictionary containing all scan results
        """
        results = {
            'symbol': symbol,
            'timestamp': pd.Timestamp.now(),
            'total_signals': 0,
            'buy_signals': 0,
            'sell_signals': 0,
            'watch_signals': 0,
            'signals': []
        }
        
        # Perform all scans
        rsi_signals = self.scan_rsi_signals(data)
        macd_signals = self.scan_macd_signals(data)
        bb_signals = self.scan_bollinger_bands_signals(data)
        volume_signals = self.scan_volume_signals(data)
        
        # Combine all signals
        all_signals = rsi_signals + macd_signals + bb_signals + volume_signals
        
        # Count signals by type
        for signal in all_signals:
            if signal['signal'] == 'BUY':
                results['buy_signals'] += 1
            elif signal['signal'] == 'SELL':
                results['sell_signals'] += 1
            elif signal['signal'] == 'WATCH':
                results['watch_signals'] += 1
        
        results['total_signals'] = len(all_signals)
        results['signals'] = all_signals
        
        return results
    
    def get_current_state(self, data: pd.DataFrame) -> Dict:
        """
        Get current technical analysis state
        
        Args:
            data: OHLCV data
            
        Returns:
            Dictionary with current technical indicators
        """
        if len(data) == 0:
            return {}
            
        current_state = {
            'timestamp': data.index[-1],
            'price': data['close'].iloc[-1],
            'indicators': {}
        }
        
        # Calculate current indicator values
        if 'close' in data.columns:
            rsi = calculate_rsi(data['close'])
            macd = calculate_macd(data['close'])
            bb = calculate_bollinger_bands(data['close'])
            
            current_state['indicators'] = {
                'rsi': rsi.iloc[-1] if len(rsi) > 0 else None,
                'macd': macd['macd'].iloc[-1] if len(macd['macd']) > 0 else None,
                'macd_signal': macd['signal'].iloc[-1] if len(macd['signal']) > 0 else None,
                'bb_upper': bb['upper'].iloc[-1] if len(bb['upper']) > 0 else None,
                'bb_middle': bb['middle'].iloc[-1] if len(bb['middle']) > 0 else None,
                'bb_lower': bb['lower'].iloc[-1] if len(bb['lower']) > 0 else None,
            }
        
        return current_state
    
    def filter_signals(self, signals: List[Dict], min_strength: str = "MEDIUM") -> List[Dict]:
        """
        Filter signals by minimum strength
        
        Args:
            signals: List of signals
            min_strength: Minimum signal strength to include
            
        Returns:
            Filtered list of signals
        """
        strength_order = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "STRONG": 4}
        min_level = strength_order.get(min_strength, 2)
        
        return [s for s in signals if strength_order.get(s.get('strength', 'MEDIUM'), 2) >= min_level]


def scan_multiple_symbols(symbols: List[str], data_dict: Dict[str, pd.DataFrame], 
                         config: Optional[Dict] = None) -> Dict:
    """
    Scan multiple symbols for trading opportunities
    
    Args:
        symbols: List of trading symbols
        data_dict: Dictionary mapping symbols to OHLCV data
        config: Scanner configuration
        
    Returns:
        Dictionary with scan results for all symbols
    """
    scanner = TechnicalScanner(config)
    results = {}
    
    for symbol in symbols:
        if symbol in data_dict:
            results[symbol] = scanner.scan_comprehensive(data_dict[symbol], symbol)
    
    return results


if __name__ == "__main__":
    # Test the scanner with sample data
    print("🔍 Technical Scanner Module - Testing")
    
    # Create sample data
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    np.random.seed(42)
    
    sample_data = pd.DataFrame({
        'open': 100 + np.cumsum(np.random.randn(100) * 0.3),
        'high': 102 + np.cumsum(np.random.randn(100) * 0.3),
        'low': 98 + np.cumsum(np.random.randn(100) * 0.3),
        'close': 100 + np.cumsum(np.random.randn(100) * 0.3),
        'volume': np.random.randint(1000, 10000, 100)
    }, index=dates)
    
    # Test scanner
    scanner = TechnicalScanner()
    results = scanner.scan_comprehensive(sample_data, "TEST_SYMBOL")
    
    print(f"Total signals found: {results['total_signals']}")
    print(f"Buy signals: {results['buy_signals']}")
    print(f"Sell signals: {results['sell_signals']}")
    print(f"Watch signals: {results['watch_signals']}")
    
    # Test current state
    state = scanner.get_current_state(sample_data)
    print(f"Current RSI: {state['indicators']['rsi']:.2f}")
    
    print("✅ Technical scanner working correctly!")
