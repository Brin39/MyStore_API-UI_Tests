"""
Base Page Object - common functionality for all pages.
"""

from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from infra.config_provider import ConfigProvider


class BasePage:
    """Base class for all Page Objects"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.config = ConfigProvider()
        self.wait = WebDriverWait(driver, self.config.timeout)
        self.base_url = self.config.base_url
    
    # ==================== NAVIGATION ====================
    
    def navigate(self, path: str = ""):
        """Navigate to path relative to base URL"""
        url = f"{self.base_url}{path}"
        self.driver.get(url)
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
    
    def refresh(self):
        """Refresh current page"""
        self.driver.refresh()
    
    # ==================== ELEMENT FINDING ====================
    
    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """Find element with explicit wait"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Find all elements matching locator"""
        return self.driver.find_elements(*locator)
    
    def find_clickable(self, locator: Tuple[str, str]) -> WebElement:
        """Find clickable element"""
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def find_visible(self, locator: Tuple[str, str]) -> WebElement:
        """Find visible element"""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    # ==================== ELEMENT BY TEST ID ====================
    
    def find_by_testid(self, testid: str) -> WebElement:
        """Find element by data-testid attribute"""
        locator = (By.CSS_SELECTOR, f'[data-testid="{testid}"]')
        return self.find_element(locator)
    
    def find_all_by_testid(self, testid: str) -> List[WebElement]:
        """Find all elements by data-testid attribute"""
        locator = (By.CSS_SELECTOR, f'[data-testid="{testid}"]')
        return self.find_elements(locator)
    
    def click_by_testid(self, testid: str):
        """Click element by data-testid"""
        locator = (By.CSS_SELECTOR, f'[data-testid="{testid}"]')
        self.find_clickable(locator).click()
    
    def get_text_by_testid(self, testid: str) -> str:
        """Get text from element by data-testid"""
        return self.find_by_testid(testid).text
    
    def is_visible_by_testid(self, testid: str, timeout: int = None) -> bool:
        """Check if element is visible by data-testid"""
        timeout = timeout or self.config.timeout
        try:
            locator = (By.CSS_SELECTOR, f'[data-testid="{testid}"]')
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_present_by_testid(self, testid: str) -> bool:
        """Check if element is present in DOM by data-testid"""
        locator = (By.CSS_SELECTOR, f'[data-testid="{testid}"]')
        elements = self.find_elements(locator)
        return len(elements) > 0
    
    # ==================== ACTIONS ====================
    
    def click(self, locator: Tuple[str, str]):
        """Click element"""
        self.find_clickable(locator).click()
    
    def type_text(self, locator: Tuple[str, str], text: str, clear: bool = True):
        """Type text into input"""
        element = self.find_element(locator)
        if clear:
            element.clear()
        element.send_keys(text)
    
    def type_by_testid(self, testid: str, text: str, clear: bool = True):
        """Type text into input by data-testid"""
        element = self.find_by_testid(testid)
        if clear:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """Get element text"""
        return self.find_element(locator).text
    
    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """Get element attribute"""
        return self.find_element(locator).get_attribute(attribute)
    
    def get_attribute_by_testid(self, testid: str, attribute: str) -> str:
        """Get element attribute by data-testid"""
        return self.find_by_testid(testid).get_attribute(attribute)
    
    # ==================== VISIBILITY ====================
    
    def is_visible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Check if element is visible"""
        timeout = timeout or self.config.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_present(self, locator: Tuple[str, str]) -> bool:
        """Check if element is present in DOM"""
        elements = self.find_elements(locator)
        return len(elements) > 0
    
    def wait_for_url_contains(self, text: str, timeout: int = None) -> bool:
        """Wait until URL contains text"""
        timeout = timeout or self.config.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(text)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_invisible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Wait until element becomes invisible"""
        timeout = timeout or self.config.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

