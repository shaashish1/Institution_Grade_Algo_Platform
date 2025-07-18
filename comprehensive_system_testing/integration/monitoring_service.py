"""
Monitoring Service
=================

Continuous monitoring and alerting service.
"""

import time
import threading
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass

from ..core.test_orchestrator import TestOrchestrator
from ..core.models import TestConfiguration, TestResult, TestStatus, Severity
from ..utils.logger import TestLogger


@dataclass
class MonitoringAlert:
    """Monitoring alert data structure"""
    id: str
    type: str  # 'critical', 'warning', 'info'
    message: str
    timestamp: datetime
    component: str
    details: Dict[str, Any]
    acknowledged: bool = False


class MonitoringService:
    """Continuous monitoring and alerting service"""
    
    def __init__(self, project_root: str = ".", config: Optional[TestConfiguration] = None):
        self.project_root = Path(project_root)
        self.config = config or TestConfiguration()
        self.logger = TestLogger()
        
        # Monitoring state
        self.is_running = False
        self.monitoring_thread = None
        self.orchestrator = TestOrchestrator(self.config)
        
        # Alert management
        self.alerts = []
        self.alert_handlers = []
        self.alert_history = []
        
        # Monitoring configuration
        self.monitoring_config = {
            "interval_minutes": 60,
            "health_threshold": 70,
            "critical_threshold": 50,
            "max_alerts": 100,
            "alert_cooldown_minutes": 30
        }
        
        # Performance tracking
        self.performance_history = []
        self.last_test_results = None
        
        # Load configuration
        self._load_monitoring_config()
    
    def _load_monitoring_config(self):
        """Load monitoring configuration"""
        config_file = Path("comprehensive_system_testing/config/monitoring_config.json")
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    custom_config = json.load(f)
                self.monitoring_config.update(custom_config)
                self.logger.info("Loaded monitoring configuration")
            except Exception as e:
                self.logger.warning(f"Could not load monitoring config: {e}")
    
    def start_monitoring(self, interval_minutes: Optional[int] = None):
        """
        Start continuous monitoring
        
        Args:
            interval_minutes: Monitoring interval in minutes
        """
        if self.is_running:
            self.logger.warning("Monitoring is already running")
            return
        
        if interval_minutes:
            self.monitoring_config["interval_minutes"] = interval_minutes
        
        self.is_running = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        self.logger.info(f"Started monitoring with {self.monitoring_config['interval_minutes']} minute intervals")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        if not self.is_running:
            self.logger.warning("Monitoring is not running")
            return
        
        self.is_running = False
        
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=10)
        
        self.logger.info("Stopped monitoring")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        self.logger.info("Monitoring loop started")
        
        while self.is_running:
            try:
                # Run monitoring cycle
                self._run_monitoring_cycle()
                
                # Wait for next interval
                interval_seconds = self.monitoring_config["interval_minutes"] * 60
                
                # Sleep in small chunks to allow for quick shutdown
                for _ in range(interval_seconds):
                    if not self.is_running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait a minute before retrying
        
        self.logger.info("Monitoring loop stopped")
    
    def _run_monitoring_cycle(self):
        """Run a single monitoring cycle"""
        cycle_start = time.time()
        
        try:
            # Run quick test
            result = self.orchestrator.run_quick_test(str(self.project_root))
            
            if "error" in result:
                self._create_alert(
                    "critical",
                    f"Monitoring test failed: {result['error']}",
                    "monitoring_service",
                    {"error": result["error"]}
                )
                return
            
            # Analyze results
            results = result.get("results", [])
            self.last_test_results = results
            
            # Calculate health metrics
            health_metrics = self._calculate_health_metrics(results)
            
            # Record performance
            performance_record = {
                "timestamp": datetime.now().isoformat(),
                "execution_time": result.get("execution_time", 0),
                "total_tests": len(results),
                "health_score": health_metrics["health_score"],
                "critical_issues": health_metrics["critical_count"],
                "warnings": health_metrics["warning_count"]
            }
            
            self.performance_history.append(performance_record)
            
            # Keep only last 100 records
            self.performance_history = self.performance_history[-100:]
            
            # Check for alerts
            self._check_for_alerts(health_metrics, results)
            
            cycle_time = time.time() - cycle_start
            self.logger.info(f"Monitoring cycle completed in {cycle_time:.2f}s - Health: {health_metrics['health_score']:.1f}/100")
            
        except Exception as e:
            self.logger.error(f"Monitoring cycle failed: {e}")
            self._create_alert(
                "critical",
                f"Monitoring cycle exception: {str(e)}",
                "monitoring_service",
                {"exception": str(e)}
            )
    
    def _calculate_health_metrics(self, results: List[TestResult]) -> Dict[str, Any]:
        """Calculate health metrics from test results"""
        if not results:
            return {
                "health_score": 0,
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "warning_tests": 0,
                "critical_count": 0,
                "high_count": 0,
                "warning_count": 0
            }
        
        # Count by status
        passed = len([r for r in results if r.status == TestStatus.PASS])
        failed = len([r for r in results if r.status == TestStatus.FAIL])
        warnings = len([r for r in results if r.status == TestStatus.WARNING])
        
        # Count by severity
        critical_count = len([r for r in results if r.severity == Severity.CRITICAL and r.status == TestStatus.FAIL])
        high_count = len([r for r in results if r.severity == Severity.HIGH and r.status == TestStatus.FAIL])
        warning_count = len([r for r in results if r.status == TestStatus.WARNING])
        
        # Calculate health score
        total_tests = len(results)
        base_score = (passed / total_tests) * 100 if total_tests > 0 else 0
        
        # Apply penalties
        penalties = critical_count * 20 + high_count * 10 + warning_count * 2
        health_score = max(0, base_score - penalties)
        
        return {
            "health_score": health_score,
            "total_tests": total_tests,
            "passed_tests": passed,
            "failed_tests": failed,
            "warning_tests": warnings,
            "critical_count": critical_count,
            "high_count": high_count,
            "warning_count": warning_count
        }
    
    def _check_for_alerts(self, health_metrics: Dict[str, Any], results: List[TestResult]):
        """Check for conditions that should trigger alerts"""
        health_score = health_metrics["health_score"]
        
        # Critical health alert
        if health_score < self.monitoring_config["critical_threshold"]:
            self._create_alert(
                "critical",
                f"System health is critical: {health_score:.1f}/100",
                "health_monitor",
                {
                    "health_score": health_score,
                    "critical_issues": health_metrics["critical_count"],
                    "failed_tests": health_metrics["failed_tests"]
                }
            )
        
        # Warning health alert
        elif health_score < self.monitoring_config["health_threshold"]:
            self._create_alert(
                "warning",
                f"System health is low: {health_score:.1f}/100",
                "health_monitor",
                {
                    "health_score": health_score,
                    "warnings": health_metrics["warning_count"]
                }
            )
        
        # Critical issue alerts
        critical_issues = [r for r in results if r.severity == Severity.CRITICAL and r.status == TestStatus.FAIL]
        for issue in critical_issues:
            self._create_alert(
                "critical",
                f"Critical issue detected: {issue.message}",
                issue.component,
                {
                    "test_name": issue.test_name,
                    "details": issue.details
                }
            )
        
        # Performance degradation alert
        if len(self.performance_history) >= 3:
            recent_times = [p["execution_time"] for p in self.performance_history[-3:]]
            avg_recent = sum(recent_times) / len(recent_times)
            
            if len(self.performance_history) >= 10:
                older_times = [p["execution_time"] for p in self.performance_history[-10:-3]]
                avg_older = sum(older_times) / len(older_times)
                
                if avg_recent > avg_older * 1.5:  # 50% slower
                    self._create_alert(
                        "warning",
                        f"Performance degradation detected: {avg_recent:.2f}s vs {avg_older:.2f}s average",
                        "performance_monitor",
                        {
                            "recent_average": avg_recent,
                            "previous_average": avg_older,
                            "degradation_percent": ((avg_recent - avg_older) / avg_older) * 100
                        }
                    )
    
    def _create_alert(self, alert_type: str, message: str, component: str, details: Dict[str, Any]):
        """Create a new alert"""
        # Check for alert cooldown
        cooldown_minutes = self.monitoring_config["alert_cooldown_minutes"]
        cutoff_time = datetime.now() - timedelta(minutes=cooldown_minutes)
        
        # Check if similar alert exists in cooldown period
        similar_alerts = [
            a for a in self.alerts
            if a.type == alert_type and a.component == component and a.timestamp > cutoff_time
        ]
        
        if similar_alerts:
            self.logger.debug(f"Alert suppressed due to cooldown: {message}")
            return
        
        # Create new alert
        alert = MonitoringAlert(
            id=f"alert_{int(time.time())}_{len(self.alerts)}",
            type=alert_type,
            message=message,
            timestamp=datetime.now(),
            component=component,
            details=details
        )
        
        self.alerts.append(alert)
        self.alert_history.append(alert)
        
        # Keep only recent alerts
        max_alerts = self.monitoring_config["max_alerts"]
        self.alerts = self.alerts[-max_alerts:]
        self.alert_history = self.alert_history[-max_alerts * 2:]
        
        # Trigger alert handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                self.logger.error(f"Alert handler failed: {e}")
        
        self.logger.warning(f"Alert created: [{alert_type.upper()}] {message}")
    
    def add_alert_handler(self, handler: Callable[[MonitoringAlert], None]):
        """Add an alert handler function"""
        self.alert_handlers.append(handler)
        self.logger.info("Added alert handler")
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.acknowledged = True
                self.logger.info(f"Alert acknowledged: {alert_id}")
                return True
        
        return False
    
    def get_active_alerts(self) -> List[MonitoringAlert]:
        """Get all active (unacknowledged) alerts"""
        return [alert for alert in self.alerts if not alert.acknowledged]
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        active_alerts = self.get_active_alerts()
        
        status = {
            "is_running": self.is_running,
            "interval_minutes": self.monitoring_config["interval_minutes"],
            "last_cycle": None,
            "next_cycle": None,
            "active_alerts": len(active_alerts),
            "total_alerts": len(self.alerts),
            "performance_records": len(self.performance_history)
        }
        
        if self.performance_history:
            last_record = self.performance_history[-1]
            status["last_cycle"] = last_record["timestamp"]
            status["last_health_score"] = last_record["health_score"]
            
            if self.is_running:
                last_time = datetime.fromisoformat(last_record["timestamp"])
                next_time = last_time + timedelta(minutes=self.monitoring_config["interval_minutes"])
                status["next_cycle"] = next_time.isoformat()
        
        return status
    
    def get_health_trend(self, hours: int = 24) -> Dict[str, Any]:
        """Get health trend over specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_records = [
            record for record in self.performance_history
            if datetime.fromisoformat(record["timestamp"]) > cutoff_time
        ]
        
        if not recent_records:
            return {"trend": "unknown", "records": 0}
        
        # Calculate trend
        scores = [record["health_score"] for record in recent_records]
        
        if len(scores) < 2:
            return {"trend": "stable", "records": len(scores), "current_score": scores[0] if scores else 0}
        
        # Simple linear trend calculation
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg + 5:
            trend = "improving"
        elif second_avg < first_avg - 5:
            trend = "degrading"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "records": len(recent_records),
            "current_score": scores[-1],
            "average_score": sum(scores) / len(scores),
            "score_change": second_avg - first_avg
        }
    
    def export_monitoring_data(self) -> Dict[str, Any]:
        """Export monitoring data for analysis"""
        return {
            "monitoring_config": self.monitoring_config,
            "performance_history": self.performance_history,
            "alert_history": [
                {
                    "id": alert.id,
                    "type": alert.type,
                    "message": alert.message,
                    "timestamp": alert.timestamp.isoformat(),
                    "component": alert.component,
                    "details": alert.details,
                    "acknowledged": alert.acknowledged
                }
                for alert in self.alert_history
            ],
            "exported_at": datetime.now().isoformat()
        }
    
    def cleanup_old_data(self, days: int = 7):
        """Clean up old monitoring data"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        # Clean performance history
        initial_count = len(self.performance_history)
        self.performance_history = [
            record for record in self.performance_history
            if datetime.fromisoformat(record["timestamp"]) > cutoff_time
        ]
        
        # Clean alert history
        initial_alert_count = len(self.alert_history)
        self.alert_history = [
            alert for alert in self.alert_history
            if alert.timestamp > cutoff_time
        ]
        
        cleaned_records = initial_count - len(self.performance_history)
        cleaned_alerts = initial_alert_count - len(self.alert_history)
        
        if cleaned_records > 0 or cleaned_alerts > 0:
            self.logger.info(f"Cleaned up {cleaned_records} performance records and {cleaned_alerts} alerts")
        
        return {"cleaned_records": cleaned_records, "cleaned_alerts": cleaned_alerts}