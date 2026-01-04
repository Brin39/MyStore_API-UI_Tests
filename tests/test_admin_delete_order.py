"""
Test admin can delete order.
"""

import pytest


class TestAdminDeleteOrder:
    """Test admin deletes order"""
    
    @pytest.mark.admin
    @pytest.mark.orders
    def test_admin_can_delete_order(
        self,
        logged_in_admin_browser,
        admin_orders_page,
        create_test_user,
        create_test_order,
        admin_api
    ):
        """
        Test admin can delete order via UI.
        
        Arrange: Create new admin, create user and order via API
        Act: Delete order via UI
        Assert: Order no longer exists
        """
        # Arrange
        admin_data = logged_in_admin_browser
        token = admin_data["token"]
        
        # Create a separate test user and order
        user_data = create_test_user()
        user_token = user_data["token"]
        
        order = create_test_order(user_token)
        order_id = order.get("_id") or order.get("order", {}).get("_id")
        
        # Act
        admin_orders_page.open()
        order_visible_before = admin_orders_page.is_order_visible(order_id)
        
        admin_orders_page.click_delete_order(order_id)
        admin_orders_page.confirm_browser_alert()
        
        admin_orders_page.refresh()
        order_visible_after = admin_orders_page.is_order_visible(order_id)
        
        # Verify via API
        orders = admin_api.get_orders(token)
        order_ids = [o.get("_id") for o in orders]
        
        # Assert
        assert order_visible_before, "Order should be visible before deletion"
        assert not order_visible_after, "Order should not be visible after deletion"
        assert order_id not in order_ids, "Order should not exist in API after deletion"

