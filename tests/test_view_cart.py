"""
Test viewing cart displays items correctly.
"""

import time
import pytest
from selenium.webdriver.common.by import By
from logic.ui.cart_page import CartPage


class TestViewCart:
    """Test viewing cart"""
    
    @pytest.mark.cart
    def test_cart_displays_added_items(
        self,
        logged_in_browser,
        cart_api,
        get_random_product
    ):
        """
        Test cart displays items added via API.
        
        Arrange: Get random product, add to cart via API
        Act: Navigate to cart page via UI click (preserves session)
        Assert: Items displayed correctly
        """
        # Arrange
        user_data = logged_in_browser
        token = user_data["token"]
        driver = user_data["driver"]
        
        cart_api.clear_cart(token)
        
        # Get random product with stock >= 2
        product = get_random_product(min_stock=2)
        cart_api.add_to_cart(product["_id"], 2, token)
        
        # Get cart from API
        api_cart = cart_api.get_cart(token)
        api_items_count = len(api_cart.get("items", []))
        
        # Act - Navigate to cart via UI click (preserves localStorage)
        cart_link = driver.find_element(By.CSS_SELECTOR, '[data-testid="cart-link"]')
        cart_link.click()
        time.sleep(1)
        
        cart_page = CartPage(driver)
        
        is_on_cart = cart_page.is_on_cart_page()
        cart_not_empty = not cart_page.is_cart_empty()
        displayed_quantity = cart_page.get_item_quantity(product["_id"])
        
        # Assert
        assert is_on_cart, "Should be on cart page"
        assert api_items_count > 0, "Cart should have items (API verification)"
        assert cart_not_empty, "Cart should not be empty"
        assert displayed_quantity == 2, \
            f"Displayed quantity should be 2, got {displayed_quantity}"

