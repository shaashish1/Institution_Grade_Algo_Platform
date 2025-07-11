#!/usr/bin/env python3
"""
Advanced Batch Runner for Enhanced Crypto Backtest
==================================================

This script runs comprehensive multi-strategy, multi-timeframe backtests
and generates detailed comparison reports to identify the best performing
strategies across different market conditions.

Features:
- Auto-discovery of all available strategies
- Multi-timeframe analysis (5m to 1d)
- Comprehensive performance comparison tables
- Best strategy identification per timeframe
- Detailed performance metrics and rankings
"""

import argparse
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path
import pandas as pd
import glob
import json
from tabulate import tabulate

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

def discover_strategies():
    """Auto-discover all available strategies from the strategies folder"""
    # Map strategy files to their expected names in enhanced_crypto_backtest.py
    strategy_mapping = {
        'bb_rsi_strategy.py': 'BB_RSI',
        'enhanced_multi_factor.py': 'Enhanced_Multi_Factor',
        'macd_only_strategy.py': 'MACD_Only',
        'optimized_crypto_v2.py': 'Optimized_Crypto_V2',
        'rsi_macd_vwap_strategy.py': 'RSI_MACD_VWAP',
        'sma_cross.py': 'SMA_Cross'
    }
    
    strategies_path = Path(__file__).resolve().parent.parent.parent / "strategies"
    strategy_files = glob.glob(str(strategies_path / "*.py"))
    
    strategies = []
    
    for file_path in strategy_files:
        filename = os.path.basename(file_path)
        if filename in strategy_mapping:
            strategies.append({
                'name': strategy_mapping[filename],
                'file': filename,
                'path': file_path
            })
    
    print(f"🔍 Discovered {len(strategies)} compatible strategies")
    return strategies

def load_crypto_symbols():
    """Auto-load all crypto symbols from crypto_assets.csv file"""
    try:
        # Path to crypto assets file
        assets_file = Path(__file__).resolve().parent.parent / "input" / "crypto_assets.csv"
        
        if assets_file.exists():
            import pandas as pd
            df = pd.read_csv(assets_file)
            symbols = df['symbol'].tolist()
            print(f"📊 Loaded {len(symbols)} symbols from crypto_assets.csv")
            return symbols
        else:
            print(f"⚠️  crypto_assets.csv not found at {assets_file}")
            print("🔄 Using default symbols")
            return ["BTC/USDT", "ETH/USDT", "ADA/USDT", "DOT/USDT", "SOL/USDT"]
    except Exception as e:
        print(f"❌ Error loading crypto symbols: {e}")
        print("🔄 Using default symbols")
        return ["BTC/USDT", "ETH/USDT"]

def get_available_timeframes():
    """Get all available timeframes for testing"""
    return ["5m", "15m", "30m", "1h", "2h", "4h", "1d"]

def run_single_backtest(symbols, strategy, interval, bars, capital, position, exchange, output_dir):
    """Run a single backtest for one strategy and timeframe"""
    
    # Get the script path relative to current directory - use subprocess-safe version
    # Use subprocess-safe version
    script_path = "enhanced_crypto_backtest.py"
    if not os.path.exists(script_path):
        script_path = "enhanced_crypto_backtest.py"  # Fallback
    
    # Build command - note: enhanced_crypto_backtest.py uses --strategy (singular)
    cmd = [
        sys.executable, 
        script_path,
        "--symbols"] + symbols + [
        "--strategy", strategy,
        "--interval", interval,
        "--bars", str(bars),
        "--capital", str(capital),
        "--position", str(position),
        "--exchange", exchange,
        "--output", output_dir,
        "--verbose"  # Enable verbose mode for debugging
    ]
    
    print(f"🚀 Testing {strategy} on {interval} timeframe...")
    print(f"📝 Command: {' '.join(cmd)}")
    
    # Run the backtest
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode != 0:
            print(f"❌ Command failed with return code {result.returncode}")
            if result.stderr:
                print(f"Error output: {result.stderr[:500]}...")
            if result.stdout:
                print(f"Output: {result.stdout[:500]}...")
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ Error running backtest: {e}")
        return False, "", str(e)

