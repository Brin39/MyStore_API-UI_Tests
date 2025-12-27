"""
Test viewing order details.
"""

import time
import pytest
from selenium.webdriver.common.by import By
from logic.ui.orders_page import OrdersPage


class TestViewOrderDetails:
    """Test viewing order details"""
    
    @pytest.mark.orders
    def test_order_displays_correct_status(
        self,
        logged_in_browser,
        orders_api,
        create_test_order
    ):
        """
        Test order card displays the correct status.
        
        Arrange: Create order via API
        Act: Navigate to orders page via UI clicks (preserves session)
        Assert: Status matches API data
        """
        # Arrange
        user_data = logged_in_browser
        token = user_data["token"]
        driver = user_data["driver"]
        
        order = create_test_order(token)
        order_id = order.get("_id") or order.get("order", {}).get("_id")
        
        # Get order from API
        api_order = orders_api.get_order_by_id(order_id, token)
        api_status = api_order.get("status", "pending")
        
        # Act - Navigate to orders via UI clicks (preserves localStorage)
        profile_btn = driver.find_element(By.CSS_SELECTOR, '[data-testid="profile-button"]')
        profile_btn.click()
        time.sleep(0.5)
        
        orders_link = driver.find_element(By.CSS_SELECTOR, '[data-testid="dashboard-my-orders"]')
        orders_link.click()
        time.sleep(1)
        
        orders_page = OrdersPage(driver)
        orders_page.wait_for_orders_loaded()
        
        displayed_status = orders_page.get_order_status(order_id)
        
        # Assert
        assert api_status.lower() in displayed_status.lower(), \
            f"Displayed status should match API. Expected '{api_status}', got '{displayed_status}'"

