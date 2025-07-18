"""
Data Models for Comprehensive System Testing
===========================================

Core data models and enums used throughout the testing framework.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional


class TestStatus(Enum):
    """Test execution status"""
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"
    IN_PROGRESS = "IN_PROGRESS"


class Severity(Enum):
    """Issue severity levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class HealthTrend(Enum):
    """System health trend indicators"""
    IMPROVING = "IMPROVING"
    STABLE = "STABLE"
    DEGRADING = "DEGRADING"


@dataclass
class TestResult:
    """Individual test result data model"""
    component: str
    test_name: str
    status: TestStatus
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    execution_time: float = 0.0
    auto_fixed: bool = False
    severity: Severity = Severity.MEDIUM
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'component': self.component,
            'test_name': self.test_name,
            'status': self.status.value,
            'message': self.message,
            'details': self.details,
            'timestamp': self.timestamp.isoformat(),
            'execution_time': self.execution_time,
            'auto_fixed': self.auto_fixed,
            'severity': self.severity.value
        }


@dataclass
class SystemHealth:
    """Overall system health data model"""
    overall_score: float  # 0-100
    component_scores: Dict[str, float] = field(default_factory=dict)
    critical_issues: List[TestResult] = field(default_factory=list)
    warnings: List[TestResult] = field(default_factory=list)
    last_test_time: datetime = field(default_factory=datetime.now)
    trend: HealthTrend = HealthTrend.STABLE
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'overall_score': self.overall_score,
            'component_scores': self.component_scores,
            'critical_issues': [issue.to_dict() for issue in self.critical_issues],
            'warnings': [warning.to_dict() for warning in self.warnings],
            'last_test_time': self.last_test_time.isoformat(),
            'trend': self.trend.value
        }


@dataclass
class TestConfiguration:
    """Test configuration settings"""
    enabled_tests: List[str] = field(default_factory=list)
    auto_fix_enabled: bool = True
    severity_threshold: Severity = Severity.MEDIUM
    timeout_seconds: int = 300
    parallel_execution: bool = True
    report_formats: List[str] = field(default_factory=lambda: ['html', 'console'])
    notification_settings: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'enabled_tests': self.enabled_tests,
            'auto_fix_enabled': self.auto_fix_enabled,
            'severity_threshold': self.severity_threshold.value,
            'timeout_seconds': self.timeout_seconds,
            'parallel_execution': self.parallel_execution,
            'report_formats': self.report_formats,
            'notification_settings': self.notification_settings
        }


@dataclass
class UserProfile:
    """User profile and preferences"""
    user_id: str
    email: str
    name: str
    preferences: TestConfiguration = field(default_factory=TestConfiguration)
    test_history: List[TestResult] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'preferences': self.preferences.to_dict(),
            'test_history': [result.to_dict() for result in self.test_history],
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }