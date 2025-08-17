"""
Quick AlgoProject System Test
============================
"""

import sys
import os

# Add algoproject to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def quick_test():
    """Quick test of core components"""
    print("🚀 AlgoProject Quick System Test")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Core Interfaces
    total_tests += 1
    try:
        from algoproject.core.interfaces import MarketData, Signal, Position
        from datetime import datetime
        
        market_data = MarketData(
            symbol="BTCUSDT",
            timestamp=datetime.now(),
            open=50000.0,
            high=51000.0,
            low=49500.0,
            close=50500.0,
            volume=1000.0,
            exchange="binance"
        )
        print("✅ Core interfaces working")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Core interfaces failed: {e}")
    
    # Test 2: Configuration
    total_tests += 1
    try:
        from algoproject.core.config_manager import ConfigManager
        config = ConfigManager()
        config.set_setting("test", "key", "value")
        assert config.get_setting("test", "key") == "value"
        print("✅ Configuration manager working")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
    
    # Test 3: Portfolio
    total_tests += 1
    try:
        from algoproject.backtesting.portfolio import Portfolio
        portfolio = Portfolio(100000.0)
        success = portfolio.buy("BTCUSDT", 1.0, 50000.0)
        assert success
        assert portfolio.get_position_quantity("BTCUSDT") == 1.0
        print("✅ Portfolio management working")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Portfolio failed: {e}")
    
    # Test 4: Base Strategy
    total_tests += 1
    try:
        from algoproject.strategies.base_strategy import BaseStrategy
        from algoproject.core.interfaces import MarketData, Signal
        
        class TestStrategy(BaseStrategy):
            def next(self, data: MarketData):
                return [Signal(
                    symbol=data.symbol,
                    action="buy",
                    quantity=1.0,
                    price=data.close
                )]
        
        strategy = TestStrategy("Test", {})
        print("✅ Base strategy working")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Base strategy failed: {e}")
    
    print("=" * 40)
    print(f"📊 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All core components working!")
        return True
    else:
        print("⚠️ Some components need attention")
        return False

if __name__ == "__main__":
    success = quick_test()
    
    if success:
        print("\n🚀 System is ready! Creating UI...")
    else:
        print("\n⚠️ Please check the failed components")