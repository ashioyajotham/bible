import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SERPER_API_KEY = os.getenv('SERPER_API_KEY')
    BIBLE_API_KEY = os.getenv('BIBLE_API_KEY')
    BIBLE_API_BASE_URL = "https://bible-api.com"
    SERPER_API_BASE_URL = "https://google.serper.dev/search"