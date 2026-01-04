"""
Admin Products Page Object for MyStore.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from logic.ui.base_page import BasePage
from utils.constants import Urls


class AdminProductsPage(BasePage):
    """Admin products page interactions"""
    
    # Test IDs
    PRODUCT_LIST = "admin-product-list"
    SEARCH_INPUT = "admin-search-input"
    ADD_BUTTON = "admin-add-button"
    TOTAL_COUNT = "admin-total-count"
    
    # Product form
    PRODUCT_FORM = "product-form"
    NAME_INPUT = "product-name-input"
    DESCRIPTION_INPUT = "product-description-input"
    PRICE_INPUT = "product-price-input"
    STOCK_INPUT = "product-stock-input"
    CATEGORY_INPUT = "product-category-input"
    BEST_OFFER_CHECKBOX = "product-best-offer-checkbox"
    SAVE_BTN = "edit-product-save-btn"
    CANCEL_BTN = "edit-product-cancel-btn"
    
    # Alert modal
    ALERT_MODAL = "alert-modal"
    CONFIRM_BTN = "confirm-alert-btn"
    CANCEL_ALERT_BTN = "cancel-alert-btn"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to admin products"""
        self.navigate(Urls.ADMIN_PRODUCTS)
    
    def click_add_product(self):
        """Click add product button"""
        self.click_by_testid(self.ADD_BUTTON)
    
    def search_products(self, query: str):
        """Search products"""
        self.type_by_testid(self.SEARCH_INPUT, query)
    
    def get_products_count(self) -> int:
        """Get number of displayed products"""
        rows = self.driver.find_elements(
            By.CSS_SELECTOR, '[data-testid^="admin-product-row-"]'
        )
        return len(rows)
    
    def get_total_count_text(self) -> str:
        """Get total count text"""
        return self.get_text_by_testid(self.TOTAL_COUNT)
    
    # ==================== PRODUCT FORM ====================
    
    def is_form_visible(self) -> bool:
        """Check if product form is visible"""
        return self.is_visible_by_testid(self.PRODUCT_FORM, timeout=3)
    
    def fill_product_form(
        self,
        name: str,
        description: str,
        price: str,
        stock: str,
        category: str = None,
        best_offer: bool = False
    ):
        """Fill product form"""
        self.type_by_testid(self.NAME_INPUT, name)
        self.type_by_testid(self.DESCRIPTION_INPUT, description)
        self.type_by_testid(self.PRICE_INPUT, price)
        self.type_by_testid(self.STOCK_INPUT, stock)
        
        if category:
            self.type_by_testid(self.CATEGORY_INPUT, category)
        
        if best_offer:
            checkbox = self.find_by_testid(self.BEST_OFFER_CHECKBOX)
            if not checkbox.is_selected():
                checkbox.click()
    
    def click_save(self):
        """Click save button"""
        self.click_by_testid(self.SAVE_BTN)
    
    def click_cancel(self):
        """Click cancel button"""
        self.click_by_testid(self.CANCEL_BTN)
    
    # ==================== PRODUCT ACTIONS ====================
    
    def click_edit_product(self, product_id: str):
        """Click edit button for product"""
        # The edit button is within the product row
        row = self.find_by_testid(f"admin-product-row-{product_id}")
        edit_btn = row.find_element(By.CSS_SELECTOR, f'[data-testid="admin-product-{product_id}-edit-btn"]')
        edit_btn.click()
    
    def click_delete_product(self, product_id: str):
        """Click delete button for product"""
        row = self.find_by_testid(f"admin-product-row-{product_id}")
        delete_btn = row.find_element(By.CSS_SELECTOR, f'[data-testid="admin-product-{product_id}-delete-btn"]')
        delete_btn.click()
    
    def confirm_delete(self):
        """Confirm delete action"""
        self.click_by_testid(self.CONFIRM_BTN)

    def cancel_delete(self):
        """Cancel delete action"""
        self.click_by_testid(self.CANCEL_ALERT_BTN)
    
    def is_product_visible(self, product_id: str) -> bool:
        """Check if product row is visible"""
        return self.is_visible_by_testid(f"admin-product-row-{product_id}", timeout=3)

