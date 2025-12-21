"""
API wrapper - HTTP client for REST API calls.
Reusable across any API testing project.
"""

from typing import Optional, Dict, Any
import requests
from requests import Response

from infra.config_provider import ConfigProvider


class ApiWrapper:
    """Base HTTP client wrapper"""
    
    def __init__(self, base_url: str = None):
        self.config = ConfigProvider()
        self.base_url = base_url or self.config.api_url
        self.session = requests.Session()
        self.timeout = self.config.timeout
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint"""
        if endpoint.startswith("http"):
            return endpoint
        return f"{self.base_url}{endpoint}"
    
    @staticmethod
    def _build_headers(token: Optional[str] = None, extra_headers: Dict = None) -> Dict:
        """Build request headers"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        if extra_headers:
            headers.update(extra_headers)
        
        return headers
    
    def get(
        self,
        endpoint: str,
        token: str = None,
        params: Dict = None,
        headers: Dict = None
    ) -> Response:
        """HTTP GET request"""
        return self.session.get(
            self._build_url(endpoint),
            params=params,
            headers=self._build_headers(token, headers),
            timeout=self.timeout
        )
    
    def post(
        self,
        endpoint: str,
        data: Dict = None,
        token: str = None,
        headers: Dict = None
    ) -> Response:
        """HTTP POST request"""
        return self.session.post(
            self._build_url(endpoint),
            json=data,
            headers=self._build_headers(token, headers),
            timeout=self.timeout
        )
    
    def put(
        self,
        endpoint: str,
        data: Dict = None,
        token: str = None,
        headers: Dict = None
    ) -> Response:
        """HTTP PUT request"""
        return self.session.put(
            self._build_url(endpoint),
            json=data,
            headers=self._build_headers(token, headers),
            timeout=self.timeout
        )
    
    def patch(
        self,
        endpoint: str,
        data: Dict = None,
        token: str = None,
        headers: Dict = None
    ) -> Response:
        """HTTP PATCH request"""
        return self.session.patch(
            self._build_url(endpoint),
            json=data,
            headers=self._build_headers(token, headers),
            timeout=self.timeout
        )
    
    def delete(
        self,
        endpoint: str,
        token: str = None,
        headers: Dict = None
    ) -> Response:
        """HTTP DELETE request"""
        return self.session.delete(
            self._build_url(endpoint),
            headers=self._build_headers(token, headers),
            timeout=self.timeout
        )
    
    def close(self):
        """Close session"""
        self.session.close()

