from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Verse:
    text: str
    reference: str
    translation: str = "KJV"
    tags: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    is_favorite: bool = False
    
    def format_verse(self) -> str:
        """Returns formatted verse with reference"""
        return f"{self.text} ({self.reference} - {self.translation})"
    
    def to_dict(self) -> dict:
        """Convert verse to dictionary for serialization"""
        return {
            "text": self.text,
            "reference": self.reference,
            "translation": self.translation,
            "tags": self.tags,
            "timestamp": self.timestamp.isoformat(),
            "is_favorite": self.is_favorite
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Verse':
        """Create verse instance from dictionary"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
    
    def __str__(self) -> str:
        return self.format_verse()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the verse"""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the verse"""
        if tag in self.tags:
            self.tags.remove(tag)