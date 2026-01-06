"""
Configuration fixtures.
"""

import pytest
from infra.config_provider import ConfigProvider


@pytest.fixture(scope="session")
def config() -> ConfigProvider:
    """Get configuration provider"""
    return ConfigProvider()

