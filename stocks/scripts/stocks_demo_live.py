#!/usr/bin/env python3
"""
Stocks Live Demo - Forward Testing Mode
Real-time stock trading demo using live Fyers API data but NO ACTUAL TRADES.
Perfect for testing strategy performance before going live.
"""

import os
import sys
import time
import pandas as pd
from datetime import datetime
import pytz

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tabulate import tabulate
from stocks.data_acquisition import fetch_data, get_live_quote, test_fyers_connection


def load_stock_assets():
    """Load stock assets from CSV file."""
    assets_file = "stocks/input/stocks_assets.csv"
    if not os.path.exists(assets_file):
        print(f"❌ Error: {assets_file} not found!")
        return []
    
    df = pd.read_csv(assets_file)
    return df['symbol'].tolist()


def load_strategy():
    """Load the trading strategy."""
    sys.path.append('strategies')
    from strategies.VWAPSigma2Strategy import VWAPSigma2Strategy
    return VWAPSigma2Strategy()


def setup_fyers_connection():
    """Setup Fyers API connection."""
    print("🔌 Setting up Fyers API connection...")
    
    if test_fyers_connection():
        print("✅ Fyers API connected successfully")
        return True
    else:
        print("❌ Fyers API connection failed!")
        print("Please check your access_token.py file and ensure it's up to date")
        return False


class DemoPortfolio:
    """Simulated portfolio for demo trading."""
    
    def __init__(self, initial_balance=100000):  # Higher balance for stocks
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions = {}
        self.trades = []
        self.trade_amount = 10000  # ₹10,000 per trade for stocks
        
    def can_open_position(self, symbol):
        """Check if we can open a new position."""
        return symbol not in self.positions and self.balance >= self.trade_amount
    
    def open_position(self, symbol, signal, price, timestamp):
        """Open a demo position."""
        if not self.can_open_position(symbol):
            return False
        
        side = "LONG" if "BUY" in signal else "SHORT"
        quantity = self.trade_amount / price
        
        self.positions[symbol] = {
            'side': side,
            'entry_price': price,
            'quantity': quantity,
            'entry_time': timestamp,
            'signal_type': signal
        }
        
        self.balance -= self.trade_amount
        
        print(f"📈 DEMO {side} position opened: {symbol} @ ₹{price:.2f}")
        return True
    
    def close_position(self, symbol, price, timestamp, reason="Strategy Exit"):
        """Close a demo position."""
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
            'signal_type': position['signal_type']
        }
        
        self.trades.append(trade)
        del self.positions[symbol]
        
        print(f"📉 DEMO {side} position closed: {symbol} @ ₹{price:.2f} | PnL: {pnl_percent:+.2f}%")
        return True
    
    def get_position_pnl(self, symbol, current_price):
        """Calculate unrealized PnL for a position."""
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


def fetch_data_fyers(symbol, bars=30):
    """Fetch stock data using Fyers API."""
    try:
        # Fetch historical data using Fyers API
        data = fetch_data(symbol, "NSE", "5m", bars, data_source="fyers")
        
        if data is None or data.empty:
            return None
        
        # Ensure we have the required columns
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        if not all(col in data.columns for col in required_columns):
            return None
        
        return data
        
    except Exception as e:
        print(f"❌ Error fetching data for {symbol}: {e}")
        return None
        
        # Convert timestamp to proper format
        if 'timestamp' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Ensure required columns exist
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in required_cols:
            if col not in data.columns:
                return None
        
        return data
        
    except Exception as e:
        return None


