"""
Admin Orders Page Object for MyStore.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from logic.ui.base_page import BasePage
from utils.constants import Urls


class AdminOrdersPage(BasePage):
    """Admin orders page interactions"""
    
    # Test IDs
    ORDERS_LIST = "admin-orders-list"
    SEARCH_INPUT = "admin-search-input"
    
    # Alert modal
    CONFIRM_BTN = "confirm-alert-btn"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to admin orders"""
        self.navigate(Urls.ADMIN_ORDERS)
    
    def get_orders_count(self) -> int:
        """Get number of displayed orders"""
        cards = self.driver.find_elements(
            By.CSS_SELECTOR, '[data-testid^="order-card-"]'
        )
        return len(cards)
    
    def is_order_visible(self, order_id: str) -> bool:
        """Check if order card is visible"""
        return self.is_visible_by_testid(f"order-card-{order_id}", timeout=3)
    
    def get_order_status(self, order_id: str) -> str:
        """Get order status"""
        return self.get_text_by_testid(f"order-status-{order_id}")
    
    def click_update_status(self, order_id: str):
        """Click update status button"""
        self.click_by_testid(f"order-{order_id}-edit-btn")
    
    
    def click_cancel_order(self, order_id: str):
        """Click cancel order button"""
        self.click_by_testid(f"order-cancel-{order_id}")
    
    def click_delete_order(self, order_id: str):
        """Click delete order button"""
        self.click_by_testid(f"order-{order_id}-delete-btn")
    
    def confirm_action(self):
        """Confirm action - handle browser alert"""
        self.confirm_browser_alert()

