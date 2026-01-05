"""
Test admin can create new product via UI.
"""

import pytest
from utils.data_factory import DataFactory


class TestAdminCreateProduct:
    """Test admin can create product"""
    
    @pytest.mark.admin
    @pytest.mark.smoke
    def test_admin_can_create_product(
        self,
        logged_in_admin_browser,
        admin_products_page,
        admin_api,
        cleanup
    ):
        """
        Test admin can create new product via UI.
        
        Arrange: Create new admin, verify product name doesn't exist via API
        Act: Create product via UI form
        Assert: Product appears in list, exists in API
        """
        # Arrange
        admin_data = logged_in_admin_browser
        token = admin_data["token"]
        
        product_name = f"AdminCreated_{DataFactory.unique_id()}"
        
        # Verify product doesn't exist via API (API Arrange)
        existing_products = admin_api.get_products(token)
        existing_names = [p["name"] for p in existing_products]
        product_not_exists = product_name not in existing_names
        
        # Act
        admin_products_page.open()
        admin_products_page.click_add_product()
        
        admin_products_page.fill_product_form(
            name=product_name,
            description="Test product created by admin UI test",
            price="49.99",
            stock="50",
            category="Test Category"
        )
        admin_products_page.click_create()
        
        admin_products_page.open()
        admin_products_page.search_products(product_name)
        
        products_count = admin_products_page.get_products_count()
        
        products = admin_api.get_products(token)
        product_names = [p["name"] for p in products]
        
        # Register created product for cleanup
        created_product = next(
            (p for p in products if p["name"] == product_name),
            None
        )
        if created_product:
            cleanup.register_product(created_product["_id"])
        
        # Assert
        assert product_not_exists, \
            "Product should not exist before creation (API verification)"
        assert products_count > 0, \
            "Created product should appear in admin list"
        assert product_name in product_names, \
            "Created product should exist in API"
