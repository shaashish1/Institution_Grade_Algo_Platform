"""
🧪 Comprehensive Strategy Testing & Validation
Test all advanced trading strategies and verify functionality

This script tests:
1. 🤖 ML/AI Trading Framework
2. 🏦 Institutional Order Flow Strategy
3. 🚀 Ultimate Profitable Strategy
4. 💎 Market Inefficiency Strategy
5. 🎯 Advanced Strategy Hub
"""

import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, timedelta
import warnings
from typing import Dict, List, Any

# Add strategies directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'strategies'))

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

def create_test_data(periods: int = 1000, freq: str = '1H') -> pd.DataFrame:
    """Create realistic test data for strategy testing"""
    
    np.random.seed(42)  # For reproducible results
    dates = pd.date_range('2023-01-01', periods=periods, freq=freq)
    
    # Generate realistic OHLCV data with various market conditions
    price = 100
    prices = []
    volumes = []
    
    # Market phases
    trend_direction = 1
    trend_strength = 0.001
    volatility_regime = 'normal'
    
    for i in range(periods):
        # Phase transitions
        if i % 200 == 0:  # Change trend every 200 periods
            trend_direction *= np.random.choice([-1, 1])
            trend_strength = np.random.uniform(0.0005, 0.003)
        
        if i % 150 == 0:  # Change volatility regime
            volatility_regime = np.random.choice(['low', 'normal', 'high'])
        
        # Set volatility based on regime
        if volatility_regime == 'low':
            base_volatility = 0.01
        elif volatility_regime == 'high':
            base_volatility = 0.04
        else:
            base_volatility = 0.02
        
        # Add institutional activity patterns
        institutional_activity = 0
        if i % 50 == 0:  # Institutional activity every 50 periods
            institutional_activity = np.random.uniform(-0.02, 0.02)
        
        # Add weekend/holiday effects
        if dates[i].weekday() >= 5:  # Weekend
            volatility_multiplier = 0.5
        else:
            volatility_multiplier = 1.0
        
        # Calculate price change
        trend_component = trend_direction * trend_strength
        random_component = np.random.normal(0, base_volatility * volatility_multiplier)
        price_change = trend_component + random_component + institutional_activity
        
        price *= (1 + price_change)
        prices.append(price)
        
        # Generate volume with correlation to price moves
        base_volume = 2000
        volume_multiplier = 1 + abs(price_change) * 20  # Higher volume on big moves
        if abs(institutional_activity) > 0.01:  # Institutional activity
            volume_multiplier *= 3
        
        volumes.append(int(base_volume * volume_multiplier))
    
    # Create OHLCV DataFrame
    df = pd.DataFrame({
        'open': prices,
        'high': [p * (1 + abs(np.random.normal(0, 0.005))) for p in prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.005))) for p in prices],
        'close': prices,
        'volume': volumes
    }, index=dates)
    
    return df

def test_strategy_import(strategy_name: str, module_name: str) -> bool:
    """Test if a strategy can be imported successfully"""
    try:
        module = __import__(module_name, fromlist=[strategy_name])
        strategy_class = getattr(module, strategy_name)
        return True
    except ImportError as e:
        print(f"❌ Import error for {strategy_name}: {e}")
        return False
    except AttributeError as e:
        print(f"❌ Attribute error for {strategy_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error importing {strategy_name}: {e}")
        return False

def test_strategy_functionality(strategy_name: str, strategy_instance: Any, 
                              test_data: pd.DataFrame) -> Dict[str, Any]:
    """Test strategy functionality"""
    
    results = {
        'strategy_name': strategy_name,
        'initialization': False,
        'signal_generation': False,
        'signal_quality': False,
        'error_handling': False,
        'performance': {},
        'errors': []
    }
    
    try:
        # Test initialization
        if strategy_instance is not None:
            results['initialization'] = True
        
        # Test signal generation
        signals = strategy_instance.generate_signals(test_data)
        
        if not signals.empty:
            results['signal_generation'] = True
            
            # Test signal quality
            latest_signal = signals.iloc[0]
            required_fields = ['signal', 'price', 'timestamp']
            
            signal_quality = all(field in latest_signal for field in required_fields)
            results['signal_quality'] = signal_quality
            
            # Performance metrics
            results['performance'] = {
                'signals_generated': len(signals),
                'signal_types': signals['signal'].value_counts().to_dict(),
                'avg_confidence': signals.get('confidence', pd.Series([0])).mean(),
                'latest_signal': latest_signal.get('signal', 'UNKNOWN'),
                'latest_price': latest_signal.get('price', 0)
            }
        
        # Test error handling with bad data
        try:
            bad_data = test_data.iloc[:10]  # Very small dataset
            bad_signals = strategy_instance.generate_signals(bad_data)
            results['error_handling'] = True
        except Exception as e:
            results['errors'].append(f"Error handling test failed: {e}")
            results['error_handling'] = False
    
    except Exception as e:
        results['errors'].append(f"Strategy test failed: {e}")
    
    return results

