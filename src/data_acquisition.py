"""
Enhanced Data Acquisition Module for AlgoProject
Supports multiple data sources with error handling and timeout management
"""

from tvDatafeed import TvDatafeed, Interval
import ccxt
import pandas as pd
import threading
from datetime import datetime

def fetch_data(symbol, exchange, interval, bars, data_source="auto", fetch_timeout=15):
    """
    Enhanced data fetching function supporting multiple data sources.
    
    Args:
        symbol (str): Trading symbol (e.g., "BTC/USDT", "RELIANCE")
        exchange (str): Exchange name (e.g., "kraken", "NSE")
        interval (str): Time interval (e.g., "5m", "1h", "1d")
        bars (int): Number of historical bars to fetch
        data_source (str): "tvdatafeed", "ccxt", or "auto" (auto-detect)
        fetch_timeout (int): Timeout in seconds for data fetching
    
    Returns:
        pandas.DataFrame: OHLCV data with columns [timestamp, open, high, low, close, volume]
    """
    
    # Auto-detect data source based on symbol format
    if data_source == "auto":
        if "/" in symbol:  # Crypto format like BTC/USDT
            data_source = "ccxt"
        else:  # Stock format like RELIANCE
            data_source = "tvdatafeed"
    
    if data_source == "tvdatafeed":
        return _fetch_tvdatafeed(symbol, exchange, interval, bars, fetch_timeout)
    elif data_source == "ccxt":
        return _fetch_ccxt(symbol, exchange, interval, bars, fetch_timeout)
    else:
        raise ValueError(f"Unsupported data source: {data_source}")

def _fetch_tvdatafeed(symbol, exchange, interval, bars, fetch_timeout, username=None, password=None):
    """Fetch data using TvDatafeed with optional authentication."""
    try:
        # Try authenticated connection first if credentials provided
        if username and password:
            try:
                tv = TvDatafeed(username=username, password=password)
                print(f"✅ TradingView authenticated for {username}")
            except Exception as auth_error:
                print(f"⚠️  TradingView auth failed: {auth_error}, using anonymous")
                tv = TvDatafeed()
        else:
            tv = TvDatafeed()
        
        # Convert interval string to Interval enum
        interval_map = {
            "1m": Interval.in_1_minute,
            "5m": Interval.in_5_minute,
            "15m": Interval.in_15_minute,
            "1h": Interval.in_1_hour,
            "4h": Interval.in_4_hour,
            "1d": Interval.in_daily,
            "in_5_minute": Interval.in_5_minute  # Support direct format
        }
        
        tv_interval = interval_map.get(interval, Interval.in_5_minute)
        data = tv.get_hist(symbol=symbol, exchange=exchange, interval=tv_interval, n_bars=bars)
        
        if data is None or data.empty:
            raise ValueError(f"No data returned for {symbol} from TvDatafeed")
        
        # Convert to standard format with proper datetime handling
        data = data.reset_index()
        
        # Fix datetime column name
        if 'datetime' in data.columns:
            data['timestamp'] = pd.to_datetime(data['datetime'])
        elif data.index.name == 'datetime':
            data = data.reset_index()
            data['timestamp'] = pd.to_datetime(data['datetime'])
        
        # Ensure timestamp is in the right format for strategy
        if 'timestamp' in data.columns:
            # Keep as datetime object for strategy compatibility
            pass
        
        return data[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        
    except Exception as e:
        print(f"TvDatafeed error for {symbol}: {e}")
        return pd.DataFrame()

def _fetch_ccxt(symbol, exchange, interval, bars, fetch_timeout):
    """Fetch data using CCXT with timeout management."""
    try:
        # Initialize exchange
        if exchange.upper() == "KRAKEN":
            exchange_obj = ccxt.kraken()
        else:
            exchange_obj = getattr(ccxt, exchange.lower())()
        
        exchange_obj.enableRateLimit = True
        markets = exchange_obj.load_markets()
        
        # Symbol mapping for different exchanges
        if symbol not in markets:
            for market in markets:
                if market.replace('/', '') == symbol.replace('/', ''):
                    symbol = market
                    break
        
        # Use threading for timeout management
        result = {}
        
        def fetch_with_timeout():
            try:
                ohlcv = exchange_obj.fetch_ohlcv(symbol, timeframe=interval, limit=bars)
                result['data'] = ohlcv
            except Exception as e:
                result['error'] = e
        
        thread = threading.Thread(target=fetch_with_timeout)
        thread.start()
        thread.join(timeout=fetch_timeout)
        
        if thread.is_alive():
            raise RuntimeError(f"Timeout fetching data for {symbol} on {exchange}")
        if 'error' in result:
            raise RuntimeError(f"Error fetching data for {symbol} on {exchange}: {result['error']}")
        
        ohlcv = result.get('data', [])
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        
        if df.empty:
            raise RuntimeError(f"No data returned for {symbol} on {exchange}")
        
        # Convert timestamp from milliseconds to seconds if needed
        if df['timestamp'].max() > 1e12:
            df['timestamp'] = df['timestamp'] // 1000
        
        return df
        
    except Exception as e:
        print(f"CCXT error for {symbol}: {e}")
        return pd.DataFrame()

def add_ist_datetime(df):
    """Add IST datetime column to the dataframe."""
    if not df.empty and 'timestamp' in df.columns:
        df['datetime_ist'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
    return df

# Example usage
if __name__ == "__main__":
    # Test crypto data (CCXT)
    crypto_data = fetch_data("BTC/USDT", "kraken", "5m", 100)
    crypto_data = add_ist_datetime(crypto_data)
    print("Crypto Data:")
    print(crypto_data.head())
    
    # Test stock data (TvDatafeed)
    # stock_data = fetch_data("RELIANCE", "NSE", "1h", 100)
    # stock_data = add_ist_datetime(stock_data)
    # print("\nStock Data:")
    # print(stock_data.head())
