"""
Test admin can edit product.
"""

import pytest
from utils.data_factory import DataFactory


class TestAdminEditProduct:
    """Test admin edits product"""
    
    @pytest.mark.admin
    def test_admin_can_edit_product(
        self,
        logged_in_admin_browser,
        admin_products_page,
        create_test_product,
        admin_api
    ):
        """
        Test admin can edit product via UI.
        
        Arrange: Create new admin, create product via API
        Act: Edit product via UI
        Assert: Product updated (API verification)
        """
        # Arrange
        admin_data = logged_in_admin_browser
        token = admin_data["token"]
        
        created = create_test_product(token)
        product_id = created.get("_id") or created.get("product", {}).get("_id")
        
        new_name = f"Updated_{DataFactory.unique_id()}"
        new_price = "199.99"
        
        # Act
        admin_products_page.open()
        admin_products_page.click_edit_product(product_id)
        admin_products_page.fill_product_form(
            name=new_name,
            description="Updated description",
            price=new_price,
            stock="50"
        )
        admin_products_page.click_save()
        
        # Verify via UI - refresh page and search for updated product
        admin_products_page.open()
        admin_products_page.search_products(new_name)
        product_visible_after_edit = admin_products_page.is_product_visible(product_id)

        # Verify via API
        products = admin_api.get_products(token)
        updated_product = next(
            (p for p in products if p["_id"] == product_id),
            None
        )
        
        # Assert
        assert product_visible_after_edit, \
            f"Product {product_id} should be visible in UI after edit with new name '{new_name}'"
        assert updated_product is not None, "Product should exist"
        assert updated_product.get("name") == new_name, \
            f"Product name should be updated. Expected '{new_name}', got '{updated_product.get('name')}'"
        assert str(updated_product.get("price")) == new_price or updated_product.get("price") == float(new_price), \
            f"Product price should be updated. Expected '{new_price}', got '{updated_product.get('price')}'"

