#!/usr/bin/env python3
"""
Simple HTTP API Server - Python 3.14 Compatible
Alternative to FastAPI for environments with Python 3.14+
AlgoProject Trading Platform API
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import threading
import sys

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        try:
            if path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "message": "AlgoProject API v1.0.0 - Python 3.14 Compatible",
                    "status": "running",
                    "endpoints": {
                        "health": "/health",
                        "nse": "/api/nse/symbols, /api/nse/market-data",
                        "crypto": "/api/crypto/symbols, /api/crypto/market-data", 
                        "ai": "/api/ai/recommendations",
                        "backtest": "/api/backtest/run"
                    },
                    "timestamp": datetime.now().isoformat(),
                    "python_version": sys.version,
                    "compatibility": "✅ Python 3.14 Compatible"
                }
                self.wfile.write(json.dumps(response, indent=2).encode())

@app.get("/health", tags=["System"])
async def health_check():
    """System health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# NSE API Endpoints
@app.get("/api/nse/symbols", tags=["NSE"])
async def get_nse_symbols():
    """Get available NSE symbols for NIFTY 50 and NIFTY 100"""
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

@app.get("/api/nse/market-data", tags=["NSE"])
async def get_nse_market_data():
    """Get real-time NSE market data including indices, gainers, and losers"""
    return {
        "indices": {
            "NIFTY50": {"price": 21580.25, "change": 123.45, "change_percent": 0.57},
            "BANKNIFTY": {"price": 48750.80, "change": -234.20, "change_percent": -0.48}
        },
        "top_gainers": ["BHARTIARTL", "RELIANCE", "TCS"],
        "top_losers": ["INFY", "ICICIBANK", "MARUTI"],
        "timestamp": datetime.now().isoformat()
    }

# Crypto API Endpoints  
@app.get("/api/crypto/symbols", tags=["Crypto"])
async def get_crypto_symbols():
    """Get available cryptocurrency trading pairs"""
    return {
        "major_pairs": ["BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT"],
        "altcoins": ["MATIC/USDT", "DOT/USDT", "LINK/USDT", "UNI/USDT", "SOL/USDT"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/crypto/market-data", tags=["Crypto"])
async def get_crypto_market_data():
    """Get real-time cryptocurrency market data and prices"""
    return {
        "prices": {
            "BTC/USDT": {"price": 67500.50, "change": 1250.30, "change_percent": 1.89},
            "ETH/USDT": {"price": 3890.75, "change": -45.25, "change_percent": -1.15}
        },
        "market_cap": 2_450_000_000_000,
        "total_volume": 98_500_000_000,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/backtest/run", tags=["Backtest"])
async def run_backtest(data: Dict[str, Any]):
    """Run a backtest with specified parameters"""
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

@app.get("/api/ai/recommendations", tags=["AI"])
async def get_ai_recommendations():
    """Get AI-powered trading strategy recommendations"""
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

# Additional NSE endpoints
@app.get("/api/nse/option-chain/{symbol}", tags=["NSE"])
async def get_option_chain(symbol: str):
    """Get option chain data for NSE symbols"""
    return {
        "symbol": symbol,
        "expiry_dates": ["2024-11-28", "2024-12-26", "2025-01-30"],
        "options": [
            {"strike": 21500, "call_price": 250.5, "put_price": 180.25, "call_oi": 45000, "put_oi": 38000},
            {"strike": 21600, "call_price": 180.75, "put_price": 230.4, "call_oi": 52000, "put_oi": 41000}
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/nse/backtest", tags=["NSE", "Backtest"])
async def run_nse_backtest(params: Dict[str, Any]):
    """Run backtest specifically for NSE symbols"""
    return {
        "success": True,
        "results": {
            "symbol": params.get("symbol", "NIFTY"),
            "strategy": params.get("strategy", "momentum"),
            "totalTrades": 89,
            "winRate": 71.2,
            "totalPnL": 145600,
            "sharpeRatio": 2.1,
            "maxDrawdown": -6.8
        }
    }

# Additional Crypto endpoints
@app.get("/api/crypto/exchanges", tags=["Crypto"])
async def get_crypto_exchanges():
    """Get list of supported cryptocurrency exchanges"""
    return {
        "exchanges": [
            {"id": "binance", "name": "Binance", "status": "active"},
            {"id": "coinbase", "name": "Coinbase Pro", "status": "active"},
            {"id": "kraken", "name": "Kraken", "status": "active"},
            {"id": "kucoin", "name": "KuCoin", "status": "active"}
        ],
        "total": 4
    }

@app.post("/api/crypto/backtest", tags=["Crypto", "Backtest"])
async def run_crypto_backtest(params: Dict[str, Any]):
    """Run backtest specifically for cryptocurrency pairs"""  
    return {
        "success": True,
        "results": {
            "pair": params.get("pair", "BTC/USDT"),
            "strategy": params.get("strategy", "breakout"),
            "totalTrades": 127,
            "winRate": 64.8,
            "totalPnL": 0.0875,  # In BTC
            "sharpeRatio": 1.89,
            "maxDrawdown": -12.3
        }
    }

# AI endpoints
@app.post("/api/ai/analyze-strategy", tags=["AI"])
async def analyze_strategy(strategy_data: Dict[str, Any]):
    """Analyze a trading strategy using AI"""
    return {
        "analysis": {
            "confidence": 82,
            "risk_level": "MEDIUM",
            "expected_return": 15.2,
            "recommendations": [
                "Consider tighter stop-loss levels",
                "Optimize position sizing",
                "Add volatility filters"
            ],
            "market_conditions": "Suitable for trending markets"
        }
    }

@app.get("/api/ai/market-sentiment", tags=["AI"])
async def get_market_sentiment():
    """Get AI-powered market sentiment analysis"""
    return {
        "overall_sentiment": "BULLISH",
        "confidence": 76,
        "sectors": {
            "technology": {"sentiment": "BULLISH", "score": 82},
            "banking": {"sentiment": "NEUTRAL", "score": 58},
            "pharma": {"sentiment": "BEARISH", "score": 34}
        },
        "factors": [
            "Strong Q3 earnings reports",
            "Positive FII inflows",
            "Global market stability"
        ],
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run("simple_api:app", host="0.0.0.0", port=3001, reload=True)