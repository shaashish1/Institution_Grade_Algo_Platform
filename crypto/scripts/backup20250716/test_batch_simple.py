#!/usr/bin/env python3
"""
Simple test for batch runner functionality in the crypto/scripts folder
"""
import sys
import os
from pathlib import Path

def test_batch_runner_simple():
    """Test batch runner components without subprocess"""
    print("🔬 BATCH RUNNER COMPONENT TEST")
    print("=" * 40)
    
    try:
        # Test basic imports
        print("1. Testing imports...")
        from batch_runner import discover_strategies, load_crypto_symbols
        print("   ✅ Imports successful")
        
        # Test strategy discovery
        print("2. Testing strategy discovery...")
        strategies = discover_strategies()
        print(f"   ✅ Found {len(strategies)} strategies:")
        for i, strategy in enumerate(strategies[:3], 1):
            print(f"      {i}. {strategy['name']}")
        if len(strategies) > 3:
            print(f"      ... and {len(strategies)-3} more")
        
        # Test symbol loading
        print("3. Testing symbol loading...")
        symbols = load_crypto_symbols()
        print(f"   ✅ Found {len(symbols)} symbols:")
        print(f"      First 5: {symbols[:5]}")
        
        print(f"\n✅ All components working!")
        print(f"📊 Ready for backtesting: {len(strategies)} strategies × {len(symbols)} symbols")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_batch_runner_simple()
