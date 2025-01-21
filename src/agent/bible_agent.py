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
from models.verse_categories import VerseCategory, VerseCatalog

from colorama import init, Fore, Style

from dotenv import load_dotenv
load_dotenv()

from .base_agent import BaseAgent
from .components.goal_system import Goal, GoalPriority
from utils.formatters.markdown_formatter import MarkdownFormatter
from utils.formatters.console_formatter import ConsoleFormatter
from .components.session import StudySession

import numpy as np

class BibleAgent(BaseAgent):
    def __init__(self):
        logging.debug("Initializing BibleAgent")
        try:
            super().__init__()
            self.console_formatter = ConsoleFormatter()
            self.model_selector = ModelSelector()
            self._models = {}
            self.current_model_type = ModelType.GEMINI
            
            # Initialize verse system
            self.verse_catalog = VerseCatalog()
            self.verse_preferences = {
                "preferred_translations": ["ESV", "NIV", "KJV"],
                "categories": [
                    VerseCategory.WISDOM,
                    VerseCategory.ENCOURAGEMENT,
                    VerseCategory.FAITH
                ],
                "review_interval_days": 7
            }
            
            self._initialize_goals()
            self._initialize_daily_verses()
            
            # Add session tracking
            self.current_session = StudySession()
            
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
        self.verse_history = []

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
        """Initialize daily verse cache"""
        try:
            verse = self.get_daily_verse()
            if verse:
                self.current_verse = verse
            else:
                raise Exception("Failed to fetch initial verse")
        except Exception as e:
            logging.error(f"Failed to initialize daily verses: {str(e)}")
            raise

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

    def _get_fallback_verse(self) -> Verse:
        """Provide a reliable fallback verse when API calls fail"""
        return Verse(
            text="The LORD is my shepherd; I shall not want.",
            reference="Psalm 23:1",
            translation="KJV",
            category=VerseCategory.ENCOURAGEMENT
        )

    def get_daily_verse(self) -> Optional[Verse]:
        """Get daily verse with proper error handling"""
        try:
            # Default verse if all else fails
            default_verse = self._get_fallback_verse()
            
            # Try to get verse from preferred categories
            category = random.choice(self.verse_preferences["categories"])
            
            # Use predefined verses if catalog fails
            verses = {
                VerseCategory.WISDOM: ["Proverbs 3:5-6", "James 1:5"],
                VerseCategory.ENCOURAGEMENT: ["Philippians 4:13", "Isaiah 41:10"],
                VerseCategory.FAITH: ["Hebrews 11:1", "Romans 10:17"]
            }
            
            reference = random.choice(verses.get(category, ["Psalm 23:1"]))
            logging.debug(f"Selected verse reference: {reference}")
            
            # Try ESV API
            verse = self._fetch_verse(reference, "ESV")
            if verse:
                return verse
                
            return default_verse
            
        except Exception as e:
            logging.error(f"Error in get_daily_verse: {str(e)}")
            return self._get_fallback_verse()

    def _fetch_verse(self, reference: str, translation: str) -> Optional[Verse]:
        """Fetch verse from ESV API"""
        try:
            url = "https://api.esv.org/v3/passage/text/"
            headers = {'Authorization': f'Token {Config.ESV_API_KEY}'}
            
            params = {
                'q': reference,
                'include-headings': False,
                'include-footnotes': False,
                'include-verse-numbers': False,
                'include-short-copyright': False,
                'include-passage-references': True
            }
            
            logging.debug(f"Fetching from ESV API: {reference}")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Save detailed response to JSON file
            output_dir = Config.DATA_DIR / "verses"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_file = output_dir / f"verse_response_{timestamp}.json"
            
            with open(json_file, 'w') as f:
                json.dump({
                    'api_response': data,
                    'timestamp': datetime.now().isoformat(),
                    'reference': reference
                }, f, indent=2)
                
            logging.info(f"Detailed response saved to: {json_file}")
            
            if not data.get('passages'):
                return None
                
            verse = Verse(
                text=data['passages'][0].strip(),
                reference=reference,
                translation="ESV",
                category=self.verse_preferences["categories"][0]
            )
            
            verse_dict = verse.to_dict()
            logging.debug(f"Processed verse: {json.dumps(verse_dict, indent=2)}")
            print(self.console_formatter.format_verse(verse_dict))
            print(f"\n{Fore.BLUE}💾 Detailed response saved to: {json_file}{Style.RESET_ALL}")
            return verse
            
        except Exception as e:
            logging.error(f"ESV API error: {str(e)}")
            return None

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

    def _create_teaching_prompt(self, topic: str) -> str:
        """Create a structured prompt for biblical teaching generation"""
        return f"""
        Provide biblical teachings and insights about: {topic}
        
        Please include:
        1. Key biblical principles
        2. Relevant scripture references
        3. Practical applications
        4. Spiritual wisdom
        5. Examples from biblical narratives
        
        Format the response with clear sections and scripture citations.
        Focus on providing deep spiritual insights while maintaining theological accuracy.
        """

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

    def analyze_passage(self, passage: str) -> Dict[str, Any]:
        """Analyze biblical passage using selected model"""
        start_time = time.time()
        model = None
        
        try:
            context = {
                'passage': passage,
                'timestamp': datetime.now().isoformat(),
                'type': 'analysis'
            }
            
            # Get initialized model
            model = self.model_selector.select_and_get_model(
                task=TaskType.ANALYSIS,
                context=context
            )
            
            if not model:
                raise Exception("Failed to initialize model for analysis")
                
            # Create analysis prompt
            prompt = self._create_analysis_prompt(passage)
            result = model.generate(prompt)
            
            if not result:
                raise Exception("No analysis generated")
                
            # Package response
            analysis_data = {
                "passage": passage,
                "analysis": result,
                "model_used": model.model_id,
                "timestamp": datetime.now().isoformat()
            }
            
            # Update metrics
            if hasattr(model, 'model_type'):
                self.model_selector.update_performance(
                    model=model.model_type,
                    success=True,
                    latency=time.time() - start_time
                )
            
            # Display results
            print(self.console_formatter.format_analysis(analysis_data))
            return analysis_data
            
        except Exception as e:
            if model and hasattr(model, 'model_type'):
                self.model_selector.update_performance(
                    model=model.model_type,
                    success=False,
                    latency=time.time() - start_time
                )
            logging.error(f"Analysis failed: {str(e)}")
            raise

    def _create_analysis_prompt(self, passage: str) -> str:
        """Create prompt for passage analysis"""
        return f"""
        Analyze the following biblical passage:
        
        {passage}
        
        Please provide:
        1. Historical context
        2. Key themes and messages
        3. Theological significance
        4. Practical applications
        5. Related cross-references
        """

    def suggest_related_verses(self, verse: Verse) -> List[Verse]:
        """Suggest related verses based on category and cross-references"""
        pass

    def get_verses_for_review(self) -> List[Verse]:
        """Get verses due for review based on review_interval_days"""
        pass