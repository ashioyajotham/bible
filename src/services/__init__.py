"""
Scripture AI Agent Services
Core services for API integrations and data processing
"""

__version__ = "0.1.0"

from .gpt_service import GPTService
from .serper_service import SerperService

# Define default configurations
DEFAULT_GPT_MODEL = "gpt-4"
DEFAULT_SERPER_TIMEOUT = 10
DEFAULT_CACHE_SIZE = 100

__all__ = [
    'GPTService',
    'SerperService',
    'DEFAULT_GPT_MODEL',
    'DEFAULT_SERPER_TIMEOUT',
    'DEFAULT_CACHE_SIZE'
]