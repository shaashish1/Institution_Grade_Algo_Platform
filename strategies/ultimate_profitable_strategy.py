"""
AlgoProject - Ultimate Profitable Strategy
The most advanced and profitable trading strategy combining:
- Machine Learning and AI
- Institutional Order Flow Analysis
- Multi-timeframe Analysis
- Dynamic Risk Management
- Market Regime Detection
- Advanced Technical Analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# Import our custom strategies
try:
    from .ml_ai_framework import MLAITradingFramework
    from .institutional_flow_strategy import InstitutionalOrderFlowStrategy
    CUSTOM_STRATEGIES_AVAILABLE = True
except ImportError:
    # Fallback for standalone execution
    try:
        from ml_ai_framework import MLAITradingFramework
        from institutional_flow_strategy import InstitutionalOrderFlowStrategy
        CUSTOM_STRATEGIES_AVAILABLE = True
    except ImportError:
        CUSTOM_STRATEGIES_AVAILABLE = False
        print("⚠️  Custom strategies not available. Some features will be limited.")

try:
    from scipy import stats
    from scipy.signal import find_peaks
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("⚠️  Scipy not available. Install with: pip install scipy")


class UltimateProfitableStrategy:
    """
    The Ultimate Profitable Trading Strategy
    
    This strategy combines multiple advanced techniques:
    1. Machine Learning predictions
    2. Institutional order flow analysis
    3. Multi-timeframe confluence
    4. Dynamic risk management
    5. Market regime detection
    6. Advanced technical analysis
    7. Sentiment analysis
    8. Volatility-based position sizing
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        
        # Initialize sub-strategies
        if CUSTOM_STRATEGIES_AVAILABLE:
            self.ml_framework = MLAITradingFramework(self.config.get('ml_config', {}))
            self.institutional_strategy = InstitutionalOrderFlowStrategy(self.config.get('institutional_config', {}))
        else:
            self.ml_framework = None
            self.institutional_strategy = None
        
        # Initialize components
        self.market_regime_detector = MarketRegimeDetector()
        self.multi_timeframe_analyzer = MultiTimeframeAnalyzer()
        self.dynamic_risk_manager = DynamicRiskManager()
        self.advanced_technical_analyzer = AdvancedTechnicalAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        
        # Strategy state
        self.current_regime = 'neutral'
        self.confidence_threshold = 0.65
        self.min_confluence_score = 0.7
        self.trade_history = []
        self.performance_metrics = {}
        
        # Multi-timeframe data storage
        self.timeframe_data = {}
        
    def _default_config(self) -> Dict:
        return {
            'timeframes': {
                'primary': '1h',
                'secondary': '4h',
                'tertiary': '1d'
            },
            'ml_config': {
                'confidence_threshold': 0.6,
                'ensemble_weight': 0.35
            },
            'institutional_config': {
                'institutional_weight': 0.25,
                'flow_sensitivity': 0.7
            },
            'technical_config': {
                'technical_weight': 0.2,
                'momentum_threshold': 0.5
            },
            'sentiment_config': {
                'sentiment_weight': 0.1,
                'sentiment_threshold': 0.3
            },
            'risk_management': {
                'max_risk_per_trade': 0.02,
                'max_portfolio_risk': 0.06,
                'volatility_adjustment': True,
                'regime_adjustment': True,
                'dynamic_position_sizing': True
            },
            'confluence_requirements': {
                'min_signals': 3,
                'min_confluence_score': 0.7,
                'max_conflicting_signals': 1
            },
            'market_regimes': {
                'trend_threshold': 0.6,
                'volatility_threshold': 0.4,
                'regime_lookback': 50
            }
        }
    
    def analyze_market_regime(self, data: pd.DataFrame) -> Dict:
        """
        Detect current market regime for strategy adaptation
        """
        regime_analysis = self.market_regime_detector.detect_regime(data)
        self.current_regime = regime_analysis['current_regime']
        return regime_analysis
    
    def multi_timeframe_analysis(self, data_dict: Dict[str, pd.DataFrame]) -> Dict:
        """
        Perform multi-timeframe analysis for confluence
        """
        return self.multi_timeframe_analyzer.analyze(data_dict)
    
    def generate_ml_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate ML/AI-based trading signals
        """
        if not self.ml_framework:
            return {'signal': 0, 'confidence': 0, 'weight': 0}
        
        ml_prediction = self.ml_framework.predict(data)
        
        return {
            'signal': ml_prediction['signal'],
            'confidence': ml_prediction['confidence'],
            'weight': self.config['ml_config']['ensemble_weight'],
            'individual_predictions': ml_prediction.get('individual_predictions', {}),
            'reasoning': 'ML ensemble prediction'
        }
    
    def generate_institutional_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate institutional order flow signals
        """
        if not self.institutional_strategy:
            return {'signal': 0, 'confidence': 0, 'weight': 0}
        
        institutional_signals = self.institutional_strategy.generate_signals(data)
        
        return {
            'signal': institutional_signals['primary_signal'],
            'confidence': institutional_signals['signal_strength'],
            'weight': self.config['institutional_config']['institutional_weight'],
            'entry_reasons': institutional_signals['entry_reasons'],
            'reasoning': 'Institutional order flow analysis'
        }
    
    def generate_technical_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate advanced technical analysis signals
        """
        technical_analysis = self.advanced_technical_analyzer.analyze(data)
        
        return {
            'signal': technical_analysis['primary_signal'],
            'confidence': technical_analysis['signal_strength'],
            'weight': self.config['technical_config']['technical_weight'],
            'indicators': technical_analysis['indicators'],
            'reasoning': 'Advanced technical analysis'
        }
    
    def generate_sentiment_signals(self, data: pd.DataFrame) -> Dict:
        """
        Generate sentiment-based signals
        """
        sentiment_analysis = self.sentiment_analyzer.analyze(data)
        
        return {
            'signal': sentiment_analysis['signal'],
            'confidence': sentiment_analysis['confidence'],
            'weight': self.config['sentiment_config']['sentiment_weight'],
            'sentiment_score': sentiment_analysis['sentiment_score'],
            'reasoning': 'Market sentiment analysis'
        }
    
    def calculate_confluence_score(self, signals: List[Dict]) -> Dict:
        """
        Calculate confluence score from multiple signals
        """
        if not signals:
            return {'confluence_score': 0, 'final_signal': 0, 'consensus': 'none'}
        
        # Weighted signal calculation
        weighted_signals = []
        total_weight = 0
        signal_details = []
        
        for signal in signals:
            if signal['confidence'] > 0.3:  # Only consider confident signals
                weighted_signal = signal['signal'] * signal['weight'] * signal['confidence']
                weighted_signals.append(weighted_signal)
                total_weight += signal['weight'] * signal['confidence']
                
                signal_details.append({
                    'signal': signal['signal'],
                    'confidence': signal['confidence'],
                    'weight': signal['weight'],
                    'reasoning': signal.get('reasoning', 'Unknown')
                })
        
        if not weighted_signals:
            return {'confluence_score': 0, 'final_signal': 0, 'consensus': 'insufficient_data'}
        
        # Calculate final signal
        final_signal_raw = sum(weighted_signals) / total_weight if total_weight > 0 else 0
        
        # Convert to discrete signal
        if final_signal_raw > 0.5:
            final_signal = 1  # Buy
            consensus = 'bullish'
        elif final_signal_raw < -0.5:
            final_signal = -1  # Sell
            consensus = 'bearish'
        else:
            final_signal = 0  # Hold
            consensus = 'neutral'
        
        # Calculate confluence score
        signal_agreement = len([s for s in signals if s['signal'] == final_signal]) / len(signals)
        confidence_average = np.mean([s['confidence'] for s in signals])
        confluence_score = (signal_agreement * 0.6) + (confidence_average * 0.4)
        
        return {
            'confluence_score': confluence_score,
            'final_signal': final_signal,
            'consensus': consensus,
            'signal_strength': abs(final_signal_raw),
            'signal_details': signal_details,
            'total_signals': len(signals),
            'agreeing_signals': len([s for s in signals if s['signal'] == final_signal])
        }
    
    def calculate_position_size(self, data: pd.DataFrame, signal_strength: float, 
                              account_balance: float = 100000) -> Dict:
        """
        Calculate optimal position size using dynamic risk management
        """
        return self.dynamic_risk_manager.calculate_position_size(
            data, signal_strength, account_balance, self.current_regime
        )
    
    def generate_ultimate_signal(self, data: pd.DataFrame, 
                               multi_timeframe_data: Dict[str, pd.DataFrame] = None) -> Dict:
        """
        Generate the ultimate trading signal by combining all strategies
        """
        ultimate_signal = {
            'primary_signal': 0,
            'signal_strength': 0,
            'confluence_score': 0,
            'signals_breakdown': {},
            'entry_reasons': [],
            'risk_management': {},
            'market_regime': self.current_regime,
            'confidence_level': 'low',
            'trade_recommendation': 'hold'
        }
        
        try:
            # Step 1: Market Regime Detection
            regime_analysis = self.analyze_market_regime(data)
            ultimate_signal['market_regime'] = regime_analysis['current_regime']
            
            # Step 2: Multi-timeframe Analysis (if data available)
            if multi_timeframe_data:
                mtf_analysis = self.multi_timeframe_analysis(multi_timeframe_data)
                ultimate_signal['mtf_confluence'] = mtf_analysis
            
            # Step 3: Generate signals from all strategies
            signals = []
            
            # ML/AI Signals
            ml_signals = self.generate_ml_signals(data)
            if ml_signals['confidence'] > 0.3:
                signals.append(ml_signals)
                ultimate_signal['signals_breakdown']['ml_ai'] = ml_signals
            
            # Institutional Signals
            institutional_signals = self.generate_institutional_signals(data)
            if institutional_signals['confidence'] > 0.3:
                signals.append(institutional_signals)
                ultimate_signal['signals_breakdown']['institutional'] = institutional_signals
            
            # Technical Signals
            technical_signals = self.generate_technical_signals(data)
            if technical_signals['confidence'] > 0.3:
                signals.append(technical_signals)
                ultimate_signal['signals_breakdown']['technical'] = technical_signals
            
            # Sentiment Signals
            sentiment_signals = self.generate_sentiment_signals(data)
            if sentiment_signals['confidence'] > 0.3:
                signals.append(sentiment_signals)
                ultimate_signal['signals_breakdown']['sentiment'] = sentiment_signals
            
            # Step 4: Calculate confluence
            confluence_result = self.calculate_confluence_score(signals)
            ultimate_signal.update(confluence_result)
            
            # Step 5: Apply regime-based filters
            if self.current_regime == 'high_volatility' and confluence_result['confluence_score'] < 0.8:
                ultimate_signal['primary_signal'] = 0
                ultimate_signal['trade_recommendation'] = 'avoid_high_volatility'
            elif self.current_regime == 'low_volatility' and confluence_result['confluence_score'] < 0.6:
                ultimate_signal['primary_signal'] = 0
                ultimate_signal['trade_recommendation'] = 'insufficient_conviction'
            
            # Step 6: Final signal validation
            if confluence_result['confluence_score'] >= self.config['confluence_requirements']['min_confluence_score']:
                ultimate_signal['primary_signal'] = confluence_result['final_signal']
                ultimate_signal['confidence_level'] = self._determine_confidence_level(confluence_result['confluence_score'])
                
                # Generate entry reasons
                entry_reasons = []
                for signal_info in confluence_result['signal_details']:
                    if signal_info['signal'] == confluence_result['final_signal']:
                        entry_reasons.append(signal_info['reasoning'])
                
                ultimate_signal['entry_reasons'] = entry_reasons
                
                # Step 7: Risk Management
                if ultimate_signal['primary_signal'] != 0:
                    position_sizing = self.calculate_position_size(
                        data, 
                        confluence_result['signal_strength']
                    )
                    ultimate_signal['risk_management'] = position_sizing
                    
                    # Trade recommendation
                    if ultimate_signal['primary_signal'] == 1:
                        ultimate_signal['trade_recommendation'] = 'strong_buy' if confluence_result['confluence_score'] > 0.8 else 'buy'
                    elif ultimate_signal['primary_signal'] == -1:
                        ultimate_signal['trade_recommendation'] = 'strong_sell' if confluence_result['confluence_score'] > 0.8 else 'sell'
            else:
                ultimate_signal['trade_recommendation'] = 'insufficient_confluence'
            
            # Step 8: Performance tracking
            self._update_performance_metrics(ultimate_signal)
            
        except Exception as e:
            print(f"⚠️  Error in ultimate signal generation: {e}")
            ultimate_signal['error'] = str(e)
        
        return ultimate_signal
    
    def generate_signals(self, data: pd.DataFrame) -> List[Dict]:
        """
        Generate signals wrapper for compatibility
        """
        try:
            ultimate_signal = self.generate_ultimate_signal(data)
            if ultimate_signal.get('primary_signal', 0) != 0:
                return [{
                    'signal_type': 'BUY' if ultimate_signal['primary_signal'] > 0 else 'SELL',
                    'strategy': 'ultimate_profitable_strategy',
                    'confidence': ultimate_signal.get('confidence', 0),
                    'strength': ultimate_signal.get('signal_strength', 0),
                    'entry_price': data['close'].iloc[-1],
                    'stop_loss': ultimate_signal.get('stop_loss', 0),
                    'take_profit': ultimate_signal.get('take_profit', 0),
                    'timestamp': datetime.now()
                }]
            else:
                return []
        except Exception as e:
            print(f"⚠️  Error in generate_signals: {e}")
            return []
    
    def _determine_confidence_level(self, confluence_score: float) -> str:
        """Determine confidence level based on confluence score"""
        if confluence_score >= 0.9:
            return 'very_high'
        elif confluence_score >= 0.8:
            return 'high'
        elif confluence_score >= 0.7:
            return 'medium'
        elif confluence_score >= 0.6:
            return 'low'
        else:
            return 'very_low'
    
    def _update_performance_metrics(self, signal: Dict):
        """Update performance metrics"""
        if 'performance_metrics' not in self.__dict__:
            self.performance_metrics = {
                'total_signals': 0,
                'buy_signals': 0,
                'sell_signals': 0,
                'hold_signals': 0,
                'high_confidence_signals': 0,
                'average_confluence': 0
            }
        
        self.performance_metrics['total_signals'] += 1
        
        if signal['primary_signal'] == 1:
            self.performance_metrics['buy_signals'] += 1
        elif signal['primary_signal'] == -1:
            self.performance_metrics['sell_signals'] += 1
        else:
            self.performance_metrics['hold_signals'] += 1
        
        if signal['confidence_level'] in ['high', 'very_high']:
            self.performance_metrics['high_confidence_signals'] += 1
        
        # Update average confluence
        total_confluence = self.performance_metrics['average_confluence'] * (self.performance_metrics['total_signals'] - 1)
        total_confluence += signal['confluence_score']
        self.performance_metrics['average_confluence'] = total_confluence / self.performance_metrics['total_signals']
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary"""
        if not self.performance_metrics:
            return {'status': 'no_data'}
        
        total_signals = self.performance_metrics['total_signals']
        
        return {
            'total_signals_generated': total_signals,
            'buy_percentage': (self.performance_metrics['buy_signals'] / total_signals * 100) if total_signals > 0 else 0,
            'sell_percentage': (self.performance_metrics['sell_signals'] / total_signals * 100) if total_signals > 0 else 0,
            'hold_percentage': (self.performance_metrics['hold_signals'] / total_signals * 100) if total_signals > 0 else 0,
            'high_confidence_percentage': (self.performance_metrics['high_confidence_signals'] / total_signals * 100) if total_signals > 0 else 0,
            'average_confluence_score': self.performance_metrics['average_confluence'],
            'current_regime': self.current_regime
        }


