"""
Cart Page Object for MyStore.
"""

from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from logic.ui.base_page import BasePage
from utils.constants import Urls


class CartPage(BasePage):
    """Cart page interactions"""
    
    # Test IDs
    EMPTY_CART_MESSAGE = "empty-cart-message"
    CART_TOTAL = "cart-total"
    CHECKOUT_BTN = "checkout-btn"
    CLEAR_CART_BTN = "clear-cart-btn"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to cart page"""
        self.navigate(Urls.CART)
    
    def open_via_ui(self):
        """Navigate to cart page via UI click (preserves localStorage)"""
        import time
        cart_link = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="cart-link"]')
        cart_link.click()
        time.sleep(1)
    
    # ==================== CART STATE ====================
    
    def is_cart_empty(self) -> bool:
        """Check if cart is empty"""
        return self.is_visible_by_testid(self.EMPTY_CART_MESSAGE, timeout=3)
    
    def get_cart_items(self) -> List:
        """Get all cart item elements (main items only, not sub-elements)"""
        # Find only main cart item containers (exact match for cart-item-{id})
        all_elements = self.driver.find_elements(
            By.CSS_SELECTOR, '[data-testid^="cart-item-"]'
        )
        # Filter to get only main item containers (not sub-elements like cart-item-quantity-{id})
        items = []
        seen_ids = set()
        for elem in all_elements:
            testid = elem.get_attribute("data-testid")
            if testid and testid.startswith("cart-item-"):
                # Extract product ID (everything after "cart-item-")
                parts = testid.split("cart-item-", 1)
                if len(parts) > 1:
                    product_id = parts[1].split("-")[0]  # Get first part before any additional dashes
                    if product_id not in seen_ids:
                        # Check if this is a main item (not a sub-element)
                        if testid == f"cart-item-{product_id}":
                            items.append(elem)
                            seen_ids.add(product_id)
        return items
    
    def get_cart_items_count(self) -> int:
        """Get number of items in cart"""
        return len(self.get_cart_items())
    
    def wait_for_item_removed(self, product_id: str, timeout: int = 10):
        """Wait for item to be removed from cart"""
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        
        # Wait for element to be removed from DOM
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, f'[data-testid="cart-item-{product_id}"]')
            )
        )
    
    def get_cart_total(self) -> str:
        """Get cart total text"""
        return self.get_text_by_testid(self.CART_TOTAL)
    
    def get_cart_total_amount(self) -> float:
        """Get cart total as float"""
        text = self.get_cart_total()
        # Extract number from "$123.45" format
        try:
            return float(text.replace("$", "").replace(",", ""))
        except ValueError:
            return 0.0
    
    # ==================== CART ITEM ACTIONS ====================
    
    def get_item_quantity(self, product_id: str) -> int:
        """Get quantity of specific item"""
        text = self.get_text_by_testid(f"cart-item-quantity-{product_id}")
        try:
            return int(text)
        except ValueError:
            return 0
    
    def increase_item_quantity(self, product_id: str):
        """Increase item quantity"""
        # Wait for increase button to be visible and clickable
        self.is_visible_by_testid(f"cart-item-increase-{product_id}", timeout=10)
        self.click_by_testid(f"cart-item-increase-{product_id}")
    
    def decrease_item_quantity(self, product_id: str):
        """Decrease item quantity"""
        self.click_by_testid(f"cart-item-decrease-{product_id}")
    
    def remove_item(self, product_id: str):
        """Remove item from cart"""
        # Wait for delete button to be visible and clickable
        self.is_visible_by_testid(f"cart-item-{product_id}-delete-btn", timeout=10)
        self.click_by_testid(f"cart-item-{product_id}-delete-btn")
    
    # ==================== CART ACTIONS ====================
    
    def click_checkout(self):
        """Click checkout button (waits for button to be visible and clickable)"""
        # Wait for checkout button to be visible and clickable
        self.is_visible_by_testid(self.CHECKOUT_BTN, timeout=10)
        self.click_by_testid(self.CHECKOUT_BTN)
    
    def wait_for_checkout_complete(self, timeout: int = 10):
        """Wait for checkout to complete and page to stabilize"""
        # Wait for redirect or page change after checkout
        # Checkout redirects away from cart page (to orders, home, or success page)
        self.wait.until(
            lambda d: Urls.CART not in self.get_current_url()
        )
    
    def click_clear_cart(self):
        """Click clear cart button"""
        self.click_by_testid(self.CLEAR_CART_BTN)
    
    def is_on_cart_page(self) -> bool:
        """Check if on cart page"""
        return Urls.CART in self.get_current_url()
    
    def wait_for_cart_empty(self, timeout: int = 10):
        """Wait for cart to be empty after clearing"""
        self.wait.until(
            lambda d: self.is_cart_empty()
        )
    
    def wait_for_item_quantity(self, product_id: str, expected_quantity: int, timeout: int = 10):
        """Wait for item quantity to match expected value"""
        self.wait.until(
            lambda d: self.get_item_quantity(product_id) == expected_quantity
        )

