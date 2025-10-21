from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
import uvicorn
from datetime import datetime
import traceback
import sys

app = FastAPI(
    title="AlgoProject Trading API",
    description="""
    ## AlgoProject Trading Platform API
    
    A comprehensive trading platform API supporting both NSE (Indian Stock Market) and Cryptocurrency trading.
    
    ### Features:
    - 📈 **NSE Trading**: NIFTY 50/100 stocks, real-time market data
    - 🚀 **Crypto Trading**: Multiple exchanges, live price feeds  
    - 🤖 **AI Recommendations**: Intelligent strategy suggestions
    - 📊 **Backtesting**: Historical performance analysis
    - ⚡ **Real-time Data**: WebSocket connections for live updates
    
    ### API Sections:
    - **NSE**: Indian stock market data and trading
    - **Crypto**: Cryptocurrency market data and trading
    - **AI**: Machine learning powered recommendations
    - **Backtest**: Strategy testing and performance analysis
    """,
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handling middleware
@app.middleware("http")
async def catch_exceptions(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"Error processing request: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(e)}"}
        )

# Basic health check
@app.get("/", tags=["System"])
async def root():
    try:
        return {
            "message": "AlgoProject API v1.0.0",
            "status": "running",
            "endpoints": {
                "health": "/health",
                "docs": "/docs",
                "nse": "/api/nse/*",
                "crypto": "/api/crypto/*",
                "ai": "/api/ai/*",
                "backtest": "/api/backtest/*"
            },
            "timestamp": datetime.now().isoformat(),
            "python_version": sys.version
        }
    except Exception as e:
        print(f"Error in root endpoint: {e}")
        return {"error": str(e), "status": "error"}

@app.get("/health", tags=["System"])
async def health_check():
    """System health check endpoint"""
    try:
        return {"status": "healthy", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        print(f"Error in health endpoint: {e}")
        return {"error": str(e), "status": "error"}

# NSE API Endpoints
@app.get("/api/nse/symbols", tags=["NSE"])
async def get_nse_symbols():
    """Get available NSE symbols for NIFTY 50 and NIFTY 100"""
    try:
        return {
            "NIFTY50": [
                "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", 
                "BHARTIARTL", "SBIN", "LT", "AXISBANK", "MARUTI",
                "HINDUNILVR", "KOTAKBANK", "ASIANPAINT", "NESTLEIND", "HCLTECH"
            ],
            "NIFTY100": [
                "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", 
                "BHARTIARTL", "SBIN", "LT", "AXISBANK", "MARUTI",
                "HINDUNILVR", "KOTAKBANK", "ASIANPAINT", "NESTLEIND", "HCLTECH",
                "ADANIPORTS", "BAJFINANCE", "GODREJCP", "MARICO", "PIDILITIND"
            ]
        }
    except Exception as e:
        print(f"Error in NSE symbols endpoint: {e}")
        return {"error": str(e)}

@app.get("/api/nse/market-data", tags=["NSE"])
async def get_nse_market_data():
    """Get real-time NSE market data including indices, gainers, and losers"""
    try:
        return {
            "indices": {
                "NIFTY50": {"price": 21580.25, "change": 123.45, "change_percent": 0.57},
                "BANKNIFTY": {"price": 48750.80, "change": -234.20, "change_percent": -0.48}
            },
            "top_gainers": ["BHARTIARTL", "RELIANCE", "TCS"],
            "top_losers": ["INFY", "ICICIBANK", "MARUTI"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error in NSE market data endpoint: {e}")
        return {"error": str(e)}

# Crypto API Endpoints  
@app.get("/api/crypto/symbols", tags=["Crypto"])
async def get_crypto_symbols():
    """Get available cryptocurrency trading pairs"""
    try:
        return {
            "major_pairs": ["BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT"],
            "altcoins": ["MATIC/USDT", "DOT/USDT", "LINK/USDT", "UNI/USDT", "SOL/USDT"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error in crypto symbols endpoint: {e}")
        return {"error": str(e)}

@app.get("/api/crypto/market-data", tags=["Crypto"])
async def get_crypto_market_data():
    """Get real-time cryptocurrency market data and prices"""
    try:
        return {
            "prices": {
                "BTC/USDT": {"price": 67500.50, "change": 1250.30, "change_percent": 1.89},
                "ETH/USDT": {"price": 3890.75, "change": -45.25, "change_percent": -1.15}
            },
            "market_cap": 2_450_000_000_000,
            "total_volume": 98_500_000_000,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error in crypto market data endpoint: {e}")
        return {"error": str(e)}

@app.post("/api/backtest/run", tags=["Backtest"])
async def run_backtest(data: Dict[str, Any]):
    """Run a backtest with specified parameters"""
    try:
        # Mock backtest results
        return {
            "success": True,
            "results": {
                "totalTrades": 150,
                "winRate": 67.3,
                "totalPnL": 185750,
                "sharpeRatio": 2.34
            }
        }
    except Exception as e:
        print(f"Error in backtest endpoint: {e}")
        return {"error": str(e)}

@app.get("/api/ai/recommendations", tags=["AI"])
async def get_ai_recommendations():
    """Get AI-powered trading strategy recommendations"""
    try:
        return {
            "recommendations": [
                {
                    "strategy": "momentum",
                    "timeframe": "1D",
                    "confidence": 87,
                    "reason": "Strong upward momentum detected",
                    "expectedReturn": 12.5,
                    "risk": "MEDIUM"
                }
            ]
        }
    except Exception as e:
        print(f"Error in AI recommendations endpoint: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("simple_api_fixed:app", host="0.0.0.0", port=3001, reload=True)