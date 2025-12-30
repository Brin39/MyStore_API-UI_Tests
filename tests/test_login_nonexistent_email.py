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
        auth_api
    ):
        """
        Test login with non-existent email shows error.
        
        Arrange: Generate email, verify via API it doesn't exist
        Act: Try to login via UI
        Assert: Error message is shown
        """
        # Arrange
        fake_email = f"nonexistent_{DataFactory.unique_id()}@test.com"
        fake_password = "SomePassword123"
        
        # Verify email doesn't exist via API
        api_result = auth_api.login_or_none(fake_email, fake_password)
        email_not_exists = api_result is None
        
        # Act
        login_page.open()
        login_page.login(fake_email, fake_password)
        
        error_visible = login_page.is_error_visible()
        
        # Assert
        assert email_not_exists, \
            "Email should not exist in the system (API verification)"
        assert error_visible, \
            "Error message should be visible for non-existent user"
