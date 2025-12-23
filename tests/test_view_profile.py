"""
Test viewing user profile displays correct data.
"""

import pytest


class TestViewProfile:
    """Test viewing user profile"""
    
    @pytest.mark.profile
    def test_profile_displays_user_data(
        self,
        logged_in_browser,
        profile_page,
        auth_api
    ):
        """
        Test profile page displays correct user data.
        
        Arrange: Create user with specific data via API, login
        Act: Navigate to profile page
        Assert: Profile displays correct name and email
        """
        # Arrange
        user_data = logged_in_browser
        token = user_data["token"]
        
        # Get profile data from API
        api_profile = auth_api.get_profile(token)
        
        # Act
        profile_page.open()
        
        displayed_name = profile_page.get_name()
        displayed_email = profile_page.get_email()
        is_on_profile = profile_page.is_on_profile_page()
        
        # Assert
        assert is_on_profile, "Should be on profile page"
        assert api_profile["name"] in displayed_name, \
            f"Profile should display user name. Expected '{api_profile['name']}', got '{displayed_name}'"
        assert api_profile["email"] in displayed_email, \
            f"Profile should display user email"

