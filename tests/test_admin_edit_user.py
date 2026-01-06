"""
Test admin can edit user.
"""

import pytest
from utils.data_factory import DataFactory


class TestAdminEditUser:
    """Test admin edits user"""
    
    @pytest.mark.admin
    def test_admin_can_edit_user(
        self,
        logged_in_admin_browser,
        admin_users_page,
        create_test_user,
        admin_api
    ):
        """
        Test admin can edit user data via UI.
        
        Arrange: Create new admin, create test user via API
        Act: Edit user via UI
        Assert: User data updated (API verification)
        """
        # Arrange
        admin_data = logged_in_admin_browser
        token = admin_data["token"]
        
        # Create a separate test user (not the admin)
        user_data = create_test_user()
        user_id = user_data["user"].get("_id") or user_data["user"].get("id")
        
        new_name = f"Updated_{DataFactory.unique_id()}"
        
        # Act
        admin_users_page.open()
        admin_users_page.search_users(user_data["email"])
        admin_users_page.click_edit_user(user_id)
        admin_users_page.fill_user_form(name=new_name)
        admin_users_page.click_save_user()
        
        # Verify via API
        updated_user = admin_api.get_user_details(user_id, token)
        
        # Assert
        assert updated_user.get("name") == new_name, \
            f"User name should be updated. Expected '{new_name}', got '{updated_user.get('name')}'"

