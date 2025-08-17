"""
Data Provider Interface
=====================

Abstract interface for data providers in AlgoProject.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime

from ..core.interfaces import MarketData


class DataProvider(ABC):
    """Abstract interface for data providers"""
    
    @abstractmethod
    def get_historical_data(self, symbol: str, timeframe: str, 
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None,
                          limit: int = 1000) -> pd.DataFrame:
        """Get historical market data
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe (e.g., '1m', '5m', '1h', '1d')
            start_date: Start date for data (optional)
            end_date: End date for data (optional)
            limit: Maximum number of candles to return
            
        Returns:
            DataFrame with OHLCV data
        """
        pass
    
    @abstractmethod
    def get_live_data(self, symbol: str) -> MarketData:
        """Get latest market data
        
        Args:
            symbol: Trading symbol
            
        Returns:
            MarketData object with latest data
        """
        pass
    
    @abstractmethod
    def get_available_symbols(self, asset_class: str = None) -> List[str]:
        """Get available trading symbols
        
        Args:
            asset_class: Filter by asset class (optional)
            
        Returns:
            List of available symbols
        """
        pass
    
    @abstractmethod
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get information about a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Dictionary with symbol information
        """
        pass