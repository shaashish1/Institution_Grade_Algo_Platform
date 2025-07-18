#!/usr/bin/env python3
"""
Crypto Assets CSV Manager
========================

This script manages the crypto_assets.csv file used by batch_runner_demo.py
and other crypto scripts. It provides utilities to:
1. Check current crypto_assets.csv status
2. Regenerate the file using CCXT validation
3. View and manage the symbol list
"""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def get_crypto_assets_path():
    """Get the path to crypto_assets.csv"""
    return Path(__file__).parent / "input" / "crypto_assets.csv"

def check_crypto_assets_status():
    """Check the current status of crypto_assets.csv"""
    print("📊 Crypto Assets CSV Status")
    print("=" * 40)
    
    assets_file = get_crypto_assets_path()
    
    if assets_file.exists():
        try:
            df = pd.read_csv(assets_file)
            print(f"✅ File exists: {assets_file}")
            print(f"📈 Total symbols: {len(df)}")
            print(f"🏢 Exchanges: {', '.join(df['exchange'].unique())}")
            print(f"💰 Quote currencies: {', '.join(df['quote_currency'].unique())}")
            print(f"📅 Last validation: {df['validated_date'].iloc[0] if len(df) > 0 else 'Unknown'}")
            
            print(f"\n🔝 Top 10 symbols:")
            for i, row in df.head(10).iterrows():
                print(f"   {row['symbol']} ({row['exchange']}) - ${row['price']}")
                
            return True, df
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False, None
    else:
        print(f"❌ File not found: {assets_file}")
        print("💡 Use the regenerate option to create it")
        return False, None

def regenerate_crypto_assets():
    """Regenerate crypto_assets.csv using CCXT validation"""
    print("🔄 Regenerating crypto_assets.csv...")
    
    try:
        # Import and run the validator
        sys.path.insert(0, str(Path(__file__).parent.parent / "helper_scripts"))
        from ccxt_symbol_validator import CCXTSymbolValidator
        
        validator = CCXTSymbolValidator()
        
        # Validate symbols from both exchanges
        print("📡 Validating Kraken symbols...")
        kraken_results = validator.validate_exchange_symbols('kraken', 20)
        
        print("📡 Validating Binance symbols...")  
        binance_results = validator.validate_exchange_symbols('binance', 20)
        
        # Save combined results
        all_results = kraken_results + binance_results
        output_file = validator.save_validated_symbols(all_results)
        
        print(f"✅ Successfully regenerated {output_file}")
        print(f"📈 Total symbols validated: {len(all_results)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error regenerating file: {e}")
        return False

def view_symbols_by_exchange():
    """View symbols grouped by exchange"""
    print("🏢 Symbols by Exchange")
    print("=" * 40)
    
    success, df = check_crypto_assets_status()
    if not success:
        return
        
    for exchange in df['exchange'].unique():
        exchange_df = df[df['exchange'] == exchange]
        print(f"\n{exchange.upper()} ({len(exchange_df)} symbols):")
        for _, row in exchange_df.iterrows():
            print(f"  {row['symbol']:<12} ${row['price']:>10}")

def main():
    """Main menu for crypto assets management"""
    print("🚀 Crypto Assets CSV Manager")
    print("=" * 50)
    print()
    
    while True:
        print("Available commands:")
        print("1. 📊 Check current status")
        print("2. 🔄 Regenerate crypto_assets.csv")
        print("3. 🏢 View symbols by exchange")
        print("4. 🚪 Exit")
        print()
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            print()
            check_crypto_assets_status()
            print()
            
        elif choice == '2':
            print()
            regenerate_crypto_assets()
            print()
            
        elif choice == '3':
            print()
            view_symbols_by_exchange()
            print()
            
        elif choice == '4':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")
            print()

if __name__ == "__main__":
    main()
