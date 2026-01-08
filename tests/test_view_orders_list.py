"""
Test viewing user orders list.
"""

import pytest
from logic.ui.orders_page import OrdersPage


class TestViewOrdersList:
    """Test viewing orders list"""
    
    @pytest.mark.orders
    def test_orders_page_displays_user_orders(
        self,
        logged_in_browser,
        orders_api,
        create_test_order
    ):
        """
        Test orders page displays user orders.
        
        Arrange: Create order via API, verify it exists
        Act: Click Orders link in UI (preserves session)
        Assert: Order displayed in list
        """
        # Arrange
        user_data = logged_in_browser
        token = user_data["token"]
        driver = user_data["driver"]
        
        order = create_test_order(token)
        order_id = order.get("_id") or order.get("order", {}).get("_id")
        
        api_orders = orders_api.get_my_orders(token)
        api_order_ids = [o.get("_id") for o in api_orders]
        
        # Act - Navigate to Orders via UI clicks (preserves session)
        orders_page = OrdersPage(driver)
        orders_page.open_via_ui()
        orders_page.wait_for_orders_loaded()
        
        is_on_orders = orders_page.is_on_orders_page()
        orders_count = orders_page.get_orders_count()
        
        # Assert
        assert order_id in api_order_ids, \
            f"Order {order_id} should exist in API. Found: {api_order_ids}"
        assert is_on_orders, "Should be on orders page"
        assert orders_count == 1, \
            f"Should have  1 order, got {orders_count}"
