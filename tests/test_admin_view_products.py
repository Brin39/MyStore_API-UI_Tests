"""
Test admin can view products list.
"""

import pytest


class TestAdminViewProducts:
    """Test admin views products list"""
    
    @pytest.mark.admin
    def test_admin_products_page_displays_products(
        self,
        logged_in_admin_browser,
        admin_products_page,
        admin_api
    ):
        """
        Test admin products page displays products.
        
        Arrange: Get products list via API
        Act: Open admin products page
        Assert: Products are displayed (UI count matches API count)
        """
        # Arrange
        admin_data = logged_in_admin_browser
        token = admin_data["token"]
        
        # Get products via API
        api_products = admin_api.get_products(token)
        api_products_count = len(api_products)
        
        # Act
        admin_products_page.open()
        
        ui_products_count = admin_products_page.get_products_count()
        
        # Assert
        assert ui_products_count == api_products_count, \
            f"UI should display all products. Expected {api_products_count}, got {ui_products_count}"

