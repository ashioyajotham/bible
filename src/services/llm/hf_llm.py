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
            # Format teaching prompt
            formatted_prompt = f"""
            As a biblical teaching assistant, provide insights on:
            {prompt}
            
            Focus on biblical accuracy and spiritual depth.
            Include scripture references and practical applications.
            """
            
            response = self.pipe(
                formatted_prompt,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                num_return_sequences=1,
                pad_token_id=self.pipe.tokenizer.eos_token_id,
                repetition_penalty=1.2
            )
            
            if response and len(response) > 0:
                generated_text = response[0]['generated_text']
                # Extract only the generated content, removing prompt
                result = generated_text[len(formatted_prompt):].strip()
                
                # Format response if empty or too short
                if not result or len(result) < 50:
                    return "I apologize, but I need to reflect more deeply on this topic to provide meaningful biblical insights."
                    
                return result
                
            return None
            
        except Exception as e:
            logging.error(f"Generation error: {str(e)}")
            return None