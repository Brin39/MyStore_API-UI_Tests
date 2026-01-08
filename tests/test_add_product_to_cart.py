"""
Test adding product to cart via UI updates cart count.
"""

import time
import pytest
from logic.ui.home_page import HomePage


class TestAddProductToCart:
    """Test adding product to cart"""
    
    @pytest.mark.cart
    @pytest.mark.smoke
    def test_add_product_to_cart_updates_count(
        self,
        logged_in_browser,
        get_random_product,
        cart_api
    ):
        """
        Test adding product to cart via UI updates cart count.
        
        Arrange: Login user, get a random product from API
        Act: Click product, add to cart via UI
        Assert: Cart count increases, product in cart (verified via API)
        """
        # Arrange
        user_data = logged_in_browser
        token = user_data["token"]
        driver = user_data["driver"]
        
        cart_api.clear_cart(token)
        
        # Get random product (avoids conflicts with other tests)
        product = get_random_product()
        
        # Act - Navigate to home page
        home_page = HomePage(driver)
        # home_page.open_user_home()
        # time.sleep(1)
        
        initial_count = home_page.get_cart_count()
        
        home_page.click_product(product["_id"])
        modal_visible = home_page.is_product_modal_visible()
        home_page.click_add_to_cart()
        
       
        # home_page.refresh()
        new_count = home_page.get_cart_count()
        
        # Verify via API that product was added
        cart = cart_api.get_cart(token)
        cart_items = cart.get("items", [])
        product_ids = [item.get("product", {}).get("_id") for item in cart_items]
        
        # Assert
        assert product is not None, "Should get a product from API"
        assert modal_visible, "Product modal should open"
        assert new_count > initial_count, \
            f"Cart count should increase after adding product. Was {initial_count}, now {new_count}"
        assert product["_id"] in product_ids, \
            "Product should be in cart (API verification)"

