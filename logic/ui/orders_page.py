"""
Orders Page Object for MyStore.
"""

from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from logic.ui.base_page import BasePage
from utils.constants import Urls


class OrdersPage(BasePage):
    """User orders page interactions"""
    
    # Test IDs
    ORDERS_LIST = "orders-list"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to orders page"""
        self.navigate(Urls.ORDERS)
    
    def open_via_ui(self):
        """Navigate to orders page via UI click (preserves localStorage)"""
        import time
        # Wait for profile button to be visible and clickable, then click
        self.is_visible_by_testid("profile-button", timeout=10)
        self.click_by_testid("profile-button")
        time.sleep(0.5)
        
        # Wait for orders link to be visible and clickable, then click
        self.is_visible_by_testid("dashboard-my-orders", timeout=10)
        self.click_by_testid("dashboard-my-orders")
        time.sleep(1)
    
    # ==================== ORDERS STATE ====================
    
    def wait_for_orders_loaded(self):
        """Wait for orders to finish loading"""
        # Wait for loading to disappear or orders to appear
        self.is_visible_by_testid(self.ORDERS_LIST, timeout=10)
    
    def get_order_cards(self) -> List:
        """Get all order card elements"""
        return self.driver.find_elements(
            By.CSS_SELECTOR, '[data-testid^="order-card-"]'
        )
    
    def get_orders_count(self) -> int:
        """Get number of displayed orders"""
        return len(self.get_order_cards())
    
    # ==================== ORDER DETAILS ====================
    
    def get_order_status(self, order_id: str) -> str:
        """Get order status text"""
        return self.get_text_by_testid(f"order-status-{order_id}")
    
    def is_order_visible(self, order_id: str) -> bool:
        """Check if order card is visible"""
        return self.is_visible_by_testid(f"order-card-{order_id}", timeout=3)
    
    def is_on_orders_page(self) -> bool:
        """Check if on orders page"""
        return Urls.ORDERS in self.get_current_url()

