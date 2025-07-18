"""
Customizable Testing Dashboard
=============================

User-customizable interface for testing framework.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..core.models import TestConfiguration, UserProfile
from ..core.test_orchestrator import TestOrchestrator
from ..utils.logger import TestLogger


class TestingDashboard:
    """Customizable testing dashboard for users"""
    
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.logger = TestLogger()
        self.orchestrator = TestOrchestrator(user_profile.preferences)
        
        # Dashboard configuration
        self.dashboard_config = self._load_dashboard_config()
    
    def _load_dashboard_config(self) -> Dict[str, Any]:
        """Load user's dashboard configuration"""
        default_config = {
            "layout": "grid",
            "widgets": [
                {"type": "system_health", "position": {"row": 0, "col": 0}, "size": {"width": 2, "height": 1}},
                {"type": "recent_tests", "position": {"row": 0, "col": 2}, "size": {"width": 2, "height": 2}},
                {"type": "quick_actions", "position": {"row": 1, "col": 0}, "size": {"width": 1, "height": 1}},
                {"type": "test_statistics", "position": {"row": 1, "col": 1}, "size": {"width": 1, "height": 1}}
            ],
            "theme": "dark",
            "auto_refresh": True,
            "refresh_interval": 30,
            "notifications": {
                "enabled": True,
                "critical_issues": True,
                "test_completion": True,
                "auto_fixes": False
            }
        }
        
        # Try to load user's custom config
        config_file = Path(f"comprehensive_system_testing/user_data/{self.user_profile.user_id}_dashboard.json")
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    custom_config = json.load(f)
                
                # Merge with defaults
                default_config.update(custom_config)
                
            except Exception as e:
                self.logger.warning(f"Could not load dashboard config: {e}")
        
        return default_config
    
    def save_dashboard_config(self, config: Dict[str, Any]) -> bool:
        """Save user's dashboard configuration"""
        try:
            config_file = Path(f"comprehensive_system_testing/user_data/{self.user_profile.user_id}_dashboard.json")
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.dashboard_config = config
            self.logger.info(f"Saved dashboard config for user: {self.user_profile.email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save dashboard config: {e}")
            return False
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get all data needed for dashboard rendering"""
        dashboard_data = {
            "user_info": {
                "name": self.user_profile.name,
                "email": self.user_profile.email,
                "member_since": self.user_profile.created_at.strftime("%Y-%m-%d"),
                "last_login": self.user_profile.last_login.strftime("%Y-%m-%d %H:%M") if self.user_profile.last_login else "Never"
            },
            "config": self.dashboard_config,
            "widgets": {}
        }
        
        # Generate data for each widget
        for widget in self.dashboard_config.get("widgets", []):
            widget_type = widget["type"]
            widget_data = self._generate_widget_data(widget_type)
            dashboard_data["widgets"][widget_type] = widget_data
        
        return dashboard_data
    
    def _generate_widget_data(self, widget_type: str) -> Dict[str, Any]:
        """Generate data for a specific widget type"""
        if widget_type == "system_health":
            return self._get_system_health_widget_data()
        elif widget_type == "recent_tests":
            return self._get_recent_tests_widget_data()
        elif widget_type == "quick_actions":
            return self._get_quick_actions_widget_data()
        elif widget_type == "test_statistics":
            return self._get_test_statistics_widget_data()
        elif widget_type == "custom_test_suites":
            return self._get_custom_test_suites_widget_data()
        elif widget_type == "notifications":
            return self._get_notifications_widget_data()
        else:
            return {"error": f"Unknown widget type: {widget_type}"}
    
    def _get_system_health_widget_data(self) -> Dict[str, Any]:
        """Get system health widget data"""
        # Get latest test results from user history
        if not self.user_profile.test_history:
            return {
                "status": "unknown",
                "score": 0,
                "message": "No tests run yet",
                "last_updated": None
            }
        
        latest_test = self.user_profile.test_history[-1]
        
        return {
            "status": "healthy" if latest_test.get("system_health_score", 0) > 80 else "warning" if latest_test.get("system_health_score", 0) > 60 else "critical",
            "score": latest_test.get("system_health_score", 0),
            "message": f"Last test: {latest_test.get('total_tests', 0)} tests run",
            "last_updated": latest_test.get("timestamp"),
            "trend": "stable"  # Could be calculated from history
        }
    
    def _get_recent_tests_widget_data(self) -> Dict[str, Any]:
        """Get recent tests widget data"""
        recent_tests = self.user_profile.test_history[-5:]  # Last 5 tests
        
        formatted_tests = []
        for test in recent_tests:
            formatted_tests.append({
                "timestamp": test.get("timestamp"),
                "mode": test.get("mode", "unknown"),
                "total_tests": test.get("total_tests", 0),
                "score": test.get("system_health_score", 0),
                "duration": test.get("execution_time", 0),
                "status": "success" if test.get("system_health_score", 0) > 70 else "warning"
            })
        
        return {
            "tests": formatted_tests,
            "total_count": len(self.user_profile.test_history)
        }
    
    def _get_quick_actions_widget_data(self) -> Dict[str, Any]:
        """Get quick actions widget data"""
        return {
            "actions": [
                {
                    "id": "run_quick_test",
                    "label": "Quick Test",
                    "description": "Run essential checks",
                    "icon": "⚡",
                    "estimated_time": "30s"
                },
                {
                    "id": "run_comprehensive_test",
                    "label": "Full Test",
                    "description": "Complete system validation",
                    "icon": "🔍",
                    "estimated_time": "5min"
                },
                {
                    "id": "run_custom_suite",
                    "label": "Custom Suite",
                    "description": "Run your custom test suite",
                    "icon": "⚙️",
                    "estimated_time": "varies"
                },
                {
                    "id": "view_reports",
                    "label": "View Reports",
                    "description": "Browse test reports",
                    "icon": "📊",
                    "estimated_time": "instant"
                }
            ]
        }
    
    def _get_test_statistics_widget_data(self) -> Dict[str, Any]:
        """Get test statistics widget data"""
        if not self.user_profile.test_history:
            return {
                "total_tests": 0,
                "average_score": 0,
                "tests_this_week": 0,
                "improvement_trend": 0
            }
        
        total_tests = len(self.user_profile.test_history)
        scores = [test.get("system_health_score", 0) for test in self.user_profile.test_history]
        average_score = sum(scores) / len(scores) if scores else 0
        
        # Calculate tests this week
        from datetime import datetime, timedelta
        week_ago = datetime.now() - timedelta(days=7)
        tests_this_week = len([
            test for test in self.user_profile.test_history
            if datetime.fromisoformat(test.get("timestamp", "1970-01-01")) > week_ago
        ])
        
        # Calculate improvement trend (simple)
        improvement_trend = 0
        if len(scores) >= 2:
            recent_avg = sum(scores[-3:]) / len(scores[-3:])
            older_avg = sum(scores[:-3]) / len(scores[:-3]) if len(scores) > 3 else scores[0]
            improvement_trend = recent_avg - older_avg
        
        return {
            "total_tests": total_tests,
            "average_score": round(average_score, 1),
            "tests_this_week": tests_this_week,
            "improvement_trend": round(improvement_trend, 1)
        }
    
    def _get_custom_test_suites_widget_data(self) -> Dict[str, Any]:
        """Get custom test suites widget data"""
        # Load user's custom test suites
        suites_file = Path(f"comprehensive_system_testing/user_data/{self.user_profile.user_id}_test_suites.json")
        
        custom_suites = []
        if suites_file.exists():
            try:
                with open(suites_file, 'r') as f:
                    custom_suites = json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load custom test suites: {e}")
        
        return {
            "suites": custom_suites,
            "count": len(custom_suites)
        }
    
    def _get_notifications_widget_data(self) -> Dict[str, Any]:
        """Get notifications widget data"""
        # Generate notifications based on recent test results and system state
        notifications = []
        
        if self.user_profile.test_history:
            latest_test = self.user_profile.test_history[-1]
            score = latest_test.get("system_health_score", 0)
            
            if score < 50:
                notifications.append({
                    "type": "critical",
                    "message": f"System health is critical ({score}/100)",
                    "timestamp": latest_test.get("timestamp"),
                    "action": "run_comprehensive_test"
                })
            elif score < 80:
                notifications.append({
                    "type": "warning",
                    "message": f"System health needs attention ({score}/100)",
                    "timestamp": latest_test.get("timestamp"),
                    "action": "view_issues"
                })
        
        # Check for auto-fixes
        auto_fixes = sum(1 for test in self.user_profile.test_history[-5:] if test.get("auto_fixes", 0) > 0)
        if auto_fixes > 0:
            notifications.append({
                "type": "info",
                "message": f"{auto_fixes} auto-fixes applied in recent tests",
                "timestamp": datetime.now().isoformat(),
                "action": "view_fixes"
            })
        
        return {
            "notifications": notifications,
            "unread_count": len([n for n in notifications if n["type"] in ["critical", "warning"]])
        }
    
    def create_custom_test_suite(self, suite_name: str, components: List[str], settings: Dict[str, Any]) -> bool:
        """Create a custom test suite"""
        try:
            suites_file = Path(f"comprehensive_system_testing/user_data/{self.user_profile.user_id}_test_suites.json")
            
            # Load existing suites
            custom_suites = []
            if suites_file.exists():
                with open(suites_file, 'r') as f:
                    custom_suites = json.load(f)
            
            # Add new suite
            new_suite = {
                "id": f"suite_{len(custom_suites) + 1}",
                "name": suite_name,
                "components": components,
                "settings": settings,
                "created_at": datetime.now().isoformat(),
                "last_run": None,
                "run_count": 0
            }
            
            custom_suites.append(new_suite)
            
            # Save suites
            suites_file.parent.mkdir(parents=True, exist_ok=True)
            with open(suites_file, 'w') as f:
                json.dump(custom_suites, f, indent=2)
            
            self.logger.info(f"Created custom test suite: {suite_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create custom test suite: {e}")
            return False
    
    def run_custom_test_suite(self, suite_id: str, target: str) -> Dict[str, Any]:
        """Run a custom test suite"""
        try:
            # Load custom suites
            suites_file = Path(f"comprehensive_system_testing/user_data/{self.user_profile.user_id}_test_suites.json")
            
            if not suites_file.exists():
                return {"error": "No custom test suites found"}
            
            with open(suites_file, 'r') as f:
                custom_suites = json.load(f)
            
            # Find the suite
            suite = None
            for s in custom_suites:
                if s["id"] == suite_id:
                    suite = s
                    break
            
            if not suite:
                return {"error": f"Test suite {suite_id} not found"}
            
            # Run the test suite
            components = suite["components"]
            result = self.orchestrator.run_targeted_test(target, components)
            
            # Update suite run statistics
            suite["last_run"] = datetime.now().isoformat()
            suite["run_count"] = suite.get("run_count", 0) + 1
            
            # Save updated suites
            with open(suites_file, 'w') as f:
                json.dump(custom_suites, f, indent=2)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to run custom test suite: {e}")
            return {"error": str(e)}
    
    def update_widget_layout(self, widgets: List[Dict[str, Any]]) -> bool:
        """Update dashboard widget layout"""
        try:
            self.dashboard_config["widgets"] = widgets
            return self.save_dashboard_config(self.dashboard_config)
        except Exception as e:
            self.logger.error(f"Failed to update widget layout: {e}")
            return False
    
    def set_notification_preferences(self, preferences: Dict[str, Any]) -> bool:
        """Set notification preferences"""
        try:
            self.dashboard_config["notifications"] = preferences
            return self.save_dashboard_config(self.dashboard_config)
        except Exception as e:
            self.logger.error(f"Failed to set notification preferences: {e}")
            return False
    
    def export_dashboard_config(self) -> Dict[str, Any]:
        """Export dashboard configuration for backup"""
        return {
            "dashboard_config": self.dashboard_config,
            "custom_suites": self._get_custom_test_suites_widget_data(),
            "exported_at": datetime.now().isoformat(),
            "user_id": self.user_profile.user_id
        }
    
    def import_dashboard_config(self, config_data: Dict[str, Any]) -> bool:
        """Import dashboard configuration from backup"""
        try:
            if "dashboard_config" in config_data:
                self.save_dashboard_config(config_data["dashboard_config"])
            
            if "custom_suites" in config_data:
                suites = config_data["custom_suites"].get("suites", [])
                if suites:
                    suites_file = Path(f"comprehensive_system_testing/user_data/{self.user_profile.user_id}_test_suites.json")
                    suites_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(suites_file, 'w') as f:
                        json.dump(suites, f, indent=2)
            
            self.logger.info("Imported dashboard configuration")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import dashboard config: {e}")
            return False