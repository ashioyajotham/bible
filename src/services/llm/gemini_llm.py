import google.generativeai as genai
from .base_llm import BaseLLM

class GeminiLLM(BaseLLM):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate(self, prompt: str, **kwargs) -> str:
        response = self.model.generate_content(prompt)
        return response.text