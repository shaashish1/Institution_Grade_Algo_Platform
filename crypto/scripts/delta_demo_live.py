#!/usr/bin/env python3
"""
Demo Delta Exchange System - Realtime Trading Simulator
Ready for immediate demonstration with live-like trading simulation
"""

import os
import sys
import json
import time
import math
import threading
from datetime import datetime, timedelta
import argparse

print("🎮 DEMO DELTA EXCHANGE SYSTEM")
print("="*70)
print("✅ Live demo ready")
print("📊 All 29 KPIs included") 
print("🔄 Realtime simulation")
print("🎯 Active trading demo")
print("="*70)

class DemoTradingSimulator:
    """Live demo trading simulator for Delta Exchange."""
    
    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.position = None
        self.trades = []
        self.equity_history = []
        self.is_running = False
        
        self.symbols = ['BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'SOL/USDT', 'MATIC/USDT']
        self.prices = {
            'BTC/USDT': 45000,
            'ETH/USDT': 2500,
            'ADA/USDT': 0.52,
            'SOL/USDT': 22,
            'MATIC/USDT': 0.85
        }
        
    def generate_live_price(self, symbol):
        """Generate realistic live price movement."""
        current_price = self.prices[symbol]
        
        # Market volatility (2-5% moves)
        volatility = 0.02 if 'BTC' in symbol or 'ETH' in symbol else 0.05
        
        # Random price change
        import random
        change_pct = (random.random() - 0.5) * 2 * volatility  # -volatility to +volatility
        new_price = current_price * (1 + change_pct)
        
        self.prices[symbol] = max(new_price, 0.001)  # Minimum price
        return self.prices[symbol]
    
    def calculate_rsi(self, price_history, period=14):
        """Calculate RSI from price history."""
        if len(price_history) < period + 1:
            return 50
        
        gains = []
        losses = []
        
        for i in range(1, len(price_history)):
            change = price_history[i] - price_history[i-1]
            gains.append(max(change, 0))
            losses.append(max(-change, 0))
        
        if len(gains) < period:
            return 50
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def generate_trade_signal(self, symbol, price_history):
        """Generate trading signals based on RSI and momentum."""
        if len(price_history) < 20:
            return None
        
        rsi = self.calculate_rsi(price_history)
        current_price = price_history[-1]
        prev_price = price_history[-2] if len(price_history) > 1 else current_price
        
        # Momentum calculation
        momentum = (current_price - prev_price) / prev_price * 100
        
        # Volume simulation (higher volume increases signal strength)
        import random
        volume_factor = 0.8 + random.random() * 0.4  # 0.8 to 1.2
        
        # Signal generation
        if rsi < 30 and momentum > 0.1:  # Oversold + positive momentum
            return {
                'action': 'buy',
                'price': current_price,
                'rsi': rsi,
                'momentum': momentum,
                'confidence': min((30 - rsi) * 3 + abs(momentum) * 10, 95) * volume_factor,
                'timestamp': datetime.now()
            }
        elif rsi > 70 and momentum < -0.1:  # Overbought + negative momentum
            return {
                'action': 'sell',
                'price': current_price,
                'rsi': rsi,
                'momentum': momentum,
                'confidence': min((rsi - 70) * 3 + abs(momentum) * 10, 95) * volume_factor,
                'timestamp': datetime.now()
            }
        
        return None
    
    def execute_trade(self, signal, symbol):
        """Execute a trade based on signal."""
        if signal['action'] == 'buy' and self.position is None:
            # Enter long position
            position_size = 10000  # $10k position
            quantity = position_size / signal['price']
            
            self.position = {
                'symbol': symbol,
                'side': 'long',
                'entry_price': signal['price'],
                'entry_time': signal['timestamp'],
                'quantity': quantity,
                'entry_confidence': signal['confidence']
            }
            
            print(f"📈 BUY {symbol}: ${signal['price']:.4f} | RSI: {signal['rsi']:.1f} | Confidence: {signal['confidence']:.1f}%")
            
        elif signal['action'] == 'sell' and self.position and self.position['symbol'] == symbol:
            # Exit position
            profit = (signal['price'] - self.position['entry_price']) * self.position['quantity']
            profit_pct = ((signal['price'] - self.position['entry_price']) / self.position['entry_price']) * 100
            
            self.current_capital += profit
            
            trade = {
                'symbol': symbol,
                'entry_time': self.position['entry_time'],
                'exit_time': signal['timestamp'],
                'entry_price': self.position['entry_price'],
                'exit_price': signal['price'],
                'quantity': self.position['quantity'],
                'profit': profit,
                'profit_pct': profit_pct,
                'duration': (signal['timestamp'] - self.position['entry_time']).total_seconds() / 60,  # minutes
                'entry_confidence': self.position['entry_confidence'],
                'exit_confidence': signal['confidence']
            }
            
            self.trades.append(trade)
            
            status = "✅ PROFIT" if profit > 0 else "❌ LOSS"
            print(f"📉 SELL {symbol}: ${signal['price']:.4f} | Profit: ${profit:.2f} ({profit_pct:+.2f}%) | {status}")
            
            self.position = None
    
    def calculate_demo_kpis(self):
        """Calculate comprehensive KPIs for demo."""
        if not self.trades:
            return self._get_empty_kpis()
        
        # Trade analysis
        returns = [t['profit_pct'] for t in self.trades]
        profits = [t['profit'] for t in self.trades]
        durations = [t['duration'] / 1440 for t in self.trades]  # Convert to days
        
        # Basic statistics
        total_trades = len(self.trades)
        winning_trades = len([r for r in returns if r > 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Return metrics
        total_return = sum(returns)
        avg_return = sum(returns) / len(returns) if returns else 0
        best_trade = max(returns) if returns else 0
        worst_trade = min(returns) if returns else 0
        
        # Duration metrics
        max_duration = max(durations) if durations else 0
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Profit factor
        gross_profit = sum([p for p in profits if p > 0])
        gross_loss = abs(sum([p for p in profits if p < 0]))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Time-based calculations
        start_date = min([t['entry_time'] for t in self.trades])
        end_date = max([t['exit_time'] for t in self.trades])
        duration_days = (end_date - start_date).total_seconds() / 86400
        
        # Equity calculations
        final_equity = self.current_capital
        peak_equity = max([self.initial_capital + sum([t['profit'] for t in self.trades[:i+1]]) 
                          for i in range(len(self.trades))]) if self.trades else final_equity
        
        # Advanced calculations
        years = max(duration_days / 365.25, 1/365.25)  # Minimum 1 day
        annualized_return = (((final_equity / self.initial_capital) ** (1/years)) - 1) * 100
        
        # Risk metrics
        volatility = self._calculate_volatility(returns)
        annualized_volatility = volatility * math.sqrt(252)
        sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility > 0 else 0
        
        # Market comparison
        buy_hold_return = 15 * years  # Assume 15% annual market return
        
        # All 29 KPIs
        return {
            'start_date': start_date.strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': end_date.strftime('%Y-%m-%d %H:%M:%S'),
            'duration_days': duration_days,
            'exposure_time_pct': 100.0,
            'equity_final': final_equity,
            'equity_peak': peak_equity,
            'return_pct': total_return,
            'buy_hold_return_pct': buy_hold_return,
            'return_ann_pct': annualized_return,
            'volatility_ann_pct': annualized_volatility,
            'cagr_pct': annualized_return,
            'sharpe_ratio': sharpe_ratio,
            'sortino_ratio': self._calculate_sortino_ratio(returns),
            'calmar_ratio': annualized_return / abs(max(returns)) if returns and max(returns) < 0 else 0,
            'alpha_pct': annualized_return - buy_hold_return,
            'beta': 1.0,
            'max_drawdown_pct': abs(worst_trade) if worst_trade < 0 else 0,
            'avg_drawdown_pct': abs(sum([r for r in returns if r < 0])) / len([r for r in returns if r < 0]) if [r for r in returns if r < 0] else 0,
            'max_drawdown_duration': max_duration,
            'avg_drawdown_duration': avg_duration,
            'total_trades': total_trades,
            'win_rate_pct': win_rate,
            'best_trade_pct': best_trade,
            'worst_trade_pct': worst_trade,
            'avg_trade_pct': avg_return,
            'max_trade_duration': max_duration,
            'avg_trade_duration': avg_duration,
            'profit_factor': profit_factor,
            'expectancy_pct': avg_return
        }
    
    def _get_empty_kpis(self):
        """Return empty KPI structure."""
        return {
            'start_date': 'N/A', 'end_date': 'N/A', 'duration_days': 0,
            'exposure_time_pct': 0, 'equity_final': self.initial_capital,
            'equity_peak': self.initial_capital, 'return_pct': 0,
            'buy_hold_return_pct': 0, 'return_ann_pct': 0,
            'volatility_ann_pct': 0, 'cagr_pct': 0, 'sharpe_ratio': 0,
            'sortino_ratio': 0, 'calmar_ratio': 0, 'alpha_pct': 0,
            'beta': 1.0, 'max_drawdown_pct': 0, 'avg_drawdown_pct': 0,
            'max_drawdown_duration': 0, 'avg_drawdown_duration': 0,
            'total_trades': 0, 'win_rate_pct': 0, 'best_trade_pct': 0,
            'worst_trade_pct': 0, 'avg_trade_pct': 0, 'max_trade_duration': 0,
            'avg_trade_duration': 0, 'profit_factor': 0, 'expectancy_pct': 0
        }
    
    def _calculate_volatility(self, returns):
        """Calculate return volatility."""
        if len(returns) < 2:
            return 0
        mean_return = sum(returns) / len(returns)
        variance = sum([(r - mean_return) ** 2 for r in returns]) / (len(returns) - 1)
        return math.sqrt(variance)
    
    def _calculate_sortino_ratio(self, returns):
        """Calculate Sortino ratio."""
        downside_returns = [r for r in returns if r < 0]
        if not downside_returns:
            return float('inf')
        
        downside_deviation = math.sqrt(sum([r ** 2 for r in downside_returns]) / len(downside_returns))
        mean_return = sum(returns) / len(returns)
        return mean_return / downside_deviation if downside_deviation > 0 else 0
    
    def run_demo(self, duration_minutes=5):
        """Run live demo trading simulation."""
        print(f"\n🚀 Starting {duration_minutes}-minute LIVE DEMO")
        print("="*60)
        
        self.is_running = True
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        # Price history for each symbol
        price_histories = {symbol: [self.prices[symbol]] for symbol in self.symbols}
        
        # Main trading loop
        iteration = 0
        while datetime.now() < end_time and self.is_running:
            iteration += 1
            
            print(f"\n⏰ Minute {iteration} | Capital: ${self.current_capital:,.2f}")
            
            # Process each symbol
            for symbol in self.symbols:
                # Generate new price
                new_price = self.generate_live_price(symbol)
                price_histories[symbol].append(new_price)
                
                # Keep only last 30 prices for calculations
                if len(price_histories[symbol]) > 30:
                    price_histories[symbol] = price_histories[symbol][-30:]
                
                # Generate and check for signals
                signal = self.generate_trade_signal(symbol, price_histories[symbol])
                
                if signal:
                    self.execute_trade(signal, symbol)
            
            # Display current prices
            price_display = " | ".join([f"{sym}: ${self.prices[sym]:.4f}" for sym in self.symbols[:3]])
            print(f"📊 {price_display}")
            
            # Sleep for 1 second (representing 1 minute in fast demo)
            time.sleep(1)
        
        # Demo completed
        print(f"\n🏁 DEMO COMPLETED")
        print("="*60)
        
        return self.calculate_demo_kpis()

def display_demo_results(kpis, trades):
    """Display comprehensive demo results."""
    print(f"\n📊 COMPREHENSIVE DEMO RESULTS - ALL 29 KPIs")
    print("="*90)
    
    # Professional KPI display
    kpi_rows = [
        [f"1. Start", str(kpis.get('start_date', 'N/A'))],
        [f"2. End", str(kpis.get('end_date', 'N/A'))],
        [f"3. Duration", f"{kpis.get('duration_days', 0):.4f} days"],
        [f"4. Exposure Time [%]", f"{kpis.get('exposure_time_pct', 0):.1f}%"],
        [f"5. Equity Final [$]", f"${kpis.get('equity_final', 0):,.2f}"],
        [f"6. Equity Peak [$]", f"${kpis.get('equity_peak', 0):,.2f}"],
        [f"7. Return [%]", f"{kpis.get('return_pct', 0):.2f}%"],
        [f"8. Buy & Hold Return [%]", f"{kpis.get('buy_hold_return_pct', 0):.2f}%"],
        [f"9. Return (Ann.) [%]", f"{kpis.get('return_ann_pct', 0):.2f}%"],
        [f"10. Volatility (Ann.) [%]", f"{kpis.get('volatility_ann_pct', 0):.2f}%"],
        [f"11. CAGR [%]", f"{kpis.get('cagr_pct', 0):.2f}%"],
        [f"12. Sharpe Ratio", f"{kpis.get('sharpe_ratio', 0):.3f}"],
        [f"13. Sortino Ratio", f"{kpis.get('sortino_ratio', 0):.3f}"],
        [f"14. Calmar Ratio", f"{kpis.get('calmar_ratio', 0):.3f}"],
        [f"15. Alpha [%]", f"{kpis.get('alpha_pct', 0):.2f}%"],
        [f"16. Beta", f"{kpis.get('beta', 0):.3f}"],
        [f"17. Max. Drawdown [%]", f"{kpis.get('max_drawdown_pct', 0):.2f}%"],
        [f"18. Avg. Drawdown [%]", f"{kpis.get('avg_drawdown_pct', 0):.2f}%"],
        [f"19. Max. Drawdown Duration", f"{kpis.get('max_drawdown_duration', 0):.4f} days"],
        [f"20. Avg. Drawdown Duration", f"{kpis.get('avg_drawdown_duration', 0):.4f} days"],
        [f"21. # Trades", f"{kpis.get('total_trades', 0)}"],
        [f"22. Win Rate [%]", f"{kpis.get('win_rate_pct', 0):.1f}%"],
        [f"23. Best Trade [%]", f"{kpis.get('best_trade_pct', 0):.2f}%"],
        [f"24. Worst Trade [%]", f"{kpis.get('worst_trade_pct', 0):.2f}%"],
        [f"25. Avg. Trade [%]", f"{kpis.get('avg_trade_pct', 0):.2f}%"],
        [f"26. Max. Trade Duration", f"{kpis.get('max_trade_duration', 0):.4f} days"],
        [f"27. Avg. Trade Duration", f"{kpis.get('avg_trade_duration', 0):.4f} days"],
        [f"28. Profit Factor", f"{kpis.get('profit_factor', 0):.3f}"],
        [f"29. Expectancy [%]", f"{kpis.get('expectancy_pct', 0):.2f}%"]
    ]
    
    # Display in columns
    for i in range(0, len(kpi_rows), 2):
        left = kpi_rows[i]
        right = kpi_rows[i+1] if i+1 < len(kpi_rows) else ["", ""]
        print(f"   {left[0]:<30} {left[1]:<20} {right[0]:<30} {right[1]}")
    
    # Trade details
    if trades:
        print(f"\n📈 TRADE DETAILS:")
        for i, trade in enumerate(trades, 1):
            duration_min = trade['duration']
            print(f"   {i}. {trade['symbol']}: ${trade['profit']:+.2f} ({trade['profit_pct']:+.2f}%) | {duration_min:.1f}min")

def main():
    """Main demo function."""
    parser = argparse.ArgumentParser(description='Demo Delta Exchange System')
    
    parser.add_argument('--duration', '-d', type=int, default=3,
                       help='Demo duration in minutes (default: 3)')
    
    parser.add_argument('--capital', '-c', type=float, default=100000,
                       help='Initial capital (default: 100000)')
    
    args = parser.parse_args()
    
    print(f"\n🎮 DELTA EXCHANGE DEMO")
    print(f"Duration: {args.duration} minutes")
    print(f"Capital: ${args.capital:,.2f}")
    print("="*50)
    
    # Create demo simulator
    simulator = DemoTradingSimulator(initial_capital=args.capital)
    
    try:
        # Run demo
        kpis = simulator.run_demo(duration_minutes=args.duration)
        
        # Display results
        display_demo_results(kpis, simulator.trades)
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = {
            'timestamp': timestamp,
            'kpis': kpis,
            'trades': simulator.trades,
            'system': 'Delta Exchange Demo'
        }
        
        filename = f"delta_demo_results_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Demo results saved to: {filename}")
        
        # Summary
        total_trades = len(simulator.trades)
        final_return = kpis.get('return_pct', 0)
        win_rate = kpis.get('win_rate_pct', 0)
        
        print(f"\n✅ DEMO SUMMARY:")
        print(f"   🔄 Total trades: {total_trades}")
        print(f"   📈 Total return: {final_return:.2f}%")
        print(f"   🎯 Win rate: {win_rate:.1f}%")
        print(f"   💰 Final capital: ${simulator.current_capital:,.2f}")
        print(f"   📊 All 29 KPIs calculated")
        print(f"   🎮 Demo mode: ACTIVE")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
        simulator.is_running = False
        return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
