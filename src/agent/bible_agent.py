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

from services.model_manager import ModelManager

class BibleAgent(BaseAgent):
    def __init__(self):
        try:
            logging.debug("Initializing BibleAgent")
            super().__init__()
            
            # Core components
            self.model_manager = ModelManager()
            self.current_model_type = ModelType.GEMINI
            self.console_formatter = ConsoleFormatter()
            
            # Initialize model system
            self._models = {}
            if not self._init_model():
                raise Exception("Failed to initialize model system")
            
            # Initialize services
            self.search_agent = SearchAgent(model_manager=self.model_manager)
            
            # Initialize session and preferences
            self.current_session = StudySession()
            self.verse_preferences = {
                "preferred_translations": ["ESV"],
                "categories": [VerseCategory.WISDOM]
            }
            
        except Exception as e:
            logging.error(f"Failed to initialize BibleAgent: {str(e)}")
            raise

    def _init_model(self) -> bool:
        """Initialize primary model"""
        try:
            model = self.model_manager.get_model(self.current_model_type)
            if model:
                self._models[self.current_model_type] = model
                return True
            return False
        except Exception as e:
            logging.error(f"Model initialization failed: {str(e)}")
            return False

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
            
            logging.debug(f"Processed verse: {json.dumps(verse.to_dict(), indent=2)}")
            return verse  # Return verse object only, don't format yet
            
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

    def process_command(self, command: str, *args) -> Optional[Dict]:
        """Process user commands"""
        try:
            logging.debug(f"Processing command: {command}")
            
            if command == "teach" or command == "t":
                return self._handle_teach_command()
            elif command == "verse" or command == "v":
                return self._handle_verse_command()
            elif command == "reflect" or command == "r":
                return self._handle_reflect_command()
            elif command == "export" or command == "e":
                return self._handle_export_command()
            elif command == "help" or command == "h":  # Add help handler
                return self._handle_help_command()
            elif command == "exit" or command == "q":
                print(f"{Fore.GREEN}Goodbye! God bless.{Style.RESET_ALL}")
                exit(0)
                
        except Exception as e:
            logging.error(f"Command execution failed: {str(e)}")
            return None

    def _handle_teach_command(self) -> Optional[Dict]:
        """Handle biblical teaching generation"""
        try:
            query = input("Enter topic for biblical teaching: ").strip()
            if not query:
                print("Please provide a topic")
                return None
            
            # Get search results and generate teaching
            search_data = self.search_agent.search_and_analyze(query)
            if not search_data:
                return None
                
            teaching_data = {
                "query": query,
                "insights": search_data.get('insights', ''),
                "references": self._extract_references(search_data.get('insights', '')),
                "application": self._generate_application(search_data.get('insights', '')),
                "prayer": self._generate_prayer_points(query, search_data.get('insights', '')),
                "sources": search_data.get('sources', []),
                "timestamp": datetime.now().isoformat()
            }
            
            # Add to session and display
            self.current_session.add_teaching(teaching_data)
            print(self.console_formatter.format_teaching(teaching_data))
            return teaching_data
            
        except Exception as e:
            logging.error(f"Teaching generation failed: {str(e)}")
            return None

    def _handle_verse_command(self) -> Optional[Dict]:
        logging.debug("Executing verse command")
        verse = self.get_daily_verse()
        if not verse:
            return None
            
        try:
            # Generate devotional
            model = self.model_manager.get_model(self.current_model_type)
            devotional = model.generate(f"""
            Create a short devotional for this verse:
            {verse.text} - {verse.reference}
            
            Include:
            1. Brief explanation
            2. Life application
            3. Prayer point
            """)
            
            verse_data = verse.to_dict()
            verse_data['devotional'] = devotional
            
            # Add to session for reflection
            self.current_session.add_verse(verse_data)
            
            print(self.console_formatter.format_verse(verse_data))
            return verse_data
            
        except Exception as e:
            logging.error(f"Error generating devotional: {str(e)}")
            return verse.to_dict()  # Return verse without devotional as fallback

    def _extract_references(self, text: str) -> List[str]:
        """Extract biblical references from text"""
        try:
            model = self.model_manager.get_model(self.current_model_type)
            prompt = f"""
            Extract all Bible verse references from this text:
            {text}
            
            Return only the references, one per line.
            Example format:
            John 3:16
            Romans 8:28
            """
            
            result = model.generate(prompt)
            return [ref.strip() for ref in result.split('\n') if ref.strip()]
        except Exception as e:
            logging.error(f"Reference extraction failed: {str(e)}")
            return []

    def _generate_application(self, insights: str) -> str:
        """Generate practical application points"""
        try:
            model = self.model_manager.get_model(self.current_model_type)
            prompt = f"""
            Based on these biblical insights:
            {insights}
            
            Generate practical application points including:
            1. Personal application
            2. Daily life implementation
            3. Spiritual growth steps
            """
            
            return model.generate(prompt)
        except Exception as e:
            logging.error(f"Application generation failed: {str(e)}")
            return ""

    def _generate_prayer_points(self, topic: str, insights: str) -> str:
        """Generate focused prayer points"""
        try:
            model = self.model_manager.get_model(self.current_model_type)
            prompt = f"""
            Based on the topic '{topic}' and these insights:
            {insights}
            
            Create focused prayer points covering:
            1. Personal transformation
            2. Spiritual understanding
            3. Practical application
            4. Community impact
            """
            
            return model.generate(prompt)
        except Exception as e:
            logging.error(f"Prayer points generation failed: {str(e)}")
            return ""

    def _handle_reflect_command(self) -> Optional[Dict]:
        try:
            logging.debug("Executing reflect command")
            
            # Get latest content from session
            if not self.current_session:
                print("No active study session to reflect on.")
                return None
            
            content = self.current_session.get_latest_content()
            if not content:
                print("Nothing to reflect on. Try studying a topic first.")
                return None
            
            # More structured prompt
            model = self.model_manager.get_model(self.current_model_type)
            reflection = model.generate(f"""
            Reflect deeply on this {content['type']}:
            {content['content'].get('insights', content['content'].get('text', ''))}
            
            Format your response exactly as follows:
            
            INSIGHTS:
            [Your spiritual insights here]
            
            APPLICATION:
            [Your personal application points here]
            
            PRAYER:
            [Your prayer focus here]
            """)
            
            # More robust parsing
            sections = reflection.split('INSIGHTS:')[1].split('APPLICATION:')
            insights = sections[0].strip()
            
            app_prayer = sections[1].split('PRAYER:')
            application = app_prayer[0].strip()
            prayer = app_prayer[1].strip() if len(app_prayer) > 1 else "Prayer focus pending..."
            
            reflection_data = {
                "context_type": content['type'],
                "insights": insights,
                "application": application,
                "prayer": prayer,
                "timestamp": datetime.now().isoformat()
            }
            
            self.current_session.add_reflection(reflection_data)
            print(self.console_formatter.format_reflection(reflection_data))
            return reflection_data
            
        except Exception as e:
            logging.error(f"Reflection generation failed: {str(e)}")
            return None

    def _handle_export_command(self) -> Optional[str]:
        """Handle study session export"""
        try:
            # Generate timestamp-based filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bible_study_{timestamp}.md"
            
            # Create exports directory
            export_dir = Config.DATA_DIR / "exports"
            export_dir.mkdir(parents=True, exist_ok=True)
            
            export_path = export_dir / filename
            
            # Format study session content
            content = [
                "# Bible Study Session\n",
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            ]
            
            # Add teachings
            if self.current_session.teachings:
                content.extend([
                    "## Teachings\n",
                    *[f"### {t['query']}\n{t['insights']}\n" 
                      for t in self.current_session.teachings],
                    "\n"
                ])
            
            # Add verses
            if self.current_session.verses:
                content.extend([
                    "## Daily Verses\n",
                    *[f"> {v['text']}\n*— {v['reference']} ({v['translation']})*\n\n{v.get('devotional', '')}\n" 
                      for v in self.current_session.verses],
                    "\n"
                ])
            
            # Add reflections
            if self.current_session.reflections:
                content.extend([
                    "## Reflections\n",
                    *[f"### Reflection on {r['context_type']}\n{r['insights']}\n\n**Application:**\n{r['application']}\n\n**Prayer:**\n{r['prayer']}\n" 
                      for r in self.current_session.reflections]
                ])
            
            # Write to file
            with open(export_path, 'w', encoding='utf-8') as f:
                f.writelines(content)
            
            print(self.console_formatter.format_export_success(str(export_path)))
            return str(export_path)
            
        except Exception as e:
            logging.error(f"Export failed: {str(e)}")
            return None

    def _handle_help_command(self) -> Optional[Dict]:
        """Handle help command"""
        try:
            print(self.console_formatter.format_welcome())
            return {'command': 'help', 'shown': True}
            
        except Exception as e:
            logging.error(f"Help display failed: {str(e)}")
            return None