"""
User Management Module
=====================

User profiles, authentication, and preferences management.
"""

from .user_manager import UserManager
from .auth_provider import AuthProvider

__all__ = ['UserManager', 'AuthProvider']