class MarketRegimeDetector:
    """Detect market regimes for strategy adaptation"""
    
    def detect_regime(self, data: pd.DataFrame) -> Dict:
        """Detect current market regime"""
        regime_analysis = {
            'current_regime': 'neutral',
            'regime_strength': 0,
            'regime_duration': 0,
            'volatility_regime': 'normal',
            'trend_regime': 'sideways'
        }
        
        try:
            if len(data) < 50:
                return regime_analysis
            
            # Volatility regime
            returns = data['close'].pct_change().dropna()
            volatility = returns.rolling(20).std()
            current_vol = volatility.iloc[-1]
            avg_vol = volatility.mean()
            
            if current_vol > avg_vol * 1.5:
                regime_analysis['volatility_regime'] = 'high_volatility'
            elif current_vol < avg_vol * 0.7:
                regime_analysis['volatility_regime'] = 'low_volatility'
            else:
                regime_analysis['volatility_regime'] = 'normal_volatility'
            
            # Trend regime
            sma_20 = data['close'].rolling(20).mean()
            sma_50 = data['close'].rolling(50).mean()
            
            if len(sma_50.dropna()) > 0:
                if sma_20.iloc[-1] > sma_50.iloc[-1] * 1.02:
                    regime_analysis['trend_regime'] = 'uptrend'
                elif sma_20.iloc[-1] < sma_50.iloc[-1] * 0.98:
                    regime_analysis['trend_regime'] = 'downtrend'
                else:
                    regime_analysis['trend_regime'] = 'sideways'
            
            # Overall regime
            if regime_analysis['volatility_regime'] == 'high_volatility':
                regime_analysis['current_regime'] = 'high_volatility'
            elif regime_analysis['trend_regime'] == 'uptrend':
                regime_analysis['current_regime'] = 'bullish_trend'
            elif regime_analysis['trend_regime'] == 'downtrend':
                regime_analysis['current_regime'] = 'bearish_trend'
            else:
                regime_analysis['current_regime'] = 'consolidation'
            
            # Regime strength
            regime_analysis['regime_strength'] = min(abs(current_vol - avg_vol) / avg_vol, 1.0)
            
        except Exception as e:
            print(f"⚠️  Error in regime detection: {e}")
        
        return regime_analysis


