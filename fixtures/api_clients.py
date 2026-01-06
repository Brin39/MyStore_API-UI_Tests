"""
API client fixtures.
"""

import pytest
from infra.api_wrapper import ApiWrapper
from logic.api.auth_api import AuthApi
from logic.api.products_api import ProductsApi
from logic.api.cart_api import CartApi
from logic.api.orders_api import OrdersApi
from logic.api.admin_api import AdminApi


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

