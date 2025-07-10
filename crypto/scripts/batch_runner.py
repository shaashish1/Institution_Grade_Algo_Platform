#!/usr/bin/env python3
"""
Batch Runner for Enhanced Crypto Backtest
==========================================

This script allows running multiple backtests with different configurations
and generates comprehensive reports comparing all strategies.
"""

import argparse
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

def run_backtest(symbols, strategies, interval, bars, capital, position, exchange, output_dir):
    """Run a single backtest with specified parameters"""
    
    # Get the script path relative to current directory
    script_path = "enhanced_crypto_backtest.py"
    
    # Build command
    cmd = [
        sys.executable, 
        script_path,
        "--symbols"] + symbols + [
        "--compare",
        "--interval", interval,
        "--bars", str(bars),
        "--capital", str(capital),
        "--position", str(position),
        "--exchange", exchange,
        "--output", output_dir
    ]
    
    if strategies:
        # When strategies are specified, the script will use them in comparison mode
        pass
    
    print(f"🚀 Running backtest: {' '.join(cmd)}")
    print("=" * 80)
    
    # Run the backtest
    try:
        result = subprocess.run(cmd, capture_output=False, text=True, cwd=os.getcwd())
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running backtest: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Batch runner for Enhanced Crypto Backtest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_runner.py --symbols BTC/USDT ETH/USDT --strategies BB_RSI,MACD_Only
  python batch_runner.py --symbols BTC/USDT --interval 4h --bars 1000
  python batch_runner.py --symbols BTC/USDT ETH/USDT LTC/USDT --strategies BB_RSI,MACD_Only,RSI_MACD_VWAP
        """
    )
    
    parser.add_argument("--symbols", "-s", nargs="+", default=["BTC/USDT", "ETH/USDT"],
                        help="Symbols to test (default: BTC/USDT ETH/USDT)")
    parser.add_argument("--strategies", type=str, 
                        help="Comma-separated list of strategies to test (default: all)")
    parser.add_argument("--interval", "-i", default="1h",
                        choices=["1m", "5m", "15m", "30m", "1h", "4h", "1d"],
                        help="Time interval (default: 1h)")
    parser.add_argument("--bars", "-b", type=int, default=720,
                        help="Number of bars to fetch (default: 720)")
    parser.add_argument("--capital", "-c", type=int, default=100000,
                        help="Initial capital (default: 100000)")
    parser.add_argument("--position", "-p", type=int, default=10000,
                        help="Position size per trade (default: 10000)")
    parser.add_argument("--exchange", "-e", default="kraken",
                        choices=["binance", "kraken", "coinbase", "bitfinex"],
                        help="Exchange to use (default: kraken)")
    parser.add_argument("--output", "-o", default="output",
                        help="Output directory (default: output)")
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # Create timestamp for this batch run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_output_dir = output_dir / f"batch_run_{timestamp}"
    batch_output_dir.mkdir(exist_ok=True)
    
    print("🔄 Enhanced Crypto Backtest - Batch Runner")
    print("=" * 80)
    print(f"📊 Symbols: {', '.join(args.symbols)}")
    print(f"⏰ Interval: {args.interval}")
    print(f"📈 Bars: {args.bars}")
    print(f"💰 Capital: ${args.capital:,}")
    print(f"📊 Position: ${args.position:,}")
    print(f"🏢 Exchange: {args.exchange}")
    print(f"📁 Output: {batch_output_dir}")
    if args.strategies:
        print(f"🧪 Strategies: {args.strategies}")
    else:
        print("🧪 Strategies: All available strategies")
    print("=" * 80)
    
    # Run the backtest
    success = run_backtest(
        symbols=args.symbols,
        strategies=args.strategies.split(",") if args.strategies else None,
        interval=args.interval,
        bars=args.bars,
        capital=args.capital,
        position=args.position,
        exchange=args.exchange,
        output_dir=str(batch_output_dir)
    )
    
    if success:
        print("\n✅ Batch run completed successfully!")
        print(f"📁 Results saved to: {batch_output_dir}")
    else:
        print("\n❌ Batch run failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
