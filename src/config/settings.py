import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SERPER_API_KEY = os.getenv('SERPER_API_KEY')
    BIBLE_API_KEY = os.getenv('BIBLE_API_KEY')
    BIBLE_API_BASE_URL = "https://bible-api.com"
    SERPER_API_BASE_URL = "https://google.serper.dev/search"
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    HF_MODEL_ID = os.getenv('HF_MODEL_ID', 'meta-llama/Llama-2-7b-chat-hf')
    ACTIVE_LLM = os.getenv('ACTIVE_LLM', 'gemini')  # gemini, llama
    
    # Daily verses for each month and day
    DAILY_VERSES = {
        # January
        "1-1": ("proverbs/16:9", "New Year - Fresh Start"),
        "1-7": ("2_corinthians/5:17", "New Beginnings"),
        
        # February
        "2-14": ("1_corinthians/13:4-7", "Valentine's Day - Love"),
        
        # March/April (Easter - needs calculation)
        "easter": ("john/11:25-26", "Easter Sunday"),
        "easter-2": ("matthew/28:6", "Easter Season"),
        
        # July
        "7-4": ("psalm/33:12", "Independence Day"),
        
        # November
        "11-25": ("psalm/100:4", "Thanksgiving"),
        
        # December
        "12-24": ("luke/2:10-11", "Christmas Eve"),
        "12-25": ("isaiah/9:6", "Christmas Day"),
        "12-31": ("psalm/90:12", "Year End")
    }
    
    # Season verses
    SEASONAL_VERSES = {
        "spring": ["song_of_solomon/2:11-12", "psalm/104:30"],
        "summer": ["psalm/74:17", "james/1:17"],
        "autumn": ["ecclesiastes/3:1-2", "psalm/126:5-6"],
        "winter": ["isaiah/1:18", "job/37:5-6"]
    }