def parse_backtest_results(output_dir, strategy, timeframe):
    """Parse backtest results from output files"""
    results = []
    
    # Look for summary.csv (subprocess-safe version) or portfolio summary files (original version)
    summary_file = Path(output_dir) / "summary.csv"
    portfolio_files = glob.glob(str(Path(output_dir) / "crypto_portfolio_summary_*.csv"))
    
    if summary_file.exists():
        # Parse subprocess-safe version results
        try:
            df = pd.read_csv(summary_file)
            if not df.empty:
                # Aggregate results from all symbols
                total_trades = df['total_trades'].sum()
                total_return = df['total_return'].sum()
                avg_win_rate = df['win_rate'].mean() if len(df) > 0 else 0
                
                results.append({
                    'Strategy': strategy,
                    'Timeframe': timeframe,
                    'Total Return (%)': round(total_return, 2),
                    'Max Drawdown (%)': 0,  # Not calculated in subprocess-safe version
                    'Sharpe Ratio': 0,     # Not calculated in subprocess-safe version
                    'Win Rate (%)': round(avg_win_rate, 2),
                    'Total Trades': int(total_trades),
                    'Risk-Adjusted Return': round(total_return / max(10, 1), 2)  # Simple approximation
                })
        except Exception as e:
            print(f"Warning: Error parsing summary.csv: {e}")
    
    elif portfolio_files:
        # Parse original version results
        # Get the most recent file
        latest_file = max(portfolio_files, key=os.path.getctime)
        
        try:
            df = pd.read_csv(latest_file)
            if not df.empty:
                # Extract key metrics
                total_return = df['Total Return (%)'].iloc[-1] if 'Total Return (%)' in df.columns else 0
                max_drawdown = df['Max Drawdown (%)'].iloc[-1] if 'Max Drawdown (%)' in df.columns else 0
                sharpe_ratio = df['Sharpe Ratio'].iloc[-1] if 'Sharpe Ratio' in df.columns else 0
                win_rate = df['Win Rate (%)'].iloc[-1] if 'Win Rate (%)' in df.columns else 0
                total_trades = df['Total Trades'].iloc[-1] if 'Total Trades' in df.columns else 0
                
                results.append({
                    'Strategy': strategy,
                    'Timeframe': timeframe,
                    'Total Return (%)': round(total_return, 2),
                    'Max Drawdown (%)': round(max_drawdown, 2),
                    'Sharpe Ratio': round(sharpe_ratio, 3),
                    'Win Rate (%)': round(win_rate, 2),
                    'Total Trades': int(total_trades),
                    'Risk-Adjusted Return': round(total_return / max(abs(max_drawdown), 1), 2)
                })
        except Exception as e:
            print(f"⚠️  Error parsing results for {strategy} on {timeframe}: {e}")
    
    return results

