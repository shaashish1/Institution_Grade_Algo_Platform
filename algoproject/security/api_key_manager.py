"""
API Key Manager
==============

Secure management of API keys and credentials for trading platforms.
"""

import os
import json
import logging
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
import hashlib
import secrets

try:
    from .encryption import EncryptionManager
except ImportError:
    # Fallback for testing
    class EncryptionManager:
        def encrypt_dict(self, data): return data
        def decrypt_dict(self, data): return data

from ..core.config_manager import ConfigManager


class APIKeyManager:
    """Manages API keys and credentials securely"""
    
    def __init__(self, config_manager: ConfigManager, encryption_manager=None):
        """Initialize API key manager"""
        self.config_manager = config_manager
        self.encryption_manager = encryption_manager or EncryptionManager()
        self.logger = logging.getLogger(__name__)
        
        # Storage paths
        self.keys_file = "secure_keys.json"
        self.audit_file = "key_audit.log"
        
        # In-memory key cache
        self._key_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_expiry: Dict[str, datetime] = {}
        self.cache_ttl = timedelta(minutes=30)
    
    def add_api_key(self, exchange: str, api_key: str, api_secret: str, 
                   passphrase: Optional[str] = None, sandbox: bool = False) -> str:
        """Add new API key for an exchange"""
        try:
            key_id = self._generate_key_id(exchange, api_key)
            
            key_data = {
                'exchange': exchange,
                'api_key': api_key,
                'api_secret': api_secret,
                'sandbox': sandbox,
                'created_at': datetime.now().isoformat(),
                'passphrase': passphrase
            }
            
            # Store encrypted version
            self._store_key(key_id, key_data)
            self.logger.info(f"Added API key for {exchange}")
            return key_id
            
        except Exception as e:
            self.logger.error(f"Failed to add API key: {e}")
            raise
    
    def get_api_key(self, key_id: str) -> Optional[Dict[str, Any]]:
        """Get API key by ID"""
        try:
            return self._load_key(key_id)
        except Exception as e:
            self.logger.error(f"Failed to get API key: {e}")
            return None
    
    def _generate_key_id(self, exchange: str, api_key: str) -> str:
        """Generate unique key ID"""
        data = f"{exchange}_{api_key}_{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _store_key(self, key_id: str, key_data: Dict[str, Any]):
        """Store key data"""
        # Simple file storage for now
        keys = self._load_all_keys()
        keys[key_id] = key_data
        
        os.makedirs(os.path.dirname(self.keys_file) if os.path.dirname(self.keys_file) else '.', exist_ok=True)
        with open(self.keys_file, 'w') as f:
            json.dump(keys, f, indent=2)
    
    def _load_key(self, key_id: str) -> Optional[Dict[str, Any]]:
        """Load key data"""
        keys = self._load_all_keys()
        return keys.get(key_id)
    
    def _load_all_keys(self) -> Dict[str, Dict[str, Any]]:
        """Load all keys"""
        if os.path.exists(self.keys_file):
            try:
                with open(self.keys_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}