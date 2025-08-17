"""
AlgoProject - Advanced Strategy Hub
Central hub for managing and coordinating all advanced trading strategies
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

# Import all strategy modules
try:
    from .ml_ai_framework import MLAITradingFramework
    from .institutional_flow_strategy import InstitutionalOrderFlowStrategy
    from .ultimate_profitable_strategy import UltimateProfitableStrategy
    from .market_inefficiency_strategy import MarketInefficiencyStrategy
    ALL_STRATEGIES_AVAILABLE = True
except ImportError:
    # Fallback for standalone execution
    try:
        from ml_ai_framework import MLAITradingFramework
        from institutional_flow_strategy import InstitutionalOrderFlowStrategy
        from ultimate_profitable_strategy import UltimateProfitableStrategy
        from market_inefficiency_strategy import MarketInefficiencyStrategy
        ALL_STRATEGIES_AVAILABLE = True
    except ImportError:
        ALL_STRATEGIES_AVAILABLE = False
        print("⚠️  Some strategy modules not available. Hub will run in limited mode.")


class AdvancedStrategyHub:
    """
    Advanced Strategy Hub - Central Command Center
    
    This hub coordinates all advanced trading strategies:
    1. ML/AI Trading Framework
    2. Institutional Order Flow Strategy
    3. Ultimate Profitable Strategy
    4. Market Inefficiency Strategy
    
    Features:
    - Strategy consensus building
    - Risk management coordination
    - Performance monitoring
    - Strategy auto-selection
    - Portfolio optimization
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or self._default_config()
        
        # Initialize all strategies
        self.strategies = {}
        self.strategy_weights = {}
        self.strategy_performance = {}
        
        if ALL_STRATEGIES_AVAILABLE:
            self._initialize_strategies()
        else:
            print("⚠️  Limited strategy initialization due to missing modules")
        
        # Hub state
        self.consensus_history = []
        self.performance_metrics = {}
        self.risk_metrics = {}
        self.active_positions = {}
        
        # Strategy auto-selection
        self.strategy_selector = StrategySelector()
        self.portfolio_optimizer = PortfolioOptimizer()
        self.risk_manager = HubRiskManager()
        
    def _default_config(self) -> Dict:
        return {
            'strategies': {
                'ml_ai': {
                    'enabled': True,
                    'weight': 0.3,
                    'confidence_threshold': 0.6
                },
                'institutional_flow': {
                    'enabled': True,
                    'weight': 0.25,
                    'confidence_threshold': 0.7
                },
                'ultimate_profitable': {
                    'enabled': True,
                    'weight': 0.35,
                    'confidence_threshold': 0.65
                },
                'market_inefficiency': {
                    'enabled': True,
                    'weight': 0.1,
                    'confidence_threshold': 0.8
                }
            },
            'consensus': {
                'min_agreement_threshold': 0.6,
                'weight_by_performance': True,
                'weight_by_confidence': True,
                'require_risk_approval': True
            },
            'risk_management': {
                'max_total_exposure': 0.1,
                'max_strategy_allocation': 0.04,
                'correlation_limit': 0.7,
                'drawdown_limit': 0.05,
                'var_limit': 0.02
            },
            'performance': {
                'lookback_period': 30,
                'min_trades_for_stats': 10,
                'performance_decay_factor': 0.9
            },
            'auto_selection': {
                'enabled': True,
                'rebalance_frequency': 'daily',
                'performance_threshold': 0.6
            }
        }
    
    def _initialize_strategies(self):
        """Initialize all strategy instances"""
        try:
            # ML/AI Framework
            if self.config['strategies']['ml_ai']['enabled']:
                self.strategies['ml_ai'] = MLAITradingFramework()
                self.strategy_weights['ml_ai'] = self.config['strategies']['ml_ai']['weight']
                
            # Institutional Flow Strategy
            if self.config['strategies']['institutional_flow']['enabled']:
                self.strategies['institutional_flow'] = InstitutionalOrderFlowStrategy()
                self.strategy_weights['institutional_flow'] = self.config['strategies']['institutional_flow']['weight']
                
            # Ultimate Profitable Strategy
            if self.config['strategies']['ultimate_profitable']['enabled']:
                self.strategies['ultimate_profitable'] = UltimateProfitableStrategy()
                self.strategy_weights['ultimate_profitable'] = self.config['strategies']['ultimate_profitable']['weight']
                
            # Market Inefficiency Strategy
            if self.config['strategies']['market_inefficiency']['enabled']:
                self.strategies['market_inefficiency'] = MarketInefficiencyStrategy()
                self.strategy_weights['market_inefficiency'] = self.config['strategies']['market_inefficiency']['weight']
                
            print(f"✅ Initialized {len(self.strategies)} strategies")
            
        except Exception as e:
            print(f"⚠️  Error initializing strategies: {e}")
    
    def get_strategy_signals(self, data: pd.DataFrame, 
                           additional_data: Dict = None) -> Dict[str, Dict]:
        """
        Get signals from all strategies
        """
        all_signals = {}
        
        try:
            # ML/AI Signals
            if 'ml_ai' in self.strategies:
                try:
                    ml_prediction = self.strategies['ml_ai'].predict(data)
                    all_signals['ml_ai'] = {
                        'signal': ml_prediction.get('signal', 0),
                        'confidence': ml_prediction.get('confidence', 0),
                        'reasoning': 'ML/AI ensemble prediction',
                        'individual_predictions': ml_prediction.get('individual_predictions', {}),
                        'timestamp': datetime.now()
                    }
                except Exception as e:
                    print(f"⚠️  Error getting ML/AI signals: {e}")
                    all_signals['ml_ai'] = {'signal': 0, 'confidence': 0, 'error': str(e)}
            
            # Institutional Flow Signals
            if 'institutional_flow' in self.strategies:
                try:
                    institutional_signals = self.strategies['institutional_flow'].generate_signals(data)
                    all_signals['institutional_flow'] = {
                        'signal': institutional_signals.get('primary_signal', 0),
                        'confidence': institutional_signals.get('signal_strength', 0),
                        'reasoning': 'Institutional order flow analysis',
                        'entry_reasons': institutional_signals.get('entry_reasons', []),
                        'risk_management': {
                            'stop_loss': institutional_signals.get('stop_loss', 0),
                            'take_profit': institutional_signals.get('take_profit', 0),
                            'risk_reward_ratio': institutional_signals.get('risk_reward_ratio', 0)
                        },
                        'timestamp': datetime.now()
                    }
                except Exception as e:
                    print(f"⚠️  Error getting institutional flow signals: {e}")
                    all_signals['institutional_flow'] = {'signal': 0, 'confidence': 0, 'error': str(e)}
            
            # Ultimate Profitable Strategy Signals
            if 'ultimate_profitable' in self.strategies:
                try:
                    ultimate_signals = self.strategies['ultimate_profitable'].generate_ultimate_signal(data)
                    all_signals['ultimate_profitable'] = {
                        'signal': ultimate_signals.get('primary_signal', 0),
                        'confidence': ultimate_signals.get('confluence_score', 0),
                        'reasoning': 'Ultimate profitable strategy consensus',
                        'signals_breakdown': ultimate_signals.get('signals_breakdown', {}),
                        'entry_reasons': ultimate_signals.get('entry_reasons', []),
                        'risk_management': ultimate_signals.get('risk_management', {}),
                        'market_regime': ultimate_signals.get('market_regime', 'unknown'),
                        'timestamp': datetime.now()
                    }
                except Exception as e:
                    print(f"⚠️  Error getting ultimate profitable signals: {e}")
                    all_signals['ultimate_profitable'] = {'signal': 0, 'confidence': 0, 'error': str(e)}
            
            # Market Inefficiency Signals
            if 'market_inefficiency' in self.strategies:
                try:
                    inefficiency_signals = self.strategies['market_inefficiency'].generate_signals(
                        data, additional_data
                    )
                    all_signals['market_inefficiency'] = {
                        'signal': inefficiency_signals.get('primary_signal', 0),
                        'confidence': inefficiency_signals.get('confidence', 0),
                        'reasoning': 'Market inefficiency exploitation',
                        'opportunity_type': inefficiency_signals.get('opportunity_type', 'none'),
                        'expected_return': inefficiency_signals.get('expected_return', 0),
                        'risk_score': inefficiency_signals.get('risk_score', 0),
                        'timestamp': datetime.now()
                    }
                except Exception as e:
                    print(f"⚠️  Error getting market inefficiency signals: {e}")
                    all_signals['market_inefficiency'] = {'signal': 0, 'confidence': 0, 'error': str(e)}
            
        except Exception as e:
            print(f"⚠️  Error collecting strategy signals: {e}")
        
        return all_signals
    
    def build_consensus(self, strategy_signals: Dict[str, Dict]) -> Dict:
        """
        Build consensus signal from all strategies
        """
        consensus = {
            'final_signal': 0,
            'consensus_strength': 0,
            'agreement_score': 0,
            'participating_strategies': 0,
            'strategy_breakdown': {},
            'consensus_reasoning': [],
            'risk_assessment': {},
            'recommendation': 'hold'
        }
        
        try:
            # Filter valid signals
            valid_signals = {}
            for strategy_name, signal_data in strategy_signals.items():
                if (signal_data.get('confidence', 0) >= 
                    self.config['strategies'].get(strategy_name, {}).get('confidence_threshold', 0.5)):
                    valid_signals[strategy_name] = signal_data
            
            if not valid_signals:
                consensus['recommendation'] = 'insufficient_confidence'
                return consensus
            
            # Calculate weighted consensus
            weighted_signals = []
            total_weight = 0
            confidence_sum = 0
            
            for strategy_name, signal_data in valid_signals.items():
                signal = signal_data.get('signal', 0)
                confidence = signal_data.get('confidence', 0)
                
                # Get strategy weight
                base_weight = self.strategy_weights.get(strategy_name, 0.25)
                
                # Adjust weight by performance if enabled
                if self.config['consensus']['weight_by_performance']:
                    performance_multiplier = self._get_performance_multiplier(strategy_name)
                    base_weight *= performance_multiplier
                
                # Adjust weight by confidence if enabled
                if self.config['consensus']['weight_by_confidence']:
                    confidence_multiplier = 0.5 + (confidence * 0.5)  # 0.5 to 1.0
                    base_weight *= confidence_multiplier
                
                weighted_signal = signal * base_weight
                weighted_signals.append(weighted_signal)
                total_weight += base_weight
                confidence_sum += confidence
                
                # Store breakdown
                consensus['strategy_breakdown'][strategy_name] = {
                    'signal': signal,
                    'confidence': confidence,
                    'weight': base_weight,
                    'weighted_contribution': weighted_signal,
                    'reasoning': signal_data.get('reasoning', 'Unknown')
                }
            
            # Calculate final consensus
            if total_weight > 0:
                consensus_signal_raw = sum(weighted_signals) / total_weight
                consensus['consensus_strength'] = abs(consensus_signal_raw)
                
                # Convert to discrete signal
                if consensus_signal_raw > 0.5:
                    consensus['final_signal'] = 1
                    consensus['recommendation'] = 'buy'
                elif consensus_signal_raw < -0.5:
                    consensus['final_signal'] = -1
                    consensus['recommendation'] = 'sell'
                else:
                    consensus['final_signal'] = 0
                    consensus['recommendation'] = 'hold'
                
                # Calculate agreement score
                agreeing_strategies = sum(1 for strategy_name, signal_data in valid_signals.items() 
                                        if signal_data.get('signal', 0) == consensus['final_signal'])
                consensus['agreement_score'] = agreeing_strategies / len(valid_signals)
                
                # Average confidence
                consensus['average_confidence'] = confidence_sum / len(valid_signals)
                
                # Participating strategies
                consensus['participating_strategies'] = len(valid_signals)
                
                # Build reasoning
                consensus_reasoning = []
                for strategy_name, breakdown in consensus['strategy_breakdown'].items():
                    if breakdown['signal'] == consensus['final_signal']:
                        consensus_reasoning.append(f"{strategy_name}: {breakdown['reasoning']}")
                
                consensus['consensus_reasoning'] = consensus_reasoning
                
                # Risk assessment
                consensus['risk_assessment'] = self._assess_consensus_risk(consensus, valid_signals)
                
                # Final recommendation check
                if consensus['agreement_score'] < self.config['consensus']['min_agreement_threshold']:
                    consensus['recommendation'] = 'insufficient_agreement'
                elif self.config['consensus']['require_risk_approval'] and consensus['risk_assessment'].get('risk_score', 0) > 0.7:
                    consensus['recommendation'] = 'risk_too_high'
            
            # Store consensus history
            self.consensus_history.append({
                'timestamp': datetime.now(),
                'consensus': consensus.copy(),
                'strategy_signals': strategy_signals.copy()
            })
            
            # Limit history size
            if len(self.consensus_history) > 100:
                self.consensus_history = self.consensus_history[-100:]
            
        except Exception as e:
            print(f"⚠️  Error building consensus: {e}")
            consensus['error'] = str(e)
        
        return consensus
    
    def _get_performance_multiplier(self, strategy_name: str) -> float:
        """
        Get performance-based weight multiplier for a strategy
        """
        try:
            if strategy_name not in self.strategy_performance:
                return 1.0
            
            performance = self.strategy_performance[strategy_name]
            
            # Use win rate and average return
            win_rate = performance.get('win_rate', 0.5)
            avg_return = performance.get('avg_return', 0)
            
            # Performance score (0.5 to 1.5)
            performance_score = 0.5 + (win_rate * 0.5) + (max(avg_return, 0) * 5)
            performance_score = max(0.5, min(1.5, performance_score))
            
            return performance_score
            
        except:
            return 1.0
    
    def _assess_consensus_risk(self, consensus: Dict, valid_signals: Dict) -> Dict:
        """
        Assess risk of consensus signal
        """
        risk_assessment = {
            'risk_score': 0,
            'risk_factors': [],
            'risk_mitigation': []
        }
        
        try:
            risk_factors = []
            
            # Low agreement risk
            if consensus['agreement_score'] < 0.7:
                risk_factors.append('low_strategy_agreement')
            
            # Low confidence risk
            if consensus.get('average_confidence', 0) < 0.6:
                risk_factors.append('low_average_confidence')
            
            # Few participating strategies
            if consensus['participating_strategies'] < 2:
                risk_factors.append('few_participating_strategies')
            
            # High signal strength might indicate overconfidence
            if consensus['consensus_strength'] > 0.9:
                risk_factors.append('potentially_overconfident')
            
            # Calculate overall risk score
            risk_score = len(risk_factors) * 0.2
            risk_score = min(risk_score, 1.0)
            
            risk_assessment['risk_score'] = risk_score
            risk_assessment['risk_factors'] = risk_factors
            
            # Risk mitigation suggestions
            if 'low_strategy_agreement' in risk_factors:
                risk_assessment['risk_mitigation'].append('reduce_position_size')
            
            if 'low_average_confidence' in risk_factors:
                risk_assessment['risk_mitigation'].append('wait_for_higher_confidence')
            
            if 'few_participating_strategies' in risk_factors:
                risk_assessment['risk_mitigation'].append('require_more_strategy_confirmation')
            
        except Exception as e:
            print(f"⚠️  Error assessing consensus risk: {e}")
        
        return risk_assessment
    
    def generate_master_signal(self, data: pd.DataFrame, 
                             additional_data: Dict = None) -> Dict:
        """
        Generate master trading signal from all strategies
        """
        master_signal = {
            'timestamp': datetime.now(),
            'primary_signal': 0,
            'signal_strength': 0,
            'consensus_data': {},
            'strategy_signals': {},
            'risk_management': {},
            'execution_plan': {},
            'performance_context': {}
        }
        
        try:
            # Get signals from all strategies
            strategy_signals = self.get_strategy_signals(data, additional_data)
            master_signal['strategy_signals'] = strategy_signals
            
            # Build consensus
            consensus = self.build_consensus(strategy_signals)
            master_signal['consensus_data'] = consensus
            
            # Set primary signal
            master_signal['primary_signal'] = consensus['final_signal']
            master_signal['signal_strength'] = consensus['consensus_strength']
            
            # Risk management
            if master_signal['primary_signal'] != 0:
                risk_management = self.risk_manager.calculate_risk_parameters(
                    data, master_signal, strategy_signals
                )
                master_signal['risk_management'] = risk_management
            
            # Execution plan
            if master_signal['primary_signal'] != 0:
                execution_plan = self._create_execution_plan(master_signal, data)
                master_signal['execution_plan'] = execution_plan
            
            # Performance context
            performance_context = self._get_performance_context()
            master_signal['performance_context'] = performance_context
            
        except Exception as e:
            print(f"⚠️  Error generating master signal: {e}")
            master_signal['error'] = str(e)
        
        return master_signal
    
    def _create_execution_plan(self, master_signal: Dict, data: pd.DataFrame) -> Dict:
        """
        Create execution plan for the master signal
        """
        execution_plan = {
            'entry_price': data['close'].iloc[-1],
            'position_size': 0,
            'stop_loss': 0,
            'take_profit': 0,
            'execution_timing': 'immediate',
            'order_type': 'market',
            'execution_notes': []
        }
        
        try:
            current_price = data['close'].iloc[-1]
            
            # Position sizing
            risk_management = master_signal.get('risk_management', {})
            execution_plan['position_size'] = risk_management.get('position_size', 0)
            execution_plan['stop_loss'] = risk_management.get('stop_loss', 0)
            execution_plan['take_profit'] = risk_management.get('take_profit', 0)
            
            # Execution timing
            signal_strength = master_signal.get('signal_strength', 0)
            if signal_strength > 0.8:
                execution_plan['execution_timing'] = 'immediate'
                execution_plan['order_type'] = 'market'
            elif signal_strength > 0.6:
                execution_plan['execution_timing'] = 'next_candle'
                execution_plan['order_type'] = 'limit'
            else:
                execution_plan['execution_timing'] = 'wait_for_confirmation'
                execution_plan['order_type'] = 'limit'
            
            # Execution notes
            consensus = master_signal.get('consensus_data', {})
            if consensus.get('agreement_score', 0) < 0.7:
                execution_plan['execution_notes'].append('Low strategy agreement - consider reduced size')
            
            if len(consensus.get('consensus_reasoning', [])) > 0:
                execution_plan['execution_notes'].append('Multiple strategy confirmation')
            
        except Exception as e:
            print(f"⚠️  Error creating execution plan: {e}")
        
        return execution_plan
    
    def _get_performance_context(self) -> Dict:
        """
        Get performance context for decision making
        """
        context = {
            'recent_performance': {},
            'strategy_rankings': {},
            'risk_metrics': {},
            'market_conditions': 'unknown'
        }
        
        try:
            # Recent performance
            if self.consensus_history:
                recent_signals = self.consensus_history[-10:]  # Last 10 signals
                context['recent_performance'] = {
                    'total_signals': len(recent_signals),
                    'buy_signals': sum(1 for s in recent_signals if s['consensus']['final_signal'] == 1),
                    'sell_signals': sum(1 for s in recent_signals if s['consensus']['final_signal'] == -1),
                    'hold_signals': sum(1 for s in recent_signals if s['consensus']['final_signal'] == 0),
                    'avg_consensus_strength': np.mean([s['consensus']['consensus_strength'] for s in recent_signals])
                }
            
            # Strategy rankings
            for strategy_name in self.strategies.keys():
                if strategy_name in self.strategy_performance:
                    perf = self.strategy_performance[strategy_name]
                    context['strategy_rankings'][strategy_name] = {
                        'win_rate': perf.get('win_rate', 0),
                        'avg_return': perf.get('avg_return', 0),
                        'total_trades': perf.get('total_trades', 0)
                    }
            
        except Exception as e:
            print(f"⚠️  Error getting performance context: {e}")
        
        return context
    
    def update_performance(self, strategy_name: str, trade_result: Dict):
        """
        Update performance metrics for a strategy
        """
        try:
            if strategy_name not in self.strategy_performance:
                self.strategy_performance[strategy_name] = {
                    'total_trades': 0,
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'total_return': 0,
                    'win_rate': 0,
                    'avg_return': 0,
                    'max_drawdown': 0,
                    'sharpe_ratio': 0
                }
            
            perf = self.strategy_performance[strategy_name]
            
            # Update trade counts
            perf['total_trades'] += 1
            
            trade_return = trade_result.get('return', 0)
            perf['total_return'] += trade_return
            
            if trade_return > 0:
                perf['winning_trades'] += 1
            elif trade_return < 0:
                perf['losing_trades'] += 1
            
            # Update metrics
            perf['win_rate'] = perf['winning_trades'] / perf['total_trades']
            perf['avg_return'] = perf['total_return'] / perf['total_trades']
            
            # Update strategy weight based on performance
            if self.config['consensus']['weight_by_performance']:
                self._update_strategy_weight(strategy_name)
            
        except Exception as e:
            print(f"⚠️  Error updating performance: {e}")
    
    def _update_strategy_weight(self, strategy_name: str):
        """
        Update strategy weight based on performance
        """
        try:
            if strategy_name in self.strategy_performance:
                perf = self.strategy_performance[strategy_name]
                
                # Calculate performance score
                win_rate = perf.get('win_rate', 0.5)
                avg_return = perf.get('avg_return', 0)
                
                # Performance-based weight adjustment
                base_weight = self.config['strategies'][strategy_name]['weight']
                performance_multiplier = 0.5 + (win_rate * 0.5) + (max(avg_return, 0) * 5)
                performance_multiplier = max(0.5, min(1.5, performance_multiplier))
                
                # Apply decay factor
                decay_factor = self.config['performance']['performance_decay_factor']
                current_weight = self.strategy_weights[strategy_name]
                new_weight = (current_weight * decay_factor) + (base_weight * performance_multiplier * (1 - decay_factor))
                
                self.strategy_weights[strategy_name] = new_weight
                
        except Exception as e:
            print(f"⚠️  Error updating strategy weight: {e}")
    
    def get_hub_status(self) -> Dict:
        """
        Get comprehensive hub status
        """
        status = {
            'timestamp': datetime.now(),
            'active_strategies': len(self.strategies),
            'strategy_weights': self.strategy_weights.copy(),
            'performance_summary': {},
            'recent_consensus': {},
            'risk_status': {},
            'configuration': self.config
        }
        
        try:
            # Performance summary
            for strategy_name, perf in self.strategy_performance.items():
                status['performance_summary'][strategy_name] = {
                    'total_trades': perf.get('total_trades', 0),
                    'win_rate': perf.get('win_rate', 0),
                    'avg_return': perf.get('avg_return', 0)
                }
            
            # Recent consensus
            if self.consensus_history:
                recent_consensus = self.consensus_history[-1]['consensus']
                status['recent_consensus'] = {
                    'final_signal': recent_consensus['final_signal'],
                    'consensus_strength': recent_consensus['consensus_strength'],
                    'agreement_score': recent_consensus['agreement_score'],
                    'recommendation': recent_consensus['recommendation']
                }
            
            # Risk status
            status['risk_status'] = {
                'total_exposure': sum(self.strategy_weights.values()),
                'max_strategy_weight': max(self.strategy_weights.values()) if self.strategy_weights else 0,
                'weight_distribution': self.strategy_weights
            }
            
        except Exception as e:
            print(f"⚠️  Error getting hub status: {e}")
            status['error'] = str(e)
        
        return status
    
    def generate_signals(self, data: pd.DataFrame, 
                        additional_data: Dict = None) -> List[Dict]:
        """
        Generate consensus signals from all strategies
        """
        try:
            # Get signals from all strategies
            strategy_signals = self.get_strategy_signals(data, additional_data)
            
            # Build consensus
            consensus = self.build_consensus(strategy_signals)
            
            # Return as list of signals for compatibility
            if consensus.get('signal', 0) != 0:
                return [{
                    'signal_type': 'BUY' if consensus['signal'] > 0 else 'SELL',
                    'strategy': 'consensus',
                    'confidence': consensus.get('confidence', 0),
                    'strength': consensus.get('strength', 0),
                    'entry_price': data['close'].iloc[-1],
                    'timestamp': datetime.now(),
                    'contributing_strategies': list(strategy_signals.keys())
                }]
            else:
                return []
                
        except Exception as e:
            print(f"⚠️  Error generating consensus signals: {e}")
            return []


