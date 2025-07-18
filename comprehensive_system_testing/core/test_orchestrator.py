"""
Test Orchestrator
================

Central coordinator for all testing activities with multiple execution modes.
"""

import time
import concurrent.futures
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .models import TestResult, SystemHealth, TestConfiguration, TestStatus, Severity, HealthTrend
from .syntax_validator import SyntaxValidator
from .import_tester import ImportTester
from .dependency_checker import DependencyChecker
from .config_validator import ConfigValidator
from .integration_tester import IntegrationTester
from .auto_fixer import AutoFixer
from ..reporting.report_generator import ReportGenerator
from ..utils.logger import TestLogger


class TestOrchestrator:
    """Central coordinator for comprehensive system testing"""
    
    def __init__(self, config: Optional[TestConfiguration] = None):
        self.config = config or TestConfiguration()
        self.logger = TestLogger()
        
        # Initialize components
        self.syntax_validator = SyntaxValidator(self.config)
        self.import_tester = ImportTester(self.config)
        self.dependency_checker = DependencyChecker(self.config)
        self.config_validator = ConfigValidator(self.config)
        self.integration_tester = IntegrationTester(self.config)
        self.auto_fixer = AutoFixer(self.config)
        self.report_generator = ReportGenerator()
        
        # Test execution history
        self.execution_history = []
    
    def run_comprehensive_test(self, target: str) -> Dict[str, Any]:
        """
        Execute full system validation
        
        Args:
            target: Directory path to test
            
        Returns:
            Dictionary with test results and system health
        """
        self.logger.info(f"Starting comprehensive test on: {target}")
        start_time = time.time()
        
        all_results = []
        
        try:
            # Phase 1: Syntax Validation
            self.logger.info("Phase 1: Syntax Validation")
            syntax_results = self.syntax_validator.validate(target)
            all_results.extend(syntax_results)
            
            # Phase 2: Import Testing
            self.logger.info("Phase 2: Import Testing")
            import_results = self.import_tester.run_tests(target)
            all_results.extend(import_results)
            
            # Phase 3: Dependency Checking
            self.logger.info("Phase 3: Dependency Checking")
            dependency_results = self.dependency_checker.run_tests(target)
            all_results.extend(dependency_results)
            
            # Phase 4: Configuration Validation
            self.logger.info("Phase 4: Configuration Validation")
            config_results = self.config_validator.validate(target)
            all_results.extend(config_results)
            
            # Phase 5: Integration Testing
            self.logger.info("Phase 5: Integration Testing")
            integration_results = self.integration_tester.run_tests(target)
            all_results.extend(integration_results)
            
            # Phase 6: Auto-fixing (if enabled)
            if self.config.auto_fix_enabled:
                self.logger.info("Phase 6: Auto-fixing Issues")
                fixable_issues = [r for r in all_results if r.status in [TestStatus.FAIL, TestStatus.WARNING]]
                if fixable_issues:
                    fix_results = self.auto_fixer.fix_issues(fixable_issues)
                    all_results.extend(fix_results)
            
            # Calculate system health
            system_health = self._calculate_system_health(all_results)
            
            # Generate reports
            self.logger.info("Generating reports...")
            report_files = self.report_generator.generate_all_formats(all_results, system_health)
            
            execution_time = time.time() - start_time
            
            # Record execution
            execution_record = {
                "timestamp": datetime.now().isoformat(),
                "target": target,
                "execution_time": execution_time,
                "total_tests": len(all_results),
                "system_health_score": system_health.overall_score,
                "mode": "comprehensive"
            }
            self.execution_history.append(execution_record)
            
            self.logger.info(f"Comprehensive test completed in {execution_time:.2f} seconds")
            
            return {
                "results": all_results,
                "system_health": system_health,
                "execution_time": execution_time,
                "report_files": report_files,
                "execution_record": execution_record
            }
            
        except Exception as e:
            self.logger.error(f"Comprehensive test failed: {e}")
            return {
                "results": all_results,
                "system_health": None,
                "execution_time": time.time() - start_time,
                "error": str(e)
            }
    
    def run_targeted_test(self, target: str, components: List[str]) -> Dict[str, Any]:
        """
        Test specific components only
        
        Args:
            target: Directory path to test
            components: List of component names to test
            
        Returns:
            Dictionary with test results
        """
        self.logger.info(f"Starting targeted test on: {target} for components: {components}")
        start_time = time.time()
        
        all_results = []
        component_map = {
            "syntax": self.syntax_validator,
            "imports": self.import_tester,
            "dependencies": self.dependency_checker,
            "config": self.config_validator,
            "integration": self.integration_tester
        }
        
        try:
            for component in components:
                if component in component_map:
                    self.logger.info(f"Testing component: {component}")
                    
                    if component == "syntax":
                        results = self.syntax_validator.validate(target)
                    elif component == "imports":
                        results = self.import_tester.run_tests(target)
                    elif component == "dependencies":
                        results = self.dependency_checker.run_tests(target)
                    elif component == "config":
                        results = self.config_validator.validate(target)
                    elif component == "integration":
                        results = self.integration_tester.run_tests(target)
                    
                    all_results.extend(results)
                else:
                    self.logger.warning(f"Unknown component: {component}")
            
            # Auto-fix if enabled
            if self.config.auto_fix_enabled:
                fixable_issues = [r for r in all_results if r.status in [TestStatus.FAIL, TestStatus.WARNING]]
                if fixable_issues:
                    fix_results = self.auto_fixer.fix_issues(fixable_issues)
                    all_results.extend(fix_results)
            
            execution_time = time.time() - start_time
            
            # Generate console summary
            console_summary = self.report_generator.generate_console_summary(all_results)
            print(console_summary)
            
            execution_record = {
                "timestamp": datetime.now().isoformat(),
                "target": target,
                "execution_time": execution_time,
                "total_tests": len(all_results),
                "components": components,
                "mode": "targeted"
            }
            self.execution_history.append(execution_record)
            
            self.logger.info(f"Targeted test completed in {execution_time:.2f} seconds")
            
            return {
                "results": all_results,
                "execution_time": execution_time,
                "components_tested": components,
                "execution_record": execution_record
            }
            
        except Exception as e:
            self.logger.error(f"Targeted test failed: {e}")
            return {
                "results": all_results,
                "execution_time": time.time() - start_time,
                "error": str(e)
            }
    
    def run_quick_test(self, target: str) -> Dict[str, Any]:
        """
        Run essential checks only for quick feedback
        
        Args:
            target: Directory path to test
            
        Returns:
            Dictionary with test results
        """
        self.logger.info(f"Starting quick test on: {target}")
        start_time = time.time()
        
        all_results = []
        
        try:
            # Quick syntax check on key files
            key_files = self._find_key_files(target)
            for file_path in key_files[:10]:  # Limit to 10 files for speed
                syntax_results = self.syntax_validator.validate(file_path)
                all_results.extend(syntax_results)
            
            # Quick dependency check
            dependency_results = self.dependency_checker.run_tests(target)
            all_results.extend(dependency_results)
            
            # Quick integration check
            integration_results = self.integration_tester.run_tests(target)
            all_results.extend(integration_results)
            
            execution_time = time.time() - start_time
            
            # Generate console summary
            console_summary = self.report_generator.generate_console_summary(all_results)
            print(console_summary)
            
            execution_record = {
                "timestamp": datetime.now().isoformat(),
                "target": target,
                "execution_time": execution_time,
                "total_tests": len(all_results),
                "mode": "quick"
            }
            self.execution_history.append(execution_record)
            
            self.logger.info(f"Quick test completed in {execution_time:.2f} seconds")
            
            return {
                "results": all_results,
                "execution_time": execution_time,
                "execution_record": execution_record
            }
            
        except Exception as e:
            self.logger.error(f"Quick test failed: {e}")
            return {
                "results": all_results,
                "execution_time": time.time() - start_time,
                "error": str(e)
            }
    
    def run_continuous_monitoring(self, target: str, interval_minutes: int = 60) -> None:
        """
        Background health monitoring (placeholder for continuous mode)
        
        Args:
            target: Directory path to monitor
            interval_minutes: Monitoring interval in minutes
        """
        self.logger.info(f"Starting continuous monitoring of: {target} (interval: {interval_minutes}min)")
        
        # This would typically run in a separate thread/process
        # For now, just run a single quick test
        result = self.run_quick_test(target)
        
        self.logger.info("Continuous monitoring cycle completed")
        return result
    
    def generate_test_plan(self, target: str) -> Dict[str, Any]:
        """
        Create dynamic test execution plan based on system state
        
        Args:
            target: Directory path to analyze
            
        Returns:
            Dictionary with recommended test plan
        """
        self.logger.info(f"Generating test plan for: {target}")
        
        plan = {
            "target": target,
            "generated_at": datetime.now().isoformat(),
            "recommended_tests": [],
            "estimated_time": 0,
            "priority_order": []
        }
        
        try:
            # Analyze target directory
            target_path = Path(target)
            
            # Check for different file types
            python_files = list(target_path.rglob("*.py"))
            config_files = list(target_path.rglob("*.yaml")) + list(target_path.rglob("*.json")) + list(target_path.rglob("*.csv"))
            
            # Recommend tests based on what's found
            if python_files:
                plan["recommended_tests"].extend([
                    {"test": "syntax_validation", "reason": f"Found {len(python_files)} Python files", "estimated_time": len(python_files) * 0.1},
                    {"test": "import_testing", "reason": "Python files need import validation", "estimated_time": len(python_files) * 0.2}
                ])
            
            if config_files:
                plan["recommended_tests"].append({
                    "test": "config_validation", 
                    "reason": f"Found {len(config_files)} configuration files", 
                    "estimated_time": len(config_files) * 0.05
                })
            
            # Always recommend dependency and integration tests
            plan["recommended_tests"].extend([
                {"test": "dependency_checking", "reason": "Verify external dependencies", "estimated_time": 30},
                {"test": "integration_testing", "reason": "Validate component interactions", "estimated_time": 60}
            ])
            
            # Calculate total estimated time
            plan["estimated_time"] = sum(test["estimated_time"] for test in plan["recommended_tests"])
            
            # Set priority order
            plan["priority_order"] = [
                "dependency_checking",
                "syntax_validation", 
                "import_testing",
                "config_validation",
                "integration_testing"
            ]
            
            self.logger.info(f"Test plan generated: {len(plan['recommended_tests'])} tests, ~{plan['estimated_time']:.1f}s estimated")
            
        except Exception as e:
            self.logger.error(f"Failed to generate test plan: {e}")
            plan["error"] = str(e)
        
        return plan
    
    def _find_key_files(self, target: str) -> List[str]:
        """Find key files for quick testing"""
        key_files = []
        target_path = Path(target)
        
        # Look for main entry points
        entry_points = ["main.py", "app.py", "__init__.py", "setup.py"]
        for entry in entry_points:
            entry_path = target_path / entry
            if entry_path.exists():
                key_files.append(str(entry_path))
        
        # Look for key directories
        key_dirs = ["src", "lib", "core", "app"]
        for dir_name in key_dirs:
            dir_path = target_path / dir_name
            if dir_path.exists():
                python_files = list(dir_path.rglob("*.py"))
                key_files.extend([str(f) for f in python_files[:5]])  # Limit per directory
        
        return key_files
    
    def _calculate_system_health(self, results: List[TestResult]) -> SystemHealth:
        """Calculate overall system health from test results"""
        if not results:
            return SystemHealth(overall_score=0.0)
        
        # Count results by status and severity
        total_tests = len(results)
        passed = len([r for r in results if r.status == TestStatus.PASS])
        failed = len([r for r in results if r.status == TestStatus.FAIL])
        warnings = len([r for r in results if r.status == TestStatus.WARNING])
        
        critical_issues = [r for r in results if r.severity == Severity.CRITICAL and r.status == TestStatus.FAIL]
        high_issues = [r for r in results if r.severity == Severity.HIGH and r.status == TestStatus.FAIL]
        warning_issues = [r for r in results if r.status == TestStatus.WARNING]
        
        # Calculate base score from pass rate
        base_score = (passed / total_tests) * 100 if total_tests > 0 else 0
        
        # Apply penalties for issues
        penalties = 0
        penalties += len(critical_issues) * 20  # -20 points per critical issue
        penalties += len(high_issues) * 10      # -10 points per high issue
        penalties += len(warning_issues) * 2    # -2 points per warning
        
        # Calculate final score
        overall_score = max(0, base_score - penalties)
        
        # Calculate component scores
        component_scores = {}
        components = set(r.component for r in results)
        
        for component in components:
            component_results = [r for r in results if r.component == component]
            component_passed = len([r for r in component_results if r.status == TestStatus.PASS])
            component_total = len(component_results)
            component_scores[component] = (component_passed / component_total * 100) if component_total > 0 else 0
        
        # Determine trend (simplified - would need historical data for real trend analysis)
        if overall_score >= 90:
            trend = HealthTrend.IMPROVING
        elif overall_score >= 70:
            trend = HealthTrend.STABLE
        else:
            trend = HealthTrend.DEGRADING
        
        return SystemHealth(
            overall_score=overall_score,
            component_scores=component_scores,
            critical_issues=critical_issues,
            warnings=warning_issues,
            last_test_time=datetime.now(),
            trend=trend
        )
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get test execution history"""
        return self.execution_history.copy()
    
    def get_orchestrator_info(self) -> Dict[str, Any]:
        """Get information about the orchestrator and its components"""
        return {
            "orchestrator": "TestOrchestrator",
            "version": "1.0.0",
            "components": {
                "syntax_validator": self.syntax_validator.get_validator_info(),
                "import_tester": self.import_tester.get_test_info(),
                "dependency_checker": self.dependency_checker.get_test_info(),
                "config_validator": self.config_validator.get_validator_info(),
                "integration_tester": self.integration_tester.get_test_info()
            },
            "execution_modes": [
                "comprehensive",
                "targeted", 
                "quick",
                "continuous"
            ],
            "auto_fix_enabled": self.config.auto_fix_enabled,
            "parallel_execution": self.config.parallel_execution,
            "total_executions": len(self.execution_history)
        }