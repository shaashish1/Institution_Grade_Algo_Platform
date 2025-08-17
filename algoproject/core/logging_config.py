"""
Logging Configuration
====================

Centralized logging configuration for AlgoProject.
"""

import logging
import logging.handlers
import os
import sys
from typing import Dict, Any, Optional
from datetime import datetime


class AlgoProjectLogger:
    """Centralized logging manager for AlgoProject"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize logging configuration
        
        Args:
            config: Logging configuration dictionary
        """
        self.config = config
        self.loggers: Dict[str, logging.Logger] = {}
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        try:
            # Create logs directory if it doesn't exist
            log_file = self.config.get('file', 'logs/algoproject.log')
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # Configure root logger
            root_logger = logging.getLogger()
            root_logger.setLevel(self._get_log_level(self.config.get('level', 'INFO')))
            
            # Clear existing handlers
            root_logger.handlers.clear()
            
            # Create formatters
            detailed_formatter = logging.Formatter(
                self.config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            
            simple_formatter = logging.Formatter(
                '%(levelname)s - %(message)s'
            )
            
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self._get_log_level(self.config.get('console_level', 'INFO')))
            console_handler.setFormatter(simple_formatter)
            root_logger.addHandler(console_handler)
            
            # File handler with rotation
            if log_file:
                max_size = self._parse_size(self.config.get('max_size', '10MB'))
                backup_count = self.config.get('backup_count', 5)
                
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file,
                    maxBytes=max_size,
                    backupCount=backup_count
                )
                file_handler.setLevel(self._get_log_level(self.config.get('file_level', 'DEBUG')))
                file_handler.setFormatter(detailed_formatter)
                root_logger.addHandler(file_handler)
            
            # Error file handler
            error_file = self.config.get('error_file', 'logs/errors.log')
            if error_file:
                error_handler = logging.handlers.RotatingFileHandler(
                    error_file,
                    maxBytes=self._parse_size('5MB'),
                    backupCount=3
                )
                error_handler.setLevel(logging.ERROR)
                error_handler.setFormatter(detailed_formatter)
                root_logger.addHandler(error_handler)
            
            # Trading-specific log file
            trading_file = self.config.get('trading_file', 'logs/trading.log')
            if trading_file:
                trading_handler = logging.handlers.RotatingFileHandler(
                    trading_file,
                    maxBytes=self._parse_size('20MB'),
                    backupCount=10
                )
                trading_handler.setLevel(logging.INFO)
                trading_handler.setFormatter(detailed_formatter)
                
                # Add filter for trading-related logs
                trading_handler.addFilter(self._trading_filter)
                root_logger.addHandler(trading_handler)
            
            logging.info("Logging system initialized successfully")
            
        except Exception as e:
            print(f"Failed to setup logging: {e}")
            # Fallback to basic logging
            logging.basicConfig(level=logging.INFO)
    
    def _get_log_level(self, level_str: str) -> int:
        """Convert string log level to logging constant"""
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return levels.get(level_str.upper(), logging.INFO)
    
    def _parse_size(self, size_str: str) -> int:
        """Parse size string to bytes"""
        size_str = size_str.upper()
        if size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        elif size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('GB'):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        else:
            return int(size_str)
    
    def _trading_filter(self, record):
        """Filter for trading-related log records"""
        trading_modules = [
            'algoproject.trading',
            'algoproject.backtesting',
            'algoproject.strategies'
        ]
        return any(record.name.startswith(module) for module in trading_modules)
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get logger instance for a specific module
        
        Args:
            name: Logger name (usually __name__)
            
        Returns:
            Logger instance
        """
        if name not in self.loggers:
            self.loggers[name] = logging.getLogger(name)
        
        return self.loggers[name]
    
    def set_level(self, level: str, logger_name: Optional[str] = None):
        """Set log level for specific logger or root logger
        
        Args:
            level: Log level string
            logger_name: Specific logger name (None for root)
        """
        log_level = self._get_log_level(level)
        
        if logger_name:
            logger = self.get_logger(logger_name)
            logger.setLevel(log_level)
        else:
            logging.getLogger().setLevel(log_level)
    
    def add_custom_handler(self, handler: logging.Handler, logger_name: Optional[str] = None):
        """Add custom handler to logger
        
        Args:
            handler: Logging handler to add
            logger_name: Specific logger name (None for root)
        """
        if logger_name:
            logger = self.get_logger(logger_name)
            logger.addHandler(handler)
        else:
            logging.getLogger().addHandler(handler)


class PerformanceMonitor:
    """Performance monitoring and health checks"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.start_time = datetime.now()
        self.metrics: Dict[str, Any] = {}
        self.health_checks: Dict[str, bool] = {}
    
    def record_metric(self, name: str, value: Any, timestamp: Optional[datetime] = None):
        """Record a performance metric
        
        Args:
            name: Metric name
            value: Metric value
            timestamp: Timestamp (defaults to now)
        """
        timestamp = timestamp or datetime.now()
        
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append({
            'value': value,
            'timestamp': timestamp.isoformat()
        })
        
        # Keep only recent metrics (last 1000 entries)
        if len(self.metrics[name]) > 1000:
            self.metrics[name] = self.metrics[name][-1000:]
    
    def get_metrics(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Get performance metrics
        
        Args:
            name: Specific metric name (None for all)
            
        Returns:
            Metrics dictionary
        """
        if name:
            return self.metrics.get(name, [])
        return self.metrics
    
    def health_check(self, component: str, check_function: callable) -> bool:
        """Perform health check for a component
        
        Args:
            component: Component name
            check_function: Function that returns True if healthy
            
        Returns:
            Health status
        """
        try:
            is_healthy = check_function()
            self.health_checks[component] = is_healthy
            
            if not is_healthy:
                self.logger.warning(f"Health check failed for {component}")
            
            return is_healthy
            
        except Exception as e:
            self.logger.error(f"Health check error for {component}: {e}")
            self.health_checks[component] = False
            return False
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status
        
        Returns:
            Health status dictionary
        """
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'uptime_seconds': uptime,
            'overall_healthy': all(self.health_checks.values()),
            'components': self.health_checks,
            'failed_components': [
                comp for comp, status in self.health_checks.items() 
                if not status
            ]
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information
        
        Returns:
            System info dictionary
        """
        try:
            import psutil
            
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'process_count': len(psutil.pids()),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
            }
        except ImportError:
            return {
                'error': 'psutil not available for system monitoring'
            }


class AlertManager:
    """Alert management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.alerts: List[Dict[str, Any]] = []
        self.alert_handlers: List[callable] = []
    
    def add_alert_handler(self, handler: callable):
        """Add alert handler function
        
        Args:
            handler: Function to handle alerts
        """
        self.alert_handlers.append(handler)
    
    def send_alert(self, level: str, message: str, component: str, 
                  metadata: Optional[Dict[str, Any]] = None):
        """Send alert
        
        Args:
            level: Alert level (INFO, WARNING, ERROR, CRITICAL)
            message: Alert message
            component: Component that generated the alert
            metadata: Additional metadata
        """
        alert = {
            'level': level,
            'message': message,
            'component': component,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.alerts.append(alert)
        
        # Keep only recent alerts
        if len(self.alerts) > 1000:
            self.alerts = self.alerts[-1000:]
        
        # Log alert
        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.log(log_level, f"ALERT [{level}] {component}: {message}")
        
        # Notify handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                self.logger.error(f"Alert handler error: {e}")
    
    def get_alerts(self, level: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent alerts
        
        Args:
            level: Filter by alert level
            limit: Maximum number of alerts
            
        Returns:
            List of alerts
        """
        alerts = self.alerts
        
        if level:
            alerts = [alert for alert in alerts if alert['level'] == level]
        
        return sorted(alerts, key=lambda x: x['timestamp'], reverse=True)[:limit]


# Global instances
_logger_instance: Optional[AlgoProjectLogger] = None
_performance_monitor: Optional[PerformanceMonitor] = None
_alert_manager: Optional[AlertManager] = None


def setup_logging(config: Dict[str, Any]):
    """Setup global logging configuration"""
    global _logger_instance
    _logger_instance = AlgoProjectLogger(config)


def get_logger(name: str) -> logging.Logger:
    """Get logger instance"""
    if _logger_instance:
        return _logger_instance.get_logger(name)
    return logging.getLogger(name)


def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor"""
    global _performance_monitor
    if not _performance_monitor:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


def get_alert_manager() -> AlertManager:
    """Get global alert manager"""
    global _alert_manager
    if not _alert_manager:
        _alert_manager = AlertManager()
    return _alert_manager