"""
File Utility Functions
======================

Utility functions for file operations in the testing framework.
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import yaml


class FileUtils:
    """Utility class for file operations"""
    
    @staticmethod
    def find_python_files(root_path: str) -> List[str]:
        """Find all Python files in a directory tree, excluding common ignore patterns"""
        python_files = []
        root = Path(root_path)
        
        # Directories to exclude from scanning
        exclude_dirs = {
            'venv', 'venv_fresh', '__pycache__', '.git', 'node_modules', 
            '.pytest_cache', '.tox', 'build', 'dist', '.eggs',
            'backup_test_files_20250715_202121'  # Specific backup directory
        }
        
        for file_path in root.rglob("*.py"):
            # Check if any parent directory is in exclude list
            if any(part in exclude_dirs for part in file_path.parts):
                continue
            python_files.append(str(file_path))
            
        return python_files
    
    @staticmethod
    def read_file_safe(file_path: str) -> Optional[str]:
        """Safely read a file, returning None if it fails"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None
    
    @staticmethod
    def write_file_safe(file_path: str, content: str) -> bool:
        """Safely write to a file, returning success status"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False
    
    @staticmethod
    def backup_file(file_path: str) -> Optional[str]:
        """Create a backup of a file, return backup path"""
        try:
            backup_path = f"{file_path}.backup"
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception:
            return None
    
    @staticmethod
    def restore_file(file_path: str, backup_path: str) -> bool:
        """Restore a file from backup"""
        try:
            shutil.copy2(backup_path, file_path)
            return True
        except Exception:
            return False
    
    @staticmethod
    def load_json_safe(file_path: str) -> Optional[Dict[str, Any]]:
        """Safely load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    @staticmethod
    def load_yaml_safe(file_path: str) -> Optional[Dict[str, Any]]:
        """Safely load YAML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception:
            return None
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """Get file information"""
        try:
            stat = os.stat(file_path)
            return {
                'exists': True,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'readable': os.access(file_path, os.R_OK),
                'writable': os.access(file_path, os.W_OK)
            }
        except Exception:
            return {'exists': False}