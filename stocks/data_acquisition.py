"""
Stocks Data Acquisition Module for AlgoProject
- NSE/BSE Stock Data: Uses FYERS API exclusively (no TradingView or other sources)
- Crypto Data: Uses CCXT for multiple exchanges (for mixed portfolios)
"""

# Lazy import CCXT to avoid blocking on module load
ccxt = None

import pandas as pd
import threading
import yaml
import os
import warnings
import logging
from datetime import datetime

# Import Fyers data provider for NSE/BSE stocks
try:
    from .simple_fyers_provider import fetch_nse_stock_data, SimpleFyersDataProvider
except ImportError:
    # Fallback import for when running as standalone script
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from simple_fyers_provider import fetch_nse_stock_data, SimpleFyersDataProvider

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _ensure_ccxt():
    """Ensure CCXT is imported when needed (lazy loading)"""
    global ccxt
    if ccxt is None:
        try:
            import ccxt as _ccxt
            ccxt = _ccxt
            logger.info("✅ CCXT imported successfully")
        except ImportError as e:
            logger.error(f"❌ Failed to import CCXT: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error importing CCXT: {e}")
            raise
    return ccxt


def fetch_data(symbol, exchange, interval, bars, data_source="auto", fetch_timeout=15):
    """
    Enhanced data fetching function with Fyers API for NSE/BSE stocks.
    
    Args:
        symbol (str): Trading symbol (e.g., "BTC/USDT", "RELIANCE")
        exchange (str): Exchange name (e.g., "kraken", "NSE", "BSE")
        interval (str): Time interval (e.g., "5m", "1h", "1d")
        bars (int): Number of historical bars to fetch
        data_source (str): "fyers", "ccxt", or "auto" (auto-detect)
        fetch_timeout (int): Timeout in seconds for data fetching
    
    Returns:
        pandas.DataFrame: OHLCV data with columns [timestamp, open, high, low, close, volume]
    """
    
    # Auto-detect data source based on symbol format and exchange
    if data_source == "auto":
        if "/" in symbol:  # Crypto format like BTC/USDT
            data_source = "ccxt"
        elif exchange.upper() in ["NSE", "BSE"]:  # Indian stock exchanges
            data_source = "fyers"
        else:  # Default to crypto for other exchanges
            data_source = "ccxt"
    
    if data_source == "fyers":
        return _fetch_fyers_data(symbol, exchange, interval, bars)
    elif data_source == "ccxt":
        return _fetch_ccxt(symbol, exchange, interval, bars, fetch_timeout)
    else:
        raise ValueError(f"Unsupported data source: {data_source}")


def _fetch_fyers_data(symbol, exchange, interval, bars):
    """
    Fetch NSE/BSE stock data using Fyers API.
    This is the ONLY data source for Indian equity markets.
    """
    try:
        from stocks.fyers_data_provider import FyersDataProvider
        provider = FyersDataProvider()
        data = provider.get_historical_data(symbol, exchange, interval, bars)
        return data
    except Exception as e:
        logger.error(f"❌ Fyers API error for {symbol}: {e}")
        return pd.DataFrame()


def _fetch_ccxt(symbol, exchange, interval, bars, fetch_timeout):
    """Fetch crypto data using CCXT with timeout management."""
    try:
        # Ensure CCXT is loaded (lazy loading)
        _ccxt = _ensure_ccxt()
        
        logger.info(f"🔄 Fetching {symbol} from {exchange} via CCXT")
        
        # Initialize exchange
        if exchange.upper() == "KRAKEN":
            exchange_obj = _ccxt.kraken()
        else:
            exchange_obj = getattr(_ccxt, exchange.lower())()
        
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
        
        # Convert timestamp from milliseconds to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        logger.info(f"✅ Successfully fetched {len(df)} bars for {symbol} from {exchange}")
        return df
        
    except Exception as e:
        logger.error(f"❌ CCXT error for {symbol}: {e}")
        return pd.DataFrame()


def get_live_quote(symbol, exchange="NSE"):
    """
    Get live quote for NSE/BSE stocks using Fyers API.
    
    Args:
        symbol (str): Stock symbol (e.g., "RELIANCE")
        exchange (str): Exchange name (NSE/BSE)
    
    Returns:
        dict: Live quote data or None if failed
    """
    try:
        provider = SimpleFyersDataProvider()
        quotes = provider.get_quote([symbol], exchange)
        
        if quotes:
            return list(quotes.values())[0]
        else:
            logger.error(f"❌ Failed to get live quote for {symbol}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error getting live quote for {symbol}: {e}")
        return None


