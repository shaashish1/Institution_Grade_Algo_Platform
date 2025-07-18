"""
Unit Tests for Configuration Manager
===================================

Test cases for the ConfigManager class.
"""

import unittest
import tempfile
import json
import yaml
from pathlib import Path

from ..core.config_manager import ConfigManager
from ..core.models import TestConfiguration, Severity


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_manager = ConfigManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_config_file(self, filename: str, content: dict, file_type: str = "yaml"):
        """Create a test configuration file"""
        file_path = Path(self.temp_dir) / filename
        
        with open(file_path, 'w') as f:
            if file_type == "yaml":
                yaml.dump(content, f)
            elif file_type == "json":
                json.dump(content, f, indent=2)
    
    def test_load_default_configuration(self):
        """Test loading default configuration when no files exist"""
        config = self.config_manager.load_configuration()
        
        self.assertIsInstance(config, TestConfiguration)
        self.assertIsInstance(config.enabled_tests, list)
        self.assertIsInstance(config.auto_fix_enabled, bool)
    
    def test_load_main_configuration(self):
        """Test loading main configuration file"""
        main_config = {
            "general": {
                "auto_fix_enabled": True,
                "timeout_seconds": 600,
                "severity_threshold": "HIGH"
            },
            "enabled_tests": ["syntax_validation", "import_testing"]
        }
        
        self._create_config_file("test_config.yaml", main_config)
        
        config = self.config_manager.load_configuration()
        
        self.assertEqual(config.timeout_seconds, 600)
        self.assertEqual(config.severity_threshold, Severity.HIGH)
        self.assertIn("syntax_validation", config.enabled_tests)
    
    def test_load_validation_rules(self):
        """Test loading validation rules"""
        validation_rules = {
            "general_validation_rules": {
                "python_syntax": {
                    "ast_parsing": True,
                    "indentation_check": True
                }
            }
        }
        
        self._create_config_file("validation_rules.json", validation_rules, "json")
        
        rules = self.config_manager._load_validation_rules()
        self.assertIn("general_validation_rules", rules)
        self.assertTrue(rules["general_validation_rules"]["python_syntax"]["ast_parsing"])
    
    def test_load_crypto_rules(self):
        """Test loading crypto-specific rules"""
        crypto_rules = {
            "crypto_specific_rules": {
                "ccxt_integration": {
                    "required_exchanges": ["binance", "coinbase"]
                }
            }
        }
        
        self._create_config_file("crypto_test_rules.json", crypto_rules, "json")
        
        rules = self.config_manager.get_crypto_rules()
        self.assertIn("crypto_specific_rules", rules)
        self.assertIn("binance", rules["crypto_specific_rules"]["ccxt_integration"]["required_exchanges"])
    
    def test_configuration_validation(self):
        """Test configuration validation"""
        # Create valid config files
        self._create_config_file("test_config.yaml", {"general": {"auto_fix_enabled": True}})
        self._create_config_file("validation_rules.json", {"rules": {}}, "json")
        
        issues = self.config_manager.validate_configuration()
        
        # Should have no issues with valid files
        self.assertEqual(len(issues), 0)
    
    def test_configuration_validation_with_invalid_files(self):
        """Test configuration validation with invalid files"""
        # Create invalid YAML file
        invalid_yaml_path = Path(self.temp_dir) / "test_config.yaml"
        with open(invalid_yaml_path, 'w') as f:
            f.write("invalid: yaml: content: [")
        
        issues = self.config_manager.validate_configuration()
        
        # Should detect invalid YAML
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("Invalid YAML" in issue for issue in issues))
    
    def test_create_default_configuration(self):
        """Test creating default configuration files"""
        success = self.config_manager.create_default_configuration()
        
        self.assertTrue(success)
        
        # Check if default config file was created
        default_config_path = Path(self.temp_dir) / "test_config.yaml"
        self.assertTrue(default_config_path.exists())
        
        # Verify content
        with open(default_config_path, 'r') as f:
            content = yaml.safe_load(f)
        
        self.assertIn("general", content)
        self.assertIn("enabled_tests", content)
    
    def test_update_configuration(self):
        """Test updating configuration"""
        # Create initial config
        initial_config = {"general": {"timeout_seconds": 300}}
        self._create_config_file("test_config.yaml", initial_config)
        
        # Update configuration
        updates = {"general": {"timeout_seconds": 600, "auto_fix_enabled": True}}
        success = self.config_manager.update_configuration(updates)
        
        self.assertTrue(success)
        
        # Verify update
        updated_config = self.config_manager._load_main_config()
        self.assertEqual(updated_config["general"]["timeout_seconds"], 600)
        self.assertTrue(updated_config["general"]["auto_fix_enabled"])
    
    def test_deep_merge(self):
        """Test deep merging of configuration dictionaries"""
        dict1 = {
            "level1": {
                "level2": {
                    "key1": "value1",
                    "key2": "value2"
                }
            }
        }
        
        dict2 = {
            "level1": {
                "level2": {
                    "key2": "updated_value2",
                    "key3": "value3"
                },
                "new_key": "new_value"
            }
        }
        
        merged = self.config_manager._deep_merge(dict1, dict2)
        
        self.assertEqual(merged["level1"]["level2"]["key1"], "value1")
        self.assertEqual(merged["level1"]["level2"]["key2"], "updated_value2")
        self.assertEqual(merged["level1"]["level2"]["key3"], "value3")
        self.assertEqual(merged["level1"]["new_key"], "new_value")
    
    def test_get_configuration_info(self):
        """Test getting configuration information"""
        info = self.config_manager.get_configuration_info()
        
        self.assertIn("config_directory", info)
        self.assertIn("enabled_tests", info)
        self.assertIn("auto_fix_enabled", info)
        self.assertIn("configuration_files", info)


if __name__ == '__main__':
    unittest.main()