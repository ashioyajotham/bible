import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API keys
    GPT_API_KEY = os.getenv('GPT_API_KEY')
    SERPER_API_KEY = os.getenv('SERPER_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    BIBLE_API_KEY = os.getenv('BIBLE_API_KEY')  # for bible-api.com

    # Application settings
    DEBUG = True
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///scripture_ai_agent.db')

    # Other constants
    DAILY_VERSE_URL = "https://api.example.com/daily-verse"
    TEACHINGS_URL = "https://api.example.com/jesus-teachings"
    INSIGHTS_URL = "https://api.example.com/insights"
    BIBLE_API_BASE_URL = "https://bible-api.com"
    SERPER_API_BASE_URL = "https://google.serper.dev/search"