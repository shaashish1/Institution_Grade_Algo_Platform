#!/usr/bin/env python3
"""
Delta Backtest Interactive Demo
Demonstrates the enhanced interactive CSV file selection
"""

import os
import sys

# Add crypto module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def demo_csv_file_selection():
    """Demonstrate the CSV file selection process."""
    print("🎯 DELTA BACKTEST INTERACTIVE DEMO")
    print("="*60)
    
    # Check input directory
    input_dir = os.path.join(os.path.dirname(__file__), '..', 'input')
    
    print(f"📁 Input Directory: {input_dir}")
    
    if os.path.exists(input_dir):
        files = os.listdir(input_dir)
        csv_files = [f for f in files if f.startswith('delta_') and f.endswith('.csv')]
        
        print(f"\n📄 Found CSV Files:")
        if csv_files:
            for i, csv_file in enumerate(csv_files, 1):
                category = csv_file.replace('delta_', '').replace('.csv', '')
                category_display = category.replace('_', ' ').title()
                
                # Try to count lines
                file_path = os.path.join(input_dir, csv_file)
                try:
                    with open(file_path, 'r') as f:
                        line_count = len(f.readlines()) - 1  # Subtract header
                    print(f"   {i}. 📊 {category_display} ({line_count} pairs)")
                except:
                    print(f"   {i}. 📊 {category_display} ({csv_file})")
        else:
            print("   ❌ No Delta Exchange CSV files found")
            print("   💡 Run: python delta_fetch_symbols.py to create them")
        
        print(f"\n📋 All Files in Input Directory:")
        for file in files:
            print(f"   📄 {file}")
    else:
        print(f"❌ Input directory does not exist: {input_dir}")
    
    print(f"\n🚀 USAGE EXAMPLES:")
    print(f"   # Interactive mode with CSV selection")
    print(f"   python delta_backtest_strategies.py --interactive")
    print(f"")
    print(f"   # Direct CSV loading")
    print(f"   python delta_backtest_strategies.py --load-csv spot_usdt")
    print(f"")
    print(f"   # Create CSV files first")
    print(f"   python delta_fetch_symbols.py")
    print(f"")
    print(f"   # Then use interactive mode")
    print(f"   python delta_backtest_strategies.py --interactive")

if __name__ == "__main__":
    demo_csv_file_selection()
