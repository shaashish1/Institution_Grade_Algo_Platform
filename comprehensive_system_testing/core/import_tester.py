"""
Import Tester
============

Tests module imports and dependency resolution with isolated testing.
"""

import ast
import sys
import time
import subprocess
import networkx as nx
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple, Optional

from .base_tester import BaseTester
from .models import TestResult, TestStatus, Severity, TestConfiguration
from ..utils.file_utils import FileUtils
from ..utils.process_utils import ProcessUtils
from ..utils.validation_utils import ValidationUtils
from ..utils.logger import TestLogger


class ImportTester(BaseTester):
    """Tests module imports and detects circular dependencies"""
    
    def __init__(self, config: TestConfiguration):
        super().__init__(config)
        self.logger = TestLogger()
        self.dependency_graph = nx.DiGraph()
    
    def run_tests(self, target: str) -> List[TestResult]:
        """
        Run import tests on the target directory or file
        
        Args:
            target: Directory path or single file path to test
            
        Returns:
            List of TestResult objects
        """
        results = []
        start_time = time.time()
        
        # Get Python files to test
        if Path(target).is_file():
            python_files = [target]
        else:
            python_files = FileUtils.find_python_files(target)
        
        self.logger.info(f"Testing imports for {len(python_files)} Python files")
        
        # Test individual file imports
        for file_path in python_files:
            file_results = self._test_file_imports(file_path)
            results.extend(file_results)
        
        # Test for circular dependencies
        circular_result = self._test_circular_dependencies(python_files)
        results.append(circular_result)
        
        # Validate __init__.py files
        init_results = self._validate_init_files(target)
        results.extend(init_results)
        
        execution_time = time.time() - start_time
        self.logger.info(f"Import testing completed in {execution_time:.2f} seconds")
        
        return results
    
    def _test_file_imports(self, file_path: str) -> List[TestResult]:
        """Test imports for a single file"""
        results = []
        
        # Read file content
        content = FileUtils.read_file_safe(file_path)
        if content is None:
            return [TestResult(
                component="import_tester",
                test_name="file_read",
                status=TestStatus.FAIL,
                message=f"Could not read file: {file_path}",
                severity=Severity.HIGH,
                details={"file_path": file_path}
            )]
        
        # Extract imports
        imports = ValidationUtils.extract_imports(content)
        
        # Test each import in isolation
        for import_name in imports:
            import_result = self._test_single_import(file_path, import_name)
            results.append(import_result)
            
            # Add to dependency graph
            self._add_to_dependency_graph(file_path, import_name)
        
        # Test relative imports
        relative_result = self._test_relative_imports(file_path, content)
        results.append(relative_result)
        
        return results
    
    def _test_single_import(self, file_path: str, import_name: str) -> TestResult:
        """Test a single import in isolation"""
        try:
            # Test import in subprocess for isolation
            success, error_msg = ProcessUtils.test_import_isolated(import_name)
            
            if success:
                return TestResult(
                    component="import_tester",
                    test_name="import_test",
                    status=TestStatus.PASS,
                    message=f"Import '{import_name}' successful",
                    details={
                        "file_path": file_path,
                        "import_name": import_name
                    }
                )
            else:
                # Determine severity based on import type
                severity = self._determine_import_severity(import_name, error_msg)
                
                return TestResult(
                    component="import_tester",
                    test_name="import_test",
                    status=TestStatus.FAIL,
                    message=f"Import '{import_name}' failed: {error_msg}",
                    severity=severity,
                    details={
                        "file_path": file_path,
                        "import_name": import_name,
                        "error": error_msg
                    }
                )
                
        except Exception as e:
            return TestResult(
                component="import_tester",
                test_name="import_test",
                status=TestStatus.FAIL,
                message=f"Error testing import '{import_name}': {str(e)}",
                severity=Severity.MEDIUM,
                details={
                    "file_path": file_path,
                    "import_name": import_name,
                    "error": str(e)
                }
            )
    
    def _determine_import_severity(self, import_name: str, error_msg: str) -> Severity:
        """Determine severity of import failure"""
        # Standard library imports should always work
        stdlib_modules = {
            'os', 'sys', 'json', 'datetime', 'time', 'math', 'random',
            'collections', 'itertools', 'functools', 'pathlib', 'typing'
        }
        
        if import_name in stdlib_modules:
            return Severity.CRITICAL
        
        # Third-party imports are high priority
        if 'no module named' in error_msg.lower():
            return Severity.HIGH
        
        # Other import errors are medium priority
        return Severity.MEDIUM
    
    def _test_relative_imports(self, file_path: str, content: str) -> TestResult:
        """Test relative imports in a file"""
        try:
            tree = ast.parse(content)
            relative_imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.level > 0:
                    relative_imports.append({
                        'module': node.module or '',
                        'level': node.level,
                        'names': [alias.name for alias in node.names]
                    })
            
            if not relative_imports:
                return TestResult(
                    component="import_tester",
                    test_name="relative_imports",
                    status=TestStatus.PASS,
                    message=f"No relative imports in {Path(file_path).name}",
                    details={"file_path": file_path}
                )
            
            # Validate relative import paths
            issues = []
            for rel_import in relative_imports:
                if not self._validate_relative_import_path(file_path, rel_import):
                    issues.append(f"Invalid relative import: {rel_import}")
            
            if issues:
                return TestResult(
                    component="import_tester",
                    test_name="relative_imports",
                    status=TestStatus.FAIL,
                    message=f"Relative import issues in {Path(file_path).name}",
                    severity=Severity.HIGH,
                    details={
                        "file_path": file_path,
                        "issues": issues,
                        "relative_imports": relative_imports
                    }
                )
            else:
                return TestResult(
                    component="import_tester",
                    test_name="relative_imports",
                    status=TestStatus.PASS,
                    message=f"Valid relative imports in {Path(file_path).name}",
                    details={
                        "file_path": file_path,
                        "relative_imports": relative_imports
                    }
                )
                
        except Exception as e:
            return TestResult(
                component="import_tester",
                test_name="relative_imports",
                status=TestStatus.FAIL,
                message=f"Error testing relative imports: {str(e)}",
                severity=Severity.MEDIUM,
                details={"file_path": file_path, "error": str(e)}
            )
    
    def _validate_relative_import_path(self, file_path: str, rel_import: Dict) -> bool:
        """Validate that a relative import path exists"""
        try:
            file_dir = Path(file_path).parent
            
            # Calculate target directory based on relative level
            target_dir = file_dir
            for _ in range(rel_import['level']):
                target_dir = target_dir.parent
            
            # Check if target module exists
            if rel_import['module']:
                module_path = target_dir / f"{rel_import['module']}.py"
                init_path = target_dir / rel_import['module'] / "__init__.py"
                return module_path.exists() or init_path.exists()
            
            return True  # Relative import without module name
            
        except Exception:
            return False
    
    def _add_to_dependency_graph(self, file_path: str, import_name: str):
        """Add dependency to the graph for circular dependency detection"""
        try:
            # Normalize file path to module name
            file_module = self._file_path_to_module_name(file_path)
            
            # Add nodes and edge
            self.dependency_graph.add_node(file_module)
            self.dependency_graph.add_node(import_name)
            self.dependency_graph.add_edge(file_module, import_name)
            
        except Exception as e:
            self.logger.warning(f"Could not add to dependency graph: {e}")
    
    def _file_path_to_module_name(self, file_path: str) -> str:
        """Convert file path to module name"""
        path = Path(file_path)
        
        # Remove .py extension
        if path.suffix == '.py':
            path = path.with_suffix('')
        
        # Convert path separators to dots
        parts = path.parts
        
        # Find the root of the project (where we start the module path)
        # This is a simplified approach
        if 'comprehensive_system_testing' in parts:
            start_idx = parts.index('comprehensive_system_testing')
            module_parts = parts[start_idx:]
        else:
            module_parts = parts[-2:]  # Take last two parts as fallback
        
        return '.'.join(module_parts)
    
    def _test_circular_dependencies(self, python_files: List[str]) -> TestResult:
        """Test for circular dependencies"""
        try:
            # Find cycles in the dependency graph
            cycles = list(nx.simple_cycles(self.dependency_graph))
            
            if not cycles:
                return TestResult(
                    component="import_tester",
                    test_name="circular_dependencies",
                    status=TestStatus.PASS,
                    message="No circular dependencies detected",
                    details={
                        "total_modules": len(python_files),
                        "dependency_count": self.dependency_graph.number_of_edges()
                    }
                )
            else:
                return TestResult(
                    component="import_tester",
                    test_name="circular_dependencies",
                    status=TestStatus.FAIL,
                    message=f"Found {len(cycles)} circular dependencies",
                    severity=Severity.HIGH,
                    details={
                        "cycles": cycles,
                        "cycle_count": len(cycles),
                        "affected_modules": list(set([module for cycle in cycles for module in cycle]))
                    }
                )
                
        except Exception as e:
            return TestResult(
                component="import_tester",
                test_name="circular_dependencies",
                status=TestStatus.FAIL,
                message=f"Error detecting circular dependencies: {str(e)}",
                severity=Severity.MEDIUM,
                details={"error": str(e)}
            )
    
    def _validate_init_files(self, target: str) -> List[TestResult]:
        """Validate __init__.py files"""
        results = []
        
        if Path(target).is_file():
            return results  # Skip if target is a single file
        
        # Find all __init__.py files
        init_files = []
        for root, dirs, files in Path(target).walk():
            if "__init__.py" in files:
                init_files.append(root / "__init__.py")
        
        for init_file in init_files:
            result = self._validate_single_init_file(str(init_file))
            results.append(result)
        
        return results
    
    def _validate_single_init_file(self, init_file_path: str) -> TestResult:
        """Validate a single __init__.py file"""
        try:
            content = FileUtils.read_file_safe(init_file_path)
            if content is None:
                return TestResult(
                    component="import_tester",
                    test_name="init_file_validation",
                    status=TestStatus.FAIL,
                    message=f"Could not read __init__.py: {init_file_path}",
                    severity=Severity.MEDIUM,
                    details={"file_path": init_file_path}
                )
            
            # Parse the file
            tree = ast.parse(content)
            
            # Check for __all__ definition
            has_all = False
            all_items = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == '__all__':
                            has_all = True
                            if isinstance(node.value, ast.List):
                                all_items = [elt.s for elt in node.value.elts if isinstance(elt, ast.Str)]
            
            # Check imports and exports
            imports = ValidationUtils.extract_imports(content)
            
            issues = []
            
            # Check if __all__ is defined for non-empty modules
            if imports and not has_all and len(content.strip()) > 50:
                issues.append("Consider defining __all__ to control public API")
            
            # Validate that __all__ items are actually defined/imported
            if has_all and all_items:
                defined_names = self._get_defined_names(tree)
                for item in all_items:
                    if item not in defined_names and item not in imports:
                        issues.append(f"__all__ item '{item}' not found in module")
            
            status = TestStatus.WARNING if issues else TestStatus.PASS
            severity = Severity.LOW if issues else Severity.LOW
            
            return TestResult(
                component="import_tester",
                test_name="init_file_validation",
                status=status,
                message=f"__init__.py validation: {Path(init_file_path).parent.name}",
                severity=severity,
                details={
                    "file_path": init_file_path,
                    "has_all": has_all,
                    "all_items": all_items,
                    "imports": imports,
                    "issues": issues
                }
            )
            
        except Exception as e:
            return TestResult(
                component="import_tester",
                test_name="init_file_validation",
                status=TestStatus.FAIL,
                message=f"Error validating __init__.py: {str(e)}",
                severity=Severity.MEDIUM,
                details={"file_path": init_file_path, "error": str(e)}
            )
    
    def _get_defined_names(self, tree: ast.AST) -> Set[str]:
        """Get all names defined in an AST"""
        names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                names.add(node.name)
            elif isinstance(node, ast.ClassDef):
                names.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        names.add(target.id)
        
        return names
    
    def get_test_info(self) -> Dict[str, Any]:
        """Get information about this tester"""
        return {
            "name": "ImportTester",
            "description": "Tests module imports and dependency resolution",
            "tests": [
                "import_test",
                "relative_imports", 
                "circular_dependencies",
                "init_file_validation"
            ],
            "dependency_graph_nodes": self.dependency_graph.number_of_nodes(),
            "dependency_graph_edges": self.dependency_graph.number_of_edges()
        }