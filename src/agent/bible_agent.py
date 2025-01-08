import random
import requests
import json
import logging
from datetime import datetime
from src.services.gpt_service import GPTService 
from src.services.serper_service import SerperService
from src.models.verse import Verse
from src.config.settings import Config
from src.services.llm.gemini_llm import GeminiLLM
from src.services.llm.hf_llm import HuggingFaceLLM

from dotenv import load_dotenv
load_dotenv()

class BibleAgent:
    def __init__(self):
        if Config.ACTIVE_LLM == 'gemini':
            self.llm = GeminiLLM(api_key=Config.GEMINI_API_KEY)
        else:
            self.llm = HuggingFaceLLM(model_id=Config.HF_MODEL_ID)
        self.serper = SerperService(api_key=Config.SERPER_API_KEY)
        self.favorites = []
        
    def get_daily_verse(self) -> Verse:
        """Get verse based on date or season"""
        today = datetime.now()
        date_key = f"{today.month}-{today.day}"
        
        # Check for special date
        if date_key in Config.DAILY_VERSES:
            verse_ref, occasion = Config.DAILY_VERSES[date_key]
        else:
            # Get season verse as fallback
            seasons = {
                1: "winter", 2: "winter", 3: "spring",
                4: "spring", 5: "spring", 6: "summer",
                7: "summer", 8: "summer", 9: "autumn",
                10: "autumn", 11: "autumn", 12: "winter"
            }
            current_season = seasons[today.month]
            verse_ref = random.choice(Config.SEASONAL_VERSES[current_season])
        
        try:
            response = requests.get(f"{Config.BIBLE_API_BASE_URL}/{verse_ref}")
            response.raise_for_status()
            data = response.json()
            
            return Verse(
                reference=data.get('reference', verse_ref),
                text=data.get('text', '').strip(),
                translation=data.get('translation_name', 'KJV')
            )
        except Exception as e:
            logging.error(f"Error fetching verse: {str(e)}")
            return None

    def get_teachings(self, topic: str = None) -> list:
        """Get Jesus's teachings, optionally filtered by topic"""
        prompt = f"What did Jesus teach about {topic}" if topic else "Share an important teaching of Jesus"
        
        # Get GPT-4 insights
        gpt_insight = self.gpt.get_completion(prompt)
        
        # Get online resources via serper
        search_results = self.serper.search(f"Jesus teachings {topic}" if topic else "Jesus main teachings")
        
        return {
            "ai_insight": gpt_insight,
            "references": search_results[:3]
        }

    def generate_reflection(self, verse: Verse) -> str:
        """Generate a reflection on a Bible verse using GPT-4"""
        prompt = f"Provide a deep spiritual reflection on this verse: {verse.text} ({verse.reference})"
        return self.llm.generate(prompt)

    def save_favorite(self, verse: Verse):
        """Save a verse to favorites"""
        self.favorites.append(verse)

    def export_to_markdown(self, content, filename: str):
        """Export content to markdown file"""
        with open(f"{filename}.md", "w") as f:
            f.write(f"# Scripture Study - {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write(content)

    def search_biblical_insights(self, query: str) -> dict:
        """Search for biblical insights using both GPT and online sources"""
        gpt_analysis = self.gpt.get_completion(f"Provide biblical insight on: {query}")
        online_results = self.serper.search(f"biblical meaning {query}")
        
        return {
            "ai_analysis": gpt_analysis,
            "online_sources": online_results[:3],
            "related_verses": self.get_related_verses(query)
        }

    def get_related_verses(self, topic: str) -> list:
        """Get related Bible verses for a topic"""
        prompt = f"List 3 relevant Bible verses about {topic}"
        return self.gpt.get_completion(prompt).split('\n')