"""
Test viewing user profile displays the correct data.
"""

import time
import pytest
from selenium.webdriver.common.by import By
from logic.ui.profile_page import ProfilePage


class TestViewProfile:
    """Test viewing user profile"""
    
    @pytest.mark.profile
    def test_profile_displays_user_data(
        self,
        logged_in_browser,
        auth_api
    ):
        """
        Test profile page displays the correct user data.
        
        Arrange: Create user with specific data via API, login
        Act: Navigate to profile page via UI clicks
        Assert: Profile displays correct name and email
        """
        # Arrange
        user_data = logged_in_browser
        token = user_data["token"]
        driver = user_data["driver"]
        
        # Get profile data from API
        api_profile = auth_api.get_profile(token)
        
        # Act - Navigate via UI clicks (preserves session)
        profile_btn = driver.find_element(By.CSS_SELECTOR, '[data-testid="profile-button"]')
        profile_btn.click()
        time.sleep(0.5)
        
        my_profile_link = driver.find_element(By.CSS_SELECTOR, '[data-testid="dashboard-my-profile"]')
        my_profile_link.click()
        time.sleep(1)
        
        profile_page = ProfilePage(driver)
        
        displayed_name = profile_page.get_name()
        displayed_email = profile_page.get_email()
        is_on_profile = profile_page.is_on_profile_page()
        
        # Assert
        assert is_on_profile, "Should be on profile page"
        assert api_profile["name"] in displayed_name, \
            f"Profile should display user name. Expected '{api_profile['name']}', got '{displayed_name}'"
        assert api_profile["email"] in displayed_email, \
            f"Profile should display user email"
