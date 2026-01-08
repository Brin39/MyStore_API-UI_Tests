"""
Test product modal displays correct product details.
"""

import pytest


class TestProductModalDetails:
    """Test product modal shows correct details"""
    
    @pytest.mark.products
    def test_product_modal_shows_correct_details(
        self,

        home_page,
        get_random_product
    ):
        """
        Test product modal displays correct product details.
        
        Arrange: Get random product details from API
        Act: Click on product to open modal
        Assert: Modal shows correct name, price, description
        """
        # Arrange
        # Get random product (avoids conflicts with other tests)
        product = get_random_product()
        
        # Act
        home_page.open()
        home_page.click_product(product["_id"])
        
        modal_visible = home_page.is_product_modal_visible()
        home_page.wait_for_modal_content_loaded()
        
        modal_name = home_page.get_modal_product_name()
        modal_price = home_page.get_modal_product_price()
        modal_description = home_page.get_modal_product_description()
        
        # Assert
        assert product is not None, "Should get a product from API"
        assert modal_visible, "Product modal should open"
        assert product["name"] in modal_name, \
            f"Modal should show product name. Expected '{product['name']}', got '{modal_name}'"
        assert str(product["price"]) in modal_price.replace("$", "").replace(",", ""), \
            "Modal should show product price"
        assert product.get("description", "") in modal_description, \
            f"Modal should show product description. Expected '{product.get('description', '')}' in '{modal_description}'"

