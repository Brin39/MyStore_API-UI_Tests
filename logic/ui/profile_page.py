"""
Profile Page Object for MyStore.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from logic.ui.base_page import BasePage
from utils.constants import Urls


class ProfilePage(BasePage):
    """User profile page interactions"""
    
    # Test IDs - Display mode
    PROFILE_INFO = "profile-info"
    PROFILE_NAME = "profile-name"
    PROFILE_EMAIL = "profile-email"
    PROFILE_PHONE = "profile-phone"
    PROFILE_ADDRESS = "profile-address"
    PROFILE_EDIT_BTN = "profile-edit-btn"
    
    # Test IDs - Edit mode
    PROFILE_FORM = "profile-form"
    PROFILE_NAME_INPUT = "profile-name-input"
    PROFILE_EMAIL_INPUT = "profile-email-input"
    PROFILE_PHONE_INPUT = "profile-phone-input"
    PROFILE_ADDRESS_INPUT = "profile-address-input"
    PROFILE_SAVE_BTN = "profile-save-btn"
    PROFILE_CANCEL_BTN = "profile-cancel-btn"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to profile page"""
        self.navigate(Urls.PROFILE)
    
    # ==================== DISPLAY MODE ====================
    
    def get_name(self) -> str:
        """Get displayed name"""
        return self.get_text_by_testid(self.PROFILE_NAME)
    
    def get_email(self) -> str:
        """Get displayed email"""
        return self.get_text_by_testid(self.PROFILE_EMAIL)
    
    def get_phone(self) -> str:
        """Get displayed phone"""
        return self.get_text_by_testid(self.PROFILE_PHONE)
    
    def get_address(self) -> str:
        """Get displayed address"""
        return self.get_text_by_testid(self.PROFILE_ADDRESS)
    
    def click_edit(self):
        """Click edit button to enter edit mode"""
        self.click_by_testid(self.PROFILE_EDIT_BTN)
    
    def is_in_display_mode(self) -> bool:
        """Check if profile is in display mode"""
        return self.is_visible_by_testid(self.PROFILE_INFO, timeout=3)
    
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
    
    def click_cancel(self):
        """Click cancel button"""
        self.click_by_testid(self.PROFILE_CANCEL_BTN)
    
    def is_in_edit_mode(self) -> bool:
        """Check if profile is in edit mode"""
        return self.is_visible_by_testid(self.PROFILE_FORM, timeout=3)
    
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
    
    def is_on_profile_page(self) -> bool:
        """Check if on profile page"""
        return Urls.PROFILE in self.get_current_url()

