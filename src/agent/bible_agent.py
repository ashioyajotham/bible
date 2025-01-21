import random
import time
import requests
import json
import logging
import urllib.parse
from datetime import datetime
from services.serper_service import SerperService
from models.verse import Verse
from config.settings import Config
from services.llm.gemini_llm import GeminiLLM
from services.llm.hf_llm import HuggingFaceLLM
from services.llm.model_selector import ModelSelector, ModelType, TaskType
from typing import Dict, List, Optional, Any

from colorama import init, Fore, Style

from dotenv import load_dotenv
load_dotenv()

from .base_agent import BaseAgent
from .components.goal_system import Goal, GoalPriority
from utils.formatters.markdown_formatter import MarkdownFormatter
from utils.formatters.console_formatter import ConsoleFormatter
from .components.session import StudySession

class BibleAgent(BaseAgent):
    def __init__(self):
        logging.debug("Initializing BibleAgent")
        try:
            super().__init__()  # Initialize BaseAgent first
            self.model_selector = ModelSelector()
            self._models = {}
            self.current_model_type = ModelType.GEMINI
            self._initialize_goals()
            self._initialize_daily_verses()
            
            # Add session tracking
            self.current_session = StudySession()
            
            logging.debug("BibleAgent initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize BibleAgent: {str(e)}")
            raise

        self.serper = SerperService(api_key=Config.SERPER_API_KEY)
        
        # Agent State
        self.memory = []
        self.favorites = []
        self.context = {}
        self.goals = {
            "primary": "Provide biblical insights and understanding",
            "secondary": ["Learn from interactions", "Improve responses", "Build context"]
        }
        self.performance_metrics = {}
        self.learning_history = []
        
        # Agent Tools
        self.tools = {
            'search': self.search_biblical_insights,
            'reflect': self.generate_reflection,
            'verse': self.get_daily_verse,
            'teach': self.get_teachings,
            'analyze': self.analyze_passage
        }
        
        self.markdown_formatter = MarkdownFormatter()
        self.console_formatter = ConsoleFormatter()

    def _initialize_goals(self):
        """Initialize agent goals"""
        self.goal_system.add_goal(Goal(
            description="Provide biblical insights and understanding",
            priority=GoalPriority.HIGH,
            success_criteria=["Relevant verse found", "Insight generated"]
        ))
        self.goal_system.add_goal(Goal(
            description="Learn from interactions",
            priority=GoalPriority.MEDIUM,
            success_criteria=["Pattern identified", "Knowledge stored"]
        ))

    def _initialize_daily_verses(self):
        """Initialize default daily verses"""
        self.daily_verses = {
            "default": [
                "john/3:16",
                "philippians/4:13",
                "psalm/23:1",
                "proverbs/3:5-6"
            ]
        }

    def get_model(self, model_type: ModelType):
        if (model_type not in self._models):
            if model_type == ModelType.GEMINI:
                self._models[model_type] = GeminiLLM(api_key=Config.GEMINI_API_KEY)
            elif model_type == ModelType.LLAMA:
                self._models[model_type] = HuggingFaceLLM(model_id=Config.HF_MODEL_ID)
        return self._models[model_type]

    @property
    def current_model(self):
        return self.get_model(self.current_model_type)

    def get_daily_verse(self) -> Optional[str]:
        verse_data = self._fetch_daily_verse()
        if verse_data:
            # Track in session
            self.current_session.verses.append({
                'text': verse_data.text,
                'reference': verse_data.reference,
                'translation': verse_data.translation,
                'timestamp': datetime.now().isoformat()
            })
            return self.console_formatter.format_verse(verse_data)
        return None

    def _fetch_daily_verse(self) -> Optional[Verse]:
        """Get verse based on date or random selection"""
        try:
            verses = self.daily_verses["default"]
            verse_ref = random.choice(verses)
            
            # URL encode the verse reference
            encoded_ref = urllib.parse.quote(verse_ref)
            url = f"https://bible-api.com/{encoded_ref}"  # Removed 'data/kjv' path
            
            logging.debug(f"Fetching verse from: {url}")
            response = requests.get(url)
            
            if response.status_code == 404:
                # Try alternate format (e.g., 'psalms' instead of 'psalm')
                alternate_ref = self._get_alternate_reference(verse_ref)
                url = f"https://bible-api.com/{urllib.parse.quote(alternate_ref)}"
                logging.debug(f"Retrying with alternate reference: {url}")
                response = requests.get(url)
            
            response.raise_for_status()
            data = response.json()
            
            verse = Verse(
                text=data['text'].strip(),
                reference=data['reference'],
                translation=data.get('translation_name', 'KJV')
            )

            # Format the verse for console output
            formatted_verse = self.console_formatter.format_verse({
                'text': verse.text,
                'reference': verse.reference,
                'translation': verse.translation
            })
            
            print(formatted_verse)
            return verse

        except Exception as e:
            logging.error(f"Error fetching verse: {str(e)}")
            return self._get_fallback_verse()

    def _get_alternate_reference(self, verse_ref: str) -> str:
        """Get alternate format for verse reference"""
        mapping = {
            'psalm/': 'psalms/',
            'proverbs/': 'proverb/',
            'song/': 'songofsolomon/'
        }
        for old, new in mapping.items():
            if old in verse_ref:
                return verse_ref.replace(old, new)
        return verse_ref

    def _get_fallback_verse(self) -> Verse:
        """Return a hardcoded verse when API fails"""
        return Verse(
            text="For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life.",
            reference="John 3:16",
            translation="ESV"
        )

    def get_teachings(self, topic: str = None) -> dict:
        start_time = time.time()
        model = None
        
        try:
            context = {'topic': topic, 'timestamp': datetime.now().isoformat()}
            
            # Get initialized model
            model = self.model_selector.select_and_get_model(
                task=TaskType.TEACHING,
                context=context
            )
            
            if not model:
                raise Exception("Failed to initialize any model")
            
            # Generate content
            result = model.generate(self._create_teaching_prompt(topic))
            if not result:
                raise Exception("No content generated")
            
            # Package response
            teaching_data = {
                "teaching": result,
                "topic": topic,
                "model_used": model.model_id,
                "timestamp": datetime.now().isoformat()
            }
            
            # Update performance metrics
            self.model_selector.update_performance(
                model=model.model_type,
                success=True,
                latency=time.time() - start_time
            )
            
            print(self.console_formatter.format_teaching(teaching_data))
            return teaching_data
            
        except Exception as e:
            if model:
                self.model_selector.update_performance(
                    model=model.model_type,
                    success=False,
                    latency=time.time() - start_time
                )
            logging.error(f"Teaching generation failed: {str(e)}")
            raise

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

    def export_to_markdown(self, content: Dict[str, Any], filename: str):
        """Export content to markdown file with rich formatting"""
        with open(f"{filename}.md", "w", encoding='utf-8') as f:
            f.write("# Bible Study Export\n\n")

    def search_biblical_insights(self, query: str) -> Dict[str, Any]:
        """Search for biblical insights using SerperAPI"""
        start_time = time.time()
        try:
            # Format search query
            search_query = f"biblical meaning {query}"
            logging.debug(f"Searching for: {search_query}")
            
            # Get search results
            results = self.serper.search(search_query)
            if not results:
                raise Exception("No search results found")
                
            # Format response
            search_data = {
                "query": query,
                "results": results,
                "timestamp": datetime.now().isoformat()
            }
            
            # Display results
            print(self.console_formatter.format_search_results(search_data))
            return search_data
            
        except Exception as e:
            logging.error(f"Search error: {str(e)}")
            raise

    def _create_search_prompt(self, query: str) -> str:
        return f"""
        Please provide biblical insights and references about: {query}
        Include relevant scripture verses and theological context.
        Focus on practical application and spiritual understanding.
        """