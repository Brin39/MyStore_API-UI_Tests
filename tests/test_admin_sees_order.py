"""
Test admin can see order created by user.
"""

import pytest


class TestAdminSeesOrder:
    """Test admin sees user order"""
    
    @pytest.mark.admin
    @pytest.mark.orders
    def test_admin_sees_user_order(
        self,
        logged_in_admin_browser,
        admin_orders_page,
        create_test_user,
        create_test_order
    ):
        """
        Test admin can see order created by user.
        
        Arrange: Create new admin, create user and order via API
        Act: Open orders page
        Assert: Order visible in admin orders
        """
        # Arrange
        admin_data = logged_in_admin_browser
        
        # Create a separate test user and order
        user_data = create_test_user()
        user_token = user_data["token"]
        
        order = create_test_order(user_token)
        order_id = order.get("_id") or order.get("order", {}).get("_id")
        
        # Act
        admin_orders_page.open()
        
        order_visible = admin_orders_page.is_order_visible(order_id)
        status = admin_orders_page.get_order_status(order_id)
        
        # Assert
        assert order_visible, \
            "Order should be visible in admin orders page"
        assert status.lower() == "pending", \
            f"New order should have pending status, got '{status}'"
