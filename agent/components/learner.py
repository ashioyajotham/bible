from typing import Dict, List
from datetime import datetime
import json

class Learner:
    def __init__(self):
        self.experiences = []
        self.patterns = {}
        self.strategies = {}
        self.performance_metrics = {}
        
    def learn(self, observation: Dict, result: Dict):
        """Learn from interaction"""
        experience = {
            'timestamp': datetime.now().isoformat(),
            'observation': observation,
            'result': result,
            'success': self._evaluate_success(result)
        }
        
        self.experiences.append(experience)
        self._update_patterns(experience)
        self._adapt_strategies(experience)
        
    def _evaluate_success(self, result: Dict) -> bool:
        """Evaluate success of interaction"""
        if 'error' in result:
            return False
        return result.get('success', True)
        
    def _update_patterns(self, experience: Dict):
        """Identify and update patterns"""
        pattern_key = self._extract_pattern(experience)
        if pattern_key not in self.patterns:
            self.patterns[pattern_key] = []
        self.patterns[pattern_key].append(experience)
        
    def _adapt_strategies(self, experience: Dict):
        """Adapt strategies based on learning"""
        if experience['success']:
            self._reinforce_strategy(experience)
        else:
            self._revise_strategy(experience)