"""
Market Data API Router
Handles real-time market data, quotes, and trading information
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import FYERS data service
from fyers_data_service import fyers_data_service, get_market_data, get_nifty_option_chain

# Import stocks data acquisition for live quotes
try:
    from stocks.data_acquisition import get_live_quote
    from stocks.fyers_data_provider import FyersDataProvider
    fyers_provider = FyersDataProvider()
except ImportError as e:
    logging.warning(f"Fyers provider not available: {e}")
    fyers_provider = None
    fyers_provider = None

logger = logging.getLogger(__name__)

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
    Get real-time quotes for multiple symbols
    
    Example request:
    ```json
    {
        "symbols": ["RELIANCE", "TCS", "INFY"],
        "exchange": "NSE"
    }
    ```
    """
    try:
        if not fyers_provider:
            # Return mock data if provider not available
            mock_quotes = {}
            for symbol in request.symbols:
                mock_quotes[symbol] = {
                    "symbol": symbol,
                    "ltp": 1000.0 + (hash(symbol) % 1000),
                    "open": 995.0,
                    "high": 1025.0,
                    "low": 985.0,
                    "close": 998.0,
                    "volume": 1000000,
                    "change": 5.0,
                    "change_percent": 0.5
                }
            return mock_quotes
        
        # Check if FYERS provider is available
        if fyers_provider is None:
            raise HTTPException(status_code=503, detail="FYERS provider not available. Please check configuration.")
        
        # Use FYERS provider for real quotes
        quotes = fyers_provider.get_quote(request.symbols, request.exchange)
        
        if quotes is None:
            raise HTTPException(status_code=500, detail="Failed to fetch quotes from FYERS API")
        
        return quotes
    
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
    Get current values of major indices (NIFTY, Bank NIFTY, etc.)
    """
    try:
        data = get_market_data()
        
        indices = []
        
        # Extract index data
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
            "data_source": data.get("data_source", "unknown")
        }
    
    except Exception as e:
        logger.error(f"Error fetching indices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_market_status():
    """Get current market status (open/closed)"""
    try:
        data = get_market_data()
        return data.get("market_status", {
            "is_open": False,
            "status": "unknown",
            "message": "Unable to determine market status"
        })
    except Exception as e:
        logger.error(f"Error fetching market status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
