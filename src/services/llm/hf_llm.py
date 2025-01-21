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
            # Create structured prompt
            formatted_prompt = f"""{self.system_prompt}

Question: {prompt}

Provide biblical teaching with:
1. Clear theological insights
2. Scripture references
3. Practical applications

Response:"""

            # Generate with optimized parameters
            response = self.pipe(
                formatted_prompt,
                max_new_tokens=256,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                top_k=40,
                num_return_sequences=1,
                repetition_penalty=1.2,
                # Stop on common end markers
                eos_token_id=self.pipe.tokenizer.eos_token_id,
                pad_token_id=self.pipe.tokenizer.eos_token_id,
                # Prevent prompt repetition
                no_repeat_ngram_size=3
            )
            
            if response and len(response) > 0:
                # Extract only the response part
                generated_text = response[0]['generated_text']
                # Find where the actual response starts
                response_start = generated_text.find("Response:") + 9
                if response_start > 8:
                    return generated_text[response_start:].strip()
                return generated_text.replace(formatted_prompt, "").strip()
                
            return None
            
        except Exception as e:
            logging.error(f"Generation error: {str(e)}")
            return None