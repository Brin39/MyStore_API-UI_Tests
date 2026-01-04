"""
Test admin can delete product via UI.
"""

import pytest


class TestAdminDeleteProduct:
    """Test admin can delete product"""
    
    @pytest.mark.admin
    def test_admin_can_delete_product(
        self,
        logged_in_admin_browser,
        admin_products_page,
        admin_api,
        create_test_product
    ):
        """
        Test admin can delete product via UI.
        
        Arrange: Create new admin, create product via API
        Act: Delete product via UI
        Assert: Product removed from list and API
        """
        # Arrange
        admin_data = logged_in_admin_browser
        token = admin_data["token"]
        
        created = create_test_product(token)
        product_id = created.get("_id") or created.get("product", {}).get("_id")
        
        # Act
        admin_products_page.open()
        product_visible_before = admin_products_page.is_product_visible(product_id)
        
        admin_products_page.click_delete_product(product_id)
        admin_products_page.confirm_browser_alert()
        
        admin_products_page.refresh()
        product_visible_after = admin_products_page.is_product_visible(product_id)
        
        products = admin_api.get_products(token)
        product_ids = [p["_id"] for p in products]
        
        # Assert
        assert product_visible_before, \
            "Product should be visible before deletion"
        assert not product_visible_after, \
            "Product should not be visible after deletion"
        assert product_id not in product_ids, \
            "Product should not exist in API after deletion"
