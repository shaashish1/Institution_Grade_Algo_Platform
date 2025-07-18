"""
Crypto Data Acquisition Module for AlgoProject
- Crypto Data: Uses CCXT for multiple exchanges
- Pure crypto module - NO stock market dependencies
"""

import pandas as pd
import threading
import os
import warnings
import logging
from datetime import datetime

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy import CCXT to avoid hanging on module load
ccxt = None

def _ensure_ccxt():
    """Ensure CCXT is imported when needed"""
    global ccxt
    if ccxt is None:
        try:
            import ccxt as _ccxt
            ccxt = _ccxt
            logger.info("CCXT imported successfully")
        except ImportError as e:
            logger.error(f"Failed to import CCXT: {e}")
            raise
        except Exception as e:
            logger.error(f"Error importing CCXT: {e}")
            raise
    return ccxt


def fetch_data(symbol, exchange, interval, bars, data_source="auto", fetch_timeout=15):
    """
    Crypto-specific data fetching function using CCXT only.
    
    Args:
        symbol (str): Trading symbol (e.g., "BTC/USDT", "ETH/USDT")
        exchange (str): Exchange name (e.g., "kraken", "binance", "coinbase")
        interval (str): Time interval (e.g., "5m", "1h", "1d")
        bars (int): Number of historical bars to fetch
        data_source (str): Always "ccxt" for crypto (maintained for compatibility)
        fetch_timeout (int): Timeout in seconds for data fetching
    
    Returns:
        pandas.DataFrame: OHLCV data with columns [timestamp, open, high, low, close, volume]
    """
    
    # Always use CCXT for crypto data
    return _fetch_ccxt_data(symbol, exchange, interval, bars, fetch_timeout)


def _fetch_ccxt_data(symbol, exchange, interval, bars, fetch_timeout=15):
    """
    Fetch crypto data using CCXT library.
    
    Args:
        symbol (str): Trading symbol (e.g., "BTC/USDT")
        exchange (str): Exchange name (e.g., "kraken", "binance")
        interval (str): Time interval (e.g., "5m", "1h", "1d")
        bars (int): Number of historical bars to fetch
        fetch_timeout (int): Timeout in seconds
    
    Returns:
        pandas.DataFrame: OHLCV data
    """
    
    try:
        # Ensure CCXT is available
        ccxt_lib = _ensure_ccxt()
        
        # Validate bars parameter
        if bars <= 0:
            logger.warning(f"Invalid bars parameter: {bars}. Must be positive.")
            return None
            
        # Validate symbol format
        if '/' not in symbol:
            logger.warning(f"Invalid symbol format: {symbol}. Expected format: BASE/QUOTE")
            return None
            
        # Initialize exchange with better error handling
        try:
            exchange_class = getattr(ccxt_lib, exchange.lower())
        except AttributeError:
            logger.error(f"Exchange {exchange} not supported by CCXT")
            return None
            
        exchange_instance = exchange_class({
            'apiKey': '',
            'secret': '',
            'timeout': fetch_timeout * 1000,
            'enableRateLimit': True,
            'sandbox': False,  # Ensure production mode
        })

        # Load markets first to validate symbol
        try:
            markets = exchange_instance.load_markets()
            if symbol not in markets:
                logger.warning(f"Symbol {symbol} not available on {exchange}")
                return None
        except Exception as e:
            logger.warning(f"Could not load markets for {exchange}: {e}")
            # Continue anyway, symbol might still work

        # Fetch OHLCV data
        ohlcv = exchange_instance.fetch_ohlcv(symbol, interval, limit=bars)
        
        if not ohlcv:
            logger.warning(f"No data received for {symbol} from {exchange}")
            return None

        # Convert to DataFrame
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        # Sort by timestamp
        df.sort_index(inplace=True)
        
        # Validate data quality
        if len(df) == 0:
            logger.warning(f"Empty dataset returned for {symbol} from {exchange}")
            return None
            
        # Check for missing values
        if df.isnull().any().any():
            logger.warning(f"Dataset contains missing values for {symbol}")
            # Fill forward missing values
            df.fillna(method='ffill', inplace=True)
        
        logger.info(f"Successfully fetched {len(df)} bars for {symbol} from {exchange}")
        return df

    except Exception as e:
        logger.error(f"Error fetching crypto data for {symbol} from {exchange}: {e}")
        return None


