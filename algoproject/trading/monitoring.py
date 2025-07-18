"""
Trading Monitoring
=================

Real-time monitoring and controls for live trading.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from ..core.interfaces import Signal, MarketData
from ..backtesting.reporting.performance_analyzer import PerformanceAnalyzer


class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class Alert:
    """Trading alert"""
    level: AlertLevel
    message: str
    timestamp: datetime
    source: str
    metadata: Dict[str, Any]


class TradingMonitor:
    """Real-time trading monitor with alerts and controls"""
    
    def __init__(self, trading_engine):
        """Initialize trading monitor
        
        Args:
            trading_engine: Live trading engine to monitor
        """
        self.trading_engine = trading_engine
        self.logger = logging.getLogger(__name__)
        
        # Monitoring state
        self.is_monitoring = False
        self.alerts: List[Alert] = []
        self.alert_callbacks: List[Callable] = []
        
        # Performance tracking
        self.performance_analyzer = PerformanceAnalyzer()
        self.kpi_history: List[Dict[str, Any]] = []
        self.last_kpi_update = datetime.now()
        
        # Risk thresholds
        self.max_drawdown_threshold = 0.10  # 10%
        self.daily_loss_threshold = 0.05    # 5%
        self.position_size_threshold = 0.15  # 15%
        self.consecutive_loss_threshold = 5
        
        # Monitoring intervals
        self.kpi_update_interval = timedelta(minutes=1)
        self.risk_check_interval = timedelta(seconds=30)
        
        # State tracking
        self.consecutive_losses = 0
        self.daily_pnl = 0.0
        self.session_start_value = 0.0
        self.max_session_value = 0.0
        
    def start_monitoring(self):
        """Start real-time monitoring"""
        try:
            if self.is_monitoring:
                self.logger.warning("Monitoring already active")
                return
            
            self.is_monitoring = True
            self.session_start_value = self._get_portfolio_value()
            self.max_session_value = self.session_start_value
            
            self.logger.info("Trading monitoring started")
            
            # Start monitoring tasks
            asyncio.create_task(self._monitoring_loop())
            asyncio.create_task(self._kpi_update_loop())
            
        except Exception as e:
            self.logger.error(f"Failed to start monitoring: {e}")
            self.is_monitoring = False
            raise
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        self.logger.info("Trading monitoring stopped")
    
    def add_alert_callback(self, callback: Callable[[Alert], None]):
        """Add callback for alert notifications
        
        Args:
            callback: Function to call when alerts are generated
        """
        self.alert_callbacks.append(callback)
    
    def get_current_kpis(self) -> Dict[str, Any]:
        """Get current KPI values"""
        try:
            current_value = self._get_portfolio_value()
            positions = self.trading_engine.get_positions()
            
            # Calculate basic metrics
            total_return = (current_value - self.session_start_value) / self.session_start_value
            current_drawdown = (self.max_session_value - current_value) / self.max_session_value
            
            # Position metrics
            total_position_value = sum(abs(pos) for pos in positions.values())
            largest_position = max(abs(pos) for pos in positions.values()) if positions else 0
            
            kpis = {
                'timestamp': datetime.now().isoformat(),
                'portfolio_value': current_value,
                'total_return_pct': total_return * 100,
                'daily_pnl': self.daily_pnl,
                'current_drawdown_pct': current_drawdown * 100,
                'max_drawdown_pct': current_drawdown * 100,  # Simplified for demo
                'total_positions': len(positions),
                'total_position_value': total_position_value,
                'largest_position_pct': (largest_position / current_value * 100) if current_value > 0 else 0,
                'consecutive_losses': self.consecutive_losses,
                'total_trades': self.trading_engine.total_trades,
                'success_rate_pct': (self.trading_engine.successful_trades / max(self.trading_engine.total_trades, 1)) * 100
            }
            
            return kpis
            
        except Exception as e:
            self.logger.error(f"Error calculating KPIs: {e}")
            return {}
    
    def get_alerts(self, level: Optional[AlertLevel] = None, limit: int = 100) -> List[Alert]:
        """Get recent alerts
        
        Args:
            level: Filter by alert level
            limit: Maximum number of alerts to return
            
        Returns:
            List of alerts
        """
        alerts = self.alerts
        
        if level:
            alerts = [alert for alert in alerts if alert.level == level]
        
        # Return most recent alerts first
        return sorted(alerts, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def check_risk_thresholds(self) -> List[Alert]:
        """Check all risk thresholds and generate alerts"""
        alerts = []
        kpis = self.get_current_kpis()
        
        if not kpis:
            return alerts
        
        # Check drawdown threshold
        if kpis['current_drawdown_pct'] > self.max_drawdown_threshold * 100:
            alert = Alert(
                level=AlertLevel.CRITICAL,
                message=f"Maximum drawdown exceeded: {kpis['current_drawdown_pct']:.2f}%",
                timestamp=datetime.now(),
                source="risk_monitor",
                metadata={'threshold': self.max_drawdown_threshold * 100, 'current': kpis['current_drawdown_pct']}
            )
            alerts.append(alert)
        
        # Check daily loss threshold
        daily_loss_pct = (self.daily_pnl / self.session_start_value) * 100 if self.session_start_value > 0 else 0
        if daily_loss_pct < -self.daily_loss_threshold * 100:
            alert = Alert(
                level=AlertLevel.CRITICAL,
                message=f"Daily loss limit exceeded: {daily_loss_pct:.2f}%",
                timestamp=datetime.now(),
                source="risk_monitor",
                metadata={'threshold': -self.daily_loss_threshold * 100, 'current': daily_loss_pct}
            )
            alerts.append(alert)
        
        # Check position size threshold
        if kpis['largest_position_pct'] > self.position_size_threshold * 100:
            alert = Alert(
                level=AlertLevel.WARNING,
                message=f"Large position detected: {kpis['largest_position_pct']:.2f}%",
                timestamp=datetime.now(),
                source="risk_monitor",
                metadata={'threshold': self.position_size_threshold * 100, 'current': kpis['largest_position_pct']}
            )
            alerts.append(alert)
        
        # Check consecutive losses
        if self.consecutive_losses >= self.consecutive_loss_threshold:
            alert = Alert(
                level=AlertLevel.WARNING,
                message=f"Consecutive losses detected: {self.consecutive_losses}",
                timestamp=datetime.now(),
                source="risk_monitor",
                metadata={'threshold': self.consecutive_loss_threshold, 'current': self.consecutive_losses}
            )
            alerts.append(alert)
        
        # Add alerts to history
        for alert in alerts:
            self._add_alert(alert)
        
        return alerts
    
    def get_orderbook_monitor(self, symbol: str) -> Dict[str, Any]:
        """Get order book monitoring data
        
        Args:
            symbol: Symbol to monitor
            
        Returns:
            Order book analysis
        """
        try:
            # TODO: Implement actual order book monitoring
            # For now, return mock data
            return {
                'symbol': symbol,
                'timestamp': datetime.now().isoformat(),
                'bid_price': 50000.0,
                'ask_price': 50001.0,
                'spread': 1.0,
                'spread_pct': 0.002,
                'bid_volume': 10.5,
                'ask_volume': 8.3,
                'market_depth': {
                    'bids': [{'price': 50000.0, 'volume': 10.5}],
                    'asks': [{'price': 50001.0, 'volume': 8.3}]
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting order book for {symbol}: {e}")
            return {}
    
    def get_position_monitor(self) -> Dict[str, Any]:
        """Get position monitoring data"""
        try:
            positions = self.trading_engine.get_positions()
            current_value = self._get_portfolio_value()
            
            position_analysis = []
            
            for symbol, quantity in positions.items():
                if quantity != 0:
                    # TODO: Get current market price
                    market_price = 50000.0  # Mock price
                    position_value = abs(quantity) * market_price
                    position_pct = (position_value / current_value * 100) if current_value > 0 else 0
                    
                    position_analysis.append({
                        'symbol': symbol,
                        'quantity': quantity,
                        'market_price': market_price,
                        'position_value': position_value,
                        'position_pct': position_pct,
                        'side': 'long' if quantity > 0 else 'short'
                    })
            
            return {
                'timestamp': datetime.now().isoformat(),
                'total_positions': len(position_analysis),
                'total_exposure': sum(pos['position_value'] for pos in position_analysis),
                'positions': position_analysis
            }
            
        except Exception as e:
            self.logger.error(f"Error getting position monitor: {e}")
            return {}
    
    def emergency_stop(self, reason: str):
        """Trigger emergency stop
        
        Args:
            reason: Reason for emergency stop
        """
        try:
            # Create emergency alert
            alert = Alert(
                level=AlertLevel.EMERGENCY,
                message=f"EMERGENCY STOP TRIGGERED: {reason}",
                timestamp=datetime.now(),
                source="monitor",
                metadata={'reason': reason}
            )
            
            self._add_alert(alert)
            
            # Stop trading engine
            self.trading_engine.emergency_stop_all()
            
            self.logger.critical(f"Emergency stop triggered: {reason}")
            
        except Exception as e:
            self.logger.error(f"Error during emergency stop: {e}")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        try:
            while self.is_monitoring:
                # Check risk thresholds
                alerts = self.check_risk_thresholds()
                
                # Handle critical alerts
                for alert in alerts:
                    if alert.level == AlertLevel.CRITICAL:
                        # Consider emergency stop for critical alerts
                        if "drawdown exceeded" in alert.message.lower():
                            self.emergency_stop("Maximum drawdown exceeded")
                        elif "loss limit exceeded" in alert.message.lower():
                            self.emergency_stop("Daily loss limit exceeded")
                
                # Sleep before next check
                await asyncio.sleep(self.risk_check_interval.total_seconds())
                
        except Exception as e:
            self.logger.error(f"Error in monitoring loop: {e}")
    
    async def _kpi_update_loop(self):
        """KPI update loop"""
        try:
            while self.is_monitoring:
                # Update KPIs
                kpis = self.get_current_kpis()
                if kpis:
                    self.kpi_history.append(kpis)
                    
                    # Keep only recent history (last 24 hours)
                    cutoff_time = datetime.now() - timedelta(hours=24)
                    self.kpi_history = [
                        kpi for kpi in self.kpi_history 
                        if datetime.fromisoformat(kpi['timestamp']) > cutoff_time
                    ]
                    
                    self.last_kpi_update = datetime.now()
                
                # Sleep before next update
                await asyncio.sleep(self.kpi_update_interval.total_seconds())
                
        except Exception as e:
            self.logger.error(f"Error in KPI update loop: {e}")
    
    def _add_alert(self, alert: Alert):
        """Add alert to history and notify callbacks"""
        self.alerts.append(alert)
        
        # Keep only recent alerts (last 1000)
        if len(self.alerts) > 1000:
            self.alerts = self.alerts[-1000:]
        
        # Notify callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {e}")
        
        # Log alert
        log_level = {
            AlertLevel.INFO: logging.INFO,
            AlertLevel.WARNING: logging.WARNING,
            AlertLevel.CRITICAL: logging.CRITICAL,
            AlertLevel.EMERGENCY: logging.CRITICAL
        }.get(alert.level, logging.INFO)
        
        self.logger.log(log_level, f"ALERT [{alert.level.value.upper()}]: {alert.message}")
    
    def _get_portfolio_value(self) -> float:
        """Get current portfolio value"""
        try:
            # TODO: Calculate actual portfolio value
            # For now, return mock value
            return 100000.0 + self.daily_pnl
        except Exception as e:
            self.logger.error(f"Error getting portfolio value: {e}")
            return 0.0
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get monitoring system status"""
        return {
            'monitoring_active': self.is_monitoring,
            'last_kpi_update': self.last_kpi_update.isoformat(),
            'total_alerts': len(self.alerts),
            'critical_alerts': len([a for a in self.alerts if a.level == AlertLevel.CRITICAL]),
            'emergency_alerts': len([a for a in self.alerts if a.level == AlertLevel.EMERGENCY]),
            'consecutive_losses': self.consecutive_losses,
            'session_start_value': self.session_start_value,
            'current_portfolio_value': self._get_portfolio_value()
        }