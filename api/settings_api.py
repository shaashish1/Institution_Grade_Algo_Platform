"""
Settings API for AlgoProject
Handles user settings, preferences, and API key management with encryption
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import os
from pathlib import Path
from cryptography.fernet import Fernet
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/settings", tags=["settings"])

# Encryption key management
ENCRYPTION_KEY_FILE = Path(__file__).parent / "data" / ".encryption_key"
SETTINGS_FILE = Path(__file__).parent / "data" / "user_settings.json"
API_KEYS_FILE = Path(__file__).parent / "data" / "api_keys.encrypted"

# Ensure data directory exists
SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)

# Initialize or load encryption key
def get_encryption_key() -> bytes:
    """Get or create encryption key for API keys"""
    if ENCRYPTION_KEY_FILE.exists():
        with open(ENCRYPTION_KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_FILE, "wb") as f:
            f.write(key)
        logger.info("✅ Generated new encryption key")
        return key

# Initialize Fernet cipher
ENCRYPTION_KEY = get_encryption_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# Data Models
class ProfileSettings(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=50)
    lastName: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')
    timezone: str = "Asia/Kolkata"
    language: str = "English"
    dateFormat: str = "DD/MM/YYYY"
    currency: str = "INR"

class NotificationSetting(BaseModel):
    id: str
    name: str
    description: str
    enabled: bool
    type: str  # email, push, sms

class TradingPreferences(BaseModel):
    defaultOrderType: str = "LIMIT"
    defaultQuantity: int = Field(default=1, gt=0)
    confirmBeforeOrder: bool = True
    showAdvancedOptions: bool = False
    autoSquareOff: bool = True
    riskWarnings: bool = True
    maxPositionSize: int = Field(default=100000, gt=0)
    stopLossDefault: float = Field(default=5.0, ge=0, le=100)

class AppearanceSettings(BaseModel):
    theme: str = "dark"  # dark, light, auto
    colorScheme: str = "blue"  # blue, purple, green
    fontSize: str = "medium"  # small, medium, large
    compactMode: bool = False
    animations: bool = True
    highContrast: bool = False

class UserSettings(BaseModel):
    profile: ProfileSettings
    notifications: List[NotificationSetting]
    trading: TradingPreferences
    appearance: AppearanceSettings
    lastUpdated: datetime = Field(default_factory=datetime.now)

class APIKeyData(BaseModel):
    provider: str  # fyers, binance, kraken, etc.
    apiKey: str
    apiSecret: str
    extraFields: Optional[Dict[str, str]] = None  # For additional fields like client_id

class APIKeyRequest(BaseModel):
    provider: str
    apiKey: str
    apiSecret: str
    extraFields: Optional[Dict[str, str]] = None

class APIKeyResponse(BaseModel):
    provider: str
    apiKeyMasked: str
    hasSecret: bool
    createdAt: datetime
    extraFields: Optional[List[str]] = None  # List of extra field names (not values)

# Helper Functions
def load_settings() -> Dict[str, Any]:
    """Load user settings from file"""
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_settings(settings: Dict[str, Any]) -> None:
    """Save user settings to file"""
    settings['lastUpdated'] = datetime.now().isoformat()
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2, default=str)
    logger.info("✅ Settings saved successfully")

def encrypt_api_key(data: APIKeyData) -> str:
    """Encrypt API key data"""
    json_data = json.dumps(data.dict(), default=str)
    encrypted = cipher_suite.encrypt(json_data.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_api_key(encrypted_data: str) -> APIKeyData:
    """Decrypt API key data"""
    decoded = base64.b64decode(encrypted_data.encode())
    decrypted = cipher_suite.decrypt(decoded)
    data_dict = json.loads(decrypted.decode())
    return APIKeyData(**data_dict)

def mask_api_key(key: str) -> str:
    """Mask API key for display (show first 4 and last 4 characters)"""
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"

def load_api_keys() -> Dict[str, str]:
    """Load encrypted API keys from file"""
    if API_KEYS_FILE.exists():
        with open(API_KEYS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_api_keys(keys: Dict[str, str]) -> None:
    """Save encrypted API keys to file"""
    with open(API_KEYS_FILE, "w") as f:
        json.dump(keys, f, indent=2)
    logger.info("✅ API keys saved successfully")

# API Endpoints

@router.get("/", response_model=Dict[str, Any])
async def get_settings():
    """Get all user settings"""
    try:
        settings = load_settings()
        if not settings:
            # Return default settings
            return {
                "profile": {
                    "firstName": "User",
                    "lastName": "Trader",
                    "email": "user@example.com",
                    "phone": "+91 00000 00000",
                    "timezone": "Asia/Kolkata",
                    "language": "English",
                    "dateFormat": "DD/MM/YYYY",
                    "currency": "INR"
                },
                "notifications": [],
                "trading": {
                    "defaultOrderType": "LIMIT",
                    "defaultQuantity": 1,
                    "confirmBeforeOrder": True,
                    "showAdvancedOptions": False,
                    "autoSquareOff": True,
                    "riskWarnings": True,
                    "maxPositionSize": 100000,
                    "stopLossDefault": 5.0
                },
                "appearance": {
                    "theme": "dark",
                    "colorScheme": "blue",
                    "fontSize": "medium",
                    "compactMode": False,
                    "animations": True,
                    "highContrast": False
                },
                "lastUpdated": datetime.now().isoformat()
            }
        return settings
    except Exception as e:
        logger.error(f"❌ Error loading settings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load settings: {str(e)}")

@router.post("/", response_model=Dict[str, Any])
async def update_settings(settings: UserSettings):
    """Update user settings"""
    try:
        settings_dict = settings.dict()
        save_settings(settings_dict)
        return {
            "success": True,
            "message": "Settings updated successfully",
            "settings": settings_dict
        }
    except Exception as e:
        logger.error(f"❌ Error updating settings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")

@router.get("/profile", response_model=Dict[str, Any])
async def get_profile():
    """Get profile settings"""
    try:
        settings = load_settings()
        return settings.get("profile", {})
    except Exception as e:
        logger.error(f"❌ Error loading profile: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load profile: {str(e)}")

@router.post("/profile", response_model=Dict[str, Any])
async def update_profile(profile: ProfileSettings):
    """Update profile settings"""
    try:
        settings = load_settings()
        settings["profile"] = profile.dict()
        save_settings(settings)
        return {
            "success": True,
            "message": "Profile updated successfully",
            "profile": profile.dict()
        }
    except Exception as e:
        logger.error(f"❌ Error updating profile: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")

@router.get("/api-keys", response_model=List[APIKeyResponse])
async def get_api_keys():
    """Get list of configured API keys (masked)"""
    try:
        encrypted_keys = load_api_keys()
        response = []
        
        for provider, encrypted_data in encrypted_keys.items():
            try:
                key_data = decrypt_api_key(encrypted_data)
                response.append(APIKeyResponse(
                    provider=key_data.provider,
                    apiKeyMasked=mask_api_key(key_data.apiKey),
                    hasSecret=bool(key_data.apiSecret),
                    createdAt=datetime.now(),
                    extraFields=list(key_data.extraFields.keys()) if key_data.extraFields else None
                ))
            except Exception as e:
                logger.error(f"❌ Error decrypting key for {provider}: {e}")
                continue
        
        return response
    except Exception as e:
        logger.error(f"❌ Error loading API keys: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load API keys: {str(e)}")

@router.post("/api-keys", response_model=Dict[str, Any])
async def add_api_key(key_request: APIKeyRequest):
    """Add or update API key for a provider (encrypted)"""
    try:
        # Create API key data object
        key_data = APIKeyData(
            provider=key_request.provider,
            apiKey=key_request.apiKey,
            apiSecret=key_request.apiSecret,
            extraFields=key_request.extraFields
        )
        
        # Encrypt the data
        encrypted_data = encrypt_api_key(key_data)
        
        # Load existing keys
        api_keys = load_api_keys()
        
        # Add/update the key
        api_keys[key_request.provider] = encrypted_data
        
        # Save to file
        save_api_keys(api_keys)
        
        return {
            "success": True,
            "message": f"API key for {key_request.provider} saved successfully",
            "provider": key_request.provider,
            "apiKeyMasked": mask_api_key(key_request.apiKey)
        }
    except Exception as e:
        logger.error(f"❌ Error saving API key: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save API key: {str(e)}")

@router.delete("/api-keys/{provider}", response_model=Dict[str, Any])
async def delete_api_key(provider: str):
    """Delete API key for a provider"""
    try:
        api_keys = load_api_keys()
        
        if provider not in api_keys:
            raise HTTPException(status_code=404, detail=f"API key for {provider} not found")
        
        del api_keys[provider]
        save_api_keys(api_keys)
        
        return {
            "success": True,
            "message": f"API key for {provider} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting API key: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete API key: {str(e)}")

@router.get("/api-keys/{provider}", response_model=Dict[str, Any])
async def get_api_key_decrypted(provider: str):
    """
    Get decrypted API key for a specific provider
    WARNING: Use with caution - returns unencrypted credentials
    """
    try:
        api_keys = load_api_keys()
        
        if provider not in api_keys:
            raise HTTPException(status_code=404, detail=f"API key for {provider} not found")
        
        # Decrypt the key
        key_data = decrypt_api_key(api_keys[provider])
        
        return {
            "provider": key_data.provider,
            "apiKey": key_data.apiKey,
            "apiSecret": key_data.apiSecret,
            "extraFields": key_data.extraFields
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error retrieving API key: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve API key: {str(e)}")

@router.get("/health", response_model=Dict[str, Any])
async def settings_health():
    """Health check endpoint for settings service"""
    return {
        "status": "healthy",
        "service": "settings",
        "timestamp": datetime.now().isoformat(),
        "encryptionEnabled": True,
        "settingsFile": str(SETTINGS_FILE),
        "apiKeysFile": str(API_KEYS_FILE)
    }

# Export router for main app
__all__ = ["router"]