def run_stocks_demo_live():
    """Run live demo trading with real-time stock data but NO actual trades."""
    print("🔴 LIVE Stocks Demo - Forward Testing Mode")
    print("=" * 80)
    print("⚠️  DEMO MODE: Uses real-time Fyers API data but NO ACTUAL TRADES")
    print("📊 Perfect for testing strategy performance before going live!")
    print("=" * 80)
    
    # Setup Fyers connection
    if not setup_fyers_connection():
        return
    
    # Load assets
    symbols = load_stock_assets()
    if not symbols:
        return
    
    print(f"🔍 Demo trading {len(symbols)} stock symbols using Fyers API (NSE)")
    print(f"📊 Strategy: VWAPSigma2Strategy")
    print(f"💰 Virtual Portfolio: ₹1,00,000 starting balance")
    print(f"🔄 Continuous demo... Press Ctrl+C to stop")
    print("=" * 80)
    
    # Load strategy and initialize portfolio
    strategy = load_strategy()
    portfolio = DemoPortfolio(initial_balance=100000)
    
    ist = pytz.timezone('Asia/Kolkata')
    scan_count = 0
    
    try:
        while True:
            scan_count += 1
            current_time = datetime.now(ist)
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n📅 {current_time_str} IST | 🔍 Demo Scan #{scan_count}")
            print("-" * 80)
            
            new_signals = []
            position_updates = []
            
            for i, symbol in enumerate(symbols, 1):
                try:
                    # Fetch real-time data
                    data = fetch_data_fyers(symbol, bars=30)
                    
                    if data is None or data.empty:
                        continue
                    
                    current_price = data['close'].iloc[-1]
                    
                    # Check for new signals
                    signal = strategy.generate_signal(data)
                    
                    # Handle existing positions
                    if symbol in portfolio.positions:
                        position = portfolio.positions[symbol]
                        unrealized_pnl = portfolio.get_position_pnl(symbol, current_price)
                        
                        position_updates.append({
                            'Symbol': symbol,
                            'Side': position['side'],
                            'Entry': f"₹{position['entry_price']:.2f}",
                            'Current': f"₹{current_price:.2f}",
                            'PnL%': f"{unrealized_pnl:+.2f}%",
                            'Duration': str(current_time - position['entry_time']).split('.')[0]
                        })
                        
                        # Simple exit logic for demo (you can enhance this)
                        if abs(unrealized_pnl) > 7:  # Exit at ±7% PnL for stocks
                            reason = "Take Profit" if unrealized_pnl > 0 else "Stop Loss"
                            portfolio.close_position(symbol, current_price, current_time, reason)
                    
                    # Handle new signals
                    elif signal and signal != "HOLD" and portfolio.can_open_position(symbol):
                        if portfolio.open_position(symbol, signal, current_price, current_time):
                            new_signals.append({
                                'Time': current_time_str,
                                'Symbol': symbol,
                                'Signal': signal.split('(')[0].strip(),
                                'Price': f"₹{current_price:.2f}",
                                'Action': 'DEMO POSITION OPENED'
                            })
                    
                    # Progress indicator
                    if i % 2 == 0 or i == len(symbols):
                        progress = (i / len(symbols)) * 100
                        print(f"📊 Progress: {i}/{len(symbols)} ({progress:.0f}%)", end="\r")
                
                except Exception as e:
                    continue  # Skip errors in demo mode
            
            # Display new signals
            if new_signals:
                print(f"\n🚨 **NEW DEMO POSITIONS** ({len(new_signals)} signals)")
                print(tabulate(new_signals, headers='keys', tablefmt='grid'))
            
            # Display open positions
            if position_updates:
                print(f"\n📈 **OPEN DEMO POSITIONS** ({len(position_updates)} positions)")
                print(tabulate(position_updates, headers='keys', tablefmt='grid'))
            
            # Display portfolio summary
            summary = portfolio.get_portfolio_summary()
            print(f"\n💰 **DEMO PORTFOLIO SUMMARY**")
            print(f"Balance: ₹{summary['current_balance']:,.2f} | Realized PnL: {summary['realized_pnl_percent']:+.2f}% | Trades: {summary['total_trades']} | Win Rate: {summary['win_rate']:.1f}%")
            
            if not new_signals and not position_updates:
                print(f"\n⚪ No new signals or open positions")
            
            # Save demo results
            if portfolio.trades:
                save_demo_results(portfolio.trades)
            
            print(f"\n⏱️  Next demo scan in 60 seconds...")
            time.sleep(60)  # Wait 60 seconds between scans (stocks are slower)
    
    except KeyboardInterrupt:
        print(f"\n\n✅ Demo trading stopped after {scan_count} scans.")
        
        # Final summary
        final_summary = portfolio.get_portfolio_summary()
        print(f"\n📊 **FINAL DEMO RESULTS**")
        print("=" * 60)
        print(f"Initial Balance:     ₹{final_summary['initial_balance']:,.2f}")
        print(f"Final Balance:       ₹{final_summary['current_balance']:,.2f}")
        print(f"Total Realized PnL:  {final_summary['realized_pnl_percent']:+.2f}%")
        print(f"Total Trades:        {final_summary['total_trades']}")
        print(f"Win Rate:            {final_summary['win_rate']:.1f}%")
        print(f"Open Positions:      {final_summary['open_positions']}")
        
        if portfolio.trades:
            print(f"\n📈 **TRADE HISTORY**")
            trade_data = []
            for trade in portfolio.trades[-10:]:  # Show last 10 trades
                trade_data.append([
                    trade['symbol'],
                    trade['side'],
                    f"₹{trade['entry_price']:.2f}",
                    f"₹{trade['exit_price']:.2f}",
                    f"{trade['pnl_percent']:+.2f}%",
                    trade['reason']
                ])
            
            print(tabulate(trade_data, headers=['Symbol', 'Side', 'Entry', 'Exit', 'PnL%', 'Reason'], tablefmt='grid'))


def save_demo_results(trades):
    """Save demo trading results to CSV file."""
    if not trades:
        return
    
    os.makedirs("output", exist_ok=True)
    
    df = pd.DataFrame(trades)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/demo_trades_stocks_{timestamp}.csv"
    
    df.to_csv(filename, index=False)
    print(f"💾 Demo trades saved to {filename}")


if __name__ == "__main__":
    try:
        run_stocks_demo_live()
    except KeyboardInterrupt:
        print("\n⚠️  Demo trading interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
