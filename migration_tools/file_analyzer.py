#!/usr/bin/env python3
"""
File Analyzer for AlgoProject
Analyzes the project structure and categorizes files for migration planning
"""

import os
from pathlib import Path
from collections import defaultdict, Counter
import json
from datetime import datetime

class FileAnalyzer:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.exclude_dirs = {'.git', 'venv', 'venv_fresh', '__pycache__'}
        
    def analyze_project_structure(self):
        """Analyze the entire project structure"""
        analysis = {
            'total_files': 0,
            'total_directories': 0,
            'file_types': defaultdict(int),
            'directory_structure': defaultdict(int),
            'large_files': [],  # Files > 1MB
            'python_files_by_directory': defaultdict(int),
            'potential_duplicates': defaultdict(list),
            'empty_directories': [],
            'analysis_date': datetime.now().isoformat()
        }
        
        print("Analyzing project structure...")
        
        for item in self.project_root.rglob("*"):
            # Skip excluded directories
            if any(excluded in item.parts for excluded in self.exclude_dirs):
                continue
                
            if item.is_file():
                analysis['total_files'] += 1
                
                # File extension analysis
                ext = item.suffix.lower() if item.suffix else 'no_extension'
                analysis['file_types'][ext] += 1
                
                # Python files by directory
                if ext == '.py':
                    parent_dir = str(item.parent.relative_to(self.project_root))
                    analysis['python_files_by_directory'][parent_dir] += 1
                
                # Large files
                file_size = item.stat().st_size
                if file_size > 1024 * 1024:  # > 1MB
                    analysis['large_files'].append({
                        'path': str(item.relative_to(self.project_root)),
                        'size_mb': round(file_size / (1024 * 1024), 2)
                    })
                
                # Potential duplicates by name
                analysis['potential_duplicates'][item.name].append(str(item.relative_to(self.project_root)))
                
            elif item.is_dir():
                analysis['total_directories'] += 1
                
                # Directory structure
                parent_dir = str(item.parent.relative_to(self.project_root)) if item.parent != self.project_root else 'root'
                analysis['directory_structure'][parent_dir] += 1
                
                # Empty directories
                try:
                    if not any(item.iterdir()):
                        analysis['empty_directories'].append(str(item.relative_to(self.project_root)))
                except PermissionError:
                    pass
        
        # Filter potential duplicates to only show actual duplicates
        analysis['potential_duplicates'] = {
            name: paths for name, paths in analysis['potential_duplicates'].items() 
            if len(paths) > 1
        }
        
        return analysis
    
    def identify_migration_candidates(self, analysis):
        """Identify files that should be migrated or removed"""
        candidates = {
            'backup_files': [],
            'test_files': [],
            'temp_files': [],
            'config_files': [],
            'documentation': [],
            'core_python_files': [],
            'utility_scripts': [],
            'generated_files': []
        }
        
        print("Identifying migration candidates...")
        
        for item in self.project_root.rglob("*"):
            if not item.is_file():
                continue
                
            # Skip excluded directories
            if any(excluded in item.parts for excluded in self.exclude_dirs):
                continue
            
            rel_path = str(item.relative_to(self.project_root))
            
            # Categorize files
            if 'backup' in rel_path.lower() or item.name.endswith('.bak'):
                candidates['backup_files'].append(rel_path)
            elif 'test' in rel_path.lower() and item.suffix == '.py':
                candidates['test_files'].append(rel_path)
            elif item.suffix in ['.tmp', '.temp', '.log', '.cache']:
                candidates['temp_files'].append(rel_path)
            elif item.suffix in ['.yaml', '.yml', '.json', '.ini', '.cfg', '.conf']:
                candidates['config_files'].append(rel_path)
            elif item.suffix in ['.md', '.txt', '.rst', '.doc', '.docx']:
                candidates['documentation'].append(rel_path)
            elif item.suffix == '.py':
                # Categorize Python files
                if any(keyword in rel_path.lower() for keyword in ['util', 'helper', 'tool', 'script']):
                    candidates['utility_scripts'].append(rel_path)
                elif 'algoproject' in rel_path.lower() or any(core_dir in rel_path for core_dir in ['core', 'strategies', 'data']):
                    candidates['core_python_files'].append(rel_path)
                else:
                    candidates['utility_scripts'].append(rel_path)
        
        return candidates
    
    def generate_report(self, analysis, candidates):
        """Generate comprehensive analysis report"""
        report = {
            'project_analysis': analysis,
            'migration_candidates': candidates,
            'recommendations': self.generate_recommendations(analysis, candidates)
        }
        
        # Save detailed report
        report_file = self.project_root / f"file_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Print summary
        self.print_summary(analysis, candidates)
        
        print(f"\nDetailed report saved to: {report_file}")
        return report_file
    
    def generate_recommendations(self, analysis, candidates):
        """Generate migration recommendations"""
        recommendations = []
        
        # File count recommendations
        total_py_files = analysis['file_types'].get('.py', 0)
        if total_py_files > 1000:
            recommendations.append(f"Consider consolidating Python files. Current count: {total_py_files}")
        
        # Backup file recommendations
        if len(candidates['backup_files']) > 10:
            recommendations.append(f"Remove {len(candidates['backup_files'])} backup files to clean up project")
        
        # Test file recommendations
        if len(candidates['test_files']) > 100:
            recommendations.append(f"Consolidate {len(candidates['test_files'])} test files into organized test suites")
        
        # Large file recommendations
        if len(analysis['large_files']) > 0:
            recommendations.append(f"Review {len(analysis['large_files'])} large files for optimization")
        
        # Duplicate recommendations
        duplicate_count = sum(len(paths) - 1 for paths in analysis['potential_duplicates'].values())
        if duplicate_count > 50:
            recommendations.append(f"Investigate {duplicate_count} potential duplicate files")
        
        return recommendations
    
    def print_summary(self, analysis, candidates):
        """Print analysis summary"""
        print(f"\n{'='*60}")
        print("PROJECT ANALYSIS SUMMARY")
        print(f"{'='*60}")
        
        print(f"Total Files: {analysis['total_files']:,}")
        print(f"Total Directories: {analysis['total_directories']:,}")
        
        print(f"\nTop File Types:")
        sorted_types = sorted(analysis['file_types'].items(), key=lambda x: x[1], reverse=True)
        for ext, count in sorted_types[:10]:
            print(f"  {ext}: {count:,}")
        
        print(f"\nPython Files by Directory:")
        sorted_py_dirs = sorted(analysis['python_files_by_directory'].items(), key=lambda x: x[1], reverse=True)
        for dir_name, count in sorted_py_dirs[:10]:
            print(f"  {dir_name}: {count}")
        
        print(f"\nMigration Candidates:")
        for category, files in candidates.items():
            if files:
                print(f"  {category.replace('_', ' ').title()}: {len(files)}")
        
        print(f"\nLarge Files (>1MB): {len(analysis['large_files'])}")
        for large_file in analysis['large_files'][:5]:
            print(f"  {large_file['path']}: {large_file['size_mb']} MB")
        
        print(f"\nPotential Duplicates: {len(analysis['potential_duplicates'])} sets")
        duplicate_count = sum(len(paths) - 1 for paths in analysis['potential_duplicates'].values())
        print(f"Total duplicate files: {duplicate_count}")

def main():
    analyzer = FileAnalyzer()
    
    # Run analysis
    analysis = analyzer.analyze_project_structure()
    candidates = analyzer.identify_migration_candidates(analysis)
    
    # Generate report
    report_file = analyzer.generate_report(analysis, candidates)
    
    print(f"\nAnalysis complete. Report saved to: {report_file}")

if __name__ == "__main__":
    main()