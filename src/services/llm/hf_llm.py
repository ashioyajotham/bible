from transformers import AutoTokenizer, pipeline, AutoModelForCausalLM
import torch
import logging
from typing import Optional
from .model_types import ModelType

class HuggingFaceLLM:
    def __init__(self, model_id: str = None):
        try:
            # Set model type and configuration
            if "phi-2" in model_id:
                self.model_type = ModelType.PHI
                self.system_prompt = "You are a biblical teaching assistant focused on providing clear, accurate spiritual insights."
            elif "llama" in model_id.lower():
                self.model_type = ModelType.LLAMA
            else:
                self.model_type = ModelType.PHI
                
            self.model_id = model_id or "microsoft/phi-2"
            self.device = "cpu"
            
            # Load model with optimizations
            model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True,
                use_cache=True,
                device_map={"": self.device}
            )
            
            tokenizer = AutoTokenizer.from_pretrained(
                self.model_id,
                use_fast=True  # Use faster tokenizer
            )
            
            # Configure pipeline with optimizations
            self.pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                torch_dtype=torch.float32,
                device_map={"": self.device},
                max_length=2048,
                trust_remote_code=True,
                # Performance optimizations
                framework="pt",
                batch_size=1,
                use_cache=True
            )
            
            logging.info(f"Successfully loaded {self.model_id} with optimizations")
            
        except Exception as e:
            logging.error(f"Failed to initialize model: {str(e)}")
            raise

    def generate(self, prompt: str) -> Optional[str]:
        try:
            # Improved prompt engineering
            formatted_prompt = f"""You are a biblical teaching assistant providing direct spiritual insights.

Topic: {prompt}

Share biblical teachings about this topic, including:
- Key Biblical principles with accurate scripture references
- Clear spiritual insights from God's Word
- Practical applications for daily life
- Examples from Biblical narratives

Remember to speak directly to the reader and maintain a pastoral tone.
"""
            # Optimize generation parameters
            response = self.pipe(
                formatted_prompt,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.8,  # Slightly increased for more natural language
                top_p=0.92,
                top_k=50,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3,
                pad_token_id=self.pipe.tokenizer.eos_token_id
            )
            
            if response and len(response) > 0:
                # Clean up response
                text = response[0]['generated_text']
                # Remove prompt and any meta-instructions
                text = text.replace(formatted_prompt, "").strip()
                text = text.split("Generated using")[0].strip()
                return text
                
            return None
            
        except Exception as e:
            logging.error(f"Generation error: {str(e)}")
            return None