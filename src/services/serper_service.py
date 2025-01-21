import requests
from typing import Dict, List, Optional
import json
from datetime import datetime
import time
from functools import lru_cache
import logging

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
    def search(self, query: str) -> List[Dict]:
        """Perform search with enhanced result length"""
        try:
            url = "https://google.serper.dev/search"
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'q': f'biblical teaching {query}',
                'num': 5,  # Number of results
                'page': 1,
                'type': 'search',
                'snippetLength': 300  # Request longer snippets
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            return data.get('organic', [])[:5]  # Return top 5 results
            
        except Exception as e:
            logging.error(f"Search error: {str(e)}")
            return []

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