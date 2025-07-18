"""
AlgoProject Trading Platform
===========================

Complete trading platform for crypto and stock trading with backtesting,
demo trading, and live trading capabilities.
"""

__version__ = "1.0.0"
__author__ = "AlgoProject Team"

# Core trading platform components
from .crypto import CryptoTrader
from .strategies import StrategyManager
from .backtesting import BacktestEngine
from .demo import DemoTrader

# Import from root-level modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from stocks import fyers_data_provider as StockTrader
except ImportError:
    StockTrader = None

__all__ = [
    'CryptoTrader',
    'StrategyManager',
    'BacktestEngine',
    'DemoTrader'
]

# Add StockTrader to exports if available
if StockTrader:
    __all__.append('StockTrader')