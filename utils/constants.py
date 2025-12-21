"""
Constants - URLs, messages, timeouts.
Project-specific constants for MyStore.
"""


class Urls:
    """UI URLs"""
    HOME = "/"
    LOGIN = "/login"
    REGISTER = "/register"
    USER_HOME = "/user"
    CART = "/user/cart"
    ORDERS = "/user/orders"
    PROFILE = "/user/profile"
    ADMIN = "/admin"
    ADMIN_PRODUCTS = "/admin/products"
    ADMIN_USERS = "/admin/users"
    ADMIN_ORDERS = "/admin/orders"


class ApiEndpoints:
    """API endpoints"""
    # Auth
    REGISTER = "/api/users/register"
    LOGIN = "/api/users/login"
    PROFILE = "/api/users/profile"
    
    # Products
    PRODUCTS = "/api/products"
    PRODUCT_SEARCH = "/api/products/search"
    PRODUCT_BY_ID = "/api/products/{id}"
    
    # Cart
    CART = "/api/cart"
    CART_UPDATE = "/api/cart/update/{product_id}"
    CART_REMOVE = "/api/cart/{product_id}"
    CART_CLEAR = "/api/cart/clear"
    
    # Orders
    ORDERS = "/api/orders"
    MY_ORDERS = "/api/orders/my-orders"
    ORDER_BY_ID = "/api/orders/{id}"
    
    # Admin
    ADMIN_STATS = "/api/admin/stats"
    ADMIN_USERS = "/api/admin/users"
    ADMIN_USER = "/api/admin/users/{id}"
    ADMIN_USER_DETAILS = "/api/admin/users/{id}/details"
    ADMIN_PRODUCTS = "/api/admin/products"
    ADMIN_PRODUCT = "/api/admin/products/{id}"
    ADMIN_ORDERS = "/api/admin/orders"
    ADMIN_ORDER = "/api/admin/orders/{id}"
    ADMIN_REGISTER = "/api/admin/register"


class Messages:
    """Expected UI messages"""
    # Auth
    LOGIN_SUCCESS = "Login successful"
    REGISTER_SUCCESS = "Registration successful"
    INVALID_CREDENTIALS = "Invalid email or password"
    EMAIL_EXISTS = "Email already exists"
    
    # Cart
    CART_EMPTY = "Your cart is empty"
    ADDED_TO_CART = "Added to cart"
    
    # Orders
    ORDER_CREATED = "Order placed successfully"
    NO_ORDERS = "You haven't placed any orders yet"
    
    # Profile
    PROFILE_UPDATED = "Profile updated successfully"
    
    # Admin
    PRODUCT_CREATED = "Product created"
    PRODUCT_UPDATED = "Product updated"
    PRODUCT_DELETED = "Product deleted"


class OrderStatus:
    """Order status values"""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Timeouts:
    """Timeout values in seconds"""
    DEFAULT = 10
    SHORT = 5
    LONG = 30
    PAGE_LOAD = 15
    ELEMENT_WAIT = 10

