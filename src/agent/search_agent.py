from typing import Dict, List
from datetime import datetime
from services.serper_service import SerperService
from config.settings import Config
from services.llm.gemini_llm import GeminiLLM
from services.llm.hf_llm import HuggingFaceLLM
from services.llm.model_selector import ModelSelector, ModelType, TaskType

class SearchAgent:
    def __init__(self):
        self.model_selector = ModelSelector()
        self.models = {
            ModelType.GEMINI: GeminiLLM(api_key=Config.GEMINI_API_KEY),
            ModelType.LLAMA: HuggingFaceLLM(model_id=Config.HF_MODEL_ID)
        }
        self.serper = SerperService(api_key=Config.SERPER_API_KEY)
        self.cache = {}

    def search_insights(self, query: str) -> Dict:
        validated_results = self._validate_sources(
            self.serper.search(f"bible {query} meaning interpretation")
        )
        
        combined_content = "\n".join([r["snippet"] for r in validated_results])
        selected_model = self.model_selector.select_model(TaskType.ANALYSIS)
        insights = self.models[selected_model].generate(
            f"Based on these sources, provide biblical insights about {query}:\n{combined_content}"
        )
        
        return {
            "insights": insights,
            "sources": validated_results[:3],
            "timestamp": datetime.now().isoformat()
        }

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

    def get_ai_insights(self, prompt: str) -> str:
        """Get insights using current LLM model"""
        selected_model = self.model_selector.select_model(TaskType.ANALYSIS)
        return self.models[selected_model].generate(prompt)

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
        """Find and validate biblical references in text"""
        selected_model = self.model_selector.select_model(TaskType.ANALYSIS)
        refs = self.models[selected_model].generate(
            f"Extract all biblical references from this text:\n{text}"
        )
        return [ref.strip() for ref in refs.split("\n") if ref.strip()]