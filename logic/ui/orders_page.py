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
    NO_ORDERS_MESSAGE = "no-orders-message"
    LOADING_SPINNER = "loading-spinner"
    ERROR_MESSAGE = "error-message"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to orders page"""
        self.navigate(Urls.ORDERS)
    
    # ==================== ORDERS STATE ====================
    
    def has_no_orders(self) -> bool:
        """Check if no orders message is shown"""
        return self.is_visible_by_testid(self.NO_ORDERS_MESSAGE, timeout=3)
    
    def is_loading(self) -> bool:
        """Check if loading spinner is shown"""
        return self.is_visible_by_testid(self.LOADING_SPINNER, timeout=1)
    
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
    
    def get_order_total(self, order_id: str) -> str:
        """Get order total text"""
        return self.get_text_by_testid(f"order-total-{order_id}")
    
    def get_order_date(self, order_id: str) -> str:
        """Get order date text"""
        return self.get_text_by_testid(f"order-date-{order_id}")
    
    def is_order_visible(self, order_id: str) -> bool:
        """Check if order card is visible"""
        return self.is_visible_by_testid(f"order-card-{order_id}", timeout=3)
    
    def is_on_orders_page(self) -> bool:
        """Check if on orders page"""
        return Urls.ORDERS in self.get_current_url()

