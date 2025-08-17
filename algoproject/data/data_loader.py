"""
Data Loader
===========

Unified data loading interface for AlgoProject.
"""

import pandas as pd
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..core.interfaces import MarketData
from ..core.config_manager import ConfigManager
from .data_provider import DataProvider


class DataLoader:
    """Unified data loading interface"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        self.providers: Dict[str, DataProvider] = {}
        self.default_provider = None
    
    def register_provider(self, name: str, provider: DataProvider, is_default: bool = False):
        """Register a data provider
        
        Args:
            name: Provider name
            provider: DataProvider instance
            is_default: Set as default provider
        """
        self.providers[name] = provider
        if is_default or self.default_provider is None:
            self.default_provider = name
        self.logger.info(f"Registered data provider: {name}")
    
    def get_historical_data(self, symbol: str, timeframe: str, 
                          provider: str = None,
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None,
                          limit: int = 1000) -> pd.DataFrame:
        """Get historical market data
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe (e.g., '1m', '5m', '1h', '1d')
            provider: Provider name (optional, uses default if None)
            start_date: Start date for data (optional)
            end_date: End date for data (optional)
            limit: Maximum number of candles to return
            
        Returns:
            DataFrame with OHLCV data
        """
        provider_name = provider or self.default_provider
        if provider_name not in self.providers:
            raise ValueError(f"Provider not found: {provider_name}")
        
        try:
            return self.providers[provider_name].get_historical_data(
                symbol, timeframe, start_date, end_date, limit
            )
        except Exception as e:
            self.logger.error(f"Error getting historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_available_symbols(self, asset_class: str = None, provider: str = None) -> List[str]:
        """Get available trading symbols
        
        Args:
            asset_class: Filter by asset class (optional)
            provider: Provider name (optional, uses default if None)
            
        Returns:
            List of available symbols
        """
        provider_name = provider or self.default_provider
        if provider_name not in self.providers:
            raise ValueError(f"Provider not found: {provider_name}")
        
        try:
            return self.providers[provider_name].get_available_symbols(asset_class)
        except Exception as e:
            self.logger.error(f"Error getting available symbols: {e}")
            return []