"""
Portfolio Management
===================

Portfolio management for backtesting and live trading.
"""

import logging
from typing import Dict, Optional
from datetime import datetime

from ..core.interfaces import Position


class Portfolio:
    """Portfolio management class"""
    
    def __init__(self, initial_cash: float = 100000.0):
        """Initialize portfolio
        
        Args:
            initial_cash: Initial cash balance
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions: Dict[str, Position] = {}
        self.market_prices: Dict[str, float] = {}
        self.logger = logging.getLogger(__name__)
    
    def buy(self, symbol: str, quantity: float, price: float, commission: float = 0.0) -> bool:
        """Buy shares of a symbol
        
        Args:
            symbol: Trading symbol
            quantity: Number of shares to buy
            price: Price per share
            commission: Commission to pay
            
        Returns:
            True if purchase successful, False otherwise
        """
        total_cost = (quantity * price) + commission
        
        if total_cost > self.cash:
            self.logger.warning(f"Insufficient cash for purchase: need {total_cost}, have {self.cash}")
            return False
        
        # Deduct cash
        self.cash -= total_cost
        
        # Update position
        if symbol in self.positions:
            # Add to existing position
            existing_pos = self.positions[symbol]
            total_quantity = existing_pos.quantity + quantity
            total_cost_basis = (existing_pos.quantity * existing_pos.avg_price) + (quantity * price)
            avg_price = total_cost_basis / total_quantity
            
            self.positions[symbol] = Position(
                symbol=symbol,
                quantity=total_quantity,
                avg_price=avg_price,
                market_price=price,
                timestamp=datetime.now()
            )
        else:
            # Create new position
            self.positions[symbol] = Position(
                symbol=symbol,
                quantity=quantity,
                avg_price=price,
                market_price=price,
                timestamp=datetime.now()
            )
        
        # Update market price
        self.market_prices[symbol] = price
        
        self.logger.info(f"Bought {quantity} shares of {symbol} at {price}")
        return True
    
    def sell(self, symbol: str, quantity: float, price: float, commission: float = 0.0) -> bool:
        """Sell shares of a symbol
        
        Args:
            symbol: Trading symbol
            quantity: Number of shares to sell
            price: Price per share
            commission: Commission to pay
            
        Returns:
            True if sale successful, False otherwise
        """
        if symbol not in self.positions:
            self.logger.warning(f"No position in {symbol} to sell")
            return False
        
        position = self.positions[symbol]
        
        if quantity > position.quantity:
            self.logger.warning(f"Insufficient shares to sell: need {quantity}, have {position.quantity}")
            return False
        
        # Calculate proceeds
        gross_proceeds = quantity * price
        net_proceeds = gross_proceeds - commission
        
        # Add cash
        self.cash += net_proceeds
        
        # Update position
        remaining_quantity = position.quantity - quantity
        
        if remaining_quantity <= 0:
            # Close position completely
            del self.positions[symbol]
        else:
            # Reduce position
            self.positions[symbol] = Position(
                symbol=symbol,
                quantity=remaining_quantity,
                avg_price=position.avg_price,  # Keep original average price
                market_price=price,
                timestamp=datetime.now()
            )
        
        # Update market price
        self.market_prices[symbol] = price
        
        self.logger.info(f"Sold {quantity} shares of {symbol} at {price}")
        return True
    
    def update_market_price(self, symbol: str, price: float):
        """Update market price for a symbol
        
        Args:
            symbol: Trading symbol
            price: Current market price
        """
        self.market_prices[symbol] = price
        
        # Update position market price if we have a position
        if symbol in self.positions:
            position = self.positions[symbol]
            self.positions[symbol] = Position(
                symbol=position.symbol,
                quantity=position.quantity,
                avg_price=position.avg_price,
                market_price=price,
                timestamp=position.timestamp
            )
    
    def get_position_quantity(self, symbol: str) -> float:
        """Get position quantity for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Position quantity (0 if no position)
        """
        if symbol in self.positions:
            return self.positions[symbol].quantity
        return 0.0
    
    def get_position_value(self, symbol: str) -> float:
        """Get current market value of a position
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Current market value of position
        """
        if symbol not in self.positions:
            return 0.0
        
        position = self.positions[symbol]
        market_price = self.market_prices.get(symbol, position.avg_price)
        return position.quantity * market_price
    
    def get_position_pnl(self, symbol: str) -> float:
        """Get unrealized P&L for a position
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Unrealized P&L
        """
        if symbol not in self.positions:
            return 0.0
        
        position = self.positions[symbol]
        market_price = self.market_prices.get(symbol, position.avg_price)
        
        cost_basis = position.quantity * position.avg_price
        market_value = position.quantity * market_price
        
        return market_value - cost_basis
    
    def get_total_positions_value(self) -> float:
        """Get total value of all positions
        
        Returns:
            Total market value of all positions
        """
        total_value = 0.0
        
        for symbol in self.positions:
            total_value += self.get_position_value(symbol)
        
        return total_value
    
    def get_total_value(self) -> float:
        """Get total portfolio value (cash + positions)
        
        Returns:
            Total portfolio value
        """
        return self.cash + self.get_total_positions_value()
    
    def get_total_pnl(self) -> float:
        """Get total unrealized P&L
        
        Returns:
            Total unrealized P&L
        """
        total_pnl = 0.0
        
        for symbol in self.positions:
            total_pnl += self.get_position_pnl(symbol)
        
        return total_pnl
    
    def get_portfolio_summary(self) -> Dict[str, float]:
        """Get portfolio summary
        
        Returns:
            Dictionary with portfolio summary
        """
        total_value = self.get_total_value()
        positions_value = self.get_total_positions_value()
        total_pnl = self.get_total_pnl()
        
        return {
            'cash': self.cash,
            'positions_value': positions_value,
            'total_value': total_value,
            'total_pnl': total_pnl,
            'total_return': (total_value - self.initial_cash) / self.initial_cash,
            'cash_percentage': (self.cash / total_value) * 100 if total_value > 0 else 100,
            'positions_percentage': (positions_value / total_value) * 100 if total_value > 0 else 0
        }