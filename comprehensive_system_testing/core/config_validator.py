"""
Configuration Validator
=======================

Validates configuration files and data formats (YAML, JSON, CSV).
"""

import json
import yaml
import csv
import io
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from .base_validator import BaseValidator
from .models import TestResult, TestStatus, Severity, TestConfiguration
from ..utils.file_utils import FileUtils
from ..utils.validation_utils import ValidationUtils
from ..utils.logger import TestLogger


class ConfigValidator(BaseValidator):
    """Validates configuration files in multiple formats"""
    
    def __init__(self, config: TestConfiguration):
        super().__init__(config)
        self.logger = TestLogger()
    
    def validate(self, target: str) -> List[TestResult]:
        """
        Validate configuration files in the target directory
        
        Args:
            target: Directory path to validate config files
            
        Returns:
            List of TestResult objects
        """
        results = []
        start_time = time.time()
        
        self.logger.info("Starting configuration validation")
        
        # Find configuration files
        config_files = self._find_config_files(target)
        
        # Validate each configuration file
        for file_path, file_type in config_files:
            file_results = self._validate_config_file(file_path, file_type)
            results.extend(file_results)
        
        execution_time = time.time() - start_time
        self.logger.info(f"Configuration validation completed in {execution_time:.2f} seconds")
        
        return results
    
    def _find_config_files(self, target: str) -> List[Tuple[str, str]]:
        """Find all configuration files in target directory"""
        config_files = []
        target_path = Path(target)
        
        # File patterns and their types
        patterns = {
            "*.yaml": "yaml",
            "*.yml": "yaml", 
            "*.json": "json",
            "*.csv": "csv",
            "config*.py": "python",
            "settings*.py": "python"
        }
        
        for pattern, file_type in patterns.items():
            files = list(target_path.rglob(pattern))
            for file_path in files:
                config_files.append((str(file_path), file_type))
        
        return config_files
    
    def _validate_config_file(self, file_path: str, file_type: str) -> List[TestResult]:
        """Validate a single configuration file"""
        results = []
        
        # Read file content
        content = FileUtils.read_file_safe(file_path)
        if content is None:
            return [TestResult(
                component="config_validator",
                test_name="file_read",
                status=TestStatus.FAIL,
                message=f"Could not read config file: {file_path}",
                severity=Severity.HIGH,
                details={"file_path": file_path, "file_type": file_type}
            )]
        
        # Validate based on file type
        if file_type == "yaml":
            results.extend(self._validate_yaml_file(file_path, content))
        elif file_type == "json":
            results.extend(self._validate_json_file(file_path, content))
        elif file_type == "csv":
            results.extend(self._validate_csv_file(file_path, content))
        elif file_type == "python":
            results.extend(self._validate_python_config(file_path, content))
        
        return results
    
    def _validate_yaml_file(self, file_path: str, content: str) -> List[TestResult]:
        """Validate YAML configuration file"""
        results = []
        
        # Test 1: YAML syntax validation
        is_valid, error_msg = ValidationUtils.validate_yaml_format(content)
        
        if is_valid:
            try:
                data = yaml.safe_load(content)
                
                results.append(TestResult(
                    component="config_validator",
                    test_name="yaml_syntax",
                    status=TestStatus.PASS,
                    message=f"Valid YAML syntax: {Path(file_path).name}",
                    details={
                        "file_path": file_path,
                        "data_type": type(data).__name__,
                        "keys": list(data.keys()) if isinstance(data, dict) else None
                    }
                ))
                
                # Test 2: YAML structure validation
                structure_result = self._validate_yaml_structure(file_path, data)
                results.append(structure_result)
                
                # Test 3: YAML content validation
                content_result = self._validate_yaml_content(file_path, data)
                results.append(content_result)
                
            except Exception as e:
                results.append(TestResult(
                    component="config_validator",
                    test_name="yaml_syntax",
                    status=TestStatus.FAIL,
                    message=f"YAML parsing error: {str(e)}",
                    severity=Severity.HIGH,
                    details={"file_path": file_path, "error": str(e)}
                ))
        else:
            results.append(TestResult(
                component="config_validator",
                test_name="yaml_syntax",
                status=TestStatus.FAIL,
                message=f"Invalid YAML syntax: {error_msg}",
                severity=Severity.HIGH,
                details={"file_path": file_path, "error": error_msg}
            ))
        
        return results
    
    def _validate_yaml_structure(self, file_path: str, data: Any) -> TestResult:
        """Validate YAML structure"""
        try:
            issues = []
            
            if isinstance(data, dict):
                # Check for empty values
                empty_keys = [k for k, v in data.items() if v is None or v == ""]
                if empty_keys:
                    issues.append(f"Empty values for keys: {empty_keys}")
                
                # Check for very deep nesting
                max_depth = self._get_dict_depth(data)
                if max_depth > 5:
                    issues.append(f"Very deep nesting detected (depth: {max_depth})")
                
            elif isinstance(data, list):
                # Check for empty list
                if not data:
                    issues.append("Empty list configuration")
            
            status = TestStatus.WARNING if issues else TestStatus.PASS
            severity = Severity.LOW if issues else Severity.LOW
            
            return TestResult(
                component="config_validator",
                test_name="yaml_structure",
                status=status,
                message=f"YAML structure validation: {Path(file_path).name}",
                severity=severity,
                details={
                    "file_path": file_path,
                    "issues": issues,
                    "data_type": type(data).__name__
                }
            )
            
        except Exception as e:
            return TestResult(
                component="config_validator",
                test_name="yaml_structure",
                status=TestStatus.FAIL,
                message=f"Error validating YAML structure: {str(e)}",
                severity=Severity.MEDIUM,
                details={"file_path": file_path, "error": str(e)}
            )
    
    def _validate_yaml_content(self, file_path: str, data: Any) -> TestResult:
        """Validate YAML content for common configuration patterns"""
        try:
            suggestions = []
            
            if isinstance(data, dict):
                # Check for common configuration keys
                common_keys = ['name', 'version', 'description', 'settings', 'config']
                has_common_keys = any(key in data for key in common_keys)
                
                if not has_common_keys and len(data) > 3:
                    suggestions.append("Consider adding descriptive keys like 'name' or 'description'")
                
                # Check for sensitive data patterns
                sensitive_patterns = ['password', 'secret', 'key', 'token']
                for key in data.keys():
                    if any(pattern in str(key).lower() for pattern in sensitive_patterns):
                        suggestions.append(f"Potential sensitive data in key: {key}")
            
            status = TestStatus.WARNING if suggestions else TestStatus.PASS
            
            return TestResult(
                component="config_validator",
                test_name="yaml_content",
                status=status,
                message=f"YAML content validation: {Path(file_path).name}",
                severity=Severity.LOW,
                details={
                    "file_path": file_path,
                    "suggestions": suggestions
                }
            )
            
        except Exception as e:
            return TestResult(
                component="config_validator",
                test_name="yaml_content",
                status=TestStatus.FAIL,
                message=f"Error validating YAML content: {str(e)}",
                severity=Severity.LOW,
                details={"file_path": file_path, "error": str(e)}
            )
    
    def _validate_json_file(self, file_path: str, content: str) -> List[TestResult]:
        """Validate JSON configuration file"""
        results = []
        
        # Test 1: JSON syntax validation
        is_valid, error_msg = ValidationUtils.validate_json_format(content)
        
        if is_valid:
            try:
                data = json.loads(content)
                
                results.append(TestResult(
                    component="config_validator",
                    test_name="json_syntax",
                    status=TestStatus.PASS,
                    message=f"Valid JSON syntax: {Path(file_path).name}",
                    details={
                        "file_path": file_path,
                        "data_type": type(data).__name__,
                        "keys": list(data.keys()) if isinstance(data, dict) else None
                    }
                ))
                
                # Test 2: JSON structure validation
                structure_result = self._validate_json_structure(file_path, data)
                results.append(structure_result)
                
            except Exception as e:
                results.append(TestResult(
                    component="config_validator",
                    test_name="json_syntax",
                    status=TestStatus.FAIL,
                    message=f"JSON parsing error: {str(e)}",
                    severity=Severity.HIGH,
                    details={"file_path": file_path, "error": str(e)}
                ))
        else:
            results.append(TestResult(
                component="config_validator",
                test_name="json_syntax",
                status=TestStatus.FAIL,
                message=f"Invalid JSON syntax: {error_msg}",
                severity=Severity.HIGH,
                details={"file_path": file_path, "error": error_msg}
            ))
        
        return results
    
    def _validate_json_structure(self, file_path: str, data: Any) -> TestResult:
        """Validate JSON structure"""
        try:
            issues = []
            
            if isinstance(data, dict):
                # Check for null values
                null_keys = [k for k, v in data.items() if v is None]
                if null_keys:
                    issues.append(f"Null values for keys: {null_keys}")
                
                # Check nesting depth
                max_depth = self._get_dict_depth(data)
                if max_depth > 6:
                    issues.append(f"Very deep nesting detected (depth: {max_depth})")
            
            status = TestStatus.WARNING if issues else TestStatus.PASS
            
            return TestResult(
                component="config_validator",
                test_name="json_structure",
                status=status,
                message=f"JSON structure validation: {Path(file_path).name}",
                severity=Severity.LOW,
                details={
                    "file_path": file_path,
                    "issues": issues,
                    "data_type": type(data).__name__
                }
            )
            
        except Exception as e:
            return TestResult(
                component="config_validator",
                test_name="json_structure",
                status=TestStatus.FAIL,
                message=f"Error validating JSON structure: {str(e)}",
                severity=Severity.MEDIUM,
                details={"file_path": file_path, "error": str(e)}
            )
    
    def _validate_csv_file(self, file_path: str, content: str) -> List[TestResult]:
        """Validate CSV configuration file"""
        results = []
        
        # Test 1: CSV format validation
        is_valid, error_msg, csv_info = ValidationUtils.validate_csv_format(content)
        
        if is_valid:
            results.append(TestResult(
                component="config_validator",
                test_name="csv_format",
                status=TestStatus.PASS,
                message=f"Valid CSV format: {Path(file_path).name}",
                details={
                    "file_path": file_path,
                    "row_count": csv_info.get("row_count", 0),
                    "column_count": csv_info.get("column_count", 0)
                }
            ))
            
            # Test 2: CSV content validation
            content_result = self._validate_csv_content(file_path, content)
            results.append(content_result)
            
        else:
            results.append(TestResult(
                component="config_validator",
                test_name="csv_format",
                status=TestStatus.FAIL,
                message=f"Invalid CSV format: {error_msg}",
                severity=Severity.HIGH,
                details={"file_path": file_path, "error": error_msg}
            ))
        
        return results
    
    def _validate_csv_content(self, file_path: str, content: str) -> TestResult:
        """Validate CSV content"""
        try:
            reader = csv.reader(io.StringIO(content))
            rows = list(reader)
            
            issues = []
            
            if not rows:
                issues.append("Empty CSV file")
            else:
                # Check for consistent column count
                if len(rows) > 1:
                    first_row_cols = len(rows[0])
                    inconsistent_rows = []
                    
                    for i, row in enumerate(rows[1:], 2):
                        if len(row) != first_row_cols:
                            inconsistent_rows.append(i)
                    
                    if inconsistent_rows:
                        issues.append(f"Inconsistent column count in rows: {inconsistent_rows}")
                
                # Check for empty cells
                empty_cells = []
                for i, row in enumerate(rows):
                    for j, cell in enumerate(row):
                        if not cell.strip():
                            empty_cells.append(f"Row {i+1}, Col {j+1}")
                
                if len(empty_cells) > len(rows) * 0.1:  # More than 10% empty
                    issues.append(f"Many empty cells detected: {len(empty_cells)} total")
            
            status = TestStatus.WARNING if issues else TestStatus.PASS
            
            return TestResult(
                component="config_validator",
                test_name="csv_content",
                status=status,
                message=f"CSV content validation: {Path(file_path).name}",
                severity=Severity.LOW,
                details={
                    "file_path": file_path,
                    "issues": issues,
                    "total_rows": len(rows),
                    "total_columns": len(rows[0]) if rows else 0
                }
            )
            
        except Exception as e:
            return TestResult(
                component="config_validator",
                test_name="csv_content",
                status=TestStatus.FAIL,
                message=f"Error validating CSV content: {str(e)}",
                severity=Severity.MEDIUM,
                details={"file_path": file_path, "error": str(e)}
            )
    
    def _validate_python_config(self, file_path: str, content: str) -> List[TestResult]:
        """Validate Python configuration file"""
        results = []
        
        try:
            # Check if it's a valid Python file
            import ast
            tree = ast.parse(content)
            
            # Look for configuration patterns
            config_vars = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            config_vars.append(target.id)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
            
            results.append(TestResult(
                component="config_validator",
                test_name="python_config",
                status=TestStatus.PASS,
                message=f"Valid Python config: {Path(file_path).name}",
                details={
                    "file_path": file_path,
                    "config_variables": config_vars,
                    "config_classes": classes
                }
            ))
            
        except SyntaxError as e:
            results.append(TestResult(
                component="config_validator",
                test_name="python_config",
                status=TestStatus.FAIL,
                message=f"Python config syntax error: {str(e)}",
                severity=Severity.HIGH,
                details={"file_path": file_path, "error": str(e)}
            ))
        except Exception as e:
            results.append(TestResult(
                component="config_validator",
                test_name="python_config",
                status=TestStatus.FAIL,
                message=f"Error validating Python config: {str(e)}",
                severity=Severity.MEDIUM,
                details={"file_path": file_path, "error": str(e)}
            ))
        
        return results
    
    def _get_dict_depth(self, d: Dict, depth: int = 0) -> int:
        """Get maximum depth of nested dictionary"""
        if not isinstance(d, dict):
            return depth
        
        if not d:
            return depth + 1
        
        return max(self._get_dict_depth(v, depth + 1) for v in d.values())
    
    def can_auto_fix(self, issue: TestResult) -> bool:
        """Check if configuration issue can be auto-fixed"""
        fixable_issues = [
            "yaml_structure",
            "json_structure", 
            "csv_content"
        ]
        
        return (issue.test_name in fixable_issues and
                self.config.auto_fix_enabled and
                issue.status in [TestStatus.WARNING, TestStatus.FAIL])
    
    def auto_fix(self, issue: TestResult) -> TestResult:
        """Attempt to auto-fix configuration issues"""
        if not self.can_auto_fix(issue):
            return TestResult(
                component="config_validator",
                test_name="auto_fix",
                status=TestStatus.SKIPPED,
                message="Configuration issue cannot be auto-fixed",
                details={"original_issue": issue.to_dict()}
            )
        
        file_path = issue.details.get("file_path")
        if not file_path:
            return TestResult(
                component="config_validator",
                test_name="auto_fix",
                status=TestStatus.FAIL,
                message="No file path in issue details",
                severity=Severity.HIGH
            )
        
        # Create backup
        backup_path = FileUtils.backup_file(file_path)
        if not backup_path:
            return TestResult(
                component="config_validator",
                test_name="auto_fix",
                status=TestStatus.FAIL,
                message="Could not create backup file",
                severity=Severity.HIGH
            )
        
        try:
            content = FileUtils.read_file_safe(file_path)
            if content is None:
                return TestResult(
                    component="config_validator",
                    test_name="auto_fix",
                    status=TestStatus.FAIL,
                    message="Could not read file for fixing",
                    severity=Severity.HIGH
                )
            
            fixed_content = content
            fixes_applied = []
            
            # Apply fixes based on issue type
            if issue.test_name == "csv_content":
                fixed_content, csv_fixes = self._fix_csv_content(content)
                fixes_applied.extend(csv_fixes)
            
            # Write fixed content
            if FileUtils.write_file_safe(file_path, fixed_content):
                return TestResult(
                    component="config_validator",
                    test_name="auto_fix",
                    status=TestStatus.PASS,
                    message=f"Successfully applied {len(fixes_applied)} fixes",
                    auto_fixed=True,
                    details={
                        "file_path": file_path,
                        "backup_path": backup_path,
                        "fixes_applied": fixes_applied
                    }
                )
            else:
                return TestResult(
                    component="config_validator",
                    test_name="auto_fix",
                    status=TestStatus.FAIL,
                    message="Could not write fixed content",
                    severity=Severity.HIGH
                )
                
        except Exception as e:
            # Restore from backup
            if backup_path:
                FileUtils.restore_file(file_path, backup_path)
            
            return TestResult(
                component="config_validator",
                test_name="auto_fix",
                status=TestStatus.FAIL,
                message=f"Auto-fix failed: {str(e)}",
                severity=Severity.HIGH,
                details={"error": str(e)}
            )
    
    def _fix_csv_content(self, content: str) -> Tuple[str, List[str]]:
        """Fix CSV content issues"""
        fixes = []
        
        try:
            reader = csv.reader(io.StringIO(content))
            rows = list(reader)
            
            if not rows:
                return content, fixes
            
            # Fix inconsistent column counts by padding with empty strings
            max_cols = max(len(row) for row in rows)
            fixed_rows = []
            
            for i, row in enumerate(rows):
                if len(row) < max_cols:
                    padded_row = row + [''] * (max_cols - len(row))
                    fixed_rows.append(padded_row)
                    fixes.append(f"Padded row {i+1} to {max_cols} columns")
                else:
                    fixed_rows.append(row)
            
            # Write back to CSV format
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerows(fixed_rows)
            
            return output.getvalue(), fixes
            
        except Exception:
            return content, fixes