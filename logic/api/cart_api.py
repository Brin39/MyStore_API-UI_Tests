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
    
    def wait_for_item_quantity(self, product_id: str, expected_quantity: int, token: str, timeout: float = 2.5) -> int:
        """
        Wait for item quantity to match expected value in cart.
        Polls API until quantity matches or timeout is reached.
        
        Args:
            product_id: Product ID to check
            expected_quantity: Expected quantity value
            token: User authentication token
            timeout: Maximum time to wait in seconds (default 2.5 = 5 attempts * 0.5s)
        
        Returns:
            int: Actual quantity found in API (may not match expected if timeout)
        """
        import time
        max_attempts = int(timeout / 0.5) or 5
        api_quantity = None
        
        for _ in range(max_attempts):
            cart = self.get_cart(token)
            cart_items = cart.get("items", [])
            for item in cart_items:
                item_product_id = item.get("product", {}).get("_id") or item.get("productId")
                if item_product_id == product_id:
                    api_quantity = item.get("quantity", 0)
                    if api_quantity == expected_quantity:
                        return api_quantity
            time.sleep(0.5)
        
        # Final check if still None
        if api_quantity is None:
            cart = self.get_cart(token)
            cart_items = cart.get("items", [])
            for item in cart_items:
                item_product_id = item.get("product", {}).get("_id") or item.get("productId")
                if item_product_id == product_id:
                    api_quantity = item.get("quantity", 0)
                    break
        
        return api_quantity if api_quantity is not None else 0

