#!/usr/bin/env python3
"""
Test script to debug enhanced_crypto_backtest.py issues
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

print("🔍 Testing enhanced_crypto_backtest.py imports...")

try:
    print("1. Testing basic imports...")
    import pandas as pd
    import numpy as np
    print("   ✅ Basic imports successful")
    
    print("2. Testing crypto imports...")
    from crypto.data_acquisition import fetch_data
    print("   ✅ Crypto imports successful")
    
    print("3. Testing strategy imports...")
    from strategies.rsi_macd_vwap_strategy import RSI_MACD_VWAP_Strategy
    print("   ✅ RSI_MACD_VWAP_Strategy imported")
    
    from strategies.enhanced_multi_factor import EnhancedMultiFactorStrategy
    print("   ✅ EnhancedMultiFactorStrategy imported")
    
    from strategies.bb_rsi_strategy import BB_RSI_Strategy
    print("   ✅ BB_RSI_Strategy imported")
    
    print("4. Testing BacktestEvaluator import...")
    from crypto.tools.backtest_evaluator import BacktestEvaluator
    print("   ✅ BacktestEvaluator imported")
    
    print("5. Testing data fetch...")
    print("   Fetching sample data for BTC/USDT...")
    data = fetch_data('BTC/USDT', bars=50, interval='1h', exchange='kraken')
    if data is not None and len(data) > 0:
        print(f"   ✅ Data fetch successful: {len(data)} bars retrieved")
    else:
        print("   ❌ Data fetch failed or returned empty data")
    
    print("6. Testing EnhancedCryptoBacktest import...")
    from enhanced_crypto_backtest import EnhancedCryptoBacktest
    print("   ✅ EnhancedCryptoBacktest imported")
    
    print("🎉 All tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
