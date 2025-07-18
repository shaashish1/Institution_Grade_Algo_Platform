"""
Crypto Trader
============

Main crypto trading functionality with CCXT integration.
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class CryptoTrader:
    """Main crypto trading class"""
    
    def __init__(self):
        self.exchanges = {}
        self.default_exchange = None
        self.initialize_exchanges()
    
    def initialize_exchanges(self):
        """Initialize available exchanges"""
        try:
            # Initialize major exchanges in sandbox mode
            self.exchanges = {
                'binance': ccxt.binance({
                    'sandbox': True,
                    'enableRateLimit': True,
                }),
                'coinbase': ccxt.coinbasepro({
                    'sandbox': True,
                    'enableRateLimit': True,
                }),
                'kraken': ccxt.kraken({
                    'enableRateLimit': True,
                })
            }
            
            # Set default exchange
            self.default_exchange = 'binance'
            print("✅ Crypto exchanges initialized successfully")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize all exchanges: {e}")
            # Fallback to basic exchange
            self.exchanges = {'binance': ccxt.binance({'enableRateLimit': True})}
            self.default_exchange = 'binance'
    
    def get_market_data(self, symbol: str, exchange: str = None) -> Optional[Dict]:
        """Get current market data for a symbol"""
        try:
            exchange_name = exchange or self.default_exchange
            exchange_obj = self.exchanges.get(exchange_name)
            
            if not exchange_obj:
                print(f"❌ Exchange {exchange_name} not available")
                return None
            
            # Get ticker data
            ticker = exchange_obj.fetch_ticker(symbol)
            
            return {
                'symbol': symbol,
                'price': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'volume': ticker['baseVolume'],
                'change_24h': ticker['percentage'],
                'high_24h': ticker['high'],
                'low_24h': ticker['low'],
                'timestamp': datetime.now().isoformat(),
                'exchange': exchange_name
            }
            
        except Exception as e:
            print(f"❌ Error getting market data for {symbol}: {e}")
            return None
    
    def get_historical_data(self, symbol: str, timeframe: str = '1h', limit: int = 100, exchange: str = None) -> Optional[pd.DataFrame]:
        """Get historical OHLCV data"""
        try:
            exchange_name = exchange or self.default_exchange
            exchange_obj = self.exchanges.get(exchange_name)
            
            if not exchange_obj:
                print(f"❌ Exchange {exchange_name} not available")
                return None
            
            # Fetch OHLCV data
            ohlcv = exchange_obj.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"❌ Error getting historical data for {symbol}: {e}")
            return None
    
    def technical_analysis(self, symbol: str, timeframe: str = '1h') -> Optional[Dict]:
        """Perform technical analysis on a symbol"""
        try:
            # Get historical data
            df = self.get_historical_data(symbol, timeframe, limit=200)
            if df is None or df.empty:
                return None
            
            # Calculate technical indicators
            analysis = {}
            
            # Simple Moving Averages
            df['sma_20'] = df['close'].rolling(window=20).mean()
            df['sma_50'] = df['close'].rolling(window=50).mean()
            
            # RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # MACD
            exp1 = df['close'].ewm(span=12).mean()
            exp2 = df['close'].ewm(span=26).mean()
            df['macd'] = exp1 - exp2
            df['macd_signal'] = df['macd'].ewm(span=9).mean()
            
            # Bollinger Bands
            df['bb_middle'] = df['close'].rolling(window=20).mean()
            bb_std = df['close'].rolling(window=20).std()
            df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
            df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
            
            # Get latest values
            latest = df.iloc[-1]
            
            analysis = {
                'Current Price': f"${latest['close']:.4f}",
                'SMA 20': f"${latest['sma_20']:.4f}",
                'SMA 50': f"${latest['sma_50']:.4f}",
                'RSI': f"{latest['rsi']:.2f}",
                'MACD': f"{latest['macd']:.6f}",
                'MACD Signal': f"{latest['macd_signal']:.6f}",
                'BB Upper': f"${latest['bb_upper']:.4f}",
                'BB Lower': f"${latest['bb_lower']:.4f}",
                'Volume': f"{latest['volume']:.2f}",
            }
            
            # Add signals
            if latest['rsi'] > 70:
                analysis['RSI Signal'] = "Overbought ⚠️"
            elif latest['rsi'] < 30:
                analysis['RSI Signal'] = "Oversold 📈"
            else:
                analysis['RSI Signal'] = "Neutral ➡️"
            
            if latest['close'] > latest['sma_20']:
                analysis['Trend (SMA20)'] = "Bullish 📈"
            else:
                analysis['Trend (SMA20)'] = "Bearish 📉"
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error in technical analysis for {symbol}: {e}")
            return None
    
    def show_price_chart(self, symbol: str, timeframe: str = '1h', days: int = 7):
        """Show interactive price chart"""
        try:
            # Calculate limit based on timeframe and days
            if timeframe == '1h':
                limit = days * 24
            elif timeframe == '4h':
                limit = days * 6
            elif timeframe == '1d':
                limit = days
            else:
                limit = 100
            
            # Get historical data
            df = self.get_historical_data(symbol, timeframe, limit=limit)
            if df is None or df.empty:
                print(f"❌ No data available for {symbol}")
                return
            
            # Create candlestick chart
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=(f'{symbol} Price Chart ({timeframe})', 'Volume'),
                row_width=[0.7, 0.3]
            )
            
            # Add candlestick
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    name='Price'
                ),
                row=1, col=1
            )
            
            # Add volume
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df['volume'],
                    name='Volume',
                    marker_color='rgba(158,202,225,0.8)'
                ),
                row=2, col=1
            )
            
            # Update layout
            fig.update_layout(
                title=f'{symbol} - {timeframe} Chart',
                yaxis_title='Price (USD)',
                xaxis_rangeslider_visible=False,
                height=600
            )
            
            fig.show()
            
        except Exception as e:
            print(f"❌ Error showing chart for {symbol}: {e}")
    
    def configure_exchanges(self):
        """Configure exchange settings"""
        print("\n⚙️  Exchange Configuration")
        print("=" * 25)
        
        print("Available exchanges:")
        for i, (name, exchange) in enumerate(self.exchanges.items(), 1):
            status = "✅ Connected" if exchange else "❌ Not connected"
            print(f"  {i}. {name.title()}: {status}")
        
        print(f"\nCurrent default exchange: {self.default_exchange}")
        
        choice = input("\nEnter exchange number to set as default (or press Enter to skip): ").strip()
        if choice.isdigit():
            exchange_names = list(self.exchanges.keys())
            idx = int(choice) - 1
            if 0 <= idx < len(exchange_names):
                self.default_exchange = exchange_names[idx]
                print(f"✅ Default exchange set to: {self.default_exchange}")
    
    def get_available_symbols(self, exchange: str = None) -> List[str]:
        """Get available trading symbols"""
        try:
            exchange_name = exchange or self.default_exchange
            exchange_obj = self.exchanges.get(exchange_name)
            
            if not exchange_obj:
                return []
            
            markets = exchange_obj.load_markets()
            return list(markets.keys())
            
        except Exception as e:
            print(f"❌ Error getting symbols: {e}")
            return []
    
    def place_order(self, symbol: str, side: str, amount: float, price: float = None, order_type: str = 'market') -> Optional[Dict]:
        """Place a trading order (demo/paper trading)"""
        try:
            print(f"📝 Demo Order Placed:")
            print(f"   Symbol: {symbol}")
            print(f"   Side: {side.upper()}")
            print(f"   Amount: {amount}")
            print(f"   Type: {order_type.upper()}")
            if price:
                print(f"   Price: ${price}")
            print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Return mock order
            return {
                'id': f'demo_{int(datetime.now().timestamp())}',
                'symbol': symbol,
                'side': side,
                'amount': amount,
                'price': price,
                'type': order_type,
                'status': 'filled',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error placing order: {e}")
            return None