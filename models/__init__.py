"""
Scripture AI Agent Models
Core data models for scripture handling and persistence
"""

__version__ = "0.1.0"

from .verse import Verse

# Define supported Bible translations
SUPPORTED_TRANSLATIONS = ["KJV", "NIV", "ESV", "NKJV", "NLT"]

# Define common verse categories
VERSE_CATEGORIES = {
    "wisdom": "Proverbs, Ecclesiastes, Psalms",
    "gospel": "Matthew, Mark, Luke, John",
    "epistles": "Romans through Jude",
    "prophecy": "Isaiah through Malachi, Revelation"
}

__all__ = [
    'Verse',
    'SUPPORTED_TRANSLATIONS',
    'VERSE_CATEGORIES'
]