"""
Integration Tester
=================

Tests module interactions and API integrations for crypto and stock trading.
"""

import time
import sys
import importlib
from pathlib import Path
from typing import List, Dict, Any, Optional

from .base_tester import BaseTester
from .models import TestResult, TestStatus, Severity, TestConfiguration
from ..utils.process_utils import ProcessUtils
from ..utils.logger import TestLogger


class IntegrationTester(BaseTester):
    """Tests integration between modules and external APIs"""
    
    def __init__(self, config: TestConfiguration):
        super().__init__(config)
        self.logger = TestLogger()
    
    def run_tests(self, target: str) -> List[TestResult]:
        """
        Run integration tests on the target directory
        
        Args:
            target: Directory path to test integrations
            
        Returns:
            List of TestResult objects
        """
        results = []
        start_time = time.time()
        
        self.logger.info("Starting integration testing")
        
        # Test crypto integrations
        crypto_results = self._test_crypto_integration(target)
        results.extend(crypto_results)
        
        # Test stock integrations
        stock_results = self._test_stock_integration(target)
        results.extend(stock_results)
        
        # Test strategy integrations
        strategy_results = self._test_strategy_integration(target)
        results.extend(strategy_results)
        
        # Test data flow
        data_flow_result = self._test_data_flow(target)
        results.append(data_flow_result)
        
        execution_time = time.time() - start_time
        self.logger.info(f"Integration testing completed in {execution_time:.2f} seconds")
        
        return results
    
    def _test_crypto_integration(self, target: str) -> List[TestResult]:
        """Test cryptocurrency integration components"""
        results = []
        
        # Test CCXT integration
        ccxt_result = self._test_ccxt_integration()
        results.append(ccxt_result)
        
        # Test crypto data acquisition
        crypto_data_result = self._test_crypto_data_acquisition(target)
        results.append(crypto_data_result)
        
        # Test crypto asset management
        crypto_assets_result = self._test_crypto_asset_management(target)
        results.append(crypto_assets_result)
        
        return results
    
    def _test_ccxt_integration(self) -> TestResult:
        """Test CCXT library integration"""
        try:
            # Try to import CCXT
            import ccxt
            
            # Test basic CCXT functionality
            exchanges_available = len(ccxt.exchanges)
            
            # Try to create a test exchange instance
            test_exchanges = ['binance', 'coinbase', 'kraken']
            working_exchanges = []
            
            for exchange_name in test_exchanges:
                try:
                    if hasattr(ccxt, exchange_name):
                        exchange_class = getattr(ccxt, exchange_name)
                        exchange = exchange_class({'sandbox': True, 'enableRateLimit': True})
                        working_exchanges.append(exchange_name)
                except Exception:
                    pass  # Exchange creation failed, skip
            
            if working_exchanges:
                return TestResult(
                    component="integration_tester",
                    test_name="ccxt_integration",
                    status=TestStatus.PASS,
                    message=f"CCXT integration working ({len(working_exchanges)} exchanges available)",
                    details={
                        "ccxt_version": ccxt.__version__,
                        "total_exchanges": exchanges_available,
                        "working_exchanges": working_exchanges
                    }
                )
            else:
                return TestResult(
                    component="integration_tester",
                    test_name="ccxt_integration",
                    status=TestStatus.WARNING,
                    message="CCXT library available but no test exchanges working",
                    severity=Severity.MEDIUM,
                    details={
                        "ccxt_version": ccxt.__version__,
                        "total_exchanges": exchanges_available,
                        "tested_exchanges": test_exchanges
                    }
                )
                
        except ImportError:
            return TestResult(
                component="integration_tester",
                test_name="ccxt_integration",
                status=TestStatus.FAIL,
                message="CCXT library not available",
                severity=Severity.HIGH,
                details={"error": "ImportError: ccxt not installed"}
            )
        except Exception as e:
            return TestResult(
                component="integration_tester",
                test_name="ccxt_integration",
                status=TestStatus.FAIL,
                message=f"CCXT integration error: {str(e)}",
                severity=Severity.HIGH,
                details={"error": str(e)}
            )
    
    def _test_crypto_data_acquisition(self, target: str) -> TestResult:
        """Test crypto data acquisition module"""
        try:
            # Try to import crypto data acquisition module
            sys.path.insert(0, target)
            
            try:
                from crypto.data_acquisition import fetch_data, health_check
                
                # Test health check function
                health_status = health_check()
                
                if health_status.get('status') == 'healthy':
                    return TestResult(
                        component="integration_tester",
                        test_name="crypto_data_acquisition",
                        status=TestStatus.PASS,
                        message="Crypto data acquisition module working",
                        details={
                            "health_status": health_status,
                            "ccxt_available": health_status.get('ccxt_available', False),
                            "working_exchanges": health_status.get('working_exchanges', [])
                        }
                    )
                else:
                    return TestResult(
                        component="integration_tester",
                        test_name="crypto_data_acquisition",
                        status=TestStatus.WARNING,
                        message="Crypto data acquisition module has issues",
                        severity=Severity.MEDIUM,
                        details={"health_status": health_status}
                    )
                    
            except ImportError as e:
                return TestResult(
                    component="integration_tester",
                    test_name="crypto_data_acquisition",
                    status=TestStatus.FAIL,
                    message="Could not import crypto data acquisition module",
                    severity=Severity.HIGH,
                    details={"error": str(e)}
                )
                
        except Exception as e:
            return TestResult(
                component="integration_tester",
                test_name="crypto_data_acquisition",
                status=TestStatus.FAIL,
                message=f"Error testing crypto data acquisition: {str(e)}",
                severity=Severity.MEDIUM,
                details={"error": str(e)}
            )
    
    def _test_crypto_asset_management(self, target: str) -> TestResult:
        """Test crypto asset management"""
        try:
            # Check for crypto assets CSV file
            crypto_assets_path = Path(target) / "crypto" / "input" / "crypto_assets.csv"
            
            if not crypto_assets_path.exists():
                return TestResult(
                    component="integration_tester",
                    test_name="crypto_asset_management",
                    status=TestStatus.WARNING,
                    message="Crypto assets file not found",
                    severity=Severity.MEDIUM,
                    details={"expected_path": str(crypto_assets_path)}
                )
            
            # Try to read and validate crypto assets
            with open(crypto_assets_path, 'r') as f:
                content = f.read()
                lines = content.strip().split('\n')
                
                if len(lines) < 2:  # Header + at least one asset
                    return TestResult(
                        component="integration_tester",
                        test_name="crypto_asset_management",
                        status=TestStatus.WARNING,
                        message="Crypto assets file appears empty",
                        severity=Severity.MEDIUM,
                        details={"file_path": str(crypto_assets_path), "line_count": len(lines)}
                    )
                
                return TestResult(
                    component="integration_tester",
                    test_name="crypto_asset_management",
                    status=TestStatus.PASS,
                    message=f"Crypto assets file valid ({len(lines)-1} assets)",
                    details={
                        "file_path": str(crypto_assets_path),
                        "asset_count": len(lines) - 1,
                        "header": lines[0] if lines else None
                    }
                )
                
        except Exception as e:
            return TestResult(
                component="integration_tester",
                test_name="crypto_asset_management",
                status=TestStatus.FAIL,
                message=f"Error testing crypto asset management: {str(e)}",
                severity=Severity.MEDIUM,
                details={"error": str(e)}
            )
    
    def _test_stock_integration(self, target: str) -> List[TestResult]:
        """Test stock trading integration components"""
        results = []
        
        # Test Fyers integration
        fyers_result = self._test_fyers_integration(target)
        results.append(fyers_result)
        
        # Test Yahoo Finance integration
        yfinance_result = self._test_yfinance_integration()
        results.append(yfinance_result)
        
        # Test stock asset management
        stock_assets_result = self._test_stock_asset_management(target)
        results.append(stock_assets_result)
        
        return results
    
    def _test_fyers_integration(self, target: str) -> TestResult:
        """Test Fyers API integration"""
        try:
            # Try to import Fyers modules
            sys.path.insert(0, target)
            
            try:
                from stocks.fyers_data_provider import FyersDataProvider
                
                # Check for Fyers credentials
                fyers_cred_path = Path(target) / "stocks" / "fyers" / "access_token.py"
                
                if not fyers_cred_path.exists():
                    return TestResult(
                        component="integration_tester",
                        test_name="fyers_integration",
                        status=TestStatus.WARNING,
                        message="Fyers credentials file not found",
                        severity=Severity.MEDIUM,
                        details={"expected_path": str(fyers_cred_path)}
                    )
                
                return TestResult(
                    component="integration_tester",
                    test_name="fyers_integration",
                    status=TestStatus.PASS,
                    message="Fyers integration components available",
                    details={"credentials_file": str(fyers_cred_path)}
                )
                
            except ImportError as e:
                # Check if fyers-apiv3 is available
                try:
                    import fyers_apiv3
                    return TestResult(
                        component="integration_tester",
                        test_name="fyers_integration",
                        status=TestStatus.WARNING,
                        message="Fyers API library available but integration module has issues",
                        severity=Severity.MEDIUM,
                        details={"error": str(e)}
                    )
                except ImportError:
                    return TestResult(
                        component="integration_tester",
                        test_name="fyers_integration",
                        status=TestStatus.WARNING,
                        message="Fyers API library not installed (optional for crypto-only usage)",
                        severity=Severity.LOW,
                        details={"note": "This is expected if focusing on crypto trading"}
                    )
                    
        except Exception as e:
            return TestResult(
                component="integration_tester",
                test_name="fyers_integration",
                status=TestStatus.FAIL,
                message=f"Error testing Fyers integration: {str(e)}",
                severity=Severity.MEDIUM,
                details={"error": str(e)}
            )
    
    def _test_yfinance_integration(self) -> TestResult:
        """Test Yahoo Finance integration"""
        try:
            import yfinance as yf
            
            # Test basic yfinance functionality
            # This is a lightweight test that doesn't make actual API calls
            ticker = yf.Ticker("AAPL")
            
            return TestResult(
                component="integration_tester",
                test_name="yfinance_integration",
                status=TestStatus.PASS,
                message="Yahoo Finance integration available",
                details={"yfinance_available": True}
            )
            
        except ImportError:
            return TestResult(
                component="integration_tester",
                test_name="yfinance_integration",
                status=TestStatus.WARNING,
                message="Yahoo Finance library not available",
                severity=Severity.MEDIUM,
                details={"error": "yfinance not installed"}
            )
        except Exception as e:
            return TestResult(
                component="integration_tester",
                test_name="yfinance_integration",
                status=TestStatus.FAIL,
                message=f"Yahoo Finance integration error: {str(e)}",
                severity=Severity.MEDIUM,
                details={"error": str(e)}
            )
    
    def _test_stock_asset_management(self, target: str) -> TestResult:
        """Test stock asset management"""
        try:
            # Check for stock assets CSV file
            stock_assets_path = Path(target) / "stocks" / "input" / "stocks_assets.csv"
            
            if not stock_assets_path.exists():
                return TestResult(
                    component="integration_tester",
                    test_name="stock_asset_management",
                    status=TestStatus.WARNING,
                    message="Stock assets file not found",
                    severity=Severity.MEDIUM,
                    details={"expected_path": str(stock_assets_path)}
                )
            
            # Try to read and validate stock assets
            with open(stock_assets_path, 'r') as f:
                content = f.read()
                lines = content.strip().split('\n')
                
                if len(lines) < 2:  # Header + at least one asset
                    return TestResult(
                        component="integration_tester",
                        test_name="stock_asset_management",
                        status=TestStatus.WARNING,
                        message="Stock assets file appears empty",
                        severity=Severity.MEDIUM,
                        details={"file_path": str(stock_assets_path), "line_count": len(lines)}
                    )
                
                return TestResult(
                    component="integration_tester",
                    test_name="stock_asset_management",
                    status=TestStatus.PASS,
                    message=f"Stock assets file valid ({len(lines)-1} assets)",
                    details={
                        "file_path": str(stock_assets_path),
                        "asset_count": len(lines) - 1,
                        "header": lines[0] if lines else None
                    }
                )
                
        except Exception as e:
            return TestResult(
                component="integration_tester",
                test_name="stock_asset_management",
                status=TestStatus.FAIL,
                message=f"Error testing stock asset management: {str(e)}",
                severity=Severity.MEDIUM,
                details={"error": str(e)}
            )
    
    def _test_strategy_integration(self, target: str) -> List[TestResult]:
        """Test strategy integration"""
        results = []
        
        # Test strategy framework
        framework_result = self._test_strategy_framework(target)
        results.append(framework_result)
        
        # Test individual strategies
        strategies_result = self._test_individual_strategies(target)
        results.append(strategies_result)
        
        return results
    
    def _test_strategy_framework(self, target: str) -> TestResult:
        """Test strategy framework integration"""
        try:
            sys.path.insert(0, target)
            
            # Try to import key strategy modules
            strategy_modules = [
                'strategies.ml_ai_framework',
                'strategies.market_inefficiency_strategy',
                'strategies.advanced_strategy_hub'
            ]
            
            imported_modules = []
            failed_imports = []
            
            for module_name in strategy_modules:
                try:
                    importlib.import_module(module_name)
                    imported_modules.append(module_name)
                except ImportError as e:
                    failed_imports.append({"module": module_name, "error": str(e)})
            
            if imported_modules:
                status = TestStatus.WARNING if failed_imports else TestStatus.PASS
                severity = Severity.MEDIUM if failed_imports else Severity.LOW
                
                return TestResult(
                    component="integration_tester",
                    test_name="strategy_framework",
                    status=status,
                    message=f"Strategy framework: {len(imported_modules)}/{len(strategy_modules)} modules imported",
                    severity=severity,
                    details={
                        "imported_modules": imported_modules,
                        "failed_imports": failed_imports
                    }
                )
            else:
                return TestResult(
                    component="integration_tester",
                    test_name="strategy_framework",
                    status=TestStatus.FAIL,
                    message="No strategy modules could be imported",
                    severity=Severity.HIGH,
                    details={"failed_imports": failed_imports}
                )
                
        except Exception as e:
            return TestResult(
                component="integration_tester",
                test_name="strategy_framework",
                status=TestStatus.FAIL,
                message=f"Error testing strategy framework: {str(e)}",
                severity=Severity.MEDIUM,
                details={"error": str(e)}
            )
    
    def _test_individual_strategies(self, target: str) -> TestResult:
        """Test individual strategy files"""
        try:
            strategies_path = Path(target) / "strategies"
            
            if not strategies_path.exists():
                return TestResult(
                    component="integration_tester",
                    test_name="individual_strategies",
                    status=TestStatus.FAIL,
                    message="Strategies directory not found",
                    severity=Severity.HIGH,
                    details={"expected_path": str(strategies_path)}
                )
            
            # Find Python strategy files
            strategy_files = list(strategies_path.glob("*.py"))
            strategy_files = [f for f in strategy_files if f.name != "__init__.py"]
            
            if not strategy_files:
                return TestResult(
                    component="integration_tester",
                    test_name="individual_strategies",
                    status=TestStatus.WARNING,
                    message="No strategy files found",
                    severity=Severity.MEDIUM,
                    details={"strategies_path": str(strategies_path)}
                )
            
            return TestResult(
                component="integration_tester",
                test_name="individual_strategies",
                status=TestStatus.PASS,
                message=f"Found {len(strategy_files)} strategy files",
                details={
                    "strategies_path": str(strategies_path),
                    "strategy_count": len(strategy_files),
                    "strategy_files": [f.name for f in strategy_files]
                }
            )
            
        except Exception as e:
            return TestResult(
                component="integration_tester",
                test_name="individual_strategies",
                status=TestStatus.FAIL,
                message=f"Error testing individual strategies: {str(e)}",
                severity=Severity.MEDIUM,
                details={"error": str(e)}
            )
    
    def _test_data_flow(self, target: str) -> TestResult:
        """Test data flow validation"""
        try:
            # Check for key directories and files that indicate proper data flow
            required_paths = [
                "crypto/input",
                "crypto/output", 
                "crypto/logs",
                "stocks/input",
                "stocks/output",
                "stocks/logs",
                "strategies"
            ]
            
            existing_paths = []
            missing_paths = []
            
            for path in required_paths:
                full_path = Path(target) / path
                if full_path.exists():
                    existing_paths.append(path)
                else:
                    missing_paths.append(path)
            
            # Check for main entry points
            entry_points = ["main.py", "crypto_launcher.py", "crypto_main.py"]
            existing_entries = []
            
            for entry in entry_points:
                entry_path = Path(target) / entry
                if entry_path.exists():
                    existing_entries.append(entry)
            
            if len(existing_paths) >= len(required_paths) * 0.7:  # At least 70% of paths exist
                return TestResult(
                    component="integration_tester",
                    test_name="data_flow_validation",
                    status=TestStatus.PASS,
                    message=f"Data flow structure validated ({len(existing_paths)}/{len(required_paths)} paths)",
                    details={
                        "existing_paths": existing_paths,
                        "missing_paths": missing_paths,
                        "entry_points": existing_entries
                    }
                )
            else:
                return TestResult(
                    component="integration_tester",
                    test_name="data_flow_validation",
                    status=TestStatus.WARNING,
                    message=f"Data flow structure incomplete ({len(existing_paths)}/{len(required_paths)} paths)",
                    severity=Severity.MEDIUM,
                    details={
                        "existing_paths": existing_paths,
                        "missing_paths": missing_paths,
                        "entry_points": existing_entries
                    }
                )
                
        except Exception as e:
            return TestResult(
                component="integration_tester",
                test_name="data_flow_validation",
                status=TestStatus.FAIL,
                message=f"Error validating data flow: {str(e)}",
                severity=Severity.MEDIUM,
                details={"error": str(e)}
            )
    
    def get_test_info(self) -> Dict[str, Any]:
        """Get information about this tester"""
        return {
            "name": "IntegrationTester",
            "description": "Tests module interactions and API integrations",
            "tests": [
                "ccxt_integration",
                "crypto_data_acquisition",
                "crypto_asset_management",
                "fyers_integration",
                "yfinance_integration",
                "stock_asset_management",
                "strategy_framework",
                "individual_strategies",
                "data_flow_validation"
            ]
        }