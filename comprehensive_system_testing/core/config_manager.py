"""
Configuration Manager
====================

Handles test configuration and loading system.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List

from .models import TestConfiguration, Severity
from ..utils.file_utils import FileUtils
from ..utils.logger import TestLogger


class ConfigManager:
    """Manages test configuration and customization"""
    
    def __init__(self, config_directory: str = "comprehensive_system_testing/config"):
        self.config_directory = Path(config_directory)
        self.logger = TestLogger()
        self._cached_config = None
    
    def load_configuration(self) -> TestConfiguration:
        """Load complete test configuration"""
        if self._cached_config is not None:
            return self._cached_config
        
        try:
            # Load main configuration
            main_config = self._load_main_config()
            
            # Load validation rules
            validation_rules = self._load_validation_rules()
            
            # Load crypto-specific rules
            crypto_rules = self._load_crypto_rules()
            
            # Load stock-specific rules
            stock_rules = self._load_stock_rules()
            
            # Load fix patterns
            fix_patterns = self._load_fix_patterns()
            
            # Merge all configurations
            merged_config = self._merge_configurations(
                main_config, validation_rules, crypto_rules, stock_rules, fix_patterns
            )
            
            # Create TestConfiguration object
            config = TestConfiguration(
                enabled_tests=merged_config.get("enabled_tests", []),
                auto_fix_enabled=merged_config.get("auto_fix", {}).get("enabled", True),
                severity_threshold=Severity(merged_config.get("general", {}).get("severity_threshold", "MEDIUM")),
                timeout_seconds=merged_config.get("general", {}).get("timeout_seconds", 300),
                parallel_execution=merged_config.get("general", {}).get("parallel_execution", True),
                report_formats=merged_config.get("reporting", {}).get("formats", ["html", "console"]),
                notification_settings=merged_config.get("notifications", {})
            )
            
            self._cached_config = config
            self.logger.info("Configuration loaded successfully")
            return config
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            # Return default configuration
            return TestConfiguration()
    
    def _load_main_config(self) -> Dict[str, Any]:
        """Load main test configuration"""
        config_file = self.config_directory / "test_config.yaml"
        
        if not config_file.exists():
            self.logger.warning(f"Main config file not found: {config_file}")
            return {}
        
        content = FileUtils.read_file_safe(str(config_file))
        if content is None:
            return {}
        
        try:
            return yaml.safe_load(content) or {}
        except yaml.YAMLError as e:
            self.logger.error(f"Failed to parse main config: {e}")
            return {}
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load general validation rules"""
        rules_file = self.config_directory / "validation_rules.json"
        
        if not rules_file.exists():
            return {}
        
        content = FileUtils.read_file_safe(str(rules_file))
        if content is None:
            return {}
        
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse validation rules: {e}")
            return {}
    
    def _load_crypto_rules(self) -> Dict[str, Any]:
        """Load crypto-specific rules"""
        crypto_file = self.config_directory / "crypto_test_rules.json"
        
        if not crypto_file.exists():
            return {}
        
        content = FileUtils.read_file_safe(str(crypto_file))
        if content is None:
            return {}
        
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse crypto rules: {e}")
            return {}
    
    def _load_stock_rules(self) -> Dict[str, Any]:
        """Load stock-specific rules"""
        stock_file = self.config_directory / "stock_test_rules.json"
        
        if not stock_file.exists():
            return {}
        
        content = FileUtils.read_file_safe(str(stock_file))
        if content is None:
            return {}
        
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse stock rules: {e}")
            return {}
    
    def _load_fix_patterns(self) -> Dict[str, Any]:
        """Load auto-fix patterns"""
        patterns_file = self.config_directory / "fix_patterns.yaml"
        
        if not patterns_file.exists():
            return {}
        
        content = FileUtils.read_file_safe(str(patterns_file))
        if content is None:
            return {}
        
        try:
            return yaml.safe_load(content) or {}
        except yaml.YAMLError as e:
            self.logger.error(f"Failed to parse fix patterns: {e}")
            return {}
    
    def _merge_configurations(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple configuration dictionaries"""
        merged = {}
        
        for config in configs:
            if config:
                merged = self._deep_merge(merged, config)
        
        return merged
    
    def _deep_merge(self, dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries"""
        result = dict1.copy()
        
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get_crypto_rules(self) -> Dict[str, Any]:
        """Get crypto-specific testing rules"""
        return self._load_crypto_rules()
    
    def get_stock_rules(self) -> Dict[str, Any]:
        """Get stock-specific testing rules"""
        return self._load_stock_rules()
    
    def get_fix_patterns(self) -> Dict[str, Any]:
        """Get auto-fix patterns"""
        return self._load_fix_patterns()
    
    def validate_configuration(self) -> List[str]:
        """Validate configuration files and return issues"""
        issues = []
        
        # Check if main config exists
        main_config_file = self.config_directory / "test_config.yaml"
        if not main_config_file.exists():
            issues.append("Main configuration file (test_config.yaml) not found")
        
        # Validate each config file
        config_files = [
            ("test_config.yaml", "yaml"),
            ("validation_rules.json", "json"),
            ("crypto_test_rules.json", "json"),
            ("stock_test_rules.json", "json"),
            ("fix_patterns.yaml", "yaml")
        ]
        
        for filename, file_type in config_files:
            file_path = self.config_directory / filename
            if file_path.exists():
                content = FileUtils.read_file_safe(str(file_path))
                if content is None:
                    issues.append(f"Could not read {filename}")
                    continue
                
                try:
                    if file_type == "yaml":
                        yaml.safe_load(content)
                    elif file_type == "json":
                        json.loads(content)
                except Exception as e:
                    issues.append(f"Invalid {file_type.upper()} in {filename}: {str(e)}")
        
        return issues
    
    def create_default_configuration(self) -> bool:
        """Create default configuration files if they don't exist"""
        try:
            self.config_directory.mkdir(parents=True, exist_ok=True)
            
            # Create default main config if it doesn't exist
            main_config_file = self.config_directory / "test_config.yaml"
            if not main_config_file.exists():
                default_config = {
                    "general": {
                        "auto_fix_enabled": True,
                        "parallel_execution": True,
                        "timeout_seconds": 300,
                        "severity_threshold": "MEDIUM"
                    },
                    "enabled_tests": [
                        "syntax_validation",
                        "import_testing",
                        "dependency_checking",
                        "configuration_validation",
                        "integration_testing"
                    ],
                    "reporting": {
                        "formats": ["html", "console", "json"],
                        "output_directory": "test_reports",
                        "include_details": True
                    },
                    "auto_fix": {
                        "enabled": True,
                        "create_backups": True,
                        "max_fixes_per_file": 10
                    }
                }
                
                with open(main_config_file, 'w') as f:
                    yaml.dump(default_config, f, default_flow_style=False, indent=2)
                
                self.logger.info(f"Created default configuration: {main_config_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create default configuration: {e}")
            return False
    
    def update_configuration(self, updates: Dict[str, Any]) -> bool:
        """Update configuration with new values"""
        try:
            # Load current configuration
            current_config = self._load_main_config()
            
            # Merge updates
            updated_config = self._deep_merge(current_config, updates)
            
            # Save updated configuration
            main_config_file = self.config_directory / "test_config.yaml"
            with open(main_config_file, 'w') as f:
                yaml.dump(updated_config, f, default_flow_style=False, indent=2)
            
            # Clear cached config to force reload
            self._cached_config = None
            
            self.logger.info("Configuration updated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update configuration: {e}")
            return False
    
    def get_configuration_info(self) -> Dict[str, Any]:
        """Get information about current configuration"""
        config = self.load_configuration()
        
        return {
            "config_directory": str(self.config_directory),
            "enabled_tests": config.enabled_tests,
            "auto_fix_enabled": config.auto_fix_enabled,
            "severity_threshold": config.severity_threshold.value,
            "timeout_seconds": config.timeout_seconds,
            "parallel_execution": config.parallel_execution,
            "report_formats": config.report_formats,
            "configuration_files": [
                str(f.name) for f in self.config_directory.glob("*") 
                if f.is_file() and f.suffix in ['.yaml', '.yml', '.json']
            ]
        }