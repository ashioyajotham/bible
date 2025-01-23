from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class StudySession:
    """Track Bible study session data"""
    teachings: List[Dict] = field(default_factory=list)
    searches: List[Dict] = field(default_factory=list)
    verses: List[Dict] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def add_search(self, search_data: Dict) -> None:
        """Add search results with consistent keys"""
        self.searches.append({
            "query": search_data["query"],
            "insights": search_data["insights"],  # Matches SearchAgent output
            "sources": search_data.get("sources", []),
            "timestamp": datetime.now().isoformat()
        })

    def add_teaching(self, teaching_data: Dict) -> None:
        """Add teaching to session with consistent keys"""
        self.teachings.append({
            "topic": teaching_data["topic"],
            "teaching": teaching_data["teaching"],  # Consistent with BibleAgent
            "timestamp": datetime.now().isoformat()
        })

    def add_verse(self, verse_data: Dict) -> None:
        """Add verse to session"""
        self.verses.append({
            "text": verse_data["text"],
            "reference": verse_data["reference"],
            "translation": verse_data["translation"],
            "timestamp": datetime.now().isoformat()
        })

    def get_latest_search(self) -> Optional[Dict]:
        """Get most recent search"""
        return self.searches[-1] if self.searches else None