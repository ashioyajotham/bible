import pytest
from datetime import datetime
from src.agent.components.planner import Planner, ActionStep
from src.agent.components.goal_system import Goal

@pytest.fixture
def planner():
    return Planner()

@pytest.fixture
def sample_goal():
    return Goal(
        topic="forgiveness",
        requires_search=True,
        requires_teaching=True,
        requires_reflection=True,
        timestamp=datetime.now()
    )

@pytest.fixture
def sample_context():
    return {
        "model_type": "gemini",
        "translation": "ESV",
        "previous_studies": []
    }

class TestPlanner:
    def test_create_plan_basic(self, planner, sample_goal, sample_context):
        # Test basic plan creation
        plan = planner.create_plan(sample_goal, sample_context)
        
        assert isinstance(plan, list)
        assert all(isinstance(step, ActionStep) for step in plan)
        
    def test_create_plan_steps_structure(self, planner, sample_goal, sample_context):
        # Test plan steps have correct structure
        plan = planner.create_plan(sample_goal, sample_context)
        
        for step in plan:
            assert hasattr(step, 'tool')
            assert hasattr(step, 'params')
            assert hasattr(step, 'expected_outcome')
            assert isinstance(step.params, dict)
            assert isinstance(step.expected_outcome, str)

    def test_execute_plan(self, planner):
        # Test plan execution
        steps = [
            ActionStep(
                tool="search",
                params={"query": "forgiveness"},
                expected_outcome="Biblical references"
            ),
            ActionStep(
                tool="teach",
                params={"topic": "forgiveness"},
                expected_outcome="Teaching content"
            )
        ]
        
        results = planner.execute_plan(steps)
        assert isinstance(results, dict)
        assert "search" in results
        assert "teach" in results

    def test_plan_with_empty_goal(self, planner):
        # Test handling empty goal
        empty_goal = Goal(
            topic="",
            requires_search=False,
            requires_teaching=False,
            requires_reflection=False,
            timestamp=datetime.now()
        )
        
        plan = planner.create_plan(empty_goal, {})
        assert len(plan) == 0

    def test_plan_execution_error_handling(self, planner):
        # Test error handling during execution
        invalid_step = ActionStep(
            tool="invalid_tool",
            params={},
            expected_outcome="Should fail"
        )
        
        with pytest.raises(Exception):
            planner.execute_plan([invalid_step])

    def test_plan_context_influence(self, planner, sample_goal):
        # Test how context affects plan creation
        context_with_history = {
            "model_type": "gemini",
            "translation": "ESV",
            "previous_studies": ["love", "faith"]
        }
        
        context_without_history = {
            "model_type": "gemini",
            "translation": "ESV",
            "previous_studies": []
        }
        
        plan_with_history = planner.create_plan(sample_goal, context_with_history)
        plan_without_history = planner.create_plan(sample_goal, context_without_history)
        
        assert len(plan_with_history) == len(plan_without_history)