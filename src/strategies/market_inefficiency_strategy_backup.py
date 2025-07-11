"""
AlgoProject - Market Inefficiency & Arbitrage Strategy
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
    from scipy.optimize import minimize
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
    4. Pairs Trading
    5. Cross-Exchange Arbitrage
    6. Time-based Inefficiencies
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        
        # Initialize analyzers
        self.statistical_arbitrage = StatisticalArbitrage()
        self.mean_reversion_detector = MeanReversionDetector()
        self.volatility_arbitrage = VolatilityArbitrage()
        self.pairs_trading = PairsTrading()
        self.cross_exchange_arbitrage = CrossExchangeArbitrage()
        self.time_inefficiency_detector = TimeInefficiencyDetector()
        
        # State tracking
        self.active_opportunities = []
        self.historical_performance = {}
        self.risk_metrics = {}
        
    def _default_config(self) -> Dict:
        return {
            'statistical_arbitrage': {
                'lookback_period': 60,
                'zscore_threshold': 2.0,
                'half_life_threshold': 10,
                'min_correlation': 0.7
            },
            'mean_reversion': {
                'bollinger_period': 20,
                'bollinger_std': 2.0,
                'rsi_period': 14,
                'rsi_oversold': 30,
                'rsi_overbought': 70
            },
            'volatility_arbitrage': {
                'vol_window': 20,
                'vol_threshold': 0.5,
                'iv_rv_threshold': 0.2
            },
            'pairs_trading': {
                'correlation_threshold': 0.8,
                'cointegration_threshold': 0.05,
                'spread_threshold': 2.0
            },
            'cross_exchange': {
                'min_spread_threshold': 0.001,
                'max_spread_threshold': 0.05,
                'execution_cost': 0.002
            },
            'time_inefficiency': {
                'time_windows': ['09:30-10:00', '15:30-16:00'],
                'pattern_length': 5,
                'significance_threshold': 0.05
            },
            'risk_management': {
                'max_position_size': 0.05,
                'max_drawdown': 0.02,
                'correlation_limit': 0.3,
                'max_holding_period': 10
            }
        }
    
    def identify_inefficiencies(self, data: pd.DataFrame, 
                              additional_data: Dict[str, pd.DataFrame] = None) -> Dict:
        """
        Identify all types of market inefficiencies
        """
        inefficiencies = {
            'statistical_arbitrage': [],
            'mean_reversion': [],
            'volatility_arbitrage': [],
            'pairs_trading': [],
            'cross_exchange': [],
            'time_inefficiencies': [],
            'total_opportunities': 0,
            'confidence_scores': {}
        }
        
        try:
            # 1. Statistical Arbitrage
            stat_arb_opportunities = self.statistical_arbitrage.find_opportunities(data)
            inefficiencies['statistical_arbitrage'] = stat_arb_opportunities
            
            # 2. Mean Reversion
            mean_reversion_opportunities = self.mean_reversion_detector.detect(data)
            inefficiencies['mean_reversion'] = mean_reversion_opportunities
            
            # 3. Volatility Arbitrage
            vol_arb_opportunities = self.volatility_arbitrage.find_opportunities(data)
            inefficiencies['volatility_arbitrage'] = vol_arb_opportunities
            
            # 4. Pairs Trading (if additional data provided)
            if additional_data:
                pairs_opportunities = self.pairs_trading.find_pairs(data, additional_data)
                inefficiencies['pairs_trading'] = pairs_opportunities
            
            # 5. Cross-Exchange Arbitrage (if multiple exchange data provided)
            if additional_data and 'exchanges' in additional_data:
                cross_exchange_opportunities = self.cross_exchange_arbitrage.find_opportunities(
                    data, additional_data['exchanges']
                )
                inefficiencies['cross_exchange'] = cross_exchange_opportunities
            
            # 6. Time-based Inefficiencies
            time_inefficiencies = self.time_inefficiency_detector.detect(data)
            inefficiencies['time_inefficiencies'] = time_inefficiencies
            
            # Calculate total opportunities
            total_opportunities = sum(len(opps) for opps in inefficiencies.values() if isinstance(opps, list))
            inefficiencies['total_opportunities'] = total_opportunities
            
            # Calculate confidence scores
            for category, opportunities in inefficiencies.items():
                if isinstance(opportunities, list) and opportunities:
                    avg_confidence = np.mean([opp.get('confidence', 0) for opp in opportunities])
                    inefficiencies['confidence_scores'][category] = avg_confidence
            
        except Exception as e:
            print(f"⚠️  Error identifying inefficiencies: {e}")
        
        return inefficiencies
    
    def generate_signals(self, data: pd.DataFrame, 
                        additional_data: Dict[str, pd.DataFrame] = None) -> Dict:
        """
        Generate trading signals based on identified inefficiencies
        """
        signals = {
            'primary_signal': 0,
            'signal_strength': 0,
            'opportunity_type': 'none',
            'entry_price': 0,
            'exit_price': 0,
            'stop_loss': 0,
            'take_profit': 0,
            'expected_return': 0,
            'risk_score': 0,
            'holding_period': 0,
            'confidence': 0
        }
        
        try:
            # Identify inefficiencies
            inefficiencies = self.identify_inefficiencies(data, additional_data)
            
            if inefficiencies['total_opportunities'] == 0:
                return signals
            
            # Find the best opportunity
            best_opportunity = self._select_best_opportunity(inefficiencies)
            
            if not best_opportunity:
                return signals
            
            # Generate signal based on best opportunity
            signals.update(self._generate_signal_from_opportunity(best_opportunity, data))
            
            # Add risk management
            signals.update(self._calculate_risk_management(signals, data))
            
        except Exception as e:
            print(f"⚠️  Error generating signals: {e}")
        
        return signals
    
    def _select_best_opportunity(self, inefficiencies: Dict) -> Optional[Dict]:
        """
        Select the best opportunity based on risk-adjusted returns
        """
        all_opportunities = []
        
        for category, opportunities in inefficiencies.items():
            if isinstance(opportunities, list):
                for opp in opportunities:
                    opp['category'] = category
                    all_opportunities.append(opp)
        
        if not all_opportunities:
            return None
        
        # Score opportunities based on risk-adjusted returns
        scored_opportunities = []
        for opp in all_opportunities:
            score = self._calculate_opportunity_score(opp)
            opp['score'] = score
            scored_opportunities.append(opp)
        
        # Return the best opportunity
        best_opportunity = max(scored_opportunities, key=lambda x: x['score'])
        return best_opportunity
    
    def _calculate_opportunity_score(self, opportunity: Dict) -> float:
        """
        Calculate risk-adjusted score for an opportunity
        """
        try:
            expected_return = opportunity.get('expected_return', 0)
            risk_score = opportunity.get('risk_score', 1)
            confidence = opportunity.get('confidence', 0.5)
            
            # Sharpe-like ratio
            if risk_score > 0:
                risk_adjusted_return = expected_return / risk_score
            else:
                risk_adjusted_return = 0
            
            # Final score incorporating confidence
            score = risk_adjusted_return * confidence
            
            return score
        except:
            return 0
    
    def _generate_signal_from_opportunity(self, opportunity: Dict, data: pd.DataFrame) -> Dict:
        """
        Generate trading signal from selected opportunity
        """
        signal_data = {
            'primary_signal': 0,
            'signal_strength': 0,
            'opportunity_type': opportunity.get('category', 'unknown'),
            'entry_price': data['close'].iloc[-1],
            'expected_return': opportunity.get('expected_return', 0),
            'risk_score': opportunity.get('risk_score', 1),
            'confidence': opportunity.get('confidence', 0.5),
            'holding_period': opportunity.get('holding_period', 5)
        }
        
        # Determine signal direction
        if opportunity.get('direction') == 'long' or opportunity.get('expected_return', 0) > 0:
            signal_data['primary_signal'] = 1
        elif opportunity.get('direction') == 'short' or opportunity.get('expected_return', 0) < 0:
            signal_data['primary_signal'] = -1
        
        # Signal strength based on confidence and expected return
        signal_data['signal_strength'] = min(
            abs(opportunity.get('expected_return', 0)) * opportunity.get('confidence', 0.5),
            1.0
        )
        
        return signal_data
    
    def _calculate_risk_management(self, signals: Dict, data: pd.DataFrame) -> Dict:
        """
        Calculate risk management parameters
        """
        risk_params = {
            'stop_loss': 0,
            'take_profit': 0,
            'position_size': 0,
            'max_loss': 0
        }
        
        try:
            current_price = data['close'].iloc[-1]
            expected_return = signals.get('expected_return', 0)
            
            if signals['primary_signal'] == 1:  # Long
                # Stop loss at 2% below entry
                risk_params['stop_loss'] = current_price * 0.98
                # Take profit based on expected return
                risk_params['take_profit'] = current_price * (1 + max(abs(expected_return), 0.01))
            elif signals['primary_signal'] == -1:  # Short
                # Stop loss at 2% above entry
                risk_params['stop_loss'] = current_price * 1.02
                # Take profit based on expected return
                risk_params['take_profit'] = current_price * (1 - max(abs(expected_return), 0.01))
            
            # Position size based on risk score
            risk_score = signals.get('risk_score', 1)
            base_position_size = self.config['risk_management']['max_position_size']
            risk_params['position_size'] = base_position_size / max(risk_score, 1)
            
            # Max loss calculation
            risk_params['max_loss'] = abs(current_price - risk_params['stop_loss']) * risk_params['position_size']
            
        except Exception as e:
            print(f"⚠️  Error calculating risk management: {e}")
        
        return risk_params


class StatisticalArbitrage:
    """Statistical arbitrage opportunity detection"""
    
    def find_opportunities(self, data: pd.DataFrame) -> List[Dict]:
        """Find statistical arbitrage opportunities"""
        opportunities = []
        
        try:
            if len(data) < 60:
                return opportunities
            
            # Z-score analysis
            returns = data['close'].pct_change().dropna()
            rolling_mean = returns.rolling(20).mean()
            rolling_std = returns.rolling(20).std()
            
            current_return = returns.iloc[-1]
            current_mean = rolling_mean.iloc[-1]
            current_std = rolling_std.iloc[-1]
            
            if current_std > 0:
                z_score = (current_return - current_mean) / current_std
                
                if abs(z_score) > 2.0:  # Significant deviation
                    opportunities.append({
                        'type': 'z_score_reversion',
                        'z_score': z_score,
                        'direction': 'short' if z_score > 0 else 'long',
                        'expected_return': -z_score * current_std,
                        'confidence': min(abs(z_score) / 3.0, 1.0),
                        'risk_score': abs(z_score) / 2.0,
                        'holding_period': 3
                    })
            
            # Momentum reversal
            short_ma = data['close'].rolling(5).mean()
            long_ma = data['close'].rolling(20).mean()
            
            if len(short_ma.dropna()) > 0 and len(long_ma.dropna()) > 0:
                ma_ratio = short_ma.iloc[-1] / long_ma.iloc[-1]
                
                if ma_ratio > 1.05:  # Overbought
                    opportunities.append({
                        'type': 'momentum_reversal',
                        'ma_ratio': ma_ratio,
                        'direction': 'short',
                        'expected_return': (1 - ma_ratio) * 0.5,
                        'confidence': min((ma_ratio - 1) * 10, 1.0),
                        'risk_score': (ma_ratio - 1) * 5,
                        'holding_period': 5
                    })
                elif ma_ratio < 0.95:  # Oversold
                    opportunities.append({
                        'type': 'momentum_reversal',
                        'ma_ratio': ma_ratio,
                        'direction': 'long',
                        'expected_return': (1 - ma_ratio) * 0.5,
                        'confidence': min((1 - ma_ratio) * 10, 1.0),
                        'risk_score': (1 - ma_ratio) * 5,
                        'holding_period': 5
                    })
            
        except Exception as e:
            print(f"⚠️  Error in statistical arbitrage: {e}")
        
        return opportunities


class MeanReversionDetector:
    """Mean reversion opportunity detection"""
    
    def detect(self, data: pd.DataFrame) -> List[Dict]:
        """Detect mean reversion opportunities"""
        opportunities = []
        
        try:
            if len(data) < 20:
                return opportunities
            
            # Bollinger Bands mean reversion
            sma = data['close'].rolling(20).mean()
            std = data['close'].rolling(20).std()
            
            upper_band = sma + (2 * std)
            lower_band = sma - (2 * std)
            
            current_price = data['close'].iloc[-1]
            
            if len(sma.dropna()) > 0:
                current_sma = sma.iloc[-1]
                current_upper = upper_band.iloc[-1]
                current_lower = lower_band.iloc[-1]
                
                if current_price > current_upper:  # Above upper band
                    opportunities.append({
                        'type': 'bollinger_reversion',
                        'direction': 'short',
                        'deviation': (current_price - current_upper) / current_upper,
                        'expected_return': (current_sma - current_price) / current_price,
                        'confidence': min((current_price - current_upper) / (current_upper - current_sma), 1.0),
                        'risk_score': 0.5,
                        'holding_period': 5
                    })
                elif current_price < current_lower:  # Below lower band
                    opportunities.append({
                        'type': 'bollinger_reversion',
                        'direction': 'long',
                        'deviation': (current_lower - current_price) / current_price,
                        'expected_return': (current_sma - current_price) / current_price,
                        'confidence': min((current_lower - current_price) / (current_sma - current_lower), 1.0),
                        'risk_score': 0.5,
                        'holding_period': 5
                    })
            
            # RSI mean reversion
            rsi = self._calculate_rsi(data)
            
            if rsi < 30:  # Oversold
                opportunities.append({
                    'type': 'rsi_reversion',
                    'direction': 'long',
                    'rsi': rsi,
                    'expected_return': (50 - rsi) / 1000,  # Rough estimate
                    'confidence': (30 - rsi) / 30,
                    'risk_score': 0.3,
                    'holding_period': 3
                })
            elif rsi > 70:  # Overbought
                opportunities.append({
                    'type': 'rsi_reversion',
                    'direction': 'short',
                    'rsi': rsi,
                    'expected_return': (rsi - 50) / 1000,  # Rough estimate
                    'confidence': (rsi - 70) / 30,
                    'risk_score': 0.3,
                    'holding_period': 3
                })
            
        except Exception as e:
            print(f"⚠️  Error in mean reversion detection: {e}")
        
        return opportunities
    
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


class VolatilityArbitrage:
    """Volatility arbitrage opportunity detection"""
    
    def find_opportunities(self, data: pd.DataFrame) -> List[Dict]:
        """Find volatility arbitrage opportunities"""
        opportunities = []
        
        try:
            if len(data) < 20:
                return opportunities
            
            # Calculate realized volatility
            returns = data['close'].pct_change().dropna()
            realized_vol = returns.rolling(20).std() * np.sqrt(252)  # Annualized
            
            # Check if we have valid volatility data
            if realized_vol.empty or realized_vol.dropna().empty:
                return opportunities
            
            try:
                current_vol = realized_vol.iloc[-1]
                vol_mean = realized_vol.mean()
                vol_std = realized_vol.std()
                
                # Check for valid values
                if pd.isna(current_vol) or pd.isna(vol_mean) or pd.isna(vol_std) or vol_std == 0:
                    return opportunities
            except (IndexError, ValueError):
                return opportunities
            
            # Volatility mean reversion
            if current_vol > vol_mean + vol_std:  # High volatility
                opportunities.append({
                    'type': 'volatility_reversion',
                    'direction': 'short_vol',
                    'current_vol': current_vol,
                    'mean_vol': vol_mean,
                    'expected_return': (current_vol - vol_mean) / vol_mean * 0.1,
                    'confidence': min((current_vol - vol_mean) / vol_std, 1.0),
                    'risk_score': 0.7,
                    'holding_period': 10
                })
            elif current_vol < vol_mean - vol_std:  # Low volatility
                opportunities.append({
                    'type': 'volatility_reversion',
                    'direction': 'long_vol',
                    'current_vol': current_vol,
                    'mean_vol': vol_mean,
                    'expected_return': (vol_mean - current_vol) / vol_mean * 0.1,
                    'confidence': min((vol_mean - current_vol) / vol_std, 1.0),
                    'risk_score': 0.7,
                    'holding_period': 10
                })
            
            # Volatility clustering
            recent_vol = realized_vol.iloc[-5:].mean()
            if recent_vol > vol_mean * 1.5:  # High volatility cluster
                opportunities.append({
                    'type': 'volatility_clustering',
                    'direction': 'expect_continued_vol',
                    'recent_vol': recent_vol,
                    'expected_return': 0.05,  # Rough estimate
                    'confidence': 0.6,
                    'risk_score': 0.8,
                    'holding_period': 3
                })
            
        except Exception as e:
            print(f"⚠️  Error in volatility arbitrage: {e}")
        
        return opportunities


class PairsTrading:
    """Pairs trading opportunity detection"""
    
    def find_pairs(self, data: pd.DataFrame, additional_data: Dict[str, pd.DataFrame]) -> List[Dict]:
        """Find pairs trading opportunities"""
        opportunities = []
        
        try:
            if not additional_data:
                return opportunities
            
            # Find correlated pairs
            for symbol, other_data in additional_data.items():
                if len(other_data) < 50 or len(data) < 50:
                    continue
                
                # Align data
                common_dates = data.index.intersection(other_data.index)
                if len(common_dates) < 30:
                    continue
                
                data_aligned = data.loc[common_dates]['close']
                other_aligned = other_data.loc[common_dates]['close']
                
                # Calculate correlation
                correlation = data_aligned.corr(other_aligned)
                
                if abs(correlation) > 0.8:  # High correlation
                    # Calculate spread
                    spread = data_aligned - other_aligned
                    spread_mean = spread.mean()
                    spread_std = spread.std()
                    
                    current_spread = spread.iloc[-1]
                    z_score = (current_spread - spread_mean) / spread_std if spread_std > 0 else 0
                    
                    if abs(z_score) > 2.0:  # Significant spread deviation
                        opportunities.append({
                            'type': 'pairs_trading',
                            'pair': f"{symbol}_spread",
                            'correlation': correlation,
                            'z_score': z_score,
                            'direction': 'short_spread' if z_score > 0 else 'long_spread',
                            'expected_return': abs(z_score) * 0.01,
                            'confidence': min(abs(z_score) / 3.0, 1.0),
                            'risk_score': 0.4,
                            'holding_period': 7
                        })
            
        except Exception as e:
            print(f"⚠️  Error in pairs trading: {e}")
        
        return opportunities


class CrossExchangeArbitrage:
    """Cross-exchange arbitrage opportunity detection"""
    
    def find_opportunities(self, data: pd.DataFrame, 
                         exchange_data: Dict[str, pd.DataFrame]) -> List[Dict]:
        """Find cross-exchange arbitrage opportunities"""
        opportunities = []
        
        try:
            if not exchange_data:
                return opportunities
            
            current_price = data['close'].iloc[-1]
            
            for exchange, exchange_df in exchange_data.items():
                if len(exchange_df) == 0:
                    continue
                
                exchange_price = exchange_df['close'].iloc[-1]
                
                # Calculate spread
                spread = abs(current_price - exchange_price) / current_price
                
                if spread > 0.005:  # 0.5% minimum spread
                    direction = 'buy_here_sell_there' if current_price < exchange_price else 'sell_here_buy_there'
                    
                    # Account for execution costs
                    net_profit = spread - 0.002  # Assume 0.2% total execution cost
                    
                    if net_profit > 0:
                        opportunities.append({
                            'type': 'cross_exchange_arbitrage',
                            'exchange': exchange,
                            'spread': spread,
                            'direction': direction,
                            'current_price': current_price,
                            'exchange_price': exchange_price,
                            'expected_return': net_profit,
                            'confidence': 0.9,  # High confidence for arbitrage
                            'risk_score': 0.2,  # Low risk for arbitrage
                            'holding_period': 1  # Should be executed immediately
                        })
            
        except Exception as e:
            print(f"⚠️  Error in cross-exchange arbitrage: {e}")
        
        return opportunities


class TimeInefficiencyDetector:
    """Time-based inefficiency detection"""
    
    def detect(self, data: pd.DataFrame) -> List[Dict]:
        """Detect time-based inefficiencies"""
        opportunities = []
        
        try:
            if len(data) < 100:
                return opportunities
            
            # Hour-of-day effects
            if hasattr(data.index, 'hour'):
                hourly_returns = data['close'].pct_change().groupby(data.index.hour).mean()
                
                current_hour = data.index[-1].hour
                if current_hour in hourly_returns.index:
                    expected_return = hourly_returns[current_hour]
                    
                    if abs(expected_return) > 0.001:  # 0.1% threshold
                        opportunities.append({
                            'type': 'hour_of_day_effect',
                            'hour': current_hour,
                            'expected_return': expected_return,
                            'direction': 'long' if expected_return > 0 else 'short',
                            'confidence': 0.3,
                            'risk_score': 0.5,
                            'holding_period': 1
                        })
            
            # Day-of-week effects
            if hasattr(data.index, 'dayofweek'):
                daily_returns = data['close'].pct_change().groupby(data.index.dayofweek).mean()
                
                current_day = data.index[-1].dayofweek
                if current_day in daily_returns.index:
                    expected_return = daily_returns[current_day]
                    
                    if abs(expected_return) > 0.002:  # 0.2% threshold
                        opportunities.append({
                            'type': 'day_of_week_effect',
                            'day': current_day,
                            'expected_return': expected_return,
                            'direction': 'long' if expected_return > 0 else 'short',
                            'confidence': 0.4,
                            'risk_score': 0.4,
                            'holding_period': 1
                        })
            
            # End-of-month effects
            if hasattr(data.index, 'day'):
                # Check if we're in the last 3 days of the month
                month_end_data = data[data.index.day >= 28]
                if len(month_end_data) > 10:
                    month_end_returns = month_end_data['close'].pct_change().mean()
                    
                    if abs(month_end_returns) > 0.003:  # 0.3% threshold
                        opportunities.append({
                            'type': 'month_end_effect',
                            'expected_return': month_end_returns,
                            'direction': 'long' if month_end_returns > 0 else 'short',
                            'confidence': 0.5,
                            'risk_score': 0.3,
                            'holding_period': 3
                        })
            
        except Exception as e:
            print(f"⚠️  Error in time inefficiency detection: {e}")
        
        return opportunities


# Example usage and testing
if __name__ == "__main__":
    # Test the Market Inefficiency Strategy
    print("💰 Testing Market Inefficiency & Arbitrage Strategy")
    
    # Create sample data
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='H')
    np.random.seed(42)
    
    # Main asset data
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
    
    # Create additional data for pairs trading
    additional_data = {
        'correlated_asset': pd.DataFrame({
            'open': 95 + np.random.randn(len(dates)).cumsum() * 0.02,
            'high': 95.5 + np.random.randn(len(dates)).cumsum() * 0.02,
            'low': 94.5 + np.random.randn(len(dates)).cumsum() * 0.02,
            'close': 95 + np.random.randn(len(dates)).cumsum() * 0.02,
            'volume': np.random.randint(800, 8000, len(dates))
        }, index=dates),
        'exchanges': {
            'exchange_b': pd.DataFrame({
                'close': sample_data['close'] * (1 + np.random.randn(len(dates)) * 0.001)
            }, index=dates)
        }
    }
    
    # Initialize strategy
    strategy = MarketInefficiencyStrategy()
    
    # Test inefficiency identification
    print("🔍 Identifying market inefficiencies...")
    inefficiencies = strategy.identify_inefficiencies(sample_data, additional_data)
    
    print(f"📊 INEFFICIENCY ANALYSIS RESULTS:")
    print(f"{'='*50}")
    print(f"Total Opportunities: {inefficiencies['total_opportunities']}")
    
    for category, opportunities in inefficiencies.items():
        if isinstance(opportunities, list) and opportunities:
            print(f"\n{category.upper().replace('_', ' ')}:")
            for i, opp in enumerate(opportunities[:3]):  # Show first 3
                print(f"  {i+1}. Type: {opp.get('type', 'Unknown')}")
                print(f"     Direction: {opp.get('direction', 'Unknown')}")
                print(f"     Expected Return: {opp.get('expected_return', 0):.3f}")
                print(f"     Confidence: {opp.get('confidence', 0):.3f}")
    
    # Test signal generation
    print(f"\n🎯 Generating trading signals...")
    signals = strategy.generate_signals(sample_data, additional_data)
    
    print(f"\n📈 TRADING SIGNAL RESULTS:")
    print(f"{'='*50}")
    print(f"Primary Signal: {signals['primary_signal']}")
    print(f"Signal Strength: {signals['signal_strength']:.3f}")
    print(f"Opportunity Type: {signals['opportunity_type']}")
    print(f"Expected Return: {signals['expected_return']:.3f}")
    print(f"Confidence: {signals['confidence']:.3f}")
    print(f"Risk Score: {signals['risk_score']:.3f}")
    print(f"Holding Period: {signals['holding_period']} periods")
    
    if signals['primary_signal'] != 0:
        print(f"\n⚠️  RISK MANAGEMENT:")
        print(f"Entry Price: ${signals['entry_price']:.2f}")
        print(f"Stop Loss: ${signals['stop_loss']:.2f}")
        print(f"Take Profit: ${signals['take_profit']:.2f}")
        print(f"Position Size: {signals['position_size']:.3f}")
        print(f"Max Loss: ${signals['max_loss']:.2f}")
    
    print(f"\n💰 Market Inefficiency Strategy test completed!")
    print(f"{'='*50}")
