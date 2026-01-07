"""
Home Page Object for MyStore.
"""

from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from logic.ui.base_page import BasePage
from utils.constants import Urls


class HomePage(BasePage):
    """Home page interactions"""
    
    # Test IDs
    SEARCH_INPUT = "search-input"
    SEARCH_BTN = "search-btn"
    CART_LINK = "cart-link"
    CART_COUNT = "cart-badge"
    PRODUCT_MODAL = "product-modal"
    ADD_TO_CART_BTN = "add-to-cart-btn"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to home page"""
        self.navigate(Urls.HOME)
    
    def open_user_home(self):
        """Navigate to authenticated user home"""
        self.navigate(Urls.USER_HOME)
    
    # ==================== HEADER ====================
    
    def get_cart_count(self) -> int:
        """Get cart items count from header"""
        # If cart is empty, the badge element doesn't exist
        if not self.is_visible_by_testid(self.CART_COUNT, timeout=2):
            return 0
        
        text = self.get_text_by_testid(self.CART_COUNT)
        try:
            return int(text)
        except ValueError:
            return 0
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated (cart link visible, login not)"""
        return self.is_visible_by_testid(self.CART_LINK, timeout=3)
    
    # ==================== SEARCH ====================
    
    def search(self, query: str):
        """Search for products"""
        self.type_by_testid(self.SEARCH_INPUT, query)
        self.click_by_testid(self.SEARCH_BTN)
    
    # ==================== PRODUCTS ====================
    
    def get_product_count(self) -> int:
        """Get number of displayed products"""
        cards = self.driver.find_elements(
            By.CSS_SELECTOR, '[data-testid^="product-card-"]'
        )
        return len(cards)
    
    def click_product(self, product_id: str):
        """Click on product card to open modal"""
        self.click_by_testid(f"view-product-btn-{product_id}")
    
    def click_first_product(self):
        """Click on first product card"""
        cards = self.driver.find_elements(
            By.CSS_SELECTOR, '[data-testid^="view-product-btn-"]'
        )
        if cards:
            cards[0].click()
    
    def is_product_visible(self, product_id: str) -> bool:
        """Check if product card is visible"""
        return self.is_visible_by_testid(f"product-card-{product_id}", timeout=3)
    
    # ==================== PRODUCT MODAL ====================
    
    def is_product_modal_visible(self) -> bool:
        """Check if product modal is open"""
        return self.is_visible_by_testid(self.PRODUCT_MODAL, timeout=5)
    
    def click_add_to_cart(self):
        """Click add to cart button in modal"""
        self.click_by_testid(self.ADD_TO_CART_BTN)
    
    def add_first_product_to_cart(self):
        """Click first product, add to cart"""
        self.click_first_product()
        self.is_product_modal_visible()
        self.click_add_to_cart()

