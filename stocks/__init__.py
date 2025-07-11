"""
Stocks Trading Module
====================

Stock trading functionality including Fyers API integration,
backtesting, and live trading capabilities for NSE/BSE markets.
"""

__version__ = "1.0.0"
__author__ = "AlgoProject Team"

# Import key components
try:
    from .simple_fyers_provider import fetch_nse_stock_data, SimpleFyersDataProvider
    from .fyers_data_provider import FyersDataProvider
except ImportError:
    # Allow module to load even if some components fail
    pass
