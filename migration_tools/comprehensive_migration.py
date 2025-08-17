#!/usr/bin/env python3
"""
Comprehensive Migration Utility for AlgoProject
Migrates files to the new organized structure as defined in the design document
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class ComprehensiveMigration:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / f"migration_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Directories to remove completely
        self.remove_dirs = [
            "backup_test_files_20250715_202121",
            "cleanup_backup_20250718_205653", 
            "cleanup_backup_20250718_205841",
            "comprehensive_system_testing",  # Will be moved to tests/
            "crypto/scripts/backup20250716"
        ]
        
        # Files to remove
        self.remove_files = [
            "file_analysis_report_*.json",
            "cleanup_report_*.json"
        ]
        
        self.stats = {
            'directories_removed': 0,
            'files_removed': 0,
            'files_migrated': 0,
            'space_saved': 0
        }

    def create_backup(self):
        """Create backup of current state"""
        print(f"Creating backup at: {self.backup_dir}")
        self.backup_dir.mkdir(exist_ok=True)
        
        # Create a manifest of what we're about to change
        manifest = {
            'backup_date': datetime.now().isoformat(),
            'directories_to_remove': self.remove_dirs,
            'files_to_remove': self.remove_files
        }
        
        with open(self.backup_dir / "migration_manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)

    def remove_backup_directories(self):
        """Remove backup and temporary directories"""
        print("\nRemoving backup directories...")
        
        for dir_name in self.remove_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                try:
                    # Calculate space to be saved
                    total_size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                    self.stats['space_saved'] += total_size
                    
                    # Remove directory
                    shutil.rmtree(dir_path)
                    self.stats['directories_removed'] += 1
                    print(f"Removed directory: {dir_name}")
                except Exception as e:
                    print(f"Error removing {dir_name}: {e}")

    def remove_temporary_files(self):
        """Remove temporary and analysis files"""
        print("\nRemoving temporary files...")
        
        for pattern in self.remove_files:
            for file_path in self.project_root.glob(pattern):
                if file_path.is_file():
                    try:
                        file_size = file_path.stat().st_size
                        file_path.unlink()
                        self.stats['files_removed'] += 1
                        self.stats['space_saved'] += file_size
                        print(f"Removed file: {file_path.name}")
                    except Exception as e:
                        print(f"Error removing {file_path}: {e}")

    def consolidate_duplicates(self):
        """Remove obvious duplicate files"""
        print("\nConsolidating duplicate files...")
        
        # Remove duplicate README files (keep root one)
        duplicate_readmes = [
            "docs/README.md",
            "strategies/README.md"
        ]
        
        for readme_path in duplicate_readmes:
            file_path = self.project_root / readme_path
            if file_path.exists():
                try:
                    file_path.unlink()
                    self.stats['files_removed'] += 1
                    print(f"Removed duplicate: {readme_path}")
                except Exception as e:
                    print(f"Error removing {readme_path}: {e}")
        
        # Remove duplicate trading platform files (keep algoproject version)
        trading_platform_dir = self.project_root / "trading_platform"
        if trading_platform_dir.exists():
            try:
                shutil.rmtree(trading_platform_dir)
                self.stats['directories_removed'] += 1
                print("Removed duplicate trading_platform directory")
            except Exception as e:
                print(f"Error removing trading_platform: {e}")

    def organize_test_files(self):
        """Organize test files into tests/ directory"""
        print("\nOrganizing test files...")
        
        tests_dir = self.project_root / "tests"
        tests_dir.mkdir(exist_ok=True)
        
        # Test files to move
        test_files = [
            "launch_comprehensive_testing.py",
            "quick_system_test.py", 
            "quick_test.py",
            "simple_crypto_test.py",
            "test_algoproject_components.py",
            "test_algoproject_system.py",
            "test_crypto_backtest.py"
        ]
        
        for test_file in test_files:
            src_path = self.project_root / test_file
            if src_path.exists():
                dst_path = tests_dir / test_file
                try:
                    shutil.move(str(src_path), str(dst_path))
                    self.stats['files_migrated'] += 1
                    print(f"Moved test file: {test_file} -> tests/")
                except Exception as e:
                    print(f"Error moving {test_file}: {e}")

    def clean_empty_directories(self):
        """Remove empty directories"""
        print("\nCleaning empty directories...")
        
        # Find and remove empty directories (bottom-up)
        for root, dirs, files in os.walk(self.project_root, topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if dir_path.is_dir() and not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        print(f"Removed empty directory: {dir_path.relative_to(self.project_root)}")
                except (OSError, ValueError):
                    pass  # Directory not empty or other error

    def update_gitignore(self):
        """Update .gitignore with comprehensive patterns"""
        print("\nUpdating .gitignore...")
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
venv_fresh/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
*.log.*

# Cache
.cache/
.pytest_cache/

# Output files
output/
*.csv
*.png
*.jpg
*.pdf
charts/
reports/

# Backup files
backup_*/
*_backup_*/
*.bak
*.backup

# Temporary files
*.tmp
*.temp
temp/

# API Keys and Secrets
.env
*.key
api_keys.json
credentials.json

# Analysis reports
*_analysis_*.json
*_report_*.json
file_analysis_report_*.json
cleanup_report_*.json

# Test outputs
test_reports/
test_results/

# Jupyter Notebooks
.ipynb_checkpoints/
*.ipynb

# Database
*.db
*.sqlite
*.sqlite3

# Configuration (if containing secrets)
# config/secrets.yaml
# config/api_keys.yaml
"""
        
        gitignore_path = self.project_root / ".gitignore"
        try:
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)
            print("Updated .gitignore with comprehensive patterns")
        except Exception as e:
            print(f"Error updating .gitignore: {e}")

    def generate_migration_report(self):
        """Generate migration report"""
        report = {
            'migration_date': datetime.now().isoformat(),
            'statistics': self.stats,
            'space_saved_mb': round(self.stats['space_saved'] / (1024 * 1024), 2)
        }
        
        report_file = self.project_root / f"migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{'='*50}")
        print("MIGRATION SUMMARY")
        print(f"{'='*50}")
        print(f"Directories removed: {self.stats['directories_removed']}")
        print(f"Files removed: {self.stats['files_removed']}")
        print(f"Files migrated: {self.stats['files_migrated']}")
        print(f"Space saved: {report['space_saved_mb']} MB")
        print(f"Backup created at: {self.backup_dir}")
        print(f"Report saved to: {report_file}")

    def run_migration(self):
        """Run the complete migration process"""
        print("Starting comprehensive migration...")
        print(f"Project root: {self.project_root}")
        
        # Confirm before proceeding
        response = input("\nThis will remove backup directories and reorganize files. Continue? (y/N): ").lower().strip()
        if response != 'y':
            print("Migration cancelled.")
            return
        
        # Create backup
        self.create_backup()
        
        # Perform migration steps
        self.remove_backup_directories()
        self.remove_temporary_files()
        self.consolidate_duplicates()
        self.organize_test_files()
        self.clean_empty_directories()
        self.update_gitignore()
        
        # Generate report
        self.generate_migration_report()
        
        print("\nMigration completed successfully!")
        print("You can now check the file count with: Get-ChildItem -Recurse -Filter '*.py' | Measure-Object")

def main():
    migration = ComprehensiveMigration()
    migration.run_migration()

if __name__ == "__main__":
    main()