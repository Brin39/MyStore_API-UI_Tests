"""
Orders API client for MyStore.
Handles order creation and retrieval.
"""

from typing import Dict, List
from infra.api_wrapper import ApiWrapper
from utils.constants import ApiEndpoints


class OrdersApi:
    """Orders API operations"""
    
    def __init__(self, api: ApiWrapper = None):
        self.api = api or ApiWrapper()
    
    def create_order(self, items: List[Dict], total_amount: float, token: str) -> Dict:
        """
        Create a new order.
        
        Args:
            items: list of {product, quantity}
            total_amount: order total
            token: auth token
        
        Returns:
            dict with created order
        """
        response = self.api.post(
            ApiEndpoints.ORDERS,
            data={
                "items": items,
                "totalAmount": total_amount
            },
            token=token
        )
        response.raise_for_status()
        return response.json()
    
    def get_my_orders(self, token: str) -> List[Dict]:
        """
        Get current user's orders.
        
        Returns:
            list of orders
        """
        response = self.api.get(ApiEndpoints.MY_ORDERS, token=token)
        response.raise_for_status()
        return response.json()
    
    def get_order_by_id(self, order_id: str, token: str) -> Dict:
        """
        Get order by ID.
        
        Returns:
            dict with order data
        """
        endpoint = ApiEndpoints.ORDER_BY_ID.format(id=order_id)
        response = self.api.get(endpoint, token=token)
        response.raise_for_status()
        return response.json()
    
    def get_orders_count(self, token: str) -> int:
        """
        Get count of user's orders.
        
        Returns:
            int count
        """
        orders = self.get_my_orders(token)
        return len(orders)

