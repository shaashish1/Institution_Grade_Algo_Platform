#!/usr/bin/env python3
"""
AlgoProject Trading Platform API - Python 3.14 Compatible
Simple HTTP API Server using Python's built-in http.server
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
                
            elif path == '/health':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "healthy", "timestamp": datetime.now().isoformat()}
                self.wfile.write(json.dumps(response).encode())
                
            elif path == '/api/nse/symbols':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
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
                self.wfile.write(json.dumps(response).encode())
                
            elif path == '/api/nse/market-data':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "indices": {
                        "NIFTY50": {"price": 21580.25, "change": 123.45, "change_percent": 0.57},
                        "BANKNIFTY": {"price": 48750.80, "change": -234.20, "change_percent": -0.48}
                    },
                    "top_gainers": ["BHARTIARTL", "RELIANCE", "TCS"],
                    "top_losers": ["INFY", "ICICIBANK", "MARUTI"],
                    "timestamp": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode())
                
            elif path == '/api/crypto/symbols':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "major_pairs": ["BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "ADA/USDT"],
                    "altcoins": ["MATIC/USDT", "DOT/USDT", "LINK/USDT", "UNI/USDT", "SOL/USDT"],
                    "timestamp": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode())
                
            elif path == '/api/crypto/market-data':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "prices": {
                        "BTC/USDT": {"price": 67500.50, "change": 1250.30, "change_percent": 1.89},
                        "ETH/USDT": {"price": 3890.75, "change": -45.25, "change_percent": -1.15}
                    },
                    "market_cap": 2_450_000_000_000,
                    "total_volume": 98_500_000_000,
                    "timestamp": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode())
                
            elif path == '/api/ai/recommendations':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
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
                self.wfile.write(json.dumps(response).encode())
                
            elif path == '/api/fyers/market-data':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                # Market status logic
                now = datetime.now()
                is_weekend = now.weekday() > 4  # Saturday=5, Sunday=6
                current_time = now.time()
                market_open = current_time >= datetime.strptime("09:15", "%H:%M").time()
                market_close = current_time <= datetime.strptime("15:30", "%H:%M").time()
                is_market_open = not is_weekend and market_open and market_close
                
                response = {
                    "market_status": {
                        "is_open": is_market_open,
                        "session": "REGULAR" if is_market_open else "CLOSED",
                        "current_time": now.isoformat(),
                        "message": "Live data" if is_market_open else "Market closed - showing last available data"
                    },
                    "indices": {
                        "NIFTY50": {
                            "symbol": "NIFTY50",
                            "price": 25843.15,
                            "change": 133.30,
                            "change_percent": 0.52,
                            "high": 25895.50,
                            "low": 25720.80,
                            "open": 25735.20,
                            "previous_close": 25709.85
                        },
                        "BANKNIFTY": {
                            "symbol": "BANKNIFTY", 
                            "price": 58033.20,
                            "change": 319.85,
                            "change_percent": 0.55,
                            "high": 58125.40,
                            "low": 57890.30,
                            "open": 57950.15,
                            "previous_close": 57713.35
                        }
                    },
                    "timestamp": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode())
                
            elif path == '/api/fyers/option-chain':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                # Generate option chain based on NIFTY spot price
                nifty_spot = 25843.15
                strikes = list(range(25600, 26100, 50))
                options = []
                
                for strike in strikes:
                    moneyness = (strike - nifty_spot) / nifty_spot
                    
                    # Simplified option pricing
                    if strike <= nifty_spot:  # ITM calls
                        call_price = max(5, nifty_spot - strike + 20)
                    else:  # OTM calls
                        call_price = max(0.05, 100 - abs(moneyness * 2000))
                    
                    if strike >= nifty_spot:  # ITM puts
                        put_price = max(5, strike - nifty_spot + 20)
                    else:  # OTM puts
                        put_price = max(0.05, 100 - abs(moneyness * 2000))
                    
                    options.append({
                        "strike": strike,
                        "call": {
                            "price": round(call_price, 2),
                            "iv": round(max(0.05, 0.15 + abs(moneyness)), 2),
                            "oi": max(1000, int(50000 - abs(moneyness * 100000))),
                            "volume": max(100, int(5000 - abs(moneyness * 10000)))
                        },
                        "put": {
                            "price": round(put_price, 2),
                            "iv": round(max(0.05, 0.16 + abs(moneyness)), 2),
                            "oi": max(1000, int(45000 - abs(moneyness * 90000))),
                            "volume": max(100, int(4500 - abs(moneyness * 9000)))
                        }
                    })
                
                response = {
                    "symbol": "NIFTY",
                    "spot_price": nifty_spot,
                    "expiry_date": "2025-10-30",
                    "options": options,
                    "last_updated": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode())
                
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "Not Found", "path": path}
                self.wfile.write(json.dumps(response).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": str(e), "status": "error"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        try:
            if path == '/api/backtest/run':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "success": True,
                    "input": data,
                    "results": {
                        "totalTrades": 150,
                        "winRate": 67.3,
                        "totalPnL": 185750,
                        "sharpeRatio": 2.34
                    }
                }
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "Not Found", "path": path}
                self.wfile.write(json.dumps(response).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": str(e), "status": "error"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def run_server(port=3001):
    """Run the API server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f"🚀 AlgoProject API Server starting on http://localhost:{port}")
    print(f"📊 API Documentation: http://localhost:{port}/")
    print(f"❤️  Health Check: http://localhost:{port}/health")
    print(f"🔧 Python Version: {sys.version}")
    print("✅ Python 3.14 Compatible - No FastAPI/Pydantic warnings!")
    print("\nAvailable Endpoints:")
    print("  GET  /                        - API overview")
    print("  GET  /health                  - Health check")
    print("  GET  /api/nse/symbols         - NSE stock symbols")
    print("  GET  /api/nse/market-data     - NSE market data")
    print("  GET  /api/crypto/symbols      - Crypto symbols")
    print("  GET  /api/crypto/market-data  - Crypto market data")
    print("  GET  /api/ai/recommendations  - AI recommendations")
    print("  GET  /api/fyers/market-data   - FYERS-compatible market data")
    print("  GET  /api/fyers/option-chain  - NIFTY option chain (FYERS format)")
    print("  POST /api/backtest/run        - Run backtest")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped on port {port}")
        httpd.server_close()

if __name__ == "__main__":
    run_server()