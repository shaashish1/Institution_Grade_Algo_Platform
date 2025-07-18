"""
WebSocket Client
===============

WebSocket client implementation for real-time data streaming.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import ssl

try:
    import websockets
    from websockets.exceptions import ConnectionClosed, InvalidURI
except ImportError:
    websockets = None
    ConnectionClosed = Exception
    InvalidURI = Exception

from .data_stream import DataStream, StreamStatus
from ...core.interfaces import MarketData


class WebSocketClient(DataStream):
    """WebSocket client for real-time data streaming"""
    
    def __init__(self, stream_id: str, url: str, headers: Optional[Dict[str, str]] = None):
        """Initialize WebSocket client
        
        Args:
            stream_id: Unique stream identifier
            url: WebSocket URL
            headers: Optional headers for connection
        """
        if websockets is None:
            raise ImportError("websockets library not installed. Please install it with 'pip install websockets'")
        
        super().__init__(stream_id)
        self.url = url
        self.headers = headers or {}
        self.websocket = None
        self.listen_task = None
        self.ping_task = None
        self.ping_interval = 30  # seconds
        self.message_handlers: Dict[str, Callable] = {}
        
    async def connect(self) -> bool:
        """Connect to WebSocket
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.set_status(StreamStatus.CONNECTING)
            
            # Create SSL context for secure connections
            ssl_context = None
            if self.url.startswith('wss://'):
                ssl_context = ssl.create_default_context()
            
            # Connect to WebSocket
            self.websocket = await websockets.connect(
                self.url,
                extra_headers=self.headers,
                ssl=ssl_context,
                ping_interval=None,  # We'll handle pings manually
                ping_timeout=10
            )
            
            self.set_status(StreamStatus.CONNECTED)
            self.update_heartbeat()
            
            # Start listening for messages
            self.listen_task = asyncio.create_task(self._listen())
            
            # Start ping task
            self.ping_task = asyncio.create_task(self._ping_loop())
            
            self.logger.info(f"Connected to WebSocket: {self.url}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to WebSocket: {e}")
            self.set_status(StreamStatus.ERROR)
            return False
    
    async def disconnect(self):
        """Disconnect from WebSocket"""
        try:
            self.set_status(StreamStatus.DISCONNECTED)
            
            # Cancel tasks
            if self.listen_task:
                self.listen_task.cancel()
                try:
                    await self.listen_task
                except asyncio.CancelledError:
                    pass
            
            if self.ping_task:
                self.ping_task.cancel()
                try:
                    await self.ping_task
                except asyncio.CancelledError:
                    pass
            
            # Close WebSocket connection
            if self.websocket:
                await self.websocket.close()
                self.websocket = None
            
            self.subscribed_symbols.clear()
            self.logger.info("Disconnected from WebSocket")
            
        except Exception as e:
            self.logger.error(f"Error during disconnect: {e}")
    
    async def send_message(self, message: Dict[str, Any]):
        """Send message to WebSocket
        
        Args:
            message: Message to send
        """
        if not self.websocket or self.status != StreamStatus.CONNECTED:
            raise ConnectionError("WebSocket not connected")
        
        try:
            await self.websocket.send(json.dumps(message))
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            raise
    
    async def subscribe(self, symbol: str, data_type: str = "ticker"):
        """Subscribe to a symbol
        
        Args:
            symbol: Trading symbol to subscribe to
            data_type: Type of data (ticker, orderbook, trades)
        """
        # This is a generic implementation - subclasses should override
        # with exchange-specific subscription messages
        message = {
            "method": "SUBSCRIBE",
            "params": [f"{symbol.lower()}@{data_type}"],
            "id": len(self.subscribed_symbols) + 1
        }
        
        await self.send_message(message)
        self.subscribed_symbols.add(symbol)
        self.logger.info(f"Subscribed to {symbol} {data_type}")
    
    async def unsubscribe(self, symbol: str, data_type: str = "ticker"):
        """Unsubscribe from a symbol
        
        Args:
            symbol: Trading symbol to unsubscribe from
            data_type: Type of data (ticker, orderbook, trades)
        """
        # This is a generic implementation - subclasses should override
        # with exchange-specific unsubscription messages
        message = {
            "method": "UNSUBSCRIBE",
            "params": [f"{symbol.lower()}@{data_type}"],
            "id": len(self.subscribed_symbols) + 1000
        }
        
        await self.send_message(message)
        self.subscribed_symbols.discard(symbol)
        self.logger.info(f"Unsubscribed from {symbol} {data_type}")
    
    def add_message_handler(self, message_type: str, handler: Callable):
        """Add a message handler for specific message types
        
        Args:
            message_type: Type of message to handle
            handler: Handler function
        """
        self.message_handlers[message_type] = handler
    
    async def _listen(self):
        """Listen for WebSocket messages"""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self._handle_message(data)
                    self.update_heartbeat()
                except json.JSONDecodeError as e:
                    self.logger.error(f"Invalid JSON received: {e}")
                except Exception as e:
                    self.logger.error(f"Error handling message: {e}")
                    
        except ConnectionClosed:
            self.logger.warning("WebSocket connection closed")
            self.set_status(StreamStatus.DISCONNECTED)
            await self.handle_reconnect()
        except Exception as e:
            self.logger.error(f"Error in listen loop: {e}")
            self.set_status(StreamStatus.ERROR)
    
    async def _handle_message(self, data: Dict[str, Any]):
        """Handle incoming WebSocket message
        
        Args:
            data: Parsed message data
        """
        # Check for error messages
        if 'error' in data:
            self.logger.error(f"WebSocket error: {data['error']}")
            self.notify_subscribers("error", data['error'])
            return
        
        # Check for subscription confirmations
        if 'result' in data and data.get('id'):
            self.logger.debug(f"Subscription confirmed: {data}")
            return
        
        # Handle stream data
        if 'stream' in data and 'data' in data:
            stream_name = data['stream']
            stream_data = data['data']
            
            # Parse market data
            market_data = self._parse_market_data(stream_name, stream_data)
            if market_data:
                self.notify_subscribers("data", market_data)
        
        # Handle custom message types
        message_type = data.get('e') or data.get('type') or 'unknown'
        if message_type in self.message_handlers:
            await self.message_handlers[message_type](data)
    
    def _parse_market_data(self, stream_name: str, data: Dict[str, Any]) -> Optional[MarketData]:
        """Parse stream data into MarketData object
        
        Args:
            stream_name: Name of the stream
            data: Stream data
            
        Returns:
            MarketData object or None if parsing fails
        """
        try:
            # Extract symbol from stream name (format: symbol@type)
            symbol = stream_name.split('@')[0].upper()
            
            # Parse ticker data (generic format)
            if '@ticker' in stream_name or 'c' in data:
                return MarketData(
                    symbol=symbol,
                    timestamp=datetime.fromtimestamp(data.get('E', data.get('timestamp', 0)) / 1000),
                    open=float(data.get('o', data.get('open', 0))),
                    high=float(data.get('h', data.get('high', 0))),
                    low=float(data.get('l', data.get('low', 0))),
                    close=float(data.get('c', data.get('close', data.get('price', 0)))),
                    volume=float(data.get('v', data.get('volume', 0))),
                    exchange=self.stream_id
                )
            
            return None
            
        except (KeyError, ValueError, TypeError) as e:
            self.logger.error(f"Error parsing market data: {e}")
            return None
    
    async def _ping_loop(self):
        """Send periodic ping messages to keep connection alive"""
        try:
            while self.status == StreamStatus.CONNECTED:
                await asyncio.sleep(self.ping_interval)
                
                if self.websocket and self.status == StreamStatus.CONNECTED:
                    try:
                        await self.websocket.ping()
                    except Exception as e:
                        self.logger.error(f"Ping failed: {e}")
                        break
                        
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f"Error in ping loop: {e}")


