"""
Cleanup utilities - manage test data cleanup.
Tracks created resources and cleans them up after tests.
"""

from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class CleanupManager:
    """
    Manages cleanup of test data.
    Registers resources during test and cleans them up after.
    """
    
    def __init__(self, admin_api=None, admin_token: str = None):
        self.admin_api = admin_api
        self.admin_token = admin_token
        
        self._users: List[str] = []
        self._products: List[str] = []
        self._orders: List[str] = []
    
    def set_admin_api(self, admin_api, admin_token: str):
        """Set admin API client for cleanup operations"""
        self.admin_api = admin_api
        self.admin_token = admin_token
    
    def register_user(self, user_id: str):
        """Register user for cleanup"""
        if user_id and user_id not in self._users:
            self._users.append(user_id)
            logger.debug(f"Registered user for cleanup: {user_id}")
    
    def register_product(self, product_id: str):
        """Register product for cleanup"""
        if product_id and product_id not in self._products:
            self._products.append(product_id)
            logger.debug(f"Registered product for cleanup: {product_id}")
    
    def register_order(self, order_id: str):
        """Register order for cleanup"""
        if order_id and order_id not in self._orders:
            self._orders.append(order_id)
            logger.debug(f"Registered order for cleanup: {order_id}")
    
    def cleanup_all(self):
        """Clean up all registered resources"""
        total_resources = len(self._users) + len(self._products) + len(self._orders)
        
        if not self.admin_api or not self.admin_token:
            logger.warning(
                f"Admin API not configured, skipping cleanup. "
                f"Resources not cleaned: {len(self._users)} users, "
                f"{len(self._products)} products, {len(self._orders)} orders"
            )
            return
        
        if total_resources == 0:
            logger.debug("No resources to clean up")
            return
        
        logger.debug(
            f"Starting cleanup: {len(self._users)} users, "
            f"{len(self._products)} products, {len(self._orders)} orders"
        )
        
        # Clean orders first (they may reference products/users)
        for order_id in self._orders:
            self._safe_delete_order(order_id)
        
        # Clean products
        for product_id in self._products:
            self._safe_delete_product(product_id)
        
        # Clean users last
        for user_id in self._users:
            self._safe_delete_user(user_id)
        
        # Clear lists
        self._orders.clear()
        self._products.clear()
        self._users.clear()
        
        logger.debug(f"Cleanup completed: {total_resources} resources cleaned")
    
    def _safe_delete_user(self, user_id: str):
        """Safely delete user, ignore errors"""
        try:
            self.admin_api.delete_user(user_id, self.admin_token)
            logger.debug(f"Deleted user: {user_id}")
        except Exception as e:
            logger.warning(f"Failed to delete user {user_id}: {e}")
    
    def _safe_delete_product(self, product_id: str):
        """Safely delete product, ignore errors"""
        try:
            self.admin_api.delete_product(product_id, self.admin_token)
            logger.debug(f"Deleted product: {product_id}")
        except Exception as e:
            logger.warning(f"Failed to delete product {product_id}: {e}")
    
    def _safe_delete_order(self, order_id: str):
        """Safely delete order, ignore errors"""
        try:
            self.admin_api.delete_order(order_id, self.admin_token)
            logger.debug(f"Deleted order: {order_id}")
        except Exception as e:
            logger.warning(f"Failed to delete order {order_id}: {e}")

