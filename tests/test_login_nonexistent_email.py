"""
Test login with non-existent email fails.
"""

import pytest
from utils.data_factory import DataFactory


class TestLoginNonexistentEmail:
    """Test login with non-existent email shows error"""
    
    @pytest.mark.auth
    def test_login_with_nonexistent_email_fails(
        self,
        login_page,
        auth_api,
        create_test_user
    ):
        """
        Test login with non-existent email shows error.
        
        Arrange: Create user via API, generate different non-existent email
        Act: Try to login with non-existent email and valid password format
        Assert: Error message is shown, user remains on login page
        """
        # Arrange
        # Create a user to ensure we have a registered email in the system
        existing_user = create_test_user()
        existing_email = existing_user["email"]
        
        # Generate a different email that doesn't exist
        fake_email = f"nonexistent_{DataFactory.unique_id()}@test.com"
        
        # Verify existing email works (to confirm our test setup is correct)
        existing_user_result = auth_api.login_or_none(existing_email, existing_user["password"])
        existing_email_works = existing_user_result is not None
        
        # Act
        login_page.open()
        login_page.login(fake_email, existing_user["password"])
        
        error_visible = login_page.is_error_visible()
        still_on_login = login_page.is_on_login_page()
        
        # Assert
        assert existing_email_works, \
            "Existing user should be able to login (test setup verification)"
      
        assert error_visible, \
            "Error message should be visible for non-existent email"
        assert still_on_login, \
            "Should remain on login page after failed login with non-existent email"
