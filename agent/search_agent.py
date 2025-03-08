from typing import Dict, List, Optional
import logging
from services.serper_service import SerperService
from services.model_manager import ModelManager
from config.settings import Config
from services.llm.gemini_llm import GeminiLLM
from services.llm.model_types import ModelType
from datetime import datetime

class SearchAgent:
    """Enhanced biblical search and analysis agent"""
    
    def __init__(self, model_manager: ModelManager):
        """Initialize with shared model manager"""
        self.model_manager = model_manager
        self.serper = SerperService(api_key=Config.SERPER_API_KEY)
        self.gemini = self.model_manager.get_model(ModelType.GEMINI)

    def search_and_analyze(self, query: str) -> Optional[Dict]:
        """Enhanced biblical search with theological analysis"""
        try:
            # Get raw search results
            raw_results = self.serper.search(query)
            if not raw_results:
                raise Exception("No search results found")

            # Generate theological analysis
            analysis_prompt = f"""Analyze biblically: {query}
            Based on these sources: {[r.get('snippet', '') for r in raw_results[:3]]}
            
            Consider:
            1. Biblical perspective
            2. Key theological points
            3. Scripture references
            4. Practical application
            """
            
            analysis = self.gemini.generate(analysis_prompt)
            if not analysis:
                raise Exception("Failed to generate analysis")

            # Structure the response
            return {
                "query": query,
                "insights": analysis,  # Key matches session storage expectation
                "sources": [{
                    "title": r.get('title', ''),
                    "link": r.get('link', ''),
                    "snippet": r.get('snippet', '')
                } for r in raw_results[:3]],
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logging.error(f"Search and analysis failed: {str(e)}")
            return None

    def reflect_on_results(self, search_results: Dict) -> str:
        """Generate spiritual reflection on search results"""
        try:
            reflection_prompt = f"""Provide a spiritual reflection on: {search_results['query']}
            Based on: {search_results['insights']}
            
            Consider:
            1. Spiritual significance
            2. Personal application
            3. Prayer points
            4. Meditation focus
            """
            
            return self.gemini.generate(reflection_prompt)
            
        except Exception as e:
            logging.error(f"Reflection generation failed: {str(e)}")
            return ""

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
        """Extract key theological points from analysis"""
        try:
            prompt = f"Extract the key theological points from this analysis: {text}"
            result = self.gemini.generate(prompt)
            return [point.strip() for point in result.split('\n') if point.strip()]
        except Exception as e:
            logging.error(f"Key point extraction failed: {str(e)}")
            return []

    def _find_biblical_references(self, text: str) -> List[str]:
        """Extract biblical references from text"""
        try:
            prompt = f"List all Bible verse references from this text: {text}"
            result = self.gemini.generate(prompt)
            return [ref.strip() for ref in result.split('\n') if ref.strip()]
        except Exception as e:
            logging.error(f"Reference extraction failed: {str(e)}")
            return []