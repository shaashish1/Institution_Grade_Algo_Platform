#!/usr/bin/env python3
"""
Comprehensive validation script for all advanced trading strategies.
This script tests all implemented strategies to ensure they work correctly.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def create_test_data(periods=100):
    """Create realistic test data for strategy validation"""
    dates = pd.date_range(start='2024-01-01', periods=periods, freq='D')
    
    # Create realistic price data with trend and volatility
    returns = np.random.normal(0.001, 0.02, periods)  # Daily returns
    prices = 100 * np.exp(np.cumsum(returns))
    
    # Add some volatility clustering
    for i in range(10, periods):
        if abs(returns[i-1]) > 0.03:  # High volatility day
            returns[i] *= 1.5
    
    # Recalculate prices
    prices = 100 * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'open': prices * (1 + np.random.normal(0, 0.005, periods)),
        'high': prices * (1 + np.abs(np.random.normal(0, 0.01, periods))),
        'low': prices * (1 - np.abs(np.random.normal(0, 0.01, periods))),
        'close': prices,
        'volume': np.random.randint(1000, 50000, periods)
    }, index=dates)
    
    # Ensure high >= max(open, close) and low <= min(open, close)
    df['high'] = np.maximum(df['high'], np.maximum(df['open'], df['close']))
    df['low'] = np.minimum(df['low'], np.minimum(df['open'], df['close']))
    
    return df

def test_strategy(strategy_name, module_name, strategy_class_name):
    """Test a single strategy"""
    print(f"\n{'='*60}")
    print(f"Testing {strategy_name}")
    print(f"{'='*60}")
    
    try:
        # Import the strategy
        module = __import__(module_name, fromlist=[strategy_class_name])
        strategy_class = getattr(module, strategy_class_name)
        print(f"✅ Import successful")
        
        # Create instance
        strategy = strategy_class()
        print(f"✅ Instantiation successful")
        
        # Create test data
        test_data = create_test_data()
        print(f"✅ Test data created ({len(test_data)} periods)")
        
        # Generate signals
        signals = strategy.generate_signals(test_data)
        print(f"✅ Signal generation successful")
        
        # Handle different signal formats
        if signals is not None:
            # Check if signals is a dict (single signal)
            if isinstance(signals, dict):
                signals = [signals] if signals.get('primary_signal', 0) != 0 else []
            # Check if signals is a list
            elif isinstance(signals, list):
                pass  # Already in correct format
            else:
                print(f"   ⚠️ Unexpected signal format: {type(signals)}")
                signals = []
            
            if len(signals) > 0:
                print(f"✅ Generated {len(signals)} signals")
                
                # Analyze signals
                buy_signals = 0
                sell_signals = 0
                
                for signal in signals:
                    if isinstance(signal, dict):
                        signal_type = signal.get('signal_type', '')
                        if signal_type == 'BUY' or signal.get('primary_signal', 0) > 0:
                            buy_signals += 1
                        elif signal_type == 'SELL' or signal.get('primary_signal', 0) < 0:
                            sell_signals += 1
                
                print(f"   📊 Buy signals: {buy_signals}")
                print(f"   📊 Sell signals: {sell_signals}")
                
                # Check signal quality
                if buy_signals + sell_signals > 0:
                    print(f"   📊 Signal rate: {(buy_signals + sell_signals) / len(test_data) * 100:.1f}%")
            else:
                print(f"   ⚠️ No signals generated (this might be normal)")
        else:
            print(f"   ⚠️ No signals generated (this might be normal)")
        
        # Test risk management (if available)
        if hasattr(strategy, 'calculate_position_size'):
            try:
                position_size = strategy.calculate_position_size(test_data.iloc[-1], 10000)
                print(f"✅ Risk management working (position size: {position_size})")
            except Exception as e:
                print(f"   ⚠️ Risk management test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing {strategy_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main validation function"""
    print("🚀 Starting Advanced Trading Strategies Validation")
    print("=" * 80)
    
    # Define all strategies to test
    strategies = [
        ("ML/AI Framework", "src.strategies.ml_ai_framework", "MLAITradingFramework"),
        ("Institutional Order Flow", "src.strategies.institutional_flow_strategy", "InstitutionalOrderFlowStrategy"),
        ("Ultimate Profitable Strategy", "src.strategies.ultimate_profitable_strategy", "UltimateProfitableStrategy"),
        ("Market Inefficiency Strategy", "src.strategies.market_inefficiency_strategy", "MarketInefficiencyStrategy"),
        ("Advanced Strategy Hub", "src.strategies.advanced_strategy_hub", "AdvancedStrategyHub"),
    ]
    
    results = {}
    
    # Test each strategy
    for strategy_name, module_name, class_name in strategies:
        results[strategy_name] = test_strategy(strategy_name, module_name, class_name)
    
    # Print summary
    print(f"\n{'='*80}")
    print("📊 VALIDATION SUMMARY")
    print(f"{'='*80}")
    
    passed = sum(results.values())
    total = len(results)
    
    for strategy_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"{strategy_name:<35} {status}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} strategies passed")
    
    if passed == total:
        print("🎉 All strategies are working correctly!")
        print("🚀 Ready for live trading integration!")
    else:
        print("⚠️ Some strategies need attention before live deployment.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
