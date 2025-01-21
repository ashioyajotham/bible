from typing import Dict, List
from datetime import datetime
from services.serper_service import SerperService
from config.settings import Config
from services.llm.gemini_llm import GeminiLLM
import logging

class SearchAgent:
    def __init__(self):
        self.gemini = GeminiLLM(api_key=Config.GEMINI_API_KEY)
        self.serper = SerperService(api_key=Config.SERPER_API_KEY)
        self.cache = {}

    def search_and_analyze(self, query: str) -> Dict:
        """Enhanced biblical search with Gemini analysis"""
        try:
            # Get search results
            raw_results = self.serper.search(query)
            validated_results = self._validate_results(raw_results)
            
            # Generate insights using Gemini
            insights_prompt = f"""
            Analyze these search results about "{query}" from a biblical perspective:
            {validated_results[:3]}
            
            Provide:
            1. Biblical interpretation
            2. Theological context
            3. Practical application
            4. Related scripture references
            """
            
            biblical_insights = self.gemini.generate(insights_prompt)
            
            return {
                "query": query,
                "insights": biblical_insights,
                "sources": validated_results[:3],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Search and analysis failed: {str(e)}")
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