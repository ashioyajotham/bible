from typing import Dict, List, Optional
from datetime import datetime
from services.serper_service import SerperService
from config.settings import Config
from services.llm.gemini_llm import GeminiLLM
import logging
from services.llm.model_types import ModelType
from services.model_manager import ModelManager

class SearchAgent:
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.serper = SerperService(api_key=Config.SERPER_API_KEY)
        self.gemini = self.model_manager.get_model(ModelType.GEMINI)
        self.cache = {}

    def search_and_analyze(self, query: str) -> Optional[Dict]:
        try:
            # Get raw search results
            raw_results = self.serper.search(query)
            if not raw_results:
                raise Exception("No search results found")
                
            # Generate analysis
            analysis = self.gemini.generate(f"""Analyze biblically: {query}
            Based on: {[r.get('snippet', '') for r in raw_results[:3]]}""")
            
            if not analysis:
                raise Exception("Failed to generate analysis")
                
            # Return structured response
            return {
                "query": query,
                "insights": analysis,
                "sources": [{
                    "title": r.get('title', ''),
                    "link": r.get('link', ''),
                    "snippet": r.get('snippet', '')
                } for r in raw_results[:3]],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Search failed: {str(e)}")
            return None

    def reflect_on_results(self, search_results: Dict) -> str:
        """Generate spiritual reflection on search results"""
        try:
            reflection_prompt = f"""Provide a spiritual reflection on these search findings about: {search_results['query']}
            
            Consider:
            1. Spiritual significance
            2. Personal application
            3. Prayer points
            4. Meditation focus
            """
            
            return self.gemini.generate(reflection_prompt)
            
        except Exception as e:
            logging.error(f"Reflection generation failed: {str(e)}")
            raise

    def get_summary(self, text: str) -> Dict:
        """Generate a comprehensive biblical summary"""
        try:
            summary_prompt = f"""
            Provide a biblical analysis of this text:
            {text}
            
            Include:
            - Main theological themes
            - Key spiritual principles
            - Biblical cross-references
            - Practical applications
            """
            
            summary = self.gemini.generate(summary_prompt)
            
            return {
                "summary": summary,
                "key_points": self._extract_key_points(summary),
                "references": self._find_biblical_references(text),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Summary generation failed: {str(e)}")
            raise

    def _validate_results(self, results: List[Dict]) -> List[Dict]:
        """Filter and validate search results"""
        valid_results = []
        for result in results:
            if self._is_reliable_source(result.get('link', '')):
                valid_results.append(result)
        return valid_results

    def _is_reliable_source(self, url: str) -> bool:
        """Check if source is from reliable biblical websites"""
        trusted_domains = [
            'biblehub.com',
            'biblegateway.com',
            'blueletterbible.org',
            'biblestudytools.com',
            'gotquestions.org'
        ]
        return any(domain in url.lower() for domain in trusted_domains)

    def _extract_key_points(self, text: str) -> List[str]:
        """
        Extract key points from a summary
        """
        points = self.gemini.generate(
            f"Extract the main points from this text as a list:\n{text}"
        )
        return points.split("\n")

    def _find_biblical_references(self, text: str) -> List[str]:
        """Find and validate biblical references in text"""
        refs = self.gemini.generate(
            f"Extract all biblical references from this text:\n{text}"
        )
        return [ref.strip() for ref in refs.split("\n") if ref.strip()]