class BinanceWebSocketClient(WebSocketClient):
    """Binance-specific WebSocket client"""
    
    def __init__(self):
        super().__init__("binance", "wss://stream.binance.com:9443/ws/")
    
    async def subscribe(self, symbol: str, data_type: str = "ticker"):
        """Subscribe to Binance stream
        
        Args:
            symbol: Trading symbol
            data_type: Type of data (ticker, depth, trade)
        """
        stream_name = f"{symbol.lower()}@{data_type}"
        if data_type == "ticker":
            stream_name = f"{symbol.lower()}@ticker"
        elif data_type == "orderbook":
            stream_name = f"{symbol.lower()}@depth"
        elif data_type == "trades":
            stream_name = f"{symbol.lower()}@trade"
        
        message = {
            "method": "SUBSCRIBE",
            "params": [stream_name],
            "id": len(self.subscribed_symbols) + 1
        }
        
        await self.send_message(message)
        self.subscribed_symbols.add(symbol)
        self.logger.info(f"Subscribed to Binance {symbol} {data_type}")


class BybitWebSocketClient(WebSocketClient):
    """Bybit-specific WebSocket client"""
    
    def __init__(self):
        super().__init__("bybit", "wss://stream.bybit.com/v5/public/spot")
    
    async def subscribe(self, symbol: str, data_type: str = "ticker"):
        """Subscribe to Bybit stream
        
        Args:
            symbol: Trading symbol
            data_type: Type of data (ticker, orderbook, trade)
        """
        topic = f"tickers.{symbol}"
        if data_type == "orderbook":
            topic = f"orderbook.1.{symbol}"
        elif data_type == "trades":
            topic = f"publicTrade.{symbol}"
        
        message = {
            "op": "subscribe",
            "args": [topic]
        }
        
        await self.send_message(message)
        self.subscribed_symbols.add(symbol)
        self.logger.info(f"Subscribed to Bybit {symbol} {data_type}")