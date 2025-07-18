#!/usr/bin/env python3
"""
Simple cleanup utility to remove zero-byte files
"""

import os
from pathlib import Path
from datetime import datetime

def find_and_remove_zero_byte_files(project_root="."):
    """Find and remove zero-byte files"""
    project_path = Path(project_root)
    
    # Directories to exclude
    exclude_dirs = {'.git', '.kiro', 'venv', 'venv_fresh', '__pycache__'}
    
    zero_byte_files = []
    
    print("Scanning for zero-byte files...")
    
    for file_path in project_path.rglob("*"):
        if file_path.is_file() and file_path.stat().st_size == 0:
            # Skip files in excluded directories
            if any(excluded in file_path.parts for excluded in exclude_dirs):
                continue
            zero_byte_files.append(file_path)
    
    print(f"Found {len(zero_byte_files)} zero-byte files")
    
    if zero_byte_files:
        print("\nFirst 20 zero-byte files:")
        for i, file_path in enumerate(zero_byte_files[:20]):
            print(f"  {i+1}. {file_path}")
        
        if len(zero_byte_files) > 20:
            print(f"  ... and {len(zero_byte_files) - 20} more")
        
        response = input(f"\nRemove all {len(zero_byte_files)} zero-byte files? (y/N): ").strip().lower()
        
        if response == 'y':
            removed_count = 0
            for file_path in zero_byte_files:
                try:
                    file_path.unlink()
                    removed_count += 1
                    if removed_count % 50 == 0:
                        print(f"Removed {removed_count} files...")
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")
            
            print(f"\nSuccessfully removed {removed_count} zero-byte files")
        else:
            print("Cleanup cancelled")
    else:
        print("No zero-byte files found")

if __name__ == "__main__":
    find_and_remove_zero_byte_files()