class MultiTimeframeAnalyzer:
    """Multi-timeframe analysis for confluence"""
    
    def analyze(self, data_dict: Dict[str, pd.DataFrame]) -> Dict:
        """Analyze multiple timeframes for confluence"""
        mtf_analysis = {
            'timeframe_signals': {},
            'confluence_score': 0,
            'primary_direction': 0,
            'timeframe_agreement': 0
        }
        
        try:
            signals = []
            
            for timeframe, data in data_dict.items():
                if len(data) < 20:
                    continue
                
                # Simple trend analysis for each timeframe
                sma_10 = data['close'].rolling(10).mean()
                sma_20 = data['close'].rolling(20).mean()
                
                if len(sma_20.dropna()) > 0:
                    current_price = data['close'].iloc[-1]
                    sma_10_val = sma_10.iloc[-1]
                    sma_20_val = sma_20.iloc[-1]
                    
                    if current_price > sma_10_val > sma_20_val:
                        signal = 1  # Bullish
                    elif current_price < sma_10_val < sma_20_val:
                        signal = -1  # Bearish
                    else:
                        signal = 0  # Neutral
                    
                    signals.append(signal)
                    mtf_analysis['timeframe_signals'][timeframe] = signal
            
            if signals:
                # Calculate confluence
                bullish_count = sum(1 for s in signals if s == 1)
                bearish_count = sum(1 for s in signals if s == -1)
                total_count = len(signals)
                
                if bullish_count > bearish_count:
                    mtf_analysis['primary_direction'] = 1
                    mtf_analysis['confluence_score'] = bullish_count / total_count
                elif bearish_count > bullish_count:
                    mtf_analysis['primary_direction'] = -1
                    mtf_analysis['confluence_score'] = bearish_count / total_count
                else:
                    mtf_analysis['primary_direction'] = 0
                    mtf_analysis['confluence_score'] = 0
                
                mtf_analysis['timeframe_agreement'] = mtf_analysis['confluence_score']
            
        except Exception as e:
            print(f"⚠️  Error in multi-timeframe analysis: {e}")
        
        return mtf_analysis


