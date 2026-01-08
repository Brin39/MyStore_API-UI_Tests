"""
Test decreasing product quantity in cart.
"""

import pytest
from logic.ui.cart_page import CartPage


class TestDecreaseCartQuantity:
    """Test decreasing product quantity in cart"""
    
    @pytest.mark.cart
    def test_decrease_product_quantity_in_cart(
        self,
        logged_in_browser,
        cart_api,
        get_random_product
    ):
        """
        Test decreasing product quantity in cart.
        
        Arrange: Get random product, add with quantity 2 to cart via API
        Act: Navigate to cart via UI clicks, decrease quantity via UI
        Assert: Quantity decreased (verified via UI and API)
        """
        # Arrange
        user_data = logged_in_browser
        token = user_data["token"]
        driver = user_data["driver"]
        
        cart_api.clear_cart(token)
        
        # Get random product (avoids conflicts with other tests)
        product = get_random_product()
        cart_api.add_to_cart(product["_id"], 2, token)
        
        # Act - Navigate to cart via UI click (preserves localStorage)
        cart_page = CartPage(driver)
        cart_page.open_via_ui()
        
        initial_quantity = cart_page.get_item_quantity(product["_id"])
        expected_quantity = initial_quantity - 1
        
        cart_page.decrease_item_quantity(product["_id"])
        cart_page.wait_for_item_quantity(product["_id"], expected_quantity)
        
        new_quantity = cart_page.get_item_quantity(product["_id"])
        
        # Wait for API to update
        api_quantity = cart_api.wait_for_item_quantity(product["_id"], expected_quantity, token)
        
        # Assert
        assert new_quantity == initial_quantity - 1, \
            f"UI quantity should decrease by 1. Was {initial_quantity}, got {new_quantity}"
        assert api_quantity == expected_quantity, \
            f"API quantity should be {expected_quantity}. Got {api_quantity}"