class StrategySelector:
    """Strategy selection and ranking system"""
    
    def select_optimal_strategies(self, performance_data: Dict, 
                                market_conditions: Dict) -> List[str]:
        """Select optimal strategies based on performance and market conditions"""
        rankings = []
        
        try:
            for strategy_name, perf in performance_data.items():
                score = self._calculate_strategy_score(perf, market_conditions)
                rankings.append((strategy_name, score))
            
            # Sort by score (highest first)
            rankings.sort(key=lambda x: x[1], reverse=True)
            
            # Return strategy names in order
            return [name for name, score in rankings]
            
        except Exception as e:
            print(f"⚠️  Error selecting strategies: {e}")
            return []
    
    def _calculate_strategy_score(self, performance: Dict, market_conditions: Dict) -> float:
        """Calculate strategy score based on performance and market conditions"""
        try:
            win_rate = performance.get('win_rate', 0.5)
            avg_return = performance.get('avg_return', 0)
            total_trades = performance.get('total_trades', 0)
            
            # Base score
            base_score = (win_rate * 0.4) + (max(avg_return, 0) * 0.6)
            
            # Adjust for sample size
            if total_trades < 10:
                base_score *= 0.5  # Reduce confidence for small sample
            
            # Adjust for market conditions
            volatility = market_conditions.get('volatility', 'normal')
            if volatility == 'high':
                # Some strategies might perform better in high volatility
                if 'volatility' in performance.get('specialties', []):
                    base_score *= 1.2
            
            return base_score
            
        except:
            return 0.5


