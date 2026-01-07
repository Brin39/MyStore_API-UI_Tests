"""
Login Page Object for MyStore.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from logic.ui.base_page import BasePage
from utils.constants import Urls


class LoginPage(BasePage):
    """Login page interactions"""
    
    # Test IDs
    EMAIL_INPUT = "email-input"
    PASSWORD_INPUT = "password-input"
    SUBMIT_BTN = "submit-btn"
    ERROR_MESSAGE = "error-message"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to login page"""
        self.navigate(Urls.LOGIN)
    
    def enter_email(self, email: str):
        """Enter email"""
        self.type_by_testid(self.EMAIL_INPUT, email)
    
    def enter_password(self, password: str):
        """Enter password"""
        self.type_by_testid(self.PASSWORD_INPUT, password)
    
    def click_submit(self):
        """Click login button"""
        self.click_by_testid(self.SUBMIT_BTN)
    
    def login(self, email: str, password: str):
        """
        Complete login flow.
        
        Args:
            email: user email
            password: user password
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()
    
    def is_error_visible(self) -> bool:
        """Check if error message is displayed"""
        return self.is_visible_by_testid(self.ERROR_MESSAGE, timeout=3)
    
    def is_on_login_page(self) -> bool:
        """Check if current page is login page"""
        return Urls.LOGIN in self.get_current_url()

