from transformers import AutoTokenizer, pipeline
import torch
import logging
from config.settings import Config
from typing import Optional

class HuggingFaceLLM:
    def __init__(self, model_id: str = None):
        try:
            # Use smaller model and set configs
            self.model_id = "microsoft/phi-2"  # Much smaller model that works on CPU
            self.device = "cpu"  # Force CPU for reliability
            
            self.pipe = pipeline(
                "text-generation",
                model=self.model_id,
                torch_dtype=torch.float32,
                device_map={"": self.device},
                trust_remote_code=True,
                max_length=2048
            )
            
            logging.info(f"Successfully loaded {self.model_id} on {self.device}")
            
        except Exception as e:
            logging.error(f"Failed to initialize model: {str(e)}")
            raise

    def generate(self, prompt: str) -> Optional[str]:
        try:
            response = self.pipe(
                prompt,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                num_return_sequences=1
            )
            
            if response and len(response) > 0:
                generated_text = response[0]['generated_text']
                # Remove prompt from response
                result = generated_text[len(prompt):].strip()
                return result
                
            return None
            
        except Exception as e:
            logging.error(f"Generation error: {str(e)}")
            return None