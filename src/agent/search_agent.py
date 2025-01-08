from typing import Dict, List
import json
from ..services.gpt_service import GPTService
from ..services.serper_service import SerperService
from config.settings import SERPER_API_KEY

class SearchAgent:
    def __init__(self):
        self.gpt = GPTService()
        self.serper = SerperService()
        self.cache = {}
        
    def search_insights(self, query: str) -> Dict:
        """
        Search for biblical insights using serper.dev and GPT
        """
        # Check cache first
        if query in self.cache:
            return self.cache[query]
            
        # Search religious and scholarly sources
        search_results = self.serper.search(
            query=f"bible {query} meaning interpretation",
            num_results=5
        )
        
        # Filter and validate sources
        validated_results = self._validate_sources(search_results)
        
        # Generate insights using GPT
        combined_content = "\n".join([r["snippet"] for r in validated_results])
        insights = self.gpt.get_completion(
            f"Based on these sources, provide biblical insights about {query}:\n{combined_content}"
        )
        
        result = {
            "insights": insights,
            "sources": validated_results,
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache the results
        self.cache[query] = result
        return result

    def get_summary(self, text: str) -> Dict:
        """
        Generate a comprehensive summary of biblical text
        """
        summary = self.gpt.get_completion(
            f"Summarize this biblical text and extract key points:\n{text}"
        )
        
        return {
            "summary": summary,
            "key_points": self._extract_key_points(summary),
            "references": self._find_biblical_references(text)
        }

    def _validate_sources(self, results: List[Dict]) -> List[Dict]:
        """
        Filter and validate religious/scholarly sources
        """
        trusted_domains = [
            'biblehub.com', 'biblegateway.com', 'biblestudytools.com',
            'gotquestions.org', 'christianity.com', 'bible.org'
        ]
        
        return [
            result for result in results
            if any(domain in result.get("link", "").lower() for domain in trusted_domains)
        ]

    def _extract_key_points(self, text: str) -> List[str]:
        """
        Extract key points from a summary
        """
        points = self.gpt.get_completion(
            f"Extract the main points from this text as a list:\n{text}"
        )
        return points.split("\n")

    def _find_biblical_references(self, text: str) -> List[str]:
        """
        Find and validate biblical references in text
        """
        refs = self.gpt.get_completion(
            f"Extract all biblical references from this text:\n{text}"
        )
        return [ref.strip() for ref in refs.split("\n") if ref.strip()]