class DynamicRiskManager:
    """Dynamic risk management with regime adaptation"""
    
    def calculate_position_size(self, data: pd.DataFrame, signal_strength: float, 
                              account_balance: float, regime: str) -> Dict:
        """Calculate optimal position size"""
        risk_params = {
            'position_size': 0,
            'stop_loss': 0,
            'take_profit': 0,
            'risk_reward_ratio': 0,
            'max_risk_amount': 0,
            'volatility_adjustment': 1.0,
            'regime_adjustment': 1.0
        }
        
        try:
            current_price = data['close'].iloc[-1]
            
            # Calculate ATR for volatility
            atr = self._calculate_atr(data)
            
            # Base risk per trade
            base_risk = 0.02  # 2%
            
            # Adjust for signal strength
            signal_adjustment = 0.5 + (signal_strength * 0.5)  # 0.5 to 1.0
            
            # Adjust for regime
            regime_adjustment = self._get_regime_adjustment(regime)
            
            # Adjust for volatility
            volatility_adjustment = self._get_volatility_adjustment(data)
            
            # Final risk percentage
            final_risk = base_risk * signal_adjustment * regime_adjustment * volatility_adjustment
            final_risk = min(final_risk, 0.05)  # Cap at 5%
            
            # Calculate position size
            max_risk_amount = account_balance * final_risk
            
            if atr > 0:
                # Use ATR-based stop loss
                stop_loss_distance = atr * 2
                position_size = max_risk_amount / stop_loss_distance
            else:
                # Fallback to percentage-based
                stop_loss_distance = current_price * 0.02  # 2% stop loss
                position_size = max_risk_amount / stop_loss_distance
            
            # Calculate stop loss and take profit
            if signal_strength > 0:  # Long position
                stop_loss = current_price - stop_loss_distance
                take_profit = current_price + (stop_loss_distance * 2)  # 2:1 RR
            else:  # Short position
                stop_loss = current_price + stop_loss_distance
                take_profit = current_price - (stop_loss_distance * 2)  # 2:1 RR
            
            risk_params.update({
                'position_size': position_size,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'risk_reward_ratio': 2.0,
                'max_risk_amount': max_risk_amount,
                'volatility_adjustment': volatility_adjustment,
                'regime_adjustment': regime_adjustment
            })
            
        except Exception as e:
            print(f"⚠️  Error in position sizing: {e}")
        
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
    
    def _get_regime_adjustment(self, regime: str) -> float:
        """Get regime-based adjustment factor"""
        adjustments = {
            'high_volatility': 0.5,
            'low_volatility': 1.2,
            'bullish_trend': 1.1,
            'bearish_trend': 0.9,
            'consolidation': 0.8,
            'neutral': 1.0
        }
        return adjustments.get(regime, 1.0)
    
    def _get_volatility_adjustment(self, data: pd.DataFrame) -> float:
        """Get volatility-based adjustment factor"""
        try:
            returns = data['close'].pct_change().dropna()
            volatility = returns.rolling(20).std().iloc[-1]
            
            if volatility > 0.03:  # High volatility
                return 0.7
            elif volatility < 0.01:  # Low volatility
                return 1.3
            else:
                return 1.0
        except:
            return 1.0


