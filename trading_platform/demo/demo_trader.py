"""
Demo Trader
==========

Paper trading functionality for risk-free strategy testing.
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import uuid

class DemoTrader:
    """Demo/Paper trading functionality"""
    
    def __init__(self):
        self.demo_data_dir = Path("data/demo_trading")
        self.demo_data_dir.mkdir(parents=True, exist_ok=True)
        
        self.account_file = self.demo_data_dir / "demo_account.json"
        self.trades_file = self.demo_data_dir / "demo_trades.json"
        
        self.account = self.load_demo_account()
        self.trades = self.load_demo_trades()
    
    def load_demo_account(self) -> Dict[str, Any]:
        """Load demo account data"""
        try:
            if self.account_file.exists():
                with open(self.account_file, 'r') as f:
                    return json.load(f)
            else:
                return self.create_default_account()
        except Exception as e:
            print(f"❌ Error loading demo account: {e}")
            return self.create_default_account()
    
    def create_default_account(self) -> Dict[str, Any]:
        """Create default demo account"""
        account = {
            "account_id": str(uuid.uuid4())[:8],
            "initial_balance": 100000.0,
            "current_balance": 100000.0,
            "currency": "USD",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "positions": {},
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "total_pnl": 0.0
        }
        
        self.save_demo_account(account)
        return account
    
    def save_demo_account(self, account: Dict[str, Any]):
        """Save demo account data"""
        try:
            account["last_updated"] = datetime.now().isoformat()
            with open(self.account_file, 'w') as f:
                json.dump(account, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving demo account: {e}")
    
    def load_demo_trades(self) -> List[Dict[str, Any]]:
        """Load demo trades history"""
        try:
            if self.trades_file.exists():
                with open(self.trades_file, 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"❌ Error loading demo trades: {e}")
            return []
    
    def save_demo_trades(self, trades: List[Dict[str, Any]]):
        """Save demo trades history"""
        try:
            with open(self.trades_file, 'w') as f:
                json.dump(trades, f, indent=2, default=str)
        except Exception as e:
            print(f"❌ Error saving demo trades: {e}")
    
    def show_balance(self):
        """Show demo account balance"""
        print(f"\n💰 Demo Account Balance")
        print("=" * 25)
        print(f"Account ID: {self.account['account_id']}")
        print(f"Current Balance: ${self.account['current_balance']:,.2f}")
        print(f"Initial Balance: ${self.account['initial_balance']:,.2f}")
        
        pnl = self.account['current_balance'] - self.account['initial_balance']
        pnl_percent = (pnl / self.account['initial_balance']) * 100
        
        pnl_symbol = "📈" if pnl >= 0 else "📉"
        print(f"Total P&L: {pnl_symbol} ${pnl:,.2f} ({pnl_percent:+.2f}%)")
        
        print(f"\nTrade Statistics:")
        print(f"Total Trades: {self.account['total_trades']}")
        print(f"Winning Trades: {self.account['winning_trades']}")
        print(f"Losing Trades: {self.account['losing_trades']}")
        
        if self.account['total_trades'] > 0:
            win_rate = (self.account['winning_trades'] / self.account['total_trades']) * 100
            print(f"Win Rate: {win_rate:.1f}%")
    
    def show_portfolio(self):
        """Show current demo portfolio"""
        print(f"\n📋 Demo Portfolio")
        print("=" * 20)
        
        positions = self.account.get('positions', {})
        
        if not positions:
            print("No open positions.")
            return
        
        total_value = 0
        print(f"{'Symbol':<15} {'Quantity':<12} {'Avg Price':<12} {'Current':<12} {'P&L':<12}")
        print("-" * 70)
        
        for symbol, position in positions.items():
            quantity = position['quantity']
            avg_price = position['avg_price']
            current_price = self.get_current_price(symbol)
            
            if current_price:
                position_value = quantity * current_price
                pnl = (current_price - avg_price) * quantity
                pnl_symbol = "📈" if pnl >= 0 else "📉"
                
                print(f"{symbol:<15} {quantity:<12.4f} ${avg_price:<11.2f} ${current_price:<11.2f} {pnl_symbol}${pnl:<10.2f}")
                total_value += position_value
        
        print("-" * 70)
        print(f"Total Portfolio Value: ${total_value:,.2f}")
        print(f"Available Cash: ${self.account['current_balance']:,.2f}")
        print(f"Total Account Value: ${total_value + self.account['current_balance']:,.2f}")
    
    def place_order_wizard(self):
        """Interactive order placement wizard"""
        print(f"\n🛒 Demo Order Placement")
        print("=" * 25)
        
        try:
            # Get order details
            symbol = input("Enter symbol (e.g., BTC/USDT, NSE:SBIN-EQ): ").strip().upper()
            if not symbol:
                print("❌ Symbol is required")
                return
            
            print("\nOrder Types:")
            print("1. Market Order")
            print("2. Limit Order")
            
            order_type_choice = input("Select order type (1-2) [1]: ").strip() or "1"
            order_type = "market" if order_type_choice == "1" else "limit"
            
            print("\nOrder Side:")
            print("1. Buy")
            print("2. Sell")
            
            side_choice = input("Select side (1-2) [1]: ").strip() or "1"
            side = "buy" if side_choice == "1" else "sell"
            
            # Get quantity
            if side == "buy":
                quantity_input = input("Enter quantity or USD amount (e.g., 0.1 or $1000): ").strip()
            else:
                quantity_input = input("Enter quantity to sell: ").strip()
            
            # Parse quantity
            if quantity_input.startswith('$'):
                # USD amount specified
                usd_amount = float(quantity_input[1:])
                current_price = self.get_current_price(symbol)
                if not current_price:
                    print("❌ Could not get current price")
                    return
                quantity = usd_amount / current_price
            else:
                quantity = float(quantity_input)
            
            # Get price for limit orders
            price = None
            if order_type == "limit":
                price_input = input("Enter limit price: ").strip()
                price = float(price_input)
            
            # Place the order
            result = self.place_demo_order(symbol, side, quantity, price, order_type)
            
            if result:
                print(f"\n✅ Demo order placed successfully!")
                print(f"Order ID: {result['order_id']}")
                print(f"Symbol: {result['symbol']}")
                print(f"Side: {result['side'].upper()}")
                print(f"Quantity: {result['quantity']}")
                print(f"Type: {result['type'].upper()}")
                if result.get('price'):
                    print(f"Price: ${result['price']}")
                print(f"Status: {result['status']}")
            
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        except Exception as e:
            print(f"❌ Error placing order: {e}")
    
    def place_demo_order(self, symbol: str, side: str, quantity: float, 
                         price: Optional[float] = None, order_type: str = "market") -> Optional[Dict]:
        """Place a demo order"""
        try:
            # Get current price
            current_price = self.get_current_price(symbol)
            if not current_price:
                print(f"❌ Could not get price for {symbol}")
                return None
            
            # Use current price for market orders
            execution_price = price if order_type == "limit" and price else current_price
            
            # Calculate order value
            order_value = quantity * execution_price
            
            # Check if we have enough balance/position
            if side == "buy":
                if order_value > self.account['current_balance']:
                    print(f"❌ Insufficient balance. Required: ${order_value:.2f}, Available: ${self.account['current_balance']:.2f}")
                    return None
            else:  # sell
                positions = self.account.get('positions', {})
                if symbol not in positions or positions[symbol]['quantity'] < quantity:
                    available = positions.get(symbol, {}).get('quantity', 0)
                    print(f"❌ Insufficient position. Required: {quantity}, Available: {available}")
                    return None
            
            # Create order
            order = {
                'order_id': str(uuid.uuid4())[:8],
                'symbol': symbol,
                'side': side,
                'quantity': quantity,
                'price': execution_price,
                'type': order_type,
                'status': 'filled',
                'timestamp': datetime.now().isoformat(),
                'order_value': order_value
            }
            
            # Execute the order
            self.execute_demo_order(order)
            
            # Save trade
            self.trades.append(order)
            self.save_demo_trades(self.trades)
            
            return order
            
        except Exception as e:
            print(f"❌ Error placing demo order: {e}")
            return None
    
    def execute_demo_order(self, order: Dict[str, Any]):
        """Execute a demo order"""
        try:
            symbol = order['symbol']
            side = order['side']
            quantity = order['quantity']
            price = order['price']
            order_value = order['order_value']
            
            positions = self.account.get('positions', {})
            
            if side == "buy":
                # Deduct cash
                self.account['current_balance'] -= order_value
                
                # Add to position
                if symbol in positions:
                    # Update existing position
                    old_quantity = positions[symbol]['quantity']
                    old_avg_price = positions[symbol]['avg_price']
                    
                    new_quantity = old_quantity + quantity
                    new_avg_price = ((old_quantity * old_avg_price) + (quantity * price)) / new_quantity
                    
                    positions[symbol] = {
                        'quantity': new_quantity,
                        'avg_price': new_avg_price,
                        'last_updated': datetime.now().isoformat()
                    }
                else:
                    # New position
                    positions[symbol] = {
                        'quantity': quantity,
                        'avg_price': price,
                        'last_updated': datetime.now().isoformat()
                    }
            
            else:  # sell
                # Add cash
                self.account['current_balance'] += order_value
                
                # Reduce position
                if symbol in positions:
                    positions[symbol]['quantity'] -= quantity
                    
                    # Remove position if quantity is zero
                    if positions[symbol]['quantity'] <= 0:
                        del positions[symbol]
            
            # Update account
            self.account['positions'] = positions
            self.account['total_trades'] += 1
            
            # Calculate P&L for trade statistics
            if side == "sell" and symbol in positions:
                trade_pnl = (price - positions[symbol]['avg_price']) * quantity
                if trade_pnl > 0:
                    self.account['winning_trades'] += 1
                else:
                    self.account['losing_trades'] += 1
                self.account['total_pnl'] += trade_pnl
            
            self.save_demo_account(self.account)
            
        except Exception as e:
            print(f"❌ Error executing demo order: {e}")
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol"""
        try:
            # Try to get real price from crypto trader
            if '/' in symbol and not symbol.startswith('NSE:'):
                from ..crypto.crypto_trader import CryptoTrader
                trader = CryptoTrader()
                market_data = trader.get_market_data(symbol)
                if market_data:
                    return market_data['price']
            
            # For stocks or if crypto fails, use synthetic price
            return self.get_synthetic_price(symbol)
            
        except Exception as e:
            print(f"⚠️  Using synthetic price for {symbol}: {e}")
            return self.get_synthetic_price(symbol)
    
    def get_synthetic_price(self, symbol: str) -> float:
        """Generate synthetic price for demo trading"""
        # Base prices for common symbols
        base_prices = {
            'BTC/USDT': 45000,
            'ETH/USDT': 3000,
            'BNB/USDT': 300,
            'ADA/USDT': 0.5,
            'SOL/USDT': 100,
            'NSE:SBIN-EQ': 500,
            'NSE:RELIANCE-EQ': 2500,
            'NSE:TCS-EQ': 3500
        }
        
        base_price = base_prices.get(symbol, 100)
        
        # Add some random variation (±2%)
        import random
        variation = random.uniform(-0.02, 0.02)
        return base_price * (1 + variation)
    
    def show_trading_history(self):
        """Show demo trading history"""
        print(f"\n📊 Demo Trading History")
        print("=" * 25)
        
        if not self.trades:
            print("No trades found.")
            return
        
        print(f"Total trades: {len(self.trades)}")
        print(f"\nRecent trades:")
        print(f"{'Date':<12} {'Symbol':<15} {'Side':<6} {'Quantity':<12} {'Price':<12} {'Value':<12}")
        print("-" * 80)
        
        for trade in self.trades[-10:]:  # Show last 10 trades
            date = trade['timestamp'][:10]
            symbol = trade['symbol']
            side = trade['side'].upper()
            quantity = trade['quantity']
            price = trade['price']
            value = trade['order_value']
            
            print(f"{date:<12} {symbol:<15} {side:<6} {quantity:<12.4f} ${price:<11.2f} ${value:<11.2f}")
    
    def reset_account(self):
        """Reset demo account to initial state"""
        try:
            print("🔄 Resetting demo account...")
            
            # Reset account
            self.account = self.create_default_account()
            
            # Clear trades
            self.trades = []
            self.save_demo_trades(self.trades)
            
            print("✅ Demo account reset successfully!")
            print(f"New balance: ${self.account['current_balance']:,.2f}")
            
        except Exception as e:
            print(f"❌ Error resetting account: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        try:
            initial_balance = self.account['initial_balance']
            current_balance = self.account['current_balance']
            
            # Calculate portfolio value
            portfolio_value = 0
            positions = self.account.get('positions', {})
            
            for symbol, position in positions.items():
                current_price = self.get_current_price(symbol)
                if current_price:
                    portfolio_value += position['quantity'] * current_price
            
            total_value = current_balance + portfolio_value
            total_return = (total_value - initial_balance) / initial_balance
            
            return {
                'initial_balance': initial_balance,
                'current_cash': current_balance,
                'portfolio_value': portfolio_value,
                'total_value': total_value,
                'total_return': total_return,
                'total_trades': self.account['total_trades'],
                'winning_trades': self.account['winning_trades'],
                'losing_trades': self.account['losing_trades'],
                'win_rate': (self.account['winning_trades'] / max(self.account['total_trades'], 1)) * 100
            }
            
        except Exception as e:
            print(f"❌ Error calculating performance: {e}")
            return {}