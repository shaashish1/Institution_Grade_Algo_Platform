"""
Unit Tests for Test Orchestrator
================================

Test cases for the TestOrchestrator class.
"""

import unittest
import tempfile
import os
from pathlib import Path

from ..core.test_orchestrator import TestOrchestrator
from ..core.models import TestConfiguration, TestResult, TestStatus, Severity


class TestTestOrchestrator(unittest.TestCase):
    """Test cases for TestOrchestrator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = TestConfiguration()
        self.orchestrator = TestOrchestrator(self.config)
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_test_structure(self):
        """Create a basic test project structure"""
        # Create directories
        (Path(self.temp_dir) / "src").mkdir()
        (Path(self.temp_dir) / "tests").mkdir()
        
        # Create Python files
        with open(Path(self.temp_dir) / "main.py", 'w') as f:
            f.write('print("Hello World")')
        
        with open(Path(self.temp_dir) / "src" / "module.py", 'w') as f:
            f.write('def function():\n    return True')
        
        # Create requirements.txt
        with open(Path(self.temp_dir) / "requirements.txt", 'w') as f:
            f.write('requests>=2.0.0\npandas>=1.0.0')
        
        # Create config file
        with open(Path(self.temp_dir) / "config.yaml", 'w') as f:
            f.write('setting: value\nother: 123')
    
    def test_generate_test_plan(self):
        """Test generating test plan"""
        self._create_test_structure()
        
        plan = self.orchestrator.generate_test_plan(self.temp_dir)
        
        self.assertIn("target", plan)
        self.assertIn("recommended_tests", plan)
        self.assertIn("estimated_time", plan)
        self.assertIn("priority_order", plan)
        
        # Should recommend tests based on found files
        test_names = [test["test"] for test in plan["recommended_tests"]]
        self.assertIn("syntax_validation", test_names)
        self.assertIn("dependency_checking", test_names)
    
    def test_find_key_files(self):
        """Test finding key files for quick testing"""
        self._create_test_structure()
        
        key_files = self.orchestrator._find_key_files(self.temp_dir)
        
        self.assertGreater(len(key_files), 0)
        
        # Should find main.py
        main_py_found = any("main.py" in f for f in key_files)
        self.assertTrue(main_py_found)
    
    def test_calculate_system_health(self):
        """Test calculating system health from results"""
        results = [
            TestResult(
                component="test1",
                test_name="test1",
                status=TestStatus.PASS,
                message="Test passed"
            ),
            TestResult(
                component="test2",
                test_name="test2",
                status=TestStatus.PASS,
                message="Test passed"
            ),
            TestResult(
                component="test3",
                test_name="test3",
                status=TestStatus.FAIL,
                message="Test failed",
                severity=Severity.HIGH
            ),
            TestResult(
                component="test4",
                test_name="test4",
                status=TestStatus.WARNING,
                message="Test warning",
                severity=Severity.MEDIUM
            )
        ]
        
        health = self.orchestrator._calculate_system_health(results)
        
        self.assertIsNotNone(health)
        self.assertGreater(health.overall_score, 0)
        self.assertLessEqual(health.overall_score, 100)
        
        # Should have component scores
        self.assertGreater(len(health.component_scores), 0)
        
        # Should identify issues
        self.assertEqual(len(health.critical_issues), 0)  # No critical issues in test data
        self.assertEqual(len(health.warnings), 1)  # One warning
    
    def test_calculate_system_health_with_critical_issues(self):
        """Test system health calculation with critical issues"""
        results = [
            TestResult(
                component="critical_test",
                test_name="critical_test",
                status=TestStatus.FAIL,
                message="Critical failure",
                severity=Severity.CRITICAL
            )
        ]
        
        health = self.orchestrator._calculate_system_health(results)
        
        # Should have low score due to critical issue
        self.assertLess(health.overall_score, 50)
        self.assertEqual(len(health.critical_issues), 1)
    
    def test_get_orchestrator_info(self):
        """Test getting orchestrator information"""
        info = self.orchestrator.get_orchestrator_info()
        
        self.assertIn("orchestrator", info)
        self.assertIn("version", info)
        self.assertIn("components", info)
        self.assertIn("execution_modes", info)
        
        # Should list all execution modes
        modes = info["execution_modes"]
        self.assertIn("comprehensive", modes)
        self.assertIn("targeted", modes)
        self.assertIn("quick", modes)
        self.assertIn("continuous", modes)
    
    def test_execution_history_tracking(self):
        """Test execution history tracking"""
        initial_history_length = len(self.orchestrator.execution_history)
        
        # This would normally run tests, but we'll just check the structure
        history = self.orchestrator.get_execution_history()
        
        self.assertIsInstance(history, list)
        self.assertEqual(len(history), initial_history_length)
    
    def test_quick_test_mode(self):
        """Test quick test mode"""
        self._create_test_structure()
        
        # Mock the quick test (since we don't want to run full tests in unit tests)
        # In a real scenario, this would execute actual tests
        result = self.orchestrator.run_quick_test(self.temp_dir)
        
        self.assertIn("results", result)
        self.assertIn("execution_time", result)
        self.assertIn("execution_record", result)
        
        # Should record execution
        self.assertGreater(len(self.orchestrator.execution_history), 0)
        
        # Check execution record
        record = result["execution_record"]
        self.assertEqual(record["mode"], "quick")
        self.assertEqual(record["target"], self.temp_dir)
    
    def test_targeted_test_mode(self):
        """Test targeted test mode"""
        self._create_test_structure()
        
        components = ["syntax", "dependencies"]
        result = self.orchestrator.run_targeted_test(self.temp_dir, components)
        
        self.assertIn("results", result)
        self.assertIn("execution_time", result)
        self.assertIn("components_tested", result)
        
        # Should test only specified components
        self.assertEqual(result["components_tested"], components)
        
        # Should record execution
        record = result["execution_record"]
        self.assertEqual(record["mode"], "targeted")
        self.assertEqual(record["components"], components)
    
    def test_continuous_monitoring_mode(self):
        """Test continuous monitoring mode"""
        self._create_test_structure()
        
        # This is a placeholder test since continuous monitoring
        # would typically run in a separate thread
        result = self.orchestrator.run_continuous_monitoring(self.temp_dir, interval_minutes=1)
        
        # Should return a result (currently just runs quick test)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()