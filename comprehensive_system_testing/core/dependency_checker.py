"""
Dependency Checker
=================

Verifies external dependencies and package installations.
"""

import pkg_resources
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import re

from .base_tester import BaseTester
from .models import TestResult, TestStatus, Severity, TestConfiguration
from ..utils.file_utils import FileUtils
from ..utils.process_utils import ProcessUtils
from ..utils.logger import TestLogger


class DependencyChecker(BaseTester):
    """Checks external package dependencies and versions"""
    
    def __init__(self, config: TestConfiguration):
        super().__init__(config)
        self.logger = TestLogger()
    
    def run_tests(self, target: str) -> List[TestResult]:
        """
        Run dependency tests on the target directory
        
        Args:
            target: Directory path to check for requirements files
            
        Returns:
            List of TestResult objects
        """
        results = []
        start_time = time.time()
        
        self.logger.info("Starting dependency checking")
        
        # Find requirements files
        requirements_files = self._find_requirements_files(target)
        
        if not requirements_files:
            results.append(TestResult(
                component="dependency_checker",
                test_name="requirements_file_found",
                status=TestStatus.WARNING,
                message="No requirements.txt file found",
                severity=Severity.MEDIUM,
                details={"target": target}
            ))
        else:
            # Test each requirements file
            for req_file in requirements_files:
                file_results = self._test_requirements_file(req_file)
                results.extend(file_results)
        
        # Check system dependencies
        system_result = self._check_system_dependencies()
        results.append(system_result)
        
        # Generate dependency report
        report_result = self._generate_dependency_report()
        results.append(report_result)
        
        execution_time = time.time() - start_time
        self.logger.info(f"Dependency checking completed in {execution_time:.2f} seconds")
        
        return results
    
    def _find_requirements_files(self, target: str) -> List[str]:
        """Find all requirements files in the target directory"""
        requirements_files = []
        target_path = Path(target)
        
        # Common requirements file patterns
        patterns = [
            "requirements.txt",
            "requirements-*.txt",
            "dev-requirements.txt",
            "test-requirements.txt",
            "setup.py",
            "pyproject.toml"
        ]
        
        for pattern in patterns:
            if '*' in pattern:
                files = list(target_path.glob(pattern))
                requirements_files.extend([str(f) for f in files])
            else:
                file_path = target_path / pattern
                if file_path.exists():
                    requirements_files.append(str(file_path))
        
        return requirements_files
    
    def _test_requirements_file(self, req_file: str) -> List[TestResult]:
        """Test a single requirements file"""
        results = []
        
        # Test file readability
        content = FileUtils.read_file_safe(req_file)
        if content is None:
            return [TestResult(
                component="dependency_checker",
                test_name="requirements_file_read",
                status=TestStatus.FAIL,
                message=f"Could not read requirements file: {req_file}",
                severity=Severity.HIGH,
                details={"file_path": req_file}
            )]
        
        # Parse requirements
        requirements = self._parse_requirements(content)
        
        # Test each requirement
        for req in requirements:
            req_result = self._test_single_requirement(req_file, req)
            results.append(req_result)
        
        # Test version compatibility
        compat_result = self._test_version_compatibility(req_file, requirements)
        results.append(compat_result)
        
        return results
    
    def _parse_requirements(self, content: str) -> List[Dict[str, Any]]:
        """Parse requirements from file content"""
        requirements = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Skip -r includes and other pip options
            if line.startswith('-'):
                continue
            
            # Parse requirement
            req = self._parse_single_requirement(line, line_num)
            if req:
                requirements.append(req)
        
        return requirements
    
    def _parse_single_requirement(self, line: str, line_num: int) -> Optional[Dict[str, Any]]:
        """Parse a single requirement line"""
        try:
            # Handle different requirement formats
            # package>=1.0.0
            # package==1.0.0
            # package~=1.0.0
            # package
            
            # Remove inline comments
            if '#' in line:
                line = line.split('#')[0].strip()
            
            # Extract package name and version spec
            version_operators = ['>=', '<=', '==', '!=', '~=', '>', '<']
            
            package_name = line
            version_spec = None
            operator = None
            
            for op in version_operators:
                if op in line:
                    parts = line.split(op, 1)
                    if len(parts) == 2:
                        package_name = parts[0].strip()
                        version_spec = parts[1].strip()
                        operator = op
                        break
            
            return {
                'name': package_name,
                'version_spec': version_spec,
                'operator': operator,
                'line_number': line_num,
                'raw_line': line
            }
            
        except Exception as e:
            self.logger.warning(f"Could not parse requirement line: {line} - {e}")
            return None
    
    def _test_single_requirement(self, req_file: str, requirement: Dict[str, Any]) -> TestResult:
        """Test a single package requirement"""
        package_name = requirement['name']
        
        try:
            # Check if package is installed
            if ProcessUtils.check_package_installed(package_name):
                # Get installed version
                try:
                    installed_version = pkg_resources.get_distribution(package_name).version
                    
                    # Check version compatibility if specified
                    if requirement['version_spec'] and requirement['operator']:
                        compatible = self._check_version_compatibility(
                            installed_version,
                            requirement['version_spec'],
                            requirement['operator']
                        )
                        
                        if compatible:
                            return TestResult(
                                component="dependency_checker",
                                test_name="package_requirement",
                                status=TestStatus.PASS,
                                message=f"Package '{package_name}' installed with compatible version {installed_version}",
                                details={
                                    "file_path": req_file,
                                    "package": package_name,
                                    "installed_version": installed_version,
                                    "required_version": requirement['version_spec'],
                                    "operator": requirement['operator']
                                }
                            )
                        else:
                            return TestResult(
                                component="dependency_checker",
                                test_name="package_requirement",
                                status=TestStatus.FAIL,
                                message=f"Package '{package_name}' version mismatch: installed {installed_version}, required {requirement['operator']}{requirement['version_spec']}",
                                severity=Severity.HIGH,
                                details={
                                    "file_path": req_file,
                                    "package": package_name,
                                    "installed_version": installed_version,
                                    "required_version": requirement['version_spec'],
                                    "operator": requirement['operator']
                                }
                            )
                    else:
                        return TestResult(
                            component="dependency_checker",
                            test_name="package_requirement",
                            status=TestStatus.PASS,
                            message=f"Package '{package_name}' installed (version {installed_version})",
                            details={
                                "file_path": req_file,
                                "package": package_name,
                                "installed_version": installed_version
                            }
                        )
                        
                except Exception as e:
                    return TestResult(
                        component="dependency_checker",
                        test_name="package_requirement",
                        status=TestStatus.WARNING,
                        message=f"Package '{package_name}' installed but version check failed: {str(e)}",
                        severity=Severity.MEDIUM,
                        details={
                            "file_path": req_file,
                            "package": package_name,
                            "error": str(e)
                        }
                    )
            else:
                return TestResult(
                    component="dependency_checker",
                    test_name="package_requirement",
                    status=TestStatus.FAIL,
                    message=f"Package '{package_name}' not installed",
                    severity=Severity.HIGH,
                    details={
                        "file_path": req_file,
                        "package": package_name,
                        "required_version": requirement.get('version_spec'),
                        "install_command": f"pip install {requirement['raw_line']}"
                    }
                )
                
        except Exception as e:
            return TestResult(
                component="dependency_checker",
                test_name="package_requirement",
                status=TestStatus.FAIL,
                message=f"Error checking package '{package_name}': {str(e)}",
                severity=Severity.MEDIUM,
                details={
                    "file_path": req_file,
                    "package": package_name,
                    "error": str(e)
                }
            )
    
    def _check_version_compatibility(self, installed: str, required: str, operator: str) -> bool:
        """Check if installed version is compatible with requirement"""
        try:
            from packaging import version
            
            installed_ver = version.parse(installed)
            required_ver = version.parse(required)
            
            if operator == '>=':
                return installed_ver >= required_ver
            elif operator == '<=':
                return installed_ver <= required_ver
            elif operator == '==':
                return installed_ver == required_ver
            elif operator == '!=':
                return installed_ver != required_ver
            elif operator == '>':
                return installed_ver > required_ver
            elif operator == '<':
                return installed_ver < required_ver
            elif operator == '~=':
                # Compatible release operator
                return installed_ver >= required_ver and installed_ver < version.parse(f"{required_ver.major}.{required_ver.minor + 1}")
            else:
                return True  # Unknown operator, assume compatible
                
        except Exception:
            # Fallback to string comparison if packaging module not available
            return installed == required if operator == '==' else True
    
    def _test_version_compatibility(self, req_file: str, requirements: List[Dict[str, Any]]) -> TestResult:
        """Test overall version compatibility"""
        try:
            conflicts = []
            
            # Check for conflicting version requirements
            package_versions = {}
            for req in requirements:
                name = req['name']
                if name in package_versions:
                    # Multiple version specs for same package
                    conflicts.append(f"Multiple version specifications for {name}")
                else:
                    package_versions[name] = req
            
            # Check Python version compatibility
            python_version = ProcessUtils.get_python_version()
            
            if conflicts:
                return TestResult(
                    component="dependency_checker",
                    test_name="version_compatibility",
                    status=TestStatus.WARNING,
                    message=f"Version compatibility issues found",
                    severity=Severity.MEDIUM,
                    details={
                        "file_path": req_file,
                        "conflicts": conflicts,
                        "python_version": python_version
                    }
                )
            else:
                return TestResult(
                    component="dependency_checker",
                    test_name="version_compatibility",
                    status=TestStatus.PASS,
                    message="No version compatibility issues detected",
                    details={
                        "file_path": req_file,
                        "python_version": python_version,
                        "total_packages": len(requirements)
                    }
                )
                
        except Exception as e:
            return TestResult(
                component="dependency_checker",
                test_name="version_compatibility",
                status=TestStatus.FAIL,
                message=f"Error checking version compatibility: {str(e)}",
                severity=Severity.MEDIUM,
                details={"file_path": req_file, "error": str(e)}
            )
    
    def _check_system_dependencies(self) -> TestResult:
        """Check system-level dependencies"""
        try:
            system_info = {
                "python_version": ProcessUtils.get_python_version(),
                "platform": sys.platform,
                "pip_available": self._check_pip_available(),
                "git_available": self._check_git_available()
            }
            
            issues = []
            
            # Check Python version
            python_ver = tuple(map(int, system_info["python_version"].split('.')))
            if python_ver < (3, 7):
                issues.append(f"Python version {system_info['python_version']} may be too old")
            
            # Check pip
            if not system_info["pip_available"]:
                issues.append("pip not available")
            
            status = TestStatus.WARNING if issues else TestStatus.PASS
            severity = Severity.MEDIUM if issues else Severity.LOW
            
            return TestResult(
                component="dependency_checker",
                test_name="system_dependencies",
                status=status,
                message="System dependencies check completed",
                severity=severity,
                details={
                    "system_info": system_info,
                    "issues": issues
                }
            )
            
        except Exception as e:
            return TestResult(
                component="dependency_checker",
                test_name="system_dependencies",
                status=TestStatus.FAIL,
                message=f"Error checking system dependencies: {str(e)}",
                severity=Severity.MEDIUM,
                details={"error": str(e)}
            )
    
    def _check_pip_available(self) -> bool:
        """Check if pip is available"""
        try:
            result = ProcessUtils.run_command("pip --version", timeout=10)
            return result['success']
        except Exception:
            return False
    
    def _check_git_available(self) -> bool:
        """Check if git is available"""
        try:
            result = ProcessUtils.run_command("git --version", timeout=10)
            return result['success']
        except Exception:
            return False
    
    def _generate_dependency_report(self) -> TestResult:
        """Generate comprehensive dependency report"""
        try:
            # Get list of installed packages
            installed_packages = []
            try:
                result = ProcessUtils.run_command("pip list --format=json", timeout=30)
                if result['success']:
                    import json
                    installed_packages = json.loads(result['stdout'])
            except Exception:
                pass
            
            report = {
                "total_installed_packages": len(installed_packages),
                "python_version": ProcessUtils.get_python_version(),
                "pip_version": self._get_pip_version(),
                "virtual_env": self._detect_virtual_environment()
            }
            
            return TestResult(
                component="dependency_checker",
                test_name="dependency_report",
                status=TestStatus.PASS,
                message=f"Dependency report generated ({len(installed_packages)} packages)",
                details=report
            )
            
        except Exception as e:
            return TestResult(
                component="dependency_checker",
                test_name="dependency_report",
                status=TestStatus.FAIL,
                message=f"Error generating dependency report: {str(e)}",
                severity=Severity.LOW,
                details={"error": str(e)}
            )
    
    def _get_pip_version(self) -> Optional[str]:
        """Get pip version"""
        try:
            result = ProcessUtils.run_command("pip --version", timeout=10)
            if result['success']:
                # Extract version from output like "pip 21.0.1 from ..."
                import re
                match = re.search(r'pip (\d+\.\d+\.\d+)', result['stdout'])
                return match.group(1) if match else None
        except Exception:
            pass
        return None
    
    def _detect_virtual_environment(self) -> Dict[str, Any]:
        """Detect if running in virtual environment"""
        venv_info = {
            "in_virtualenv": hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix),
            "virtual_env_path": sys.prefix,
            "base_prefix": getattr(sys, 'base_prefix', sys.prefix)
        }
        return venv_info
    
    def get_test_info(self) -> Dict[str, Any]:
        """Get information about this tester"""
        return {
            "name": "DependencyChecker",
            "description": "Verifies external dependencies and package installations",
            "tests": [
                "requirements_file_found",
                "package_requirement",
                "version_compatibility",
                "system_dependencies",
                "dependency_report"
            ]
        }