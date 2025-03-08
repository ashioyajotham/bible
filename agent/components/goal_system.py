from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class GoalPriority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Goal:
    description: str
    priority: GoalPriority
    success_criteria: List[str]
    
class GoalSystem:
    def __init__(self):
        self.goals = []
        self.active_goals = []
        
    def add_goal(self, goal: Goal):
        self.goals.append(goal)
        
    def prioritize_goals(self, context: Dict) -> List[Goal]:
        return sorted(self.goals, key=lambda x: x.priority.value)