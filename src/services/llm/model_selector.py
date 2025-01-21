from enum import Enum
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import logging
import numpy as np
from dataclasses import dataclass, field

class TaskType(Enum):
    SEARCH = "search"           # Biblical search and research
    TEACHING = "teaching"       # Extracting teachings and lessons
    ANALYSIS = "analysis"       # Deep scriptural analysis
    REFLECTION = "reflection"   # Personal/devotional reflection

class ModelType(Enum):
    GEMINI = "gemini"  # Better for factual, structured responses
    LLAMA = "llama"    # Better for creative, reflective content

class ModelMetrics:
    def __init__(self):
        self.success_count: int = 0
        self.fail_count: int = 0
        self.latencies: List[float] = []
        self.last_used: Optional[datetime] = None
        
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.fail_count
        return self.success_count / total if total > 0 else 0.5

class ModelSelector:
    def __init__(self):
        self.metrics = {
            ModelType.GEMINI: ModelMetrics(),
            ModelType.LLAMA: ModelMetrics()
        }
        
        # Initialize base weights
        self.task_preferences = {
            TaskType.TEACHING: {
                ModelType.GEMINI: 0.6,
                ModelType.LLAMA: 0.8  # LLAMA preferred for teaching
            },
            TaskType.SEARCH: {
                ModelType.GEMINI: 0.8,  # Gemini preferred for search
                ModelType.LLAMA: 0.6
            }
        }

    def select_model(self, task: TaskType, context: Optional[Dict] = None) -> ModelType:
        try:
            scores = {}
            for model in ModelType:
                metrics = self.metrics[model]
                base_score = self.task_preferences[task][model]
                
                # Calculate score components
                success_component = metrics.success_rate * 0.4
                recency_component = self._calculate_recency(metrics.last_used) * 0.2
                task_component = base_score * 0.4
                
                scores[model] = success_component + recency_component + task_component
                
            logging.debug(f"Detailed scores - {scores}")
            
            # Try Gemini first
            if scores[ModelType.GEMINI] > 0.4:
                return ModelType.GEMINI
                
            # Fallback to LLAMA
            logging.info("Falling back to LLAMA model")
            return ModelType.LLAMA
            
        except Exception as e:
            logging.error(f"Error in model selection: {str(e)}")
            return ModelType.LLAMA  # Default fallback
            
    def _calculate_recency(self, last_used: Optional[datetime]) -> float:
        if not last_used:
            return 0.5
        hours_ago = (datetime.now() - last_used).total_seconds() / 3600
        return 1.0 / (1.0 + hours_ago)  # Decay over time

    def update_performance(self, model: ModelType, success: bool, latency: float):
        metrics = self.metrics[model]
        if success:
            metrics.success_count += 1
        else:
            metrics.fail_count += 1
        
        metrics.latencies.append(latency)
        metrics.last_used = datetime.now()
        
        # Keep only last 100 latencies
        if len(metrics.latencies) > 100:
            metrics.latencies.pop(0)