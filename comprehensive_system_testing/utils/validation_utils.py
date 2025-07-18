"""
Validation Utility Functions
===========================

Common validation utilities used across the testing framework.
"""

import ast
import re
from typing import List, Dict, Any, Optional, Tuple


class ValidationUtils:
    """Utility class for validation operations"""
    
    @staticmethod
    def validate_python_syntax(code: str) -> Tuple[bool, Optional[str]]:
        """Validate Python syntax using AST"""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"Parse error: {str(e)}"
    
    @staticmethod
    def extract_imports(code: str) -> List[str]:
        """Extract import statements from Python code"""
        imports = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except Exception:
            pass
        return imports
    
    @staticmethod
    def check_indentation_consistency(code: str) -> Tuple[bool, List[str]]:
        """Check for consistent indentation in Python code"""
        lines = code.split('\n')
        issues = []
        
        for i, line in enumerate(lines, 1):
            if line.strip() and line.startswith(' ') and line.startswith('\t'):
                issues.append(f"Line {i}: Mixed tabs and spaces")
        
        return len(issues) == 0, issues
    
    @staticmethod
    def validate_json_format(content: str) -> Tuple[bool, Optional[str]]:
        """Validate JSON format"""
        try:
            import json
            json.loads(content)
            return True, None
        except json.JSONDecodeError as e:
            return False, f"JSON error: {str(e)}"
    
    @staticmethod
    def validate_yaml_format(content: str) -> Tuple[bool, Optional[str]]:
        """Validate YAML format"""
        try:
            import yaml
            yaml.safe_load(content)
            return True, None
        except yaml.YAMLError as e:
            return False, f"YAML error: {str(e)}"
    
    @staticmethod
    def validate_csv_format(content: str) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        """Validate CSV format and return basic info"""
        try:
            import csv
            import io
            
            reader = csv.reader(io.StringIO(content))
            rows = list(reader)
            
            if not rows:
                return False, "Empty CSV file", {}
            
            info = {
                'row_count': len(rows),
                'column_count': len(rows[0]) if rows else 0,
                'has_header': True  # Assume first row is header
            }
            
            return True, None, info
        except Exception as e:
            return False, f"CSV error: {str(e)}", {}
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations"""
        # Remove or replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return sanitized.strip()