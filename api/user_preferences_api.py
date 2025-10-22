"""
User Preferences API
====================

Handles user preferences for:
- Market selection (NSE, Crypto)
- Trading mode (Backtest, Paper, Live)
- Persistence and synchronization

Endpoints:
- GET /api/user/preferences - Retrieve user preferences
- POST /api/user/preferences - Update user preferences
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
import json
import os

router = APIRouter(prefix="/api/user", tags=["User Preferences"])

# ===== TYPE DEFINITIONS =====

Market = Literal["NSE", "Crypto"]
TradingMode = Literal["Backtest", "Paper", "Live"]


class UserPreferences(BaseModel):
    """User preferences model"""
    market: Market = Field(default="NSE", description="Selected market")
    mode: TradingMode = Field(default="Paper", description="Selected trading mode")
    timestamp: datetime = Field(default_factory=datetime.now, description="Last updated timestamp")


class PreferencesUpdateRequest(BaseModel):
    """Request model for updating preferences"""
    market: Market
    mode: TradingMode
    timestamp: Optional[datetime] = None


# ===== STORAGE =====
# For now, we'll use a simple JSON file for persistence
# TODO: Replace with proper database when user authentication is implemented

PREFERENCES_FILE = "user_preferences.json"


def load_preferences() -> UserPreferences:
    """Load user preferences from file"""
    try:
        if os.path.exists(PREFERENCES_FILE):
            with open(PREFERENCES_FILE, 'r') as f:
                data = json.load(f)
                return UserPreferences(**data)
        else:
            # Return default preferences
            return UserPreferences()
    except Exception as e:
        print(f"⚠️ Error loading preferences: {e}")
        return UserPreferences()


def save_preferences(preferences: UserPreferences) -> bool:
    """Save user preferences to file"""
    try:
        with open(PREFERENCES_FILE, 'w') as f:
            json.dump(
                {
                    "market": preferences.market,
                    "mode": preferences.mode,
                    "timestamp": preferences.timestamp.isoformat() if isinstance(preferences.timestamp, datetime) else preferences.timestamp
                },
                f,
                indent=2
            )
        return True
    except Exception as e:
        print(f"❌ Error saving preferences: {e}")
        return False


# ===== ENDPOINTS =====

@router.get("/preferences", response_model=UserPreferences)
async def get_preferences():
    """
    Get user preferences
    
    Returns:
        UserPreferences: Current user preferences
    
    Example:
        GET /api/user/preferences
        
        Response:
        {
            "market": "NSE",
            "mode": "Paper",
            "timestamp": "2025-01-24T10:30:00"
        }
    """
    preferences = load_preferences()
    return preferences


@router.post("/preferences", response_model=UserPreferences)
async def update_preferences(request: PreferencesUpdateRequest):
    """
    Update user preferences
    
    Args:
        request: PreferencesUpdateRequest with market and mode
    
    Returns:
        UserPreferences: Updated preferences
    
    Raises:
        HTTPException: If update fails
    
    Example:
        POST /api/user/preferences
        {
            "market": "Crypto",
            "mode": "Live"
        }
        
        Response:
        {
            "market": "Crypto",
            "mode": "Live",
            "timestamp": "2025-01-24T10:31:00"
        }
    """
    try:
        # Create preferences object
        preferences = UserPreferences(
            market=request.market,
            mode=request.mode,
            timestamp=request.timestamp or datetime.now()
        )
        
        # Save to file
        if save_preferences(preferences):
            print(f"✅ Preferences updated: Market={preferences.market}, Mode={preferences.mode}")
            return preferences
        else:
            raise HTTPException(status_code=500, detail="Failed to save preferences")
            
    except Exception as e:
        print(f"❌ Error updating preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preferences/status")
async def get_preferences_status():
    """
    Get preferences sync status
    
    Returns:
        Status information about preferences storage
    
    Example:
        GET /api/user/preferences/status
        
        Response:
        {
            "storage": "file",
            "file_exists": true,
            "last_modified": "2025-01-24T10:31:00"
        }
    """
    try:
        file_exists = os.path.exists(PREFERENCES_FILE)
        last_modified = None
        
        if file_exists:
            last_modified = datetime.fromtimestamp(os.path.getmtime(PREFERENCES_FILE)).isoformat()
        
        return {
            "storage": "file",
            "storage_location": os.path.abspath(PREFERENCES_FILE),
            "file_exists": file_exists,
            "last_modified": last_modified,
            "status": "operational"
        }
    except Exception as e:
        return {
            "storage": "file",
            "status": "error",
            "error": str(e)
        }
