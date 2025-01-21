import google.generativeai as genai
from typing import Optional
import logging

class GeminiLLM:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate(self, prompt: str) -> Optional[str]:
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.8,
                    'top_k': 40,
                    'max_output_tokens': 2048,
                },
                safety_settings={
                    "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                    "HARM_CATEGORY_HATE_SPEECH": "BLOCK_ONLY_HIGH",
                    "HARM_CATEGORY_HARASSMENT": "BLOCK_ONLY_HIGH",
                    "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_ONLY_HIGH"
                }
            )
            
            # Check if response has content
            if not response.parts:
                logging.error("No content in response")
                return None
                
            # Get text from first part
            content = response.parts[0].text
            if not content:
                logging.error("Empty content in response")
                return None
                
            logging.debug(f"Generated content length: {len(content)}")
            return content
            
        except Exception as e:
            logging.error(f"Gemini generation error: {str(e)}")
            return None