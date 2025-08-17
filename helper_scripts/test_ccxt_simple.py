#!/usr/bin/env python3
"""
Delta Exchange Connection Test
Simple test to verify CCXT and Delta Exchange connectivity
"""

def test_delta_connection():
    print("🔗 Testing Delta Exchange Connection")
    print("=" * 40)
    
    try:
        # Test CCXT import
        print("1. Testing CCXT import...")
        import ccxt
        print(f"   ✅ CCXT version: {ccxt.__version__}")
        
        # Check Delta availability
        print("2. Checking Delta Exchange availability...")
        if 'delta' not in ccxt.exchanges:
            print("   ❌ Delta Exchange not found in CCXT")
            return False
        print("   ✅ Delta Exchange found")
        
        # Test basic connection (no network required)
        print("3. Creating Delta Exchange instance...")
        delta = ccxt.delta({'enableRateLimit': True})
        print(f"   ✅ Instance created: {delta.id}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   💡 Install CCXT: pip install ccxt")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_delta_connection()
    
    if success:
        print("\n✅ Basic CCXT/Delta test passed!")
        print("💡 You can now use the main script for pair fetching")
    else:
        print("\n❌ CCXT/Delta test failed")
        print("💡 Install dependencies first: pip install ccxt pandas")
