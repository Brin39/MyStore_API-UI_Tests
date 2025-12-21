"""
Authentication API client for MyStore.
Handles user registration, login, and profile operations.
"""

from typing import Dict, Optional
from infra.api_wrapper import ApiWrapper
from utils.constants import ApiEndpoints


class AuthApi:
    """Authentication API operations"""
    
    def __init__(self, api: ApiWrapper = None):
        self.api = api or ApiWrapper()
    
    def register(
        self,
        name: str,
        email: str,
        password: str,
        role: str = "user"
    ) -> Dict:
        """
        Register a new user.
        
        Returns:
            dict with user data and token
        
        Raises:
            Exception if registration fails
        """
        response = self.api.post(
            ApiEndpoints.REGISTER,
            data={
                "name": name,
                "email": email,
                "password": password,
                "role": role
            }
        )
        response.raise_for_status()
        return response.json()
    
    def register_admin(
        self,
        name: str,
        email: str,
        password: str,
        admin_code: str
    ) -> Dict:
        """
        Register a new admin user.
        
        Returns:
            dict with user data and token
        """
        response = self.api.post(
            ApiEndpoints.ADMIN_REGISTER,
            data={
                "name": name,
                "email": email,
                "password": password,
                "adminCode": admin_code
            }
        )
        response.raise_for_status()
        return response.json()
    
    def login(self, email: str, password: str) -> Dict:
        """
        Login user.
        
        Returns:
            dict with user data and token
        """
        response = self.api.post(
            ApiEndpoints.LOGIN,
            data={
                "email": email,
                "password": password
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_profile(self, token: str) -> Dict:
        """
        Get user profile.
        
        Returns:
            dict with user profile data
        """
        response = self.api.get(ApiEndpoints.PROFILE, token=token)
        response.raise_for_status()
        return response.json()
    
    def update_profile(self, token: str, data: Dict) -> Dict:
        """
        Update user profile.
        
        Returns:
            dict with updated profile data
        """
        response = self.api.put(ApiEndpoints.PROFILE, data=data, token=token)
        response.raise_for_status()
        return response.json()
    
    def login_or_none(self, email: str, password: str) -> Optional[Dict]:
        """
        Try to login, return None if fails.
        
        Returns:
            dict with user data or None
        """
        try:
            return self.login(email, password)
        except Exception:
            return None

