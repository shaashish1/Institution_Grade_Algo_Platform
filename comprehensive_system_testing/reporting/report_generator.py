"""
Report Generator
===============

Generates comprehensive test reports in multiple formats.
"""

import json
import csv
import io
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import base64

from ..core.models import TestResult, SystemHealth, TestStatus, Severity
from ..utils.logger import TestLogger


class ReportGenerator:
    """Generates test reports in multiple formats"""
    
    def __init__(self, output_directory: str = "test_reports"):
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True, exist_ok=True)
        self.logger = TestLogger()
    
    def generate_html_report(self, results: List[TestResult], system_health: Optional[SystemHealth] = None) -> str:
        """Generate interactive HTML report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_directory / f"test_report_{timestamp}.html"
        
        # Generate HTML content
        html_content = self._create_html_content(results, system_health)
        
        # Write to file
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.info(f"HTML report generated: {report_file}")
        return str(report_file)
    
    def generate_console_summary(self, results: List[TestResult], system_health: Optional[SystemHealth] = None) -> str:
        """Generate console-friendly summary"""
        summary = []
        
        # Header
        summary.append("=" * 80)
        summary.append("🔍 COMPREHENSIVE SYSTEM TEST REPORT")
        summary.append("=" * 80)
        summary.append(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append("")
        
        # System Health Overview
        if system_health:
            summary.append("🏥 SYSTEM HEALTH OVERVIEW")
            summary.append("-" * 40)
            summary.append(f"Overall Score: {system_health.overall_score:.1f}/100")
            summary.append(f"Critical Issues: {len(system_health.critical_issues)}")
            summary.append(f"Warnings: {len(system_health.warnings)}")
            summary.append(f"Trend: {system_health.trend.value}")
            summary.append("")
        
        # Test Results Summary
        summary.append("📊 TEST RESULTS SUMMARY")
        summary.append("-" * 40)
        
        # Count results by status
        status_counts = {}
        for result in results:
            status = result.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        total_tests = len(results)
        passed = status_counts.get(TestStatus.PASS, 0)
        failed = status_counts.get(TestStatus.FAIL, 0)
        warnings = status_counts.get(TestStatus.WARNING, 0)
        skipped = status_counts.get(TestStatus.SKIPPED, 0)
        
        summary.append(f"Total Tests: {total_tests}")
        summary.append(f"✅ Passed: {passed} ({passed/total_tests*100:.1f}%)")
        summary.append(f"❌ Failed: {failed} ({failed/total_tests*100:.1f}%)")
        summary.append(f"⚠️  Warnings: {warnings} ({warnings/total_tests*100:.1f}%)")
        summary.append(f"⏭️  Skipped: {skipped} ({skipped/total_tests*100:.1f}%)")
        summary.append("")
        
        # Component Breakdown
        summary.append("🔧 COMPONENT BREAKDOWN")
        summary.append("-" * 40)
        
        component_stats = {}
        for result in results:
            component = result.component
            if component not in component_stats:
                component_stats[component] = {"pass": 0, "fail": 0, "warning": 0, "skip": 0}
            
            if result.status == TestStatus.PASS:
                component_stats[component]["pass"] += 1
            elif result.status == TestStatus.FAIL:
                component_stats[component]["fail"] += 1
            elif result.status == TestStatus.WARNING:
                component_stats[component]["warning"] += 1
            else:
                component_stats[component]["skip"] += 1
        
        for component, stats in component_stats.items():
            total = sum(stats.values())
            pass_rate = stats["pass"] / total * 100 if total > 0 else 0
            summary.append(f"{component}: {stats['pass']}/{total} passed ({pass_rate:.1f}%)")
        
        summary.append("")
        
        # Critical Issues
        critical_issues = [r for r in results if r.severity == Severity.CRITICAL and r.status == TestStatus.FAIL]
        if critical_issues:
            summary.append("🚨 CRITICAL ISSUES")
            summary.append("-" * 40)
            for issue in critical_issues[:5]:  # Show top 5
                summary.append(f"• {issue.component}: {issue.message}")
            if len(critical_issues) > 5:
                summary.append(f"... and {len(critical_issues) - 5} more critical issues")
            summary.append("")
        
        # Auto-fixes Applied
        auto_fixed = [r for r in results if r.auto_fixed]
        if auto_fixed:
            summary.append("🔧 AUTO-FIXES APPLIED")
            summary.append("-" * 40)
            summary.append(f"Total fixes applied: {len(auto_fixed)}")
            for fix in auto_fixed[:3]:  # Show top 3
                summary.append(f"• {fix.component}: {fix.message}")
            if len(auto_fixed) > 3:
                summary.append(f"... and {len(auto_fixed) - 3} more fixes")
            summary.append("")
        
        # Recommendations
        summary.append("💡 RECOMMENDATIONS")
        summary.append("-" * 40)
        
        if failed > 0:
            summary.append("• Address failed tests before deployment")
        if critical_issues:
            summary.append("• Fix critical issues immediately")
        if warnings > total_tests * 0.2:
            summary.append("• Review and address warnings to improve code quality")
        if passed / total_tests > 0.9:
            summary.append("• Excellent test results! System is in good health")
        
        summary.append("")
        summary.append("=" * 80)
        
        console_output = "\n".join(summary)
        
        # Also save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = self.output_directory / f"test_summary_{timestamp}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(console_output)
        
        return console_output
    
    def export_json(self, results: List[TestResult], system_health: Optional[SystemHealth] = None) -> str:
        """Export results to JSON format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = self.output_directory / f"test_results_{timestamp}.json"
        
        export_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_tests": len(results),
                "generator": "comprehensive_system_testing"
            },
            "system_health": system_health.to_dict() if system_health else None,
            "test_results": [result.to_dict() for result in results]
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"JSON report exported: {json_file}")
        return str(json_file)
    
    def export_csv(self, results: List[TestResult]) -> str:
        """Export results to CSV format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = self.output_directory / f"test_results_{timestamp}.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Component', 'Test Name', 'Status', 'Severity', 'Message',
                'Timestamp', 'Execution Time', 'Auto Fixed', 'Details'
            ])
            
            # Data rows
            for result in results:
                writer.writerow([
                    result.component,
                    result.test_name,
                    result.status.value,
                    result.severity.value,
                    result.message,
                    result.timestamp.isoformat(),
                    result.execution_time,
                    result.auto_fixed,
                    json.dumps(result.details) if result.details else ""
                ])
        
        self.logger.info(f"CSV report exported: {csv_file}")
        return str(csv_file)
    
    def _create_html_content(self, results: List[TestResult], system_health: Optional[SystemHealth] = None) -> str:
        """Create HTML report content"""
        # Calculate statistics
        total_tests = len(results)
        passed = len([r for r in results if r.status == TestStatus.PASS])
        failed = len([r for r in results if r.status == TestStatus.FAIL])
        warnings = len([r for r in results if r.status == TestStatus.WARNING])
        skipped = len([r for r in results if r.status == TestStatus.SKIPPED])
        
        # Component statistics
        component_stats = {}
        for result in results:
            component = result.component
            if component not in component_stats:
                component_stats[component] = {"pass": 0, "fail": 0, "warning": 0, "skip": 0}
            
            if result.status == TestStatus.PASS:
                component_stats[component]["pass"] += 1
            elif result.status == TestStatus.FAIL:
                component_stats[component]["fail"] += 1
            elif result.status == TestStatus.WARNING:
                component_stats[component]["warning"] += 1
            else:
                component_stats[component]["skip"] += 1
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive System Test Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
        .pass {{ color: #28a745; }}
        .fail {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        .skip {{ color: #6c757d; }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section h2 {{
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .component-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .component-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            background: #fafafa;
        }}
        .component-name {{
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 10px;
            color: #333;
        }}
        .component-stats {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9em;
        }}
        .test-results {{
            margin-top: 30px;
        }}
        .test-item {{
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 10px;
            overflow: hidden;
        }}
        .test-header {{
            padding: 15px;
            background: #f8f9fa;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .test-header:hover {{
            background: #e9ecef;
        }}
        .test-details {{
            padding: 15px;
            background: white;
            border-top: 1px solid #ddd;
            display: none;
        }}
        .status-badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .status-pass {{
            background: #d4edda;
            color: #155724;
        }}
        .status-fail {{
            background: #f8d7da;
            color: #721c24;
        }}
        .status-warning {{
            background: #fff3cd;
            color: #856404;
        }}
        .status-skip {{
            background: #e2e3e5;
            color: #383d41;
        }}
        .auto-fixed {{
            background: #d1ecf1;
            color: #0c5460;
            margin-left: 10px;
        }}
        .filter-buttons {{
            margin-bottom: 20px;
        }}
        .filter-btn {{
            padding: 8px 16px;
            margin-right: 10px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 4px;
            cursor: pointer;
        }}
        .filter-btn.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 10px;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            transition: width 0.3s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Comprehensive System Test Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_tests}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number pass">{passed}</div>
                <div class="stat-label">Passed</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {passed/total_tests*100 if total_tests > 0 else 0:.1f}%"></div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-number fail">{failed}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number warning">{warnings}</div>
                <div class="stat-label">Warnings</div>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📊 Component Overview</h2>
                <div class="component-grid">
"""
        
        # Add component cards
        for component, stats in component_stats.items():
            total = sum(stats.values())
            pass_rate = stats["pass"] / total * 100 if total > 0 else 0
            
            html_content += f"""
                    <div class="component-card">
                        <div class="component-name">{component}</div>
                        <div class="component-stats">
                            <span class="pass">✅ {stats["pass"]}</span>
                            <span class="fail">❌ {stats["fail"]}</span>
                            <span class="warning">⚠️ {stats["warning"]}</span>
                            <span class="skip">⏭️ {stats["skip"]}</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {pass_rate:.1f}%"></div>
                        </div>
                    </div>
"""
        
        html_content += """
                </div>
            </div>
            
            <div class="section">
                <h2>🔍 Test Results</h2>
                <div class="filter-buttons">
                    <button class="filter-btn active" onclick="filterTests('all')">All</button>
                    <button class="filter-btn" onclick="filterTests('fail')">Failed</button>
                    <button class="filter-btn" onclick="filterTests('warning')">Warnings</button>
                    <button class="filter-btn" onclick="filterTests('pass')">Passed</button>
                </div>
                <div class="test-results">
"""
        
        # Add test results
        for result in results:
            status_class = f"status-{result.status.value.lower()}"
            auto_fixed_badge = '<span class="status-badge auto-fixed">AUTO-FIXED</span>' if result.auto_fixed else ''
            
            html_content += f"""
                    <div class="test-item" data-status="{result.status.value.lower()}">
                        <div class="test-header" onclick="toggleDetails(this)">
                            <div>
                                <strong>{result.component}</strong> - {result.test_name}
                                <br><small>{result.message}</small>
                            </div>
                            <div>
                                <span class="status-badge {status_class}">{result.status.value}</span>
                                {auto_fixed_badge}
                            </div>
                        </div>
                        <div class="test-details">
                            <p><strong>Severity:</strong> {result.severity.value}</p>
                            <p><strong>Timestamp:</strong> {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
                            <p><strong>Execution Time:</strong> {result.execution_time:.3f}s</p>
                            {f'<p><strong>Details:</strong></p><pre>{json.dumps(result.details, indent=2)}</pre>' if result.details else ''}
                        </div>
                    </div>
"""
        
        html_content += """
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function toggleDetails(header) {
            const details = header.nextElementSibling;
            details.style.display = details.style.display === 'block' ? 'none' : 'block';
        }
        
        function filterTests(status) {
            const items = document.querySelectorAll('.test-item');
            const buttons = document.querySelectorAll('.filter-btn');
            
            // Update button states
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Filter items
            items.forEach(item => {
                if (status === 'all' || item.dataset.status === status) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""
        
        return html_content
    
    def create_test_history(self, results: List[TestResult]) -> Dict[str, Any]:
        """Create test history record"""
        history_record = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(results),
            "passed": len([r for r in results if r.status == TestStatus.PASS]),
            "failed": len([r for r in results if r.status == TestStatus.FAIL]),
            "warnings": len([r for r in results if r.status == TestStatus.WARNING]),
            "skipped": len([r for r in results if r.status == TestStatus.SKIPPED]),
            "auto_fixes": len([r for r in results if r.auto_fixed]),
            "components": list(set(r.component for r in results)),
            "critical_issues": len([r for r in results if r.severity == Severity.CRITICAL and r.status == TestStatus.FAIL])
        }
        
        # Save to history file
        history_file = self.output_directory / "test_history.json"
        
        try:
            # Load existing history
            if history_file.exists():
                with open(history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
            
            # Add new record
            history.append(history_record)
            
            # Keep only last 100 records
            history = history[-100:]
            
            # Save updated history
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            self.logger.warning(f"Could not save test history: {e}")
        
        return history_record
    
    def generate_all_formats(self, results: List[TestResult], system_health: Optional[SystemHealth] = None) -> Dict[str, str]:
        """Generate reports in all supported formats"""
        generated_files = {}
        
        try:
            generated_files['html'] = self.generate_html_report(results, system_health)
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {e}")
        
        try:
            generated_files['json'] = self.export_json(results, system_health)
        except Exception as e:
            self.logger.error(f"Failed to generate JSON report: {e}")
        
        try:
            generated_files['csv'] = self.export_csv(results)
        except Exception as e:
            self.logger.error(f"Failed to generate CSV report: {e}")
        
        try:
            console_summary = self.generate_console_summary(results, system_health)
            print(console_summary)  # Display to console
        except Exception as e:
            self.logger.error(f"Failed to generate console summary: {e}")
        
        # Create test history
        try:
            self.create_test_history(results)
        except Exception as e:
            self.logger.error(f"Failed to create test history: {e}")
        
        return generated_files