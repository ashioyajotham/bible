from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from .components.goal_system import GoalSystem
from .components.planner import Planner
from .components.memory import Memory
from .components.learner import Learner

class AgentState(Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    LEARNING = "learning"
    REFLECTING = "reflecting"

@dataclass
class AgentContext:
    state: AgentState
    confidence: float
    last_action: Optional[str]
    current_goal: Optional[Dict]

class BaseAgent:
    def __init__(self):
        self.goal_system = GoalSystem()
        self.planner = Planner()
        self.memory = Memory()
        self.learner = Learner()
        self.context = AgentContext(
            state=AgentState.IDLE,
            confidence=1.0,
            last_action=None,
            current_goal=None
        )
        
    def step(self, observation: Dict) -> Dict:
        self.context.state = AgentState.PLANNING
        
        # Self-reflection
        self._reflect_on_state()
        
        # Dynamic goal adjustment
        goals = self.goal_system.prioritize_goals(observation)
        self._adjust_goals(observation, goals)
        
        # Planning with confidence
        plan = self.planner.create_plan(goals[0], observation)
        if not self._validate_plan(plan):
            plan = self._create_alternative_plan(observation)
            
        # Execute with monitoring
        self.context.state = AgentState.EXECUTING
        result = self.planner.execute_plan(plan)
        
        # Learn and adapt
        self.context.state = AgentState.LEARNING
        self.memory.store(observation, result)
        self.learner.learn(observation, result)
        
        # Final reflection
        self.context.state = AgentState.REFLECTING
        self._reflect_on_execution(result)
        
        self.context.state = AgentState.IDLE
        return result

    def _reflect_on_state(self):
        """Agent self-reflection"""
        recent_performance = self.learner.get_recent_performance()
        self.context.confidence = self._calculate_confidence(recent_performance)
        
    def _adjust_goals(self, observation: Dict, current_goals: List):
        """Dynamic goal adjustment"""
        if self.context.confidence < 0.5:
            self.goal_system.add_remedial_goals()
        
    def _validate_plan(self, plan: Dict) -> bool:
        """Validate plan against current context"""
        return self.context.confidence > 0.7 and plan.get('steps')
        
    def _reflect_on_execution(self, result: Dict):
        """Post-execution reflection"""
        success = result.get('success', False)
        self.learner.update_strategies(success)
        self.context.last_action = result.get('action')