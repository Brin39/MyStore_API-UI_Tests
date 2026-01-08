# MyStore API & UI Test Automation Framework

A comprehensive end-to-end test automation framework for MyStore e-commerce application, implementing both API and UI testing using Python, pytest, and Selenium WebDriver.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Organization](#test-organization)
- [Architecture](#architecture)
- [Page Object Model](#page-object-model)
- [API Testing](#api-testing)
- [Test Data Management](#test-data-management)
- [Cleanup Mechanism](#cleanup-mechanism)
- [Reporting](#reporting)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This test automation framework provides comprehensive coverage for the MyStore e-commerce platform, testing both the user-facing UI and backend API. The framework follows industry best practices including:

- **Page Object Model (POM)** for UI test organization
- **API client abstraction** for backend testing
- **Automatic test data cleanup** after test execution
- **Modular fixture architecture** for maintainability
- **Parallel test execution** support
- **Comprehensive test reporting**

## ✨ Features

- **Dual Testing Approach**: Both API and UI testing capabilities
- **Page Object Model**: Maintainable and reusable UI test code
- **Automatic Cleanup**: Test data is automatically cleaned up after execution
- **Fixture-Based Architecture**: Modular and reusable test fixtures
- **Parallel Execution**: Support for running tests in parallel using pytest-xdist
- **HTML Reporting**: Generate detailed HTML test reports
- **Test Markers**: Organize tests by category (smoke, regression, auth, cart, etc.)
- **Data Factory**: Generate unique test data dynamically
- **Browser Management**: Automatic WebDriver management with webdriver-manager
- **Configuration Management**: Centralized configuration via JSON

## 📁 Project Structure

```
MyStore_API&UI_Tests/
│
├── config/
│   └── config.json              # Application configuration
│
├── fixtures/                    # Pytest fixtures
│   ├── api_clients.py           # API client fixtures
│   ├── auth.py                  # Authentication fixtures
│   ├── browser.py               # Browser and page object fixtures
│   ├── cleanup.py               # Test data creation fixtures
│   └── config.py                # Configuration fixtures
│
├── infra/                       # Infrastructure layer
│   ├── api_wrapper.py          # HTTP request wrapper
│   ├── browser_wrapper.py      # Selenium WebDriver wrapper
│   └── config_provider.py      # Configuration loader
│
├── logic/                       # Business logic layer
│   ├── api/                    # API clients
│   │   ├── admin_api.py        # Admin API operations
│   │   ├── auth_api.py         # Authentication API
│   │   ├── cart_api.py         # Shopping cart API
│   │   ├── orders_api.py       # Orders API
│   │   └── products_api.py     # Products API
│   │
│   └── ui/                     # Page Objects
│       ├── base_page.py        # Base page class
│       ├── home_page.py        # Home page
│       ├── login_page.py       # Login page
│       ├── register_page.py    # Registration page
│       ├── cart_page.py        # Shopping cart page
│       ├── orders_page.py      # User orders page
│       ├── profile_page.py     # User profile page
│       ├── admin_dashboard_page.py
│       ├── admin_products_page.py
│       ├── admin_users_page.py
│       └── admin_orders_page.py
│
├── tests/                       # Test cases
│   ├── test_login_*.py         # Authentication tests
│   ├── test_register_*.py      # Registration tests
│   ├── test_add_product_to_cart.py
│   ├── test_clear_cart.py
│   ├── test_checkout_creates_order.py
│   ├── test_admin_*.py         # Admin panel tests
│   └── ...
│
├── utils/                       # Utility modules
│   ├── constants.py            # Application constants
│   ├── data_factory.py        # Test data generation
│   └── cleanup_utils.py       # Cleanup manager
│
├── conftest.py                 # Main pytest configuration
├── pytest.ini                  # Pytest settings
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Prerequisites

- **Python 3.8+**
- **Google Chrome** browser (for UI tests)
- **MyStore Application** running locally or remotely
- **pip** (Python package manager)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Brin39/MyStore_API-UI_Tests.git
   cd MyStore_API-UI_Tests
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application:**
   - Edit `config/config.json` with your application URLs and credentials
   - See [Configuration](#configuration) section for details

## ⚙️ Configuration

The framework uses `config/config.json` for configuration. Example:

```json
{
    "base_url": "http://localhost:3000",
    "api_url": "http://localhost:5000",
    "timeout": 10,
    "implicit_wait": 10,
    "headless": false,
    "browser": "chrome",
    "admin": {
        "email": "admin@gmail.com",
        "password": "your_admin_password"
    },
    "admin_creation_code": "your_admin_creation_code"
}
```

### Configuration Parameters

- **base_url**: Frontend application URL
- **api_url**: Backend API URL
- **timeout**: Default timeout for UI operations (seconds)
- **implicit_wait**: Selenium implicit wait time (seconds)
- **headless**: Run browser in headless mode (true/false)
- **browser**: Browser type (currently supports "chrome")
- **admin.email**: Admin user email for cleanup operations
- **admin.password**: Admin user password
- **admin_creation_code**: Code required for admin user creation

## 🚀 Running Tests

### Run All Tests
```bash
pytest
```

### Run Tests with HTML Report
```bash
pytest --html=report.html --self-contained-html
```

### Run Tests in Parallel
```bash
pytest -n auto
```

### Run Tests by Marker
```bash
# Smoke tests only
pytest -m smoke

# Authentication tests
pytest -m auth

# Cart tests
pytest -m cart

# Admin tests
pytest -m admin

# E2E tests
pytest -m e2e
```

### Run Specific Test File
```bash
pytest tests/test_login_valid_credentials.py
```

### Run Specific Test
```bash
pytest tests/test_login_valid_credentials.py::TestLoginValidCredentials::test_login_with_valid_credentials_success
```

### Run Tests with Verbose Output
```bash
pytest -v
```

### Run Tests with Detailed Failure Information
```bash
pytest -v --tb=long
```

## 🏷️ Test Organization

Tests are organized using pytest markers defined in `pytest.ini`:

- **@pytest.mark.smoke**: Quick smoke tests for critical functionality
- **@pytest.mark.regression**: Full regression test suite
- **@pytest.mark.auth**: Authentication-related tests
- **@pytest.mark.cart**: Shopping cart functionality tests
- **@pytest.mark.orders**: Order management tests
- **@pytest.mark.products**: Product-related tests
- **@pytest.mark.admin**: Admin panel tests
- **@pytest.mark.e2e**: End-to-end workflow tests

## 🏗️ Architecture

### Page Object Model (POM)

The framework follows the Page Object Model pattern, where each page of the application has a corresponding Page Object class that encapsulates:

- **Element locators** (using `data-testid` attributes)
- **Page interactions** (clicks, inputs, navigation)
- **Page state verification** (element visibility, text content)

**Example Page Object:**
```python
class LoginPage(BasePage):
    """Login page interactions"""
    
    EMAIL_INPUT = "email-input"
    PASSWORD_INPUT = "password-input"
    LOGIN_BTN = "login-btn"
    
    def login(self, email: str, password: str):
        """Login with credentials"""
        self.type_by_testid(self.EMAIL_INPUT, email)
        self.type_by_testid(self.PASSWORD_INPUT, password)
        self.click_by_testid(self.LOGIN_BTN)
```

### API Client Layer

API clients provide a clean interface for backend testing:

```python
# Example: Using CartApi
cart_api.add_to_cart(product_id, quantity, token)
cart = cart_api.get_cart(token)
cart_api.clear_cart(token)
```

### Fixture Architecture

Fixtures are organized into modules:

- **fixtures/api_clients.py**: API client fixtures (auth_api, products_api, etc.)
- **fixtures/auth.py**: Authentication fixtures (logged_in_browser, logged_in_admin_browser)
- **fixtures/browser.py**: Browser and page object fixtures
- **fixtures/cleanup.py**: Test data creation fixtures (create_test_user, create_test_product, etc.)
- **fixtures/config.py**: Configuration fixtures

## 📄 Page Object Model Details

### Base Page

All page objects inherit from `BasePage`, which provides common functionality:

- Element location by `data-testid`
- Wait utilities (explicit waits)
- Navigation methods
- Common UI interactions

### Page Object Methods

Page objects expose high-level methods that hide Selenium implementation details:

```python
# Instead of:
driver.find_element(By.CSS_SELECTOR, '[data-testid="login-btn"]').click()

# Use:
login_page.click_by_testid("login-btn")
```

### Wait Methods

Page objects include wait methods for async operations:

```python
home_page.wait_for_search_results(expected_count=1)
cart_page.wait_for_cart_empty()
cart_page.wait_for_item_quantity(product_id, expected_quantity)
```

## 🔌 API Testing

### API Clients

The framework includes dedicated API clients for each domain:

- **AuthApi**: User authentication, registration, profile management
- **ProductsApi**: Product listing, search, details
- **CartApi**: Shopping cart operations
- **OrdersApi**: Order creation and management
- **AdminApi**: Admin operations (user/product/order management)

### Example API Test

```python
def test_api_create_order(create_test_user, create_test_order, orders_api):
    user_data = create_test_user()
    order = create_test_order(user_data["token"])
    
    assert order is not None
    assert order.get("status") == "pending"
```

## 🗄️ Test Data Management

### Data Factory

The `DataFactory` utility generates unique test data:

```python
from utils.data_factory import DataFactory

# Generate unique email
email = f"test_{DataFactory.unique_id()}@example.com"

# Generate product data
product_data = DataFactory.product(name="Test Product", price=99.99)
```

### Test Data Creation Fixtures

Fixtures automatically create and register test data for cleanup:

- **create_test_user()**: Creates a test user via API
- **create_test_product(admin_token)**: Creates a test product
- **create_test_order(user_token)**: Creates a test order
- **create_test_admin()**: Creates a test admin user

## 🧹 Cleanup Mechanism

The framework automatically cleans up test data after test execution:

### How It Works

1. **Registration**: Test fixtures register created resources (users, products, orders)
2. **Cleanup Manager**: Tracks all registered resources
3. **Automatic Cleanup**: After test completion, `cleanup` fixture deletes all registered resources

### Cleanup Order

1. Orders (first)
2. Products
3. Regular users
4. Admin users (last, as they're needed for cleanup)

### Manual Registration

If you create resources outside of fixtures, register them manually:

```python
def test_custom_creation(admin_api, cleanup, token):
    product = admin_api.create_product(product_data, token)
    cleanup.register_product(product["_id"])
```

## 📊 Reporting

### HTML Reports

Generate detailed HTML reports:

```bash
pytest --html=report.html --self-contained-html
```

The report includes:
- Test execution summary
- Pass/fail status
- Execution time
- Error messages and stack traces
- Screenshots (if configured)

### Console Output

Default pytest output shows:
- Test names and status
- Failure messages
- Execution time

## 💡 Best Practices

### 1. Use Page Objects

Always interact with UI through page objects, never directly with Selenium:

```python
# ✅ Good
home_page.search("product name")

# ❌ Bad
driver.find_element(By.ID, "search").send_keys("product name")
```

### 2. Use Fixtures for Test Data

Leverage fixtures for creating test data:

```python
# ✅ Good
def test_cart(user_data, cart_api):
    cart_api.add_to_cart(product_id, 1, user_data["token"])

# ❌ Bad
# Creating users/products manually without cleanup
```

### 3. Keep Tests Independent

Each test should be independent and not rely on other tests:

```python
# ✅ Good - Each test creates its own data
def test_1(create_test_user):
    user = create_test_user()
    # test logic

def test_2(create_test_user):
    user = create_test_user()
    # test logic
```

### 4. Use Descriptive Test Names

Test names should clearly describe what they test:

```python
# ✅ Good
def test_login_with_invalid_password_shows_error(self):
    pass

# ❌ Bad
def test_login(self):
    pass
```

### 5. Arrange-Act-Assert Pattern

Structure tests using AAA pattern:

```python
def test_example(self):
    # Arrange
    user = create_test_user()
    
    # Act
    result = perform_action(user)
    
    # Assert
    assert result == expected
```

### 6. Use Wait Methods

Always use page object wait methods instead of `time.sleep()`:

```python
# ✅ Good
cart_page.wait_for_cart_empty()

# ❌ Bad
import time
time.sleep(2)
```

## 🐛 Troubleshooting

### Common Issues

#### 1. WebDriver Not Found
**Error**: `WebDriverException: 'chromedriver' executable needs to be in PATH`

**Solution**: The framework uses `webdriver-manager` which automatically downloads drivers. Ensure you have internet connection on first run.

#### 2. Tests Failing Due to Timeouts
**Error**: `TimeoutException: Message:`

**Solution**: 
- Increase timeout in `config/config.json`
- Check if application is running and accessible
- Verify network connectivity

#### 3. Cleanup Failing
**Error**: `401 Unauthorized` during cleanup

**Solution**: 
- Verify admin credentials in `config/config.json`
- Ensure admin user has proper permissions
- Check API connectivity

#### 4. Tests Not Running in Parallel
**Error**: Tests fail when running with `-n auto`

**Solution**: 
- Some tests may share state - ensure tests are independent
- Use `pytest-xdist` markers to control parallel execution
- Check for shared resources (database, files)

#### 5. Import Errors
**Error**: `ModuleNotFoundError: No module named 'logic'`

**Solution**: 
- Ensure you're in the project root directory
- Activate virtual environment
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Debug Mode

Run tests with maximum verbosity for debugging:

```bash
pytest -vvv --tb=long --capture=no
```

### Browser Debugging

To see browser during test execution:
- Set `"headless": false` in `config/config.json`
- Add `time.sleep()` temporarily to pause execution

## 📝 Writing New Tests

### Example: New UI Test

```python
"""
Test description.
"""

import pytest


class TestNewFeature:
    """Test new feature"""
    
    @pytest.mark.smoke
    def test_new_feature_works(
        self,
        logged_in_browser,
        home_page
    ):
        """
        Test new feature works correctly.
        
        Arrange: Setup test data
        Act: Perform actions
        Assert: Verify results
        """
        # Arrange
        user_data = logged_in_browser
        
        # Act
        home_page.open()
        result = home_page.perform_action()
        
        # Assert
        assert result == expected_value
```

### Example: New API Test

```python
"""
Test API endpoint.
"""

import pytest


class TestNewApiEndpoint:
    """Test new API endpoint"""
    
    @pytest.mark.api
    def test_api_endpoint_works(
        self,
        auth_api,
        create_test_user
    ):
        """Test API endpoint returns correct data"""
        # Arrange
        user = create_test_user()
        token = user["token"]
        
        # Act
        result = auth_api.get_endpoint(token)
        
        # Assert
        assert result is not None
        assert result.get("field") == expected_value
```

## 🤝 Contributing

When contributing to this project:

1. Follow the existing code structure and patterns
2. Write tests for new functionality
3. Ensure all tests pass before submitting
4. Update documentation as needed
5. Use meaningful commit messages

## 📄 License

[Specify your license here]

## 👥 Authors

[Gidon Brin]

## 🙏 Acknowledgments

- pytest team for the excellent testing framework
- Selenium team for browser automation tools
- All contributors to the open-source libraries used

---

For questions or issues, please open an issue in the repository.

