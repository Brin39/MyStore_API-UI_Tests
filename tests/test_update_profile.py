"""
Test updating user profile.
"""

import time
import pytest
from selenium.webdriver.common.by import By
from utils.data_factory import DataFactory
from logic.ui.profile_page import ProfilePage


class TestUpdateProfile:
    """Test updating user profile"""
    
    @pytest.mark.profile
    def test_update_profile_saves_changes(
        self,
        logged_in_browser,
        auth_api
    ):
        """
        Test updating profile saves changes.
        
        Arrange: Create and login user via API, get current profile
        Act: Navigate to profile via UI clicks, update profile
        Assert: Changes saved (API verification)
        """
        # Arrange
        user_data = logged_in_browser
        token = user_data["token"]
        driver = user_data["driver"]
        
        # Get current profile from API (API Arrange)
        initial_profile = auth_api.get_profile(token)
        initial_phone = initial_profile.get("phone", "")
        initial_address = initial_profile.get("address", "")
        
        new_phone = f"+1-555-{DataFactory.unique_id()[:7]}"
        new_address = f"Test Address {DataFactory.unique_id()}"
        
        # Act - Navigate to profile via UI clicks (preserves session)
        profile_btn = driver.find_element(By.CSS_SELECTOR, '[data-testid="profile-button"]')
        profile_btn.click()
        time.sleep(0.5)
        
        my_profile_link = driver.find_element(By.CSS_SELECTOR, '[data-testid="dashboard-my-profile"]')
        my_profile_link.click()
        time.sleep(1)
        
        profile_page = ProfilePage(driver)
        profile_page.update_profile(phone=new_phone, address=new_address)
        
        # Wait for save
        time.sleep(1)
        
        # Get updated profile from API
        updated_profile = auth_api.get_profile(token)
        
        # Assert
        assert new_phone != initial_phone, \
            "New phone should be different from initial"
        assert updated_profile.get("phone") == new_phone, \
            f"Phone should be updated. Expected '{new_phone}', got '{updated_profile.get('phone')}'"
        assert updated_profile.get("address") == new_address, \
            f"Address should be updated. Expected '{new_address}', got '{updated_profile.get('address')}'"

