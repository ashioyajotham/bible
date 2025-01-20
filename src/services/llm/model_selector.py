from enum import Enum
from typing import Dict, Optional
from datetime import datetime
import logging

class TaskType(Enum):
    SEARCH = "search"           # Biblical search and research
    TEACHING = "teaching"       # Extracting teachings and lessons
    ANALYSIS = "analysis"       # Deep scriptural analysis
    REFLECTION = "reflection"   # Personal/devotional reflection

class ModelType(Enum):
    GEMINI = "gemini"  # Better for factual, structured responses
    LLAMA = "llama"    # Better for creative, reflective content

class ModelSelector:
    def __init__(self):
        self.performance_metrics = {
            ModelType.GEMINI: {"success_rate": 0.9, "avg_latency": 1.2},
            ModelType.LLAMA: {"success_rate": 0.85, "avg_latency": 2.0}
        }
        self.task_preferences = {
            TaskType.SEARCH: {"factual_weight": 0.8, "creative_weight": 0.2},
            TaskType.TEACHING: {"factual_weight": 0.6, "creative_weight": 0.4},
            TaskType.ANALYSIS: {"factual_weight": 0.7, "creative_weight": 0.3},
            TaskType.REFLECTION: {"factual_weight": 0.3, "creative_weight": 0.7}
        }
        self.history = []

    def select_model(self, task: TaskType, context: Optional[Dict] = None) -> ModelType:
        """Select best model based on task requirements and context"""
        context = context or {}
        logging.debug(f"Selecting model for task: {task.value} with context: {context}")

        try:
            # Get task preferences
            preferences = self.task_preferences[task]
            
            # Calculate scores for each model
            scores = {}
            for model in ModelType:
                metrics = self.performance_metrics[model]
                score = self._calculate_model_score(model, task, metrics, preferences)
                scores[model] = score

            # Select model with highest score
            selected_model = max(scores.items(), key=lambda x: x[1])[0]
            
            # Record selection
            self._record_selection(selected_model, task, context)
            
            logging.debug(f"Selected model {selected_model.value} with scores: {scores}")
            return selected_model

        except Exception as e:
            logging.error(f"Error selecting model: {str(e)}")
            return ModelType.GEMINI  # Default fallback

    def _calculate_model_score(self, model: ModelType, task: TaskType, 
                             metrics: Dict, preferences: Dict) -> float:
        """Calculate score for a model based on task requirements"""
        base_score = metrics['success_rate'] * 0.7 + (1 / metrics['avg_latency']) * 0.3
        
        if model == ModelType.GEMINI:
            task_alignment = preferences['factual_weight']
        else:  # LLAMA
            task_alignment = preferences['creative_weight']
            
        return base_score * task_alignment

    def _record_selection(self, model: ModelType, task: TaskType, context: Dict):
        """Record model selection for performance tracking"""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'model': model.value,
            'task': task.value,
            'context': context
        })

    def update_performance(self, model: ModelType, success: bool, latency: float):
        """Update performance metrics for a model"""
        metrics = self.performance_metrics[model]
        current_success = metrics['success_rate']
        current_latency = metrics['avg_latency']
        
        # Update with moving average
        alpha = 0.1  # Learning rate
        metrics['success_rate'] = current_success * (1-alpha) + int(success) * alpha
        metrics['avg_latency'] = current_latency * (1-alpha) + latency * alpha