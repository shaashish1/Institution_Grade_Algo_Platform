#!/usr/bin/env python3
"""
Simple import test to verify all modules are working
"""

import sys
import os

# Add project root to path
project_root = r"D:\AlgoProject"
sys.path.insert(0, project_root)

print("Testing module imports from D:\\AlgoProject...")
print("=" * 50)

# Test 1: ML AI Framework
try:
    from strategies.ml_ai_framework import MLAITradingFramework
    print("✅ MLAITradingFramework - PASS")
except Exception as e:
    print(f"❌ MLAITradingFramework - FAIL: {e}")

# Test 2: Market Inefficiency Strategy
try:
    from strategies.market_inefficiency_strategy import MarketInefficiencyStrategy
    strategy = MarketInefficiencyStrategy()
    print("✅ MarketInefficiencyStrategy - PASS")
except Exception as e:
    print(f"❌ MarketInefficiencyStrategy - FAIL: {e}")

# Test 3: Advanced Strategy Hub
try:
    from strategies.advanced_strategy_hub import AdvancedStrategyHub
    hub = AdvancedStrategyHub()
    print("✅ AdvancedStrategyHub - PASS")
except Exception as e:
    print(f"❌ AdvancedStrategyHub - FAIL: {e}")

# Test 4: Crypto data acquisition
try:
    from crypto.data_acquisition import CryptoDataFetcher
    fetcher = CryptoDataFetcher()
    print("✅ CryptoDataFetcher - PASS")
except Exception as e:
    print(f"❌ CryptoDataFetcher - FAIL: {e}")

# Test 5: Backtest engine
try:
    from backtest.backtest_engine import BacktestEngine
    engine = BacktestEngine()
    print("✅ BacktestEngine - PASS")
except Exception as e:
    print(f"❌ BacktestEngine - FAIL: {e}")

print("=" * 50)
print("Import test complete!")
