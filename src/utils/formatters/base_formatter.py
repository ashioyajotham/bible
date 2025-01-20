from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
import logging

class BaseFormatter(ABC):
    """Base class for formatting Bible Agent outputs"""
    
    @abstractmethod
    def format_verse(self, verse: Dict[str, Any]) -> str:
        """Format a verse output"""
        pass

    @abstractmethod
    def format_teaching(self, teaching: Dict[str, Any]) -> str:
        """Format a teaching output"""
        pass

    @abstractmethod
    def format_search_results(self, results: Dict[str, Any]) -> str:
        """Format search results"""
        pass