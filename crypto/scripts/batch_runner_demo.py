#!/usr/bin/env python3
"""
Enhanced Batch Runner Demo
=========================

This script demonstrates how to use the enhanced batch runner for comprehensive
strategy analysis across multiple timeframes.
"""

import os
import sys
from pathlib import Path

def main():
    print("🚀 Enhanced Batch Runner Demo")
    print("=" * 50)
    
    # Change to crypto scripts directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print(f"📁 Working directory: {os.getcwd()}")
    print()
    
    print("📊 Available Demo Commands:")
    print()
    
    print("1. 🤖 AUTO MODE - Complete Analysis (Recommended)")
    print("   python batch_runner.py --auto --symbols BTC/USDT ETH/USDT")
    print("   → Tests ALL strategies on ALL timeframes")
    print("   → Generates comprehensive comparison report")
    print()
    
    print("2. ⚡ Quick Test - Single Symbol")
    print("   python batch_runner.py --auto --symbols BTC/USDT")
    print("   → Faster testing with one symbol")
    print()
    
    print("3. 🎯 Custom Strategies")
    print("   python batch_runner.py --symbols BTC/USDT --strategies \"BB RSI,MACD Only\"")
    print("   → Test specific strategies only")
    print()
    
    print("4. ⏰ Custom Timeframes")
    print("   python batch_runner.py --symbols BTC/USDT --timeframes 1h 4h 1d")
    print("   → Test specific timeframes only")
    print()
    
    print("5. 🔧 Single Test (Legacy)")
    print("   python batch_runner.py --legacy --symbols BTC/USDT --strategies \"RSI MACD VWAP\" --interval 1h")
    print("   → Single strategy, single timeframe")
    print()
    
    print("📈 Expected Output Files:")
    print("- strategy_comparison_report_YYYYMMDD_HHMMSS.md (Main report)")
    print("- strategy_comparison_data_YYYYMMDD_HHMMSS.csv (Raw data)")
    print("- Individual test results in subdirectories")
    print()
    
    print("🎯 Pro Tips:")
    print("- Start with --auto mode for comprehensive analysis")
    print("- Use single symbol (BTC/USDT) for faster testing")
    print("- Check the markdown report for best strategy recommendations")
    print("- CSV file contains raw data for further analysis")
    
    choice = input("\nWould you like to run a quick demo? (y/n): ").lower().strip()
    
    if choice == 'y':
        print("\n🚀 Running Quick Demo: Auto mode with BTC/USDT")
        print("This will test all strategies on all timeframes...")
        
        import subprocess
        
        cmd = [sys.executable, "batch_runner.py", "--auto", "--symbols", "BTC/USDT", "--bars", "100"]
        
        try:
            result = subprocess.run(cmd, cwd=os.getcwd())
            if result.returncode == 0:
                print("\n✅ Demo completed successfully!")
                print("📁 Check the output directory for results")
            else:
                print("\n❌ Demo failed")
        except Exception as e:
            print(f"\n❌ Error running demo: {e}")
    else:
        print("\n👋 Demo cancelled. Run the commands above manually when ready!")

if __name__ == "__main__":
    main()
