from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
import logging
import numpy as np
from dataclasses import dataclass, field
from collections import defaultdict
from .model_types import ModelType, TaskType  # Updated import
from .gemini_llm import GeminiLLM
from .hf_llm import HuggingFaceLLM
from config.settings import Config

@dataclass
class ModelCapability:
    name: str
    strengths: List[str]
    max_tokens: int
    avg_latency: float
    base_weight: float = 1.0

@dataclass
class ModelMetrics:
    success_count: int = 0
    fail_count: int = 0
    latencies: List[float] = field(default_factory=list)
    last_success: Optional[datetime] = None

class ModelSelector:
    def __init__(self):
        self._model_instances: Dict[ModelType, Any] = {}
        self.metrics = {model_type: ModelMetrics() for model_type in ModelType}
        self.capabilities = {
            ModelType.PHI: ModelCapability(
                name="microsoft/phi-2",
                strengths=["teaching", "reflection"],
                max_tokens=2048,
                avg_latency=2.0,
                base_weight=1.0  # Default fallback
            ),
            ModelType.GEMINI: ModelCapability(
                name="gemini-pro",
                strengths=["search", "analysis"],
                max_tokens=4096,
                avg_latency=1.5,
                base_weight=0.8
            ),
            ModelType.LLAMA: ModelCapability(
                name="meta-llama/Llama-2-7b-chat-hf",
                strengths=["teaching", "reflection"],
                max_tokens=4096,
                avg_latency=3.0,
                base_weight=0.7
            )
        }
        
        self.performance_history = defaultdict(list)
        self.task_affinity = self._initialize_task_affinity()
        self.models: Dict[ModelType, Any] = {}

    def _initialize_task_affinity(self) -> Dict:
        return {
            TaskType.TEACHING.value: {
                "required_capabilities": ["teaching"],
                "token_importance": 0.3,
                "latency_importance": 0.2
            },
            TaskType.SEARCH.value: {
                "required_capabilities": ["search"],
                "token_importance": 0.4,
                "latency_importance": 0.4
            },
            TaskType.ANALYSIS.value: {
                "required_capabilities": ["analysis"],
                "token_importance": 0.5,
                "latency_importance": 0.2
            },
            TaskType.REFLECTION.value: {
                "required_capabilities": ["reflection"],
                "token_importance": 0.2,
                "latency_importance": 0.1
            }
        }

    def select_model(self, task: TaskType, context: Optional[Dict] = None) -> ModelType:
        try:
            scores = {}
            task_config = self.task_affinity[task.value]
            
            for model_type, capability in self.capabilities.items():
                # Calculate capability match
                capability_score = self._calculate_capability_score(
                    capability.strengths,
                    task_config["required_capabilities"]
                )
                
                # Calculate performance score
                performance_score = self._calculate_performance_score(
                    model_type,
                    task_config["latency_importance"]
                )
                
                # Calculate context suitability
                context_score = self._calculate_context_score(
                    capability,
                    context,
                    task_config["token_importance"]
                )
                
                # Combine scores with base weight
                scores[model_type] = (
                    capability_score * 0.4 +
                    performance_score * 0.3 +
                    context_score * 0.3
                ) * capability.base_weight
                
            logging.debug(f"Model scores for {task.value}: {scores}")
            
            # Select highest scoring model or fallback to PHI
            selected = max(scores.items(), key=lambda x: x[1])[0]
            return selected if scores[selected] > 0.4 else ModelType.PHI
            
        except Exception as e:
            logging.error(f"Model selection error: {str(e)}")
            return ModelType.PHI  # Safe fallback

    def _initialize_model(self, model_type: ModelType) -> Optional[Any]:
        """Initialize a new model instance"""
        try:
            if model_type == ModelType.PHI:
                return HuggingFaceLLM(model_id="microsoft/phi-2")
            elif model_type == ModelType.GEMINI:
                return GeminiLLM(api_key=Config.GEMINI_API_KEY)
            elif model_type == ModelType.LLAMA:
                return HuggingFaceLLM(model_id="meta-llama/Llama-2-7b-chat-hf")
            return None
        except Exception as e:
            logging.error(f"Model initialization error for {model_type}: {str(e)}")
            return None

    def get_model(self, model_type: ModelType) -> Optional[Any]:
        """Get or create model instance"""
        if model_type not in self._model_instances:
            model = self._initialize_model(model_type)
            if model:
                self._model_instances[model_type] = model
            else:
                return None
        return self._model_instances.get(model_type)

    def select_and_get_model(self, task: TaskType, context: Optional[Dict] = None) -> Optional[Any]:
        """Select and return initialized model"""
        try:
            # Get model type with highest score
            selected_type = self.select_model(task, context)
            logging.info(f"Selected model type: {selected_type}")

            # Try to get/initialize selected model
            model = self.get_model(selected_type)
            if model:
                return model

            # Fallback to PHI if primary fails
            logging.warning(f"Primary model {selected_type} failed, trying PHI")
            return self.get_model(ModelType.PHI)

        except Exception as e:
            logging.error(f"Model selection/initialization failed: {str(e)}")
            return None

    def _calculate_capability_score(self, model_strengths: List[str], required_capabilities: List[str]) -> float:
        if not required_capabilities:
            return 1.0
        matches = sum(1 for cap in required_capabilities if cap in model_strengths)
        return matches / len(required_capabilities)

    def _calculate_performance_score(self, model_type: ModelType, latency_importance: float) -> float:
        metrics = self.metrics[model_type]
        total_attempts = metrics.success_count + metrics.fail_count
        
        if total_attempts == 0:
            return 0.5  # Default score for new models
            
        success_rate = metrics.success_count / total_attempts
        avg_latency = np.mean(metrics.latencies[-20:]) if metrics.latencies else 3.0
        latency_score = 1.0 / (1.0 + avg_latency)
        
        return (success_rate * (1 - latency_importance) + 
                latency_score * latency_importance)

    def _calculate_context_score(self, capability: ModelCapability, 
                               context: Optional[Dict], token_importance: float) -> float:
        if not context:
            return 0.5
            
        input_length = len(str(context.get('topic', '')))
        token_capacity = min(1.0, capability.max_tokens / 4096)  # Normalize to 0-1
        
        return token_capacity * token_importance + 0.5 * (1 - token_importance)

    def _calculate_recency(self, last_used: Optional[datetime]) -> float:
        if not last_used:
            return 0.5
        hours_ago = (datetime.now() - last_used).total_seconds() / 3600
        return 1.0 / (1.0 + hours_ago)  # Decay over time

    def update_performance(self, model: ModelType, success: bool, latency: float):
        metrics = self.metrics[model]
        if success:
            metrics.success_count += 1
            metrics.last_success = datetime.now()
        else:
            metrics.fail_count += 1
        metrics.latencies.append(latency)
        
        # Keep only last 100 latency measurements
        if len(metrics.latencies) > 100:
            metrics.latencies.pop(0)