"""
Test admin can change order status.
"""

import pytest


class TestAdminChangeOrderStatus:
    """Test admin changes order status"""
    
    @pytest.mark.admin
    @pytest.mark.orders
    def test_admin_can_change_order_status(
        self,
        logged_in_admin_browser,
        admin_orders_page,
        create_test_user,
        create_test_order,
        admin_api
    ):
        """
        Test admin can change order status via UI.
        
        Arrange: Create new admin, create user and order via API
        Act: Change order status via UI
        Assert: Status updated (API verification)
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
        admin_orders_page.click_update_status(order_id)
        admin_orders_page.confirm_action()
        
        
        admin_orders_page.refresh()
        displayed_status = admin_orders_page.get_order_status(order_id)
        
        # Verify via API
        orders = admin_api.get_orders(token)
        updated_order = next(
            (o for o in orders if o["_id"] == order_id),
            None
        )
        
        # Assert
        assert updated_order is not None, "Order should exist"
        assert updated_order.get("status") == "processing", \
            f"Order status should be 'processing', got '{updated_order.get('status')}'"
        assert "processing" in displayed_status.lower(), \
            "UI should display updated status"

