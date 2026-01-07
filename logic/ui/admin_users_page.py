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
    SEARCH_INPUT = "admin-search-input"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to admin users"""
        self.navigate(Urls.ADMIN_USERS)
    
    def search_users(self, query: str):
        """Search users"""
        self.type_by_testid(self.SEARCH_INPUT, query)
    
    def is_user_visible(self, user_id: str) -> bool:
        """Check if user card is visible"""
        return self.is_visible_by_testid(f"admin-user-row-{user_id}", timeout=3)
    
    def get_user_name(self, user_id: str) -> str:
        """Get user name"""
        return self.get_text_by_testid(f"admin-user-name-{user_id}")
    
    def click_view_user(self, user_id: str):
        """Click view button to open user details modal"""
        self.click_by_testid(f"admin-user-{user_id}-view-btn")
    
    def click_delete_user(self, user_id: str):
        """Click delete button for user"""
        self.click_by_testid(f"admin-user-{user_id}-delete-btn")
    
    # Note: confirm_browser_alert() is inherited from BasePage
    
    # ==================== USER MODAL ====================
    
    def is_user_modal_visible(self) -> bool:
        """Check if user modal is visible"""
        return self.is_visible_by_testid("user-modal-name", timeout=5)
    
    def get_user_modal_name(self) -> str:
        """Get user name from modal"""
        return self.get_text_by_testid("user-modal-name")
    
    def get_user_modal_email(self) -> str:
        """Get user email from modal"""
        return self.get_text_by_testid("user-modal-email")
    
    def get_user_modal_id(self) -> str:
        """Get user ID from modal"""
        return self.get_text_by_testid("user-modal-detail-id")
    
    def get_user_modal_role(self) -> str:
        """Get user role from modal"""
        return self.get_text_by_testid("user-modal-detail-role")
    
    def close_user_modal(self):
        """Close user modal"""
        self.click_by_testid("user-modal-close-button")

