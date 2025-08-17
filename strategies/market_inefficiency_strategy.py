"""
AlgoProject - Market Inefficiency & Arbitrage Strategy (Simplified)
Advanced strategy for exploiting market inefficiencies and arbitrage opportunities
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("⚠️  Scipy not available. Install with: pip install scipy")


class MarketInefficiencyStrategy:
    """
    Advanced Market Inefficiency and Arbitrage Strategy
    
    This strategy identifies and exploits various market inefficiencies:
    1. Statistical Arbitrage
    2. Mean Reversion Opportunities
    3. Volatility Arbitrage
    4. Time-based Inefficiencies
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        self.name = "Market Inefficiency Strategy"
        
        # State tracking
        self.active_opportunities = []
        self.historical_performance = {}
        self.risk_metrics = {}
        
    def _default_config(self) -> Dict:
        return {
            'min_data_points': 50,
            'mean_reversion_window': 20,
            'volatility_window': 10,
            'confidence_threshold': 0.6,
            'max_position_size': 0.1,
            'stop_loss_pct': 0.02,
            'take_profit_pct': 0.05,
            'risk_per_trade': 0.02
        }
    
    def generate_signals(self, data: pd.DataFrame, 
                        additional_data: Dict[str, pd.DataFrame] = None) -> List[Dict]:
        """
        Generate trading signals based on identified inefficiencies
        """
        signals = []
        
        if len(data) < self.config['min_data_points']:
            return signals
        
        try:
            # 1. Mean Reversion Signals
            mean_reversion_signals = self._detect_mean_reversion(data)
            signals.extend(mean_reversion_signals)
            
            # 2. Volatility Arbitrage
            volatility_signals = self._detect_volatility_arbitrage(data)
            signals.extend(volatility_signals)
            
            # 3. Statistical Arbitrage
            statistical_signals = self._detect_statistical_arbitrage(data)
            signals.extend(statistical_signals)
            
            # 4. Time-based Inefficiencies
            time_signals = self._detect_time_inefficiencies(data)
            signals.extend(time_signals)
            
        except Exception as e:
            print(f"⚠️  Error generating signals: {e}")
        
        return signals
    
    def _detect_mean_reversion(self, data: pd.DataFrame) -> List[Dict]:
        """Detect mean reversion opportunities"""
        signals = []
        
        try:
            if len(data) < 20:
                return signals
            
            # Bollinger Bands mean reversion
            window = self.config['mean_reversion_window']
            sma = data['close'].rolling(window).mean()
            std = data['close'].rolling(window).std()
            
            upper_band = sma + (2 * std)
            lower_band = sma - (2 * std)
            
            current_price = data['close'].iloc[-1]
            
            if len(sma.dropna()) > 0:
                current_sma = sma.iloc[-1]
                current_upper = upper_band.iloc[-1]
                current_lower = lower_band.iloc[-1]
                
                if current_price > current_upper:  # Above upper band
                    signals.append({
                        'signal_type': 'SELL',
                        'strategy': 'mean_reversion',
                        'entry_price': current_price,
                        'target_price': current_sma,
                        'stop_loss': current_price * 1.02,
                        'confidence': 0.7,
                        'expected_return': (current_sma - current_price) / current_price,
                        'holding_period': 5,
                        'timestamp': data.index[-1]
                    })
                
                elif current_price < current_lower:  # Below lower band
                    signals.append({
                        'signal_type': 'BUY',
                        'strategy': 'mean_reversion',
                        'entry_price': current_price,
                        'target_price': current_sma,
                        'stop_loss': current_price * 0.98,
                        'confidence': 0.7,
                        'expected_return': (current_sma - current_price) / current_price,
                        'holding_period': 5,
                        'timestamp': data.index[-1]
                    })
            
        except Exception as e:
            print(f"⚠️  Error in mean reversion detection: {e}")
        
        return signals
    
    def _detect_volatility_arbitrage(self, data: pd.DataFrame) -> List[Dict]:
        """Detect volatility arbitrage opportunities"""
        signals = []
        
        try:
            if len(data) < 20:
                return signals
            
            # Calculate realized volatility
            returns = data['close'].pct_change()
            realized_vol = returns.rolling(10).std() * np.sqrt(252)
            
            # Calculate implied volatility proxy (ATR-based)
            high_low = data['high'] - data['low']
            high_close = abs(data['high'] - data['close'].shift())
            low_close = abs(data['low'] - data['close'].shift())
            
            true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = true_range.rolling(14).mean()
            implied_vol_proxy = atr / data['close'] * np.sqrt(252)
            
            if len(realized_vol.dropna()) > 0 and len(implied_vol_proxy.dropna()) > 0:
                current_realized = realized_vol.iloc[-1]
                current_implied = implied_vol_proxy.iloc[-1]
                
                vol_diff = current_implied - current_realized
                
                if abs(vol_diff) > 0.1:  # 10% volatility difference
                    signal_type = 'BUY' if vol_diff > 0 else 'SELL'
                    signals.append({
                        'signal_type': signal_type,
                        'strategy': 'volatility_arbitrage',
                        'entry_price': data['close'].iloc[-1],
                        'volatility_difference': vol_diff,
                        'confidence': min(abs(vol_diff) * 5, 0.9),
                        'expected_return': abs(vol_diff) * 0.5,
                        'holding_period': 3,
                        'timestamp': data.index[-1]
                    })
            
        except Exception as e:
            print(f"⚠️  Error in volatility arbitrage detection: {e}")
        
        return signals
    
    def _detect_statistical_arbitrage(self, data: pd.DataFrame) -> List[Dict]:
        """Detect statistical arbitrage opportunities"""
        signals = []
        
        try:
            if len(data) < 30:
                return signals
            
            # Z-score based statistical arbitrage
            returns = data['close'].pct_change()
            z_scores = (returns - returns.mean()) / returns.std()
            
            current_z = z_scores.iloc[-1]
            
            if abs(current_z) > 2:  # 2 standard deviations
                signal_type = 'SELL' if current_z > 0 else 'BUY'
                signals.append({
                    'signal_type': signal_type,
                    'strategy': 'statistical_arbitrage',
                    'entry_price': data['close'].iloc[-1],
                    'z_score': current_z,
                    'confidence': min(abs(current_z) / 3, 0.9),
                    'expected_return': abs(current_z) * 0.01,
                    'holding_period': 2,
                    'timestamp': data.index[-1]
                })
            
        except Exception as e:
            print(f"⚠️  Error in statistical arbitrage detection: {e}")
        
        return signals
    
    def _detect_time_inefficiencies(self, data: pd.DataFrame) -> List[Dict]:
        """Detect time-based inefficiencies"""
        signals = []
        
        try:
            if len(data) < 100:
                return signals
            
            # Hour-of-day effects (if timestamp data available)
            if hasattr(data.index, 'hour'):
                returns = data['close'].pct_change()
                hourly_returns = returns.groupby(data.index.hour).mean()
                
                current_hour = data.index[-1].hour
                if current_hour in hourly_returns.index:
                    expected_return = hourly_returns[current_hour]
                    
                    if abs(expected_return) > 0.001:  # 0.1% threshold
                        signal_type = 'BUY' if expected_return > 0 else 'SELL'
                        signals.append({
                            'signal_type': signal_type,
                            'strategy': 'time_inefficiency',
                            'entry_price': data['close'].iloc[-1],
                            'hour_effect': current_hour,
                            'expected_return': expected_return,
                            'confidence': 0.4,
                            'holding_period': 1,
                            'timestamp': data.index[-1]
                        })
            
        except Exception as e:
            print(f"⚠️  Error in time inefficiency detection: {e}")
        
        return signals
    
    def calculate_position_size(self, signal: Dict, portfolio_value: float) -> float:
        """Calculate position size based on risk management"""
        try:
            risk_per_trade = self.config['risk_per_trade']
            confidence = signal.get('confidence', 0.5)
            
            # Adjust position size based on confidence
            base_position = portfolio_value * risk_per_trade
            adjusted_position = base_position * confidence
            
            # Ensure we don't exceed max position size
            max_position = portfolio_value * self.config['max_position_size']
            
            return min(adjusted_position, max_position)
            
        except Exception as e:
            print(f"⚠️  Error calculating position size: {e}")
            return 0.0
    
    def get_strategy_info(self) -> Dict:
        """Get strategy information"""
        return {
            'name': self.name,
            'description': 'Advanced Market Inefficiency and Arbitrage Strategy',
            'version': '2.0',
            'author': 'AlgoProject',
            'strategies': [
                'Mean Reversion',
                'Volatility Arbitrage', 
                'Statistical Arbitrage',
                'Time-based Inefficiencies'
            ],
            'risk_level': 'Medium',
            'time_horizon': 'Short to Medium-term',
            'market_conditions': 'All markets'
        }


# Test the strategy
if __name__ == "__main__":
    print("Testing Market Inefficiency Strategy...")
    
    # Create sample data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    prices = 100 + np.cumsum(np.random.randn(100) * 0.5)
    
    test_data = pd.DataFrame({
        'open': prices,
        'high': prices * 1.01,
        'low': prices * 0.99,
        'close': prices,
        'volume': np.random.randint(1000, 10000, 100)
    }, index=dates)
    
    strategy = MarketInefficiencyStrategy()
    signals = strategy.generate_signals(test_data)
    
    print(f"Generated {len(signals)} signals")
    for i, signal in enumerate(signals[:3]):  # Show first 3 signals
        print(f"Signal {i+1}: {signal}")
    
    print("Market Inefficiency Strategy test completed!")
