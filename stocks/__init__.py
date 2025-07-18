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
    from .data_acquisition import fetch_data, get_live_quote, health_check
    # Only import full Fyers provider if fyers-apiv3 is available (for stock trading)
    try:
        from fyers_apiv3 import fyersModel
        from .fyers_data_provider import FyersDataProvider
    except ImportError:
        # fyers-apiv3 not available - this is OK for crypto-only usage
        FyersDataProvider = None
except ImportError:
    # Allow module to load even if some components fail
    pass
