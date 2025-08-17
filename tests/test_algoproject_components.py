"""
AlgoProject Comprehensive Test Suite
===================================

Complete test suite for all AlgoProject components.
"""

import unittest
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Add algoproject to path
sys.path.insert(0, '.')


class TestCoreInterfaces(unittest.TestCase):
    """Test core interfaces and data structures"""
    
    def setUp(self):
        """Set up test fixtures"""
        from algoproject.core.interfaces import MarketData, Signal, Position
        self.MarketData = MarketData
        self.Signal = Signal
        self.Position = Position
    
    def test_market_data_creation(self):
        """Test MarketData creation"""
        data = self.MarketData(
            symbol="BTCUSDT",
            timestamp=datetime.now(),
            open=50000.0,
            high=51000.0,
            low=49500.0,
            close=50500.0,
            volume=1000.0,
            exchange="binance"
        )
        
        self.assertEqual(data.symbol, "BTCUSDT")
        self.assertEqual(data.open, 50000.0)
        self.assertEqual(data.exchange, "binance")
    
    def test_signal_creation(self):
        """Test Signal creation"""
        signal = self.Signal(
            symbol="BTCUSDT",
            action="buy",
            quantity=0.1,
            price=50000.0,
            confidence=0.8
        )
        
        self.assertEqual(signal.symbol, "BTCUSDT")
        self.assertEqual(signal.action, "buy")
        self.assertEqual(signal.quantity, 0.1)
        self.assertEqual(signal.confidence, 0.8)
    
    def test_position_creation(self):
        """Test Position creation"""
        position = self.Position(
            symbol="BTCUSDT",
            quantity=1.0,
            avg_price=50000.0,
            market_price=50500.0,
            timestamp=datetime.now()
        )
        
        self.assertEqual(position.symbol, "BTCUSDT")
        self.assertEqual(position.quantity, 1.0)
        self.assertEqual(position.avg_price, 50000.0)


