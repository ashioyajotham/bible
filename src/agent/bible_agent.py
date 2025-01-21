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
from .search_agent import SearchAgent

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
        try:
            logging.debug("Initializing BibleAgent")
            super().__init__()
            
            # Initialize formatters and models
            self.console_formatter = ConsoleFormatter()
            self.model_selector = ModelSelector()
            self._models = {}
            self.current_model_type = ModelType.GEMINI
            
            # Initialize verse preferences
            self.verse_preferences = {
                "preferred_translations": ["ESV"],
                "categories": [
                    VerseCategory.WISDOM,
                    VerseCategory.ENCOURAGEMENT,
                    VerseCategory.FAITH,
                    VerseCategory.PROMISES
                ],
                "review_interval_days": 7
            }
            
            # Ensure StudySession is properly initialized
            self.current_session = StudySession() 
            
            # Initialize search agent
            self.search_agent = SearchAgent()
            
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
        self.search_agent = SearchAgent()

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
        """Enhanced search with Gemini insights"""
        try:
            # Get raw search results
            raw_results = self.serper.search(query)
            
            # Use Gemini to enhance results
            model = self.get_model(ModelType.GEMINI)
            
            enhanced_results = []
            for result in raw_results:
                prompt = f"""Based on this search result about "{query}":
                {result['snippet']}
                
                Provide:
                1. Biblical perspective
                2. Key spiritual insights
                3. Relevant scripture references
                """
                
                insight = model.generate(prompt)
                result['enhanced_insight'] = insight
                enhanced_results.append(result)
            
            search_data = {
                "query": query,
                "results": enhanced_results,
                "timestamp": datetime.now().isoformat()
            }
            
            print(self.console_formatter.format_search_results(search_data))
            return search_data
            
        except Exception as e:
            logging.error(f"Search failed: {str(e)}")
            raise

    def _create_search_prompt(self, query: str) -> str:
        return f"""
        Please provide biblical insights and references about: {query}
        Include relevant scripture verses and theological context.
        Focus on practical application and spiritual understanding.
        """

    def analyze_passage(self, passage: str) -> Dict[str, Any]:
        """Analyze biblical passage using Gemini"""
        start_time = time.time()
        try:
            model = self.get_model(ModelType.GEMINI)
            
            prompt = f"""Analyze this biblical passage:
            {passage}
            
            Provide:
            1. Historical Context
            2. Key Themes
            3. Theological Significance
            4. Practical Applications
            5. Cross References
            """
            
            analysis = model.generate(prompt)
            
            analysis_data = {
                "passage": passage,
                "analysis": analysis,
                "model_used": "gemini-pro",
                "timestamp": datetime.now().isoformat()
            }
            
            print(self.console_formatter.format_analysis(analysis_data))
            return analysis_data
            
        except Exception as e:
            logging.error(f"Analysis failed: {str(e)}")
            raise

    def suggest_related_verses(self, verse: Verse) -> List[Verse]:
        """Suggest related verses based on category and cross-references"""
        pass

    def get_verses_for_review(self) -> List[Verse]:
        """Get verses due for review based on review_interval_days"""
        pass

    def export_study_session(self, filename: Optional[str] = None) -> str:
        """Export current study session to markdown file"""
        try:
            # Generate timestamp-based filename if none provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"bible_study_{timestamp}"
            
            # Ensure filename has .md extension
            if not filename.endswith('.md'):
                filename += '.md'
            
            # Create exports directory if it doesn't exist
            export_dir = Config.DATA_DIR / "exports"
            export_dir.mkdir(parents=True, exist_ok=True)
            
            export_path = export_dir / filename
            
            # Format study session content
            content = [
                "# Bible Study Session\n",
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                "\n## Study Content\n"
            ]
            
            # Add verse if available
            if hasattr(self, 'current_verse') and self.current_verse:
                content.extend([
                    "\n### Daily Verse\n",
                    f"> {self.current_verse.text}\n",
                    f"*— {self.current_verse.reference} ({self.current_verse.translation})*\n"
                ])
            
            # Add current session content if available
            if hasattr(self, 'current_session') and self.current_session:
                if hasattr(self.current_session, 'teachings'):
                    content.extend([
                        "\n### Teachings\n",
                        *[f"#### {t['topic']}\n{t['teaching']}\n" 
                          for t in self.current_session.teachings]
                    ])
                
                if hasattr(self.current_session, 'searches'):
                    content.extend([
                        "\n### Search Results\n",
                        *[f"#### Query: {s['query']}\n{s['insights']}\n" 
                          for s in self.current_session.searches]
                    ])
            
            # Write content to file
            with open(export_path, 'w', encoding='utf-8') as f:
                f.writelines(content)
            
            print(self.console_formatter.format_export_success(str(export_path)))
            return str(export_path)
            
        except Exception as e:
            logging.error(f"Export failed: {str(e)}")
            raise

    def search_with_analysis(self, query: str) -> Dict:
        """Enhanced search with theological analysis"""
        start_time = time.time()
        model = None
        
        try:
            # Get search results and analysis
            search_data = self.search_agent.search_and_analyze(query)
            
            if not search_data:
                raise Exception("Failed to get search results")
                
            # Track model performance
            if model := self.get_model(self.current_model_type):
                self.model_selector.update_performance(
                    model=model.model_type,
                    success=True,
                    latency=time.time() - start_time
                )
                
            # Add to session
            if hasattr(self, 'current_session'):
                self.current_session.add_search(search_data)
                
            # Format and display results
            print(self.console_formatter.format_search_results(search_data))
            return search_data
            
        except Exception as e:
            if model:
                self.model_selector.update_performance(
                    model=model.model_type,
                    success=False,
                    latency=time.time() - start_time
                )
            logging.error(f"Search failed: {str(e)}")
            return None

    def generate_reflection(self, topic: str) -> Dict:
        """Generate spiritual reflection on a topic"""
        search_agent = SearchAgent()
        
        # Get initial search results
        results = search_agent.search_and_analyze(topic)
        
        # Generate reflection
        reflection = search_agent.reflect_on_results(results)
        
        # Extract biblical references
        references = search_agent._find_biblical_references(
            results["theological_analysis"]
        )
        
        # Get key points
        key_points = search_agent._extract_key_points(
            results["theological_analysis"]
        )
        
        enhanced_results = {
            **results,
            "reflection": reflection,
            "biblical_references": references,
            "key_points": key_points
        }
        
        # Store in session
        if hasattr(self, 'current_session'):
            self.current_session.searches.append(enhanced_results)
        
        print(self.console_formatter.format_search_results(enhanced_results))
        return enhanced_results

    def process_command(self, command: str, *args) -> None:
        """Process user commands with enhanced error handling"""
        try:
            if command == "search" or command == "s":
                query = input("Enter search query: ")
                results = self.search_agent.search_and_analyze(query)
                key_points = self.search_agent._extract_key_points(results['theological_analysis'])
                refs = self.search_agent._find_biblical_references(results['theological_analysis'])
                
                self.current_session.add_search({
                    "query": query,
                    "results": results,
                    "key_points": key_points,
                    "references": refs,
                    "reflection": self.search_agent.reflect_on_results(results)
                })
                
                print(self.console_formatter.format_search_results(results))
                
            elif command == "reflect" or command == "r":
                if not self.current_session.searches:
                    print("No search results to reflect on. Try searching first.")
                    return
                    
                latest_search = self.current_session.searches[-1]
                reflection = self.search_agent.reflect_on_results(latest_search)
                print(self.console_formatter.format_reflection(reflection))
                
            elif command == "verse" or command == "v":
                self.get_daily_verse()
                
            elif command == "teach" or command == "t":
                topic = input("Enter topic: ")
                self.teach_biblical_topic(topic)
                
            elif command == "export" or command == "e":
                filename = input("Enter filename (optional): ")
                self.export_study_session(filename)
                
            elif command == "help" or command == "h":
                print(self.console_formatter.format_help())
                
            elif command == "exit" or command == "q":
                print("Goodbye! God bless.")
                exit(0)
                
            else:
                print(f"Unknown command: {command}")
                print(self.console_formatter.format_help())
                
        except Exception as e:
            logging.error(f"Error processing command {command}: {str(e)}")
            raise

    def teach_biblical_topic(self, topic: str) -> Optional[Dict]:
        """Generate biblical teaching with enhanced response handling"""
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
                raise Exception("Failed to initialize model")
            
            # Generate content with response validation
            response = model.generate(self._create_teaching_prompt(topic))
            if not response:
                raise Exception("No content generated")
                
            # Structure the teaching data
            teaching_data = {
                "topic": topic,
                "teaching": response,
                "model_used": str(self.current_model_type),
                "generation_time": time.time() - start_time
            }
            
            # Add to session
            if hasattr(self, 'current_session'):
                self.current_session.add_teaching(teaching_data)
            
            # Format and display
            print(self.console_formatter.format_teaching(teaching_data))
            return teaching_data
            
        except Exception as e:
            logging.error(f"Teaching generation failed: {str(e)}")
            return None