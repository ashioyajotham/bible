from enum import Enum
from typing import Dict, Optional
from datetime import datetime

class ModelType(Enum):
    GEMINI = "gemini"
    LLAMA = "llama"

class TaskType(Enum):
    REFLECTION = "reflection"
    ANALYSIS = "analysis"
    TEACHING = "teaching"
    SEARCH = "search"

class ModelSelector:
    def __init__(self):
        self.model_strengths = {
            ModelType.GEMINI: {
                TaskType.REFLECTION: 0.9,
                TaskType.TEACHING: 0.8,
                TaskType.ANALYSIS: 0.7,
                TaskType.SEARCH: 0.7
            },
            ModelType.LLAMA: {
                TaskType.ANALYSIS: 0.9,
                TaskType.SEARCH: 0.8,
                TaskType.TEACHING: 0.7,
                TaskType.REFLECTION: 0.6
            }
        }
        self.performance_history = {}
        
    def select_model(self, task: TaskType, context: Dict) -> ModelType:
        """Select best model based on task type and context"""
        scores = {}
        for model in ModelType:
            base_score = self.model_strengths[model][task]
            performance_score = self._get_performance_score(model)
            scores[model] = base_score * performance_score
            
        return max(scores.items(), key=lambda x: x[1])[0]
        
    def _get_performance_score(self, model: ModelType) -> float:
        if model not in self.performance_history:
            return 1.0
        
        successes = sum(1 for x in self.performance_history[model] if x['success'])
        total = len(self.performance_history[model])
        return successes / total if total > 0 else 1.0

    def track_performance(self, model: ModelType, success: bool):
        if model not in self.performance_history:
            self.performance_history[model] = []
            
        self.performance_history[model].append({
            'timestamp': datetime.now(),
            'success': success
        })