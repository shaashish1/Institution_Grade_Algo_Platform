"""
NSE Free Data Provider - Real-time NSE data without API credentials
Uses public NSE APIs and web scraping for free market data
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Optional, Dict, Any, List
import json

logger = logging.getLogger(__name__)

class NSEFreeDataProvider:
    """
    Free NSE data provider that doesn't require API credentials.
    Uses NSE public APIs for real-time quotes and historical data.
    
    Data Sources:
    1. NSE India official website APIs (public)
    2. Yahoo Finance India (backup)
    3. NSE indices data (NIFTY 50, BANK NIFTY, etc.)
    """
    
    def __init__(self):
        """Initialize NSE free data provider"""
        self.base_url = "https://www.nseindia.com/api"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        # Create session for cookies
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        # Get cookies by visiting homepage
        self._init_session()
        logger.info("✅ NSE Free Data Provider initialized")
    
    def _init_session(self):
        """Initialize session with NSE website to get cookies"""
        try:
            response = self.session.get("https://www.nseindia.com", timeout=10)
            logger.info(f"Session initialized: {response.status_code}")
        except Exception as e:
            logger.warning(f"Failed to initialize NSE session: {e}")
    
    def get_quote(self, symbols: List[str], exchange: str = "NSE") -> Dict[str, Any]:
        """
        Get real-time quotes for NSE stocks (FREE - no credentials needed)
        
        Args:
            symbols: List of stock symbols (e.g., ["RELIANCE", "TCS", "INFY"])
            exchange: Exchange name (NSE/BSE)
        
        Returns:
            Dictionary with quote data for each symbol
        """
        quotes = {}
        
        for symbol in symbols:
            try:
                quote_data = self._get_nse_quote(symbol)
                if quote_data:
                    quotes[symbol] = quote_data
                else:
                    # Fallback to Yahoo Finance
                    quotes[symbol] = self._get_yahoo_quote(symbol)
            except Exception as e:
                logger.error(f"Error fetching quote for {symbol}: {e}")
                quotes[symbol] = self._get_mock_quote(symbol)
        
        return quotes
    
    def _get_nse_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get quote from NSE official API
        Endpoint: https://www.nseindia.com/api/quote-equity?symbol=RELIANCE
        """
        try:
            url = f"{self.base_url}/quote-equity?symbol={symbol}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                price_info = data.get('priceInfo', {})
                
                return {
                    'symbol': symbol,
                    'ltp': price_info.get('lastPrice', 0),
                    'open': price_info.get('open', 0),
                    'high': price_info.get('intraDayHighLow', {}).get('max', 0),
                    'low': price_info.get('intraDayHighLow', {}).get('min', 0),
                    'close': price_info.get('previousClose', 0),
                    'volume': data.get('securityWiseDP', {}).get('quantityTraded', 0),
                    'change': price_info.get('change', 0),
                    'change_percent': price_info.get('pChange', 0),
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'NSE_FREE'
                }
        except Exception as e:
            logger.error(f"NSE API error for {symbol}: {e}")
            return None
    
    def _get_yahoo_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Fallback: Get quote from Yahoo Finance India
        """
        try:
            yahoo_symbol = f"{symbol}.NS"  # NSE suffix for Yahoo
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                result = data['chart']['result'][0]
                meta = result['meta']
                quote = result['indicators']['quote'][0]
                
                return {
                    'symbol': symbol,
                    'ltp': meta.get('regularMarketPrice', 0),
                    'open': quote.get('open', [0])[-1] if quote.get('open') else 0,
                    'high': quote.get('high', [0])[-1] if quote.get('high') else 0,
                    'low': quote.get('low', [0])[-1] if quote.get('low') else 0,
                    'close': meta.get('previousClose', 0),
                    'volume': quote.get('volume', [0])[-1] if quote.get('volume') else 0,
                    'change': meta.get('regularMarketPrice', 0) - meta.get('previousClose', 0),
                    'change_percent': ((meta.get('regularMarketPrice', 0) - meta.get('previousClose', 0)) / meta.get('previousClose', 1)) * 100,
                    'timestamp': datetime.now().isoformat(),
                    'data_source': 'YAHOO_FINANCE'
                }
        except Exception as e:
            logger.error(f"Yahoo Finance error for {symbol}: {e}")
            return self._get_mock_quote(symbol)
    
    def _get_mock_quote(self, symbol: str) -> Dict[str, Any]:
        """Generate mock quote as last resort"""
        base_price = 1000.0 + (hash(symbol) % 2000)
        return {
            'symbol': symbol,
            'ltp': base_price,
            'open': base_price * 0.995,
            'high': base_price * 1.025,
            'low': base_price * 0.985,
            'close': base_price * 0.998,
            'volume': 1000000,
            'change': base_price * 0.005,
            'change_percent': 0.5,
            'timestamp': datetime.now().isoformat(),
            'data_source': 'MOCK'
        }
    
    def get_nifty_indices(self) -> Dict[str, Any]:
        """
        Get NIFTY indices data (NIFTY 50, BANK NIFTY, etc.)
        FREE - No credentials needed
        """
        try:
            url = f"{self.base_url}/allIndices"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                indices = {}
                
                for index_data in data.get('data', []):
                    index_name = index_data.get('index')
                    if index_name in ['NIFTY 50', 'NIFTY BANK', 'NIFTY FIN SERVICE', 'NIFTY IT']:
                        indices[index_name] = {
                            'symbol': index_name,
                            'ltp': index_data.get('last', 0),
                            'open': index_data.get('open', 0),
                            'high': index_data.get('high', 0),
                            'low': index_data.get('low', 0),
                            'close': index_data.get('previousClose', 0),
                            'change': index_data.get('last', 0) - index_data.get('previousClose', 0),
                            'change_percent': index_data.get('percentChange', 0),
                            'timestamp': datetime.now().isoformat(),
                            'data_source': 'NSE_FREE'
                        }
                
                return indices
        except Exception as e:
            logger.error(f"Error fetching NIFTY indices: {e}")
            return self._get_mock_indices()
    
    def _get_mock_indices(self) -> Dict[str, Any]:
        """Generate mock indices data"""
        return {
            'NIFTY 50': {
                'symbol': 'NIFTY 50',
                'ltp': 19850.25,
                'open': 19800.00,
                'high': 19900.50,
                'low': 19750.00,
                'close': 19725.75,
                'change': 124.50,
                'change_percent': 0.63,
                'timestamp': datetime.now().isoformat(),
                'data_source': 'MOCK'
            },
            'NIFTY BANK': {
                'symbol': 'BANK NIFTY',
                'ltp': 44250.75,
                'open': 44300.00,
                'high': 44400.25,
                'low': 44150.50,
                'close': 44336.00,
                'change': -85.25,
                'change_percent': -0.19,
                'timestamp': datetime.now().isoformat(),
                'data_source': 'MOCK'
            }
        }
    
    def get_top_gainers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top gainers from NSE"""
        try:
            url = f"{self.base_url}/live-analysis-variations?index=gainers"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                gainers = []
                
                for item in data.get('NIFTY', {}).get('data', [])[:limit]:
                    gainers.append({
                        'symbol': item.get('symbol'),
                        'ltp': item.get('lastPrice', 0),
                        'change': item.get('change', 0),
                        'change_percent': item.get('pChange', 0),
                        'volume': item.get('totalTradedVolume', 0)
                    })
                
                return gainers
        except Exception as e:
            logger.error(f"Error fetching top gainers: {e}")
            return []
    
    def get_top_losers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top losers from NSE"""
        try:
            url = f"{self.base_url}/live-analysis-variations?index=losers"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                losers = []
                
                for item in data.get('NIFTY', {}).get('data', [])[:limit]:
                    losers.append({
                        'symbol': item.get('symbol'),
                        'ltp': item.get('lastPrice', 0),
                        'change': item.get('change', 0),
                        'change_percent': item.get('pChange', 0),
                        'volume': item.get('totalTradedVolume', 0)
                    })
                
                return losers
        except Exception as e:
            logger.error(f"Error fetching top losers: {e}")
            return []
    
    def get_market_status(self) -> Dict[str, Any]:
        """Get NSE market status (open/closed)"""
        try:
            url = f"{self.base_url}/marketStatus"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                market_state = data.get('marketState', [])
                
                for market in market_state:
                    if market.get('market') == 'Capital Market':
                        return {
                            'market': 'NSE',
                            'status': market.get('marketStatus'),
                            'timestamp': datetime.now().isoformat()
                        }
            
            return {
                'market': 'NSE',
                'status': 'UNKNOWN',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching market status: {e}")
            return {
                'market': 'NSE',
                'status': 'ERROR',
                'timestamp': datetime.now().isoformat()
            }


# Singleton instance
nse_free_provider = NSEFreeDataProvider()
