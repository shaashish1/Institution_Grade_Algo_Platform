from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import asyncio
import json
import logging
import uvicorn
from datetime import datetime, date
import pandas as pd
import numpy as np

# Import CCXT service
from ccxt_service import ccxt_service, TradingMode, ExchangeConfig, ExchangeCredentials

# Import Fyers user service
from fyers_user_service import (
    fyers_user_service, 
    FyersCredentials, 
    FyersTokenRequest, 
    FyersConnectionStatus
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Institution Grade Algo Trading Platform API",
    description="Professional trading platform with real-time data and advanced analytics",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class BacktestRequest(BaseModel):
    strategy: str = Field(..., description="Strategy name")
    symbol: str = Field(..., description="Trading symbol (e.g., BTC/USDT)")
    exchange: str = Field(..., description="Exchange name")
    start_date: date = Field(..., description="Backtest start date")
    end_date: date = Field(..., description="Backtest end date")
    initial_capital: float = Field(10000, description="Initial capital amount")

class BacktestResults(BaseModel):
    metrics: Dict[str, float]
    equity_curve: List[float]
    trades: List[Dict[str, Any]]
    summary: Dict[str, Any]

class PortfolioHolding(BaseModel):
    symbol: str
    quantity: float
    value: float
    percentage: float
    change_24h: float

class Portfolio(BaseModel):
    total_value: float
    holdings: List[PortfolioHolding]
    daily_pnl: float
    total_return: float

class Position(BaseModel):
    id: str
    symbol: str
    side: str
    size: float
    entry_price: float
    current_price: float
    pnl: float
    timestamp: datetime

class Strategy(BaseModel):
    id: str
    name: str
    description: str
    return_: float = Field(alias="return")
    sharpe_ratio: float
    max_drawdown: float
    status: str

class TradingStatus(BaseModel):
    is_active: bool
    strategy: Optional[str] = None
    start_time: Optional[datetime] = None
    positions_count: int = 0

class DeltaExchangeConfig(BaseModel):
    api_key: str
    secret_key: str

class ExchangeConnectionRequest(BaseModel):
    exchange_id: str = Field(..., description="Exchange identifier (e.g., 'binance', 'kraken')")
    trading_mode: str = Field(..., description="Trading mode: 'backtest', 'paper', or 'live'")
    api_key: Optional[str] = Field(None, description="API key (required for live trading)")
    secret: Optional[str] = Field(None, description="API secret (required for live trading)")
    passphrase: Optional[str] = Field(None, description="Passphrase (required for some exchanges)")
    sandbox: bool = Field(True, description="Use sandbox/testnet")

class MarketDataRequest(BaseModel):
    exchange_id: str = Field(..., description="Exchange identifier")
    symbol: str = Field(..., description="Trading pair (e.g., 'BTC/USDT')")
    timeframe: str = Field("1h", description="Timeframe (e.g., '1m', '5m', '1h', '1d')")
    limit: int = Field(100, description="Number of candles to fetch")

class OrderRequest(BaseModel):
    exchange_id: str = Field(..., description="Exchange identifier")
    symbol: str = Field(..., description="Trading pair")
    order_type: str = Field(..., description="Order type: 'market' or 'limit'")
    side: str = Field(..., description="Order side: 'buy' or 'sell'")
    amount: float = Field(..., description="Order amount")
    price: Optional[float] = Field(None, description="Order price (for limit orders)")

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"✅ WebSocket client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"❌ WebSocket client disconnected. Total connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Failed to send personal message: {e}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            return
        
        message_str = json.dumps(message)
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                logger.error(f"Failed to broadcast to connection: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

manager = ConnectionManager()

# Global state (In production, use proper database)
trading_status = TradingStatus(is_active=False, positions_count=0)
current_portfolio = Portfolio(
    total_value=10000.0,
    holdings=[],
    daily_pnl=0.0,
    total_return=0.0
)
active_positions: List[Position] = []

# API Routes

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0",
        "services": {
            "api": "running",
            "websocket": "running",
            "trading_engine": "ready"
        }
    }

@app.get("/portfolio", response_model=Portfolio)
async def get_portfolio():
    """Get current portfolio information"""
    try:
        # In production, fetch real portfolio data
        sample_holdings = [
            PortfolioHolding(symbol="BTC", quantity=0.5, value=25000, percentage=50.0, change_24h=2.5),
            PortfolioHolding(symbol="ETH", quantity=10.0, value=20000, percentage=40.0, change_24h=-1.2),
            PortfolioHolding(symbol="USDT", quantity=5000, value=5000, percentage=10.0, change_24h=0.0)
        ]
        
        portfolio = Portfolio(
            total_value=50000.0,
            holdings=sample_holdings,
            daily_pnl=1250.0,
            total_return=25.5
        )
        
        return portfolio
    except Exception as e:
        logger.error(f"Failed to get portfolio: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve portfolio")

@app.post("/backtest", response_model=BacktestResults)
async def run_backtest(request: BacktestRequest):
    """Execute strategy backtest"""
    try:
        logger.info(f"🧪 Starting backtest: {request.strategy} on {request.symbol}")
        
        # Simulate backtest execution
        await asyncio.sleep(0.5)  # Simulate processing time
        
        # Generate sample backtest results
        days = (request.end_date - request.start_date).days
        equity_curve = []
        current_value = request.initial_capital
        
        for i in range(days):
            # Simulate random walk with positive drift
            daily_return = np.random.normal(0.001, 0.02)  # 0.1% daily return, 2% volatility
            current_value *= (1 + daily_return)
            equity_curve.append(current_value)
        
        # Calculate metrics
        returns = np.array(equity_curve[1:]) / np.array(equity_curve[:-1]) - 1
        total_return = (equity_curve[-1] / request.initial_capital - 1) * 100
        
        # Calculate Sharpe ratio (simplified)
        sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        
        # Calculate max drawdown
        running_max = np.maximum.accumulate(equity_curve)
        drawdowns = (np.array(equity_curve) - running_max) / running_max
        max_drawdown = np.min(drawdowns) * 100
        
        # Win rate (simplified)
        win_rate = len(returns[returns > 0]) / len(returns) * 100 if len(returns) > 0 else 0
        
        results = BacktestResults(
            metrics={
                "total_return": round(total_return, 2),
                "sharpe_ratio": round(sharpe_ratio, 2),
                "max_drawdown": round(max_drawdown, 2),
                "win_rate": round(win_rate, 2),
                "total_trades": np.random.randint(50, 200),
                "profitable_trades": np.random.randint(30, 120)
            },
            equity_curve=equity_curve,
            trades=[],  # Simplified for now
            summary={
                "strategy": request.strategy,
                "symbol": request.symbol,
                "exchange": request.exchange,
                "duration_days": days,
                "initial_capital": request.initial_capital,
                "final_value": equity_curve[-1]
            }
        )
        
        # Broadcast backtest completion
        await manager.broadcast({
            "type": "backtest_complete",
            "data": {
                "strategy": request.strategy,
                "symbol": request.symbol,
                "total_return": total_return
            }
        })
        
        logger.info(f"✅ Backtest completed: {total_return:.2f}% return")
        return results
        
    except Exception as e:
        logger.error(f"❌ Backtest failed: {e}")
        raise HTTPException(status_code=500, detail=f"Backtest execution failed: {str(e)}")

@app.get("/strategies", response_model=List[Strategy])
async def get_strategies():
    """Get available trading strategies"""
    try:
        strategies = [
            Strategy(
                id="rsi_macd_vwap",
                name="RSI MACD VWAP",
                description="Combined RSI, MACD, and VWAP strategy for trend following",
                return_=15.25,
                sharpe_ratio=1.45,
                max_drawdown=-8.5,
                status="active"
            ),
            Strategy(
                id="bb_rsi",
                name="Bollinger Bands RSI",
                description="Mean reversion strategy using Bollinger Bands and RSI",
                return_=22.10,
                sharpe_ratio=1.82,
                max_drawdown=-12.3,
                status="active"
            ),
            Strategy(
                id="ema_crossover",
                name="EMA Crossover",
                description="Simple exponential moving average crossover strategy",
                return_=8.75,
                sharpe_ratio=0.95,
                max_drawdown=-15.2,
                status="inactive"
            )
        ]
        return strategies
    except Exception as e:
        logger.error(f"Failed to get strategies: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve strategies")

@app.post("/strategies/deploy")
async def deploy_strategy(strategy_data: dict):
    """Deploy a trading strategy"""
    try:
        strategy_id = strategy_data.get("strategy_id")
        logger.info(f"🚀 Deploying strategy: {strategy_id}")
        
        # Simulate strategy deployment
        await asyncio.sleep(0.5)
        
        await manager.broadcast({
            "type": "strategy_deployed",
            "data": {"strategy_id": strategy_id, "status": "deployed"}
        })
        
        return {"status": "success", "message": f"Strategy {strategy_id} deployed successfully"}
    except Exception as e:
        logger.error(f"Failed to deploy strategy: {e}")
        raise HTTPException(status_code=500, detail="Failed to deploy strategy")

@app.get("/positions", response_model=List[Position])
async def get_positions():
    """Get current trading positions"""
    try:
        # Return sample positions for demo
        sample_positions = [
            Position(
                id="pos_001",
                symbol="BTC/USDT",
                side="long",
                size=0.1,
                entry_price=45000.0,
                current_price=46200.0,
                pnl=120.0,
                timestamp=datetime.now()
            ),
            Position(
                id="pos_002",
                symbol="ETH/USDT",
                side="short",
                size=2.0,
                entry_price=3000.0,
                current_price=2980.0,
                pnl=40.0,
                timestamp=datetime.now()
            )
        ]
        return sample_positions
    except Exception as e:
        logger.error(f"Failed to get positions: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve positions")

@app.post("/positions/{position_id}/close")
async def close_position(position_id: str):
    """Close a specific position"""
    try:
        logger.info(f"🔄 Closing position: {position_id}")
        
        # Simulate position closing
        await asyncio.sleep(0.5)
        
        await manager.broadcast({
            "type": "position_closed",
            "data": {"position_id": position_id, "status": "closed"}
        })
        
        return {"status": "success", "message": f"Position {position_id} closed successfully"}
    except Exception as e:
        logger.error(f"Failed to close position: {e}")
        raise HTTPException(status_code=500, detail="Failed to close position")

@app.post("/trading/start")
async def start_trading():
    """Start live trading"""
    try:
        global trading_status
        trading_status.is_active = True
        trading_status.start_time = datetime.now()
        
        logger.info("▶️ Live trading started")
        
        await manager.broadcast({
            "type": "trading_status",
            "data": {"status": "started", "timestamp": datetime.now().isoformat()}
        })
        
        return {"status": "success", "message": "Live trading started successfully"}
    except Exception as e:
        logger.error(f"Failed to start trading: {e}")
        raise HTTPException(status_code=500, detail="Failed to start trading")

@app.post("/trading/stop")
async def stop_trading():
    """Stop live trading"""
    try:
        global trading_status
        trading_status.is_active = False
        trading_status.start_time = None
        
        logger.info("⏹️ Live trading stopped")
        
        await manager.broadcast({
            "type": "trading_status",
            "data": {"status": "stopped", "timestamp": datetime.now().isoformat()}
        })
        
        return {"status": "success", "message": "Live trading stopped successfully"}
    except Exception as e:
        logger.error(f"Failed to stop trading: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop trading")

@app.post("/trading/pause")
async def pause_trading():
    """Pause live trading"""
    try:
        logger.info("⏸️ Live trading paused")
        
        await manager.broadcast({
            "type": "trading_status",
            "data": {"status": "paused", "timestamp": datetime.now().isoformat()}
        })
        
        return {"status": "success", "message": "Live trading paused successfully"}
    except Exception as e:
        logger.error(f"Failed to pause trading: {e}")
        raise HTTPException(status_code=500, detail="Failed to pause trading")

@app.get("/analytics")
async def get_analytics():
    """Get trading analytics and performance metrics"""
    try:
        analytics = {
            "performance": {
                "total_trades": 156,
                "profitable_trades": 98,
                "win_rate": 62.8,
                "average_profit": 245.50,
                "average_loss": -187.25,
                "profit_factor": 1.31
            },
            "metrics": {
                "total_return": 18.75,
                "sharpe_ratio": 1.42,
                "sortino_ratio": 1.68,
                "max_drawdown": -11.2,
                "calmar_ratio": 1.67
            },
            "charts": {
                "equity_curve": [10000 + i * 50 + np.random.normal(0, 200) for i in range(100)],
                "drawdown": [abs(np.random.normal(0, 5)) for _ in range(100)]
            }
        }
        return analytics
    except Exception as e:
        logger.error(f"Failed to get analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")

@app.get("/stats")
async def get_stats():
    """Get general trading statistics"""
    try:
        stats = {
            "total_portfolio_value": 52450.75,
            "daily_pnl": 1245.30,
            "active_trades": 3,
            "win_rate": 64.2,
            "total_trades_today": 12,
            "profit_today": 892.15
        }
        return stats
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve stats")

@app.get("/exchanges/supported")
async def get_supported_exchanges():
    """Get list of supported exchanges"""
    try:
        exchanges = ccxt_service.get_supported_exchanges()
        return {
            "supported_exchanges": exchanges,
            "count": len(exchanges),
            "trading_modes": ["backtest", "paper", "live"],
            "credential_requirements": {
                "backtest": "No credentials needed - public data only",
                "paper": "No credentials needed - public data only", 
                "live": "API credentials required for trading"
            }
        }
    except Exception as e:
        logger.error(f"Failed to get supported exchanges: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve supported exchanges")

@app.post("/exchanges/connect")
async def connect_exchange(request: ExchangeConnectionRequest):
    """Connect to exchange with appropriate authentication based on trading mode"""
    try:
        # Validate trading mode
        if request.trading_mode not in ["backtest", "paper", "live"]:
            raise HTTPException(status_code=400, detail="Invalid trading mode. Must be 'backtest', 'paper', or 'live'")
        
        trading_mode = TradingMode(request.trading_mode)
        
        # Check credentials requirement
        if ccxt_service.requires_credentials(trading_mode):
            if not request.api_key or not request.secret:
                raise HTTPException(
                    status_code=400, 
                    detail=f"API credentials required for {request.trading_mode} trading mode"
                )
            
            credentials = ExchangeCredentials(
                api_key=request.api_key,
                secret=request.secret,
                passphrase=request.passphrase,
                sandbox=request.sandbox
            )
        else:
            credentials = None
            logger.info(f"🔓 Connecting to {request.exchange_id} in {request.trading_mode} mode (no credentials needed)")
        
        # Create exchange configuration
        config = ExchangeConfig(
            exchange_id=request.exchange_id,
            trading_mode=trading_mode,
            credentials=credentials
        )
        
        # Initialize exchange
        success = await ccxt_service.initialize_exchange(config)
        
        if success:
            status = ccxt_service.get_exchange_status(request.exchange_id)
            return {
                "status": "success",
                "message": f"{request.exchange_id} connected successfully in {request.trading_mode} mode",
                "exchange_status": status
            }
        else:
            raise HTTPException(status_code=500, detail=f"Failed to connect to {request.exchange_id}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to connect exchange: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to connect exchange: {str(e)}")

@app.get("/exchanges/{exchange_id}/status")
async def get_exchange_status(exchange_id: str):
    """Get exchange connection status"""
    try:
        status = ccxt_service.get_exchange_status(exchange_id)
        return {
            "exchange_id": exchange_id,
            **status
        }
    except Exception as e:
        logger.error(f"Failed to get exchange status: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve exchange status")

@app.get("/exchanges/active")
async def get_active_exchanges():
    """Get list of currently connected exchanges"""
    try:
        initialized_exchanges = ccxt_service.get_initialized_exchanges()
        exchanges_info = []
        
        for exchange_id in initialized_exchanges:
            status = ccxt_service.get_exchange_status(exchange_id)
            exchanges_info.append({
                "exchange_id": exchange_id,
                **status
            })
        
        return {
            "active_exchanges": exchanges_info,
            "count": len(exchanges_info)
        }
    except Exception as e:
        logger.error(f"Failed to get active exchanges: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve active exchanges")

@app.post("/market-data/fetch")
async def fetch_market_data(request: MarketDataRequest):
    """Fetch market data from exchange - works for all trading modes"""
    try:
        # Check if exchange is initialized
        if request.exchange_id not in ccxt_service.get_initialized_exchanges():
            raise HTTPException(
                status_code=400, 
                detail=f"Exchange {request.exchange_id} not connected. Please connect first."
            )
        
        # Fetch market data
        ohlcv_data = await ccxt_service.get_market_data(
            exchange_id=request.exchange_id,
            symbol=request.symbol,
            timeframe=request.timeframe,
            limit=request.limit
        )
        
        if ohlcv_data is None:
            raise HTTPException(status_code=500, detail="Failed to fetch market data")
        
        # Convert to structured format
        formatted_data = []
        for candle in ohlcv_data:
            formatted_data.append({
                "timestamp": candle[0],
                "datetime": datetime.fromtimestamp(candle[0] / 1000).isoformat(),
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4],
                "volume": candle[5]
            })
        
        return {
            "exchange_id": request.exchange_id,
            "symbol": request.symbol,
            "timeframe": request.timeframe,
            "data_count": len(formatted_data),
            "data": formatted_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch market data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch market data: {str(e)}")

@app.post("/orders/place")
async def place_order(request: OrderRequest):
    """Place trading order - only works in LIVE mode"""
    try:
        # Check if exchange is initialized
        if request.exchange_id not in ccxt_service.get_initialized_exchanges():
            raise HTTPException(
                status_code=400, 
                detail=f"Exchange {request.exchange_id} not connected. Please connect first."
            )
        
        # Check if live trading is enabled
        if not ccxt_service.is_live_trading_enabled(request.exchange_id):
            exchange_info = ccxt_service.get_exchange_info(request.exchange_id)
            current_mode = exchange_info['mode'].value if exchange_info else 'unknown'
            raise HTTPException(
                status_code=403, 
                detail=f"Live trading not enabled for {request.exchange_id}. Current mode: {current_mode}. Order placement requires LIVE mode with API credentials."
            )
        
        # Place order
        order_result = await ccxt_service.place_order(
            exchange_id=request.exchange_id,
            symbol=request.symbol,
            order_type=request.order_type,
            side=request.side,
            amount=request.amount,
            price=request.price
        )
        
        if order_result is None:
            raise HTTPException(status_code=500, detail="Failed to place order")
        
        return {
            "status": "success",
            "message": "Order placed successfully",
            "order": order_result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to place order: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to place order: {str(e)}")

@app.get("/delta-exchange/status")
async def get_delta_exchange_status():
    """Get Delta Exchange connection status (legacy endpoint)"""
    try:
        status = ccxt_service.get_exchange_status("delta")
        return {
            "connected": status["initialized"],
            "api_key_configured": status["live_trading_enabled"],
            "last_sync": None,
            "account_info": None,
            "trading_mode": status["trading_mode"],
            "markets_count": status["markets_count"]
        }
    except Exception as e:
        logger.error(f"Failed to get Delta Exchange status: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve Delta Exchange status")

@app.post("/delta-exchange/configure")
async def configure_delta_exchange(config: DeltaExchangeConfig):
    """Configure Delta Exchange API credentials (legacy endpoint)"""
    try:
        # Use new CCXT service for Delta Exchange
        request = ExchangeConnectionRequest(
            exchange_id="delta",
            trading_mode="live",
            api_key=config.api_key,
            secret=config.secret_key,
            sandbox=True
        )
        
        result = await connect_exchange(request)
        return {"status": "success", "message": "Delta Exchange configured successfully"}
        
    except Exception as e:
        logger.error(f"Failed to configure Delta Exchange: {e}")
        raise HTTPException(status_code=500, detail="Failed to configure Delta Exchange")

# =============================================================================
# FYERS USER CREDENTIALS MANAGEMENT
# =============================================================================

@app.post("/fyers/credentials")
async def add_fyers_credentials(credentials: FyersCredentials):
    """Add or update Fyers credentials for a user"""
    try:
        # Validate credentials format
        validation = fyers_user_service.validate_credentials(credentials)
        if not validation["valid"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid credentials: {', '.join(validation['errors'])}"
            )
        
        success = fyers_user_service.add_user_credentials(credentials)
        if success:
            return {
                "status": "success",
                "message": f"Fyers credentials added/updated for user: {credentials.user_id}",
                "user_id": credentials.user_id
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save credentials")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add Fyers credentials: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/fyers/credentials/{user_id}")
async def get_fyers_credentials(user_id: str):
    """Get Fyers credentials for a user (excluding sensitive data)"""
    try:
        credentials = fyers_user_service.get_user_credentials(user_id)
        if not credentials:
            raise HTTPException(status_code=404, detail="User credentials not found")
        
        # Return safe version without sensitive data
        return {
            "user_id": credentials.user_id,
            "client_id": credentials.client_id,
            "user_name": credentials.user_name,
            "redirect_uri": credentials.redirect_uri,
            "has_totp_key": bool(credentials.totp_key),
            "has_access_token": bool(credentials.access_token),
            "token_expires": credentials.token_expires,
            "is_active": credentials.is_active,
            "created_at": credentials.created_at,
            "updated_at": credentials.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get Fyers credentials: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/fyers/credentials/{user_id}")  
async def remove_fyers_credentials(user_id: str):
    """Remove Fyers credentials for a user"""
    try:
        success = fyers_user_service.remove_user_credentials(user_id)
        if success:
            return {
                "status": "success",
                "message": f"Fyers credentials removed for user: {user_id}",
                "user_id": user_id
            }
        else:
            raise HTTPException(status_code=404, detail="User credentials not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to remove Fyers credentials: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/fyers/status/{user_id}")
async def get_fyers_status(user_id: str):
    """Get Fyers connection status for a user"""
    try:
        status = fyers_user_service.get_connection_status(user_id)
        return status.dict()
        
    except Exception as e:
        logger.error(f"Failed to get Fyers status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/fyers/test-connection/{user_id}")
async def test_fyers_connection(user_id: str):
    """Test Fyers connection for a user"""
    try:
        result = fyers_user_service.test_connection(user_id)
        return result
        
    except Exception as e:
        logger.error(f"Failed to test Fyers connection: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/fyers/users")
async def list_fyers_users():
    """List all users with Fyers credentials"""
    try:
        users = fyers_user_service.list_users()
        return {
            "users": users,
            "count": len(users)
        }
        
    except Exception as e:
        logger.error(f"Failed to list Fyers users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/fyers/token/{user_id}")
async def update_fyers_token(user_id: str, token_data: dict):
    """Update access token for a user"""
    try:
        access_token = token_data.get("access_token")
        expires_in_hours = token_data.get("expires_in_hours", 24)
        
        if not access_token:
            raise HTTPException(status_code=400, detail="Access token required")
        
        success = fyers_user_service.update_access_token(
            user_id, access_token, expires_in_hours
        )
        
        if success:
            return {
                "status": "success",
                "message": f"Access token updated for user: {user_id}",
                "user_id": user_id
            }
        else:
            raise HTTPException(status_code=404, detail="User not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update Fyers token: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# =============================================================================
# WEBSOCKET ENDPOINT  
# =============================================================================

# WebSocket Endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        # Send initial connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "data": {"message": "Connected to trading platform", "timestamp": datetime.now().isoformat()}
        }))
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for client messages (ping/pong, etc.)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                message = json.loads(data)
                
                # Handle different message types
                if message.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong", "timestamp": datetime.now().isoformat()}))
                elif message.get("type") == "subscribe":
                    # Handle subscription requests
                    await websocket.send_text(json.dumps({
                        "type": "subscription_confirmed",
                        "data": {"channels": message.get("channels", [])}
                    }))
                    
            except asyncio.TimeoutError:
                # Send periodic updates even if no client messages
                await websocket.send_text(json.dumps({
                    "type": "heartbeat",
                    "timestamp": datetime.now().isoformat()
                }))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Background task for sending periodic updates
@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    asyncio.create_task(periodic_updates())
    logger.info("🚀 Institution Grade Algo Trading Platform API started")
    logger.info("📡 WebSocket server ready for connections")
    logger.info("🔗 API documentation available at http://localhost:8000/docs")

async def periodic_updates():
    """Send periodic updates to connected clients"""
    while True:
        try:
            await asyncio.sleep(10)  # Update every 10 seconds
            
            # Send portfolio updates
            portfolio_update = {
                "type": "portfolio_update",
                "data": {
                    "total_value": 50000 + np.random.normal(0, 500),
                    "daily_pnl": np.random.normal(100, 200),
                    "timestamp": datetime.now().isoformat()
                }
            }
            await manager.broadcast(portfolio_update)
            
            # Send price updates
            price_update = {
                "type": "price_update",
                "data": {
                    "BTC/USDT": 45000 + np.random.normal(0, 1000),
                    "ETH/USDT": 3000 + np.random.normal(0, 100),
                    "timestamp": datetime.now().isoformat()
                }
            }
            await manager.broadcast(price_update)
            
        except Exception as e:
            logger.error(f"Error in periodic updates: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
