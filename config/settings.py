import os
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

# Load environment variables
load_dotenv()

@dataclass
class Config:
    # API Keys with fallbacks
    GEMINI_API_KEY: str = os.getenv('GEMINI_API_KEY', '')
    SERPER_API_KEY: str = os.getenv('SERPER_API_KEY', '')
    ESV_API_KEY: str = os.getenv('ESV_API_KEY', '') 
    HF_API_KEY: str = os.getenv('HF_API_KEY', '')
    
    # Model Configuration
    DEFAULT_MODEL: str = "phi-2"
    MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.7
    
    # File Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    CACHE_DIR: Path = PROJECT_ROOT / "cache"
    VERSES_DIR: Path = DATA_DIR / "verses"
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: Path = PROJECT_ROOT / "logs" / "bible_agent.log"
    
    # Search Configuration
    MAX_SEARCH_RESULTS: int = 5
    SEARCH_TIMEOUT: int = 10
    
    # Session Configuration
    MAX_MEMORY_ITEMS: int = 100
    MAX_FAVORITES: int = 50
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required_keys = ['GEMINI_API_KEY', 'SERPER_API_KEY']
        missing = [key for key in required_keys if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        return True
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist"""
        for directory in [cls.DATA_DIR, cls.CACHE_DIR, cls.LOG_FILE.parent, cls.VERSES_DIR]:
            directory.mkdir(parents=True, exist_ok=True)