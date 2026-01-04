"""
Admin Users Page Object for MyStore.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from logic.ui.base_page import BasePage
from utils.constants import Urls


class AdminUsersPage(BasePage):
    """Admin users page interactions"""
    
    # Test IDs
    USER_LIST = "admin-user-list"
    SEARCH_INPUT = "admin-search-input"
    NO_USERS_MESSAGE = "no-users-message"
    
    # Alert modal
    CONFIRM_BTN = "confirm-alert-btn"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to admin users"""
        self.navigate(Urls.ADMIN_USERS)
    
    def search_users(self, query: str):
        """Search users"""
        self.type_by_testid(self.SEARCH_INPUT, query)
    
    def get_users_count(self) -> int:
        """Get number of displayed users"""
        cards = self.driver.find_elements(
            By.CSS_SELECTOR, '[data-testid^="admin-user-card-"]'
        )
        return len(cards)
    
    def is_user_visible(self, user_id: str) -> bool:
        """Check if user card is visible"""
        return self.is_visible_by_testid(f"admin-user-row-{user_id}", timeout=3)
    
    def get_user_name(self, user_id: str) -> str:
        """Get user name"""
        return self.get_text_by_testid(f"admin-user-name-{user_id}")
    
    def get_user_email(self, user_id: str) -> str:
        """Get user email"""
        return self.get_text_by_testid(f"admin-user-email-{user_id}")
    
    def get_user_role(self, user_id: str) -> str:
        """Get user role"""
        return self.get_text_by_testid(f"admin-user-role-{user_id}")
    
    def click_edit_user(self, user_id: str):
        """Click edit button for user"""
        self.click_by_testid(f"admin-user-edit-{user_id}")
    
    def click_delete_user(self, user_id: str):
        """Click delete button for user"""
        self.click_by_testid(f"admin-user-{user_id}-delete-btn")
    
    def confirm_delete(self):
        """Confirm delete action"""
        self.click_by_testid(self.CONFIRM_BTN)
    
    # Note: confirm_browser_alert() is inherited from BasePage

    def is_edit_form_visible(self) -> bool:
        """Check if edit form is visible"""
        return self.is_visible_by_testid("user-edit-form", timeout=3)
    
    def fill_user_form(self, name: str = None, email: str = None):
        """Fill user edit form"""
        if name:
            self.type_by_testid("user-name-input", name)
        if email:
            self.type_by_testid("user-email-input", email)
    
    def click_save_user(self):
        """Click save button"""
        self.click_by_testid("save-form-btn")

