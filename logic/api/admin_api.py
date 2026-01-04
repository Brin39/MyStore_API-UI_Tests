"""
Admin API client for MyStore.
Handles admin operations for products, users, and orders.
"""

from typing import Dict, List
from infra.api_wrapper import ApiWrapper
from utils.constants import ApiEndpoints


class AdminApi:
    """Admin API operations"""
    
    def __init__(self, api: ApiWrapper = None):
        self.api = api or ApiWrapper()
    
    # ==================== PRODUCTS ====================
    
    def get_products(self, token: str) -> List[Dict]:
        """Get all products (admin)."""
        response = self.api.get(ApiEndpoints.ADMIN_PRODUCTS, token=token)
        response.raise_for_status()
        return response.json()
    
    def create_product(self, product_data: Dict, token: str) -> Dict:
        """
        Create a new product.
        
        Returns:
            dict with created product
        """
        response = self.api.post(
            ApiEndpoints.ADMIN_PRODUCTS,
            data=product_data,
            token=token
        )
        response.raise_for_status()
        return response.json()
    
    def update_product(self, product_id: str, product_data: Dict, token: str) -> Dict:
        """
        Update product.
        
        Returns:
            dict with updated product
        """
        endpoint = ApiEndpoints.ADMIN_PRODUCT.format(id=product_id)
        response = self.api.put(endpoint, data=product_data, token=token)
        response.raise_for_status()
        return response.json()
    
    def delete_product(self, product_id: str, token: str):
        """Delete product."""
        endpoint = ApiEndpoints.ADMIN_PRODUCT.format(id=product_id)
        response = self.api.delete(endpoint, token=token)
        response.raise_for_status()
    
    # ==================== USERS ====================
    
    def get_users(self, token: str) -> List[Dict]:
        """Get all users."""
        response = self.api.get(ApiEndpoints.ADMIN_USERS, token=token)
        response.raise_for_status()
        return response.json()
    
    def get_user_details(self, user_id: str, token: str) -> Dict:
        """Get user details."""
        endpoint = ApiEndpoints.ADMIN_USER_DETAILS.format(id=user_id)
        response = self.api.get(endpoint, token=token)
        response.raise_for_status()
        return response.json()
    
    def update_user(self, user_id: str, user_data: Dict, token: str) -> Dict:
        """Update user."""
        endpoint = ApiEndpoints.ADMIN_USER.format(id=user_id)
        response = self.api.put(endpoint, data=user_data, token=token)
        response.raise_for_status()
        return response.json()
    
    def delete_user(self, user_id: str, token: str):
        """Delete user."""
        endpoint = ApiEndpoints.ADMIN_USER.format(id=user_id)
        response = self.api.delete(endpoint, token=token)
        response.raise_for_status()
    
    # ==================== ORDERS ====================
    
    def get_orders(self, token: str) -> List[Dict]:
        """Get all orders."""
        response = self.api.get(ApiEndpoints.ADMIN_ORDERS, token=token)
        response.raise_for_status()
        return response.json()
    
    def update_order_status(self, order_id: str, status: str, token: str) -> Dict:
        """
        Update order status.
        
        Args:
            order_id: order ID
            status: new status (pending, processing, shipped, delivered, cancelled)
            token: admin token
        
        Returns:
            dict with updated order
        """
        endpoint = ApiEndpoints.ADMIN_ORDER.format(id=order_id)
        response = self.api.put(
            endpoint,
            data={"status": status},
            token=token
        )
        response.raise_for_status()
        return response.json()
    
    def delete_order(self, order_id: str, token: str):
        """Delete order."""
        endpoint = ApiEndpoints.ADMIN_ORDER.format(id=order_id)
        response = self.api.delete(endpoint, token=token)
        response.raise_for_status()

