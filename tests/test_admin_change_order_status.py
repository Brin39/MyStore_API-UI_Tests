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
        
        # Verify initial status is "pending"
        initial_orders = admin_api.get_orders(token)
        initial_order = next(
            (o for o in initial_orders if o["_id"] == order_id),
            None
        )
        
        # Act
        admin_orders_page.open()
        
        # Verify initial status in UI
        initial_displayed_status = admin_orders_page.get_order_status(order_id)

        # Change status
        admin_orders_page.click_update_status(order_id)
        admin_orders_page.confirm_action()
        admin_orders_page.wait_for_status_update(order_id)
        
        # Get updated status from UI
        displayed_status = admin_orders_page.get_order_status(order_id)
        
        # Verify via API
        orders = admin_api.get_orders(token)
        updated_order = next(
            (o for o in orders if o["_id"] == order_id),
            None
        )
        
        # Assert
        assert initial_order is not None, "Order should exist"
        assert initial_order.get("status") == "pending", \
            f"Initial order status should be 'pending', got '{initial_order.get('status')}'"
        assert "pending" in initial_displayed_status.lower(), \
            f"UI should display initial 'pending' status, got '{initial_displayed_status}'"
        assert updated_order is not None, "Order should exist"
        assert updated_order.get("status") == "processing", \
            f"Order status should be 'processing', got '{updated_order.get('status')}'"
        assert "processing" in displayed_status.lower(), \
            f"UI should display updated status 'processing', got '{displayed_status}'"

