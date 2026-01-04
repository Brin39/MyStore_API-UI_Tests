"""
Admin Dashboard Page Object for MyStore.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from logic.ui.base_page import BasePage
from utils.constants import Urls


class AdminDashboardPage(BasePage):
    """Admin dashboard page interactions"""
    
    # Test IDs
    DASHBOARD = "admin-dashboard"
    PRODUCTS_CARD = "admin-card-products"
    USERS_CARD = "admin-card-users"
    ORDERS_CARD = "admin-card-orders"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to admin dashboard"""
        self.navigate(Urls.ADMIN)
    
    def is_dashboard_visible(self) -> bool:
        """Check if dashboard is visible"""
        return self.is_visible_by_testid(self.DASHBOARD, timeout=5)
    
    def click_products_card(self):
        """Navigate to products management"""
        self.click_by_testid(self.PRODUCTS_CARD)
    
    def click_users_card(self):
        """Navigate to users management"""
        self.click_by_testid(self.USERS_CARD)
    
    def click_orders_card(self):
        """Navigate to orders management"""
        self.click_by_testid(self.ORDERS_CARD)

