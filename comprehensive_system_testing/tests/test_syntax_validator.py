"""
Unit Tests for Syntax Validator
==============================

Test cases for the SyntaxValidator class.
"""

import unittest
import tempfile
import os
from pathlib import Path

from ..core.syntax_validator import SyntaxValidator
from ..core.models import TestConfiguration, TestStatus, Severity


class TestSyntaxValidator(unittest.TestCase):
    """Test cases for SyntaxValidator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = TestConfiguration(auto_fix_enabled=True)
        self.validator = SyntaxValidator(self.config)
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_test_file(self, filename: str, content: str) -> str:
        """Create a temporary test file"""
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path
    
    def test_valid_python_syntax(self):
        """Test validation of valid Python syntax"""
        content = '''
def hello_world():
    """A simple function"""
    print("Hello, World!")
    return True

class TestClass:
    def __init__(self):
        self.value = 42
'''
        file_path = self._create_test_file("valid.py", content)
        results = self.validator.validate(file_path)
        
        # Should have results for syntax, imports, structure, and indentation
        self.assertEqual(len(results), 4)
        
        # Syntax test should pass
        syntax_result = next(r for r in results if r.test_name == "python_syntax")
        self.assertEqual(syntax_result.status, TestStatus.PASS)
    
    def test_invalid_python_syntax(self):
        """Test validation of invalid Python syntax"""
        content = '''
def broken_function(
    print("Missing closing parenthesis")
    return True
'''
        file_path = self._create_test_file("invalid.py", content)
        results = self.validator.validate(file_path)
        
        # Syntax test should fail
        syntax_result = next(r for r in results if r.test_name == "python_syntax")
        self.assertEqual(syntax_result.status, TestStatus.FAIL)
        self.assertEqual(syntax_result.severity, Severity.CRITICAL)
    
    def test_indentation_issues(self):
        """Test detection of indentation issues"""
        content = '''
def mixed_indentation():
    print("Using spaces")
\tprint("Using tabs")  # This line uses tabs
    return True
'''
        file_path = self._create_test_file("mixed_indent.py", content)
        results = self.validator.validate(file_path)
        
        # Indentation test should fail
        indent_result = next(r for r in results if r.test_name == "indentation")
        self.assertEqual(indent_result.status, TestStatus.FAIL)
    
    def test_import_statement_issues(self):
        """Test detection of import statement issues"""
        content = '''
import os,
from sys import *
import json
'''
        file_path = self._create_test_file("import_issues.py", content)
        results = self.validator.validate(file_path)
        
        # Import test should show warnings
        import_result = next(r for r in results if r.test_name == "import_statements")
        self.assertEqual(import_result.status, TestStatus.WARNING)
    
    def test_auto_fix_capability(self):
        """Test auto-fix capability detection"""
        from ..core.models import TestResult
        
        # Create a fixable issue
        fixable_issue = TestResult(
            component="syntax_validator",
            test_name="indentation",
            status=TestStatus.FAIL,
            message="Indentation issue",
            details={"file_path": "/test/file.py"}
        )
        
        # Should be fixable
        self.assertTrue(self.validator.can_auto_fix(fixable_issue))
        
        # Create a non-fixable issue
        non_fixable_issue = TestResult(
            component="syntax_validator",
            test_name="python_syntax",
            status=TestStatus.FAIL,
            message="Syntax error",
            details={"file_path": "/test/file.py"}
        )
        
        # Should not be fixable
        self.assertFalse(self.validator.can_auto_fix(non_fixable_issue))
    
    def test_auto_fix_indentation(self):
        """Test auto-fixing of indentation issues"""
        content = '''
def mixed_function():
    print("Spaces")
\tprint("Tabs")
    return True
'''
        file_path = self._create_test_file("to_fix.py", content)
        
        # Create an indentation issue
        from ..core.models import TestResult
        issue = TestResult(
            component="syntax_validator",
            test_name="indentation",
            status=TestStatus.FAIL,
            message="Mixed indentation",
            details={"file_path": file_path}
        )
        
        # Apply auto-fix
        fix_result = self.validator.auto_fix(issue)
        
        # Fix should succeed
        self.assertEqual(fix_result.status, TestStatus.PASS)
        self.assertTrue(fix_result.auto_fixed)
        
        # Check that file was actually fixed
        with open(file_path, 'r') as f:
            fixed_content = f.read()
        
        # Should not contain tabs anymore
        self.assertNotIn('\t', fixed_content)
    
    def test_code_structure_analysis(self):
        """Test code structure analysis"""
        content = '''
class MyClass:
    """A test class"""
    
    def __init__(self):
        self.value = 0
    
    def method1(self):
        return self.value
    
    def method2(self):
        return self.value * 2

def standalone_function():
    """A standalone function"""
    return "hello"
'''
        file_path = self._create_test_file("structure.py", content)
        results = self.validator.validate(file_path)
        
        # Structure test should pass
        structure_result = next(r for r in results if r.test_name == "code_structure")
        self.assertEqual(structure_result.status, TestStatus.PASS)
        
        # Should detect classes and functions
        details = structure_result.details
        self.assertIn("MyClass", details["classes"])
        self.assertIn("standalone_function", details["functions"])
    
    def test_empty_file_detection(self):
        """Test detection of empty or minimal files"""
        content = "# Just a comment\n"
        file_path = self._create_test_file("empty.py", content)
        results = self.validator.validate(file_path)
        
        # Structure test should show warning for empty file
        structure_result = next(r for r in results if r.test_name == "code_structure")
        self.assertEqual(structure_result.status, TestStatus.WARNING)


if __name__ == '__main__':
    unittest.main()    

    def test_trailing_whitespace_detection(self):
        """Test detection of trailing whitespace"""
        content = '''
def function_with_whitespace():
    print("Hello")   
    return True  
'''
        file_path = self._create_test_file("whitespace.py", content)
        results = self.validator.validate(file_path)
        
        # Should detect trailing whitespace
        whitespace_result = next(r for r in results if r.test_name == "trailing_whitespace")
        self.assertEqual(whitespace_result.status, TestStatus.WARNING)
    
    def test_quote_consistency_detection(self):
        """Test detection of mixed quote usage"""
        content = '''
def mixed_quotes():
    single = 'Hello'
    double = "World"
    return single + double
'''
        file_path = self._create_test_file("mixed_quotes.py", content)
        results = self.validator.validate(file_path)
        
        # Should detect mixed quotes
        quote_result = next(r for r in results if r.test_name == "quote_consistency")
        self.assertEqual(quote_result.status, TestStatus.WARNING)
    
    def test_bracket_matching_detection(self):
        """Test detection of bracket matching issues"""
        content = '''
def unmatched_brackets():
    my_list = [1, 2, 3
    return my_list
'''
        file_path = self._create_test_file("unmatched.py", content)
        results = self.validator.validate(file_path)
        
        # Should detect bracket issues
        bracket_result = next(r for r in results if r.test_name == "bracket_matching")
        self.assertEqual(bracket_result.status, TestStatus.FAIL)
    
    def test_auto_fix_trailing_whitespace(self):
        """Test auto-fixing of trailing whitespace"""
        content = '''
def function_with_whitespace():
    print("Hello")   
    return True  
'''
        file_path = self._create_test_file("fix_whitespace.py", content)
        
        # Create a trailing whitespace issue
        from ..core.models import TestResult
        issue = TestResult(
            component="syntax_validator",
            test_name="trailing_whitespace",
            status=TestStatus.WARNING,
            message="Trailing whitespace",
            details={"file_path": file_path}
        )
        
        # Apply auto-fix
        fix_result = self.validator.auto_fix(issue)
        
        # Fix should succeed
        self.assertEqual(fix_result.status, TestStatus.PASS)
        self.assertTrue(fix_result.auto_fixed)
        
        # Check that file was actually fixed
        with open(file_path, 'r') as f:
            fixed_content = f.read()
        
        # Should not have trailing whitespace
        lines = fixed_content.split('\n')
        for line in lines:
            self.assertFalse(line.endswith(' ') or line.endswith('\t'))
    
    def test_comprehensive_validation(self):
        """Test comprehensive validation of a complex file"""
        content = '''
import os,
from sys import *

class TestClass:
\tdef __init__(self):  
\t\tself.value = 'mixed quotes'
\t\tself.other = "double quotes"
    
    def method_with_issues():
        my_list = [1, 2, 3,
        return my_list
'''
        file_path = self._create_test_file("complex.py", content)
        results = self.validator.validate(file_path)
        
        # Should have multiple validation results
        self.assertGreater(len(results), 5)
        
        # Should detect various issues
        test_names = [r.test_name for r in results]
        self.assertIn("python_syntax", test_names)
        self.assertIn("import_statements", test_names)
        self.assertIn("indentation", test_names)
        self.assertIn("trailing_whitespace", test_names)
        self.assertIn("quote_consistency", test_names)