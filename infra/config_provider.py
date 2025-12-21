"""
Configuration provider - loads settings from config.json
Reusable across any project.
"""

import json
import os
from typing import Any


class ConfigProvider:
    """Singleton configuration provider"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from config.json"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "config",
            "config.json"
        )
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, "r", encoding="utf-8") as f:
            self._config = json.load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by key (supports dot notation)"""
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    @property
    def base_url(self) -> str:
        """Frontend base URL"""
        return self._config.get("base_url", "http://localhost:3000")
    
    @property
    def api_url(self) -> str:
        """API base URL"""
        return self._config.get("api_url", "http://localhost:5000")
    
    @property
    def timeout(self) -> int:
        """Default timeout in seconds"""
        return self._config.get("timeout", 10)
    
    @property
    def implicit_wait(self) -> int:
        """Selenium implicit wait in seconds"""
        return self._config.get("implicit_wait", 10)
    
    @property
    def headless(self) -> bool:
        """Run browser in headless mode"""
        return self._config.get("headless", False)
    
    @property
    def browser(self) -> str:
        """Browser type (chrome, firefox)"""
        return self._config.get("browser", "chrome")
    
    @property
    def admin_email(self) -> str:
        """Admin email for tests"""
        return self._config.get("admin", {}).get("email", "admin@test.com")
    
    @property
    def admin_password(self) -> str:
        """Admin password for tests"""
        return self._config.get("admin", {}).get("password", "Admin123456")
    
    @property
    def admin_creation_code(self) -> str:
        """Code required to create an admin account"""
        return self._config.get("admin_creation_code", "")

