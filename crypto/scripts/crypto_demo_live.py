#!/usr/bin/env python3
"""
Crypto Live Demo - Forward Testing Mode
Real-time crypto trading demo using live data but NO ACTUAL TRADES.
Perfect for testing strategy performance before going live.
"""

import os
import sys
import time
import pandas as pd
from datetime import datetime
import pytz
import concurrent.futures
import threading
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from crypto.data_acquisition import fetch_data
from tabulate import tabulate

try:
    from colorama import Fore, Back, Style, init
    # Initialize colorama for colored output
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    # Fallback if colorama is not available
    class ColorFallback:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ""
        RESET_ALL = ""
    
    Fore = ColorFallback()
    Style = ColorFallback()
    COLORS_AVAILABLE = False


def load_crypto_assets():
    """Load crypto assets from CSV file with limit for demo stability."""
    # Use full asset file for production
    assets_file = "crypto/input/crypto_assets.csv"
    if not os.path.exists(assets_file):
        print(f"❌ Error: {assets_file} not found!")
        return []
    
    df = pd.read_csv(assets_file)
    symbols = df['symbol'].tolist()
    
    # Limit to first 30 symbols for demo stability
    if len(symbols) > 30:
        symbols = symbols[:30]
        print(f"{Fore.YELLOW}⚠️  Limited to first 30 symbols for demo stability{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}✅ Loaded {len(symbols)} crypto symbols from {assets_file}{Style.RESET_ALL}")
    return symbols


def load_strategy():
    """Load the trading strategy."""
    sys.path.append('strategies')
    from strategies.VWAPSigma2Strategy import VWAPSigma2Strategy
    return VWAPSigma2Strategy()


