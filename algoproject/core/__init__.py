"""
AlgoProject Core Module
======================

Core trading engine and shared components for the AlgoProject platform.
"""

__version__ = "2.0.0"
__author__ = "AlgoProject Team"

from .strategy_engine import StrategyEngine
from .kpi_calculator import KPICalculator
from .trade_executor import TradeExecutor
from .risk_manager import RiskManager
from .config_manager import ConfigManager

__all__ = [
    'StrategyEngine',
    'KPICalculator', 
    'TradeExecutor',
    'RiskManager',
    'ConfigManager'
]