"""
Admin Page Objects for MyStore.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logic.ui.base_page import BasePage
from utils.constants import Urls


class AdminDashboardPage(BasePage):
    """Admin dashboard page interactions"""
    
    # Test IDs
    DASHBOARD = "admin-dashboard"
    PRODUCTS_CARD = "admin-card-products"
    USERS_CARD = "admin-card-users"
    ORDERS_CARD = "admin-card-orders"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to admin dashboard"""
        self.navigate(Urls.ADMIN)
    
    def is_dashboard_visible(self) -> bool:
        """Check if dashboard is visible"""
        return self.is_visible_by_testid(self.DASHBOARD, timeout=5)
    
    def click_products_card(self):
        """Navigate to products management"""
        self.click_by_testid(self.PRODUCTS_CARD)
    
    def click_users_card(self):
        """Navigate to users management"""
        self.click_by_testid(self.USERS_CARD)
    
    def click_orders_card(self):
        """Navigate to orders management"""
        self.click_by_testid(self.ORDERS_CARD)
    
    def get_products_stat(self) -> str:
        """Get products count from stat card"""
        return self.get_text_by_testid("stat-products-count")
    
    def get_users_stat(self) -> str:
        """Get users count from stat card"""
        return self.get_text_by_testid("stat-users-count")
    
    def get_orders_stat(self) -> str:
        """Get orders count from stat card"""
        return self.get_text_by_testid("stat-orders-count")
    
    def are_stats_visible(self) -> bool:
        """Check if stats are visible"""
        return (self.is_visible_by_testid("stat-products-count", timeout=5) and
                self.is_visible_by_testid("stat-users-count", timeout=2) and
                self.is_visible_by_testid("stat-orders-count", timeout=2))


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


class AdminUsersPage(BasePage):
    """Admin users page interactions"""
    
    # Test IDs
    USER_LIST = "admin-user-list"
    SEARCH_INPUT = "admin-search-input"
    NO_USERS_MESSAGE = "no-users-message"
    
    # Alert modal
    CONFIRM_BTN = "confirm-alert-btn"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to admin users"""
        self.navigate(Urls.ADMIN_USERS)
    
    def search_users(self, query: str):
        """Search users"""
        self.type_by_testid(self.SEARCH_INPUT, query)
    
    def get_users_count(self) -> int:
        """Get number of displayed users"""
        cards = self.driver.find_elements(
            By.CSS_SELECTOR, '[data-testid^="admin-user-card-"]'
        )
        return len(cards)
    
    def is_user_visible(self, user_id: str) -> bool:
        """Check if user card is visible"""
        return self.is_visible_by_testid(f"admin-user-row-{user_id}", timeout=3)
    
    def get_user_name(self, user_id: str) -> str:
        """Get user name"""
        return self.get_text_by_testid(f"admin-user-name-{user_id}")
    
    def get_user_email(self, user_id: str) -> str:
        """Get user email"""
        return self.get_text_by_testid(f"admin-user-email-{user_id}")
    
    def get_user_role(self, user_id: str) -> str:
        """Get user role"""
        return self.get_text_by_testid(f"admin-user-role-{user_id}")
    
    def click_edit_user(self, user_id: str):
        """Click edit button for user"""
        self.click_by_testid(f"admin-user-edit-{user_id}")
    
    def click_delete_user(self, user_id: str):
        """Click delete button for user"""
        self.click_by_testid(f"admin-user-{user_id}-delete-btn")
    
    def confirm_delete(self):
        """Confirm delete action"""
        self.click_by_testid(self.CONFIRM_BTN)
    
    # Note: confirm_browser_alert() is inherited from BasePage

    def is_edit_form_visible(self) -> bool:
        """Check if edit form is visible"""
        return self.is_visible_by_testid("user-edit-form", timeout=3)
    
    def fill_user_form(self, name: str = None, email: str = None):
        """Fill user edit form"""
        if name:
            self.type_by_testid("user-name-input", name)
        if email:
            self.type_by_testid("user-email-input", email)
    
    def click_save_user(self):
        """Click save button"""
        self.click_by_testid("save-form-btn")


class AdminOrdersPage(BasePage):
    """Admin orders page interactions"""
    
    # Test IDs
    ORDERS_LIST = "admin-orders-list"
    SEARCH_INPUT = "admin-search-input"
    
    # Alert modal
    CONFIRM_BTN = "confirm-alert-btn"
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    def open(self):
        """Navigate to admin orders"""
        self.navigate(Urls.ADMIN_ORDERS)
    
    def get_orders_count(self) -> int:
        """Get number of displayed orders"""
        cards = self.driver.find_elements(
            By.CSS_SELECTOR, '[data-testid^="order-card-"]'
        )
        return len(cards)
    
    def is_order_visible(self, order_id: str) -> bool:
        """Check if order card is visible"""
        return self.is_visible_by_testid(f"order-card-{order_id}", timeout=3)
    
    def get_order_status(self, order_id: str) -> str:
        """Get order status"""
        return self.get_text_by_testid(f"order-status-{order_id}")
    
    def click_change_status(self, order_id: str):
        """Click change status button"""
        self.click_by_testid(f"order-change-status-{order_id}")
    
    def select_status(self, status: str):
        """Select status from dropdown"""
        self.click_by_testid(f"status-option-{status}")
    
    def click_cancel_order(self, order_id: str):
        """Click cancel order button"""
        self.click_by_testid(f"order-cancel-{order_id}")
    
    def click_delete_order(self, order_id: str):
        """Click delete order button"""
        self.click_by_testid(f"order-{order_id}-delete-btn")
    
    def confirm_action(self):
        """Confirm action in modal"""
        self.click_by_testid(self.CONFIRM_BTN)

