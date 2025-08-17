#!/usr/bin/env python3
"""
Fyers Data Provider - NSE/BSE Stock Data using Fyers API
This is the primary and exclusive data source for NSE/BSE stock data.
"""

import pandas as pd
import time
from datetime import datetime, timedelta
import logging
import json
import os
from typing import Optional, Dict, Any, List

# Import Fyers API library
try:
    from fyers_apiv3 import fyersModel
except ImportError:
    print("❌ fyers-apiv3 not installed. Please install it: pip install fyers-apiv3")
    fyersModel = None

# Import access token
try:
    import sys
    import os
    # Add the fyers directory to path to import access_token
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fyers'))
    import access_token
except ImportError:
    access_token = None

logger = logging.getLogger(__name__)

class FyersDataProvider:
    """
    Fyers API data provider for NSE/BSE stocks.
    This is the ONLY data source for Indian equity data.
    """
    
    def __init__(self, access_token_str: Optional[str] = None, client_id: Optional[str] = None):
        """
        Initialize Fyers data provider
        Args:
            access_token_str: Fyers API access token (optional, will read from access_token.py)
            client_id: Fyers client ID (optional, will read from access_token.py)
        """
        if not fyersModel:
            raise ImportError("fyers-apiv3 library not found. Please install it: pip install fyers-apiv3")
        
        # Load credentials from access_token.py if not provided
        if access_token_str and client_id:
            self.access_token = access_token_str
            self.client_id = client_id
        else:
            self._load_credentials()
        
        # Initialize Fyers model
        if self.access_token and self.client_id:
            self.fyers = fyersModel.FyersModel(client_id=self.client_id, token=self.access_token)
            logger.info("✅ Fyers API credentials loaded successfully")
        else:
            logger.error("❌ Failed to load Fyers API credentials")
            raise ValueError("Fyers API credentials not found. Please run generate_token.py first.")
    
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
        Get historical data from Fyers API
        Args:
            symbol: Stock symbol (e.g., "RELIANCE", "TCS")
            resolution: Time resolution (1, 2, 3, 5, 10, 15, 20, 30, 60, 120, 240, 1D)
            bars: Number of bars to fetch
            exchange: Exchange name (NSE/BSE)
        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
        """
        try:
            # Convert symbol to Fyers format
            fyers_symbol = self._convert_to_fyers_symbol(symbol, exchange)
            
            # Calculate date range based on bars and resolution
            end_date = datetime.now()
            
            # Estimate days needed based on resolution and bars
            if resolution == "1D":
                days = bars + 5  # Add buffer for weekends
            elif resolution in ["60", "120", "240"]:
                days = max(bars // 6, 5)  # Rough estimate for hourly data
            else:
                days = max(bars // 78, 2)  # Rough estimate for minute data
            
            start_date = end_date - timedelta(days=days)
            
            # Prepare data request
            data_request = {
                "symbol": fyers_symbol,
                "resolution": resolution,
                "date_format": "1",  # Timestamp format
                "range_from": start_date.strftime("%Y-%m-%d"),
                "range_to": end_date.strftime("%Y-%m-%d"),
                "cont_flag": "1"
            }
            
            # Fetch data using Fyers API
            response = self.fyers.history(data_request)
            
            if response["s"] == "ok" and "candles" in response:
                # Convert to DataFrame
                candles = response["candles"]
                if not candles:
                    logger.warning(f"No data returned for {symbol}")
                    return None
                
                df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                
                # Convert timestamp to datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                
                # Ensure proper data types
                for col in ['open', 'high', 'low', 'close', 'volume']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Sort by timestamp and limit to requested bars
                df = df.sort_values('timestamp')
                if len(df) > bars:
                    df = df.tail(bars)
                
                logger.info(f"✅ Fetched {len(df)} bars for {symbol} from Fyers API")
                return df
            else:
                logger.error(f"❌ Fyers API error for {symbol}: {response.get('message', 'Unknown error')}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Fyers API exception for {symbol}: {e}")
            return None
    
    def get_quote(self, symbols: List[str], exchange: str = "NSE") -> Optional[Dict[str, Any]]:
        """
        Get current quotes from Fyers API
        Args:
            symbols: List of symbols or single symbol
            exchange: Exchange name (NSE/BSE)
        Returns:
            Dictionary with quote data
        """
        try:
            if isinstance(symbols, str):
                symbols = [symbols]
            
            # Convert symbols to Fyers format
            fyers_symbols = [self._convert_to_fyers_symbol(s, exchange) for s in symbols]
            
            # Prepare quotes request
            quotes_request = {
                "symbols": fyers_symbols
            }
            
            # Fetch quotes using Fyers API
            response = self.fyers.quotes(quotes_request)
            
            if response["s"] == "ok" and "d" in response:
                quotes = {}
                for symbol_data in response["d"]:
                    symbol = symbol_data["n"]
                    quotes[symbol] = {
                        'symbol': symbol,
                        'ltp': symbol_data["v"]["lp"],  # Last traded price
                        'open': symbol_data["v"]["o"],
                        'high': symbol_data["v"]["h"],
                        'low': symbol_data["v"]["l"],
                        'close': symbol_data["v"]["c"],
                        'volume': symbol_data["v"]["vol"],
                        'change': symbol_data["v"]["ch"],
                        'change_percent': symbol_data["v"]["chp"]
                    }
                
                logger.info(f"✅ Fetched quotes for {len(quotes)} symbols from Fyers API")
                return quotes
            else:
                logger.error(f"❌ Fyers quotes API error: {response.get('message', 'Unknown error')}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Fyers quotes API exception: {e}")
            return None
    
    def _convert_to_fyers_symbol(self, symbol: str, exchange: str = "NSE") -> str:
        """
        Convert symbol to Fyers format
        Args:
            symbol: Symbol like "RELIANCE" or "RELIANCE.NS"
            exchange: Exchange name (NSE/BSE)
        Returns:
            Fyers format like "NSE:RELIANCE-EQ"
        """
        # Clean symbol
        symbol = symbol.replace('.NS', '').replace('.BO', '').strip().upper()
        
        # Map exchange
        exchange_map = {
            'NSE': 'NSE',
            'BSE': 'BSE',
            'NATIONAL': 'NSE',
            'BOMBAY': 'BSE'
        }
        
        fyers_exchange = exchange_map.get(exchange.upper(), 'NSE')
        
        # Add exchange prefix and equity suffix
        if not symbol.startswith(f'{fyers_exchange}:'):
            symbol = f"{fyers_exchange}:{symbol}-EQ"
        
        return symbol
    
    def test_connection(self) -> bool:
        """
        Test the Fyers API connection
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Test with a simple quote request
            test_result = self.get_quote(["RELIANCE"], "NSE")
            if test_result:
                logger.info("✅ Fyers API connection test successful")
                return True
            else:
                logger.error("❌ Fyers API connection test failed")
                return False
        except Exception as e:
            logger.error(f"❌ Fyers API connection test exception: {e}")
            return False


