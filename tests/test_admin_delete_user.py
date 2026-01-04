"""
Test admin can delete user.
"""

import pytest


class TestAdminDeleteUser:
    """Test admin deletes user"""
    
    @pytest.mark.admin
    def test_admin_can_delete_user(
        self,
        logged_in_admin_browser,
        admin_users_page,
        create_test_user,
        admin_api
    ):
        """
        Test admin can delete user via UI.
        
        Arrange: Create new admin, create test user via API
        Act: Delete user via UI
        Assert: User no longer exists (API verification)
        """
        # Arrange
        admin_data = logged_in_admin_browser
        token = admin_data["token"]
        
        # Create a separate test user (not the admin)
        user_data = create_test_user()
        user_id = user_data["user"].get("_id") or user_data["user"].get("id")
        
        # Act
        admin_users_page.open()
        admin_users_page.search_users(user_data["email"])
        
        user_visible_before = admin_users_page.is_user_visible(user_id)
        
        admin_users_page.click_delete_user(user_id)
        admin_users_page.confirm_browser_alert()
        
        admin_users_page.refresh()
        user_visible_after = admin_users_page.is_user_visible(user_id)
        
        # Verify via API
        users_response = admin_api.get_users(token)
        # API returns dict with 'users' key containing list of user objects
        users = users_response.get("users", [])
        user_ids = [u.get("_id") for u in users]
        
        # Assert
        assert user_visible_before, "User should be visible before deletion"
        assert not user_visible_after, "User should not be visible after deletion"
        assert user_id not in user_ids, "User should not exist in API after deletion"