def generate_comparison_report(all_results, output_dir):
    """Generate comprehensive comparison report"""
    if not all_results:
        print("❌ No results to generate report")
        return
    
    df = pd.DataFrame(all_results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create comprehensive report
    report_file = Path(output_dir) / f"strategy_comparison_report_{timestamp}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Comprehensive Strategy Performance Report\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Overall Performance Table
        f.write("## Overall Performance Rankings\n\n")
        df_sorted = df.sort_values('Risk-Adjusted Return', ascending=False)
        f.write(df_sorted.to_markdown(index=False))
        f.write("\n\n")
        
        # Best Strategy per Timeframe
        f.write("## Best Strategy per Timeframe\n\n")
        best_per_timeframe = df.loc[df.groupby('Timeframe')['Risk-Adjusted Return'].idxmax()]
        f.write(best_per_timeframe[['Timeframe', 'Strategy', 'Total Return (%)', 'Risk-Adjusted Return']].to_markdown(index=False))
        f.write("\n\n")
        
        # Best Timeframe per Strategy
        f.write("## Best Timeframe per Strategy\n\n")
        best_per_strategy = df.loc[df.groupby('Strategy')['Risk-Adjusted Return'].idxmax()]
        f.write(best_per_strategy[['Strategy', 'Timeframe', 'Total Return (%)', 'Risk-Adjusted Return']].to_markdown(index=False))
        f.write("\n\n")
        
        # Performance Metrics Summary
        f.write("## Performance Metrics Summary\n\n")
        
        # Top 5 by Total Return
        f.write("### 🚀 Top 5 by Total Return\n")
        top_return = df.nlargest(5, 'Total Return (%)')[['Strategy', 'Timeframe', 'Total Return (%)']]
        f.write(top_return.to_markdown(index=False))
        f.write("\n\n")
        
        # Top 5 by Sharpe Ratio
        f.write("### 📏 Top 5 by Sharpe Ratio\n")
        top_sharpe = df.nlargest(5, 'Sharpe Ratio')[['Strategy', 'Timeframe', 'Sharpe Ratio']]
        f.write(top_sharpe.to_markdown(index=False))
        f.write("\n\n")
        
        # Top 5 by Win Rate
        f.write("### Top 5 by Win Rate\n")
        top_winrate = df.nlargest(5, 'Win Rate (%)')[['Strategy', 'Timeframe', 'Win Rate (%)']]
        f.write(top_winrate.to_markdown(index=False))
        f.write("\n\n")
        
        # Lowest Drawdown
        f.write("### 🛡️ Lowest Drawdown (Best Risk Management)\n")
        low_drawdown = df.nsmallest(5, 'Max Drawdown (%)')[['Strategy', 'Timeframe', 'Max Drawdown (%)']]
        f.write(low_drawdown.to_markdown(index=False))
        f.write("\n\n")
        
        # Recommendations
        f.write("## 💡 Strategy Recommendations\n\n")
        
        overall_best = df_sorted.iloc[0]
        f.write(f"**🥇 Overall Best Strategy**: {overall_best['Strategy']} on {overall_best['Timeframe']} timeframe\n")
        f.write(f"- Total Return: {overall_best['Total Return (%)']}%\n")
        f.write(f"- Risk-Adjusted Return: {overall_best['Risk-Adjusted Return']}\n")
        f.write(f"- Max Drawdown: {overall_best['Max Drawdown (%)']}%\n")
        f.write(f"- Win Rate: {overall_best['Win Rate (%)']}%\n\n")
        
        # Conservative recommendation (lowest drawdown with decent return)
        conservative = df[(df['Total Return (%)'] > 0) & (df['Max Drawdown (%)'] < 10)].nsmallest(1, 'Max Drawdown (%)')
        if not conservative.empty:
            cons = conservative.iloc[0]
            f.write(f"**🛡️ Conservative Choice**: {cons['Strategy']} on {cons['Timeframe']} timeframe\n")
            f.write(f"- Low risk with {cons['Max Drawdown (%)']}% max drawdown\n")
            f.write(f"- Steady return: {cons['Total Return (%)']}%\n\n")
        
        # Aggressive recommendation (highest return)
        aggressive = df.nlargest(1, 'Total Return (%)').iloc[0]
        f.write(f"**🚀 Aggressive Choice**: {aggressive['Strategy']} on {aggressive['Timeframe']} timeframe\n")
        f.write(f"- Highest return potential: {aggressive['Total Return (%)']}%\n")
        f.write(f"- Max drawdown: {aggressive['Max Drawdown (%)']}%\n\n")
    
    # Also create CSV for further analysis
    csv_file = Path(output_dir) / f"strategy_comparison_data_{timestamp}.csv"
    df.to_csv(csv_file, index=False)
    
    print(f"📊 Comprehensive report generated: {report_file}")
    print(f"📈 Data saved to: {csv_file}")
    
    # Print summary to console
    print("\n" + "="*80)
    print("🏆 STRATEGY PERFORMANCE SUMMARY")
    print("="*80)
    print(f"🥇 Best Overall: {overall_best['Strategy']} ({overall_best['Timeframe']}) - {overall_best['Risk-Adjusted Return']} risk-adjusted return")
    print(f"🚀 Highest Return: {aggressive['Strategy']} ({aggressive['Timeframe']}) - {aggressive['Total Return (%)']}%")
    if not conservative.empty:
        cons = conservative.iloc[0]
        print(f"🛡️ Most Conservative: {cons['Strategy']} ({cons['Timeframe']}) - {cons['Max Drawdown (%)']}% max drawdown")
    print("="*80)

def run_comprehensive_backtest(symbols, strategies, timeframes, bars, capital, position, exchange, output_dir):
    """Run comprehensive backtest across all strategies and timeframes"""
    
    all_results = []
    total_tests = len(strategies) * len(timeframes)
    current_test = 0
    
    print(f"🚀 Starting comprehensive backtest analysis...")
    print(f"📊 Testing {len(strategies)} strategies across {len(timeframes)} timeframes")
    print(f"🎯 Total tests to run: {total_tests}")
    print("="*80)
    
    for strategy in strategies:
        strategy_name = strategy['name'] if isinstance(strategy, dict) else strategy
        
        for timeframe in timeframes:
            current_test += 1
            print(f"\n📈 Test {current_test}/{total_tests}: {strategy_name} on {timeframe}")
            print("-" * 50)
            
            # Create sub-directory for this test
            test_output_dir = Path(output_dir) / f"{strategy_name.replace(' ', '_')}_{timeframe}"
            test_output_dir.mkdir(exist_ok=True)
            
            # Run the backtest
            success, stdout, stderr = run_single_backtest(
                symbols=symbols,
                strategy=strategy_name,
                interval=timeframe,
                bars=bars,
                capital=capital,
                position=position,
                exchange=exchange,
                output_dir=str(test_output_dir)
            )
            
            if success:
                print(f"✅ Completed: {strategy_name} on {timeframe}")
                
                # Parse results
                results = parse_backtest_results(test_output_dir, strategy_name, timeframe)
                all_results.extend(results)
            else:
                print(f"❌ Failed: {strategy_name} on {timeframe}")
                if stderr:
                    print(f"Error: {stderr[:200]}...")
    
    print("\n" + "="*80)
    print("🎉 All backtests completed!")
    print("="*80)
    
    # Generate comprehensive comparison report
    if all_results:
        generate_comparison_report(all_results, output_dir)
    else:
        print("❌ No successful results to analyze")
    
    return len(all_results) > 0

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
        description="Advanced Batch Runner for Enhanced Crypto Backtest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🚀 COMPREHENSIVE BACKTEST MODES:

1. AUTO MODE (Recommended):
   python batch_runner.py --auto
   → Tests ALL strategies on ALL timeframes
   → Uses ALL symbols from crypto_assets.csv
   → Generates comprehensive comparison report

2. AUTO MODE with Symbol Limit (Quick Test):
   python batch_runner.py --auto --limit-symbols 3
   → Tests ALL strategies on ALL timeframes
   → Uses only first 3 symbols (faster)

3. CUSTOM STRATEGY MODE:
   python batch_runner.py --symbols BTC/USDT ETH/USDT --strategies "BB_RSI,MACD_Only"
   → Tests specific strategies on all timeframes

4. CUSTOM TIMEFRAME MODE:
   python batch_runner.py --symbols BTC/USDT --timeframes 1h 4h 1d
   → Tests all strategies on specific timeframes

📊 AVAILABLE STRATEGIES:
- RSI_MACD_VWAP (default)
- BB_RSI
- MACD_Only  
- Enhanced_Multi_Factor
- Optimized_Crypto_V2
- SMA_Cross

🎯 RECOMMENDED USAGE:
Quick test: python batch_runner.py --auto --limit-symbols 2 --bars 100
Full test:  python batch_runner.py --auto
        """
    )
    
    parser.add_argument("--auto", action="store_true",
                        help="Auto mode: Test ALL strategies on ALL timeframes (recommended)")
    parser.add_argument("--symbols", "-s", nargs="+", 
                        help="Symbols to test (default: auto-load from crypto_assets.csv)")
    parser.add_argument("--strategies", type=str, 
                        help="Comma-separated list of strategies to test (default: auto-discover all)")
    parser.add_argument("--timeframes", "-t", nargs="+", 
                        help="Timeframes to test (default: all - 5m,15m,30m,1h,2h,4h,1d)")
    parser.add_argument("--interval", "-i", default="1h",
                        choices=["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d"],
                        help="Single time interval (used only in legacy mode)")
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
    parser.add_argument("--legacy", action="store_true",
                        help="Use legacy mode (single strategy, single timeframe)")
    parser.add_argument("--limit-symbols", type=int, 
                        help="Limit number of symbols for testing (useful for quick tests)")
    
    args = parser.parse_args()
    
    # Auto-load symbols if not specified
    if args.symbols:
        symbols = args.symbols
    else:
        symbols = load_crypto_symbols()
        
    # Limit symbols if requested (useful for quick testing)
    if args.limit_symbols and len(symbols) > args.limit_symbols:
        symbols = symbols[:args.limit_symbols]
        print(f"🔥 Limited to first {args.limit_symbols} symbols for quick testing")
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # Create timestamp for this batch run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Determine mode and setup
    if args.auto or (not args.legacy and not args.strategies and not args.timeframes):
        # AUTO MODE - comprehensive testing
        batch_output_dir = output_dir / f"comprehensive_analysis_{timestamp}"
        batch_output_dir.mkdir(exist_ok=True)
        
        # Auto-discover strategies
        discovered_strategies = discover_strategies()
        strategy_names = [s['name'] for s in discovered_strategies]
        
        # Use all timeframes
        timeframes = get_available_timeframes()
        
        print("🤖 AUTO MODE: Comprehensive Strategy Analysis")
        print("=" * 80)
        print(f"📊 Symbols ({len(symbols)}): {', '.join(symbols)}")
        print(f"🧪 Strategies ({len(strategy_names)}): {', '.join(strategy_names)}")
        print(f"⏰ Timeframes ({len(timeframes)}): {', '.join(timeframes)}")
        print(f"📈 Bars: {args.bars}")
        print(f"💰 Capital: ${args.capital:,}")
        print(f"📊 Position: ${args.position:,}")
        print(f"🏢 Exchange: {args.exchange}")
        print(f"📁 Output: {batch_output_dir}")
        print(f"🎯 Total Tests: {len(strategy_names) * len(timeframes)}")
        print("=" * 80)
        
        # Run comprehensive backtest
        success = run_comprehensive_backtest(
            symbols=symbols,
            strategies=strategy_names,
            timeframes=timeframes,
            bars=args.bars,
            capital=args.capital,
            position=args.position,
            exchange=args.exchange,
            output_dir=str(batch_output_dir)
        )
        
    elif args.legacy:
        # LEGACY MODE - single strategy, single timeframe
        batch_output_dir = output_dir / f"single_test_{timestamp}"
        batch_output_dir.mkdir(exist_ok=True)
        
        print("🔄 LEGACY MODE: Single Test")
        print("=" * 50)
        
        success = run_backtest(
            symbols=symbols,
            strategies=args.strategies.split(",") if args.strategies else None,
            interval=args.interval,
            bars=args.bars,
            capital=args.capital,
            position=args.position,
            exchange=args.exchange,
            output_dir=str(batch_output_dir)
        )
        
    else:
        # CUSTOM MODE - user-specified strategies/timeframes
        batch_output_dir = output_dir / f"custom_analysis_{timestamp}"
        batch_output_dir.mkdir(exist_ok=True)
        
        # Handle strategies
        if args.strategies:
            strategy_names = [s.strip() for s in args.strategies.split(",")]
        else:
            discovered_strategies = discover_strategies()
            strategy_names = [s['name'] for s in discovered_strategies]
        
        # Handle timeframes
        if args.timeframes:
            timeframes = args.timeframes
        else:
            timeframes = get_available_timeframes()
        
        print("⚙️ CUSTOM MODE: User-Specified Analysis")
        print("=" * 60)
        print(f"📊 Symbols ({len(symbols)}): {', '.join(symbols)}")
        print(f"🧪 Strategies: {', '.join(strategy_names)}")
        print(f"⏰ Timeframes: {', '.join(timeframes)}")
        print(f"📁 Output: {batch_output_dir}")
        print("=" * 60)
        
        # Run comprehensive backtest
        success = run_comprehensive_backtest(
            symbols=symbols,
            strategies=strategy_names,
            timeframes=timeframes,
            bars=args.bars,
            capital=args.capital,
            position=args.position,
            exchange=args.exchange,
            output_dir=str(batch_output_dir)
        )
    
    if success:
        print(f"\n✅ Analysis completed successfully!")
        print(f"📁 Results saved to: {batch_output_dir}")
        print(f"📊 Check the comprehensive report for detailed insights!")
    else:
        print(f"\n❌ Analysis failed or no results generated!")
        sys.exit(1)

def run_backtest(symbols, strategies, interval, bars, capital, position, exchange, output_dir):
    """Run a single backtest with specified parameters (legacy mode)"""
    
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
    
    print(f"🚀 Running legacy backtest: {' '.join(cmd)}")
    print("=" * 80)
    
    # Run the backtest
    try:
        result = subprocess.run(cmd, capture_output=False, text=True, cwd=os.getcwd())
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running backtest: {e}")
        return False

if __name__ == "__main__":
    main()
