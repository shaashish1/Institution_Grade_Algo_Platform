#!/usr/bin/env python3
"""
Test the interactive crypto demo functionality
"""

def test_interactive_demo():
    """Test the interactive demo features"""
    
    print("🧪 TESTING INTERACTIVE CRYPTO DEMO FEATURES")
    print("=" * 60)
    
    # Import and test the functions
    try:
        from interactive_crypto_demo import (
            get_available_strategies, 
            get_available_timeframes, 
            display_best_strategies_from_backtest
        )
        
        print("✅ All imports successful")
        
        print("\n1. Testing strategy list...")
        strategies = get_available_strategies()
        print(f"   Found {len(strategies)} strategies:")
        for i, strategy in enumerate(strategies, 1):
            print(f"   {i}. {strategy['name']}")
        
        print("\n2. Testing timeframe list...")
        timeframes = get_available_timeframes()
        print(f"   Found {len(timeframes)} timeframes:")
        for i, tf in enumerate(timeframes, 1):
            print(f"   {i}. {tf['name']} - {tf['description']}")
        
        print("\n3. Testing backtest recommendations display...")
        display_best_strategies_from_backtest()
        
        print("\n✅ All interactive demo features working!")
        print("\n📋 To run full interactive demo:")
        print("   python crypto\\scripts\\interactive_crypto_demo.py")
        print("\n🎮 The interactive demo will prompt you to:")
        print("   1. Select strategy from numbered list")
        print("   2. Select timeframe from numbered list") 
        print("   3. Enter capital amount")
        print("   4. Enter demo duration")
        print("   5. Confirm and run live simulation")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_interactive_demo()
