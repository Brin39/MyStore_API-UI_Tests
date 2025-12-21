"""
Browser wrapper - Selenium WebDriver management.
Reusable across any web testing project.
"""

import os
from datetime import datetime
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from infra.config_provider import ConfigProvider


class BrowserWrapper:
    """WebDriver wrapper with automatic setup and teardown"""
    
    def __init__(self):
        self.config = ConfigProvider()
        self.driver: Optional[WebDriver] = None
        self._screenshots_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "screenshots"
        )
    
    def start(self) -> WebDriver:
        """Initialize and return WebDriver"""
        browser_type = self.config.browser.lower()
        
        if browser_type == "chrome":
            self.driver = self._create_chrome_driver()
        elif browser_type == "firefox":
            self.driver = self._create_firefox_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser_type}")
        
        self.driver.implicitly_wait(self.config.implicit_wait)
        self.driver.set_window_size(1920, 1080)
        
        return self.driver
    
    def _create_chrome_driver(self) -> WebDriver:
        """Create Chrome WebDriver"""
        options = ChromeOptions()
        
        if self.config.headless:
            options.add_argument("--headless=new")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        
        # Suppress logging
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _create_firefox_driver(self) -> WebDriver:
        """Create Firefox WebDriver"""
        options = FirefoxOptions()
        
        if self.config.headless:
            options.add_argument("--headless")
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    def stop(self):
        """Close browser and cleanup"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            finally:
                self.driver = None
    
    def take_screenshot(self, name: str = None) -> str:
        """Take screenshot and return path"""
        if not self.driver:
            return ""
        
        # Create screenshots directory if not exists
        os.makedirs(self._screenshots_dir, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png" if name else f"screenshot_{timestamp}.png"
        filepath = os.path.join(self._screenshots_dir, filename)
        
        self.driver.save_screenshot(filepath)
        return filepath
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url if self.driver else ""
    
    def refresh(self):
        """Refresh current page"""
        if self.driver:
            self.driver.refresh()
    
    def clear_cookies(self):
        """Clear all cookies"""
        if self.driver:
            self.driver.delete_all_cookies()
    
    def clear_local_storage(self):
        """Clear localStorage"""
        if self.driver:
            self.driver.execute_script("window.localStorage.clear();")
    
    def clear_session_storage(self):
        """Clear sessionStorage"""
        if self.driver:
            self.driver.execute_script("window.sessionStorage.clear();")

