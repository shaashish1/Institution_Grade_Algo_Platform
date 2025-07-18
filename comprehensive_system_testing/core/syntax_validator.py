"""
Syntax Validator
===============

AST-based Python syntax validation with auto-fixing capabilities.
"""

import ast
import re
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from .base_validator import BaseValidator
from .models import TestResult, TestStatus, Severity, TestConfiguration
from ..utils.file_utils import FileUtils
from ..utils.validation_utils import ValidationUtils
from ..utils.logger import TestLogger


class SyntaxValidator(BaseValidator):
    """Validates Python syntax using AST parsing and provides auto-fixing"""
    
    def __init__(self, config: TestConfiguration):
        super().__init__(config)
        self.logger = TestLogger()
    
    def validate(self, target: str) -> List[TestResult]:
        """
        Validate Python files in the target directory or single file
        
        Args:
            target: Directory path or single file path to validate
            
        Returns:
            List of TestResult objects
        """
        results = []
        start_time = time.time()
        
        # Get Python files to validate
        if Path(target).is_file():
            python_files = [target]
        else:
            python_files = FileUtils.find_python_files(target)
        
        self.logger.info(f"Validating syntax for {len(python_files)} Python files")
        
        for file_path in python_files:
            file_results = self._validate_file(file_path)
            results.extend(file_results)
        
        execution_time = time.time() - start_time
        self.logger.info(f"Syntax validation completed in {execution_time:.2f} seconds")
        
        return results
    
    def _validate_file(self, file_path: str) -> List[TestResult]:
        """Validate a single Python file"""
        results = []
        
        # Read file content
        content = FileUtils.read_file_safe(file_path)
        if content is None:
            return [TestResult(
                component="syntax_validator",
                test_name="file_read",
                status=TestStatus.FAIL,
                message=f"Could not read file: {file_path}",
                severity=Severity.HIGH,
                details={"file_path": file_path}
            )]
        
        # Test 1: Basic syntax validation
        syntax_result = self._validate_python_syntax(file_path, content)
        results.append(syntax_result)
        
        # Test 2: Import statement validation
        import_result = self._validate_import_statements(file_path, content)
        results.append(import_result)
        
        # Test 3: Code structure validation
        structure_result = self._validate_code_structure(file_path, content)
        results.append(structure_result)
        
        # Test 4: Indentation consistency
        indent_result = self._validate_indentation(file_path, content)
        results.append(indent_result)
        
        # Test 5: Quote consistency
        quote_result = self._validate_quote_consistency(file_path, content)
        results.append(quote_result)
        
        # Test 6: Trailing whitespace
        whitespace_result = self._validate_trailing_whitespace(file_path, content)
        results.append(whitespace_result)
        
        # Test 7: Bracket matching
        bracket_result = self._validate_bracket_matching(file_path, content)
        results.append(bracket_result)
        
        return results
    
    def _validate_python_syntax(self, file_path: str, content: str) -> TestResult:
        """Validate Python syntax using AST"""
        try:
            ast.parse(content)
            return TestResult(
                component="syntax_validator",
                test_name="python_syntax",
                status=TestStatus.PASS,
                message=f"Valid Python syntax: {Path(file_path).name}",
                details={"file_path": file_path}
            )
        except SyntaxError as e:
            return TestResult(
                component="syntax_validator",
                test_name="python_syntax",
                status=TestStatus.FAIL,
                message=f"Syntax error in {Path(file_path).name}: {e.msg}",
                severity=Severity.CRITICAL,
                details={
                    "file_path": file_path,
                    "line_number": e.lineno,
                    "column": e.offset,
                    "error_text": e.text,
                    "error_message": e.msg
                }
            )
        except Exception as e:
            return TestResult(
                component="syntax_validator",
                test_name="python_syntax",
                status=TestStatus.FAIL,
                message=f"Parse error in {Path(file_path).name}: {str(e)}",
                severity=Severity.HIGH,
                details={"file_path": file_path, "error": str(e)}
            )
    
    def _validate_import_statements(self, file_path: str, content: str) -> TestResult:
        """Validate import statement syntax"""
        try:
            imports = ValidationUtils.extract_imports(content)
            
            # Check for common import issues
            issues = []
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    # Check for trailing commas in imports
                    if line.endswith(','):
                        issues.append(f"Line {i}: Trailing comma in import statement")
                    
                    # Check for wildcard imports (not critical, but warning)
                    if 'import *' in line:
                        issues.append(f"Line {i}: Wildcard import detected (consider explicit imports)")
            
            if issues:
                return TestResult(
                    component="syntax_validator",
                    test_name="import_statements",
                    status=TestStatus.WARNING,
                    message=f"Import issues found in {Path(file_path).name}",
                    severity=Severity.MEDIUM,
                    details={
                        "file_path": file_path,
                        "issues": issues,
                        "import_count": len(imports)
                    }
                )
            else:
                return TestResult(
                    component="syntax_validator",
                    test_name="import_statements",
                    status=TestStatus.PASS,
                    message=f"Import statements valid: {Path(file_path).name}",
                    details={
                        "file_path": file_path,
                        "import_count": len(imports)
                    }
                )
                
        except Exception as e:
            return TestResult(
                component="syntax_validator",
                test_name="import_statements",
                status=TestStatus.FAIL,
                message=f"Error validating imports in {Path(file_path).name}: {str(e)}",
                severity=Severity.MEDIUM,
                details={"file_path": file_path, "error": str(e)}
            )
    
    def _validate_code_structure(self, file_path: str, content: str) -> TestResult:
        """Validate code structure (classes, functions, etc.)"""
        try:
            tree = ast.parse(content)
            
            # Count different types of nodes
            classes = []
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
            
            # Check for basic structure issues
            issues = []
            
            # Check if file has any meaningful content
            if not classes and not functions and len(content.strip()) < 50:
                issues.append("File appears to be mostly empty")
            
            # Check for very long functions (>100 lines)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if hasattr(node, 'end_lineno') and node.end_lineno:
                        func_length = node.end_lineno - node.lineno
                        if func_length > 100:
                            issues.append(f"Function '{node.name}' is very long ({func_length} lines)")
            
            status = TestStatus.WARNING if issues else TestStatus.PASS
            severity = Severity.LOW if issues else Severity.LOW
            
            return TestResult(
                component="syntax_validator",
                test_name="code_structure",
                status=status,
                message=f"Code structure analysis: {Path(file_path).name}",
                severity=severity,
                details={
                    "file_path": file_path,
                    "classes": classes,
                    "functions": functions,
                    "issues": issues
                }
            )
            
        except Exception as e:
            return TestResult(
                component="syntax_validator",
                test_name="code_structure",
                status=TestStatus.FAIL,
                message=f"Error analyzing structure of {Path(file_path).name}: {str(e)}",
                severity=Severity.MEDIUM,
                details={"file_path": file_path, "error": str(e)}
            )
    
    def _validate_indentation(self, file_path: str, content: str) -> TestResult:
        """Validate indentation consistency"""
        is_consistent, issues = ValidationUtils.check_indentation_consistency(content)
        
        if is_consistent:
            return TestResult(
                component="syntax_validator",
                test_name="indentation",
                status=TestStatus.PASS,
                message=f"Consistent indentation: {Path(file_path).name}",
                details={"file_path": file_path}
            )
        else:
            return TestResult(
                component="syntax_validator",
                test_name="indentation",
                status=TestStatus.FAIL,
                message=f"Indentation issues in {Path(file_path).name}",
                severity=Severity.MEDIUM,
                details={
                    "file_path": file_path,
                    "issues": issues
                }
            )
    
    def can_auto_fix(self, issue: TestResult) -> bool:
        """Check if an issue can be automatically fixed"""
        fixable_tests = [
            "indentation",
            "import_statements",
            "quote_consistency",
            "bracket_matching",
            "trailing_whitespace"
        ]
        
        # Check for specific syntax errors that can be auto-fixed
        if issue.test_name == "python_syntax":
            error_msg = issue.details.get("error_message", "").lower()
            fixable_syntax_errors = [
                "trailing comma",
                "missing comma",
                "inconsistent use of tabs and spaces",
                "unexpected indent",
                "unindent does not match"
            ]
            
            for fixable_error in fixable_syntax_errors:
                if fixable_error in error_msg:
                    return True
        
        return (issue.test_name in fixable_tests and 
                self.config.auto_fix_enabled and
                issue.status in [TestStatus.FAIL, TestStatus.WARNING])
    
    def auto_fix(self, issue: TestResult) -> TestResult:
        """Attempt to automatically fix an issue"""
        if not self.can_auto_fix(issue):
            return TestResult(
                component="syntax_validator",
                test_name="auto_fix",
                status=TestStatus.SKIPPED,
                message="Issue cannot be auto-fixed",
                details={"original_issue": issue.to_dict()}
            )
        
        file_path = issue.details.get("file_path")
        if not file_path:
            return TestResult(
                component="syntax_validator",
                test_name="auto_fix",
                status=TestStatus.FAIL,
                message="No file path in issue details",
                severity=Severity.HIGH
            )
        
        # Create backup
        backup_path = FileUtils.backup_file(file_path)
        if not backup_path:
            return TestResult(
                component="syntax_validator",
                test_name="auto_fix",
                status=TestStatus.FAIL,
                message="Could not create backup file",
                severity=Severity.HIGH
            )
        
        try:
            content = FileUtils.read_file_safe(file_path)
            if content is None:
                return TestResult(
                    component="syntax_validator",
                    test_name="auto_fix",
                    status=TestStatus.FAIL,
                    message="Could not read file for fixing",
                    severity=Severity.HIGH
                )
            
            fixed_content = content
            fixes_applied = []
            
            # Apply fixes based on issue type
            if issue.test_name == "indentation":
                fixed_content, indent_fixes = self._fix_indentation(content)
                fixes_applied.extend(indent_fixes)
            
            elif issue.test_name == "import_statements":
                fixed_content, import_fixes = self._fix_import_statements(content)
                fixes_applied.extend(import_fixes)
            
            elif issue.test_name == "trailing_whitespace":
                fixed_content, whitespace_fixes = self._fix_trailing_whitespace(content)
                fixes_applied.extend(whitespace_fixes)
            
            elif issue.test_name == "quote_consistency":
                fixed_content, quote_fixes = self._fix_quote_consistency(content)
                fixes_applied.extend(quote_fixes)
            
            # Write fixed content
            if FileUtils.write_file_safe(file_path, fixed_content):
                return TestResult(
                    component="syntax_validator",
                    test_name="auto_fix",
                    status=TestStatus.PASS,
                    message=f"Successfully fixed {len(fixes_applied)} issues",
                    auto_fixed=True,
                    details={
                        "file_path": file_path,
                        "backup_path": backup_path,
                        "fixes_applied": fixes_applied,
                        "original_issue": issue.test_name
                    }
                )
            else:
                return TestResult(
                    component="syntax_validator",
                    test_name="auto_fix",
                    status=TestStatus.FAIL,
                    message="Could not write fixed content to file",
                    severity=Severity.HIGH
                )
                
        except Exception as e:
            # Restore from backup if fix failed
            if backup_path:
                FileUtils.restore_file(file_path, backup_path)
            
            return TestResult(
                component="syntax_validator",
                test_name="auto_fix",
                status=TestStatus.FAIL,
                message=f"Auto-fix failed: {str(e)}",
                severity=Severity.HIGH,
                details={"error": str(e), "backup_restored": backup_path is not None}
            )
    
    def _fix_indentation(self, content: str) -> Tuple[str, List[str]]:
        """Fix indentation issues"""
        lines = content.split('\n')
        fixed_lines = []
        fixes = []
        
        for i, line in enumerate(lines):
            if line.strip():  # Non-empty line
                # Convert tabs to spaces (4 spaces per tab)
                if '\t' in line:
                    fixed_line = line.replace('\t', '    ')
                    if fixed_line != line:
                        fixes.append(f"Line {i+1}: Converted tabs to spaces")
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines), fixes
    
    def _fix_import_statements(self, content: str) -> Tuple[str, List[str]]:
        """Fix import statement issues"""
        lines = content.split('\n')
        fixed_lines = []
        fixes = []
        
        for i, line in enumerate(lines):
            fixed_line = line
            
            # Remove trailing commas from import statements
            if (line.strip().startswith('import ') or line.strip().startswith('from ')) and line.rstrip().endswith(','):
                fixed_line = line.rstrip().rstrip(',')
                fixes.append(f"Line {i+1}: Removed trailing comma from import")
            
            fixed_lines.append(fixed_line)
        
        return '\n'.join(fixed_lines), fixes
    
    def _validate_quote_consistency(self, file_path: str, content: str) -> TestResult:
        """Validate quote consistency in strings"""
        try:
            lines = content.split('\n')
            issues = []
            
            # Count single vs double quotes
            single_quote_count = 0
            double_quote_count = 0
            
            for i, line in enumerate(lines, 1):
                # Skip comments
                if line.strip().startswith('#'):
                    continue
                
                # Count quotes (simple heuristic)
                single_quotes = line.count("'") - line.count("\\'")
                double_quotes = line.count('"') - line.count('\\"')
                
                single_quote_count += single_quotes
                double_quote_count += double_quotes
            
            # Check for mixed usage (warning, not error)
            if single_quote_count > 0 and double_quote_count > 0:
                ratio = min(single_quote_count, double_quote_count) / max(single_quote_count, double_quote_count)
                if ratio > 0.3:  # Mixed usage threshold
                    issues.append("Mixed single and double quotes detected")
            
            if issues:
                return TestResult(
                    component="syntax_validator",
                    test_name="quote_consistency",
                    status=TestStatus.WARNING,
                    message=f"Quote consistency issues in {Path(file_path).name}",
                    severity=Severity.LOW,
                    details={
                        "file_path": file_path,
                        "issues": issues,
                        "single_quotes": single_quote_count,
                        "double_quotes": double_quote_count
                    }
                )
            else:
                return TestResult(
                    component="syntax_validator",
                    test_name="quote_consistency",
                    status=TestStatus.PASS,
                    message=f"Quote usage consistent: {Path(file_path).name}",
                    details={"file_path": file_path}
                )
                
        except Exception as e:
            return TestResult(
                component="syntax_validator",
                test_name="quote_consistency",
                status=TestStatus.FAIL,
                message=f"Error checking quotes in {Path(file_path).name}: {str(e)}",
                severity=Severity.LOW,
                details={"file_path": file_path, "error": str(e)}
            )
    
    def _validate_trailing_whitespace(self, file_path: str, content: str) -> TestResult:
        """Validate trailing whitespace"""
        lines = content.split('\n')
        issues = []
        
        for i, line in enumerate(lines, 1):
            if line.endswith(' ') or line.endswith('\t'):
                issues.append(f"Line {i}: Trailing whitespace")
        
        if issues:
            return TestResult(
                component="syntax_validator",
                test_name="trailing_whitespace",
                status=TestStatus.WARNING,
                message=f"Trailing whitespace found in {Path(file_path).name}",
                severity=Severity.LOW,
                details={
                    "file_path": file_path,
                    "issues": issues
                }
            )
        else:
            return TestResult(
                component="syntax_validator",
                test_name="trailing_whitespace",
                status=TestStatus.PASS,
                message=f"No trailing whitespace: {Path(file_path).name}",
                details={"file_path": file_path}
            )
    
    def _validate_bracket_matching(self, file_path: str, content: str) -> TestResult:
        """Validate bracket matching (basic check)"""
        try:
            # Use AST parsing to check for bracket issues
            ast.parse(content)
            
            # Additional manual checks for common bracket issues
            bracket_pairs = {'(': ')', '[': ']', '{': '}'}
            stack = []
            issues = []
            
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                for char_pos, char in enumerate(line):
                    if char in bracket_pairs:
                        stack.append((char, line_num, char_pos))
                    elif char in bracket_pairs.values():
                        if not stack:
                            issues.append(f"Line {line_num}: Unmatched closing bracket '{char}'")
                        else:
                            open_bracket, _, _ = stack.pop()
                            if bracket_pairs[open_bracket] != char:
                                issues.append(f"Line {line_num}: Mismatched bracket pair")
            
            # Check for unclosed brackets
            for open_bracket, line_num, char_pos in stack:
                issues.append(f"Line {line_num}: Unclosed bracket '{open_bracket}'")
            
            if issues:
                return TestResult(
                    component="syntax_validator",
                    test_name="bracket_matching",
                    status=TestStatus.FAIL,
                    message=f"Bracket matching issues in {Path(file_path).name}",
                    severity=Severity.HIGH,
                    details={
                        "file_path": file_path,
                        "issues": issues
                    }
                )
            else:
                return TestResult(
                    component="syntax_validator",
                    test_name="bracket_matching",
                    status=TestStatus.PASS,
                    message=f"Brackets properly matched: {Path(file_path).name}",
                    details={"file_path": file_path}
                )
                
        except SyntaxError:
            # If AST parsing fails, there might be bracket issues
            return TestResult(
                component="syntax_validator",
                test_name="bracket_matching",
                status=TestStatus.FAIL,
                message=f"Potential bracket issues in {Path(file_path).name}",
                severity=Severity.HIGH,
                details={"file_path": file_path}
            )
        except Exception as e:
            return TestResult(
                component="syntax_validator",
                test_name="bracket_matching",
                status=TestStatus.FAIL,
                message=f"Error checking brackets in {Path(file_path).name}: {str(e)}",
                severity=Severity.MEDIUM,
                details={"file_path": file_path, "error": str(e)}
            )  
  
    def _fix_trailing_whitespace(self, content: str) -> Tuple[str, List[str]]:
        """Fix trailing whitespace issues"""
        lines = content.split('\n')
        fixed_lines = []
        fixes = []
        
        for i, line in enumerate(lines):
            original_line = line
            # Remove trailing whitespace
            fixed_line = line.rstrip()
            
            if fixed_line != original_line:
                fixes.append(f"Line {i+1}: Removed trailing whitespace")
            
            fixed_lines.append(fixed_line)
        
        return '\n'.join(fixed_lines), fixes
    
    def _fix_quote_consistency(self, content: str) -> Tuple[str, List[str]]:
        """Fix quote consistency issues by standardizing to double quotes"""
        lines = content.split('\n')
        fixed_lines = []
        fixes = []
        
        for i, line in enumerate(lines):
            fixed_line = line
            
            # Simple quote standardization (convert single to double quotes)
            # This is a basic implementation - more sophisticated parsing would be needed for production
            if "'" in line and not line.strip().startswith('#'):
                # Only fix simple cases to avoid breaking code
                if line.count("'") == 2 and '"' not in line:
                    fixed_line = line.replace("'", '"')
                    fixes.append(f"Line {i+1}: Standardized quotes to double quotes")
            
            fixed_lines.append(fixed_line)
        
        return '\n'.join(fixed_lines), fixes