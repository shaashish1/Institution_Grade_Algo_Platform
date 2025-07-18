"""
Risk Manager
============

Advanced risk management system for trading operations.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from .interfaces import Signal, Position, MarketData


class RiskLevel(Enum):
    """Risk level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskMetrics:
    """Risk metrics data structure"""
    portfolio_value: float
    total_exposure: float
    max_position_size: float
    var_95: float
    var_99: float
    sharpe_ratio: float
    max_drawdown: float
    risk_level: RiskLevel


class RiskManager:
    """Advanced risk management system"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize risk manager
        
        Args:
            config: Risk management configuration
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Risk limits
        self.max_portfolio_risk = self.config.get('max_portfolio_risk', 0.02)  # 2% max portfolio risk
        self.max_position_size = self.config.get('max_position_size', 0.1)     # 10% max position size
        self.max_correlation = self.config.get('max_correlation', 0.7)         # 70% max correlation
        self.max_drawdown_limit = self.config.get('max_drawdown_limit', 0.15)  # 15% max drawdown
        self.max_daily_loss = self.config.get('max_daily_loss', 0.05)          # 5% max daily loss
        
        # Position sizing
        self.position_sizing_method = self.config.get('position_sizing_method', 'fixed_fractional')
        self.risk_per_trade = self.config.get('risk_per_trade', 0.01)          # 1% risk per trade
        
        # Stop loss and take profit
        self.default_stop_loss = self.config.get('default_stop_loss', 0.05)    # 5% stop loss
        self.default_take_profit = self.config.get('default_take_profit', 0.10) # 10% take profit
        
        # Risk tracking
        self.daily_pnl = 0.0
        self.daily_start_value = 0.0
        self.current_drawdown = 0.0
        self.peak_portfolio_value = 0.0
        
        # Position tracking
        self.positions: Dict[str, Position] = {}
        self.position_risks: Dict[str, float] = {}
        
    def validate_signal(self, signal: Signal, portfolio_value: float, 
                       current_positions: Dict[str, Position],
                       market_data: Dict[str, MarketData]) -> Tuple[bool, str, float]:
        """Validate a trading signal against risk parameters
        
        Args:
            signal: Trading signal to validate
            portfolio_value: Current portfolio value
            current_positions: Current positions
            market_data: Current market data
            
        Returns:
            Tuple of (is_valid, reason, adjusted_quantity)
        """
        try:
            # Update internal state
            self.positions = current_positions
            
            # Basic signal validation
            if not signal.symbol or not signal.action or signal.quantity <= 0:
                return False, "Invalid signal parameters", 0.0
            
            # Check if we have market data
            if signal.symbol not in market_data:
                return False, f"No market data for {signal.symbol}", 0.0
            
            current_price = market_data[signal.symbol].close
            
            # Calculate position value
            position_value = signal.quantity * current_price
            
            # Check maximum position size
            max_position_value = portfolio_value * self.max_position_size
            if position_value > max_position_value:
                # Adjust quantity to maximum allowed
                adjusted_quantity = max_position_value / current_price
                return True, f"Position size adjusted to risk limit", adjusted_quantity
            
            # Check portfolio risk
            if signal.action.lower() == 'buy':
                # Calculate total exposure after this trade
                total_exposure = sum(pos.quantity * pos.market_price for pos in current_positions.values())
                total_exposure += position_value
                
                max_exposure = portfolio_value * 0.95  # Max 95% exposure
                if total_exposure > max_exposure:
                    return False, "Maximum portfolio exposure exceeded", 0.0
            
            # Check daily loss limit
            if self._check_daily_loss_limit(portfolio_value):
                return False, "Daily loss limit exceeded", 0.0
            
            # Check drawdown limit
            if self._check_drawdown_limit(portfolio_value):
                return False, "Maximum drawdown limit exceeded", 0.0
            
            # Position sizing based on risk
            risk_adjusted_quantity = self._calculate_position_size(
                signal, current_price, portfolio_value
            )
            
            return True, "Signal validated", risk_adjusted_quantity
            
        except Exception as e:
            self.logger.error(f"Error validating signal: {e}")
            return False, f"Validation error: {e}", 0.0
    
    def calculate_position_size(self, symbol: str, entry_price: float, 
                              stop_loss_price: float, portfolio_value: float) -> float:
        """Calculate optimal position size based on risk management
        
        Args:
            symbol: Trading symbol
            entry_price: Entry price
            stop_loss_price: Stop loss price
            portfolio_value: Current portfolio value
            
        Returns:
            Optimal position size
        """
        try:
            if self.position_sizing_method == 'fixed_fractional':
                return self._fixed_fractional_sizing(portfolio_value)
            
            elif self.position_sizing_method == 'risk_based':
                return self._risk_based_sizing(entry_price, stop_loss_price, portfolio_value)
            
            elif self.position_sizing_method == 'volatility_adjusted':
                return self._volatility_adjusted_sizing(symbol, entry_price, portfolio_value)
            
            else:
                # Default to fixed fractional
                return self._fixed_fractional_sizing(portfolio_value)
                
        except Exception as e:
            self.logger.error(f"Error calculating position size: {e}")
            return 0.0
    
    def _fixed_fractional_sizing(self, portfolio_value: float) -> float:
        """Fixed fractional position sizing"""
        return portfolio_value * self.max_position_size
    
    def _risk_based_sizing(self, entry_price: float, stop_loss_price: float, 
                          portfolio_value: float) -> float:
        """Risk-based position sizing"""
        if stop_loss_price <= 0 or entry_price <= 0:
            return self._fixed_fractional_sizing(portfolio_value)
        
        # Calculate risk per share
        risk_per_share = abs(entry_price - stop_loss_price)
        
        # Calculate maximum risk amount
        max_risk_amount = portfolio_value * self.risk_per_trade
        
        # Calculate position size
        if risk_per_share > 0:
            position_size = max_risk_amount / risk_per_share
            max_position_value = portfolio_value * self.max_position_size
            
            # Ensure we don't exceed maximum position size
            if position_size * entry_price > max_position_value:
                position_size = max_position_value / entry_price
            
            return position_size
        
        return self._fixed_fractional_sizing(portfolio_value)
    
    def _volatility_adjusted_sizing(self, symbol: str, entry_price: float, 
                                   portfolio_value: float) -> float:
        """Volatility-adjusted position sizing"""
        # This would require historical volatility data
        # For now, use fixed fractional as fallback
        return self._fixed_fractional_sizing(portfolio_value)
    
    def _calculate_position_size(self, signal: Signal, current_price: float, 
                               portfolio_value: float) -> float:
        """Calculate position size for a signal"""
        # Use risk-based sizing if stop loss is provided
        if signal.metadata and 'stop_loss' in signal.metadata:
            stop_loss_price = signal.metadata['stop_loss']
            return self.calculate_position_size(
                signal.symbol, current_price, stop_loss_price, portfolio_value
            ) / current_price
        
        # Otherwise use fixed fractional
        max_position_value = portfolio_value * self.max_position_size
        return min(signal.quantity, max_position_value / current_price)
    
    def _check_daily_loss_limit(self, current_portfolio_value: float) -> bool:
        """Check if daily loss limit is exceeded"""
        if self.daily_start_value == 0:
            self.daily_start_value = current_portfolio_value
            return False
        
        daily_loss = (self.daily_start_value - current_portfolio_value) / self.daily_start_value
        return daily_loss > self.max_daily_loss
    
    def _check_drawdown_limit(self, current_portfolio_value: float) -> bool:
        """Check if maximum drawdown limit is exceeded"""
        if current_portfolio_value > self.peak_portfolio_value:
            self.peak_portfolio_value = current_portfolio_value
            self.current_drawdown = 0.0
            return False
        
        if self.peak_portfolio_value > 0:
            self.current_drawdown = (self.peak_portfolio_value - current_portfolio_value) / self.peak_portfolio_value
            return self.current_drawdown > self.max_drawdown_limit
        
        return False
    
    def calculate_risk_metrics(self, portfolio_value: float, positions: Dict[str, Position],
                             historical_returns: List[float] = None) -> RiskMetrics:
        """Calculate comprehensive risk metrics
        
        Args:
            portfolio_value: Current portfolio value
            positions: Current positions
            historical_returns: Historical returns for VaR calculation
            
        Returns:
            RiskMetrics object
        """
        try:
            # Calculate total exposure
            total_exposure = sum(pos.quantity * pos.market_price for pos in positions.values())
            
            # Calculate maximum position size
            max_pos_size = max([pos.quantity * pos.market_price for pos in positions.values()]) if positions else 0
            
            # Calculate VaR if historical returns provided
            var_95 = var_99 = 0.0
            if historical_returns and len(historical_returns) > 0:
                import numpy as np
                returns_array = np.array(historical_returns)
                var_95 = np.percentile(returns_array, 5) * portfolio_value
                var_99 = np.percentile(returns_array, 1) * portfolio_value
            
            # Calculate Sharpe ratio (simplified)
            sharpe_ratio = 0.0
            if historical_returns and len(historical_returns) > 1:
                import numpy as np
                returns_array = np.array(historical_returns)
                if np.std(returns_array) > 0:
                    sharpe_ratio = np.mean(returns_array) / np.std(returns_array) * np.sqrt(252)
            
            # Determine risk level
            risk_level = self._determine_risk_level(
                total_exposure / portfolio_value if portfolio_value > 0 else 0,
                self.current_drawdown,
                sharpe_ratio
            )
            
            return RiskMetrics(
                portfolio_value=portfolio_value,
                total_exposure=total_exposure,
                max_position_size=max_pos_size,
                var_95=var_95,
                var_99=var_99,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=self.current_drawdown,
                risk_level=risk_level
            )
            
        except Exception as e:
            self.logger.error(f"Error calculating risk metrics: {e}")
            return RiskMetrics(
                portfolio_value=portfolio_value,
                total_exposure=0.0,
                max_position_size=0.0,
                var_95=0.0,
                var_99=0.0,
                sharpe_ratio=0.0,
                max_drawdown=0.0,
                risk_level=RiskLevel.MEDIUM
            )
    
    def _determine_risk_level(self, exposure_ratio: float, drawdown: float, 
                            sharpe_ratio: float) -> RiskLevel:
        """Determine overall risk level"""
        risk_score = 0
        
        # Exposure risk
        if exposure_ratio > 0.9:
            risk_score += 3
        elif exposure_ratio > 0.7:
            risk_score += 2
        elif exposure_ratio > 0.5:
            risk_score += 1
        
        # Drawdown risk
        if drawdown > 0.2:
            risk_score += 3
        elif drawdown > 0.1:
            risk_score += 2
        elif drawdown > 0.05:
            risk_score += 1
        
        # Sharpe ratio (lower is riskier)
        if sharpe_ratio < 0:
            risk_score += 2
        elif sharpe_ratio < 0.5:
            risk_score += 1
        
        # Determine risk level
        if risk_score >= 6:
            return RiskLevel.CRITICAL
        elif risk_score >= 4:
            return RiskLevel.HIGH
        elif risk_score >= 2:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def get_stop_loss_price(self, symbol: str, entry_price: float, 
                           action: str, custom_stop_loss: float = None) -> float:
        """Calculate stop loss price
        
        Args:
            symbol: Trading symbol
            entry_price: Entry price
            action: Trade action (buy/sell)
            custom_stop_loss: Custom stop loss percentage
            
        Returns:
            Stop loss price
        """
        stop_loss_pct = custom_stop_loss or self.default_stop_loss
        
        if action.lower() == 'buy':
            return entry_price * (1 - stop_loss_pct)
        else:
            return entry_price * (1 + stop_loss_pct)
    
    def get_take_profit_price(self, symbol: str, entry_price: float, 
                             action: str, custom_take_profit: float = None) -> float:
        """Calculate take profit price
        
        Args:
            symbol: Trading symbol
            entry_price: Entry price
            action: Trade action (buy/sell)
            custom_take_profit: Custom take profit percentage
            
        Returns:
            Take profit price
        """
        take_profit_pct = custom_take_profit or self.default_take_profit
        
        if action.lower() == 'buy':
            return entry_price * (1 + take_profit_pct)
        else:
            return entry_price * (1 - take_profit_pct)
    
    def reset_daily_tracking(self, current_portfolio_value: float):
        """Reset daily tracking metrics"""
        self.daily_start_value = current_portfolio_value
        self.daily_pnl = 0.0
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """Get risk management summary
        
        Returns:
            Dictionary with risk summary
        """
        return {
            'max_portfolio_risk': self.max_portfolio_risk,
            'max_position_size': self.max_position_size,
            'max_drawdown_limit': self.max_drawdown_limit,
            'current_drawdown': self.current_drawdown,
            'daily_loss_limit': self.max_daily_loss,
            'risk_per_trade': self.risk_per_trade,
            'position_sizing_method': self.position_sizing_method,
            'default_stop_loss': self.default_stop_loss,
            'default_take_profit': self.default_take_profit
        }