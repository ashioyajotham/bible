import torch
from transformers import pipeline
from huggingface_hub import login, HfFolder
from .base_llm import BaseLLM
import os
import logging
from config.settings import Config

class HuggingFaceLLM(BaseLLM):
    def __init__(self, model_id: str = "meta-llama/Llama-3.1-70B-Instruct"):
        self._authenticate()
        try:
            # Suppress TensorFlow logging
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Only show errors
            # Disable oneDNN custom operations message
            os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
            
            self.generator = pipeline(
                "text-generation",
                model=model_id,
                device_map="auto",
                trust_remote_code=True,
                temperature=0.7,
                max_length=512
            )
            logging.info(f"Successfully loaded model {model_id}")
        except Exception as e:
            logging.error(f"Failed to load model {model_id}: {str(e)}")
            raise

    def _authenticate(self):
        """Authenticate with HuggingFace"""
        hf_token = Config.HF_TOKEN
        if not hf_token:
            raise ValueError("HF_TOKEN not found in environment variables")
        try:
            login(token=hf_token)
            logging.info("Successfully authenticated with HuggingFace")
        except Exception as e:
            logging.error(f"HuggingFace authentication failed: {str(e)}")
            raise

    def generate(self, prompt: str, **kwargs) -> str:
        try:
            response = self.generator(
                prompt,
                max_length=kwargs.get('max_length', 512),
                do_sample=True,
                temperature=kwargs.get('temperature', 0.7)
            )
            return response[0]['generated_text']
        except Exception as e:
            logging.error(f"Generation failed: {str(e)}")
            raise