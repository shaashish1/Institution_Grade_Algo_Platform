#!/usr/bin/env python3
"""
File Cleanup Utility for AlgoProject
Identifies and removes unwanted files including zero-byte files, duplicates, and temporary files.
"""

import os
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import json
import argparse


class FileCleanupUtility:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / f"cleanup_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.stats = {
            'zero_byte_files': 0,
            'duplicate_files': 0,
            'temp_files': 0,
            'total_files_removed': 0,
            'space_saved': 0
        }
        
        # File patterns to consider for cleanup
        self.temp_patterns = [
            '*.tmp', '*.temp', '*~', '*.bak', '*.backup',
            '*.log', '*.cache', '__pycache__', '*.pyc', '*.pyo'
        ]
        
        # Directories to exclude from cleanup
        self.exclude_dirs = {
            '.git', '.kiro', 'venv', 'venv_fresh', '__pycache__',
            'node_modules', '.pytest_cache'
        }

    def create_backup_dir(self):
        """Create backup directory for deleted files"""
        self.backup_dir.mkdir(exist_ok=True)
        print(f"Created backup directory: {self.backup_dir}")

    def get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content"""
        if file_path.stat().st_size == 0:
            return "empty_file"
        
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except (IOError, OSError):
            return "error_reading_file"

    def find_zero_byte_files(self) -> list:
        """Find all zero-byte files in the project"""
        zero_byte_files = []
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file() and file_path.stat().st_size == 0:
                # Skip files in excluded directories
                if any(excluded in file_path.parts for excluded in self.exclude_dirs):
                    continue
                zero_byte_files.append(file_path)
        
        return zero_byte_files

    def find_duplicate_files(self) -> dict:
        """Find duplicate files based on content hash"""
        file_hashes = defaultdict(list)
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                # Skip files in excluded directories
                if any(excluded in file_path.parts for excluded in self.exclude_dirs):
                    continue
                
                # Skip very large files (>100MB) for performance
                if file_path.stat().st_size > 100 * 1024 * 1024:
                    continue
                
                file_hash = self.get_file_hash(file_path)
                file_hashes[file_hash].append(file_path)
        
        # Return only hashes with multiple files (duplicates)
        duplicates = {hash_val: files for hash_val, files in file_hashes.items() if len(files) > 1}
        return duplicates

    def find_temp_files(self) -> list:
        """Find temporary and cache files"""
        temp_files = []
        
        for pattern in self.temp_patterns:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    # Skip files in excluded directories (except __pycache__ which we want to clean)
                    if any(excluded in file_path.parts for excluded in self.exclude_dirs if excluded != '__pycache__'):
                        continue
                    temp_files.append(file_path)
        
        return temp_files

    def backup_file(self, file_path: Path):
        """Backup a file before deletion"""
        relative_path = file_path.relative_to(self.project_root)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(file_path, backup_path)
        except (IOError, OSError) as e:
            print(f"Warning: Could not backup {file_path}: {e}")

    def remove_zero_byte_files(self, zero_byte_files: list, backup: bool = True):
        """Remove zero-byte files"""
        print(f"\nRemoving {len(zero_byte_files)} zero-byte files...")
        
        for file_path in zero_byte_files:
            try:
                if backup:
                    self.backup_file(file_path)
                
                file_path.unlink()
                self.stats['zero_byte_files'] += 1
                print(f"Removed: {file_path}")
            except (IOError, OSError) as e:
                print(f"Error removing {file_path}: {e}")

    def remove_duplicate_files(self, duplicates: dict, backup: bool = True):
        """Remove duplicate files, keeping the first one"""
        print(f"\nProcessing {len(duplicates)} sets of duplicate files...")
        
        for file_hash, files in duplicates.items():
            if file_hash == "empty_file":  # Skip empty files, handled separately
                continue
            
            # Sort files to keep the one with the shortest path or most recent
            files.sort(key=lambda x: (len(str(x)), -x.stat().st_mtime))
            keep_file = files[0]
            remove_files = files[1:]
            
            print(f"\nKeeping: {keep_file}")
            for file_path in remove_files:
                try:
                    if backup:
                        self.backup_file(file_path)
                    
                    file_size = file_path.stat().st_size
                    file_path.unlink()
                    self.stats['duplicate_files'] += 1
                    self.stats['space_saved'] += file_size
                    print(f"Removed duplicate: {file_path}")
                except (IOError, OSError) as e:
                    print(f"Error removing {file_path}: {e}")

    def remove_temp_files(self, temp_files: list, backup: bool = True):
        """Remove temporary files"""
        print(f"\nRemoving {len(temp_files)} temporary files...")
        
        for file_path in temp_files:
            try:
                if backup and not file_path.name.endswith(('.pyc', '.pyo')):
                    self.backup_file(file_path)
                
                file_size = file_path.stat().st_size
                file_path.unlink()
                self.stats['temp_files'] += 1
                self.stats['space_saved'] += file_size
                print(f"Removed: {file_path}")
            except (IOError, OSError) as e:
                print(f"Error removing {file_path}: {e}")

    def generate_report(self):
        """Generate cleanup report"""
        self.stats['total_files_removed'] = (
            self.stats['zero_byte_files'] + 
            self.stats['duplicate_files'] + 
            self.stats['temp_files']
        )
        
        report = {
            'cleanup_date': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'backup_directory': str(self.backup_dir),
            'statistics': self.stats
        }
        
        report_file = self.project_root / f"cleanup_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{'='*50}")
        print("CLEANUP SUMMARY")
        print(f"{'='*50}")
        print(f"Zero-byte files removed: {self.stats['zero_byte_files']}")
        print(f"Duplicate files removed: {self.stats['duplicate_files']}")
        print(f"Temporary files removed: {self.stats['temp_files']}")
        print(f"Total files removed: {self.stats['total_files_removed']}")
        print(f"Space saved: {self.stats['space_saved'] / (1024*1024):.2f} MB")
        print(f"Backup directory: {self.backup_dir}")
        print(f"Report saved to: {report_file}")

    def run_cleanup(self, remove_zero_byte=True, remove_duplicates=True, remove_temp=True, backup=True):
        """Run the complete cleanup process"""
        print("Starting AlgoProject File Cleanup...")
        print(f"Project root: {self.project_root}")
        
        if backup:
            self.create_backup_dir()
        
        # Find files to clean
        zero_byte_files = self.find_zero_byte_files() if remove_zero_byte else []
        duplicates = self.find_duplicate_files() if remove_duplicates else {}
        temp_files = self.find_temp_files() if remove_temp else []
        
        print(f"\nFound:")
        print(f"- Zero-byte files: {len(zero_byte_files)}")
        print(f"- Duplicate file sets: {len(duplicates)}")
        print(f"- Temporary files: {len(temp_files)}")
        
        # Confirm before proceeding
        if zero_byte_files or duplicates or temp_files:
            response = input("\nProceed with cleanup? (y/N): ").lower().strip()
            if response != 'y':
                print("Cleanup cancelled.")
                return
        
        # Perform cleanup
        if remove_zero_byte and zero_byte_files:
            self.remove_zero_byte_files(zero_byte_files, backup)
        
        if remove_duplicates and duplicates:
            self.remove_duplicate_files(duplicates, backup)
        
        if remove_temp and temp_files:
            self.remove_temp_files(temp_files, backup)
        
        # Generate report
        self.generate_report()


def main():
    parser = argparse.ArgumentParser(description='AlgoProject File Cleanup Utility')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backup')
    parser.add_argument('--skip-zero-byte', action='store_true', help='Skip zero-byte file removal')
    parser.add_argument('--skip-duplicates', action='store_true', help='Skip duplicate file removal')
    parser.add_argument('--skip-temp', action='store_true', help='Skip temporary file removal')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be removed without actually removing')
    
    args = parser.parse_args()
    
    cleanup = FileCleanupUtility(args.project_root)
    
    if args.dry_run:
        print("DRY RUN MODE - No files will be removed")
        zero_byte_files = cleanup.find_zero_byte_files()
        duplicates = cleanup.find_duplicate_files()
        temp_files = cleanup.find_temp_files()
        
        print(f"\nWould remove:")
        print(f"- Zero-byte files: {len(zero_byte_files)}")
        print(f"- Duplicate file sets: {len(duplicates)}")
        print(f"- Temporary files: {len(temp_files)}")
        
        if zero_byte_files:
            print(f"\nFirst 10 zero-byte files:")
            for f in zero_byte_files[:10]:
                print(f"  {f}")
    else:
        cleanup.run_cleanup(
            remove_zero_byte=not args.skip_zero_byte,
            remove_duplicates=not args.skip_duplicates,
            remove_temp=not args.skip_temp,
            backup=not args.no_backup
        )


if __name__ == "__main__":
    main()