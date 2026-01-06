"""
Authentication and browser login fixtures.
"""

import pytest
from typing import Dict


@pytest.fixture
def get_admin_token(auth_api, config) -> callable:
    """
    Get admin token for test setup.
    Uses configured admin credentials.
    NOTE: This uses shared admin from config. For isolated tests, use create_test_admin.
    """
    def _get_token() -> str:
        result = auth_api.login(
            email=config.admin_email,
            password=config.admin_password
        )
        return result.get("token")
    
    return _get_token


@pytest.fixture
def logged_in_browser(browser, create_test_user, login_page) -> Dict:
    """
    Fixture that provides browser with logged in user.
    Creates NEW user via API for each test, logs in via UI.
    User is automatically cleaned up after test.
    Returns dict with browser, user info, token from localStorage.
    """
    # Create user via API (unique for this test, will be cleaned up)
    user_data = create_test_user()
    
    # Get user_id from registration response
    user_id = user_data.get("user_id")
    
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


@pytest.fixture
def logged_in_admin_browser(browser, create_test_admin, login_page) -> Dict:
    """
    Fixture that provides browser with logged in admin.
    Creates NEW admin via API for each test, logs in via UI.
    Admin is automatically cleaned up after test.
    Returns dict with browser, admin info, token from localStorage.
    """
    # Create admin via API (unique for this test, will be cleaned up)
    admin_data = create_test_admin()
    
    # Get admin_id from registration response
    admin_id = admin_data.get("admin_id")
    
    # Login via UI
    login_page.open()
    login_page.login(admin_data["email"], admin_data["password"])
    
    # Wait for redirect
    login_page.wait_for_url_contains("/user")
    
    # Get token from browser localStorage
    browser_token = browser.driver.execute_script("return localStorage.getItem('token');")
    
    return {
        "browser": browser,
        "driver": browser.driver,
        "admin": admin_data["user"],
        "admin_id": admin_id,
        "token": browser_token,
        "email": admin_data["email"],
        "password": admin_data["password"]
    }

