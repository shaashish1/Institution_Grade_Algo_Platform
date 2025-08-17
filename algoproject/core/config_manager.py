"""
Configuration Manager
====================

Centralized configuration management for AlgoProject.
"""

import yaml
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """Manages application configuration from YAML/JSON files"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self._config_cache = {}
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Ensure config directory exists"""
        self.config_dir.mkdir(exist_ok=True)
    
    def load_config(self, config_name: str) -> Dict[str, Any]:
        """Load configuration from file"""
        if config_name in self._config_cache:
            return self._config_cache[config_name]
        
        # Try YAML first, then JSON
        yaml_path = self.config_dir / f"{config_name}.yaml"
        json_path = self.config_dir / f"{config_name}.json"
        
        config = {}
        
        if yaml_path.exists():
            with open(yaml_path, 'r') as f:
                config = yaml.safe_load(f) or {}
        elif json_path.exists():
            with open(json_path, 'r') as f:
                config = json.load(f)
        else:
            # Create default config
            config = self._create_default_config(config_name)
            self.save_config(config_name, config)
        
        self._config_cache[config_name] = config
        return config
    
    def save_config(self, config_name: str, config: Dict[str, Any], format: str = "yaml"):
        """Save configuration to file"""
        if format == "yaml":
            file_path = self.config_dir / f"{config_name}.yaml"
            with open(file_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
        else:
            file_path = self.config_dir / f"{config_name}.json"
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=2)
        
        self._config_cache[config_name] = config
    
    def get_setting(self, config_name: str, key: str, default: Any = None) -> Any:
        """Get specific setting from config"""
        config = self.load_config(config_name)
        return config.get(key, default)
    
    def set_setting(self, config_name: str, key: str, value: Any):
        """Set specific setting in config"""
        config = self.load_config(config_name)
        config[key] = value
        self.save_config(config_name, config)
    
    def _create_default_config(self, config_name: str) -> Dict[str, Any]:
        """Create default configuration based on config name"""
        defaults = {
            "app_config": {
                "debug": False,
                "log_level": "INFO",
                "max_workers": 4,
                "cache_enabled": True,
                "cache_ttl": 3600
            },
            "strategy_config": {
                "default_risk_per_trade": 0.02,
                "max_positions": 10,
                "stop_loss_pct": 0.05,
                "take_profit_pct": 0.10,
                "position_sizing": "fixed"
            },
            "exchange_config": {
                "crypto": {
                    "default_exchange": "binance",
                    "supported_exchanges": ["binance", "bybit", "okx", "kucoin"],
                    "rate_limit": 1200,
                    "timeout": 30
                },
                "stocks": {
                    "default_broker": "fyers",
                    "supported_brokers": ["fyers"],
                    "rate_limit": 100,
                    "timeout": 30
                }
            },
            "thresholds": {
                "profit_factor": {
                    "excellent": 1.5,
                    "good": 1.2,
                    "acceptable": 1.0
                },
                "sharpe_ratio": {
                    "excellent": 1.5,
                    "good": 1.0,
                    "acceptable": 0.5
                },
                "max_drawdown": {
                    "acceptable": 0.10,
                    "warning": 0.15,
                    "critical": 0.20
                }
            }
        }
        
        return defaults.get(config_name, {})
    
    def validate_config(self, config_name: str) -> List[str]:
        """Validate configuration and return list of issues"""
        config = self.load_config(config_name)
        issues = []
        
        if config_name == "app_config":
            if not isinstance(config.get("max_workers"), int) or config.get("max_workers") < 1:
                issues.append("max_workers must be a positive integer")
            
            if config.get("log_level") not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
                issues.append("log_level must be one of: DEBUG, INFO, WARNING, ERROR")
        
        elif config_name == "strategy_config":
            risk = config.get("default_risk_per_trade", 0)
            if not isinstance(risk, (int, float)) or risk <= 0 or risk > 1:
                issues.append("default_risk_per_trade must be between 0 and 1")
        
        return issues
    
    def reload_config(self, config_name: str = None):
        """Reload configuration from disk"""
        if config_name:
            self._config_cache.pop(config_name, None)
        else:
            self._config_cache.clear()