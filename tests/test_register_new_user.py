"""
Test successful user registration.
"""

import pytest
from utils.data_factory import DataFactory


class TestRegisterNewUser:
    """Test successful user registration"""
    
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_register_new_user_success(
        self,
        register_page,
        login_page,
        cleanup,
        auth_api
    ):
        """
        Test successful user registration.
        
        Arrange: Generate unique user data, verify email doesn't exist via API
        Act: Fill and submit registration form
        Assert: Success modal appears, redirect to login works
        """
        # Arrange
        user_data = DataFactory.user()
        
        # Verify email doesn't exist via API
        api_result = auth_api.login_or_none(user_data["email"], user_data["password"])
        email_not_exists = api_result is None
        
        # Act
        register_page.open()
        register_page.register(
            name=user_data["name"],
            email=user_data["email"],
            password=user_data["password"]
        )
        
        success_modal_visible = register_page.is_success_modal_visible()
        register_page.click_modal_login()
        
        # Wait for redirect to login page
        login_page.wait_for_url_contains("/login")
        is_on_login = login_page.is_on_login_page()
        
        # Register for cleanup - get user ID by logging in
        try:
            result = auth_api.login(user_data["email"], user_data["password"])
            user_id = result.get("_id") or result.get("user", {}).get("_id")
            if user_id:
                cleanup.register_user(user_id)
        except Exception:
            pass
        
        # Assert
        assert email_not_exists, \
            "Email should not exist before registration (API verification)"
        assert success_modal_visible, \
            "Success modal should be visible after registration"
        assert is_on_login, \
            "Should redirect to login page after successful registration"
