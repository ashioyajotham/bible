"""Scripture AI Agent Core Package for Bible study and research assistant"""

__version__ = "0.1.0"

# Import core components
from .agent.bible_agent import BibleAgent
from .agent.search_agent import SearchAgent
from .utils.helpers import setup_logging
from .config.settings import Config

# Configure package-level logging
setup_logging()

# Package metadata
PACKAGE_NAME = "scripture-ai-agent"
AUTHOR = "Scripture AI Team"
LICENSE = "MIT"
DESCRIPTION = "AI-powered Bible study and research assistant"

# Model configurations
DEFAULT_LLM = "gemini"
SUPPORTED_MODELS = ["gemini", "llama"]

__all__ = [
    'BibleAgent',
    'SearchAgent',
    'Config',
    'PACKAGE_NAME',
    'AUTHOR',
    'LICENSE',
    '__version__',
    'DEFAULT_LLM',
    'SUPPORTED_MODELS'
]