class AdvancedTechnicalAnalyzer:
    """Advanced technical analysis"""
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """Perform advanced technical analysis"""
        analysis = {
            'primary_signal': 0,
            'signal_strength': 0,
            'indicators': {},
            'momentum_score': 0,
            'trend_strength': 0
        }
        
        try:
            if len(data) < 50:
                return analysis
            
            # Multiple technical indicators
            indicators = {}
            
            # RSI
            rsi = self._calculate_rsi(data)
            indicators['rsi'] = rsi
            
            # MACD
            macd_data = self._calculate_macd(data)
            indicators['macd'] = macd_data
            
            # Bollinger Bands
            bb_data = self._calculate_bollinger_bands(data)
            indicators['bollinger_bands'] = bb_data
            
            # Stochastic
            stoch_data = self._calculate_stochastic(data)
            indicators['stochastic'] = stoch_data
            
            # Signal generation
            signals = []
            
            # RSI signals
            if rsi < 30:
                signals.append(1)  # Oversold
            elif rsi > 70:
                signals.append(-1)  # Overbought
            
            # MACD signals
            if macd_data['macd'] > macd_data['signal'] and macd_data['histogram'] > 0:
                signals.append(1)  # Bullish
            elif macd_data['macd'] < macd_data['signal'] and macd_data['histogram'] < 0:
                signals.append(-1)  # Bearish
            
            # Bollinger Bands signals
            if data['close'].iloc[-1] < bb_data['lower']:
                signals.append(1)  # Oversold
            elif data['close'].iloc[-1] > bb_data['upper']:
                signals.append(-1)  # Overbought
            
            # Calculate final signal
            if signals:
                signal_sum = sum(signals)
                if signal_sum > 0:
                    analysis['primary_signal'] = 1
                    analysis['signal_strength'] = min(signal_sum / len(signals), 1.0)
                elif signal_sum < 0:
                    analysis['primary_signal'] = -1
                    analysis['signal_strength'] = min(abs(signal_sum) / len(signals), 1.0)
            
            analysis['indicators'] = indicators
            
        except Exception as e:
            print(f"⚠️  Error in technical analysis: {e}")
        
        return analysis
    
    def _calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> float:
        """Calculate RSI"""
        try:
            delta = data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
        except:
            return 50
    
    def _calculate_macd(self, data: pd.DataFrame) -> Dict:
        """Calculate MACD"""
        try:
            ema_12 = data['close'].ewm(span=12).mean()
            ema_26 = data['close'].ewm(span=26).mean()
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9).mean()
            histogram = macd - signal
            
            return {
                'macd': macd.iloc[-1],
                'signal': signal.iloc[-1],
                'histogram': histogram.iloc[-1]
            }
        except:
            return {'macd': 0, 'signal': 0, 'histogram': 0}
    
    def _calculate_bollinger_bands(self, data: pd.DataFrame, period: int = 20) -> Dict:
        """Calculate Bollinger Bands"""
        try:
            sma = data['close'].rolling(period).mean()
            std = data['close'].rolling(period).std()
            upper = sma + (std * 2)
            lower = sma - (std * 2)
            
            return {
                'upper': upper.iloc[-1],
                'middle': sma.iloc[-1],
                'lower': lower.iloc[-1]
            }
        except:
            return {'upper': 0, 'middle': 0, 'lower': 0}
    
    def _calculate_stochastic(self, data: pd.DataFrame, period: int = 14) -> Dict:
        """Calculate Stochastic Oscillator"""
        try:
            low_14 = data['low'].rolling(period).min()
            high_14 = data['high'].rolling(period).max()
            k_percent = 100 * (data['close'] - low_14) / (high_14 - low_14)
            d_percent = k_percent.rolling(3).mean()
            
            return {
                'k': k_percent.iloc[-1],
                'd': d_percent.iloc[-1]
            }
        except:
            return {'k': 50, 'd': 50}


