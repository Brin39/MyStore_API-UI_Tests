"""
Test admin can view user details.
"""

import pytest


class TestAdminViewUser:
    """Test admin views user details"""
    
    @pytest.mark.admin
    def test_admin_can_view_user(
        self,
        logged_in_admin_browser,
        admin_users_page,
        create_test_user,
        admin_api
    ):
        """
        Test admin can view user details via UI modal.
        
        Arrange: Create new admin, create test user via API
        Act: Open users page, search for user, view user details
        Assert: User details in modal match API data
        """
        # Arrange
        admin_data = logged_in_admin_browser
        token = admin_data["token"]
        
        # Create a separate test user (not the admin)
        user_data = create_test_user()
        user_id = user_data["user"].get("_id") or user_data["user"].get("id")
        
        # Get user details from API
        api_user = admin_api.get_user_details(user_id, token)
        
        # Act
        admin_users_page.open()
        admin_users_page.search_users(user_data["email"])
        admin_users_page.click_view_user(user_id)
        
        # Wait for modal to be visible
        modal_visible = admin_users_page.is_user_modal_visible()
        
        # Get displayed details from modal
        displayed_name = admin_users_page.get_user_modal_name()
        displayed_email = admin_users_page.get_user_modal_email()
        displayed_id = admin_users_page.get_user_modal_id()
        displayed_role = admin_users_page.get_user_modal_role()
        
        # Close modal
        admin_users_page.close_user_modal()
        
        # Assert
        assert modal_visible, "User modal should be visible"
        assert api_user.get("name") in displayed_name, \
            f"Name should match. Expected '{api_user.get('name')}' in '{displayed_name}'"
        assert api_user.get("email") == displayed_email, \
            f"Email should match. Expected '{api_user.get('email')}', got '{displayed_email}'"
        assert user_id in displayed_id, \
            f"ID should match. Expected '{user_id}' in '{displayed_id}'"
        assert api_user.get("role", "user").lower() in displayed_role.lower(), \
            f"Role should match. Expected '{api_user.get('role', 'user')}' in '{displayed_role}'"

