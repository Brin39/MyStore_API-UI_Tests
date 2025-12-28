"""
Test removing item from cart.
"""

import time
import pytest
from selenium.webdriver.common.by import By
from logic.ui.cart_page import CartPage


class TestRemoveCartItem:
    """Test removing item from cart"""
    
    @pytest.mark.cart
    def test_remove_item_from_cart(
        self,
        logged_in_browser,
        cart_api,
        get_random_product
    ):
        """
        Test removing item from cart.
        
        Arrange: Get random product, add to cart via API
        Act: Navigate to cart via UI clicks, remove item via UI
        Assert: Item removed from cart
        """
        # Arrange
        user_data = logged_in_browser
        token = user_data["token"]
        driver = user_data["driver"]
        
        cart_api.clear_cart(token)
        
        # Get random product (avoids conflicts with other tests)
        product = get_random_product()
        cart_api.add_to_cart(product["_id"], 1, token)
        
        # Act - Navigate to cart via UI click (preserves localStorage)
        cart_link = driver.find_element(By.CSS_SELECTOR, '[data-testid="cart-link"]')
        cart_link.click()
        time.sleep(1)
        
        cart_page = CartPage(driver)
        item_visible_before = not cart_page.is_cart_empty()
        
        cart_page.remove_item(product["_id"])
        
        # Wait for item to be removed from DOM
        cart_page.wait_for_item_removed(product["_id"])
        
        # Verify via API (more reliable)
        cart = cart_api.get_cart(token)
        api_items_count = len(cart.get("items", []))
        
        # Check UI state
        cart_is_empty = cart_page.is_cart_empty()
        
        # Assert
        assert item_visible_before, "Item should be in cart before removal"
        assert api_items_count == 0, f"Cart should be empty via API. Found {api_items_count} items"
        assert cart_is_empty, "Cart should be empty after removing item"