def add_ist_datetime(df):
    """Add IST datetime column to the dataframe."""
    if not df.empty and 'timestamp' in df.columns:
        # Ensure timestamp is datetime
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Add IST timezone
        df['datetime_ist'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
    return df


def test_fyers_connection():
    """Test Fyers API connection."""
    try:
        provider = SimpleFyersDataProvider()
        return provider.test_connection()
    except Exception as e:
        logger.error(f"❌ Fyers connection test failed: {e}")
        return False


# Health check function
def health_check():
    """
    Perform health check on stocks data acquisition module.
    
    Returns:
        dict: Health check results
    """
    results = {
        'module': 'stocks.data_acquisition',
        'fyers_available': False,
        'ccxt_available': False,
        'fyers_connection': False,
        'status': 'unknown'
    }
    
    try:
        # Check Fyers availability
        try:
            from .simple_fyers_provider import SimpleFyersDataProvider
            results['fyers_available'] = True
            
            # Test Fyers connection
            if test_fyers_connection():
                results['fyers_connection'] = True
        except Exception:
            pass
        
        # Check CCXT availability
        try:
            import ccxt
            results['ccxt_available'] = True
        except Exception:
            pass
        
        if results['fyers_connection']:
            results['status'] = 'healthy'
        elif results['fyers_available']:
            results['status'] = 'degraded'
        else:
            results['status'] = 'error'
            
    except Exception as e:
        results['status'] = 'error'
        results['error'] = str(e)
    
    return results


# Example usage and testing
if __name__ == "__main__":
    print("🚀 Testing Stocks Data Acquisition Module")
    print("=" * 60)
    
    # Health check
    health = health_check()
    print(f"Health Status: {health['status']}")
    print(f"Fyers Available: {health['fyers_available']}")
    print(f"Fyers Connection: {health['fyers_connection']}")
    print(f"CCXT Available: {health['ccxt_available']}")
    
    # Test Fyers connection
    print("\n🔌 Testing Fyers API connection...")
    if test_fyers_connection():
        print("✅ Fyers API connection successful")
    else:
        print("❌ Fyers API connection failed")
        print("Please check your access_token.py file and ensure it's up to date")
    
    # Test stock data (Fyers)
    print("\n📊 Testing NSE stock data (Fyers API)...")
    stock_data = fetch_data("RELIANCE", "NSE", "5m", 10, data_source="fyers")
    if not stock_data.empty:
        stock_data = add_ist_datetime(stock_data)
        print(f"✅ Stock data fetched: {len(stock_data)} bars")
        print(f"📅 Latest timestamp: {stock_data['timestamp'].iloc[-1]}")
        print(f"💰 Latest close: ₹{stock_data['close'].iloc[-1]:.2f}")
        print(f"📊 Volume: {stock_data['volume'].iloc[-1]:,.0f}")
    else:
        print("❌ Failed to fetch stock data")
    
    # Test live quote
    print("\n💹 Testing live quote...")
    quote = get_live_quote("RELIANCE", "NSE")
    if quote:
        print(f"✅ Live quote fetched")
        print(f"💰 LTP: ₹{quote['ltp']:.2f}")
        print(f"📊 Change: {quote['change']:.2f} ({quote['change_percent']:.2f}%)")
    else:
        print("❌ Failed to fetch live quote")
    
    # Test crypto data (CCXT)
    print("\n🪙 Testing crypto data (CCXT)...")
    crypto_data = fetch_data("BTC/USDT", "kraken", "5m", 10, data_source="ccxt")
    if not crypto_data.empty:
        crypto_data = add_ist_datetime(crypto_data)
        print(f"✅ Crypto data fetched: {len(crypto_data)} bars")
        print(f"📅 Latest timestamp: {crypto_data['timestamp'].iloc[-1]}")
        print(f"💰 Latest close: ${crypto_data['close'].iloc[-1]:,.2f}")
        print(f"📊 Volume: {crypto_data['volume'].iloc[-1]:,.2f}")
    else:
        print("❌ Failed to fetch crypto data")
    
    print("\n🎉 Testing completed!")
