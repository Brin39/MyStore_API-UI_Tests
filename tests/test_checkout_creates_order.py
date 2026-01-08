"""
Test checkout creates new order.
"""

import pytest
from logic.ui.cart_page import CartPage
from logic.ui.orders_page import OrdersPage


class TestCheckoutCreatesOrder:
    """Test checkout creates order"""
    
    @pytest.mark.cart
    @pytest.mark.orders
    @pytest.mark.e2e
    def test_checkout_creates_order(
        self,
        logged_in_browser,
        cart_api,
        orders_api,
        get_random_product,
        cleanup
    ):
        """
        Test checkout creates new order.
        
        Arrange: Get random product, add to cart via API
        Act: Navigate to cart via UI clicks, click checkout, navigate to orders
        Assert: Order created, visible in orders page (verified via UI and API)
        """
        # Arrange
        user_data = logged_in_browser
        token = user_data["token"]
        driver = user_data["driver"]
        
        cart_api.clear_cart(token)
        
        # Get random product (avoids conflicts with other tests)
        product = get_random_product()
        cart_api.add_to_cart(product["_id"], 1, token)
        initial_orders = orders_api.get_orders_count(token)
        
        # Act - Navigate to cart via UI click (preserves localStorage)
        cart_page = CartPage(driver)
        cart_page.open_via_ui()
        
        cart_page.click_checkout()
        cart_page.wait_for_checkout_complete()
        
        # Navigate to orders via UI clicks (preserves session)
        orders_page = OrdersPage(driver)
        orders_page.open_via_ui()
        orders_page.wait_for_orders_loaded()
        
        new_orders_count = orders_page.get_orders_count()
        api_orders_count = orders_api.get_orders_count(token)
        
        # Register created order for cleanup
        # Get all orders and find the new one (created after initial_orders)
        api_orders = orders_api.get_my_orders(token)
        if len(api_orders) > initial_orders:
            # Get the newest order (first in list, assuming API returns newest first)
            new_order = api_orders[0]
            order_id = new_order.get("_id")
            if order_id:
                cleanup.register_order(order_id)
        
        # Assert
        assert new_orders_count > initial_orders, \
            f"New order should be created. Had {initial_orders}, now {new_orders_count}"
        assert api_orders_count == new_orders_count, \
            f"Orders count should match between UI and API. UI: {new_orders_count}, API: {api_orders_count}"

