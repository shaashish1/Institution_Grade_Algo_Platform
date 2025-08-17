"""
Cache Manager
=============

Manages data caching for AlgoProject.
"""

import pandas as pd
import pickle
import hashlib
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import os


class CacheManager:
    """Manages data caching"""
    
    def __init__(self, cache_dir: str = "cache", ttl: int = 3600):
        """Initialize cache manager
        
        Args:
            cache_dir: Directory to store cache files
            ttl: Default time-to-live in seconds
        """
        self.cache_dir = cache_dir
        self.default_ttl = ttl
        self.logger = logging.getLogger(__name__)
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached item or None if not found or expired
        """
        # Check memory cache first
        if key in self.memory_cache:
            cache_item = self.memory_cache[key]
            if cache_item['expires_at'] > datetime.now():
                return cache_item['data']
            else:
                del self.memory_cache[key]
        
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set item in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        ttl = ttl or self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        cache_item = {
            'data': value,
            'expires_at': expires_at,
            'created_at': datetime.now()
        }
        
        self.memory_cache[key] = cache_item