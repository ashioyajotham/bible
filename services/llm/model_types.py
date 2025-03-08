from enum import Enum, auto

class ModelType(Enum):
    """Available model types"""
    GEMINI = auto()

class TaskType(Enum):
    """Task categories for model selection"""
    TEACHING = auto()
    REFLECTION = auto()
    VERSE_ANALYSIS = auto()