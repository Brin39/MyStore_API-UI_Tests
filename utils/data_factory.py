"""
Data Factory - generates unique test data.
Ensures test isolation with unique identifiers.
"""

import uuid
import time
from typing import Dict, Optional


class DataFactory:
    """Factory for generating unique test data"""
    
    @staticmethod
    def unique_id() -> str:
        """Generate unique identifier"""
        timestamp = int(time.time() * 1000)
        random_part = uuid.uuid4().hex[:6]
        return f"{timestamp}_{random_part}"
    
    @classmethod
    def user(
        cls,
        name: str = None,
        email: str = None,
        password: str = "TestPass123",
        role: str = "user"
    ) -> Dict:
        """
        Generate unique user data.
        
        Returns:
            dict with name, email, password, role
        """
        uid = cls.unique_id()
        return {
            "name": name or f"Test User {uid}",
            "email": email or f"testuser_{uid}@test.com",
            "password": password,
            "role": role
        }
    
    @classmethod
    def admin(
        cls,
        name: str = None,
        email: str = None,
        password: str = "AdminPass123",
        admin_code: str = None
    ) -> Dict:
        """
        Generate unique admin user data.
        
        Returns:
            dict with name, email, password, role, adminCode
        """
        uid = cls.unique_id()
        return {
            "name": name or f"Test Admin {uid}",
            "email": email or f"testadmin_{uid}@test.com",
            "password": password,
            "role": "admin",
            "adminCode": admin_code or ""
        }
    
    @classmethod
    def product(
        cls,
        name: str = None,
        description: str = None,
        price: float = 99.99,
        stock: int = 100,
        category: str = "Electronics",
        best_offer: bool = False,
        images: list = None
    ) -> Dict:
        """
        Generate unique product data.
        
        Returns:
            dict with product fields
        """
        uid = cls.unique_id()
        return {
            "name": name or f"Test Product {uid}",
            "description": description or f"Description for test product {uid}",
            "price": price,
            "stock": stock,
            "category": category,
            "bestOffer": best_offer,
            "images": images or ["https://via.placeholder.com/300"]
        }
    
    @classmethod
    def order(
        cls,
        address: str = None,
        city: str = None,
        postal_code: str = None,
        country: str = None
    ) -> Dict:
        """
        Generate order shipping data.
        
        Returns:
            dict with shippingAddress
        """
        return {
            "shippingAddress": {
                "address": address or "123 Test Street",
                "city": city or "Test City",
                "postalCode": postal_code or "12345",
                "country": country or "Test Country"
            }
        }
    
    @classmethod
    def profile_update(
        cls,
        name: str = None,
        email: str = None,
        phone: str = None,
        address: str = None
    ) -> Dict:
        """
        Generate profile update data.
        
        Returns:
            dict with profile fields (only provided ones)
        """
        data = {}
        if name:
            data["name"] = name
        if email:
            data["email"] = email
        if phone:
            data["phone"] = phone
        if address:
            data["address"] = address
        return data

