import requests
from typing import Dict, List, Optional
import json
from datetime import datetime
import time
from functools import lru_cache

class SerperService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev"
        self.headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        self.timeout = 10
        self.max_retries = 3

    @lru_cache(maxsize=100)
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Execute search with retry logic"""
        endpoint = f"{self.base_url}/search"
        
        payload = {
            "q": query,
            "num": num_results
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    endpoint,
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return self._parse_results(response.json())
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Search failed after {self.max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff

    def _parse_results(self, raw_results: Dict) -> List[Dict]:
        """Parse and clean search results"""
        parsed = []
        
        for result in raw_results.get('organic', []):
            parsed.append({
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'snippet': result.get('snippet', ''),
                'date': result.get('date', ''),
                'position': result.get('position', 0)
            })
            
        return parsed

    def search_news(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search news articles"""
        endpoint = f"{self.base_url}/news"
        payload = {
            "q": query,
            "num": num_results
        }
        
        response = requests.post(
            endpoint,
            headers=self.headers,
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        return self._parse_news_results(response.json())

    def _parse_news_results(self, raw_results: Dict) -> List[Dict]:
        """Parse news search results"""
        return [{
            'title': item.get('title', ''),
            'link': item.get('link', ''),
            'snippet': item.get('snippet', ''),
            'date': item.get('date', ''),
            'source': item.get('source', '')
        } for item in raw_results.get('news', [])]

    def clear_cache(self):
        """Clear the search cache"""
        self.search.cache_clear()