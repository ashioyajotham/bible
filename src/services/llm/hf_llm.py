from transformers import AutoTokenizer, pipeline
import torch
import logging
from typing import Optional
from .model_types import ModelType

class HuggingFaceLLM:
    def __init__(self, model_id: str = None):
        try:
            # Set model type based on model_id
            if "phi-2" in model_id:
                self.model_type = ModelType.PHI
            elif "llama" in model_id.lower():
                self.model_type = ModelType.LLAMA
            else:
                self.model_type = ModelType.PHI  # Default fallback
                
            self.model_id = model_id or "microsoft/phi-2"  # Default to PHI-2
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