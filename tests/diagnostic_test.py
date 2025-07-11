#!/usr/bin/env python3
"""
Simple test to diagnose module loading issues
"""

import sys
import os

# Get the project root directory (parent of tests directory)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_dir = os.path.join(project_root, 'src')

# Add directories to Python path
sys.path.insert(0, project_root)
sys.path.insert(0, src_dir)

# Debug path information
print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")
print(f"Source directory: {src_dir}")
print(f"Source directory exists: {os.path.exists(src_dir)}")
print("Source contents:", os.listdir(src_dir) if os.path.exists(src_dir) else "Not found")
print()

print("Testing module imports...")

# Test 1: Direct import
try:
    from src.strategies.ml_ai_framework import MLAITradingFramework
    print("✅ MLAITradingFramework imported successfully")
except Exception as e:
    print(f"❌ MLAITradingFramework import failed: {e}")

# Test 2: Module import
try:
    import src.strategies.ml_ai_framework as ml_module
    print(f"✅ Module imported. Attributes: {[attr for attr in dir(ml_module) if 'Framework' in attr or 'AI' in attr]}")
except Exception as e:
    print(f"❌ Module import failed: {e}")

# Test 3: Market Inefficiency Strategy
try:
    from src.strategies.market_inefficiency_strategy import MarketInefficiencyStrategy
    print("✅ MarketInefficiencyStrategy imported successfully")
    
    # Test instantiation
    strategy = MarketInefficiencyStrategy()
    print("✅ MarketInefficiencyStrategy instantiated successfully")
except Exception as e:
    print(f"❌ MarketInefficiencyStrategy failed: {e}")

# Test 4: Advanced Strategy Hub
try:
    from src.strategies.advanced_strategy_hub import AdvancedStrategyHub
    print("✅ AdvancedStrategyHub imported successfully")
    
    # Test instantiation
    hub = AdvancedStrategyHub()
    print("✅ AdvancedStrategyHub instantiated successfully")
    
    # Test generate_signals method
    if hasattr(hub, 'generate_signals'):
        print("✅ generate_signals method exists")
    else:
        print("❌ generate_signals method missing")
except Exception as e:
    print(f"❌ AdvancedStrategyHub failed: {e}")

print("Diagnostic complete.")
