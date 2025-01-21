"""
Scripture AI Agent Services
Core services for API integrations and data processing
"""

__version__ = "0.1.0"

from llm.hf_llm import HuggingFaceLLM
from .serper_service import SerperService

# Define default configurations
DEFAULT_MODEL = "llama-3.1-70B-Instruct"
DEFAULT_SERPER_TIMEOUT = 10
DEFAULT_CACHE_SIZE = 100

__all__ = [
    'HuggingFaceLLM',
    'SerperService',
    'DEFAULT_MODEL',
    'DEFAULT_SERPER_TIMEOUT',
    'DEFAULT_CACHE_SIZE'
]