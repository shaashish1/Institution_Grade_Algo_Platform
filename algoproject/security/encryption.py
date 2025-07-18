"""
Encryption Manager
=================

Handles encryption and decryption of sensitive data like API keys.
"""

import os
import base64
import hashlib
import logging
from typing import Optional, Dict, Any
from datetime import datetime

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False


class EncryptionManager:
    """Manages encryption and decryption of sensitive data"""
    
    def __init__(self, master_key: Optional[str] = None):
        """Initialize encryption manager
        
        Args:
            master_key: Master key for encryption (generated if None)
        """
        self.logger = logging.getLogger(__name__)
        
        if not CRYPTOGRAPHY_AVAILABLE:
            self.logger.warning("Cryptography library not available. Using basic encoding.")
            self._use_encryption = False
        else:
            self._use_encryption = True
        
        if self._use_encryption:
            if master_key:
                self._master_key = master_key.encode()
            else:
                self._master_key = self._generate_master_key()
            
            self._fernet = self._create_fernet()
        else:
            self._master_key = None
            self._fernet = None
    
    def _generate_master_key(self) -> bytes:
        """Generate a master key for encryption"""
        # In production, this should be stored securely
        key_file = os.path.join(os.path.expanduser("~"), ".algoproject_key")
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            # Generate new key
            key = os.urandom(32)  # 256-bit key
            
            # Save key securely
            try:
                with open(key_file, 'wb') as f:
                    f.write(key)
                # Set restrictive permissions (Unix-like systems)
                if hasattr(os, 'chmod'):
                    os.chmod(key_file, 0o600)
            except Exception as e:
                self.logger.error(f"Could not save master key: {e}")
            
            return key
    
    def _create_fernet(self) -> 'Fernet':
        """Create Fernet cipher from master key"""
        if not self._use_encryption:
            return None
        
        # Derive key using PBKDF2
        salt = b'algoproject_salt'  # In production, use random salt per key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(self._master_key))
        return Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data
        
        Args:
            data: Data to encrypt
            
        Returns:
            Encrypted data as base64 string
        """
        if not self._use_encryption:
            # Fallback to basic base64 encoding
            return base64.b64encode(data.encode()).decode()
        
        try:
            encrypted_data = self._fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            self.logger.error(f"Encryption failed: {e}")
            raise
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data
        
        Args:
            encrypted_data: Encrypted data as base64 string
            
        Returns:
            Decrypted data
        """
        if not self._use_encryption:
            # Fallback to basic base64 decoding
            return base64.b64decode(encrypted_data.encode()).decode()
        
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self._fernet.decrypt(encrypted_bytes)
            return decrypted_data.decode()
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            raise
    
    def hash_data(self, data: str) -> str:
        """Create hash of data for verification
        
        Args:
            data: Data to hash
            
        Returns:
            SHA256 hash as hex string
        """
        return hashlib.sha256(data.encode()).hexdigest()
    
    def verify_hash(self, data: str, hash_value: str) -> bool:
        """Verify data against hash
        
        Args:
            data: Original data
            hash_value: Hash to verify against
            
        Returns:
            True if hash matches, False otherwise
        """
        return self.hash_data(data) == hash_value
    
    def generate_token(self, length: int = 32) -> str:
        """Generate secure random token
        
        Args:
            length: Token length in bytes
            
        Returns:
            Random token as hex string
        """
        return os.urandom(length).hex()
    
    def is_encryption_available(self) -> bool:
        """Check if encryption is available
        
        Returns:
            True if encryption is available, False otherwise
        """
        return self._use_encryption