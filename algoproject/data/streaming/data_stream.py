"""
Data Stream
===========

Real-time data streaming interface for AlgoProject.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Callable, Set
from datetime import datetime
from abc import ABC, abstractmethod
from enum import Enum

from ...core.interfaces import MarketData


class StreamStatus(Enum):
    """Stream status enumeration"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    ERROR = "error"


class DataStream(ABC):
    """Abstract base class for real-time data streams"""
    
    def __init__(self, stream_id: str):
        self.stream_id = stream_id
        self.status = StreamStatus.DISCONNECTED
        self.logger = logging.getLogger(f"{__name__}.{stream_id}")
        self.subscribers: Dict[str, List[Callable]] = {}
        self.subscribed_symbols: Set[str] = set()
        self.last_heartbeat = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 5  # seconds
        
    @abstractmethod
    async def connect(self) -> bool:
        """Connect to the data stream
        
        Returns:
            True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def disconnect(self):
        """Disconnect from the data stream"""
        pass
    
    @abstractmethod
    async def subscribe(self, symbol: str, data_type: str = "ticker"):
        """Subscribe to a symbol
        
        Args:
            symbol: Trading symbol to subscribe to
            data_type: Type of data (ticker, orderbook, trades)
        """
        pass
    
    @abstractmethod
    async def unsubscribe(self, symbol: str, data_type: str = "ticker"):
        """Unsubscribe from a symbol
        
        Args:
            symbol: Trading symbol to unsubscribe from
            data_type: Type of data (ticker, orderbook, trades)
        """
        pass
    
    def add_subscriber(self, event_type: str, callback: Callable):
        """Add a callback for stream events
        
        Args:
            event_type: Type of event (data, status, error)
            callback: Callback function
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def remove_subscriber(self, event_type: str, callback: Callable):
        """Remove a callback for stream events
        
        Args:
            event_type: Type of event
            callback: Callback function to remove
        """
        if event_type in self.subscribers:
            try:
                self.subscribers[event_type].remove(callback)
            except ValueError:
                pass
    
    def notify_subscribers(self, event_type: str, data: Any):
        """Notify all subscribers of an event
        
        Args:
            event_type: Type of event
            data: Event data
        """
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        asyncio.create_task(callback(data))
                    else:
                        callback(data)
                except Exception as e:
                    self.logger.error(f"Error in subscriber callback: {e}")
    
    def set_status(self, status: StreamStatus):
        """Set stream status and notify subscribers
        
        Args:
            status: New stream status
        """
        old_status = self.status
        self.status = status
        self.logger.info(f"Stream status changed: {old_status.value} -> {status.value}")
        self.notify_subscribers("status", {"old": old_status, "new": status})
    
    async def handle_reconnect(self):
        """Handle automatic reconnection"""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            self.logger.error("Max reconnection attempts reached")
            self.set_status(StreamStatus.ERROR)
            return
        
        self.reconnect_attempts += 1
        self.set_status(StreamStatus.RECONNECTING)
        
        await asyncio.sleep(self.reconnect_delay)
        
        try:
            if await self.connect():
                self.reconnect_attempts = 0
                # Re-subscribe to all symbols
                for symbol in self.subscribed_symbols.copy():
                    await self.subscribe(symbol)
            else:
                await self.handle_reconnect()
        except Exception as e:
            self.logger.error(f"Reconnection failed: {e}")
            await self.handle_reconnect()
    
    def get_status(self) -> StreamStatus:
        """Get current stream status
        
        Returns:
            Current stream status
        """
        return self.status
    
    def is_connected(self) -> bool:
        """Check if stream is connected
        
        Returns:
            True if connected, False otherwise
        """
        return self.status == StreamStatus.CONNECTED
    
    def get_subscribed_symbols(self) -> Set[str]:
        """Get set of subscribed symbols
        
        Returns:
            Set of subscribed symbols
        """
        return self.subscribed_symbols.copy()
    
    def update_heartbeat(self):
        """Update last heartbeat timestamp"""
        self.last_heartbeat = datetime.now()
    
    def get_last_heartbeat(self) -> Optional[datetime]:
        """Get last heartbeat timestamp
        
        Returns:
            Last heartbeat timestamp or None
        """
        return self.last_heartbeat