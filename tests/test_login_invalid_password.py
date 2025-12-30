"""
Test login with invalid password fails.
"""

import pytest


class TestLoginInvalidPassword:
    """Test login with wrong password shows error"""
    
    @pytest.mark.auth
    def test_login_with_invalid_password_fails(
        self,
        login_page,
        create_test_user
    ):
        """
        Test login with wrong password shows error.
        
        Arrange: Create user via API
        Act: Try to login with wrong password
        Assert: Error message is shown, still on login page
        """
        # Arrange
        user_data = create_test_user()
        
        # Act
        login_page.open()
        login_page.login(user_data["email"], "WrongPassword123")
        
        error_visible = login_page.is_error_visible()
        still_on_login = login_page.is_on_login_page()
        
        # Assert
        assert error_visible, \
            "Error message should be visible for invalid credentials"
        assert still_on_login, \
            "Should remain on login page after failed login"

