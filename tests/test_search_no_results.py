"""
Test search with no matches shows empty state.
"""

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from utils.data_factory import DataFactory


class TestSearchNoResults:
    """Test search with no results shows empty"""
    
    @pytest.mark.products
    def test_search_with_no_results_shows_empty(
        self,
    
        home_page,
        products_api
    ):
        """
        Test search with no matches shows empty state.
        
        Arrange: Generate unique search term, verify via API no products match
        Act: Search for non-existent product
        Assert: No products displayed or empty message shown
        """
        # Arrange
        nonexistent_name = f"NonExistentProduct_{DataFactory.unique_id()}"
        
        # Verify via API that no products with this name exist
        all_products = products_api.get_all_products()
        matching_products = [p for p in all_products if nonexistent_name.lower() in p.get("name", "").lower()]
        no_matching_products_in_api = len(matching_products) == 0
        
        # Act
        home_page.open()
        
        # Get initial products count (before search)
        initial_count = home_page.get_product_count()
        
        home_page.search(nonexistent_name)
        
        # Wait for search results to update (polling until count changes or becomes 0)
        driver = home_page.driver
        wait = WebDriverWait(driver, 2)
        
        # Wait until product count changes (search results updated)
        # This handles both cases: count becomes 0 or count decreases
        wait.until(
            lambda d: home_page.get_product_count() != initial_count
        )
        
               
        products_count = home_page.get_product_count()
        
        # Verify via API that no products match
        from logic.api.products_api import ProductsApi
        products_api = ProductsApi()
        api_products = products_api.search_products(nonexistent_name)
        
        # Assert
        assert no_matching_products_in_api, \
            "Search term should not match any products in API"
        assert len(api_products) == 0, \
            f"API should return 0 products for '{nonexistent_name}'. Found {len(api_products)} products"
        assert products_count == 0, \
            f"Search for non-existent product should return no results in UI. Found {products_count} products"

