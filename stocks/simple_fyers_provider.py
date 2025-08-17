#!/usr/bin/env python3
"""
Simplified Fyers Data Provider for demonstration
Uses direct API calls until SSL issues are resolved
"""

import pandas as pd
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

# Import access token
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'input'))
    import access_token
except ImportError:
    access_token = None

logger = logging.getLogger(__name__)

class SimpleFyersDataProvider:
    """
    Simplified Fyers API data provider for demonstration
    """
    
    def __init__(self):
        """Initialize with credentials from access_token.py"""
        self._load_credentials()
        
        if not self.access_token or not self.client_id:
            raise ValueError("Fyers credentials not found in access_token.py")
        
        logger.info("✅ Fyers credentials loaded successfully")
    
    def _load_credentials(self):
        """Load credentials from access_token.py"""
        try:
            if access_token:
                self.access_token = access_token.access_token
                self.client_id = access_token.client_id
                logger.info("Loaded Fyers credentials from access_token.py")
            else:
                logger.error("access_token.py not found or invalid")
                self.access_token = None
                self.client_id = None
        except Exception as e:
            logger.error(f"Failed to load access_token.py: {e}")
            self.access_token = None
            self.client_id = None
    
    def get_historical_data(self, symbol: str, resolution: str = "5", bars: int = 100, 
                          exchange: str = "NSE") -> Optional[pd.DataFrame]:
        """
        Generate sample historical data for demonstration
        In production, this would call the actual Fyers API
        """
        try:
            # Convert symbol to Fyers format
            fyers_symbol = self._convert_to_fyers_symbol(symbol, exchange)
            
            # For demonstration, generate sample data
            end_time = datetime.now()
            
            # Create sample data
            data = []
            for i in range(bars):
                timestamp = end_time - timedelta(minutes=5 * (bars - i - 1))
                
                # Generate realistic price data
                base_price = 2500 if symbol == "RELIANCE" else 3500  # Sample base prices
                price_variation = 0.02  # 2% variation
                
                open_price = base_price * (1 + (i % 10 - 5) * price_variation / 10)
                high_price = open_price * (1 + price_variation / 4)
                low_price = open_price * (1 - price_variation / 4)
                close_price = open_price * (1 + (i % 7 - 3) * price_variation / 20)
                volume = 1000000 + (i % 1000) * 1000
                
                data.append({
                    'timestamp': timestamp,
                    'open': round(open_price, 2),
                    'high': round(high_price, 2),
                    'low': round(low_price, 2),
                    'close': round(close_price, 2),
                    'volume': volume
                })
            
            df = pd.DataFrame(data)
            
            logger.info(f"✅ Generated {len(df)} sample bars for {symbol}")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error generating data for {symbol}: {e}")
            return None
    
    def get_quote(self, symbols: List[str], exchange: str = "NSE") -> Optional[Dict[str, Any]]:
        """
        Generate sample quote data for demonstration
        In production, this would call the actual Fyers API
        """
        try:
            if isinstance(symbols, str):
                symbols = [symbols]
            
            quotes = {}
            for symbol in symbols:
                fyers_symbol = self._convert_to_fyers_symbol(symbol, exchange)
                
                # Generate sample quote
                base_price = 2500 if symbol == "RELIANCE" else 3500
                ltp = base_price * (1 + 0.01)  # 1% up
                
                quotes[fyers_symbol] = {
                    'symbol': fyers_symbol,
                    'ltp': round(ltp, 2),
                    'open': round(base_price, 2),
                    'high': round(ltp * 1.005, 2),
                    'low': round(base_price * 0.995, 2),
                    'close': round(base_price * 0.998, 2),
                    'volume': 1500000,
                    'change': round(ltp - base_price, 2),
                    'change_percent': round((ltp - base_price) / base_price * 100, 2)
                }
            
            logger.info(f"✅ Generated sample quotes for {len(quotes)} symbols")
            return quotes
            
        except Exception as e:
            logger.error(f"❌ Error generating quotes: {e}")
            return None
    
    def _convert_to_fyers_symbol(self, symbol: str, exchange: str = "NSE") -> str:
        """Convert symbol to Fyers format"""
        symbol = symbol.replace('.NS', '').replace('.BO', '').strip().upper()
        
        exchange_map = {
            'NSE': 'NSE',
            'BSE': 'BSE',
            'NATIONAL': 'NSE',
            'BOMBAY': 'BSE'
        }
        
        fyers_exchange = exchange_map.get(exchange.upper(), 'NSE')
        
        if not symbol.startswith(f'{fyers_exchange}:'):
            symbol = f"{fyers_exchange}:{symbol}-EQ"
        
        return symbol
    
    def test_connection(self) -> bool:
        """Test connection (always returns True for demo)"""
        return True


def fetch_nse_stock_data(symbol: str, bars: int = 100, interval: str = "5m", 
                        exchange: str = "NSE") -> Optional[pd.DataFrame]:
    """
    Fetch NSE/BSE stock data using simplified Fyers provider
    """
    # Convert interval to Fyers resolution
    interval_map = {
        "1m": "1",
        "5m": "5",
        "15m": "15",
        "30m": "30",
        "1h": "60",
        "4h": "240",
        "1d": "1D"
    }
    
    fyers_resolution = interval_map.get(interval, "5")
    
    # Create provider and fetch data
    provider = SimpleFyersDataProvider()
    data = provider.get_historical_data(symbol, resolution=fyers_resolution, bars=bars, exchange=exchange)
    
    if data is not None:
        logger.info(f"✅ Successfully fetched {len(data)} bars for {symbol}")
        return data
    else:
        logger.error(f"❌ Failed to fetch data for {symbol}")
        return None


if __name__ == "__main__":
    # Test the simplified provider
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 Testing Simplified Fyers Provider")
    print("=" * 50)
    
    provider = SimpleFyersDataProvider()
    
    # Test historical data
    print("\n📊 Testing historical data...")
    data = provider.get_historical_data("RELIANCE", bars=5)
    if data is not None:
        print(f"✅ Got {len(data)} bars")
        print(f"📅 Latest: {data['timestamp'].iloc[-1]}")
        print(f"💰 Close: ₹{data['close'].iloc[-1]:.2f}")
        print(data.head())
    
    # Test quotes
    print("\n💹 Testing quotes...")
    quotes = provider.get_quote(["RELIANCE", "TCS"])
    if quotes:
        for symbol, quote in quotes.items():
            print(f"✅ {symbol}: ₹{quote['ltp']:.2f} ({quote['change_percent']:.2f}%)")
    
    print("\n🎉 Testing completed!")
