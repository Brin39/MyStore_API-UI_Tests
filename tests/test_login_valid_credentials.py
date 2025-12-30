"""
Test successful login with valid credentials.
"""

import pytest


class TestLoginValidCredentials:
    """Test successful login with valid credentials"""
    
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_login_with_valid_credentials_success(
        self,
        login_page,
        home_page,
        create_test_user
    ):
        """
        Test successful login with valid credentials.
        
        Arrange: Create user via API
        Act: Login via UI with correct credentials
        Assert: Redirected to user home, authenticated state visible
        """
        # Arrange
        user_data = create_test_user()
        
        # Act
        login_page.open()
        login_page.login(user_data["email"], user_data["password"])
        
        redirected_to_user = login_page.wait_for_url_contains("/user")
        is_authenticated = home_page.is_authenticated()
        
        # Assert
        assert redirected_to_user, \
            "Should redirect to user area after login"
        assert is_authenticated, \
            "User should be authenticated after login"

