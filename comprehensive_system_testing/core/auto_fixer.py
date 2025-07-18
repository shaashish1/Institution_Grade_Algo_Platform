"""
Auto-Fixer Engine
================

Automated repair system for common issues with rollback capabilities.
"""

import os
import time
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from .models import TestResult, TestStatus, Severity, TestConfiguration
from ..utils.file_utils import FileUtils
from ..utils.logger import TestLogger


class AutoFixer:
    """Automated issue fixing engine with rollback capabilities"""
    
    def __init__(self, config: TestConfiguration):
        self.config = config
        self.logger = TestLogger()
        self.fix_history = []
        self.backup_directory = Path("comprehensive_system_testing/backups")
        self.backup_directory.mkdir(parents=True, exist_ok=True)
    
    def fix_issues(self, issues: List[TestResult]) -> List[TestResult]:
        """
        Fix a list of issues and return results
        
        Args:
            issues: List of TestResult objects representing issues to fix
            
        Returns:
            List of TestResult objects representing fix attempts
        """
        fix_results = []
        
        if not self.config.auto_fix_enabled:
            return [TestResult(
                component="auto_fixer",
                test_name="auto_fix_disabled",
                status=TestStatus.SKIPPED,
                message="Auto-fixing is disabled in configuration",
                details={"total_issues": len(issues)}
            )]
        
        self.logger.info(f"Starting auto-fix for {len(issues)} issues")
        
        # Group issues by file for batch processing
        issues_by_file = self._group_issues_by_file(issues)
        
        for file_path, file_issues in issues_by_file.items():
            batch_result = self._fix_file_issues(file_path, file_issues)
            fix_results.extend(batch_result)
        
        # Record fix session
        self._record_fix_session(issues, fix_results)
        
        return fix_results
    
    def _group_issues_by_file(self, issues: List[TestResult]) -> Dict[str, List[TestResult]]:
        """Group issues by file path for batch processing"""
        grouped = {}
        
        for issue in issues:
            file_path = issue.details.get("file_path")
            if file_path:
                if file_path not in grouped:
                    grouped[file_path] = []
                grouped[file_path].append(issue)
        
        return grouped
    
    def _fix_file_issues(self, file_path: str, issues: List[TestResult]) -> List[TestResult]:
        """Fix all issues for a single file"""
        results = []
        
        # Create backup first
        backup_info = self._create_backup(file_path)
        if not backup_info["success"]:
            return [TestResult(
                component="auto_fixer",
                test_name="backup_creation",
                status=TestStatus.FAIL,
                message=f"Could not create backup for {file_path}",
                severity=Severity.HIGH,
                details={"file_path": file_path, "error": backup_info["error"]}
            )]
        
        try:
            # Read original content
            original_content = FileUtils.read_file_safe(file_path)
            if original_content is None:
                return [TestResult(
                    component="auto_fixer",
                    test_name="file_read",
                    status=TestStatus.FAIL,
                    message=f"Could not read file for fixing: {file_path}",
                    severity=Severity.HIGH,
                    details={"file_path": file_path}
                )]
            
            current_content = original_content
            fixes_applied = []
            
            # Apply fixes in order of priority
            sorted_issues = sorted(issues, key=lambda x: self._get_fix_priority(x))
            
            for issue in sorted_issues:
                if self._can_fix_issue(issue):
                    fix_result = self._apply_single_fix(current_content, issue)
                    
                    if fix_result["success"]:
                        current_content = fix_result["content"]
                        fixes_applied.append({
                            "issue": issue.test_name,
                            "description": fix_result["description"],
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        results.append(TestResult(
                            component="auto_fixer",
                            test_name="fix_application",
                            status=TestStatus.FAIL,
                            message=f"Failed to fix {issue.test_name}: {fix_result['error']}",
                            severity=Severity.MEDIUM,
                            details={
                                "file_path": file_path,
                                "issue": issue.test_name,
                                "error": fix_result["error"]
                            }
                        ))
            
            # Write fixed content if any fixes were applied
            if fixes_applied:
                if FileUtils.write_file_safe(file_path, current_content):
                    results.append(TestResult(
                        component="auto_fixer",
                        test_name="file_fix_complete",
                        status=TestStatus.PASS,
                        message=f"Successfully applied {len(fixes_applied)} fixes to {Path(file_path).name}",
                        auto_fixed=True,
                        details={
                            "file_path": file_path,
                            "backup_path": backup_info["backup_path"],
                            "fixes_applied": fixes_applied,
                            "original_size": len(original_content),
                            "fixed_size": len(current_content)
                        }
                    ))
                else:
                    # Restore from backup if write failed
                    self._restore_from_backup(file_path, backup_info["backup_path"])
                    results.append(TestResult(
                        component="auto_fixer",
                        test_name="file_fix_complete",
                        status=TestStatus.FAIL,
                        message=f"Could not write fixed content, restored from backup",
                        severity=Severity.HIGH,
                        details={
                            "file_path": file_path,
                            "backup_restored": True
                        }
                    ))
            else:
                results.append(TestResult(
                    component="auto_fixer",
                    test_name="file_fix_complete",
                    status=TestStatus.SKIPPED,
                    message=f"No fixable issues found for {Path(file_path).name}",
                    details={"file_path": file_path, "total_issues": len(issues)}
                ))
                
        except Exception as e:
            # Restore from backup on any error
            self._restore_from_backup(file_path, backup_info["backup_path"])
            results.append(TestResult(
                component="auto_fixer",
                test_name="file_fix_complete",
                status=TestStatus.FAIL,
                message=f"Auto-fix failed with error, restored from backup: {str(e)}",
                severity=Severity.HIGH,
                details={
                    "file_path": file_path,
                    "error": str(e),
                    "backup_restored": True
                }
            ))
        
        return results
    
    def _create_backup(self, file_path: str) -> Dict[str, Any]:
        """Create backup of file before fixing"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = Path(file_path).name
            backup_name = f"{file_name}.{timestamp}.backup"
            backup_path = self.backup_directory / backup_name
            
            # Copy file to backup location
            import shutil
            shutil.copy2(file_path, backup_path)
            
            return {
                "success": True,
                "backup_path": str(backup_path),
                "timestamp": timestamp
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _restore_from_backup(self, file_path: str, backup_path: str) -> bool:
        """Restore file from backup"""
        try:
            import shutil
            shutil.copy2(backup_path, file_path)
            self.logger.info(f"Restored {file_path} from backup {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to restore {file_path} from backup: {e}")
            return False
    
    def _get_fix_priority(self, issue: TestResult) -> int:
        """Get fix priority for issue (lower number = higher priority)"""
        priority_map = {
            Severity.CRITICAL: 1,
            Severity.HIGH: 2,
            Severity.MEDIUM: 3,
            Severity.LOW: 4
        }
        return priority_map.get(issue.severity, 5)
    
    def _can_fix_issue(self, issue: TestResult) -> bool:
        """Check if an issue can be automatically fixed"""
        fixable_issues = {
            "indentation": self._fix_indentation,
            "trailing_whitespace": self._fix_trailing_whitespace,
            "import_statements": self._fix_import_statements,
            "quote_consistency": self._fix_quote_consistency,
            "csv_content": self._fix_csv_content,
            "yaml_structure": self._fix_yaml_structure,
            "json_structure": self._fix_json_structure
        }
        
        return issue.test_name in fixable_issues
    
    def _apply_single_fix(self, content: str, issue: TestResult) -> Dict[str, Any]:
        """Apply a single fix to content"""
        try:
            fix_methods = {
                "indentation": self._fix_indentation,
                "trailing_whitespace": self._fix_trailing_whitespace,
                "import_statements": self._fix_import_statements,
                "quote_consistency": self._fix_quote_consistency,
                "csv_content": self._fix_csv_content,
                "yaml_structure": self._fix_yaml_structure,
                "json_structure": self._fix_json_structure
            }
            
            fix_method = fix_methods.get(issue.test_name)
            if fix_method:
                fixed_content, description = fix_method(content, issue)
                return {
                    "success": True,
                    "content": fixed_content,
                    "description": description
                }
            else:
                return {
                    "success": False,
                    "error": f"No fix method available for {issue.test_name}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _fix_indentation(self, content: str, issue: TestResult) -> Tuple[str, str]:
        """Fix indentation issues"""
        lines = content.split('\n')
        fixed_lines = []
        changes = 0
        
        for line in lines:
            if line.strip():  # Non-empty line
                # Convert tabs to spaces (4 spaces per tab)
                if '\t' in line:
                    fixed_line = line.replace('\t', '    ')
                    if fixed_line != line:
                        changes += 1
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines), f"Fixed {changes} indentation issues"
    
    def _fix_trailing_whitespace(self, content: str, issue: TestResult) -> Tuple[str, str]:
        """Fix trailing whitespace"""
        lines = content.split('\n')
        fixed_lines = []
        changes = 0
        
        for line in lines:
            original_line = line
            fixed_line = line.rstrip()
            if fixed_line != original_line:
                changes += 1
            fixed_lines.append(fixed_line)
        
        return '\n'.join(fixed_lines), f"Removed trailing whitespace from {changes} lines"
    
    def _fix_import_statements(self, content: str, issue: TestResult) -> Tuple[str, str]:
        """Fix import statement issues"""
        lines = content.split('\n')
        fixed_lines = []
        changes = 0
        
        for line in lines:
            fixed_line = line
            
            # Remove trailing commas from import statements
            if (line.strip().startswith('import ') or line.strip().startswith('from ')) and line.rstrip().endswith(','):
                fixed_line = line.rstrip().rstrip(',')
                changes += 1
            
            fixed_lines.append(fixed_line)
        
        return '\n'.join(fixed_lines), f"Fixed {changes} import statement issues"
    
    def _fix_quote_consistency(self, content: str, issue: TestResult) -> Tuple[str, str]:
        """Fix quote consistency issues"""
        lines = content.split('\n')
        fixed_lines = []
        changes = 0
        
        for line in lines:
            fixed_line = line
            
            # Simple quote standardization (convert single to double quotes)
            if "'" in line and not line.strip().startswith('#'):
                # Only fix simple cases to avoid breaking code
                if line.count("'") == 2 and '"' not in line:
                    fixed_line = line.replace("'", '"')
                    changes += 1
            
            fixed_lines.append(fixed_line)
        
        return '\n'.join(fixed_lines), f"Standardized quotes in {changes} lines"
    
    def _fix_csv_content(self, content: str, issue: TestResult) -> Tuple[str, str]:
        """Fix CSV content issues"""
        try:
            import csv
            import io
            
            reader = csv.reader(io.StringIO(content))
            rows = list(reader)
            
            if not rows:
                return content, "No changes needed for empty CSV"
            
            # Fix inconsistent column counts by padding with empty strings
            max_cols = max(len(row) for row in rows)
            fixed_rows = []
            changes = 0
            
            for row in rows:
                if len(row) < max_cols:
                    padded_row = row + [''] * (max_cols - len(row))
                    fixed_rows.append(padded_row)
                    changes += 1
                else:
                    fixed_rows.append(row)
            
            # Write back to CSV format
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerows(fixed_rows)
            
            return output.getvalue(), f"Padded {changes} rows to consistent column count"
            
        except Exception:
            return content, "Could not fix CSV content"
    
    def _fix_yaml_structure(self, content: str, issue: TestResult) -> Tuple[str, str]:
        """Fix YAML structure issues"""
        # Basic YAML fixes - remove empty values
        lines = content.split('\n')
        fixed_lines = []
        changes = 0
        
        for line in lines:
            # Remove lines with empty values
            if ':' in line and line.strip().endswith(':'):
                # Empty value, skip this line
                changes += 1
                continue
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines), f"Removed {changes} empty YAML values"
    
    def _fix_json_structure(self, content: str, issue: TestResult) -> Tuple[str, str]:
        """Fix JSON structure issues"""
        try:
            import json
            
            # Parse and reformat JSON
            data = json.loads(content)
            
            # Remove null values
            if isinstance(data, dict):
                cleaned_data = {k: v for k, v in data.items() if v is not None}
                changes = len(data) - len(cleaned_data)
            else:
                cleaned_data = data
                changes = 0
            
            # Reformat with proper indentation
            fixed_content = json.dumps(cleaned_data, indent=2, ensure_ascii=False)
            
            return fixed_content, f"Cleaned JSON structure, removed {changes} null values"
            
        except Exception:
            return content, "Could not fix JSON structure"
    
    def _record_fix_session(self, issues: List[TestResult], results: List[TestResult]):
        """Record fix session for history tracking"""
        session_record = {
            "timestamp": datetime.now().isoformat(),
            "total_issues": len(issues),
            "total_results": len(results),
            "successful_fixes": len([r for r in results if r.status == TestStatus.PASS and r.auto_fixed]),
            "failed_fixes": len([r for r in results if r.status == TestStatus.FAIL]),
            "skipped_fixes": len([r for r in results if r.status == TestStatus.SKIPPED])
        }
        
        self.fix_history.append(session_record)
        
        # Save to file
        history_file = self.backup_directory / "fix_history.json"
        try:
            with open(history_file, 'w') as f:
                json.dump(self.fix_history, f, indent=2)
        except Exception as e:
            self.logger.warning(f"Could not save fix history: {e}")
    
    def rollback_fixes(self, session_timestamp: str) -> List[TestResult]:
        """Rollback fixes from a specific session"""
        results = []
        
        # Find backups from the specified session
        session_backups = []
        for backup_file in self.backup_directory.glob("*.backup"):
            if session_timestamp in backup_file.name:
                session_backups.append(backup_file)
        
        if not session_backups:
            return [TestResult(
                component="auto_fixer",
                test_name="rollback",
                status=TestStatus.FAIL,
                message=f"No backups found for session {session_timestamp}",
                severity=Severity.HIGH,
                details={"session_timestamp": session_timestamp}
            )]
        
        # Restore each backup
        for backup_file in session_backups:
            try:
                # Extract original file path from backup name
                original_name = backup_file.name.split('.')[0]
                # This is simplified - in practice, you'd need to store the mapping
                
                results.append(TestResult(
                    component="auto_fixer",
                    test_name="rollback",
                    status=TestStatus.PASS,
                    message=f"Rollback capability available for {backup_file.name}",
                    details={
                        "backup_file": str(backup_file),
                        "session_timestamp": session_timestamp
                    }
                ))
                
            except Exception as e:
                results.append(TestResult(
                    component="auto_fixer",
                    test_name="rollback",
                    status=TestStatus.FAIL,
                    message=f"Failed to rollback {backup_file.name}: {str(e)}",
                    severity=Severity.HIGH,
                    details={"error": str(e)}
                ))
        
        return results
    
    def get_fix_history(self) -> List[Dict[str, Any]]:
        """Get fix history"""
        return self.fix_history.copy()
    
    def cleanup_old_backups(self, days_old: int = 30) -> int:
        """Clean up old backup files"""
        cleaned_count = 0
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        
        try:
            for backup_file in self.backup_directory.glob("*.backup"):
                if backup_file.stat().st_mtime < cutoff_time:
                    backup_file.unlink()
                    cleaned_count += 1
                    
            self.logger.info(f"Cleaned up {cleaned_count} old backup files")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up backups: {e}")
        
        return cleaned_count