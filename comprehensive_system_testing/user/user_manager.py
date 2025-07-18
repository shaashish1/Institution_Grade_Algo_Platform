"""
User Manager
===========

Manages user profiles, preferences, and session data.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

from ..core.models import UserProfile, TestConfiguration
from ..utils.file_utils import FileUtils
from ..utils.logger import TestLogger


class UserManager:
    """Manages user profiles and preferences"""
    
    def __init__(self, data_directory: str = "comprehensive_system_testing/user_data"):
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(parents=True, exist_ok=True)
        self.logger = TestLogger()
        self.current_user = None
    
    def create_user_profile(self, email: str, name: str, password: str) -> UserProfile:
        """
        Create a new user profile
        
        Args:
            email: User email address
            name: User display name
            password: User password (will be hashed)
            
        Returns:
            UserProfile object
        """
        # Generate user ID
        user_id = self._generate_user_id(email)
        
        # Check if user already exists
        if self._user_exists(user_id):
            raise ValueError(f"User with email {email} already exists")
        
        # Hash password
        password_hash = self._hash_password(password)
        
        # Create user profile
        profile = UserProfile(
            user_id=user_id,
            email=email,
            name=name,
            preferences=TestConfiguration(),  # Default preferences
            test_history=[],
            created_at=datetime.now()
        )
        
        # Save user data
        user_data = {
            "profile": profile.to_dict(),
            "password_hash": password_hash,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        self._save_user_data(user_id, user_data)
        
        self.logger.info(f"Created user profile for: {email}")
        return profile
    
    def authenticate_user(self, email: str, password: str) -> Optional[UserProfile]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            UserProfile if authentication successful, None otherwise
        """
        user_id = self._generate_user_id(email)
        
        if not self._user_exists(user_id):
            return None
        
        # Load user data
        user_data = self._load_user_data(user_id)
        if not user_data:
            return None
        
        # Verify password
        password_hash = self._hash_password(password)
        if user_data.get("password_hash") != password_hash:
            return None
        
        # Create profile from data
        profile_data = user_data.get("profile", {})
        profile = self._create_profile_from_data(profile_data)
        
        # Update last login
        profile.last_login = datetime.now()
        self._update_user_profile(profile)
        
        self.current_user = profile
        self.logger.info(f"User authenticated: {email}")
        return profile
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user profile by ID
        
        Args:
            user_id: User ID
            
        Returns:
            UserProfile if found, None otherwise
        """
        if not self._user_exists(user_id):
            return None
        
        user_data = self._load_user_data(user_id)
        if not user_data:
            return None
        
        profile_data = user_data.get("profile", {})
        return self._create_profile_from_data(profile_data)
    
    def update_user_preferences(self, user_id: str, preferences: TestConfiguration) -> bool:
        """
        Update user preferences
        
        Args:
            user_id: User ID
            preferences: New test configuration preferences
            
        Returns:
            True if successful, False otherwise
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return False
        
        profile.preferences = preferences
        return self._update_user_profile(profile)
    
    def add_test_result_to_history(self, user_id: str, test_result: Dict[str, Any]) -> bool:
        """
        Add test result to user's history
        
        Args:
            user_id: User ID
            test_result: Test result data
            
        Returns:
            True if successful, False otherwise
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return False
        
        # Add timestamp if not present
        if "timestamp" not in test_result:
            test_result["timestamp"] = datetime.now().isoformat()
        
        # Add to history (keep last 100 results)
        profile.test_history.append(test_result)
        profile.test_history = profile.test_history[-100:]
        
        return self._update_user_profile(profile)
    
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        Get user statistics
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with user statistics
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return {}
        
        # Calculate statistics from test history
        total_tests = len(profile.test_history)
        
        if total_tests == 0:
            return {
                "total_tests": 0,
                "average_score": 0,
                "last_test": None,
                "favorite_components": []
            }
        
        # Calculate average score
        scores = [result.get("system_health_score", 0) for result in profile.test_history if "system_health_score" in result]
        average_score = sum(scores) / len(scores) if scores else 0
        
        # Find most recent test
        last_test = max(profile.test_history, key=lambda x: x.get("timestamp", ""))
        
        # Find favorite components (most tested)
        component_counts = {}
        for result in profile.test_history:
            components = result.get("components_tested", [])
            for component in components:
                component_counts[component] = component_counts.get(component, 0) + 1
        
        favorite_components = sorted(component_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_tests": total_tests,
            "average_score": average_score,
            "last_test": last_test,
            "favorite_components": [comp for comp, count in favorite_components],
            "member_since": profile.created_at.isoformat(),
            "last_login": profile.last_login.isoformat() if profile.last_login else None
        }
    
    def export_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Export all user data for backup/portability
        
        Args:
            user_id: User ID
            
        Returns:
            Complete user data dictionary
        """
        if not self._user_exists(user_id):
            return None
        
        user_data = self._load_user_data(user_id)
        if not user_data:
            return None
        
        # Remove sensitive data from export
        export_data = user_data.copy()
        export_data.pop("password_hash", None)
        export_data["exported_at"] = datetime.now().isoformat()
        
        return export_data
    
    def import_user_data(self, user_data: Dict[str, Any], password: str) -> bool:
        """
        Import user data from backup
        
        Args:
            user_data: User data dictionary
            password: New password for the user
            
        Returns:
            True if successful, False otherwise
        """
        try:
            profile_data = user_data.get("profile", {})
            user_id = profile_data.get("user_id")
            
            if not user_id:
                return False
            
            # Add password hash
            user_data["password_hash"] = self._hash_password(password)
            user_data["imported_at"] = datetime.now().isoformat()
            user_data["last_updated"] = datetime.now().isoformat()
            
            # Save imported data
            self._save_user_data(user_id, user_data)
            
            self.logger.info(f"Imported user data for: {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import user data: {e}")
            return False
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete user profile and all associated data
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user_file = self.data_directory / f"{user_id}.json"
            
            if user_file.exists():
                user_file.unlink()
                self.logger.info(f"Deleted user: {user_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to delete user {user_id}: {e}")
            return False
    
    def list_users(self) -> List[Dict[str, Any]]:
        """
        List all users (admin function)
        
        Returns:
            List of user summary information
        """
        users = []
        
        for user_file in self.data_directory.glob("*.json"):
            try:
                user_data = self._load_user_data(user_file.stem)
                if user_data:
                    profile_data = user_data.get("profile", {})
                    users.append({
                        "user_id": profile_data.get("user_id"),
                        "email": profile_data.get("email"),
                        "name": profile_data.get("name"),
                        "created_at": profile_data.get("created_at"),
                        "last_login": profile_data.get("last_login"),
                        "test_count": len(profile_data.get("test_history", []))
                    })
            except Exception as e:
                self.logger.warning(f"Could not load user file {user_file}: {e}")
        
        return users
    
    def _generate_user_id(self, email: str) -> str:
        """Generate user ID from email"""
        return hashlib.sha256(email.lower().encode()).hexdigest()[:16]
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = "comprehensive_system_testing_salt"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _user_exists(self, user_id: str) -> bool:
        """Check if user exists"""
        user_file = self.data_directory / f"{user_id}.json"
        return user_file.exists()
    
    def _save_user_data(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """Save user data to file"""
        try:
            user_file = self.data_directory / f"{user_id}.json"
            
            with open(user_file, 'w') as f:
                json.dump(user_data, f, indent=2, default=str)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save user data for {user_id}: {e}")
            return False
    
    def _load_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Load user data from file"""
        try:
            user_file = self.data_directory / f"{user_id}.json"
            
            if not user_file.exists():
                return None
            
            with open(user_file, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f"Failed to load user data for {user_id}: {e}")
            return None
    
    def _update_user_profile(self, profile: UserProfile) -> bool:
        """Update user profile"""
        user_data = self._load_user_data(profile.user_id)
        if not user_data:
            return False
        
        user_data["profile"] = profile.to_dict()
        user_data["last_updated"] = datetime.now().isoformat()
        
        return self._save_user_data(profile.user_id, user_data)
    
    def _create_profile_from_data(self, profile_data: Dict[str, Any]) -> UserProfile:
        """Create UserProfile object from data dictionary"""
        # Parse dates
        created_at = datetime.fromisoformat(profile_data.get("created_at", datetime.now().isoformat()))
        last_login = None
        if profile_data.get("last_login"):
            last_login = datetime.fromisoformat(profile_data["last_login"])
        
        # Parse preferences
        preferences_data = profile_data.get("preferences", {})
        preferences = TestConfiguration(
            enabled_tests=preferences_data.get("enabled_tests", []),
            auto_fix_enabled=preferences_data.get("auto_fix_enabled", True),
            timeout_seconds=preferences_data.get("timeout_seconds", 300),
            parallel_execution=preferences_data.get("parallel_execution", True),
            report_formats=preferences_data.get("report_formats", ["html", "console"])
        )
        
        return UserProfile(
            user_id=profile_data.get("user_id", ""),
            email=profile_data.get("email", ""),
            name=profile_data.get("name", ""),
            preferences=preferences,
            test_history=profile_data.get("test_history", []),
            created_at=created_at,
            last_login=last_login
        )