class DemoPortfolio:
    """Simulated portfolio for demo trading with enhanced position tracking."""
    
    def __init__(self, initial_balance=10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions = {}  # symbol: {'side': 'LONG/SHORT', 'entry_price': float, 'quantity': float, 'entry_time': datetime, 'signal_type': str, 'strategy': str}
        self.trades = []
        self.trade_amount = 1000  # Fixed amount per trade
        self.lock = threading.Lock()  # Thread safety for parallel operations
        
    def can_open_position(self, symbol):
        """Check if we can open a new position - prevents duplicate positions."""
        with self.lock:
            return symbol not in self.positions and self.balance >= self.trade_amount
    
    def open_position(self, symbol, signal, price, timestamp, strategy_name="VWAPSigma2Strategy"):
        """Open a demo position with enhanced tracking."""
        with self.lock:
            if not self.can_open_position(symbol):
                return False
            
            side = "LONG" if "BUY" in signal else "SHORT"
            quantity = self.trade_amount / price
            
            self.positions[symbol] = {
                'side': side,
                'entry_price': price,
                'quantity': quantity,
                'entry_time': timestamp,
                'signal_type': signal,
                'strategy': strategy_name
            }
            
            self.balance -= self.trade_amount
            
            # Enhanced position opening display
            print(f"\n{Fore.GREEN}� NEW DEMO POSITION OPENED{Style.RESET_ALL}")
            print(f"{Fore.CYAN}┌─────────────────────────────────────────┐")
            print(f"│ Symbol:      {Fore.YELLOW}{symbol:<10}{Fore.CYAN}              │")
            print(f"│ Side:        {Fore.MAGENTA}{side:<10}{Fore.CYAN}              │")
            print(f"│ Entry Price: {Fore.WHITE}${price:<10.4f}{Fore.CYAN}           │")
            print(f"│ Entry Time:  {Fore.WHITE}{timestamp.strftime('%H:%M:%S'):<10}{Fore.CYAN}          │")
            print(f"│ Signal:      {Fore.GREEN}{signal:<20}{Fore.CYAN}     │")
            print(f"│ Strategy:    {Fore.BLUE}{strategy_name:<20}{Fore.CYAN}     │")
            print(f"│ Quantity:    {Fore.WHITE}{quantity:<10.6f}{Fore.CYAN}          │")
            print(f"└─────────────────────────────────────────┘{Style.RESET_ALL}")
            
            return True
    
    def close_position(self, symbol, price, timestamp, reason="Strategy Exit"):
        """Close a demo position with enhanced tracking."""
        with self.lock:
            if symbol not in self.positions:
                return False
            
            position = self.positions[symbol]
            quantity = position['quantity']
            entry_price = position['entry_price']
            side = position['side']
            
            # Calculate PnL
            if side == "LONG":
                pnl = (price - entry_price) * quantity
            else:  # SHORT
                pnl = (entry_price - price) * quantity
            
            pnl_percent = (pnl / self.trade_amount) * 100
            
            # Update balance
            exit_value = price * quantity
            self.balance += exit_value
            
            # Record trade
            trade = {
                'symbol': symbol,
                'side': side,
                'entry_price': entry_price,
                'exit_price': price,
                'quantity': quantity,
                'pnl': pnl,
                'pnl_percent': pnl_percent,
                'entry_time': position['entry_time'],
                'exit_time': timestamp,
                'reason': reason,
                'signal_type': position['signal_type'],
                'strategy': position['strategy']
            }
            
            self.trades.append(trade)
            del self.positions[symbol]
            
            # Enhanced position closing display
            color = Fore.GREEN if pnl_percent > 0 else Fore.RED
            print(f"\n{color}📉 DEMO POSITION CLOSED{Style.RESET_ALL}")
            print(f"{Fore.CYAN}┌─────────────────────────────────────────┐")
            print(f"│ Symbol:      {Fore.YELLOW}{symbol:<10}{Fore.CYAN}              │")
            print(f"│ Side:        {Fore.MAGENTA}{side:<10}{Fore.CYAN}              │")
            print(f"│ Exit Price:  {Fore.WHITE}${price:<10.4f}{Fore.CYAN}           │")
            print(f"│ PnL:         {color}{pnl_percent:+.2f}%{Fore.CYAN}                │")
            print(f"│ Reason:      {Fore.WHITE}{reason:<20}{Fore.CYAN}     │")
            print(f"└─────────────────────────────────────────┘{Style.RESET_ALL}")
            
            return True
    
    def get_position_pnl(self, symbol, current_price):
        """Calculate unrealized PnL for a position."""
        with self.lock:
            if symbol not in self.positions:
                return 0
            
            position = self.positions[symbol]
            quantity = position['quantity']
            entry_price = position['entry_price']
            side = position['side']
            
            if side == "LONG":
                pnl = (current_price - entry_price) * quantity
            else:  # SHORT
                pnl = (entry_price - current_price) * quantity
            
            return (pnl / self.trade_amount) * 100
    
    def get_portfolio_summary(self):
        """Get portfolio performance summary."""
        with self.lock:
            total_realized_pnl = sum(trade['pnl'] for trade in self.trades)
            total_realized_pnl_percent = (total_realized_pnl / self.initial_balance) * 100
            
            total_trades = len(self.trades)
            winning_trades = len([t for t in self.trades if t['pnl'] > 0])
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            return {
                'initial_balance': self.initial_balance,
                'current_balance': self.balance,
                'open_positions': len(self.positions),
                'total_trades': total_trades,
                'realized_pnl': total_realized_pnl,
                'realized_pnl_percent': total_realized_pnl_percent,
                'win_rate': win_rate,
                'winning_trades': winning_trades,
                'losing_trades': total_trades - winning_trades
            }
    
    def get_detailed_positions(self, current_prices):
        """Get detailed information about all open positions."""
        with self.lock:
            detailed_positions = []
            for symbol, position in self.positions.items():
                current_price = current_prices.get(symbol, position['entry_price'])
                unrealized_pnl = self.get_position_pnl(symbol, current_price)
                
                duration = datetime.now(pytz.timezone('Asia/Kolkata')) - position['entry_time']
                duration_str = str(duration).split('.')[0]
                
                # Color code based on PnL
                pnl_color = "🟢" if unrealized_pnl > 0 else "🔴" if unrealized_pnl < 0 else "⚪"
                
                detailed_positions.append({
                    'Symbol': f"{symbol}",
                    'Side': position['side'],
                    'Entry Price': f"${position['entry_price']:.4f}",
                    'Current Price': f"${current_price:.4f}",
                    'Unrealized PnL': f"{pnl_color} {unrealized_pnl:+.2f}%",
                    'Duration': duration_str,
                    'Signal': position['signal_type'],
                    'Strategy': position['strategy']
                })
            
            return detailed_positions


def setup_logging():
    """Set up logging for live demo session."""
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"crypto/logs/crypto_demo_live_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    return log_filename


def scan_single_symbol(symbol, strategy, current_time):
    """Scan a single symbol for signals with improved error handling."""
    try:
        # Add random delay to prevent rate limiting
        time.sleep(0.1 + (hash(symbol) % 100) / 1000)  # 0.1-0.2 second delay
        
        # Fetch real-time data with timeout
        data = fetch_data(
            symbol=symbol,
            exchange="kraken",
            interval="5m",
            bars=30,
            data_source="ccxt",
            fetch_timeout=8  # Increased timeout slightly
        )
        
        if data is None or data.empty:
            logging.debug(f"No data for {symbol}")
            return None
        
        current_price = data['close'].iloc[-1]
        
        # Generate signal with error handling
        try:
            signal = strategy.generate_signal(data)
        except Exception as e:
            logging.warning(f"Strategy error for {symbol}: {e}")
            signal = None
        
        return {
            'symbol': symbol,
            'price': current_price,
            'signal': signal,
            'data': data
        }
        
    except Exception as e:
        # Log the error but don't print to avoid spam
        logging.debug(f"Scan error {symbol}: {e}")
        return None


def parallel_scan_symbols(symbols, strategy, current_time, max_workers=8):
    """Scan multiple symbols in parallel with improved error handling and timeout management."""
    results = {}
    completed_count = 0
    total_symbols = len(symbols)
    failed_symbols = []
    
    print(f"{Fore.YELLOW}🔄 Starting parallel scan with {max_workers} workers...{Style.RESET_ALL}")
    scan_start = time.time()
    
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all scanning tasks
            future_to_symbol = {
                executor.submit(scan_single_symbol, symbol, strategy, current_time): symbol
                for symbol in symbols
            }
            
            print(f"{Fore.CYAN}📋 Submitted {len(future_to_symbol)} scanning tasks{Style.RESET_ALL}")
            
            # Collect results as they complete with shorter timeout
            try:
                for future in concurrent.futures.as_completed(future_to_symbol, timeout=90):  # 1.5 minute timeout
                    symbol = future_to_symbol[future]
                    completed_count += 1
                    
                    # Show progress more frequently
                    if completed_count % 2 == 0 or completed_count == total_symbols:
                        progress_percent = (completed_count / total_symbols) * 100
                        elapsed = time.time() - scan_start
                        print(f"{Fore.CYAN}📈 Progress: {completed_count}/{total_symbols} ({progress_percent:.0f}%) | {elapsed:.1f}s | Latest: {symbol}{Style.RESET_ALL}")
                    
                    try:
                        result = future.result(timeout=20)  # Reduced timeout per symbol
                        if result:
                            results[symbol] = result
                            print(f"{Fore.GREEN}✅ {symbol}: ${result['price']:.4f} | {result['signal'] or 'HOLD'}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}⚠️  {symbol}: No data/signal{Style.RESET_ALL}")
                            failed_symbols.append(symbol)
                    except concurrent.futures.TimeoutError:
                        print(f"{Fore.RED}⏰ {symbol}: Timeout (20s){Style.RESET_ALL}")
                        failed_symbols.append(symbol)
                    except Exception as e:
                        print(f"{Fore.RED}❌ {symbol}: {str(e)[:50]}{Style.RESET_ALL}")
                        failed_symbols.append(symbol)
                        logging.warning(f"Error in parallel scan for {symbol}: {e}")
                        
            except concurrent.futures.TimeoutError:
                print(f"{Fore.RED}⏰ Overall scan timeout after 90 seconds{Style.RESET_ALL}")
                # Cancel remaining futures
                for future in future_to_symbol:
                    if not future.done():
                        future.cancel()
                        remaining_symbol = future_to_symbol[future]
                        print(f"{Fore.YELLOW}⚠️  Cancelled: {remaining_symbol}{Style.RESET_ALL}")
                        failed_symbols.append(remaining_symbol)
    
    except Exception as e:
        print(f"{Fore.RED}❌ Parallel scan failed: {e}{Style.RESET_ALL}")
        logging.error(f"Parallel scan failed: {e}")
    
    scan_duration = time.time() - scan_start
    success_rate = (len(results) / total_symbols) * 100 if total_symbols > 0 else 0
    
    print(f"{Fore.GREEN}🎯 Parallel scan completed in {scan_duration:.1f}s: {len(results)}/{total_symbols} successful ({success_rate:.1f}%){Style.RESET_ALL}")
    
    if failed_symbols:
        print(f"{Fore.RED}❌ Failed symbols ({len(failed_symbols)}): {', '.join(failed_symbols[:10])}{'...' if len(failed_symbols) > 10 else ''}{Style.RESET_ALL}")
    
    return results
def run_crypto_demo_live():
    """Run live demo trading with real-time data, parallel scanning, and enhanced position tracking."""
    print(f"{Fore.RED}🔴 LIVE Crypto Demo - Forward Testing Mode{Style.RESET_ALL}")
    print("=" * 80)
    print(f"{Fore.YELLOW}⚠️  DEMO MODE: Uses real-time data but NO ACTUAL TRADES are executed{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 Perfect for testing strategy performance before going live!{Style.RESET_ALL}")
    print("=" * 80)
    print(f"{Fore.GREEN}🚀 ENHANCED FEATURES:{Style.RESET_ALL}")
    print(f"  • {Fore.CYAN}⚡ Parallel scanning with real-time progress tracking{Style.RESET_ALL}")
    print(f"  • {Fore.CYAN}📊 Detailed per-symbol status and signal monitoring{Style.RESET_ALL}")
    print(f"  • {Fore.CYAN}⏰ Smart timeouts and error handling{Style.RESET_ALL}")
    print(f"  • {Fore.CYAN}💰 Live portfolio tracking with PnL monitoring{Style.RESET_ALL}")
    print(f"  • {Fore.CYAN}📝 Comprehensive logging and CSV outputs{Style.RESET_ALL}")
    print("=" * 80)
    
    # Set up logging
    log_filename = setup_logging()
    logging.info("Starting crypto demo live trading session")
    print(f"{Fore.GREEN}📝 Session logged to: {log_filename}{Style.RESET_ALL}")
    
    # Load assets
    symbols = load_crypto_assets()
    if not symbols:
        return
    
    print(f"{Fore.CYAN}🔍 Demo trading {len(symbols)} crypto symbols using CCXT (Kraken){Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 Strategy: VWAPSigma2Strategy{Style.RESET_ALL}")
    print(f"{Fore.CYAN}💰 Virtual Portfolio: $10,000 starting balance{Style.RESET_ALL}")
    print(f"{Fore.CYAN}⚡ Parallel scanning enabled for faster performance{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🔄 Continuous demo... Press Ctrl+C to stop{Style.RESET_ALL}")
    print("=" * 80)
    
    # Load strategy and initialize portfolio
    print(f"{Fore.YELLOW}🔄 Loading trading strategy...{Style.RESET_ALL}")
    strategy_start = time.time()
    strategy = load_strategy()
    strategy_duration = time.time() - strategy_start
    print(f"{Fore.GREEN}✅ Strategy loaded in {strategy_duration:.2f}s{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}🔄 Initializing demo portfolio...{Style.RESET_ALL}")
    portfolio = DemoPortfolio(initial_balance=10000)
    print(f"{Fore.GREEN}✅ Portfolio initialized with $10,000 balance{Style.RESET_ALL}")
    
    ist = pytz.timezone('Asia/Kolkata')
    scan_count = 0
    
    print(f"{Fore.MAGENTA}🚀 Starting live demo trading loop...{Style.RESET_ALL}")
    print("=" * 80)
    
    try:
        while True:
            scan_count += 1
            current_time = datetime.now(ist)
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n{Fore.MAGENTA}📅 {current_time_str} IST | 🔍 Demo Scan #{scan_count}{Style.RESET_ALL}")
            print("-" * 80)
            logging.info(f"Starting scan #{scan_count}")
            
            # Parallel scanning for better performance
            print(f"{Fore.YELLOW}⚡ Scanning {len(symbols)} symbols in parallel...{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📋 Symbols to scan: {', '.join(symbols[:10])}{'...' if len(symbols) > 10 else ''}{Style.RESET_ALL}")
            scan_start_time = time.time()
            
            scan_results = parallel_scan_symbols(symbols, strategy, current_time, max_workers=6)
            
            scan_duration = time.time() - scan_start_time
            success_rate = (len(scan_results) / len(symbols)) * 100 if symbols else 0
            
            print(f"{Fore.GREEN}✅ Parallel scan completed in {scan_duration:.1f}s ({len(scan_results)}/{len(symbols)} symbols processed, {success_rate:.1f}% success){Style.RESET_ALL}")
            
            # Circuit breaker: if too many failures, wait longer
            if success_rate < 50:
                print(f"{Fore.RED}⚠️  Low success rate ({success_rate:.1f}%), extending wait time to 60s{Style.RESET_ALL}")
                extended_wait = True
            else:
                extended_wait = False
            
            if not scan_results:
                print(f"{Fore.RED}⚠️  WARNING: No scan results returned! Skipping this scan cycle.{Style.RESET_ALL}")
                logging.warning(f"No scan results in scan #{scan_count}")
                time.sleep(10)
                continue
            
            new_signals = []
            current_prices = {}
            processed_count = 0
            positions_checked = 0
            signals_found = 0
            
            print(f"{Fore.CYAN}🔍 Processing {len(scan_results)} scan results...{Style.RESET_ALL}")
            
            # Process scan results
            for symbol, result in scan_results.items():
                processed_count += 1
                if processed_count % 10 == 0 or processed_count == len(scan_results):
                    print(f"{Fore.YELLOW}📊 Processing: {processed_count}/{len(scan_results)} symbols...{Style.RESET_ALL}", end="\r")
                current_price = result['price']
                signal = result['signal']
                current_prices[symbol] = current_price
                
                # Handle existing positions - check for exits first
                if symbol in portfolio.positions:
                    positions_checked += 1
                    position = portfolio.positions[symbol]
                    unrealized_pnl = portfolio.get_position_pnl(symbol, current_price)
                    
                    print(f"{Fore.BLUE}🔍 Checking position: {symbol} | Current PnL: {unrealized_pnl:+.2f}%{Style.RESET_ALL}")
                    
                    # Enhanced exit logic for demo
                    should_exit = False
                    exit_reason = ""
                    
                    # Exit conditions
                    if unrealized_pnl > 5:  # Take profit at +5%
                        should_exit = True
                        exit_reason = "Take Profit (+5%)"
                    elif unrealized_pnl < -3:  # Stop loss at -3%
                        should_exit = True
                        exit_reason = "Stop Loss (-3%)"
                    elif signal and "EXIT" in signal:  # Strategy exit signal
                        should_exit = True
                        exit_reason = f"Strategy Exit ({signal})"
                    
                    if should_exit:
                        print(f"{Fore.RED}🚨 Exit condition triggered for {symbol}: {exit_reason}{Style.RESET_ALL}")
                        portfolio.close_position(symbol, current_price, current_time, exit_reason)
                        logging.info(f"Position closed: {symbol} @ ${current_price:.4f} | Reason: {exit_reason} | PnL: {unrealized_pnl:+.2f}%")
                
                # Handle new signals - only if no existing position
                elif signal and signal != "HOLD" and portfolio.can_open_position(symbol):
                    signals_found += 1
                    print(f"{Fore.GREEN}📈 Signal detected: {symbol} | {signal} @ ${current_price:.4f}{Style.RESET_ALL}")
                    if portfolio.open_position(symbol, signal, current_price, current_time, "VWAPSigma2Strategy"):
                        new_signals.append({
                            'Time': current_time_str,
                            'Symbol': symbol,
                            'Signal': signal.split('(')[0].strip(),
                            'Price': f"${current_price:.4f}",
                            'Strategy': 'VWAPSigma2Strategy',
                            'Action': f'{Fore.GREEN}DEMO POSITION OPENED{Style.RESET_ALL}'
                        })
                        logging.info(f"New position opened: {symbol} @ ${current_price:.4f} | Signal: {signal}")
                elif signal and signal != "HOLD":
                    print(f"{Fore.YELLOW}⚪ Signal ignored (position exists or insufficient balance): {symbol} | {signal}{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}📊 Scan Analysis Complete:{Style.RESET_ALL}")
            print(f"  • Symbols Processed: {processed_count}")
            print(f"  • Existing Positions Checked: {positions_checked}")
            print(f"  • New Signals Found: {signals_found}")
            print(f"  • New Positions Opened: {len(new_signals)}")
            
            # Display new signals
            if new_signals:
                print(f"\n{Fore.GREEN}🚨 **NEW DEMO POSITIONS** ({len(new_signals)} signals){Style.RESET_ALL}")
                print(tabulate(new_signals, headers='keys', tablefmt='grid'))
            
            # Display detailed open positions
            detailed_positions = portfolio.get_detailed_positions(current_prices)
            if detailed_positions:
                print(f"\n{Fore.BLUE}📈 **OPEN DEMO POSITIONS** ({len(detailed_positions)} positions){Style.RESET_ALL}")
                print(tabulate(detailed_positions, headers='keys', tablefmt='grid'))
            
            # Display portfolio summary with colors
            summary = portfolio.get_portfolio_summary()
            pnl_color = Fore.GREEN if summary['realized_pnl_percent'] > 0 else Fore.RED if summary['realized_pnl_percent'] < 0 else Fore.YELLOW
            
            print(f"\n{Fore.CYAN}💰 **DEMO PORTFOLIO SUMMARY**{Style.RESET_ALL}")
            print(f"Balance: {Fore.WHITE}${summary['current_balance']:.2f}{Style.RESET_ALL} | "
                  f"Realized PnL: {pnl_color}{summary['realized_pnl_percent']:+.2f}%{Style.RESET_ALL} | "
                  f"Trades: {Fore.WHITE}{summary['total_trades']}{Style.RESET_ALL} | "
                  f"Win Rate: {Fore.WHITE}{summary['win_rate']:.1f}%{Style.RESET_ALL} | "
                  f"Open: {Fore.WHITE}{summary['open_positions']}{Style.RESET_ALL}")
            
            if not new_signals and not detailed_positions:
                print(f"\n{Fore.YELLOW}⚪ No new signals or open positions{Style.RESET_ALL}")
            
            # Save demo results
            if portfolio.trades:
                save_demo_results(portfolio.trades, portfolio.positions)
            
            # Dynamic wait time based on success rate with heartbeat
            wait_time = 60 if extended_wait else 30
            print(f"\n{Fore.CYAN}⏱️  Next demo scan in {wait_time} seconds...{Style.RESET_ALL}")
            
            # Show heartbeat during wait
            for i in range(wait_time):
                if i % 10 == 0 and i > 0:
                    remaining = wait_time - i
                    print(f"{Fore.BLUE}💓 Heartbeat: {remaining}s remaining...{Style.RESET_ALL}")
                time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.GREEN}✅ Demo trading stopped after {scan_count} scans.{Style.RESET_ALL}")
        logging.info(f"Demo trading session ended after {scan_count} scans")
        
        # Final summary
        final_summary = portfolio.get_portfolio_summary()
        print(f"\n{Fore.CYAN}📊 **FINAL DEMO RESULTS**{Style.RESET_ALL}")
        print("=" * 60)
        print(f"Initial Balance:     ${final_summary['initial_balance']:,.2f}")
        print(f"Final Balance:       ${final_summary['current_balance']:,.2f}")
        
        pnl_color = Fore.GREEN if final_summary['realized_pnl_percent'] > 0 else Fore.RED
        print(f"Total Realized PnL:  {pnl_color}{final_summary['realized_pnl_percent']:+.2f}%{Style.RESET_ALL}")
        print(f"Total Trades:        {final_summary['total_trades']}")
        print(f"Win Rate:            {final_summary['win_rate']:.1f}%")
        print(f"Open Positions:      {final_summary['open_positions']}")
        
        if portfolio.trades:
            print(f"\n{Fore.CYAN}📈 **RECENT TRADE HISTORY**{Style.RESET_ALL}")
            trade_data = []
            for trade in portfolio.trades[-10:]:  # Show last 10 trades
                pnl_symbol = "🟢" if trade['pnl_percent'] > 0 else "🔴"
                trade_data.append([
                    trade['symbol'],
                    trade['side'],
                    f"${trade['entry_price']:.4f}",
                    f"${trade['exit_price']:.4f}",
                    f"{pnl_symbol} {trade['pnl_percent']:+.2f}%",
                    trade['reason'],
                    trade['strategy']
                ])
            
            print(tabulate(trade_data, headers=['Symbol', 'Side', 'Entry', 'Exit', 'PnL%', 'Reason', 'Strategy'], tablefmt='grid'))
        
        # Close any remaining positions
        if portfolio.positions:
            print(f"\n{Fore.YELLOW}⚠️  Closing {len(portfolio.positions)} remaining positions...{Style.RESET_ALL}")
            current_time = datetime.now(ist)
            for symbol in list(portfolio.positions.keys()):
                if symbol in current_prices:
                    portfolio.close_position(symbol, current_prices[symbol], current_time, "Session End")
                    logging.info(f"Session end - Position closed: {symbol}")


def save_demo_results(trades, positions):
    """Save demo trading results to CSV file with enhanced logging."""
    if not trades and not positions:
        return
    
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save trades
    if trades:
        trades_df = pd.DataFrame(trades)
        trades_filename = f"output/demo_trades_crypto_{timestamp}.csv"
        trades_df.to_csv(trades_filename, index=False)
        logging.info(f"Demo trades saved to {trades_filename}")
    
    # Save current positions
    if positions:
        positions_data = []
        for symbol, pos in positions.items():
            positions_data.append({
                'symbol': symbol,
                'side': pos['side'],
                'entry_price': pos['entry_price'],
                'quantity': pos['quantity'],
                'entry_time': pos['entry_time'],
                'signal_type': pos['signal_type'],
                'strategy': pos['strategy']
            })
        
        positions_df = pd.DataFrame(positions_data)
        positions_filename = f"output/demo_positions_crypto_{timestamp}.csv"
        positions_df.to_csv(positions_filename, index=False)
        logging.info(f"Demo positions saved to {positions_filename}")


if __name__ == "__main__":
    try:
        run_crypto_demo_live()
    except KeyboardInterrupt:
        print("\n⚠️  Demo trading interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
