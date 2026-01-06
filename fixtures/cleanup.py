"""
Cleanup and test data fixtures.
"""

import random
import logging
import pytest
from typing import Generator, Dict
from utils.data_factory import DataFactory
from utils.cleanup_utils import CleanupManager

logger = logging.getLogger(__name__)


@pytest.fixture
def data_factory() -> DataFactory:
    """Get data factory for unique test data"""
    return DataFactory()


@pytest.fixture
def cleanup(admin_api, auth_api, config) -> Generator[CleanupManager, None, None]:
    """
    Get cleanup manager.
    Cleans up all registered resources after test.
    Configures admin API BEFORE test to ensure cleanup works.
    If config admin fails, creates a test admin for cleanup.
    """
    manager = CleanupManager()
    cleanup_admin_id = None
    
    # Try to login with config admin first
    try:
        admin_result = auth_api.login(config.admin_email, config.admin_password)
        admin_token = admin_result.get("token")
        if admin_token:
            manager.set_admin_api(admin_api, admin_token)
            logger.debug("Cleanup manager configured with admin token from config")
        else:
            logger.warning("Failed to get admin token from config - will create test admin")
    except Exception as e:
        logger.warning(f"Failed to login with config admin: {e} - will create test admin for cleanup")
    
    # If admin API not configured, create a test admin for cleanup directly
    if not manager.admin_api or not manager.admin_token:
        try:
            admin_data = DataFactory.user(password="CleanupAdmin123")
            admin_data["name"] = f"CleanupAdmin_{admin_data['name']}"
            
            result = auth_api.register_admin(
                name=admin_data["name"],
                email=admin_data["email"],
                password=admin_data["password"],
                admin_code=config.admin_creation_code
            )
            
            cleanup_admin_id = result.get("_id") or result.get("user", {}).get("_id")
            admin_token = result.get("token")
            
            if admin_token and cleanup_admin_id:
                # Register cleanup admin for deletion (will be deleted last)
                manager.register_user(cleanup_admin_id, is_admin=True)
                manager.set_admin_api(admin_api, admin_token)
                logger.info(f"Cleanup manager configured with test admin token (admin_id: {cleanup_admin_id})")
            else:
                logger.warning("Failed to get token or ID from test admin - cleanup may not work")
        except Exception as e:
            logger.error(f"Failed to create test admin for cleanup: {e} - cleanup will not work")
    
    yield manager
    
    # Cleanup all registered resources after test
    # The cleanup admin (if created) will be deleted last as admin user
    manager.cleanup_all()


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
        
        # Register for cleanup - extract user_id from different possible response formats
        user_id = result.get("_id") or result.get("user", {}).get("_id")
        if user_id:
            cleanup.register_user(user_id)
        
        return {
            "user": result.get("user", result),
            "token": result.get("token"),
            "email": user_data["email"],
            "password": user_data["password"],
            "user_id": user_id
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
    Uses RANDOM product from database for test isolation.
    Returns function that creates order.
    """
    def _create_order(user_token: str, product: Dict = None) -> Dict:
        # Use provided product or get random one
        if product is None:
            products = products_api.get_all_products()
            if not products:
                raise ValueError("No products available in the database")
            product = random.choice(products)
        
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
def create_test_admin(auth_api, cleanup, config) -> callable:
    """
    Factory fixture to create test admin via API.
    Creates a NEW admin for each test with cleanup.
    Returns function that creates admin and returns admin data with token.
    """
    def _create_admin(
        name: str = None,
        email: str = None,
        password: str = "AdminPass123"
    ) -> Dict:
        admin_data = DataFactory.user(name=name, email=email, password=password)
        # Add "Admin" prefix to name for clarity
        if not name:
            admin_data["name"] = f"TestAdmin_{admin_data['name']}"
        
        result = auth_api.register_admin(
            name=admin_data["name"],
            email=admin_data["email"],
            password=admin_data["password"],
            admin_code=config.admin_creation_code
        )
        
        # Register for cleanup
        admin_id = result.get("_id") or result.get("user", {}).get("_id")
        admin_token = result.get("token")
        
        if admin_id:
            cleanup.register_user(admin_id, is_admin=True)  # Mark as admin - will be deleted last
        
        # Update cleanup to use created admin token (needed to delete resources created by this admin)
        if admin_token:
            from logic.api.admin_api import AdminApi
            admin_api = AdminApi()
            cleanup.set_admin_api(admin_api, admin_token)
        
        return {
            "user": result.get("user", result),
            "token": admin_token,
            "email": admin_data["email"],
            "password": admin_data["password"],
            "admin_id": admin_id
        }
    
    return _create_admin


@pytest.fixture
def get_random_product(products_api) -> callable:
    """
    Get a random product from existing products in the database.
    Each call returns a different random product WITH STOCK > 0.
    """
    def _get_product(min_stock: int = 1) -> Dict:
        products = products_api.get_all_products()
        if not products:
            raise ValueError("No products available in the database")
        
        # Filter products with sufficient stock
        available_products = [p for p in products if p.get("stock", 0) >= min_stock]
        if not available_products:
            raise ValueError(f"No products available with stock >= {min_stock}")
        
        return random.choice(available_products)
    
    return _get_product

