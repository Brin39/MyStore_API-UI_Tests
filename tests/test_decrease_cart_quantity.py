"""
Test decreasing product quantity in cart.
"""

import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
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
        driver = user_data["driver"]  # Needed for WebDriverWait
        
        cart_api.clear_cart(token)
        
        # Get random product (avoids conflicts with other tests)
        product = get_random_product()
        cart_api.add_to_cart(product["_id"], 2, token)
        
        # Act - Navigate to cart via UI click (preserves localStorage)
        cart_page = CartPage(driver)
        cart_page.open_via_ui()
        time.sleep(2)
        
        initial_quantity = cart_page.get_item_quantity(product["_id"])
        cart_page.decrease_item_quantity(product["_id"])
        
        # Wait for backend to process the quantity decrease
        time.sleep(2)
        
        # Wait for quantity to update in UI (polling until it changes)
        wait = WebDriverWait(driver, 10)
        expected_quantity = initial_quantity - 1
        
        # Wait until UI quantity matches expected value
        # Reads from data-testid="cart-item-quantity-{product_id}"
        wait.until(
            lambda d: cart_page.get_item_quantity(product["_id"]) == expected_quantity
        )
        
        new_quantity = cart_page.get_item_quantity(product["_id"])
        
        # Verify via API that quantity was actually decreased
        cart = cart_api.get_cart(token)
        cart_items = cart.get("items", [])
        api_quantity = None
        for item in cart_items:
            item_product_id = item.get("product", {}).get("_id") or item.get("productId")
            if item_product_id == product["_id"]:
                api_quantity = item.get("quantity", 0)
                break
        
        # Assert
        assert new_quantity == initial_quantity - 1, \
            f"UI quantity should decrease by 1. Was {initial_quantity}, got {new_quantity}"
        assert api_quantity == expected_quantity, \
            f"API quantity should be {expected_quantity}. Got {api_quantity}"

