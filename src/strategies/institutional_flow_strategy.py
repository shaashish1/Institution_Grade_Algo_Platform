"""
AlgoProject - Institutional Order Flow Strategy
Advanced strategy for detecting and following institutional trading patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

try:
    from scipy import stats
    from scipy.signal import find_peaks
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("⚠️  Scipy not available. Install with: pip install scipy")


class InstitutionalOrderFlowStrategy:
    """
    Advanced Institutional Order Flow Strategy
    Detects and follows institutional trading patterns using:
    - Volume Profile Analysis
    - Large Order Detection
    - Institutional Footprint Analysis
    - Smart Money Concepts
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        self.volume_profile = VolumeProfileAnalyzer()
        self.large_order_detector = LargeOrderDetector()
        self.institutional_footprint = InstitutionalFootprint()
        self.smart_money_concepts = SmartMoneyConcepts()
        
        # State tracking
        self.current_levels = []
        self.institutional_zones = []
        self.order_flow_imbalance = 0
        self.smart_money_bias = 0
        
    def _default_config(self) -> Dict:
        return {
            'volume_profile': {
                'poc_sensitivity': 0.1,  # Point of Control sensitivity
                'value_area_percent': 0.7,  # Value Area percentage
                'profile_periods': 20  # Periods for profile calculation
            },
            'large_orders': {
                'volume_threshold_multiplier': 3,  # Volume threshold multiplier
                'price_impact_threshold': 0.001,  # Minimum price impact
                'detection_window': 5  # Detection window in periods
            },
            'institutional_zones': {
                'zone_strength_threshold': 0.7,  # Zone strength threshold
                'zone_age_limit': 100,  # Maximum age of zones
                'min_touches': 2  # Minimum touches for zone validation
            },
            'smart_money': {
                'liquidity_threshold': 1.5,  # Liquidity grab threshold
                'manipulation_detection': True,  # Enable manipulation detection
                'accumulation_threshold': 0.6  # Accumulation strength threshold
            },
            'risk_management': {
                'max_risk_per_trade': 0.02,  # Maximum risk per trade
                'risk_reward_ratio': 2.0,  # Minimum risk-reward ratio
                'max_drawdown_threshold': 0.10  # Maximum drawdown threshold
            }
        }
    
    def analyze_market_structure(self, data: pd.DataFrame) -> Dict:
        """
        Analyze overall market structure for institutional activity
        """
        analysis = {
            'trend_direction': 0,
            'market_phase': 'consolidation',
            'institutional_bias': 0,
            'liquidity_levels': [],
            'supply_demand_zones': []
        }
        
        try:
            # Trend Analysis
            sma_20 = data['close'].rolling(20).mean()
            sma_50 = data['close'].rolling(50).mean()
            
            if len(data) >= 50:
                current_price = data['close'].iloc[-1]
                sma_20_val = sma_20.iloc[-1]
                sma_50_val = sma_50.iloc[-1]
                
                if current_price > sma_20_val > sma_50_val:
                    analysis['trend_direction'] = 1  # Uptrend
                    analysis['market_phase'] = 'uptrend'
                elif current_price < sma_20_val < sma_50_val:
                    analysis['trend_direction'] = -1  # Downtrend
                    analysis['market_phase'] = 'downtrend'
                else:
                    analysis['trend_direction'] = 0  # Sideways
                    analysis['market_phase'] = 'consolidation'
            
            # Institutional Bias Detection
            institutional_signals = self.detect_institutional_activity(data)
            analysis['institutional_bias'] = institutional_signals['overall_bias']
            
            # Liquidity Levels
            liquidity_levels = self.identify_liquidity_levels(data)
            analysis['liquidity_levels'] = liquidity_levels
            
            # Supply and Demand Zones
            supply_demand_zones = self.identify_supply_demand_zones(data)
            analysis['supply_demand_zones'] = supply_demand_zones
            
        except Exception as e:
            print(f"⚠️  Error in market structure analysis: {e}")
        
        return analysis
    
    def detect_institutional_activity(self, data: pd.DataFrame) -> Dict:
        """
        Detect institutional trading activity
        """
        signals = {
            'volume_anomalies': [],
            'price_action_signals': [],
            'order_flow_imbalance': 0,
            'smart_money_activity': 0,
            'overall_bias': 0
        }
        
        try:
            # Volume Analysis
            volume_profile_data = self.volume_profile.analyze(data)
            signals['volume_anomalies'] = volume_profile_data['anomalies']
            
            # Large Order Detection
            large_orders = self.large_order_detector.detect(data)
            signals['large_orders'] = large_orders
            
            # Institutional Footprint
            footprint_data = self.institutional_footprint.analyze(data)
            signals['order_flow_imbalance'] = footprint_data['order_flow_imbalance']
            
            # Smart Money Analysis
            smart_money_data = self.smart_money_concepts.analyze(data)
            signals['smart_money_activity'] = smart_money_data['activity_score']
            
            # Calculate overall bias
            bias_factors = []
            
            # Volume bias
            if len(signals['volume_anomalies']) > 0:
                volume_bias = np.mean([anomaly['direction'] for anomaly in signals['volume_anomalies']])
                bias_factors.append(volume_bias * 0.3)
            
            # Order flow bias
            if abs(signals['order_flow_imbalance']) > 0.1:
                bias_factors.append(signals['order_flow_imbalance'] * 0.4)
            
            # Smart money bias
            if abs(signals['smart_money_activity']) > 0.1:
                bias_factors.append(signals['smart_money_activity'] * 0.3)
            
            signals['overall_bias'] = np.mean(bias_factors) if bias_factors else 0
            
        except Exception as e:
            print(f"⚠️  Error in institutional activity detection: {e}")
        
        return signals
    
    def identify_liquidity_levels(self, data: pd.DataFrame) -> List[Dict]:
        """
        Identify key liquidity levels where institutions might place orders
        """
        liquidity_levels = []
        
        try:
            # Support and Resistance Levels
            highs = data['high'].rolling(10).max()
            lows = data['low'].rolling(10).min()
            
            # Find significant levels
            for i in range(10, len(data) - 10):
                current_high = data['high'].iloc[i]
                current_low = data['low'].iloc[i]
                
                # Resistance level
                if current_high == highs.iloc[i]:
                    touches = sum(1 for j in range(max(0, i-20), min(len(data), i+20)) 
                                 if abs(data['high'].iloc[j] - current_high) / current_high < 0.002)
                    if touches >= 2:
                        liquidity_levels.append({
                            'level': current_high,
                            'type': 'resistance',
                            'strength': touches,
                            'age': len(data) - i,
                            'volume': data['volume'].iloc[i]
                        })
                
                # Support level
                if current_low == lows.iloc[i]:
                    touches = sum(1 for j in range(max(0, i-20), min(len(data), i+20)) 
                                 if abs(data['low'].iloc[j] - current_low) / current_low < 0.002)
                    if touches >= 2:
                        liquidity_levels.append({
                            'level': current_low,
                            'type': 'support',
                            'strength': touches,
                            'age': len(data) - i,
                            'volume': data['volume'].iloc[i]
                        })
            
            # Sort by strength and recency
            liquidity_levels.sort(key=lambda x: (x['strength'], -x['age']), reverse=True)
            
        except Exception as e:
            print(f"⚠️  Error identifying liquidity levels: {e}")
        
        return liquidity_levels[:10]  # Return top 10 levels
    
    def identify_supply_demand_zones(self, data: pd.DataFrame) -> List[Dict]:
        """
        Identify supply and demand zones based on institutional activity
        """
        zones = []
        
        try:
            # Look for strong moves away from levels
            for i in range(20, len(data) - 5):
                # Check for demand zone (strong move up)
                if i >= 5:
                    recent_low = data['low'].iloc[i-5:i+1].min()
                    future_high = data['high'].iloc[i:i+5].max()
                    
                    if future_high / recent_low > 1.02:  # 2% move
                        # Check volume confirmation
                        avg_volume = data['volume'].iloc[i-10:i].mean()
                        breakout_volume = data['volume'].iloc[i:i+3].mean()
                        
                        if breakout_volume > avg_volume * 1.5:
                            zones.append({
                                'zone_start': recent_low * 0.999,
                                'zone_end': recent_low * 1.001,
                                'type': 'demand',
                                'strength': breakout_volume / avg_volume,
                                'age': len(data) - i,
                                'test_count': 0
                            })
                
                # Check for supply zone (strong move down)
                if i >= 5:
                    recent_high = data['high'].iloc[i-5:i+1].max()
                    future_low = data['low'].iloc[i:i+5].min()
                    
                    if recent_high / future_low > 1.02:  # 2% move
                        # Check volume confirmation
                        avg_volume = data['volume'].iloc[i-10:i].mean()
                        breakdown_volume = data['volume'].iloc[i:i+3].mean()
                        
                        if breakdown_volume > avg_volume * 1.5:
                            zones.append({
                                'zone_start': recent_high * 0.999,
                                'zone_end': recent_high * 1.001,
                                'type': 'supply',
                                'strength': breakdown_volume / avg_volume,
                                'age': len(data) - i,
                                'test_count': 0
                            })
            
            # Remove overlapping zones and sort by strength
            zones = self._remove_overlapping_zones(zones)
            zones.sort(key=lambda x: x['strength'], reverse=True)
            
        except Exception as e:
            print(f"⚠️  Error identifying supply/demand zones: {e}")
        
        return zones[:15]  # Return top 15 zones
    
    def _remove_overlapping_zones(self, zones: List[Dict]) -> List[Dict]:
        """Remove overlapping supply/demand zones"""
        if not zones:
            return zones
        
        # Sort by strength (descending)
        zones.sort(key=lambda x: x['strength'], reverse=True)
        
        filtered_zones = []
        for zone in zones:
            is_overlapping = False
            for existing_zone in filtered_zones:
                # Check if zones overlap
                if (zone['zone_start'] <= existing_zone['zone_end'] and 
                    zone['zone_end'] >= existing_zone['zone_start']):
                    is_overlapping = True
                    break
            
            if not is_overlapping:
                filtered_zones.append(zone)
        
        return filtered_zones
    
    def generate_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate trading signals based on institutional order flow
        """
        signals = {
            'primary_signal': 0,
            'signal_strength': 0,
            'entry_reasons': [],
            'exit_reasons': [],
            'stop_loss': 0,
            'take_profit': 0,
            'risk_reward_ratio': 0
        }
        
        try:
            if len(data) < 50:
                return signals
            
            # Market Structure Analysis
            market_structure = self.analyze_market_structure(data)
            
            # Institutional Activity Detection
            institutional_activity = self.detect_institutional_activity(data)
            
            # Current price and levels
            current_price = data['close'].iloc[-1]
            current_high = data['high'].iloc[-1]
            current_low = data['low'].iloc[-1]
            
            # Signal generation logic
            signal_factors = []
            entry_reasons = []
            
            # Factor 1: Institutional Bias
            if abs(institutional_activity['overall_bias']) > 0.3:
                signal_factors.append(institutional_activity['overall_bias'] * 0.4)
                entry_reasons.append(f"Institutional bias: {institutional_activity['overall_bias']:.3f}")
            
            # Factor 2: Liquidity Level Interaction
            liquidity_levels = market_structure['liquidity_levels']
            for level in liquidity_levels[:3]:  # Top 3 levels
                distance = abs(current_price - level['level']) / current_price
                if distance < 0.005:  # Within 0.5%
                    level_signal = 1 if level['type'] == 'support' else -1
                    signal_factors.append(level_signal * 0.3)
                    entry_reasons.append(f"Near {level['type']} level: {level['level']:.2f}")
            
            # Factor 3: Supply/Demand Zone Interaction
            supply_demand_zones = market_structure['supply_demand_zones']
            for zone in supply_demand_zones[:3]:  # Top 3 zones
                if zone['zone_start'] <= current_price <= zone['zone_end']:
                    zone_signal = 1 if zone['type'] == 'demand' else -1
                    signal_factors.append(zone_signal * 0.3)
                    entry_reasons.append(f"In {zone['type']} zone: {zone['zone_start']:.2f}-{zone['zone_end']:.2f}")
            
            # Factor 4: Order Flow Imbalance
            if abs(institutional_activity['order_flow_imbalance']) > 0.2:
                signal_factors.append(institutional_activity['order_flow_imbalance'] * 0.2)
                entry_reasons.append(f"Order flow imbalance: {institutional_activity['order_flow_imbalance']:.3f}")
            
            # Calculate final signal
            if signal_factors:
                primary_signal = np.mean(signal_factors)
                signal_strength = min(abs(primary_signal), 1.0)
                
                # Convert to discrete signal
                if primary_signal > 0.4:
                    signals['primary_signal'] = 1  # Buy
                elif primary_signal < -0.4:
                    signals['primary_signal'] = -1  # Sell
                else:
                    signals['primary_signal'] = 0  # Hold
                
                signals['signal_strength'] = signal_strength
                signals['entry_reasons'] = entry_reasons
            
            # Risk Management
            if signals['primary_signal'] != 0:
                risk_management = self._calculate_risk_management(data, signals['primary_signal'])
                signals.update(risk_management)
            
        except Exception as e:
            print(f"⚠️  Error generating signals: {e}")
        
        return signals
    
    def _calculate_risk_management(self, data: pd.DataFrame, signal: int) -> Dict:
        """
        Calculate stop loss, take profit, and risk-reward ratio
        """
        risk_params = {
            'stop_loss': 0,
            'take_profit': 0,
            'risk_reward_ratio': 0
        }
        
        try:
            current_price = data['close'].iloc[-1]
            atr = self._calculate_atr(data, period=14)
            
            if atr > 0:
                if signal == 1:  # Buy signal
                    # Stop loss below recent low or ATR-based
                    recent_low = data['low'].iloc[-10:].min()
                    atr_stop = current_price - (atr * 2)
                    risk_params['stop_loss'] = max(recent_low, atr_stop)
                    
                    # Take profit based on risk-reward ratio
                    risk_amount = current_price - risk_params['stop_loss']
                    risk_params['take_profit'] = current_price + (risk_amount * self.config['risk_management']['risk_reward_ratio'])
                    
                elif signal == -1:  # Sell signal
                    # Stop loss above recent high or ATR-based
                    recent_high = data['high'].iloc[-10:].max()
                    atr_stop = current_price + (atr * 2)
                    risk_params['stop_loss'] = min(recent_high, atr_stop)
                    
                    # Take profit based on risk-reward ratio
                    risk_amount = risk_params['stop_loss'] - current_price
                    risk_params['take_profit'] = current_price - (risk_amount * self.config['risk_management']['risk_reward_ratio'])
                
                # Calculate risk-reward ratio
                if signal == 1:
                    risk = current_price - risk_params['stop_loss']
                    reward = risk_params['take_profit'] - current_price
                elif signal == -1:
                    risk = risk_params['stop_loss'] - current_price
                    reward = current_price - risk_params['take_profit']
                
                if risk > 0:
                    risk_params['risk_reward_ratio'] = reward / risk
                
        except Exception as e:
            print(f"⚠️  Error calculating risk management: {e}")
        
        return risk_params
    
    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> float:
        """Calculate Average True Range"""
        try:
            high_low = data['high'] - data['low']
            high_close = np.abs(data['high'] - data['close'].shift())
            low_close = np.abs(data['low'] - data['close'].shift())
            
            true_range = np.maximum(high_low, np.maximum(high_close, low_close))
            atr = true_range.rolling(period).mean()
            
            return atr.iloc[-1] if not pd.isna(atr.iloc[-1]) else 0
        except:
            return 0


class VolumeProfileAnalyzer:
    """Volume Profile Analysis for institutional activity detection"""
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """Analyze volume profile"""
        analysis = {
            'point_of_control': 0,
            'value_area_high': 0,
            'value_area_low': 0,
            'volume_nodes': [],
            'anomalies': []
        }
        
        try:
            if len(data) < 20:
                return analysis
            
            # Create price levels
            price_range = data['high'].max() - data['low'].min()
            num_levels = min(50, len(data))
            price_levels = np.linspace(data['low'].min(), data['high'].max(), num_levels)
            
            # Calculate volume at each price level
            volume_at_price = {}
            for i, price in enumerate(price_levels):
                volume_at_price[price] = 0
                
                # For each bar, distribute volume across price levels it covers
                for j in range(len(data)):
                    if data['low'].iloc[j] <= price <= data['high'].iloc[j]:
                        # Simple volume distribution
                        volume_at_price[price] += data['volume'].iloc[j] / (data['high'].iloc[j] - data['low'].iloc[j] + 0.001)
            
            # Find Point of Control (highest volume)
            poc_price = max(volume_at_price.keys(), key=lambda x: volume_at_price[x])
            analysis['point_of_control'] = poc_price
            
            # Find Value Area (70% of volume)
            sorted_levels = sorted(volume_at_price.items(), key=lambda x: x[1], reverse=True)
            total_volume = sum(volume_at_price.values())
            target_volume = total_volume * 0.7
            
            cumulative_volume = 0
            value_area_prices = []
            
            for price, volume in sorted_levels:
                cumulative_volume += volume
                value_area_prices.append(price)
                if cumulative_volume >= target_volume:
                    break
            
            analysis['value_area_high'] = max(value_area_prices)
            analysis['value_area_low'] = min(value_area_prices)
            
            # Identify high volume nodes
            avg_volume = np.mean(list(volume_at_price.values()))
            high_volume_nodes = [(price, vol) for price, vol in volume_at_price.items() if vol > avg_volume * 2]
            analysis['volume_nodes'] = sorted(high_volume_nodes, key=lambda x: x[1], reverse=True)[:10]
            
            # Detect volume anomalies
            recent_volume = data['volume'].iloc[-5:].mean()
            avg_volume_total = data['volume'].mean()
            
            if recent_volume > avg_volume_total * 2:
                analysis['anomalies'].append({
                    'type': 'high_volume',
                    'direction': 1 if data['close'].iloc[-1] > data['open'].iloc[-1] else -1,
                    'strength': recent_volume / avg_volume_total
                })
            
        except Exception as e:
            print(f"⚠️  Error in volume profile analysis: {e}")
        
        return analysis


class LargeOrderDetector:
    """Detect large institutional orders"""
    
    def detect(self, data: pd.DataFrame) -> List[Dict]:
        """Detect large orders"""
        large_orders = []
        
        try:
            if len(data) < 10:
                return large_orders
            
            # Volume-based detection
            volume_ma = data['volume'].rolling(20).mean()
            volume_std = data['volume'].rolling(20).std()
            
            for i in range(20, len(data)):
                current_volume = data['volume'].iloc[i]
                threshold = volume_ma.iloc[i] + (3 * volume_std.iloc[i])
                
                if current_volume > threshold:
                    # Check price impact
                    price_change = abs(data['close'].iloc[i] - data['open'].iloc[i]) / data['open'].iloc[i]
                    
                    if price_change > 0.001:  # 0.1% minimum price impact
                        large_orders.append({
                            'timestamp': data.index[i],
                            'volume': current_volume,
                            'price_impact': price_change,
                            'direction': 1 if data['close'].iloc[i] > data['open'].iloc[i] else -1,
                            'strength': current_volume / volume_ma.iloc[i]
                        })
            
        except Exception as e:
            print(f"⚠️  Error in large order detection: {e}")
        
        return large_orders[-10:]  # Return last 10 orders


class InstitutionalFootprint:
    """Institutional footprint analysis"""
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """Analyze institutional footprint"""
        analysis = {
            'order_flow_imbalance': 0,
            'delta': 0,
            'cumulative_delta': 0,
            'absorption': []
        }
        
        try:
            if len(data) < 5:
                return analysis
            
            # Calculate delta (buy volume - sell volume approximation)
            deltas = []
            for i in range(len(data)):
                close_price = data['close'].iloc[i]
                open_price = data['open'].iloc[i]
                volume = data['volume'].iloc[i]
                
                if close_price > open_price:
                    # More buying pressure
                    delta = volume * 0.6  # 60% buy, 40% sell
                elif close_price < open_price:
                    # More selling pressure
                    delta = volume * -0.6  # 60% sell, 40% buy
                else:
                    # Neutral
                    delta = 0
                
                deltas.append(delta)
            
            analysis['delta'] = deltas[-1] if deltas else 0
            analysis['cumulative_delta'] = sum(deltas[-10:])  # Last 10 periods
            
            # Order flow imbalance
            recent_deltas = deltas[-5:]
            if recent_deltas:
                analysis['order_flow_imbalance'] = np.mean(recent_deltas) / data['volume'].iloc[-5:].mean()
            
        except Exception as e:
            print(f"⚠️  Error in institutional footprint analysis: {e}")
        
        return analysis


class SmartMoneyConcepts:
    """Smart Money Concepts analysis"""
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """Analyze smart money concepts"""
        analysis = {
            'activity_score': 0,
            'liquidity_grabs': [],
            'order_blocks': [],
            'fair_value_gaps': []
        }
        
        try:
            if len(data) < 20:
                return analysis
            
            # Liquidity grab detection
            liquidity_grabs = self._detect_liquidity_grabs(data)
            analysis['liquidity_grabs'] = liquidity_grabs
            
            # Order block detection
            order_blocks = self._detect_order_blocks(data)
            analysis['order_blocks'] = order_blocks
            
            # Fair value gap detection
            fair_value_gaps = self._detect_fair_value_gaps(data)
            analysis['fair_value_gaps'] = fair_value_gaps
            
            # Calculate activity score
            activity_factors = []
            if liquidity_grabs:
                activity_factors.append(len(liquidity_grabs) * 0.3)
            if order_blocks:
                activity_factors.append(len(order_blocks) * 0.4)
            if fair_value_gaps:
                activity_factors.append(len(fair_value_gaps) * 0.3)
            
            analysis['activity_score'] = min(sum(activity_factors), 1.0) if activity_factors else 0
            
        except Exception as e:
            print(f"⚠️  Error in smart money concepts analysis: {e}")
        
        return analysis
    
    def _detect_liquidity_grabs(self, data: pd.DataFrame) -> List[Dict]:
        """Detect liquidity grabs"""
        grabs = []
        
        try:
            # Look for stop runs followed by reversals
            for i in range(10, len(data) - 3):
                # Check for sweep of recent high/low
                recent_high = data['high'].iloc[i-10:i].max()
                recent_low = data['low'].iloc[i-10:i].min()
                
                current_high = data['high'].iloc[i]
                current_low = data['low'].iloc[i]
                
                # High liquidity grab
                if current_high > recent_high * 1.001:  # 0.1% above recent high
                    # Check for reversal
                    if data['close'].iloc[i:i+3].min() < data['close'].iloc[i]:
                        grabs.append({
                            'type': 'high_grab',
                            'level': current_high,
                            'timestamp': data.index[i],
                            'strength': (current_high - recent_high) / recent_high
                        })
                
                # Low liquidity grab
                if current_low < recent_low * 0.999:  # 0.1% below recent low
                    # Check for reversal
                    if data['close'].iloc[i:i+3].max() > data['close'].iloc[i]:
                        grabs.append({
                            'type': 'low_grab',
                            'level': current_low,
                            'timestamp': data.index[i],
                            'strength': (recent_low - current_low) / recent_low
                        })
            
        except Exception as e:
            print(f"⚠️  Error detecting liquidity grabs: {e}")
        
        return grabs[-5:]  # Return last 5 grabs
    
    def _detect_order_blocks(self, data: pd.DataFrame) -> List[Dict]:
        """Detect order blocks"""
        order_blocks = []
        
        try:
            # Look for strong moves away from levels
            for i in range(5, len(data) - 5):
                # Strong bullish move
                if data['close'].iloc[i+3] > data['close'].iloc[i] * 1.02:  # 2% move up
                    # Order block is the last down candle before the move
                    for j in range(i, -1, -1):
                        if data['close'].iloc[j] < data['open'].iloc[j]:  # Down candle
                            order_blocks.append({
                                'type': 'bullish_ob',
                                'high': data['high'].iloc[j],
                                'low': data['low'].iloc[j],
                                'timestamp': data.index[j],
                                'strength': (data['close'].iloc[i+3] - data['close'].iloc[i]) / data['close'].iloc[i]
                            })
                            break
                
                # Strong bearish move
                if data['close'].iloc[i+3] < data['close'].iloc[i] * 0.98:  # 2% move down
                    # Order block is the last up candle before the move
                    for j in range(i, -1, -1):
                        if data['close'].iloc[j] > data['open'].iloc[j]:  # Up candle
                            order_blocks.append({
                                'type': 'bearish_ob',
                                'high': data['high'].iloc[j],
                                'low': data['low'].iloc[j],
                                'timestamp': data.index[j],
                                'strength': (data['close'].iloc[i] - data['close'].iloc[i+3]) / data['close'].iloc[i]
                            })
                            break
            
        except Exception as e:
            print(f"⚠️  Error detecting order blocks: {e}")
        
        return order_blocks[-5:]  # Return last 5 order blocks
    
    def _detect_fair_value_gaps(self, data: pd.DataFrame) -> List[Dict]:
        """Detect fair value gaps"""
        gaps = []
        
        try:
            for i in range(1, len(data) - 1):
                # Bullish FVG: gap between previous high and next low
                if data['high'].iloc[i-1] < data['low'].iloc[i+1]:
                    gaps.append({
                        'type': 'bullish_fvg',
                        'gap_low': data['high'].iloc[i-1],
                        'gap_high': data['low'].iloc[i+1],
                        'timestamp': data.index[i],
                        'size': (data['low'].iloc[i+1] - data['high'].iloc[i-1]) / data['high'].iloc[i-1]
                    })
                
                # Bearish FVG: gap between previous low and next high
                if data['low'].iloc[i-1] > data['high'].iloc[i+1]:
                    gaps.append({
                        'type': 'bearish_fvg',
                        'gap_low': data['high'].iloc[i+1],
                        'gap_high': data['low'].iloc[i-1],
                        'timestamp': data.index[i],
                        'size': (data['low'].iloc[i-1] - data['high'].iloc[i+1]) / data['low'].iloc[i-1]
                    })
            
        except Exception as e:
            print(f"⚠️  Error detecting fair value gaps: {e}")
        
        return gaps[-5:]  # Return last 5 gaps


# Example usage and testing
if __name__ == "__main__":
    # Test the Institutional Order Flow Strategy
    print("🏦 Testing Institutional Order Flow Strategy")
    
    # Create sample data
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    
    sample_data = pd.DataFrame({
        'open': 100 + np.random.randn(len(dates)).cumsum() * 0.5,
        'high': 101 + np.random.randn(len(dates)).cumsum() * 0.5,
        'low': 99 + np.random.randn(len(dates)).cumsum() * 0.5,
        'close': 100 + np.random.randn(len(dates)).cumsum() * 0.5,
        'volume': np.random.randint(1000, 10000, len(dates))
    }, index=dates)
    
    # Ensure realistic OHLC relationships
    sample_data['high'] = np.maximum(sample_data[['open', 'close']].max(axis=1), sample_data['high'])
    sample_data['low'] = np.minimum(sample_data[['open', 'close']].min(axis=1), sample_data['low'])
    
    # Initialize strategy
    strategy = InstitutionalOrderFlowStrategy()
    
    # Test market structure analysis
    print("📊 Analyzing market structure...")
    market_structure = strategy.analyze_market_structure(sample_data)
    print(f"Trend Direction: {market_structure['trend_direction']}")
    print(f"Market Phase: {market_structure['market_phase']}")
    print(f"Institutional Bias: {market_structure['institutional_bias']:.3f}")
    print(f"Liquidity Levels: {len(market_structure['liquidity_levels'])}")
    print(f"Supply/Demand Zones: {len(market_structure['supply_demand_zones'])}")
    
    # Test signal generation
    print("\n🎯 Generating trading signals...")
    signals = strategy.generate_signals(sample_data)
    print(f"Primary Signal: {signals['primary_signal']}")
    print(f"Signal Strength: {signals['signal_strength']:.3f}")
    print(f"Entry Reasons: {signals['entry_reasons']}")
    
    if signals['primary_signal'] != 0:
        print(f"Stop Loss: {signals['stop_loss']:.2f}")
        print(f"Take Profit: {signals['take_profit']:.2f}")
        print(f"Risk-Reward Ratio: {signals['risk_reward_ratio']:.2f}")
    
    print("\n🏦 Institutional Order Flow Strategy test completed!")
