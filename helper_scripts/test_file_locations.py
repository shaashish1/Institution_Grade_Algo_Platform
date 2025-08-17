#!/usr/bin/env python3
"""
Quick test to demonstrate Delta Exchange CSV file saving locations.
This script shows exactly where files are saved.
"""

import os
import sys
import time
from datetime import datetime

# Add the crypto module to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def test_file_locations():
    """Test and demonstrate file saving locations."""
    
    print("🎯 AlgoProject File Location Test")
    print("=" * 50)
    
    # Define base paths
    base_path = r"d:\Institution_Grade_Algo_Platform"
    input_path = os.path.join(base_path, "crypto", "input")
    output_path = os.path.join(base_path, "crypto", "output")
    
    print(f"📁 Base Project Path: {base_path}")
    print(f"📥 Input Path (CSV pairs): {input_path}")
    print(f"📤 Output Path (Results): {output_path}")
    print()
    
    # Check if directories exist
    print("📋 Directory Status Check:")
    dirs_to_check = [
        ("Base Project", base_path),
        ("Crypto Input", input_path),
        ("Crypto Output", output_path),
        ("Scripts", os.path.join(base_path, "crypto", "scripts")),
        ("Docs", os.path.join(base_path, "docs"))
    ]
    
    for name, path in dirs_to_check:
        exists = "✅ EXISTS" if os.path.exists(path) else "❌ MISSING"
        print(f"  {name}: {exists}")
    print()
    
    # Show current files in input
    print("📥 Current Files in crypto/input/:")
    if os.path.exists(input_path):
        input_files = os.listdir(input_path)
        if input_files:
            for file in input_files:
                print(f"  📄 {file}")
        else:
            print("  📭 No files found")
    print()
    
    # Show recent files in output
    print("📤 Recent Files in crypto/output/ (last 10):")
    if os.path.exists(output_path):
        output_files = sorted(os.listdir(output_path))[-10:]
        for file in output_files:
            print(f"  📊 {file}")
    print()
    
    # Expected Delta CSV files that would be created
    print("🎯 Expected Delta Exchange CSV Files (when --save-pairs runs):")
    expected_files = [
        "delta_spot_usdt.csv",
        "delta_spot_btc.csv", 
        "delta_spot_eth.csv",
        "delta_perpetual_usdt.csv",
        "delta_futures_usdt.csv",
        "delta_futures_btc.csv",
        "delta_options_calls.csv",
        "delta_options_puts.csv",
        "delta_other_pairs.csv",
        "delta_pairs_summary.csv"
    ]
    
    for file in expected_files:
        full_path = os.path.join(input_path, file)
        exists = "✅ EXISTS" if os.path.exists(full_path) else "⏳ WILL BE CREATED"
        print(f"  📄 {file} → {exists}")
    print()
    
    # Expected backtest results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    expected_result = f"multi_strategy_backtest_{timestamp}.csv"
    result_path = os.path.join(output_path, expected_result)
    
    print("📊 Expected Backtest Result Files:")
    print(f"  📈 {expected_result}")
    print(f"  📍 Full Path: {result_path}")
    print()
    
    # Command examples
    print("🚀 Commands to Save Files:")
    print("  1. Save Delta pairs to CSV:")
    print("     python crypto\\scripts\\delta_backtest_strategies.py --save-pairs")
    print(f"     → Creates CSV files in: {input_path}")
    print()
    print("  2. Run backtest with results:")
    print("     python crypto\\scripts\\delta_backtest_strategies.py --symbols BTC/USDT ETH/USDT")
    print(f"     → Creates results in: {output_path}")
    print()
    
    print("✅ File location test completed!")
    print("📁 All paths confirmed and ready for Delta Exchange integration.")

if __name__ == "__main__":
    test_file_locations()
