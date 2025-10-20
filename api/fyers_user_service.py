"""
Fyers User Credentials Service
============================

Manages individual user Fyers API credentials for the trading platform.
Each user can configure their own Fyers APP credentials independently.
"""

from typing import Optional, Dict, Any, List
import json
import hashlib
import logging
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import os

logger = logging.getLogger(__name__)

class FyersCredentials(BaseModel):
    """Individual user's Fyers API credentials"""
    user_id: str = Field(..., description="User identifier")
    client_id: str = Field(..., description="Fyers Client ID (APP ID)")
    secret_key: str = Field(..., description="Fyers Secret Key")
    redirect_uri: str = Field(default="https://www.google.com", description="OAuth redirect URI")
    user_name: str = Field(..., description="Fyers username/user ID")
    totp_key: Optional[str] = Field(None, description="TOTP secret key for 2FA")
    pin: str = Field(..., description="4-digit trading PIN")
    access_token: Optional[str] = Field(None, description="Generated access token")
    token_expires: Optional[datetime] = Field(None, description="Token expiry timestamp")
    is_active: bool = Field(default=True, description="Whether credentials are active")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class FyersTokenRequest(BaseModel):
    """Request to generate/refresh Fyers token"""
    user_id: str
    client_id: str
    secret_key: str
    user_name: str
    pin: str
    totp_key: Optional[str] = None

class FyersConnectionStatus(BaseModel):
    """Fyers connection status response"""
    user_id: str
    is_connected: bool
    has_credentials: bool
    token_valid: bool
    token_expires: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    error_message: Optional[str] = None

class FyersUserService:
    """Service for managing individual user Fyers credentials"""
    
    def __init__(self, credentials_file: str = "data/fyers_users.json"):
        self.credentials_file = credentials_file
        self.credentials_cache: Dict[str, FyersCredentials] = {}
        self._ensure_data_directory()
        self._load_credentials()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.credentials_file), exist_ok=True)
    
    def _load_credentials(self):
        """Load all user credentials from file"""
        try:
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    data = json.load(f)
                    for user_id, cred_data in data.items():
                        self.credentials_cache[user_id] = FyersCredentials(**cred_data)
                logger.info(f"Loaded {len(self.credentials_cache)} Fyers user credentials")
            else:
                logger.info("No existing Fyers credentials file found - starting fresh")
        except Exception as e:
            logger.error(f"Failed to load Fyers credentials: {e}")
            self.credentials_cache = {}
    
    def _save_credentials(self):
        """Save all credentials to file"""
        try:
            data = {}
            for user_id, credentials in self.credentials_cache.items():
                data[user_id] = credentials.dict()
            
            with open(self.credentials_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info("Saved Fyers user credentials")
        except Exception as e:
            logger.error(f"Failed to save Fyers credentials: {e}")
            raise
    
    def add_user_credentials(self, credentials: FyersCredentials) -> bool:
        """Add or update user credentials"""
        try:
            credentials.updated_at = datetime.now()
            self.credentials_cache[credentials.user_id] = credentials
            self._save_credentials()
            logger.info(f"Added/updated Fyers credentials for user: {credentials.user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add user credentials: {e}")
            return False
    
    def get_user_credentials(self, user_id: str) -> Optional[FyersCredentials]:
        """Get credentials for a specific user"""
        return self.credentials_cache.get(user_id)
    
    def remove_user_credentials(self, user_id: str) -> bool:
        """Remove user credentials"""
        try:
            if user_id in self.credentials_cache:
                del self.credentials_cache[user_id]
                self._save_credentials()
                logger.info(f"Removed Fyers credentials for user: {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove user credentials: {e}")
            return False
    
    def list_users(self) -> List[str]:
        """List all users with Fyers credentials"""
        return list(self.credentials_cache.keys())
    
    def get_connection_status(self, user_id: str) -> FyersConnectionStatus:
        """Get connection status for a user"""
        credentials = self.get_user_credentials(user_id)
        
        if not credentials:
            return FyersConnectionStatus(
                user_id=user_id,
                is_connected=False,
                has_credentials=False,
                token_valid=False,
                error_message="No credentials found"
            )
        
        # Check if token is valid and not expired
        token_valid = bool(
            credentials.access_token and 
            credentials.token_expires and 
            credentials.token_expires > datetime.now()
        )
        
        return FyersConnectionStatus(
            user_id=user_id,
            is_connected=token_valid,
            has_credentials=True,
            token_valid=token_valid,
            token_expires=credentials.token_expires,
            last_updated=credentials.updated_at
        )
    
    def update_access_token(self, user_id: str, access_token: str, expires_in_hours: int = 24) -> bool:
        """Update access token for a user"""
        try:
            credentials = self.get_user_credentials(user_id)
            if not credentials:
                logger.error(f"No credentials found for user: {user_id}")
                return False
            
            credentials.access_token = access_token
            credentials.token_expires = datetime.now() + timedelta(hours=expires_in_hours)
            credentials.updated_at = datetime.now()
            
            self.credentials_cache[user_id] = credentials
            self._save_credentials()
            
            logger.info(f"Updated access token for user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to update access token: {e}")
            return False
    
    def validate_credentials(self, credentials: FyersCredentials) -> Dict[str, Any]:
        """Validate Fyers credentials format"""
        errors = []
        
        # Validate client_id format (should be like "XA12345-100")
        if not credentials.client_id or '-' not in credentials.client_id:
            errors.append("Invalid client_id format. Should be like 'XA12345-100'")
        
        # Validate PIN (should be 4 digits)
        if not credentials.pin or len(credentials.pin) != 4 or not credentials.pin.isdigit():
            errors.append("PIN must be exactly 4 digits")
        
        # Validate user_name (Fyers user ID)
        if not credentials.user_name or len(credentials.user_name) < 6:
            errors.append("Invalid Fyers user name")
        
        # Validate secret_key
        if not credentials.secret_key or len(credentials.secret_key) < 10:
            errors.append("Invalid secret key")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def test_connection(self, user_id: str) -> Dict[str, Any]:
        """Test connection for a user (mock implementation)"""
        credentials = self.get_user_credentials(user_id)
        
        if not credentials:
            return {
                "success": False,
                "message": "No credentials found",
                "user_id": user_id
            }
        
        # In a real implementation, this would test the actual Fyers API connection
        # For now, we'll do basic validation
        validation = self.validate_credentials(credentials)
        
        if not validation["valid"]:
            return {
                "success": False,
                "message": f"Invalid credentials: {', '.join(validation['errors'])}",
                "user_id": user_id
            }
        
        return {
            "success": True,
            "message": "Credentials validated successfully",
            "user_id": user_id,
            "has_token": bool(credentials.access_token),
            "token_valid": bool(
                credentials.access_token and 
                credentials.token_expires and 
                credentials.token_expires > datetime.now()
            )
        }

# Global service instance
fyers_user_service = FyersUserService()