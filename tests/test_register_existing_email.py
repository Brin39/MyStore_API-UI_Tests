"""
Test registration with existing email fails.
"""

import pytest


class TestRegisterExistingEmail:
    """Test registration with existing email shows error"""
    
    @pytest.mark.auth
    def test_register_with_existing_email_fails(
        self,
        register_page,
        create_test_user,
        data_factory
    ):
        """
        Test registration with existing email shows error.
        
        Arrange: Create user via API
        Act: Try to register with same email via UI
        Assert: Error message is shown
        """
        # Arrange
        existing_user = create_test_user()
        
        # Act
        register_page.open()
        register_page.register(
            name="New User",
            email=existing_user["email"],
            password="DifferentPass123"
        )
        
        error_visible = register_page.is_error_visible()
        
        # Assert
        assert error_visible, \
            "Error message should be visible for duplicate email"