def get_available_exchanges():
    """
    Get list of available CCXT exchanges.
    
    Returns:
        list: List of available exchange names
    """
    try:
        ccxt_lib = _ensure_ccxt()
        exchanges = ccxt_lib.exchanges
        # Filter out exchanges that might not work well
        working_exchanges = ['binance', 'kraken', 'coinbase', 'bitfinex', 'kucoin', 'huobi']
        available = [ex for ex in working_exchanges if ex in exchanges]
        return available
    except Exception as e:
        logger.error(f"Error getting exchanges: {e}")
        return ['kraken', 'binance']  # Default fallback


def test_exchange_connection(exchange_name):
    """
    Test connection to a specific exchange.
    
    Args:
        exchange_name (str): Name of the exchange to test
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        ccxt_lib = _ensure_ccxt()
        exchange_class = getattr(ccxt_lib, exchange_name.lower())
        exchange_instance = exchange_class({
            'timeout': 10000,
            'enableRateLimit': True,
        })
        
        # Try to fetch markets (doesn't require authentication)
        markets = exchange_instance.load_markets()
        logger.info(f"Successfully connected to {exchange_name} - {len(markets)} markets available")
        return True
        
    except Exception as e:
        logger.warning(f"Failed to connect to {exchange_name}: {e}")
        return False


def get_crypto_symbols(exchange='kraken', limit=50):
    """
    Get available crypto trading symbols from an exchange.
    
    Args:
        exchange (str): Exchange name
        limit (int): Maximum number of symbols to return
    
    Returns:
        list: List of trading symbols
    """
    try:
        ccxt_lib = _ensure_ccxt()
        exchange_class = getattr(ccxt_lib, exchange.lower())
        exchange_instance = exchange_class({
            'timeout': 15000,
            'enableRateLimit': True,
        })
        
        markets = exchange_instance.load_markets()
        
        # Filter for USDT pairs (most liquid)
        usdt_pairs = [symbol for symbol in markets.keys() if '/USDT' in symbol]
        
        # Sort by popularity (BTC, ETH first)
        priority_coins = ['BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'DOT/USDT', 'SOL/USDT']
        result = []
        
        # Add priority coins first
        for coin in priority_coins:
            if coin in usdt_pairs:
                result.append(coin)
        
        # Add remaining coins
        for symbol in usdt_pairs:
            if symbol not in result and len(result) < limit:
                result.append(symbol)
        
        logger.info(f"Found {len(result)} crypto symbols on {exchange}")
        return result[:limit]
        
    except Exception as e:
        logger.error(f"Error getting crypto symbols from {exchange}: {e}")
        # Return default symbols as fallback
        return ['BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'DOT/USDT', 'SOL/USDT']


# Health check function
def health_check():
    """
    Perform health check on crypto data acquisition module.
    
    Returns:
        dict: Health check results
    """
    results = {
        'module': 'crypto.data_acquisition',
        'ccxt_available': False,
        'exchanges_tested': [],
        'working_exchanges': [],
        'status': 'unknown'
    }
    
    try:
        # Check CCXT availability
        ccxt_lib = _ensure_ccxt()
        results['ccxt_available'] = True
        
        # Test a few exchanges with timeout
        test_exchanges = ['kraken', 'binance']
        for exchange in test_exchanges:
            results['exchanges_tested'].append(exchange)
            try:
                # Quick connection test with timeout
                ccxt_lib = _ensure_ccxt()
                exchange_class = getattr(ccxt_lib, exchange.lower())
                exchange_instance = exchange_class({
                    'timeout': 5000,  # 5 second timeout
                    'enableRateLimit': True,
                })
                
                # Try to load markets with timeout
                markets = exchange_instance.load_markets()
                if markets:
                    results['working_exchanges'].append(exchange)
                    
            except Exception as e:
                logger.warning(f"Exchange {exchange} failed health check: {e}")
                continue
        
        if results['working_exchanges']:
            results['status'] = 'healthy'
        else:
            results['status'] = 'degraded'
            
    except Exception as e:
        results['status'] = 'error'
        results['error'] = str(e)
    
    return results


if __name__ == "__main__":
    # Test the module
    print("Testing Crypto Data Acquisition Module")
    print("=" * 50)
    
    # Health check
    health = health_check()
    print(f"Health Status: {health['status']}")
    print(f"CCXT Available: {health['ccxt_available']}")
    print(f"Working Exchanges: {health['working_exchanges']}")
    
    if health['working_exchanges']:
        # Test data fetch
        print("\nTesting data fetch...")
        exchange = health['working_exchanges'][0]
        data = fetch_data('BTC/USDT', exchange, '1h', 24)
        if data is not None:
            print(f"✅ Successfully fetched {len(data)} bars from {exchange}")
            print(data.tail())
        else:
            print("❌ Failed to fetch data")
