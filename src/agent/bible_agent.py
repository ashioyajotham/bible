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

from dotenv import load_dotenv
load_dotenv()

from .base_agent import BaseAgent
from .components.goal_system import Goal, GoalPriority
from utils.formatters.markdown_formatter import MarkdownFormatter
from utils.formatters.console_formatter import ConsoleFormatter

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
        """Get verse based on date or random selection with formatted output"""
        try:
            verses = self.daily_verses["default"]
            verse_ref = random.choice(verses)
            response = requests.get(f"https://bible-api.com/{verse_ref}")
            response.raise_for_status()
            
            data = response.json()
            verse = Verse(
                text=data['text'].strip(),
                reference=data['reference'],
                translation=data.get('translation_name', 'ESV')
            )
            
            # Return only the formatted version
            return self.console_formatter.format_verse({
                'text': verse.text,
                'reference': verse.reference,
                'translation': verse.translation
            })
        except Exception as e:
            logging.error(f"Error fetching verse: {str(e)}")
            # Return formatted fallback verse
            fallback = self._get_fallback_verse()
            return self.console_formatter.format_verse({
                'text': fallback.text,
                'reference': fallback.reference,
                'translation': fallback.translation
            })

    def _fetch_daily_verse(self) -> Optional[Verse]:
        """Get verse based on date or random selection"""
        try:
            verses = self.daily_verses["default"]
            verse_ref = random.choice(verses)
            
            # URL encode the verse reference
            encoded_ref = urllib.parse.quote(verse_ref)
            url = f"https://bible-api.com/{encoded_ref}"
            
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
            
            return Verse(
                text=data['text'].strip(),
                reference=data['reference'],
                translation=data.get('translation_name', 'KJV')
            )
            
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
        try:
            context = {
                'topic': topic,
                'timestamp': datetime.now().isoformat()
            }
            
            selected_model = self.model_selector.select_model(
                task=TaskType.TEACHING,
                context=context
            )
            
            result = self.get_model(selected_model).generate(
                f"What did Jesus teach about {topic}"
            )
            
            # Update model performance
            success = bool(result and len(result) > 0)
            latency = time.time() - start_time
            self.model_selector.update_performance(selected_model, success, latency)
            
            return {
                "teaching": result,
                "topic": topic,
                "model_used": selected_model.value,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logging.error(f"Error in get_teachings: {str(e)}")
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
            f.write("# 📚 Scripture Study Report\n\n")
            f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            
            if 'verse' in content:
                f.write(self.markdown_formatter.format_verse(content['verse']))
            if 'teaching' in content:
                f.write(self.markdown_formatter.format_teaching(content['teaching']))
            if 'search_results' in content:
                f.write(self.markdown_formatter.format_search_results(content['search_results']))

    def search_biblical_insights(self, query: str) -> dict:
        """Search for biblical insights using both LLM and online sources"""
        context = {
            'query': query,
            'timestamp': datetime.now().isoformat()
        }
        
        selected_model = self.model_selector.select_model(
            task=TaskType.SEARCH,
            context=context
        )
        
        ai_analysis = self.get_model(selected_model).generate(
            f"Provide biblical insight on: {query}"
        )
        online_results = self.serper.search(f"biblical meaning {query}")
        
        return {
            "ai_analysis": ai_analysis,
            "online_sources": online_results[:3],
            "timestamp": datetime.now().isoformat()
        }

    def get_related_verses(self, topic: str) -> list:
        """Get related Bible verses for a topic"""
        prompt = f"List 3 relevant Bible verses about {topic}"
        return self.get_llm_response(prompt, task_type='related_verses').split('\n')

    def plan_action(self, user_input: str) -> Dict:
        """Strategic planning with goals and context"""
        context = self._get_context()
        relevant_history = self._get_relevant_history(user_input)
        
        plan = {
            "goals": self._identify_relevant_goals(user_input),
            "tools": self._select_tools(user_input, context),
            "steps": self._create_action_steps(user_input),
            "fallback": self._create_fallback_plan()
        }
        
        return self._execute_plan(plan)

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

    def learn_from_interaction(self, interaction: Dict):
        """Agent learning from experiences"""
        self.learning_history.append({
            "interaction": interaction,
            "outcome": interaction.get("success", False),
            "improvements": self._identify_improvements(interaction)
        })
        self._update_strategies(self.learning_history[-1])

    def analyze_passage(self, passage: str) -> Dict:
        """Analyze a biblical passage for deeper understanding"""
        try:
            context = self._get_context()
            selected_model = self.model_selector.select_model(TaskType.ANALYSIS)
            
            prompt = f"Analyze this biblical passage deeply:\n{passage}\n\nProvide:\n1. Context\n2. Key themes\n3. Interpretations\n4. Applications"
            analysis = self.get_model(selected_model).generate(prompt)
            
            # Get related verses
            related_verses = self.get_related_verses(passage)
            
            return {
                "analysis": analysis,
                "related_verses": related_verses,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logging.error(f"Failed to analyze passage: {str(e)}")
            raise

def handle_interactive_mode(agent: BibleAgent):
    """Handle interactive mode with command processing"""
    print("\nBible Study AI Agent - Interactive Mode")
    print("Commands: verse, teach, search, export, quit")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'verse':
                formatted_verse = agent.get_daily_verse()
                print(formatted_verse)
            elif command == 'teach':
                topic = input("Enter topic: ")
                teachings = agent.get_teachings(topic)
                print(agent.console_formatter.format_teaching(teachings))
            elif command == 'search':
                query = input("Enter search query: ")
                results = agent.search_biblical_insights(query)
                print(agent.console_formatter.format_search_results(results))
            elif command == 'export':
                filename = input("Enter filename (without extension): ")
                agent.export_to_markdown({"verse": agent.get_daily_verse()}, filename)
                print(f"Exported to {filename}.md")
            else:
                print("Unknown command. Available commands: verse, teach, search, export, quit")
                
        except Exception as e:
            logging.error(f"Error processing command {command}: {str(e)}")
            print(f"Error: {str(e)}")