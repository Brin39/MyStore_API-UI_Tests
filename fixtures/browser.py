"""
Browser and page object fixtures.
"""

import pytest
from typing import Generator
from infra.browser_wrapper import BrowserWrapper
from logic.ui.login_page import LoginPage
from logic.ui.register_page import RegisterPage
from logic.ui.home_page import HomePage
from logic.ui.cart_page import CartPage
from logic.ui.orders_page import OrdersPage
from logic.ui.profile_page import ProfilePage
from logic.ui.admin_dashboard_page import AdminDashboardPage
from logic.ui.admin_products_page import AdminProductsPage
from logic.ui.admin_users_page import AdminUsersPage
from logic.ui.admin_orders_page import AdminOrdersPage


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

