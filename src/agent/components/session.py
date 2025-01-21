from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class StudySession:
    verses: List[Dict] = field(default_factory=list)
    teachings: List[Dict] = field(default_factory=list)
    searches: List[Dict] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class StudySession:
    verses: List[Dict] = field(default_factory=list)
    teachings: List[Dict] = field(default_factory=list)
    searches: List[Dict] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())