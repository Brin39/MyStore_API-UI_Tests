"""
Test admin can see newly created user in users list.
"""

import pytest


class TestAdminSeesUser:
    """Test admin sees created user"""
    
    @pytest.mark.admin
    def test_admin_sees_created_user(
        self,
        logged_in_admin_browser,
        admin_users_page,
        create_test_user
    ):
        """
        Test admin can see newly created user in a user's list.
        
        Arrange: Create new admin, create test user via API
        Act: Open users page, search for user
        Assert: Created user visible in a list
        """
        # Arrange
        # Create a separate test user (not the admin)
        user_data = create_test_user()
        user_id = user_data["user"].get("_id") or user_data["user"].get("id")
        user_name = user_data["user"].get("name")
        
        # Act
        admin_users_page.open()
        admin_users_page.search_users(user_name)
        
        user_visible = admin_users_page.is_user_visible(user_id)
        displayed_name = admin_users_page.get_user_name(user_id)
        
        # Assert
        assert user_visible, \
            "Created user should be visible in admin users list"
        assert user_name in displayed_name, \
            f"User name should be displayed correctly. Expected '{user_name}' in '{displayed_name}'"
