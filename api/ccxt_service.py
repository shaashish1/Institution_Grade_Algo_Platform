"""
CCXT Service for Exchange Integration
Provides tiered authentication:
- No credentials: Backtest and Paper Trading
- With credentials: Live Trading
"""

import logging
from typing import Dict, Optional, Any, List
from dataclasses import dataclass
from enum import Enum
import asyncio

# Configure logging
logger = logging.getLogger(__name__)

class TradingMode(Enum):
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"

@dataclass
class ExchangeCredentials:
    api_key: str
    secret: str
    passphrase: Optional[str] = None  # For exchanges like OKX, KuCoin
    sandbox: bool = True

@dataclass
class ExchangeConfig:
    exchange_id: str
    trading_mode: TradingMode
    credentials: Optional[ExchangeCredentials] = None
    rate_limit: int = 1000  # milliseconds
    timeout: int = 30000  # milliseconds

class CCXTService:
    """CCXT Service with tiered authentication support"""
    
    def __init__(self):
        self.ccxt = None
        self.exchanges: Dict[str, Any] = {}
        self.supported_exchanges = [
            'binance', 'coinbase', 'kraken', 'kucoin', 
            'okx', 'bybit', 'bitfinex', 'huobi', 'gate'
        ]
    
    def _ensure_ccxt(self):
        """Lazy load CCXT library"""
        if self.ccxt is None:
            try:
                import ccxt
                self.ccxt = ccxt
                logger.info("✅ CCXT library loaded successfully")
            except ImportError as e:
                logger.error(f"❌ Failed to import CCXT: {e}")
                raise RuntimeError("CCXT library not available")
        return self.ccxt
    
    async def initialize_exchange(self, config: ExchangeConfig) -> bool:
        """
        Initialize exchange based on trading mode and credentials
        
        Args:
            config: Exchange configuration
            
        Returns:
            bool: True if initialization successful
        """
        try:
            ccxt_lib = self._ensure_ccxt()
            
            # Validate exchange support
            if config.exchange_id not in self.supported_exchanges:
                logger.error(f"❌ Exchange {config.exchange_id} not supported")
                return False
            
            # Get exchange class
            exchange_class = getattr(ccxt_lib, config.exchange_id)
            
            # Base configuration
            exchange_config = {
                'enableRateLimit': True,
                'rateLimit': config.rate_limit,
                'timeout': config.timeout,
                'sandbox': True,  # Default to sandbox
            }
            
            # Configure based on trading mode
            if config.trading_mode == TradingMode.BACKTEST:
                # Backtest mode: No credentials needed, public data only
                logger.info(f"🔍 Initializing {config.exchange_id} for BACKTEST mode (no credentials)")
                exchange_config.update({
                    'sandbox': True,
                    'headers': {'User-Agent': 'AlgoProject-Backtest/1.0'}
                })
                
            elif config.trading_mode == TradingMode.PAPER:
                # Paper trading: No credentials needed, public data only
                logger.info(f"📄 Initializing {config.exchange_id} for PAPER trading (no credentials)")
                exchange_config.update({
                    'sandbox': True,
                    'headers': {'User-Agent': 'AlgoProject-Paper/1.0'}
                })
                
            elif config.trading_mode == TradingMode.LIVE:
                # Live trading: Credentials required
                if not config.credentials:
                    logger.error(f"❌ LIVE trading requires API credentials for {config.exchange_id}")
                    return False
                
                logger.info(f"🔴 Initializing {config.exchange_id} for LIVE trading (with credentials)")
                exchange_config.update({
                    'apiKey': config.credentials.api_key,
                    'secret': config.credentials.secret,
                    'sandbox': config.credentials.sandbox,
                    'headers': {'User-Agent': 'AlgoProject-Live/1.0'}
                })
                
                # Add passphrase for exchanges that require it
                if config.credentials.passphrase:
                    exchange_config['passphrase'] = config.credentials.passphrase
            
            # Initialize exchange
            exchange = exchange_class(exchange_config)
            
            # Test connection (public markets)
            try:
                markets = await asyncio.get_event_loop().run_in_executor(
                    None, exchange.load_markets
                )
                logger.info(f"✅ {config.exchange_id} connected - {len(markets)} markets loaded")
                
                # For live trading, test account access
                if config.trading_mode == TradingMode.LIVE:
                    await self._test_account_access(exchange, config.exchange_id)
                
                # Store exchange instance
                self.exchanges[config.exchange_id] = {
                    'instance': exchange,
                    'mode': config.trading_mode,
                    'markets': markets,
                    'initialized_at': asyncio.get_event_loop().time()
                }
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Failed to load markets for {config.exchange_id}: {e}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize {config.exchange_id}: {e}")
            return False
    
    async def _test_account_access(self, exchange, exchange_id: str):
        """Test account access for live trading"""
        try:
            balance = await asyncio.get_event_loop().run_in_executor(
                None, exchange.fetch_balance
            )
            logger.info(f"✅ {exchange_id} account access verified")
        except Exception as e:
            logger.warning(f"⚠️ {exchange_id} account access test failed: {e}")
            # Don't fail initialization, just log the warning
    
    def get_exchange(self, exchange_id: str) -> Optional[Any]:
        """Get initialized exchange instance"""
        return self.exchanges.get(exchange_id, {}).get('instance')
    
    def get_exchange_info(self, exchange_id: str) -> Optional[Dict]:
        """Get exchange information"""
        return self.exchanges.get(exchange_id)
    
    def is_live_trading_enabled(self, exchange_id: str) -> bool:
        """Check if exchange is configured for live trading"""
        exchange_info = self.exchanges.get(exchange_id)
        return exchange_info and exchange_info['mode'] == TradingMode.LIVE
    
    def requires_credentials(self, trading_mode: TradingMode) -> bool:
        """Check if trading mode requires credentials"""
        return trading_mode == TradingMode.LIVE
    
    async def get_market_data(self, exchange_id: str, symbol: str, timeframe: str, limit: int = 100) -> Optional[List]:
        """
        Get market data (OHLCV) - works for all trading modes
        
        Args:
            exchange_id: Exchange identifier
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Timeframe (e.g., '1h', '1d')
            limit: Number of candles to fetch
            
        Returns:
            List of OHLCV data or None if failed
        """
        try:
            exchange = self.get_exchange(exchange_id)
            if not exchange:
                logger.error(f"❌ Exchange {exchange_id} not initialized")
                return None
            
            # Fetch OHLCV data (public endpoint, no credentials needed)
            ohlcv = await asyncio.get_event_loop().run_in_executor(
                None, exchange.fetch_ohlcv, symbol, timeframe, None, limit
            )
            
            logger.info(f"📊 Fetched {len(ohlcv)} {timeframe} candles for {symbol} from {exchange_id}")
            return ohlcv
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch market data from {exchange_id}: {e}")
            return None
    
    async def place_order(self, exchange_id: str, symbol: str, order_type: str, 
                         side: str, amount: float, price: Optional[float] = None) -> Optional[Dict]:
        """
        Place trading order - only works in LIVE mode
        
        Args:
            exchange_id: Exchange identifier
            symbol: Trading pair
            order_type: 'market' or 'limit'
            side: 'buy' or 'sell'
            amount: Order amount
            price: Order price (for limit orders)
            
        Returns:
            Order info dict or None if failed
        """
        try:
            exchange_info = self.get_exchange_info(exchange_id)
            if not exchange_info:
                logger.error(f"❌ Exchange {exchange_id} not initialized")
                return None
            
            if exchange_info['mode'] != TradingMode.LIVE:
                logger.error(f"❌ Order placement requires LIVE trading mode. Current mode: {exchange_info['mode'].value}")
                return None
            
            exchange = exchange_info['instance']
            
            # Place order
            order = await asyncio.get_event_loop().run_in_executor(
                None, exchange.create_order, symbol, order_type, side, amount, price
            )
            
            logger.info(f"📝 Order placed on {exchange_id}: {side} {amount} {symbol} @ {price}")
            return order
            
        except Exception as e:
            logger.error(f"❌ Failed to place order on {exchange_id}: {e}")
            return None
    
    def get_supported_exchanges(self) -> List[str]:
        """Get list of supported exchanges"""
        return self.supported_exchanges.copy()
    
    def get_initialized_exchanges(self) -> List[str]:
        """Get list of initialized exchanges"""
        return list(self.exchanges.keys())
    
    def get_exchange_status(self, exchange_id: str) -> Dict[str, Any]:
        """Get detailed exchange status"""
        if exchange_id not in self.exchanges:
            return {
                'initialized': False,
                'trading_mode': None,
                'markets_count': 0,
                'live_trading_enabled': False,
                'credentials_required': False
            }
        
        exchange_info = self.exchanges[exchange_id]
        return {
            'initialized': True,
            'trading_mode': exchange_info['mode'].value,
            'markets_count': len(exchange_info['markets']),
            'live_trading_enabled': exchange_info['mode'] == TradingMode.LIVE,
            'credentials_required': self.requires_credentials(exchange_info['mode']),
            'initialized_at': exchange_info['initialized_at']
        }

# Global service instance
ccxt_service = CCXTService()