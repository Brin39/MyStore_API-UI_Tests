"""
Test search finds products by name.
"""

import pytest
from utils.data_factory import DataFactory


class TestSearchFindsProducts:
    """Test search finds matching products"""
    
    @pytest.mark.products
    def test_search_finds_matching_products(
        self,
        home_page,
        create_test_product,
        create_test_admin,
        products_api
    ):
        """
        Test search finds products by name.
        
        Arrange: Create new admin via API, create unique product via API
        Act: Search for product name
        Assert: Product appears in results
        """
        # Arrange
        admin_data = create_test_admin()
        admin_token = admin_data["token"]
        
        product_name = f"UniqueSearchTest_{DataFactory.unique_id()}"
        created = create_test_product(admin_token, name=product_name)
        product_id = created.get("_id") or created.get("product", {}).get("_id")
        
        # Act
        home_page.open()
        
        # Use full product name for search to ensure match
        home_page.search(product_name)
        
        # Wait for search results to update
        home_page.wait_for_search_results(expected_count=1)
        
        # Wait until product is visible
        product_visible = home_page.wait_for_product_visible(product_id)
        
        # Verify product exists via API
        api_products = products_api.search_products(product_name)
        api_product_ids = [p.get("_id") for p in api_products]
        
        # Get UI products count
        ui_products_count = home_page.get_product_count()
        
        # Assert
        assert len(api_products) == 1, \
            f"API should return exactly 1 product for '{product_name}'. Found {len(api_products)} products"
        assert product_id in api_product_ids, \
            f"Product {product_id} should be found via API search for '{product_name}'. Found: {api_product_ids}"
        assert ui_products_count == 1, \
            f"UI should display exactly 1 product for '{product_name}'. Found {ui_products_count} products"
        assert product_visible, \
            f"Created product {product_id} with name '{product_name}' should appear in search results for '{product_name}'"
