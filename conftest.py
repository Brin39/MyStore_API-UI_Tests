"""
Pytest fixtures for MyStore E2E tests.
Provides browser, API clients, and test data management.
"""

import pytest
from typing import Generator, Dict

from infra.browser_wrapper import BrowserWrapper
from infra.api_wrapper import ApiWrapper
from infra.config_provider import ConfigProvider

from logic.api.auth_api import AuthApi
from logic.api.products_api import ProductsApi
from logic.api.cart_api import CartApi
from logic.api.orders_api import OrdersApi
from logic.api.admin_api import AdminApi

from logic.ui.login_page import LoginPage
from logic.ui.register_page import RegisterPage
from logic.ui.home_page import HomePage
from logic.ui.cart_page import CartPage
from logic.ui.orders_page import OrdersPage
from logic.ui.profile_page import ProfilePage
from logic.ui.admin_page import (
    AdminDashboardPage,
    AdminProductsPage,
    AdminUsersPage,
    AdminOrdersPage
)

from utils.data_factory import DataFactory
from utils.cleanup_utils import CleanupManager


# ==================== CONFIG ====================

@pytest.fixture(scope="session")
def config() -> ConfigProvider:
    """Get configuration provider"""
    return ConfigProvider()


# ==================== API CLIENTS ====================

@pytest.fixture(scope="session")
def api() -> ApiWrapper:
    """Get API wrapper"""
    return ApiWrapper()


@pytest.fixture(scope="session")
def auth_api(api) -> AuthApi:
    """Get Auth API client"""
    return AuthApi(api)


@pytest.fixture(scope="session")
def products_api(api) -> ProductsApi:
    """Get Products API client"""
    return ProductsApi(api)


@pytest.fixture(scope="session")
def cart_api(api) -> CartApi:
    """Get Cart API client"""
    return CartApi(api)


@pytest.fixture(scope="session")
def orders_api(api) -> OrdersApi:
    """Get Orders API client"""
    return OrdersApi(api)


@pytest.fixture(scope="session")
def admin_api(api) -> AdminApi:
    """Get Admin API client"""
    return AdminApi(api)


# ==================== BROWSER ====================

@pytest.fixture(scope="function")
def browser() -> Generator[BrowserWrapper, None, None]:
    """
    Get browser wrapper for each test.
    Automatically closes after test.
    """
    browser_wrapper = BrowserWrapper()
    browser_wrapper.start()
    
    yield browser_wrapper
    
    browser_wrapper.stop()


@pytest.fixture(scope="function")
def driver(browser):
    """Get Selenium WebDriver"""
    return browser.driver


# ==================== PAGE OBJECTS ====================

@pytest.fixture
def login_page(driver) -> LoginPage:
    """Get Login page object"""
    return LoginPage(driver)


@pytest.fixture
def register_page(driver) -> RegisterPage:
    """Get Register page object"""
    return RegisterPage(driver)


@pytest.fixture
def home_page(driver) -> HomePage:
    """Get Home page object"""
    return HomePage(driver)


@pytest.fixture
def cart_page(driver) -> CartPage:
    """Get Cart page object"""
    return CartPage(driver)


@pytest.fixture
def orders_page(driver) -> OrdersPage:
    """Get Orders page object"""
    return OrdersPage(driver)


@pytest.fixture
def profile_page(driver) -> ProfilePage:
    """Get Profile page object"""
    return ProfilePage(driver)


@pytest.fixture
def admin_dashboard(driver) -> AdminDashboardPage:
    """Get Admin Dashboard page object"""
    return AdminDashboardPage(driver)


@pytest.fixture
def admin_products_page(driver) -> AdminProductsPage:
    """Get Admin Products page object"""
    return AdminProductsPage(driver)


@pytest.fixture
def admin_users_page(driver) -> AdminUsersPage:
    """Get Admin Users page object"""
    return AdminUsersPage(driver)


@pytest.fixture
def admin_orders_page(driver) -> AdminOrdersPage:
    """Get Admin Orders page object"""
    return AdminOrdersPage(driver)


# ==================== TEST DATA ====================

