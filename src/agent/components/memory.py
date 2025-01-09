from typing import Dict, List, Optional
from datetime import datetime
import json

class Memory:
    def __init__(self):
        self.short_term = []  # Recent interactions
        self.long_term = {}   # Persistent knowledge
        self.episodic = []    # Specific events/experiences
        self.semantic = {}    # Biblical knowledge base
        self.max_short_term = 50
        
    def store(self, observation: Dict, result: Dict):
        """Store new memory"""
        memory_entry = {
            'timestamp': datetime.now().isoformat(),
            'observation': observation,
            'result': result,
            'type': self._classify_memory(observation)
        }
        
        self.short_term.append(memory_entry)
        if len(self.short_term) > self.max_short_term:
            self._consolidate_memory()
            
    def _classify_memory(self, observation: Dict) -> str:
        """Classify memory type"""
        if 'verse' in observation:
            return 'biblical'
        elif 'question' in observation:
            return 'interaction'
        return 'general'
        
    def _consolidate_memory(self):
        """Move short-term to long-term memory"""
        for memory in self.short_term[:-10]:  # Keep last 10 memories
            if memory['type'] == 'biblical':
                self._store_semantic(memory)
            else:
                self._store_episodic(memory)
        self.short_term = self.short_term[-10:]