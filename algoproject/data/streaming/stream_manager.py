"""
Stream Manager
==============

Manages multiple real-time data streams for AlgoProject.
"""

import asyncio
import logging
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
import threading
from concurrent.futures import ThreadPoo
from .data_stream import DataStream, StreamStatus
from .websocket_client import WebSocketClient, BinanceWebSocketClient, BybitWebSocketClient
from ...core.interfaces import MarketData
from ...core.config_manager import ConfigManager


class StreamManager:
    """Manages multiple real-time data streams"""
    
    def __init__(self, config_manager: ConfigManager):
        """Initialize stream manager
        
        Args:
            config_manager: Configuration manager
        """
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        self.streams: Dict[str, DataStream] = {}
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.symbol_streams: Dict[str, Set[str]] = defaultdict(set)  # symbol -> stream_ids
        self.stream_symbols: Dict[str, Set[str]] = defaultdict(set)  # stream_id -> symbols
        self.data_buffer: Dict[str, List[MarketData]] = defaultdict(list)
        self.buffer_size = 1000
        self.health_check_task = None
        self.health_check_interval = 30  # seconds
        
    async def start(self):
        """Start the stream manager"""
        self.logger.info("Starting stream manager")
        
        # Start health check task
        self.health_check_task = asyncio.create_task(self._health_check_loop())
        
        # Initialize configured streams
        await self._initialize_streams()
    
    async def stop(self):
        """Stop the stream manager"""
        self.logger.info("Stopping stream manager")
        
        # Cancel health check task
        if self.health_check_task:
            self.health_check_task.cancel()
            try:
                await self.health_check_task
            except asyncio.CancelledError:
                pass
        
        # Disconnect all streams
        for stream in self.streams.values():
            await stream.disconnect()
        
        self.streams.clear()
        self.symbol_streams.clear()
        self.stream_symbols.clear()
    
    async def _initialize_streams(self):
        """Initialize streams from configuration"""
        try:
            # Get streaming configuration
            streaming_config = self.config_manager.get_setting("exchange_config", "streaming", {})
            
            # Initialize crypto streams
            crypto_config = streaming_config.get("crypto", {})
            if crypto_config.get("binance", {}).get("enabled", False):
                await self.add_stream("binance", BinanceWebSocketClient())
            
            if crypto_config.get("bybit", {}).get("enabled", False):
                await self.add_stream("bybit", BybitWebSocketClient())
            
            # Initialize custom streams
            custom_streams = streaming_config.get("custom", [])
            for stream_config in custom_streams:
                stream_id = stream_config.get("id")
                url = stream_config.get("url")
                headers = stream_config.get("headers", {})
                
                if stream_id and url:
                    client = WebSocketClient(stream_id, url, headers)
                    await self.add_stream(stream_id, client)
            
        except Exception as e:
            self.logger.error(f"Error initializing streams: {e}")
    
    async def add_stream(self, stream_id: str, stream: DataStream) -> bool:
        """Add a data stream
        
        Args:
            stream_id: Unique stream identifier
            stream: DataStream instance
            
        Returns:
            True if stream added successfully, False otherwise
        """
        try:
            if stream_id in self.streams:
                self.logger.warning(f"Stream {stream_id} already exists")
                return False
            
            # Add event handlers
            stream.add_subscriber("data", self._handle_stream_data)
            stream.add_subscriber("status", self._handle_stream_status)
            stream.add_subscriber("error", self._handle_stream_error)
            
            # Connect the stream
            if await stream.connect():
                self.streams[stream_id] = stream
                self.logger.info(f"Added stream: {stream_id}")
                return True
            else:
                self.logger.error(f"Failed to connect stream: {stream_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error adding stream {stream_id}: {e}")
            return False
    
    async def remove_stream(self, stream_id: str) -> bool:
        """Remove a data stream
        
        Args:
            stream_id: Stream identifier to remove
            
        Returns:
            True if stream removed successfully, False otherwise
        """
        try:
            if stream_id not in self.streams:
                self.logger.warning(f"Stream {stream_id} not found")
                return False
            
            stream = self.streams[stream_id]
            await stream.disconnect()
            
            # Clean up mappings
            symbols = self.stream_symbols[stream_id].copy()
            for symbol in symbols:
                self.symbol_streams[symbol].discard(stream_id)
                if not self.symbol_streams[symbol]:
                    del self.symbol_streams[symbol]
            
            del self.streams[stream_id]
            del self.stream_symbols[stream_id]
            
            self.logger.info(f"Removed stream: {stream_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error removing stream {stream_id}: {e}")
            return False
    
    async def subscribe_symbol(self, symbol: str, data_type: str = "ticker", 
                             preferred_stream: Optional[str] = None) -> bool:
        """Subscribe to a symbol across available streams
        
        Args:
            symbol: Trading symbol to subscribe to
            data_type: Type of data (ticker, orderbook, trades)
            preferred_stream: Preferred stream ID (optional)
            
        Returns:
            True if subscription successful, False otherwise
        """
        try:
            # Find available streams for this symbol
            available_streams = []
            
            if preferred_stream and preferred_stream in self.streams:
                if self.streams[preferred_stream].is_connected():
                    available_streams.append(preferred_stream)
            else:
                # Use all connected streams
                for stream_id, stream in self.streams.items():
                    if stream.is_connected():
                        available_streams.append(stream_id)
            
            if not available_streams:
                self.logger.error(f"No available streams for symbol {symbol}")
                return False
            
            # Subscribe to the first available stream
            stream_id = available_streams[0]
            stream = self.streams[stream_id]
            
            await stream.subscribe(symbol, data_type)
            
            # Update mappings
            self.symbol_streams[symbol].add(stream_id)
            self.stream_symbols[stream_id].add(symbol)
            
            self.logger.info(f"Subscribed to {symbol} on stream {stream_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error subscribing to symbol {symbol}: {e}")
            return False
    
    async def unsubscribe_symbol(self, symbol: str, data_type: str = "ticker") -> bool:
        """Unsubscribe from a symbol across all streams
        
        Args:
            symbol: Trading symbol to unsubscribe from
            data_type: Type of data (ticker, orderbook, trades)
            
        Returns:
            True if unsubscription successful, False otherwise
        """
        try:
            if symbol not in self.symbol_streams:
                self.logger.warning(f"Symbol {symbol} not subscribed")
                return False
            
            # Unsubscribe from all streams
            stream_ids = self.symbol_streams[symbol].copy()
            for stream_id in stream_ids:
                if stream_id in self.streams:
                    stream = self.streams[stream_id]
                    await stream.unsubscribe(symbol, data_type)
                    
                    # Update mappings
                    self.stream_symbols[stream_id].discard(symbol)
            
            del self.symbol_streams[symbol]
            
            self.logger.info(f"Unsubscribed from {symbol}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error unsubscribing from symbol {symbol}: {e}")
            return False
    
    def add_subscriber(self, event_type: str, callback: Callable):
        """Add a subscriber for stream events
        
        Args:
            event_type: Type of event (data, status, error)
            callback: Callback function
        """
        self.subscribers[event_type].append(callback)
    
    def remove_subscriber(self, event_type: str, callback: Callable):
        """Remove a subscriber for stream events
        
        Args:
            event_type: Type of event
            callback: Callback function to remove
        """
        try:
            self.subscribers[event_type].remove(callback)
        except ValueError:
            pass
    
    def get_stream_status(self, stream_id: str) -> Optional[StreamStatus]:
        """Get status of a specific stream
        
        Args:
            stream_id: Stream identifier
            
        Returns:
            Stream status or None if stream not found
        """
        if stream_id in self.streams:
            return self.streams[stream_id].get_status()
        return None
    
    def get_all_stream_status(self) -> Dict[str, StreamStatus]:
        """Get status of all streams
        
        Returns:
            Dictionary mapping stream IDs to their status
        """
        return {stream_id: stream.get_status() for stream_id, stream in self.streams.items()}
    
    def get_subscribed_symbols(self, stream_id: Optional[str] = None) -> Set[str]:
        """Get subscribed symbols
        
        Args:
            stream_id: Specific stream ID (optional, returns all if None)
            
        Returns:
            Set of subscribed symbols
        """
        if stream_id:
            return self.stream_symbols.get(stream_id, set()).copy()
        else:
            return set(self.symbol_streams.keys())
    
    def get_latest_data(self, symbol: str, limit: int = 1) -> List[MarketData]:
        """Get latest data for a symbol
        
        Args:
            symbol: Trading symbol
            limit: Number of latest data points to return
            
        Returns:
            List of latest MarketData objects
        """
        if symbol in self.data_buffer:
            return self.data_buffer[symbol][-limit:]
        return []
    
    def get_stream_health(self) -> Dict[str, Any]:
        """Get health information for all streams
        
        Returns:
            Dictionary with stream health information
        """
        health = {}
        
        for stream_id, stream in self.streams.items():
            last_heartbeat = stream.get_last_heartbeat()
            health[stream_id] = {
                "status": stream.get_status().value,
                "subscribed_symbols": len(stream.get_subscribed_symbols()),
                "last_heartbeat": last_heartbeat.isoformat() if last_heartbeat else None,
                "reconnect_attempts": stream.reconnect_attempts
            }
        
        return health
    
    async def _handle_stream_data(self, data: MarketData):
        """Handle incoming stream data
        
        Args:
            data: MarketData object
        """
        # Add to buffer
        symbol = data.symbol
        self.data_buffer[symbol].append(data)
        
        # Maintain buffer size
        if len(self.data_buffer[symbol]) > self.buffer_size:
            self.data_buffer[symbol] = self.data_buffer[symbol][-self.buffer_size:]
        
        # Notify subscribers
        for callback in self.subscribers["data"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(data))
                else:
                    callback(data)
            except Exception as e:
                self.logger.error(f"Error in data subscriber callback: {e}")
    
    async def _handle_stream_status(self, status_data: Dict[str, Any]):
        """Handle stream status changes
        
        Args:
            status_data: Status change data
        """
        # Notify subscribers
        for callback in self.subscribers["status"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(status_data))
                else:
                    callback(status_data)
            except Exception as e:
                self.logger.error(f"Error in status subscriber callback: {e}")
    
    async def _handle_stream_error(self, error_data: Any):
        """Handle stream errors
        
        Args:
            error_data: Error data
        """
        self.logger.error(f"Stream error: {error_data}")
        
        # Notify subscribers
        for callback in self.subscribers["error"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(error_data))
                else:
                    callback(error_data)
            except Exception as e:
                self.logger.error(f"Error in error subscriber callback: {e}")
    
    async def _health_check_loop(self):
        """Periodic health check for all streams"""
        try:
            while True:
                await asyncio.sleep(self.health_check_interval)
                
                current_time = datetime.now()
                
                for stream_id, stream in self.streams.items():
                    # Check if stream is healthy
                    last_heartbeat = stream.get_last_heartbeat()
                    
                    if last_heartbeat:
                        time_since_heartbeat = current_time - last_heartbeat
                        
                        # If no heartbeat for more than 2 minutes, consider unhealthy
                        if time_since_heartbeat > timedelta(minutes=2):
                            self.logger.warning(f"Stream {stream_id} appears unhealthy - no heartbeat for {time_since_heartbeat}")
                            
                            # Trigger reconnection if connected
                            if stream.is_connected():
                                await stream.handle_reconnect()
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error(f"Error in health check loop: {e}")