def fetch_nse_stock_data(symbol: str, bars: int = 100, interval: str = "5m", 
                        exchange: str = "NSE") -> Optional[pd.DataFrame]:
    """
    Main function to fetch NSE/BSE stock data using Fyers API
    This is the ONLY function used for stock data fetching.
    
    Args:
        symbol: Stock symbol (e.g., "RELIANCE", "TCS")
        bars: Number of bars to fetch
        interval: Data interval (1m, 5m, 15m, 30m, 1h, 4h, 1d)
        exchange: Exchange name (NSE/BSE)
    
    Returns:
        DataFrame with OHLCV data
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
    provider = FyersDataProvider()
    data = provider.get_historical_data(symbol, resolution=fyers_resolution, bars=bars, exchange=exchange)
    
    if data is not None:
        logger.info(f"✅ Successfully fetched {len(data)} bars for {symbol} from Fyers API")
        return data
    else:
        logger.error(f"❌ Failed to fetch data for {symbol} from Fyers API")
        return None


if __name__ == "__main__":
    # Test the Fyers data provider
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 Testing Fyers Data Provider")
    print("=" * 50)
    
    # Test connection
    provider = FyersDataProvider()
    if not provider.test_connection():
        print("❌ Failed to connect to Fyers API")
        exit(1)
    
    # Test data fetching
    test_symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]
    
    for symbol in test_symbols:
        print(f"\n📊 Testing {symbol}")
        print("-" * 30)
        
        # Test historical data
        data = fetch_nse_stock_data(symbol, bars=10, interval="5m", exchange="NSE")
        
        if data is not None:
            print(f"✅ Historical data: {len(data)} bars")
            print(f"📅 Latest timestamp: {data['timestamp'].iloc[-1]}")
            print(f"💰 Latest close price: ₹{data['close'].iloc[-1]:.2f}")
            print(f"📈 High: ₹{data['high'].iloc[-1]:.2f}")
            print(f"📉 Low: ₹{data['low'].iloc[-1]:.2f}")
            print(f"📊 Volume: {data['volume'].iloc[-1]:,.0f}")
        else:
            print("❌ Failed to fetch historical data")
        
        # Test quotes
        quotes = provider.get_quote([symbol], "NSE")
        if quotes:
            quote = list(quotes.values())[0]
            print(f"💹 Live quote: ₹{quote['ltp']:.2f}")
            print(f"📊 Change: {quote['change']:.2f} ({quote['change_percent']:.2f}%)")
        else:
            print("❌ Failed to fetch quote")
        
        time.sleep(1)  # Rate limiting
    
    print("\n🎉 Fyers Data Provider testing completed!")
