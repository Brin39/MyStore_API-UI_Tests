"""
Admin Dashboard Page Object for MyStore.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from logic.ui.base_page import BasePage
from utils.constants import Urls


class AdminDashboardPage(BasePage):
    """Admin dashboard page interactions"""
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to admin dashboard"""
        self.navigate(Urls.ADMIN)

