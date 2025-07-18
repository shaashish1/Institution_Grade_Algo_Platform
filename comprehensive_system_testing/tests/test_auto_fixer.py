"""
Unit Tests for Auto Fixer
=========================

Test cases for the AutoFixer class.
"""

import unittest
import tempfile
import os
from pathlib import Path

from ..core.auto_fixer import AutoFixer
from ..core.models import TestResult, TestStatus, Severity, TestConfiguration


class TestAutoFixer(unittest.TestCase):
    """Test cases for AutoFixer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = TestConfiguration(auto_fix_enabled=True)
        self.auto_fixer = AutoFixer(self.config)
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
    
    def test_fix_indentation_issues(self):
        """Test fixing indentation issues"""
        content_with_tabs = '''
def function_with_tabs():
\tprint("Using tabs")
\treturn True
'''
        
        fixed_content, description = self.auto_fixer._fix_indentation(content_with_tabs, None)
        
        # Should convert tabs to spaces
        self.assertNotIn('\t', fixed_content)
        self.assertIn('    print("Using tabs")', fixed_content)
        self.assertIn("Fixed", description)
    
    def test_fix_trailing_whitespace(self):
        """Test fixing trailing whitespace"""
        content_with_whitespace = '''
def function():
    print("Hello")   
    return True  
'''
        
        fixed_content, description = self.auto_fixer._fix_trailing_whitespace(content_with_whitespace, None)
        
        # Should remove trailing whitespace
        lines = fixed_content.split('\n')
        for line in lines:
            self.assertFalse(line.endswith(' ') or line.endswith('\t'))
        self.assertIn("Removed trailing whitespace", description)
    
    def test_fix_import_statements(self):
        """Test fixing import statement issues"""
        content_with_import_issues = '''
import os,
from sys import path,
import json
'''
        
        fixed_content, description = self.auto_fixer._fix_import_statements(content_with_import_issues, None)
        
        # Should remove trailing commas
        self.assertNotIn('import os,', fixed_content)
        self.assertNotIn('from sys import path,', fixed_content)
        self.assertIn('import os', fixed_content)
        self.assertIn("Fixed", description)
    
    def test_fix_quote_consistency(self):
        """Test fixing quote consistency"""
        content_with_mixed_quotes = '''
def function():
    single = 'Hello'
    return single
'''
        
        fixed_content, description = self.auto_fixer._fix_quote_consistency(content_with_mixed_quotes, None)
        
        # Should standardize to double quotes
        self.assertIn('"Hello"', fixed_content)
        self.assertNotIn("'Hello'", fixed_content)
    
    def test_fix_csv_content(self):
        """Test fixing CSV content issues"""
        csv_content = '''name,age,city
John,25
Jane,30,New York
Bob,35,Chicago,Extra
'''
        
        fixed_content, description = self.auto_fixer._fix_csv_content(csv_content, None)
        
        # Should pad rows to consistent column count
        lines = fixed_content.strip().split('\n')
        header_cols = len(lines[0].split(','))
        
        for line in lines[1:]:
            cols = len(line.split(','))
            self.assertEqual(cols, header_cols)
    
    def test_group_issues_by_file(self):
        """Test grouping issues by file path"""
        issues = [
            TestResult(
                component="test",
                test_name="test1",
                status=TestStatus.FAIL,
                message="Issue 1",
                details={"file_path": "/path/file1.py"}
            ),
            TestResult(
                component="test",
                test_name="test2",
                status=TestStatus.FAIL,
                message="Issue 2",
                details={"file_path": "/path/file1.py"}
            ),
            TestResult(
                component="test",
                test_name="test3",
                status=TestStatus.FAIL,
                message="Issue 3",
                details={"file_path": "/path/file2.py"}
            )
        ]
        
        grouped = self.auto_fixer._group_issues_by_file(issues)
        
        self.assertEqual(len(grouped), 2)
        self.assertEqual(len(grouped["/path/file1.py"]), 2)
        self.assertEqual(len(grouped["/path/file2.py"]), 1)
    
    def test_can_fix_issue(self):
        """Test checking if an issue can be fixed"""
        fixable_issue = TestResult(
            component="test",
            test_name="indentation",
            status=TestStatus.FAIL,
            message="Indentation issue"
        )
        
        non_fixable_issue = TestResult(
            component="test",
            test_name="unknown_issue",
            status=TestStatus.FAIL,
            message="Unknown issue"
        )
        
        self.assertTrue(self.auto_fixer._can_fix_issue(fixable_issue))
        self.assertFalse(self.auto_fixer._can_fix_issue(non_fixable_issue))
    
    def test_create_backup(self):
        """Test creating file backup"""
        test_file = self._create_test_file("test.py", "print('hello')")
        
        backup_info = self.auto_fixer._create_backup(test_file)
        
        self.assertTrue(backup_info["success"])
        self.assertIn("backup_path", backup_info)
        
        # Verify backup file exists
        backup_path = backup_info["backup_path"]
        self.assertTrue(os.path.exists(backup_path))
        
        # Verify backup content
        with open(backup_path, 'r') as f:
            backup_content = f.read()
        self.assertEqual(backup_content, "print('hello')")
    
    def test_restore_from_backup(self):
        """Test restoring file from backup"""
        test_file = self._create_test_file("test.py", "original content")
        
        # Create backup
        backup_info = self.auto_fixer._create_backup(test_file)
        backup_path = backup_info["backup_path"]
        
        # Modify original file
        with open(test_file, 'w') as f:
            f.write("modified content")
        
        # Restore from backup
        success = self.auto_fixer._restore_from_backup(test_file, backup_path)
        
        self.assertTrue(success)
        
        # Verify restoration
        with open(test_file, 'r') as f:
            restored_content = f.read()
        self.assertEqual(restored_content, "original content")
    
    def test_fix_issues_with_auto_fix_disabled(self):
        """Test fix_issues when auto-fix is disabled"""
        config = TestConfiguration(auto_fix_enabled=False)
        auto_fixer = AutoFixer(config)
        
        issues = [TestResult(
            component="test",
            test_name="indentation",
            status=TestStatus.FAIL,
            message="Test issue"
        )]
        
        results = auto_fixer.fix_issues(issues)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, TestStatus.SKIPPED)
        self.assertIn("disabled", results[0].message)
    
    def test_get_fix_priority(self):
        """Test getting fix priority for issues"""
        critical_issue = TestResult(
            component="test",
            test_name="test",
            status=TestStatus.FAIL,
            message="Critical issue",
            severity=Severity.CRITICAL
        )
        
        low_issue = TestResult(
            component="test",
            test_name="test",
            status=TestStatus.FAIL,
            message="Low issue",
            severity=Severity.LOW
        )
        
        critical_priority = self.auto_fixer._get_fix_priority(critical_issue)
        low_priority = self.auto_fixer._get_fix_priority(low_issue)
        
        # Critical issues should have higher priority (lower number)
        self.assertLess(critical_priority, low_priority)
    
    def test_fix_history_recording(self):
        """Test recording fix session history"""
        issues = [TestResult(
            component="test",
            test_name="test",
            status=TestStatus.FAIL,
            message="Test issue"
        )]
        
        results = [TestResult(
            component="auto_fixer",
            test_name="fix",
            status=TestStatus.PASS,
            message="Fix applied",
            auto_fixed=True
        )]
        
        initial_history_length = len(self.auto_fixer.fix_history)
        
        self.auto_fixer._record_fix_session(issues, results)
        
        # Should add one record to history
        self.assertEqual(len(self.auto_fixer.fix_history), initial_history_length + 1)
        
        # Check record content
        latest_record = self.auto_fixer.fix_history[-1]
        self.assertEqual(latest_record["total_issues"], 1)
        self.assertEqual(latest_record["successful_fixes"], 1)


if __name__ == '__main__':
    unittest.main()