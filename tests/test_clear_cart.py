"""
Test clearing cart removes all items.
"""

import pytest
from logic.ui.cart_page import CartPage


class TestClearCart:
    """Test clearing cart removes all items"""
    
    @pytest.mark.cart
    def test_clear_cart_removes_all_items(
        self,
        logged_in_browser,
        cart_api,
        get_random_product
    ):
        """
        Test clearing cart removes all items.
        
        Arrange: Add multiple random products to cart via API
        Act: Navigate to cart via UI clicks, click clear cart button
        Assert: Cart is empty (verified via UI and API)
        """
        # Arrange
        user_data = logged_in_browser
        token = user_data["token"]
        driver = user_data["driver"]
        
        cart_api.clear_cart(token)
        
        # Add two different products with sufficient stock
        product1 = get_random_product()
        cart_api.add_to_cart(product1["_id"], 1, token)
        
        # Get second product (different from first)
        product2 = get_random_product()
        # Ensure it's different product
        max_attempts = 10
        attempts = 0
        while product2["_id"] == product1["_id"] and attempts < max_attempts:
            product2 = get_random_product()
            attempts += 1
        
        cart_api.add_to_cart(product2["_id"], 1, token)
        
        # Verify cart has items via API
        cart_before = cart_api.get_cart(token)
        items_before = cart_before.get("items", [])
        
        # Act - Navigate to cart via UI click (preserves localStorage)
        cart_page = CartPage(driver)
        cart_page.open_via_ui()
        
        cart_had_items = not cart_page.is_cart_empty()
        cart_page.click_clear_cart()
        
        # Wait for cart to be empty in UI
        cart_page.wait_for_cart_empty()
        
        cart_is_empty = cart_page.is_cart_empty()
        
        # Verify via API that cart is empty
        cart = cart_api.get_cart(token)
        api_items_count = len(cart.get("items", []))
        
        # Assert
        assert len(items_before) == 2, "Cart should have 2 items before clearing"
        assert cart_had_items, "Cart should have items before clearing"
        assert cart_is_empty, "Cart should be empty after clearing"
        assert api_items_count == 0, f"Cart should be empty (API verification). Found {api_items_count} items"

