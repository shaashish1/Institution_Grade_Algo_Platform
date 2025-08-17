#!/usr/bin/env python3
"""
List all available CCXT exchanges
"""

def list_exchanges():
    """List all available CCXT exchanges"""
    try:
        import ccxt
        exchanges = ccxt.exchanges
        print("📊 Available CCXT Exchanges:")
        print("=" * 40)
        
        for i, exchange in enumerate(exchanges, 1):
            print(f"{i:3d}. {exchange}")
        
        print(f"\nTotal: {len(exchanges)} exchanges")
        return exchanges
        
    except ImportError as e:
        print(f"❌ CCXT not available: {e}")
        return []
    except Exception as e:
        print(f"❌ Error listing exchanges: {e}")
        return []

def main():
    """Main function"""
    list_exchanges()

if __name__ == "__main__":
    main()
