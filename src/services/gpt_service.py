from typing import Dict, Any, Optional
import openai
from datetime import datetime
import time
from functools import lru_cache

class GPTService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.model = "gpt-4"
        self.max_retries = 3
        self.retry_delay = 1

    def get_completion(self, prompt: str, **kwargs) -> str:
        """Generate completion with retry logic"""
        for attempt in range(self.max_retries):
            try:
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a biblical scholar and spiritual guide."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=kwargs.get('temperature', 0.7),
                    max_tokens=kwargs.get('max_tokens', 500)
                )
                return response.choices[0].message.content
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(self.retry_delay * (attempt + 1))

    @lru_cache(maxsize=100)
    def analyze_verse(self, verse_text: str) -> Dict[str, Any]:
        """Analyze verse content and context"""
        prompt = f"Analyze this Bible verse and provide insights:\n{verse_text}"
        analysis = self.get_completion(prompt)
        return {
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }

    def extract_teachings(self, text: str) -> Dict[str, Any]:
        """Extract key teachings from biblical text"""
        prompt = f"Extract and explain the key teachings from:\n{text}"
        return {
            "teachings": self.get_completion(prompt),
            "summary": self.get_completion(f"Summarize the main points of:\n{text}", 
                                        temperature=0.5,
                                        max_tokens=200)
        }

    def generate_study_questions(self, verse_text: str) -> list:
        """Generate study questions for deeper understanding"""
        prompt = f"Generate 3 thought-provoking study questions for:\n{verse_text}"
        response = self.get_completion(prompt)
        return response.split('\n')

    def clear_cache(self):
        """Clear the analysis cache"""
        self.analyze_verse.cache_clear()