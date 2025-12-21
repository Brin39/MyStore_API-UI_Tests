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
    CART_CONTENT = "cart-content"
    CART_ITEMS_LIST = "cart-items-list"
    EMPTY_CART_MESSAGE = "empty-cart-message"
    CART_SUMMARY = "cart-summary"
    CART_TOTAL = "cart-total"
    CHECKOUT_BTN = "checkout-btn"
    CLEAR_CART_BTN = "clear-cart-btn"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to cart page"""
        self.navigate(Urls.CART)
    
    # ==================== CART STATE ====================
    
    def is_cart_empty(self) -> bool:
        """Check if cart is empty"""
        return self.is_visible_by_testid(self.EMPTY_CART_MESSAGE, timeout=3)
    
    def get_cart_items(self) -> List:
        """Get all cart item elements"""
        return self.driver.find_elements(
            By.CSS_SELECTOR, '[data-testid^="cart-item-"]'
        )
    
    def get_cart_items_count(self) -> int:
        """Get number of items in cart"""
        items = self.get_cart_items()
        # Filter out non-item elements (like cart-item-quantity, etc.)
        return len([i for i in items if "-" not in i.get_attribute("data-testid").split("cart-item-")[1]])
    
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
        self.click_by_testid(f"cart-item-increase-{product_id}")
    
    def decrease_item_quantity(self, product_id: str):
        """Decrease item quantity"""
        self.click_by_testid(f"cart-item-decrease-{product_id}")
    
    def remove_item(self, product_id: str):
        """Remove item from cart"""
        self.click_by_testid(f"cart-item-{product_id}-delete-btn")
    
    def get_item_name(self, product_id: str) -> str:
        """Get item name"""
        return self.get_text_by_testid(f"cart-item-name-{product_id}")
    
    def get_item_price(self, product_id: str) -> str:
        """Get item price"""
        return self.get_text_by_testid(f"cart-item-price-{product_id}")
    
    # ==================== CART ACTIONS ====================
    
    def click_checkout(self):
        """Click checkout button"""
        self.click_by_testid(self.CHECKOUT_BTN)
    
    def click_clear_cart(self):
        """Click clear cart button"""
        self.click_by_testid(self.CLEAR_CART_BTN)
    
    def is_on_cart_page(self) -> bool:
        """Check if on cart page"""
        return Urls.CART in self.get_current_url()

