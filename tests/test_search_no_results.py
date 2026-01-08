"""
Test search with no matches shows empty state.
"""

import pytest
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
        
        # Verify via API search that no products match
        api_products = products_api.search_products(nonexistent_name)
        
        # Act
        home_page.open()
        initial_count = home_page.get_product_count()
        
        home_page.search(nonexistent_name)
        home_page.wait_for_search_results_changed(initial_count)
        
        products_count = home_page.get_product_count()
        
        # Assert
        assert no_matching_products_in_api, \
            "Search term should not match any products in API"
        assert len(api_products) == 0, \
            f"API should return 0 products for '{nonexistent_name}'. Found {len(api_products)} products"
        assert products_count == 0, \
            f"Search for non-existent product should return no results in UI. Found {products_count} products"

