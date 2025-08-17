"""
Strategy Engine
==============

Dynamic strategy loading and execution engine.
"""

import importlib
import inspect
from typing import Dict, Any, List, Optional, Type
from pathlib import Path
import logging

from .interfaces import IStrategy, TradingContext, Signal, MarketData
from .config_manager import ConfigManager


class StrategyEngine:
    """Manages strategy loading, validation, and execution"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        self.loaded_strategies: Dict[str, Type[IStrategy]] = {}
        self.active_strategies: Dict[str, IStrategy] = {}
        self.strategy_configs = {}
        
    def discover_strategies(self, strategy_path: str = "algoproject/strategies") -> List[str]:
        """Discover available strategy classes"""
        strategy_names = []
        strategy_dir = Path(strategy_path)
        
        if not strategy_dir.exists():
            self.logger.warning(f"Strategy directory not found: {strategy_path}")
            return strategy_names
        
        # Scan for Python files in strategy directories
        for py_file in strategy_dir.rglob("*.py"):
            if py_file.name.startswith("__"):
                continue
                
            try:
                # Convert file path to module path
                module_path = str(py_file.with_suffix("")).replace("/", ".").replace("\\", ".")
                module = importlib.import_module(module_path)
                
                # Find strategy classes
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (issubclass(obj, IStrategy) and 
                        obj != IStrategy and 
                        not inspect.isabstract(obj)):
                        strategy_names.append(f"{module_path}.{name}")
                        self.loaded_strategies[name] = obj
                        
            except Exception as e:
                self.logger.error(f"Error loading strategy from {py_file}: {e}")
        
        return strategy_names
    
    def load_strategy(self, strategy_name: str, parameters: Optional[Dict[str, Any]] = None) -> IStrategy:
        """Load and instantiate a strategy"""
        if strategy_name not in self.loaded_strategies:
            raise ValueError(f"Strategy not found: {strategy_name}")
        
        strategy_class = self.loaded_strategies[strategy_name]
        strategy_instance = strategy_class()
        
        # Set parameters if provided
        if parameters:
            strategy_instance.set_parameters(parameters)
        
        return strategy_instance
    
    def validate_strategy(self, strategy: IStrategy) -> bool:
        """Validate strategy implementation"""
        try:
            # Check required methods
            required_methods = ['initialize', 'next', 'get_parameters', 'set_parameters']
            for method in required_methods:
                if not hasattr(strategy, method):
                    self.logger.error(f"Strategy missing required method: {method}")
                    return False
            
            # Test parameter handling
            params = strategy.get_parameters()
            if not isinstance(params, dict):
                self.logger.error("Strategy get_parameters() must return a dictionary")
                return False
            
            # Test signal generation with dummy data
            dummy_data = MarketData(
                symbol="TEST",
                timestamp=None,
                open=100.0,
                high=105.0,
                low=95.0,
                close=102.0,
                volume=1000.0,
                exchange="test"
            )
            
            signals = strategy.next(dummy_data)
            if not isinstance(signals, list):
                self.logger.error("Strategy next() must return a list of signals")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Strategy validation failed: {e}")
            return False
    
    def start_strategy(self, strategy_name: str, context: TradingContext, 
                      parameters: Optional[Dict[str, Any]] = None) -> bool:
        """Start a strategy with given context"""
        try:
            strategy = self.load_strategy(strategy_name, parameters)
            
            if not self.validate_strategy(strategy):
                return False
            
            strategy.initialize(context)
            self.active_strategies[strategy_name] = strategy
            
            self.logger.info(f"Strategy started: {strategy_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start strategy {strategy_name}: {e}")
            return False
    
    def stop_strategy(self, strategy_name: str) -> bool:
        """Stop a running strategy"""
        if strategy_name in self.active_strategies:
            del self.active_strategies[strategy_name]
            self.logger.info(f"Strategy stopped: {strategy_name}")
            return True
        return False
    
    def process_market_data(self, data: MarketData) -> Dict[str, List[Signal]]:
        """Process market data through all active strategies"""
        all_signals = {}
        
        for strategy_name, strategy in self.active_strategies.items():
            try:
                signals = strategy.next(data)
                all_signals[strategy_name] = signals
            except Exception as e:
                self.logger.error(f"Error processing data in strategy {strategy_name}: {e}")
                all_signals[strategy_name] = []
        
        return all_signals
    
    def get_strategy_info(self, strategy_name: str) -> Dict[str, Any]:
        """Get information about a strategy"""
        if strategy_name not in self.loaded_strategies:
            return {}
        
        strategy_class = self.loaded_strategies[strategy_name]
        return {
            'name': strategy_name,
            'class': strategy_class.__name__,
            'module': strategy_class.__module__,
            'doc': strategy_class.__doc__,
            'active': strategy_name in self.active_strategies
        }
    
    def list_strategies(self) -> List[Dict[str, Any]]:
        """List all available strategies"""
        return [self.get_strategy_info(name) for name in self.loaded_strategies.keys()]
    
    def get_active_strategies(self) -> List[str]:
        """Get list of active strategy names"""
        return list(self.active_strategies.keys())