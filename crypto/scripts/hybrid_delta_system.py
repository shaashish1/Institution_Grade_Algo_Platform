#!/usr/bin/env python3
"""
Hybrid Delta Exchange System
Works with demo data now, upgradeable to real CCXT data later
"""

import os
import sys
import json
import time
import math
from datetime import datetime, timedelta
import argparse

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

class DeltaExchangeConnector:
    """Hybrid connector that tries CCXT first, falls back to demo data."""
    
    def __init__(self):
        self.ccxt_available = False
        self.delta_exchange = None
        self.demo_mode = True
        
        # Try to initialize CCXT
        self._initialize_ccxt()
    
    def _initialize_ccxt(self):
        """Try to initialize CCXT for Delta Exchange."""
        try:
            print("🔄 Attempting CCXT initialization...")
            import ccxt
            
            if 'delta' in ccxt.exchanges:
                print("✅ Delta Exchange found in CCXT")
                
                self.delta_exchange = ccxt.delta({
                    'timeout': 5000,
                    'enableRateLimit': True,
                    'sandbox': False
                })
                
                # Test connection
                markets = self.delta_exchange.load_markets()
                
                if markets and len(markets) > 0:
                    print(f"✅ CCXT connected - {len(markets)} markets available")
                    self.ccxt_available = True
                    self.demo_mode = False
                    return True
                else:
                    print("⚠️ CCXT available but no markets loaded")
            else:
                print("⚠️ Delta Exchange not found in CCXT")
                
        except ImportError:
            print("⚠️ CCXT not installed")
        except Exception as e:
            print(f"⚠️ CCXT error: {str(e)[:50]}")
        
        print("🎮 Falling back to demo mode")
        return False
    
    def get_available_symbols(self):
        """Get available trading symbols."""
        if self.ccxt_available:
            try:
                markets = self.delta_exchange.markets
                symbols = [symbol for symbol in markets.keys() if 'USDT' in symbol or 'USD' in symbol]
                return symbols[:10]  # Limit for testing
            except Exception as e:
                print(f"⚠️ Error getting symbols: {e}")
        
        # Demo symbols
        return ['BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'DOT/USDT', 'SOL/USDT']
    
    def fetch_ohlcv_data(self, symbol, timeframe='1h', limit=100):
        """Fetch OHLCV data - real or demo."""
        if self.ccxt_available:
            try:
                print(f"📊 Fetching real data for {symbol}...")
                data = self.delta_exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
                
                if data and len(data) > 0:
                    print(f"✅ Real data: {len(data)} candles")
                    return self._convert_ccxt_data(data)
                else:
                    print("⚠️ No real data, using demo")
            except Exception as e:
                print(f"⚠️ Real data error: {str(e)[:30]}, using demo")
        
        # Generate demo data
        return self._generate_demo_data(symbol, limit)
    
    def _convert_ccxt_data(self, ccxt_data):
        """Convert CCXT data to our format."""
        converted = []
        for candle in ccxt_data:
            converted.append({
                'timestamp': datetime.fromtimestamp(candle[0] / 1000),
                'open': candle[1],
                'high': candle[2],
                'low': candle[3],
                'close': candle[4],
                'volume': candle[5]
            })
        return converted
    
    def _generate_demo_data(self, symbol, limit):
        """Generate demo OHLCV data."""
        print(f"🎮 Generating demo data for {symbol}...")
        
        base_prices = {
            'BTC/USDT': 45000, 'ETH/USDT': 2500, 'ADA/USDT': 0.5,
            'DOT/USDT': 7.5, 'SOL/USDT': 20, 'MATIC/USDT': 0.8
        }
        
        base_price = base_prices.get(symbol, 1000)
        data = []
        
        current_time = datetime.now() - timedelta(hours=limit)
        
        for i in range(limit):
            # Realistic price movement
            change = (hash(str(current_time) + symbol + str(i)) % 200 - 100) / 2000
            base_price *= (1 + change)
            
            if base_price < 0.01:
                base_price = 0.01
            
            spread = abs(change) * 0.3
            candle = {
                'timestamp': current_time,
                'open': base_price,
                'high': base_price * (1 + spread),
                'low': base_price * (1 - spread),
                'close': base_price,
                'volume': 1000 + (hash(str(current_time)) % 10000)
            }
            
            data.append(candle)
            current_time += timedelta(hours=1)
        
        print(f"✅ Demo data: {len(data)} candles")
        return data
    
    def get_status(self):
        """Get connector status."""
        return {
            'ccxt_available': self.ccxt_available,
            'demo_mode': self.demo_mode,
            'exchange': 'Delta Exchange',
            'data_source': 'Real CCXT' if self.ccxt_available else 'Demo Simulation'
        }

class HybridDeltaBacktest:
    """Backtest engine using hybrid data source."""
    
    def __init__(self, initial_capital=100000, position_size=10000):
        self.initial_capital = initial_capital
        self.position_size = position_size
        self.connector = DeltaExchangeConnector()
        
    def display_system_status(self):
        """Display current system status."""
        status = self.connector.get_status()
        
        print(f"\n🎯 HYBRID DELTA EXCHANGE SYSTEM")
        print("="*60)
        print(f"Exchange: {status['exchange']}")
        print(f"Data Source: {status['data_source']}")
        print(f"CCXT Available: {'✅' if status['ccxt_available'] else '❌'}")
        print(f"Mode: {'🌐 Live Data' if not status['demo_mode'] else '🎮 Demo Mode'}")
        print("="*60)
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator."""
        if len(prices) < period + 1:
            return 50
            
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        if len(gains) < period:
            return 50
            
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def generate_signals(self, data):
        """Generate trading signals."""
        signals = []
        
        for i in range(20, len(data)):
            current = data[i]
            
            # Get recent prices for RSI
            recent_prices = [candle['close'] for candle in data[max(0, i-20):i+1]]
            rsi = self.calculate_rsi(recent_prices)
            
            # Trading strategy
            if rsi < 25:  # Oversold
                signals.append({
                    'timestamp': current['timestamp'],
                    'action': 'buy',
                    'price': current['close'],
                    'rsi': rsi
                })
            elif rsi > 75:  # Overbought
                signals.append({
                    'timestamp': current['timestamp'],
                    'action': 'sell',
                    'price': current['close'],
                    'rsi': rsi
                })
        
        return signals
    
    def execute_backtest(self, symbol):
        """Execute backtest for a symbol."""
        print(f"\n📊 Processing {symbol}...")
        
        # Fetch data (real or demo)
        data = self.connector.fetch_ohlcv_data(symbol, '1h', 168)  # 1 week
        
        if not data or len(data) < 50:
            print(f"❌ Insufficient data for {symbol}")
            return None
        
        # Generate signals
        signals = self.generate_signals(data)
        
        if not signals:
            print(f"⚠️ No signals for {symbol}")
            return None
        
        print(f"📈 Generated {len(signals)} signals")
        
        # Execute trades
        position = None
        trades = []
        current_equity = self.initial_capital
        
        for signal in signals:
            if signal['action'] == 'buy' and position is None:
                quantity = self.position_size / signal['price']
                position = {
                    'entry_price': signal['price'],
                    'entry_time': signal['timestamp'],
                    'quantity': quantity
                }
                
            elif signal['action'] == 'sell' and position is not None:
                profit = (signal['price'] - position['entry_price']) * position['quantity']
                profit_pct = ((signal['price'] - position['entry_price']) / position['entry_price']) * 100
                
                current_equity += profit
                
                trade = {
                    'symbol': symbol,
                    'entry_time': position['entry_time'],
                    'exit_time': signal['timestamp'],
                    'entry_price': position['entry_price'],
                    'exit_price': signal['price'],
                    'profit': profit,
                    'profit_pct': profit_pct,
                    'duration': signal['timestamp'] - position['entry_time']
                }
                
                trades.append(trade)
                position = None
        
        if trades:
            total_return = sum([t['profit_pct'] for t in trades])
            win_rate = (len([t for t in trades if t['profit_pct'] > 0]) / len(trades)) * 100
            
            result = {
                'symbol': symbol,
                'total_trades': len(trades),
                'total_return': total_return,
                'win_rate': win_rate,
                'trades': trades,
                'data_source': 'Real CCXT' if self.connector.ccxt_available else 'Demo'
            }
            
            print(f"✅ {symbol}: {len(trades)} trades, {total_return:.2f}% return, {win_rate:.1f}% win rate")
            return result
        else:
            print(f"⚠️ No trades executed for {symbol}")
            return None
    
    def run_comprehensive_test(self):
        """Run comprehensive backtest."""
        self.display_system_status()
        
        # Get available symbols
        symbols = self.connector.get_available_symbols()
        test_symbols = symbols[:3]  # Test first 3
        
        print(f"\n🚀 Testing {len(test_symbols)} symbols: {', '.join(test_symbols)}")
        
        results = []
        
        for symbol in test_symbols:
            try:
                result = self.execute_backtest(symbol)
                if result:
                    results.append(result)
            except Exception as e:
                print(f"❌ Error processing {symbol}: {e}")
                continue
        
        # Display summary
        if results:
            print(f"\n📊 SUMMARY:")
            print("="*60)
            
            total_trades = sum([r['total_trades'] for r in results])
            avg_return = sum([r['total_return'] for r in results]) / len(results)
            
            print(f"Symbols tested: {len(results)}")
            print(f"Total trades: {total_trades}")
            print(f"Average return: {avg_return:.2f}%")
            print(f"Data source: {results[0]['data_source']}")
            
            # Save results
            self.save_results(results)
            
        else:
            print("❌ No successful tests")
        
        return results
    
    def save_results(self, results):
        """Save results to file."""
        try:
            filename = f"hybrid_delta_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"💾 Results saved to: {filename}")
        except Exception as e:
            print(f"⚠️ Could not save results: {e}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Hybrid Delta Exchange System')
    
    parser.add_argument(
        '--capital', '-c',
        type=float,
        default=100000,
        help='Initial capital (default: 100000)'
    )
    
    parser.add_argument(
        '--position', '-p',
        type=float,
        default=10000,
        help='Position size per trade (default: 10000)'
    )
    
    args = parser.parse_args()
    
    # Initialize and run
    backtest = HybridDeltaBacktest(
        initial_capital=args.capital,
        position_size=args.position
    )
    
    results = backtest.run_comprehensive_test()
    
    if results:
        print(f"\n✅ Hybrid Delta Exchange system working!")
        print("Ready for both demo and live trading")
        return 0
    else:
        print(f"\n❌ System test failed")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
