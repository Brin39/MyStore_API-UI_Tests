"""
Register Page Object for MyStore.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from logic.ui.base_page import BasePage
from utils.constants import Urls


class RegisterPage(BasePage):
    """Registration page interactions"""
    
    # Test IDs
    NAME_INPUT = "name-input"
    EMAIL_INPUT = "email-input"
    PASSWORD_INPUT = "password-input"
    CONFIRM_PASSWORD_INPUT = "confirm-password-input"
    ADMIN_CODE_INPUT = "admin-code-input"
    SUBMIT_BTN = "submit-btn"
    ERROR_MESSAGE = "error-message"
    LOGIN_LINK = "login-link"
    REGISTER_FORM = "register-form"
    SUCCESS_MODAL = "success-modal"
    SUCCESS_MESSAGE = "success-message"
    MODAL_LOGIN_BTN = "modal-login-btn"
    MODAL_CLOSE_BTN = "modal-close-btn"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to registration page"""
        self.navigate(Urls.REGISTER)
    
    def enter_name(self, name: str):
        """Enter name"""
        self.type_by_testid(self.NAME_INPUT, name)
    
    def enter_email(self, email: str):
        """Enter email"""
        self.type_by_testid(self.EMAIL_INPUT, email)
    
    def enter_password(self, password: str):
        """Enter password"""
        self.type_by_testid(self.PASSWORD_INPUT, password)
    
    def enter_confirm_password(self, password: str):
        """Enter password confirmation"""
        self.type_by_testid(self.CONFIRM_PASSWORD_INPUT, password)
    
    def enter_admin_code(self, code: str):
        """Enter admin code (if visible)"""
        self.type_by_testid(self.ADMIN_CODE_INPUT, code)
    
    def click_submit(self):
        """Click register button"""
        self.click_by_testid(self.SUBMIT_BTN)
    
    def register(self, name: str, email: str, password: str):
        """
        Complete registration flow.
        
        Args:
            name: user name
            email: user email
            password: user password
        """
        self.enter_name(name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.click_submit()
    
    def register_admin(self, name: str, email: str, password: str, admin_code: str):
        """
        Complete admin registration flow.
        """
        self.enter_name(name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.enter_admin_code(admin_code)
        self.click_submit()
    
    def get_error_message(self) -> str:
        """Get error message text"""
        return self.get_text_by_testid(self.ERROR_MESSAGE)
    
    def is_error_visible(self) -> bool:
        """Check if error message is displayed"""
        return self.is_visible_by_testid(self.ERROR_MESSAGE, timeout=3)
    
    def is_success_modal_visible(self) -> bool:
        """Check if success modal is displayed"""
        return self.is_visible_by_testid(self.SUCCESS_MODAL, timeout=5)
    
    def click_modal_login(self):
        """Click login button on success modal"""
        self.click_by_testid(self.MODAL_LOGIN_BTN)
    
    def click_login_link(self):
        """Click link to login page"""
        self.click_by_testid(self.LOGIN_LINK)
    
    def is_on_register_page(self) -> bool:
        """Check if current page is register page"""
        return Urls.REGISTER in self.get_current_url()