class SentimentAnalyzer:
    """Market sentiment analysis"""
    
    def analyze(self, data: pd.DataFrame) -> Dict:
        """Analyze market sentiment"""
        sentiment_analysis = {
            'signal': 0,
            'confidence': 0,
            'sentiment_score': 0,
            'fear_greed_index': 50
        }
        
        try:
            # Volume-based sentiment
            volume_ma = data['volume'].rolling(20).mean()
            recent_volume = data['volume'].iloc[-5:].mean()
            
            if recent_volume > volume_ma.iloc[-1] * 1.2:
                volume_sentiment = 0.3  # Positive
            elif recent_volume < volume_ma.iloc[-1] * 0.8:
                volume_sentiment = -0.3  # Negative
            else:
                volume_sentiment = 0  # Neutral
            
            # Price action sentiment
            price_changes = data['close'].pct_change().iloc[-10:]
            positive_days = sum(1 for change in price_changes if change > 0)
            
            if positive_days > 7:
                price_sentiment = 0.4  # Bullish
            elif positive_days < 3:
                price_sentiment = -0.4  # Bearish
            else:
                price_sentiment = 0  # Neutral
            
            # Combined sentiment
            sentiment_score = volume_sentiment + price_sentiment
            
            if sentiment_score > 0.3:
                sentiment_analysis['signal'] = 1
                sentiment_analysis['confidence'] = min(sentiment_score, 1.0)
            elif sentiment_score < -0.3:
                sentiment_analysis['signal'] = -1
                sentiment_analysis['confidence'] = min(abs(sentiment_score), 1.0)
            
            sentiment_analysis['sentiment_score'] = sentiment_score
            sentiment_analysis['fear_greed_index'] = 50 + (sentiment_score * 50)
            
        except Exception as e:
            print(f"⚠️  Error in sentiment analysis: {e}")
        
        return sentiment_analysis