class TestConfigManager(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        """Set up test fixtures"""
        from algoproject.core.config_manager import ConfigManager
        self.config_manager = ConfigManager()
    
    def test_set_get_setting(self):
        """Test setting and getting configuration values"""
        self.config_manager.set_setting("test_section", "test_key", "test_value")
        value = self.config_manager.get_setting("test_section", "test_key")
        self.assertEqual(value, "test_value")
    
    def test_get_nonexistent_setting(self):
        """Test getting non-existent setting returns default"""
        value = self.config_manager.get_setting("nonexistent", "key", "default")
        self.assertEqual(value, "default")
    
    def test_nested_setting(self):
        """Test nested configuration settings"""
        self.config_manager.set_setting("parent.child", "key", "nested_value")
        value = self.config_manager.get_setting("parent.child", "key")
        self.assertEqual(value, "nested_value")


class TestPortfolio(unittest.TestCase):
    """Test portfolio management"""
    
    def setUp(self):
        """Set up test fixtures"""
        from algoproject.backtesting.portfolio import Portfolio
        self.portfolio = Portfolio(initial_cash=100000.0)
    
    def test_initial_state(self):
        """Test initial portfolio state"""
        self.assertEqual(self.portfolio.cash, 100000.0)
        self.assertEqual(self.portfolio.initial_cash, 100000.0)
        self.assertEqual(len(self.portfolio.positions), 0)
    
    def test_buy_operation(self):
        """Test buying securities"""
        success = self.portfolio.buy("BTCUSDT", 1.0, 50000.0, 50.0)
        self.assertTrue(success)
        self.assertEqual(self.portfolio.cash, 49950.0)  # 100000 - 50000 - 50
        self.assertEqual(self.portfolio.get_position_quantity("BTCUSDT"), 1.0)
    
    def test_sell_operation(self):
        """Test selling securities"""
        # First buy
        self.portfolio.buy("BTCUSDT", 1.0, 50000.0, 50.0)
        
        # Then sell
        success = self.portfolio.sell("BTCUSDT", 0.5, 51000.0, 25.0)
        self.assertTrue(success)
        self.assertEqual(self.portfolio.get_position_quantity("BTCUSDT"), 0.5)
    
    def test_insufficient_cash(self):
        """Test buying with insufficient cash"""
        success = self.portfolio.buy("BTCUSDT", 10.0, 50000.0, 0.0)
        self.assertFalse(success)
    
    def test_insufficient_shares(self):
        """Test selling more shares than owned"""
        success = self.portfolio.sell("BTCUSDT", 1.0, 50000.0, 0.0)
        self.assertFalse(success)
    
    def test_portfolio_value(self):
        """Test portfolio value calculation"""
        self.portfolio.buy("BTCUSDT", 1.0, 50000.0, 50.0)
        self.portfolio.update_market_price("BTCUSDT", 51000.0)
        
        total_value = self.portfolio.get_total_value()
        expected_value = self.portfolio.cash + (1.0 * 51000.0)
        self.assertEqual(total_value, expected_value)


class TestBaseStrategy(unittest.TestCase):
    """Test base strategy functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        from algoproject.strategies.base_strategy import BaseStrategy
        from algoproject.core.interfaces import MarketData, Signal
        
        class TestStrategy(BaseStrategy):
            def next(self, data: MarketData):
                return [Signal(
                    symbol=data.symbol,
                    action="buy",
                    quantity=1.0,
                    price=data.close
                )]
        
        self.TestStrategy = TestStrategy
        self.MarketData = MarketData
    
    def test_strategy_creation(self):
        """Test strategy creation"""
        strategy = self.TestStrategy("Test Strategy", {"param1": 10})
        self.assertEqual(strategy.name, "Test Strategy")
        self.assertEqual(strategy.parameters["param1"], 10)
    
    def test_strategy_signal_generation(self):
        """Test strategy signal generation"""
        strategy = self.TestStrategy("Test Strategy")
        
        market_data = self.MarketData(
            symbol="BTCUSDT",
            timestamp=datetime.now(),
            open=50000.0,
            high=51000.0,
            low=49500.0,
            close=50500.0,
            volume=1000.0,
            exchange="test"
        )
        
        signals = strategy.next(market_data)
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].symbol, "BTCUSDT")
        self.assertEqual(signals[0].action, "buy")


class TestBacktestEngine(unittest.TestCase):
    """Test backtesting engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        from algoproject.backtesting.backtest_engine import BacktestEngine
        from algoproject.data.data_loader import DataLoader
        from algoproject.core.config_manager import ConfigManager
        
        # Create mock data loader
        self.mock_data_loader = Mock(spec=DataLoader)
        self.mock_data_loader.get_historical_data.return_value = self._create_mock_data()
        
        self.engine = BacktestEngine(
            data_loader=self.mock_data_loader,
            initial_capital=100000.0,
            commission=0.001,
            slippage=0.0005
        )
    
    def _create_mock_data(self):
        """Create mock historical data"""
        dates = pd.date_range(start='2023-01-01', end='2023-01-31', freq='D')
        data = []
        
        price = 50000.0
        for date in dates:
            price *= (1 + np.random.normal(0, 0.02))
            data.append({
                'open': price * 0.999,
                'high': price * 1.01,
                'low': price * 0.99,
                'close': price,
                'volume': np.random.uniform(100, 1000)
            })
        
        return pd.DataFrame(data, index=dates)
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        self.assertEqual(self.engine.initial_capital, 100000.0)
        self.assertEqual(self.engine.commission, 0.001)
        self.assertEqual(self.engine.slippage, 0.0005)
    
    @patch('algoproject.strategies.base_strategy.BaseStrategy')
    def test_backtest_execution(self, mock_strategy_class):
        """Test backtest execution"""
        # Create mock strategy
        mock_strategy = Mock()
        mock_strategy.name = "Test Strategy"
        mock_strategy.parameters = {}
        mock_strategy_class.return_value = mock_strategy
        
        # Mock strategy.next to return empty signals
        mock_strategy.next.return_value = []
        
        # Run backtest
        results = self.engine.run_backtest(
            strategy=mock_strategy,
            symbols=["BTCUSDT"],
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 1, 31),
            timeframe='1d'
        )
        
        # Verify results structure
        self.assertIn('strategy_name', results)
        self.assertIn('performance', results)
        self.assertEqual(results['strategy_name'], "Test Strategy")


