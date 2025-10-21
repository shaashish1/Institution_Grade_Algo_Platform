"""
Market Data API Router
Handles real-time market data, quotes, and trading information

DATA ARCHITECTURE:
- PRIMARY: NSE Free Provider (no credentials needed) - for market quotes and indices
- SECONDARY: FYERS Provider (credentials required) - ONLY for actual trading operations

This allows development and testing without FYERS API subscription.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

# ===== FREE NSE DATA PROVIDER (PRIMARY - NO CREDENTIALS NEEDED) =====
# This provides real-time NSE market data without any configuration
try:
    from stocks.nse_free_data_provider import NSEFreeDataProvider
    nse_provider = NSEFreeDataProvider()
    logger.info("✅ NSE Free Data Provider loaded successfully (NO CONFIG NEEDED)")
except Exception as e:
    logger.error(f"❌ Failed to load NSE Free Provider: {e}")
    nse_provider = None

# ===== FYERS PROVIDER (SECONDARY - ONLY FOR TRADING) =====
# This is OPTIONAL and only needed for actual order execution
# Market data will work fine without FYERS credentials
try:
    from stocks.fyers_data_provider import FyersDataProvider
    fyers_provider = FyersDataProvider()
    logger.info("✅ FYERS Provider loaded (for trading operations)")
except ImportError as e:
    logger.warning(f"FYERS provider not installed: {e}")
    fyers_provider = None
except ValueError as e:
    logger.warning(f"FYERS credentials not configured: {e}")
    logger.info("ℹ️  Market data will use FREE NSE provider. FYERS only needed for trading.")
    fyers_provider = None
except Exception as e:
    logger.warning(f"Could not initialize FYERS provider: {e}")
    fyers_provider = None

# Import FYERS data service (for trading operations)
try:
    from api.fyers_data_service import fyers_data_service, get_market_data, get_nifty_option_chain
except ImportError:
    try:
        from fyers_data_service import fyers_data_service, get_market_data, get_nifty_option_chain
    except ImportError:
        logger.warning("FYERS data service not available - trading features disabled")
        # Create dummy functions
        def get_market_data():
            return {"indices": {}, "market_status": {"is_open": False}}
        def get_nifty_option_chain(expiry="current"):
            return {"data": []}

router = APIRouter(prefix="/api/market", tags=["Market Data"])

# Data Models
class QuoteRequest(BaseModel):
    symbols: List[str]
    exchange: str = "NSE"

class HistoricalDataRequest(BaseModel):
    symbol: str
    resolution: str = "5"
    bars: int = 100
    exchange: str = "NSE"

# Endpoints
@router.get("/health")
async def health_check():
    """Health check for market data service"""
    try:
        # Test if we can get market data
        data = get_market_data()
        return {
            "status": "ok",
            "message": "Market data service is operational",
            "market_status": data.get("market_status", {})
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/data")
async def get_comprehensive_market_data():
    """
    Get comprehensive market data including NIFTY, Bank NIFTY, and market status
    Returns cached data when market is closed
    """
    try:
        data = get_market_data()
        return data
    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quotes")
async def get_quotes(request: QuoteRequest):
    """
    Get real-time quotes for multiple symbols from FREE NSE data source
    NO CREDENTIALS NEEDED!
    
    Example request:
    ```json
    {
        "symbols": ["RELIANCE", "TCS", "INFY"],
        "exchange": "NSE"
    }
    ```
    
    Data Source Priority:
    1. NSE Free Provider (real-time NSE data - NO CONFIG)
    2. FYERS Provider (if configured - for trading)
    """
    try:
        # PRIMARY: Use FREE NSE provider (no credentials needed)
        if nse_provider:
            quotes = nse_provider.get_quote(request.symbols, request.exchange)
            logger.info(f"✅ Fetched quotes for {len(quotes)} symbols from FREE NSE provider")
            return quotes
        
        # SECONDARY: Use FYERS if NSE provider fails (requires credentials)
        elif fyers_provider:
            quotes = {}
            for symbol in request.symbols:
                quote = fyers_provider.get_quote(symbol, request.exchange)
                if quote:
                    quotes[symbol] = quote
            logger.info(f"Fetched quotes using FYERS provider")
            return quotes
        
        # FALLBACK: Return error if both providers unavailable
        else:
            raise HTTPException(
                status_code=503, 
                detail="No data provider available. Please check NSE provider initialization."
            )
    
    except Exception as e:
        logger.error(f"Error fetching quotes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/historical")
async def get_historical(request: HistoricalDataRequest):
    """
    Get historical OHLCV data for a symbol
    
    Example request:
    ```json
    {
        "symbol": "RELIANCE",
        "resolution": "5",
        "bars": 100,
        "exchange": "NSE"
    }
    ```
    
    Resolution options: 1, 5, 15, 30, 60, 120, 240, 1D
    """
    try:
        if not fyers_provider:
            # Return empty data if provider not available
            return []
        
        # Use FYERS provider for historical data
        data = fyers_provider.get_historical_data(
            symbol=request.symbol,
            resolution=request.resolution,
            bars=request.bars,
            exchange=request.exchange
        )
        
        if data is None or data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for {request.symbol}")
        
        # Convert DataFrame to list of dicts
        data_dict = data.to_dict(orient='records')
        return data_dict
    
    except Exception as e:
        logger.error(f"Error fetching historical data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/indices")
async def get_indices():
    """
    Get current values of major indices (NIFTY 50, BANK NIFTY, etc.)
    Uses FREE NSE data - NO CREDENTIALS NEEDED!
    """
    try:
        # PRIMARY: Use FREE NSE provider
        if nse_provider:
            indices_data = nse_provider.get_nifty_indices()
            
            # Convert to frontend format
            indices = []
            for symbol, data in indices_data.items():
                indices.append({
                    "symbol": data.get("symbol", symbol),
                    "price": data.get("ltp", 0),
                    "change": data.get("change", 0),
                    "change_percent": data.get("change_percent", 0),
                    "high": data.get("high", 0),
                    "low": data.get("low", 0),
                    "open": data.get("open", 0),
                    "previous_close": data.get("close", 0),
                    "data_source": data.get("data_source", "NSE_FREE")
                })
            
            # Get market status
            market_status = nse_provider.get_market_status()
            
            logger.info(f"✅ Fetched {len(indices)} indices from FREE NSE provider")
            
            return {
                "indices": indices,
                "market_status": market_status,
                "data_source": "NSE_FREE"
            }
        
        # FALLBACK: Try to use legacy method if NSE provider unavailable
        else:
            logger.warning("NSE provider not available, using fallback")
            data = get_market_data()
            
            indices = []
            if "indices" in data:
                for key, value in data["indices"].items():
                    indices.append({
                        "symbol": value.get("symbol", key),
                        "price": value.get("price", 0),
                        "change": value.get("change", 0),
                        "change_percent": value.get("change_percent", 0),
                        "high": value.get("high", 0),
                        "low": value.get("low", 0),
                        "open": value.get("open", 0),
                        "previous_close": value.get("previous_close", 0)
                    })
            
            return {
                "indices": indices,
                "market_status": data.get("market_status", {}),
                "data_source": "FALLBACK"
            }
    
    except Exception as e:
        logger.error(f"Error fetching indices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_market_status():
    """Get current market status (open/closed) - FREE NSE data"""
    try:
        if nse_provider:
            return nse_provider.get_market_status()
        else:
            data = get_market_data()
            return data.get("market_status", {
                "is_open": False,
                "status": "unknown",
                "message": "Unable to determine market status"
            })
    except Exception as e:
        logger.error(f"Error fetching market status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/provider-status")
async def get_provider_status():
    """
    Check which data providers are available
    Helps users understand configuration status
    """
    return {
        "nse_free_provider": {
            "available": nse_provider is not None,
            "status": "active" if nse_provider else "unavailable",
            "requires_config": False,
            "description": "Free NSE data for market quotes and indices",
            "use_case": "Market data, quotes, indices (NO credentials needed)"
        },
        "fyers_provider": {
            "available": fyers_provider is not None,
            "status": "active" if fyers_provider else "not_configured",
            "requires_config": True,
            "description": "FYERS API for trading operations",
            "use_case": "Order execution, positions, historical data (credentials required)"
        },
        "recommendation": "Market data works without FYERS. Configure FYERS only when ready to trade."
    }

@router.get("/option-chain")
async def get_option_chain(expiry: str = "current"):
    """
    Get NIFTY option chain data
    
    Parameters:
    - expiry: "current", "next", or specific date (YYYY-MM-DD)
    """
    try:
        data = get_nifty_option_chain(expiry)
        return data
    except Exception as e:
        logger.error(f"Error fetching option chain: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Mock positions endpoint (to be replaced with real FYERS positions)
@router.get("/positions")
async def get_positions():
    """
    Get current open positions
    Note: This is a mock endpoint. Real implementation requires FYERS API authentication
    """
    try:
        # Mock data - replace with real FYERS API call
        return {
            "positions": [
                {
                    "symbol": "RELIANCE",
                    "quantity": 50,
                    "buy_price": 2450.00,
                    "current_price": 2478.50,
                    "pnl": 1425.00,
                    "pnl_percent": 1.16
                },
                {
                    "symbol": "TCS",
                    "quantity": 30,
                    "buy_price": 3650.00,
                    "current_price": 3625.00,
                    "pnl": -750.00,
                    "pnl_percent": -0.68
                },
                {
                    "symbol": "INFY",
                    "quantity": 100,
                    "buy_price": 1550.00,
                    "current_price": 1568.00,
                    "pnl": 1800.00,
                    "pnl_percent": 1.16
                }
            ],
            "total_pnl": 2475.00,
            "message": "Mock data - configure FYERS credentials for real positions"
        }
    except Exception as e:
        logger.error(f"Error fetching positions: {e}")
        raise HTTPException(status_code=500, detail=str(e))
