"""
Scripture AI Agent
Core package for Bible study and research assistant
"""

__version__ = "0.1.0"

from .agent.bible_agent import BibleAgent
from .agent.search_agent import SearchAgent
from .utils.helpers import setup_logging

# Configure package-level logging
setup_logging()

# Define core constants
PACKAGE_NAME = "scripture-ai-agent"
AUTHOR = "Scripture AI Team"
LICENSE = "MIT"

__all__ = [
    'BibleAgent',
    'SearchAgent',
    'PACKAGE_NAME',
    'AUTHOR',
    'LICENSE',
    '__version__'
]