"""
Cart API client for MyStore.
Handles shopping cart operations.
"""

from typing import Dict, List
from infra.api_wrapper import ApiWrapper
from utils.constants import ApiEndpoints


class CartApi:
    """Cart API operations"""
    
    def __init__(self, api: ApiWrapper = None):
        self.api = api or ApiWrapper()
    
    def get_cart(self, token: str) -> Dict:
        """
        Get user's cart.
        
        Returns:
            dict with cart items
        """
        response = self.api.get(ApiEndpoints.CART, token=token)
        response.raise_for_status()
        return response.json()
    
    def add_to_cart(self, product_id: str, quantity: int, token: str) -> Dict:
        """
        Add product to cart.
        
        Returns:
            dict with updated cart
        """
        response = self.api.post(
            ApiEndpoints.CART,
            data={
                "productId": product_id,
                "quantity": quantity
            },
            token=token
        )
        response.raise_for_status()
        return response.json()
    
    def update_quantity(self, product_id: str, quantity: int, token: str) -> Dict:
        """
        Update product quantity in cart.
        
        Returns:
            dict with updated cart
        """
        endpoint = ApiEndpoints.CART_UPDATE.format(product_id=product_id)
        response = self.api.put(
            endpoint,
            data={"quantity": quantity},
            token=token
        )
        response.raise_for_status()
        return response.json()
    
    def remove_from_cart(self, product_id: str, token: str) -> Dict:
        """
        Remove product from cart.
        
        Returns:
            dict with updated cart
        """
        endpoint = ApiEndpoints.CART_REMOVE.format(product_id=product_id)
        response = self.api.delete(endpoint, token=token)
        response.raise_for_status()
        return response.json()
    
    def clear_cart(self, token: str):
        """Clear all items from cart."""
        try:
            response = self.api.delete(ApiEndpoints.CART_CLEAR, token=token)
            # Don't raise for empty cart
        except Exception:
            pass
    
    def get_cart_items_count(self, token: str) -> int:
        """
        Get number of items in cart.
        
        Returns:
            int count of cart items
        """
        cart = self.get_cart(token)
        items = cart.get("items", [])
        return len(items)

