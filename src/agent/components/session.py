from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime

@dataclass
class StudySession:
    teachings: List[Dict] = field(default_factory=list)
    searches: List[Dict] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def add_search(self, search_data: Dict) -> None:
        """Add search results to session"""
        self.searches.append({
            "query": search_data["query"],
            "theological_analysis": search_data["theological_analysis"],
            "key_points": search_data["key_points"],
            "references": search_data["references"],
            "reflection": search_data["reflection"],
            "sources": search_data["sources"],
            "timestamp": datetime.now().isoformat()
        })