class PortfolioOptimizer:
    """Portfolio optimization for strategy allocation"""
    
    def optimize_allocations(self, strategies: List[str], 
                           performance_data: Dict, 
                           risk_data: Dict) -> Dict[str, float]:
        """Optimize strategy allocations"""
        allocations = {}
        
        try:
            # Equal weight as starting point
            equal_weight = 1.0 / len(strategies)
            
            for strategy in strategies:
                # Start with equal weight
                allocation = equal_weight
                
                # Adjust based on performance
                if strategy in performance_data:
                    perf = performance_data[strategy]
                    performance_multiplier = 0.5 + (perf.get('win_rate', 0.5) * 0.5)
                    allocation *= performance_multiplier
                
                # Adjust based on risk
                if strategy in risk_data:
                    risk = risk_data[strategy]
                    risk_multiplier = 1.0 / (1.0 + risk.get('volatility', 0.5))
                    allocation *= risk_multiplier
                
                allocations[strategy] = allocation
            
            # Normalize to sum to 1.0
            total_allocation = sum(allocations.values())
            if total_allocation > 0:
                for strategy in allocations:
                    allocations[strategy] /= total_allocation
            
        except Exception as e:
            print(f"⚠️  Error optimizing allocations: {e}")
        
        return allocations


class HubRiskManager:
    """Centralized risk management for the hub"""
    
    def calculate_risk_parameters(self, data: pd.DataFrame, 
                                master_signal: Dict, 
                                strategy_signals: Dict) -> Dict:
        """Calculate comprehensive risk parameters"""
        risk_params = {
            'position_size': 0,
            'stop_loss': 0,
            'take_profit': 0,
            'max_loss': 0,
            'risk_score': 0,
            'var_estimate': 0
        }
        
        try:
            current_price = data['close'].iloc[-1]
            
            # Calculate volatility
            returns = data['close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252)  # Annualized
            
            # Base position size (2% risk)
            base_risk = 0.02
            
            # Adjust for signal strength
            signal_strength = master_signal.get('signal_strength', 0)
            signal_adjustment = 0.5 + (signal_strength * 0.5)
            
            # Adjust for consensus
            consensus = master_signal.get('consensus_data', {})
            agreement_score = consensus.get('agreement_score', 0)
            consensus_adjustment = 0.5 + (agreement_score * 0.5)
            
            # Final position size
            final_risk = base_risk * signal_adjustment * consensus_adjustment
            
            # Calculate position size based on ATR
            atr = self._calculate_atr(data)
            if atr > 0:
                stop_distance = atr * 2
                position_size = final_risk / (stop_distance / current_price)
            else:
                position_size = final_risk / 0.02  # 2% stop loss fallback
            
            # Risk management levels
            if master_signal['primary_signal'] == 1:  # Long
                risk_params['stop_loss'] = current_price - stop_distance
                risk_params['take_profit'] = current_price + (stop_distance * 2)
            elif master_signal['primary_signal'] == -1:  # Short
                risk_params['stop_loss'] = current_price + stop_distance
                risk_params['take_profit'] = current_price - (stop_distance * 2)
            
            risk_params['position_size'] = position_size
            risk_params['max_loss'] = position_size * stop_distance
            
            # Risk score
            risk_params['risk_score'] = volatility * position_size
            
            # VaR estimate (95% confidence)
            if len(returns) > 0:
                var_95 = np.percentile(returns, 5) * position_size
                risk_params['var_estimate'] = abs(var_95)
            
        except Exception as e:
            print(f"⚠️  Error calculating risk parameters: {e}")
        
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


# Example usage and testing
if __name__ == "__main__":
    # Test the Advanced Strategy Hub
    print("🎯 Testing Advanced Strategy Hub")
    
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
    
    # Initialize hub
    hub = AdvancedStrategyHub()
    
    # Get hub status
    print("📊 Hub Status:")
    status = hub.get_hub_status()
    print(f"  Active Strategies: {status['active_strategies']}")
    print(f"  Strategy Weights: {status['strategy_weights']}")
    
    # Generate master signal
    print("\n🚀 Generating Master Signal...")
    master_signal = hub.generate_master_signal(sample_data)
    
    print(f"\n📈 MASTER SIGNAL RESULTS:")
    print(f"{'='*60}")
    print(f"Primary Signal: {master_signal['primary_signal']}")
    print(f"Signal Strength: {master_signal['signal_strength']:.3f}")
    print(f"Timestamp: {master_signal['timestamp']}")
    
    # Consensus details
    consensus = master_signal.get('consensus_data', {})
    if consensus:
        print(f"\n🤝 CONSENSUS DETAILS:")
        print(f"  Agreement Score: {consensus.get('agreement_score', 0):.3f}")
        print(f"  Participating Strategies: {consensus.get('participating_strategies', 0)}")
        print(f"  Recommendation: {consensus.get('recommendation', 'unknown')}")
        
        # Strategy breakdown
        breakdown = consensus.get('strategy_breakdown', {})
        if breakdown:
            print(f"\n📊 STRATEGY BREAKDOWN:")
            for strategy, details in breakdown.items():
                print(f"  {strategy.upper()}:")
                print(f"    Signal: {details.get('signal', 0)}")
                print(f"    Confidence: {details.get('confidence', 0):.3f}")
                print(f"    Weight: {details.get('weight', 0):.3f}")
    
    # Risk management
    risk_mgmt = master_signal.get('risk_management', {})
    if risk_mgmt:
        print(f"\n⚠️  RISK MANAGEMENT:")
        print(f"  Position Size: {risk_mgmt.get('position_size', 0):.4f}")
        print(f"  Stop Loss: ${risk_mgmt.get('stop_loss', 0):.2f}")
        print(f"  Take Profit: ${risk_mgmt.get('take_profit', 0):.2f}")
        print(f"  Max Loss: ${risk_mgmt.get('max_loss', 0):.2f}")
        print(f"  Risk Score: {risk_mgmt.get('risk_score', 0):.3f}")
    
    # Execution plan
    execution = master_signal.get('execution_plan', {})
    if execution:
        print(f"\n⚡ EXECUTION PLAN:")
        print(f"  Entry Price: ${execution.get('entry_price', 0):.2f}")
        print(f"  Order Type: {execution.get('order_type', 'unknown')}")
        print(f"  Timing: {execution.get('execution_timing', 'unknown')}")
        
        notes = execution.get('execution_notes', [])
        if notes:
            print(f"  Notes: {', '.join(notes)}")
    
    print(f"\n🎯 Advanced Strategy Hub test completed!")
    print(f"{'='*60}")
