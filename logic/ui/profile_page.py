"""
Profile Page Object for MyStore.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from logic.ui.base_page import BasePage
from utils.constants import Urls


class ProfilePage(BasePage):
    """User profile page interactions"""
    
    # Test IDs - Display mode
    PROFILE_EDIT_BTN = "profile-edit-btn"
    
    # Test IDs - Edit mode
    PROFILE_NAME_INPUT = "profile-name-input"
    PROFILE_EMAIL_INPUT = "profile-email-input"
    PROFILE_PHONE_INPUT = "profile-phone-input"
    PROFILE_ADDRESS_INPUT = "profile-address-input"
    PROFILE_SAVE_BTN = "profile-save-btn"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to profile page"""
        self.navigate(Urls.PROFILE)
    
    def open_via_ui(self):
        """Navigate to profile page via UI click (preserves localStorage)"""
        import time
        # Wait for profile button to be visible and clickable, then click
        self.is_visible_by_testid("profile-button", timeout=10)
        self.click_by_testid("profile-button")
        time.sleep(0.5)
        
        # Wait for profile link to be visible and clickable, then click
        self.is_visible_by_testid("dashboard-my-profile", timeout=10)
        self.click_by_testid("dashboard-my-profile")
        time.sleep(1)
    
    # ==================== DISPLAY MODE ====================
    
    def click_edit(self):
        """Click edit button to enter edit mode"""
        # Wait for edit button to be visible and clickable
        self.is_visible_by_testid(self.PROFILE_EDIT_BTN, timeout=10)
        self.click_by_testid(self.PROFILE_EDIT_BTN)
    
    # ==================== EDIT MODE ====================
    
    def enter_name(self, name: str):
        """Enter name in edit mode"""
        self.type_by_testid(self.PROFILE_NAME_INPUT, name)
    
    def enter_email(self, email: str):
        """Enter email in edit mode"""
        self.type_by_testid(self.PROFILE_EMAIL_INPUT, email)
    
    def enter_phone(self, phone: str):
        """Enter phone in edit mode"""
        self.type_by_testid(self.PROFILE_PHONE_INPUT, phone)
    
    def enter_address(self, address: str):
        """Enter address in edit mode"""
        self.type_by_testid(self.PROFILE_ADDRESS_INPUT, address)
    
    def click_save(self):
        """Click save button"""
        self.click_by_testid(self.PROFILE_SAVE_BTN)
    
    def update_profile(self, name: str = None, phone: str = None, address: str = None):
        """
        Update profile with provided values.
        """
        self.click_edit()
        
        if name:
            self.enter_name(name)
        if phone:
            self.enter_phone(phone)
        if address:
            self.enter_address(address)
        
        self.click_save()
    
    def wait_for_profile_saved(self, timeout: int = 5):
        """Wait for profile save to complete"""
        # Wait for edit button to reappear (indicating save completed and back to display mode)
        self.is_visible_by_testid(self.PROFILE_EDIT_BTN, timeout=timeout)

