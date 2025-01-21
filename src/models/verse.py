"""
The Verse class represents a Bible verse with text, reference, translation, tags, timestamp, and favorite status.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from .verse_categories import VerseCategory

@dataclass
class Verse:
    text: str
    reference: str
    translation: str = "KJV"
    tags: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    is_favorite: bool = False
    category: Optional[VerseCategory] = None
    study_notes: List[str] = field(default_factory=list)
    cross_references: List[str] = field(default_factory=list)
    last_reviewed: Optional[datetime] = None
    times_reviewed: int = 0
    
    def format_verse(self) -> str:
        """Returns formatted verse with reference"""
        return f"{self.text} ({self.reference} - {self.translation})"
    
    def to_dict(self) -> dict:
        """Convert verse to dictionary for serialization"""
        return {
            "text": self.text,
            "reference": self.reference,
            "translation": self.translation
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
    
    def add_study_note(self, note: str):
        self.study_notes.append(note)
        self.last_reviewed = datetime.now()
        self.times_reviewed += 1
    
    def add_cross_reference(self, reference: str):
        if reference not in self.cross_references:
            self.cross_references.append(reference)
    
    def get_review_status(self) -> str:
        if not self.last_reviewed:
            return "Never reviewed"
        days_since = (datetime.now() - self.last_reviewed).days
        return f"Last reviewed {days_since} days ago"