import random
import requests
from datetime import datetime
from ..services.gpt_service import GPTService 
from ..services.serper_service import SerperService
from ..models.verse import Verse
from ..config.settings import Config

from dotenv import load_dotenv
load_dotenv()

class BibleAgent:
    def __init__(self):
        self.gpt = GPTService(api_key=Config.OPENAI_API_KEY)
        self.serper = SerperService(api_key=Config.SERPER_API_KEY)
        self.favorites = []
        
    def get_daily_verse(self) -> Verse:
        """Fetch a daily verse randomly or based on date"""
        common_verses = [
            "john/3:16",
            "philippians/4:13",
            "jeremiah/29:11",
            "romans/8:28",
            "psalm/23:1"
        ]
        verse_ref = random.choice(common_verses)
        response = requests.get(f"{BIBLE_API_BASE_URL}/{verse_ref}")
        data = response.json()
        
        return Verse(
            reference=data['reference'],
            text=data['text'],
            translation=data.get('translation_name', 'KJV')
        )

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
        return self.gpt.get_completion(prompt)

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