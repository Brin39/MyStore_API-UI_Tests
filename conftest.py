"""
Pytest fixtures for MyStore E2E tests.
All fixtures are organized in separate modules for better maintainability.
"""

# Register fixture modules so pytest can discover them
pytest_plugins = [
    "fixtures.config",
    "fixtures.api_clients",
    "fixtures.browser",
    "fixtures.cleanup",
    "fixtures.auth"
]
