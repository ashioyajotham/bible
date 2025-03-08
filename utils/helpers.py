from typing import Dict, List, Optional
import json
import logging
from datetime import datetime
from pathlib import Path

def format_verse(text: str, reference: str) -> str:
    """Format a Bible verse with its reference."""
    return f"{text} - {reference}"

def setup_logging(level=logging.INFO):
    """Setup logging configuration"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def validate_verse_reference(reference: str) -> bool:
    """Validate Bible verse reference format."""
    import re
    pattern = r'^[1-3]?[A-Za-z]+\s*\d+:\d+$'
    return bool(re.match(pattern, reference))

def save_to_file(data: Dict, filename: str, format: str = 'json') -> None:
    """Save data to file in specified format."""
    path = Path(filename)
    if format == 'json':
        with path.open('w') as f:
            json.dump(data, f, indent=4)
    elif format == 'txt':
        with path.open('w') as f:
            f.write(str(data))

def load_from_file(filename: str, format: str = 'json') -> Dict:
    """Load data from file."""
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"File {filename} not found")
    
    if format == 'json':
        with path.open('r') as f:
            return json.load(f)
    return {}

def sanitize_text(text: str) -> str:
    """Remove unwanted characters and normalize text."""
    return ' '.join(text.strip().split())

def format_timestamp(dt: datetime = None) -> str:
    """Format timestamp for logging."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def create_export_filename(prefix: str, format: str = 'md') -> str:
    """Create filename for exports."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{format}"

def log_message(message):
    """Log a message to the console."""
    print(f"[LOG] {message}")

def validate_input(data):
    """Validate input data for required fields."""
    if not data:
        raise ValueError("Input data cannot be empty.")
    return True

def parse_verse_data(verse_data: Dict) -> Dict:
    """Parse verse data from an API response."""
    return {
        "text": verse_data.get("text", "").strip(),
        "reference": verse_data.get("reference", ""),
        "translation": verse_data.get("translation", "KJV"),
        "timestamp": format_timestamp()
    }