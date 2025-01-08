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
from src.services.llm.model_selector import ModelSelector, ModelType, TaskType
from typing import Dict, List, Optional

from dotenv import load_dotenv
load_dotenv()

class BibleAgent:
    def __init__(self):
        self.model_selector = ModelSelector()
        self.models = {
            ModelType.GEMINI: GeminiLLM(api_key=Config.GEMINI_API_KEY),
            ModelType.LLAMA: HuggingFaceLLM(model_id=Config.HF_MODEL_ID)
        }
        
        self.current_model = self.models[ModelType.GEMINI]  # Default model

        self.serper = SerperService(api_key=Config.SERPER_API_KEY)
        
        # Agent State
        self.memory = []
        self.favorites = []
        self.context = {}
        
        # Agent Tools
        self.tools = {
            'search': self.search_biblical_insights,
            'reflect': self.generate_reflection,
            'verse': self.get_daily_verse,
            'teach': self.get_teachings,
            'analyze': self.analyze_passage
        }
        
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
        """Generate reflection using best-suited model"""
        selected_model = self.model_selector.select_model(
            task=TaskType.REFLECTION,
            context={'verse_length': len(verse.text)}
        )
        
        try:
            self.current_model = self.models[selected_model]
            prompt = f"Provide a deep spiritual reflection on this verse: {verse.text} ({verse.reference})"
            response = self.current_model.generate(prompt)
            self.model_selector.track_performance(selected_model, True)
            return response
        except Exception as e:
            self.model_selector.track_performance(selected_model, False)
            fallback_model = next(m for m in ModelType if m != selected_model)
            return self.models[fallback_model].generate(prompt)

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
        gpt_analysis = self.get_llm_response(f"Provide biblical insight on: {query}", task_type='search')
        online_results = self.serper.search(f"biblical meaning {query}")
        
        return {
            "ai_analysis": gpt_analysis,
            "online_sources": online_results[:3],
            "related_verses": self.get_related_verses(query)
        }

    def get_related_verses(self, topic: str) -> list:
        """Get related Bible verses for a topic"""
        prompt = f"List 3 relevant Bible verses about {topic}"
        return self.get_llm_response(prompt, task_type='related_verses').split('\n')

    def plan_action(self, user_input: str) -> Dict:
        """Strategic planning for agent actions"""
        prompt = f"Determine best action for: {user_input}"
        plan = self.get_llm_response(prompt, task_type='planning')
        
        return {
            'input': user_input,
            'plan': plan,
            'tool': self._select_tool(plan),
            'context': self._get_context()
        }

    def execute_action(self, plan: Dict) -> Dict:
        """Execute planned action using appropriate tool"""
        tool = self.tools.get(plan['tool'])
        if not tool:
            return {'error': 'Tool not found'}
            
        result = tool(plan['input'])
        self._update_memory(plan, result)
        return result

    def _select_tool(self, plan: str) -> str:
        """Select appropriate tool based on plan"""
        keywords = {
            'search': ['find', 'search', 'look up'],
            'reflect': ['reflect', 'meditate', 'think'],
            'verse': ['verse', 'scripture', 'passage'],
            'teach': ['teach', 'explain', 'understand'],
            'analyze': ['analyze', 'study', 'examine']
        }
        
        for tool, words in keywords.items():
            if any(word in plan.lower() for word in words):
                return tool
        return 'search'  # default tool

    def _get_context(self) -> Dict:
        """Get current context for agent"""
        return {
            'date': datetime.now(),
            'last_interaction': self.memory[-1] if self.memory else None,
            'favorites_count': len(self.favorites)
        }

    def _update_memory(self, plan: Dict, result: Dict):
        """Update agent memory with interaction"""
        self.memory.append({
            'timestamp': datetime.now(),
            'plan': plan,
            'result': result,
            'context': self._get_context()
        })

    def remember(self, interaction: dict):
        """Agent memory system"""
        self.memory.append({
            'timestamp': datetime.now(),
            'interaction': interaction,
            'context': {'date': datetime.now().date()}
        })

    def get_llm_response(self, prompt: str, task_type: str) -> str:
        selected_model = self.model_selector.select_model(
            task_type=task_type,
            context=self._get_context()
        )
        
        try:
            self.current_model = self.models[selected_model]
            response = self.current_model.generate(prompt)
            self.model_selector.track_performance(selected_model, True)
            return response
        except Exception as e:
            logging.error(f"Model {selected_model} failed: {str(e)}")
            self.model_selector.track_performance(selected_model, False)
            return self._fallback_response(prompt)

    def _fallback_response(self, prompt: str) -> str:
        """Try fallback models if primary fails"""
        for model_type in self.model_selector.fallback_order:
            if model_type in self.models:
                try:
                    return self.models[model_type].generate(prompt)
                except:
                    continue
        return "Sorry, all models are currently unavailable."