@pytest.fixture
def data_factory() -> DataFactory:
    """Get data factory for unique test data"""
    return DataFactory()


@pytest.fixture
def cleanup(admin_api, auth_api, config) -> Generator[CleanupManager, None, None]:
    """
    Get cleanup manager.
    Cleans up all registered resources after test.
    """
    manager = CleanupManager()
    
    yield manager
    
    # Get admin token and configure cleanup
    try:
        admin_result = auth_api.login(config.admin_email, config.admin_password)
        admin_token = admin_result.get("token")
        manager.set_admin_api(admin_api, admin_token)
    except Exception:
        pass
    
    manager.cleanup_all()


# ==================== AUTH HELPERS ====================

@pytest.fixture
def create_test_user(auth_api, cleanup) -> callable:
    """
    Factory fixture to create test user via API.
    Returns function that creates user and returns (user_data, token).
    """
    def _create_user(
        name: str = None,
        email: str = None,
        password: str = "TestPass123"
    ) -> Dict:
        user_data = DataFactory.user(name=name, email=email, password=password)
        result = auth_api.register(
            name=user_data["name"],
            email=user_data["email"],
            password=user_data["password"]
        )
        
        # Register for cleanup
        if "_id" in result:
            cleanup.register_user(result["_id"])
        elif "user" in result and "_id" in result["user"]:
            cleanup.register_user(result["user"]["_id"])
        
        return {
            "user": result.get("user", result),
            "token": result.get("token"),
            "email": user_data["email"],
            "password": user_data["password"]
        }
    
    return _create_user


@pytest.fixture
def create_test_product(admin_api, config, cleanup) -> callable:
    """
    Factory fixture to create test product via API.
    Requires admin token. Returns function that creates product.
    """
    def _create_product(
        admin_token: str,
        name: str = None,
        price: float = 99.99,
        stock: int = 100,
        best_offer: bool = False
    ) -> Dict:
        product_data = DataFactory.product(
            name=name,
            price=price,
            stock=stock,
            best_offer=best_offer
        )
        result = admin_api.create_product(product_data, admin_token)
        
        # Register for cleanup
        product_id = result.get("_id") or result.get("product", {}).get("_id")
        if product_id:
            cleanup.register_product(product_id)
        
        return result
    
    return _create_product


@pytest.fixture
def create_test_order(orders_api, products_api, cleanup) -> callable:
    """
    Factory fixture to create test order via API.
    Returns function that creates order.
    """
    def _create_order(user_token: str) -> Dict:
        products = products_api.get_all_products()
        product = products[0]
        
        result = orders_api.create_order(
            items=[{"product": product["_id"], "quantity": 1}],
            total_amount=product["price"],
            token=user_token
        )
        
        # Register for cleanup
        order_id = result.get("_id") or result.get("order", {}).get("_id")
        if order_id:
            cleanup.register_order(order_id)
        
        return result
    
    return _create_order


@pytest.fixture
def get_admin_token(auth_api, config) -> callable:
    """
    Get admin token for test setup.
    Uses configured admin credentials.
    """
    def _get_token() -> str:
        result = auth_api.login(
            email=config.admin_email,
            password=config.admin_password
        )
        return result.get("token")
    
    return _get_token


# ==================== BROWSER AUTH HELPERS ====================

@pytest.fixture
def logged_in_browser(browser, create_test_user, login_page) -> Dict:
    """
    Fixture that provides browser with logged in user.
    Creates user via API, logs in via UI.
    Returns dict with browser, user info, token from localStorage.
    """
    # Create user via API
    user_data = create_test_user()
    
    # Get user_id from registration response
    user_id = user_data.get("user", {}).get("_id")
    
    # Login via UI
    login_page.open()
    login_page.login(user_data["email"], user_data["password"])
    
    # Wait for redirect
    login_page.wait_for_url_contains("/user")
    
    # Get token from browser localStorage (SAME token that UI uses)
    browser_token = browser.driver.execute_script("return localStorage.getItem('token');")
    
    return {
        "browser": browser,
        "driver": browser.driver,
        "user": user_data["user"],
        "user_id": user_id,
        "token": browser_token,
        "email": user_data["email"],
        "password": user_data["password"]
    }

