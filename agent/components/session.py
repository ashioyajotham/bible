from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class StudySession:
    """Track Bible study session with consistent data structures"""
    teachings: List[Dict] = field(default_factory=list)
    verses: List[Dict] = field(default_factory=list)
    reflections: List[Dict] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def add_teaching(self, data: Dict) -> None:
        """Add teaching with standardized structure"""
        teaching = {
            "query": data["query"],
            "insights": data["insights"],
            "references": data.get("references", []),
            "application": data.get("application", ""),
            "prayer": data.get("prayer", ""),
            "sources": data.get("sources", []),
            "timestamp": datetime.now().isoformat()
        }
        self.teachings.append(teaching)

    def add_verse(self, verse_data: Dict) -> None:
        """Add verse with standardized structure"""
        verse = {
            "text": verse_data["text"],
            "reference": verse_data["reference"],
            "translation": verse_data["translation"],
            "devotional": verse_data.get("devotional", ""),
            "timestamp": datetime.now().isoformat()
        }
        self.verses.append(verse)

    def add_reflection(self, reflection: Dict) -> None:
        """Add reflection with standardized structure"""
        self.reflections.append({
            "context_type": reflection["context_type"],
            "insights": reflection["insights"],
            "application": reflection["application"],
            "prayer": reflection["prayer"],
            "timestamp": datetime.now().isoformat()
        })

    def get_latest_content(self) -> Optional[Dict]:
        """Get most recent content for reflection"""
        if self.teachings:
            return {'type': 'teaching', 'content': self.teachings[-1]}
        if self.verses:
            return {'type': 'verse', 'content': self.verses[-1]}
        return None