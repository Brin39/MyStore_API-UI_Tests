"""
Test home page displays products from database.
"""

import pytest


class TestHomePageDisplaysProducts:
    """Test home page displays products"""
    
    @pytest.mark.products
    @pytest.mark.smoke
    def test_home_page_displays_products(
        self,
        browser,
        home_page,
        products_api
    ):
        """
        Test home page displays products from database.
        
        Arrange: Get products count from API
        Act: Open home page
        Assert: Products are displayed
        """
        # Arrange
        api_products = products_api.get_all_products()
        
        # Act
        home_page.open()
        ui_products_count = home_page.get_product_count()
        
        # Assert
        assert ui_products_count > 0, \
            "Home page should display products"
        assert ui_products_count <= len(api_products), \
            "UI should not show more products than exist in database"

