"""
Products API client for MyStore.
Handles product listing and search operations.
"""

from typing import Dict, List
from infra.api_wrapper import ApiWrapper
from utils.constants import ApiEndpoints


class ProductsApi:
    """Products API operations (public)"""
    
    def __init__(self, api: ApiWrapper = None):
        self.api = api or ApiWrapper()
    
    def get_products(self, page: int = 1, limit: int = 20) -> Dict:
        """
        Get paginated list of products.
        
        Returns:
            dict with products list and pagination
        """
        response = self.api.get(
            ApiEndpoints.PRODUCTS,
            params={"page": page, "limit": limit}
        )
        response.raise_for_status()
        return response.json()
    
    def get_product_by_id(self, product_id: str) -> Dict:
        """
        Get product by ID.
        
        Returns:
            dict with product data
        """
        endpoint = ApiEndpoints.PRODUCT_BY_ID.format(id=product_id)
        response = self.api.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def search_products(self, query: str) -> List[Dict]:
        """
        Search products by query.
        
        Returns:
            list of matching products
        """
        response = self.api.get(
            ApiEndpoints.PRODUCT_SEARCH,
            params={"query": query}
        )
        response.raise_for_status()
        return response.json()
    
    def get_all_products(self) -> List[Dict]:
        """
        Get all products (for testing).
        
        Returns:
            list of all products
        """
        result = self.get_products(page=1, limit=1000)
        if isinstance(result, list):
            return result
        return result.get("products", [])

