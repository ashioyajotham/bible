def format_verse(text, reference):
    """Format a Bible verse with its reference."""
    return f"{text} - {reference}"

def log_message(message):
    """Log a message to the console."""
    print(f"[LOG] {message}")

def validate_input(data):
    """Validate input data for required fields."""
    if not data:
        raise ValueError("Input data cannot be empty.")
    return True

def parse_verse_data(verse_data):
    """Parse verse data from an API response."""
    return {
        "text": verse_data.get("text"),
        "reference": verse_data.get("reference"),
    }