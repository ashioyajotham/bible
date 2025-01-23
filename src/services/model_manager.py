from typing import Dict, Optional
from .llm.gemini_llm import GeminiLLM
from .llm.model_types import ModelType
from config.settings import Config
import logging

class ModelManager:
    _instance = None
    _models: Dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance

    def get_model(self, model_type: ModelType):
        """Get or create model instance"""
        if model_type not in self._models:
            try:
                if model_type == ModelType.GEMINI:
                    self._models[model_type] = GeminiLLM(api_key=Config.GEMINI_API_KEY)
                logging.info(f"Initialized model: {model_type}")
            except Exception as e:
                logging.error(f"Failed to initialize model {model_type}: {str(e)}")
                return None
        return self._models[model_type]