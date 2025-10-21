#!/usr/bin/env python3
"""
Market Hours and Trading Session Utility
========================================

Handles NSE market hours, holidays, and trading session detection.
Ensures data is only fetched during active trading hours.
"""

from datetime import datetime, time, date
from typing import Dict, Any, Tuple, Optional
import pytz
import calendar

class NSEMarketHours:
    """NSE (National Stock Exchange) market hours and session management"""
    
    def __init__(self):
        self.timezone = pytz.timezone('Asia/Kolkata')
        
        # NSE Trading Hours (IST)
        self.market_open_time = time(9, 15)  # 9:15 AM
        self.market_close_time = time(15, 30)  # 3:30 PM
        self.pre_market_open = time(9, 0)  # 9:00 AM
        self.pre_market_close = time(9, 15)  # 9:15 AM
        self.after_market_open = time(15, 40)  # 3:40 PM
        self.after_market_close = time(16, 0)  # 4:00 PM
        
        # NSE Holidays 2025 (major ones)
        self.holidays_2025 = [
            date(2025, 1, 26),  # Republic Day
            date(2025, 3, 14),  # Holi
            date(2025, 3, 29),  # Good Friday
            date(2025, 4, 14),  # Ram Navami
            date(2025, 5, 1),   # Labour Day
            date(2025, 8, 15),  # Independence Day
            date(2025, 10, 2),  # Gandhi Jayanti
            date(2025, 10, 20), # Dussehra
            date(2025, 11, 1),  # Diwali Balipratipada
            date(2025, 11, 5),  # Diwali
            date(2025, 12, 25), # Christmas
        ]
    
    def get_current_ist_time(self) -> datetime:
        """Get current time in IST"""
        return datetime.now(self.timezone)
    
    def is_trading_day(self, check_date: Optional[date] = None) -> bool:
        """Check if given date is a trading day (not weekend/holiday)"""
        if check_date is None:
            check_date = self.get_current_ist_time().date()
        
        # Check if weekend (Saturday=5, Sunday=6)
        if check_date.weekday() > 4:
            return False
        
        # Check if holiday
        if check_date in self.holidays_2025:
            return False
        
        return True
    
    def is_market_open(self) -> bool:
        """Check if market is currently open for regular trading"""
        now = self.get_current_ist_time()
        
        # Check if trading day
        if not self.is_trading_day(now.date()):
            return False
        
        # Check if within trading hours
        current_time = now.time()
        return self.market_open_time <= current_time <= self.market_close_time
    
    def is_pre_market_open(self) -> bool:
        """Check if pre-market session is active"""
        now = self.get_current_ist_time()
        
        if not self.is_trading_day(now.date()):
            return False
        
        current_time = now.time()
        return self.pre_market_open <= current_time < self.pre_market_close
    
    def is_after_market_open(self) -> bool:
        """Check if after-market session is active"""
        now = self.get_current_ist_time()
        
        if not self.is_trading_day(now.date()):
            return False
        
        current_time = now.time()
        return self.after_market_open <= current_time <= self.after_market_close
    
    def get_market_status(self) -> Dict[str, Any]:
        """Get comprehensive market status"""
        now = self.get_current_ist_time()
        
        status = {
            "current_time": now.isoformat(),
            "is_trading_day": self.is_trading_day(),
            "is_market_open": self.is_market_open(),
            "is_pre_market": self.is_pre_market_open(),
            "is_after_market": self.is_after_market_open(),
            "session": "CLOSED"
        }
        
        if status["is_market_open"]:
            status["session"] = "REGULAR"
        elif status["is_pre_market"]:
            status["session"] = "PRE_MARKET"
        elif status["is_after_market"]:
            status["session"] = "AFTER_MARKET"
        
        # Add next market open time
        if not status["is_trading_day"]:
            status["next_trading_day"] = self._get_next_trading_day().isoformat()
        
        return status
    
    def _get_next_trading_day(self) -> date:
        """Find the next trading day"""
        check_date = self.get_current_ist_time().date()
        
        # Check next 10 days to find trading day
        for i in range(1, 11):
            next_date = date.fromordinal(check_date.toordinal() + i)
            if self.is_trading_day(next_date):
                return next_date
        
        # Fallback - should not reach here normally
        return check_date
    
    def should_fetch_live_data(self) -> bool:
        """Determine if live data should be fetched"""
        return self.is_market_open() or self.is_pre_market_open() or self.is_after_market_open()

# Global instance
market_hours = NSEMarketHours()

def get_market_status() -> Dict[str, Any]:
    """Get current market status - convenience function"""
    return market_hours.get_market_status()

def is_market_open() -> bool:
    """Check if market is open - convenience function"""
    return market_hours.is_market_open()

def should_fetch_live_data() -> bool:
    """Check if live data should be fetched - convenience function"""
    return market_hours.should_fetch_live_data()

if __name__ == "__main__":
    # Test the market hours functionality
    status = get_market_status()
    print("Market Status:", status)
    print("Should fetch live data:", should_fetch_live_data())