class TestPerformanceAnalyzer(unittest.TestCase):
    """Test performance analysis"""
    
    def setUp(self):
        """Set up test fixtures"""
        from algoproject.backtesting.reporting.performance_analyzer import PerformanceAnalyzer
        self.analyzer = PerformanceAnalyzer()
    
    def test_analyzer_creation(self):
        """Test analyzer creation"""
        self.assertIsNotNone(self.analyzer)
    
    def test_metrics_calculation(self):
        """Test metrics calculation with mock data"""
        # Create mock equity curve
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        portfolio_values = []
        
        value = 100000
        for _ in dates:
            value *= (1 + np.random.normal(0.0005, 0.02))
            portfolio_values.append(value)
        
        equity_curve = pd.DataFrame({
            'portfolio_value': portfolio_values
        }, index=dates)
        
        # Create empty trade log for testing
        trade_log = pd.DataFrame()
        
        # Calculate metrics
        metrics = self.analyzer.calculate_comprehensive_metrics(equity_curve, trade_log)
        
        # Verify key metrics exist
        self.assertIn('total_return_pct', metrics)
        self.assertIn('sharpe_ratio', metrics)
        self.assertIn('max_drawdown_pct', metrics)


class TestAPIKeyManager(unittest.TestCase):
    """Test API key management"""
    
    def setUp(self):
        """Set up test fixtures"""
        from algoproject.security.api_key_manager import APIKeyManager
        from algoproject.core.config_manager import ConfigManager
        
        self.config_manager = ConfigManager()
        self.api_manager = APIKeyManager(self.config_manager)
    
    def test_add_api_key(self):
        """Test adding API key"""
        key_id = self.api_manager.add_api_key(
            exchange="binance",
            api_key="test_key",
            api_secret="test_secret",
            sandbox=True
        )
        
        self.assertIsNotNone(key_id)
        self.assertIsInstance(key_id, str)
    
    def test_get_api_key(self):
        """Test retrieving API key"""
        # Add key first
        key_id = self.api_manager.add_api_key(
            exchange="binance",
            api_key="test_key",
            api_secret="test_secret"
        )
        
        # Retrieve key
        key_data = self.api_manager.get_api_key(key_id)
        
        self.assertIsNotNone(key_data)
        self.assertEqual(key_data['exchange'], "binance")
        self.assertEqual(key_data['api_key'], "test_key")


class TestLiveTradingEngine(unittest.TestCase):
    """Test live trading engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        from algoproject.trading.live_engine import LiveTradingEngine
        from algoproject.security.api_key_manager import APIKeyManager
        from algoproject.data.data_loader import DataLoader
        from algoproject.core.config_manager import ConfigManager
        
        # Create mocks
        self.mock_api_manager = Mock(spec=APIKeyManager)
        self.mock_data_loader = Mock(spec=DataLoader)
        
        self.engine = LiveTradingEngine(
            api_key_manager=self.mock_api_manager,
            data_loader=self.mock_data_loader
        )
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        self.assertFalse(self.engine.is_running)
        self.assertEqual(len(self.engine.active_strategies), 0)
        self.assertEqual(self.engine.total_trades, 0)
    
    def test_engine_status(self):
        """Test engine status"""
        status = self.engine.get_status()
        
        self.assertIn('running', status)
        self.assertIn('mode', status)
        self.assertIn('total_trades', status)
        self.assertFalse(status['running'])


def run_comprehensive_tests():
    """Run all tests and generate report"""
    print("🧪 Running AlgoProject Comprehensive Test Suite")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestCoreInterfaces,
        TestConfigManager,
        TestPortfolio,
        TestBaseStrategy,
        TestBacktestEngine,
        TestPerformanceAnalyzer,
        TestAPIKeyManager,
        TestLiveTradingEngine
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Generate summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\n💥 ERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if not result.failures and not result.errors:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ AlgoProject components are working correctly")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)