# Example usage and testing
if __name__ == "__main__":
    # Test the Ultimate Profitable Strategy
    print("🚀 Testing Ultimate Profitable Strategy")
    
    # Create sample data
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='H')
    np.random.seed(42)
    
    sample_data = pd.DataFrame({
        'open': 100 + np.random.randn(len(dates)).cumsum() * 0.02,
        'high': 100.5 + np.random.randn(len(dates)).cumsum() * 0.02,
        'low': 99.5 + np.random.randn(len(dates)).cumsum() * 0.02,
        'close': 100 + np.random.randn(len(dates)).cumsum() * 0.02,
        'volume': np.random.randint(1000, 10000, len(dates))
    }, index=dates)
    
    # Ensure realistic OHLC relationships
    sample_data['high'] = np.maximum(sample_data[['open', 'close']].max(axis=1), sample_data['high'])
    sample_data['low'] = np.minimum(sample_data[['open', 'close']].min(axis=1), sample_data['low'])
    
    # Initialize strategy
    strategy = UltimateProfitableStrategy()
    
    # Test signal generation
    print("🎯 Generating ultimate trading signal...")
    
    # Create multi-timeframe data (simulated)
    multi_timeframe_data = {
        '1h': sample_data,
        '4h': sample_data.resample('4H').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna(),
        '1d': sample_data.resample('1D').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()
    }
    
    # Generate ultimate signal
    ultimate_signal = strategy.generate_ultimate_signal(sample_data, multi_timeframe_data)
    
    # Display results
    print(f"\n📊 ULTIMATE TRADING SIGNAL RESULTS")
    print(f"{'='*50}")
    print(f"Primary Signal: {ultimate_signal['primary_signal']}")
    print(f"Signal Strength: {ultimate_signal['signal_strength']:.3f}")
    print(f"Confluence Score: {ultimate_signal['confluence_score']:.3f}")
    print(f"Confidence Level: {ultimate_signal['confidence_level']}")
    print(f"Trade Recommendation: {ultimate_signal['trade_recommendation']}")
    print(f"Market Regime: {ultimate_signal['market_regime']}")
    
    print(f"\n🔍 SIGNALS BREAKDOWN:")
    for signal_type, signal_data in ultimate_signal['signals_breakdown'].items():
        print(f"  {signal_type.upper()}: Signal={signal_data['signal']}, Confidence={signal_data['confidence']:.3f}")
    
    if ultimate_signal['entry_reasons']:
        print(f"\n✅ ENTRY REASONS:")
        for reason in ultimate_signal['entry_reasons']:
            print(f"  • {reason}")
    
    if ultimate_signal['risk_management']:
        print(f"\n⚠️  RISK MANAGEMENT:")
        rm = ultimate_signal['risk_management']
        print(f"  Position Size: {rm['position_size']:.2f}")
        print(f"  Stop Loss: {rm['stop_loss']:.2f}")
        print(f"  Take Profit: {rm['take_profit']:.2f}")
        print(f"  Risk-Reward Ratio: {rm['risk_reward_ratio']:.2f}")
        print(f"  Max Risk Amount: ${rm['max_risk_amount']:.2f}")
    
    # Performance summary
    print(f"\n📈 PERFORMANCE SUMMARY:")
    performance = strategy.get_performance_summary()
    if performance.get('status') != 'no_data':
        print(f"  Total Signals: {performance['total_signals_generated']}")
        print(f"  Buy Signals: {performance['buy_percentage']:.1f}%")
        print(f"  Sell Signals: {performance['sell_percentage']:.1f}%")
        print(f"  Hold Signals: {performance['hold_percentage']:.1f}%")
        print(f"  High Confidence: {performance['high_confidence_percentage']:.1f}%")
        print(f"  Avg Confluence: {performance['average_confluence_score']:.3f}")
    
    print(f"\n🚀 Ultimate Profitable Strategy test completed!")
    print(f"{'='*50}")