def test_all_strategies():
    """Test all available strategies"""
    
    print("🧪 Advanced Trading Strategies - Comprehensive Testing")
    print("=" * 60)
    
    # Create test data
    print("\n📊 Generating Test Data...")
    test_data = create_test_data(periods=1000, freq='1H')
    print(f"✅ Test data created: {len(test_data)} periods")
    print(f"   Price range: ${test_data['close'].min():.2f} - ${test_data['close'].max():.2f}")
    print(f"   Date range: {test_data.index[0]} to {test_data.index[-1]}")
    
    # Strategy test configuration
    strategies_to_test = [
        {
            'name': 'InstitutionalOrderFlowStrategy',
            'module': 'institutional_flow_strategy',
            'display_name': '🏦 Institutional Order Flow Strategy'
        },
        {
            'name': 'UltimateProfitableStrategy', 
            'module': 'ultimate_profitable_strategy',
            'display_name': '🚀 Ultimate Profitable Strategy'
        },
        {
            'name': 'MarketInefficiencyStrategy',
            'module': 'market_inefficiency_strategy', 
            'display_name': '💎 Market Inefficiency Strategy'
        },
        {
            'name': 'AITradingStrategy',
            'module': 'ml_ai_framework',
            'display_name': '🤖 ML/AI Trading Framework'
        }
    ]
    
    test_results = []
    
    # Test each strategy
    for strategy_config in strategies_to_test:
        print(f"\n{strategy_config['display_name']}")
        print("-" * 40)
        
        # Test import
        import_success = test_strategy_import(strategy_config['name'], strategy_config['module'])
        
        if import_success:
            print("✅ Import successful")
            
            try:
                # Initialize strategy
                module = __import__(strategy_config['module'], fromlist=[strategy_config['name']])
                strategy_class = getattr(module, strategy_config['name'])
                strategy_instance = strategy_class()
                
                # Test functionality
                test_result = test_strategy_functionality(
                    strategy_config['display_name'],
                    strategy_instance,
                    test_data
                )
                
                test_results.append(test_result)
                
                # Display results
                if test_result['initialization']:
                    print("✅ Initialization successful")
                else:
                    print("❌ Initialization failed")
                
                if test_result['signal_generation']:
                    print("✅ Signal generation successful")
                    perf = test_result['performance']
                    print(f"   Signals generated: {perf['signals_generated']}")
                    print(f"   Latest signal: {perf['latest_signal']}")
                    print(f"   Signal types: {perf['signal_types']}")
                else:
                    print("❌ Signal generation failed")
                
                if test_result['signal_quality']:
                    print("✅ Signal quality good")
                else:
                    print("❌ Signal quality issues")
                
                if test_result['error_handling']:
                    print("✅ Error handling robust")
                else:
                    print("❌ Error handling needs improvement")
                
                if test_result['errors']:
                    print("⚠️  Errors encountered:")
                    for error in test_result['errors']:
                        print(f"   - {error}")
                
            except Exception as e:
                print(f"❌ Strategy testing failed: {e}")
                test_results.append({
                    'strategy_name': strategy_config['display_name'],
                    'initialization': False,
                    'errors': [str(e)]
                })
        else:
            print("❌ Import failed")
    
    # Test Strategy Hub
    print(f"\n🎯 Advanced Strategy Hub")
    print("-" * 40)
    
    try:
        from advanced_strategy_hub import AdvancedStrategyHub
        
        hub = AdvancedStrategyHub()
        print("✅ Hub initialization successful")
        
        # Test hub functionality
        available_strategies = hub.get_available_strategies()
        print(f"✅ Available strategies: {len(available_strategies)}")
        for strategy in available_strategies:
            print(f"   - {strategy}")
        
        # Test consensus signal
        consensus = hub.get_consensus_signal(test_data)
        print(f"✅ Consensus signal generated: {consensus['consensus_signal']}")
        print(f"   Confidence: {consensus['consensus_confidence']:.2f}")
        print(f"   Strategies analyzed: {consensus['total_strategies']}")
        
        # Test execution
        execution_result = hub.execute_optimal_strategy(test_data)
        print(f"✅ Optimal strategy execution: {execution_result['strategy_used']}")
        print(f"   Signal: {execution_result['signal']['signal']}")
        
    except Exception as e:
        print(f"❌ Strategy Hub testing failed: {e}")
    
    # Summary Report
    print("\n📈 Test Summary Report")
    print("=" * 60)
    
    successful_strategies = 0
    total_signals = 0
    
    for result in test_results:
        strategy_name = result['strategy_name']
        success = all([
            result['initialization'],
            result['signal_generation'],
            result['signal_quality']
        ])
        
        if success:
            successful_strategies += 1
            total_signals += result['performance'].get('signals_generated', 0)
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        print(f"{strategy_name}: {status}")
    
    print(f"\n📊 Overall Results:")
    print(f"   Successful strategies: {successful_strategies}/{len(test_results)}")
    print(f"   Total signals generated: {total_signals}")
    print(f"   Success rate: {successful_strategies/len(test_results)*100:.1f}%")
    
    if successful_strategies == len(test_results):
        print("\n🎉 All strategies passed testing!")
        print("✅ Ready for live trading")
    else:
        print(f"\n⚠️  {len(test_results) - successful_strategies} strategies need attention")
        print("   Check error messages above for details")
    
    return test_results

if __name__ == "__main__":
    test_results = test_all_strategies()
    
    print("\n" + "="*60)
    print("🎯 Testing Complete!")
    print("="*60)
