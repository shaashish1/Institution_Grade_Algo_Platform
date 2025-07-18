"""
Authentication Provider
======================

Handles user authentication including Gmail OAuth integration.
"""

import json
import secrets
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from urllib.parse import urlencode
import webbrowser

from ..utils.logger import TestLogger


class AuthProvider:
    """Handles user authentication and OAuth integration"""
    
    def __init__(self):
        self.logger = TestLogger()
        self.sessions = {}  # In-memory session storage
        self.session_timeout = timedelta(hours=24)
    
    def create_session(self, user_id: str) -> str:
        """
        Create a new user session
        
        Args:
            user_id: User ID
            
        Returns:
            Session token
        """
        session_token = secrets.token_urlsafe(32)
        
        self.sessions[session_token] = {
            "user_id": user_id,
            "created_at": datetime.now(),
            "last_accessed": datetime.now(),
            "expires_at": datetime.now() + self.session_timeout
        }
        
        self.logger.info(f"Created session for user: {user_id}")
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[str]:
        """
        Validate session token and return user ID
        
        Args:
            session_token: Session token to validate
            
        Returns:
            User ID if session is valid, None otherwise
        """
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        
        # Check if session has expired
        if datetime.now() > session["expires_at"]:
            del self.sessions[session_token]
            return None
        
        # Update last accessed time
        session["last_accessed"] = datetime.now()
        
        return session["user_id"]
    
    def revoke_session(self, session_token: str) -> bool:
        """
        Revoke a session token
        
        Args:
            session_token: Session token to revoke
            
        Returns:
            True if session was revoked, False if not found
        """
        if session_token in self.sessions:
            del self.sessions[session_token]
            self.logger.info("Session revoked")
            return True
        
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions
        
        Returns:
            Number of sessions cleaned up
        """
        now = datetime.now()
        expired_tokens = [
            token for token, session in self.sessions.items()
            if now > session["expires_at"]
        ]
        
        for token in expired_tokens:
            del self.sessions[token]
        
        if expired_tokens:
            self.logger.info(f"Cleaned up {len(expired_tokens)} expired sessions")
        
        return len(expired_tokens)
    
    def get_session_info(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        Get session information
        
        Args:
            session_token: Session token
            
        Returns:
            Session information dictionary
        """
        if session_token not in self.sessions:
            return None
        
        session = self.sessions[session_token]
        
        return {
            "user_id": session["user_id"],
            "created_at": session["created_at"].isoformat(),
            "last_accessed": session["last_accessed"].isoformat(),
            "expires_at": session["expires_at"].isoformat(),
            "time_remaining": str(session["expires_at"] - datetime.now())
        }
    
    def initiate_gmail_oauth(self, client_id: str, redirect_uri: str) -> str:
        """
        Initiate Gmail OAuth flow
        
        Args:
            client_id: Google OAuth client ID
            redirect_uri: Redirect URI for OAuth callback
            
        Returns:
            OAuth authorization URL
        """
        # OAuth parameters
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": "openid email profile",
            "response_type": "code",
            "access_type": "offline",
            "state": secrets.token_urlsafe(16)  # CSRF protection
        }
        
        # Build authorization URL
        auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
        
        self.logger.info("Initiated Gmail OAuth flow")
        return auth_url
    
    def open_gmail_oauth_in_browser(self, client_id: str, redirect_uri: str = "http://localhost:8080/callback") -> str:
        """
        Open Gmail OAuth in browser
        
        Args:
            client_id: Google OAuth client ID
            redirect_uri: Redirect URI for OAuth callback
            
        Returns:
            OAuth authorization URL
        """
        auth_url = self.initiate_gmail_oauth(client_id, redirect_uri)
        
        try:
            webbrowser.open(auth_url)
            self.logger.info("Opened OAuth URL in browser")
        except Exception as e:
            self.logger.warning(f"Could not open browser: {e}")
        
        return auth_url
    
    def handle_oauth_callback(self, authorization_code: str, client_id: str, client_secret: str, redirect_uri: str) -> Optional[Dict[str, Any]]:
        """
        Handle OAuth callback and exchange code for tokens
        
        Args:
            authorization_code: Authorization code from OAuth callback
            client_id: Google OAuth client ID
            client_secret: Google OAuth client secret
            redirect_uri: Redirect URI used in OAuth flow
            
        Returns:
            User information if successful, None otherwise
        """
        # This is a simplified implementation
        # In a real application, you would make HTTP requests to Google's token endpoint
        
        # For demonstration purposes, we'll simulate the OAuth flow
        self.logger.info("Processing OAuth callback")
        
        # Simulate token exchange (in real implementation, make HTTP request to Google)
        simulated_user_info = {
            "id": "google_user_123",
            "email": "user@gmail.com",
            "name": "Gmail User",
            "picture": "https://example.com/avatar.jpg",
            "verified_email": True
        }
        
        return simulated_user_info
    
    def create_oauth_user_session(self, oauth_user_info: Dict[str, Any]) -> str:
        """
        Create session for OAuth authenticated user
        
        Args:
            oauth_user_info: User information from OAuth provider
            
        Returns:
            Session token
        """
        # Generate user ID from OAuth info
        user_id = f"oauth_{oauth_user_info.get('id', 'unknown')}"
        
        return self.create_session(user_id)
    
    def generate_api_key(self, user_id: str) -> str:
        """
        Generate API key for programmatic access
        
        Args:
            user_id: User ID
            
        Returns:
            API key
        """
        # Create API key with user ID embedded
        key_data = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "type": "api_key"
        }
        
        # Encode key data
        key_json = json.dumps(key_data)
        api_key = base64.b64encode(key_json.encode()).decode()
        
        self.logger.info(f"Generated API key for user: {user_id}")
        return f"cst_{api_key}"
    
    def validate_api_key(self, api_key: str) -> Optional[str]:
        """
        Validate API key and return user ID
        
        Args:
            api_key: API key to validate
            
        Returns:
            User ID if valid, None otherwise
        """
        try:
            if not api_key.startswith("cst_"):
                return None
            
            # Decode key data
            encoded_data = api_key[4:]  # Remove "cst_" prefix
            key_json = base64.b64decode(encoded_data).decode()
            key_data = json.loads(key_json)
            
            return key_data.get("user_id")
            
        except Exception as e:
            self.logger.warning(f"Invalid API key: {e}")
            return None
    
    def get_active_sessions_count(self) -> int:
        """
        Get count of active sessions
        
        Returns:
            Number of active sessions
        """
        now = datetime.now()
        active_sessions = [
            session for session in self.sessions.values()
            if now <= session["expires_at"]
        ]
        
        return len(active_sessions)
    
    def get_auth_statistics(self) -> Dict[str, Any]:
        """
        Get authentication statistics
        
        Returns:
            Authentication statistics
        """
        now = datetime.now()
        
        active_sessions = 0
        expired_sessions = 0
        
        for session in self.sessions.values():
            if now <= session["expires_at"]:
                active_sessions += 1
            else:
                expired_sessions += 1
        
        return {
            "active_sessions": active_sessions,
            "expired_sessions": expired_sessions,
            "total_sessions": len(self.sessions),
            "session_timeout_hours": self.session_timeout.total_seconds() / 3600
        }