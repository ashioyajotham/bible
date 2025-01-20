from .base_formatter import BaseFormatter
from typing import Dict, Any
from datetime import datetime

class MarkdownFormatter(BaseFormatter):
    def format_verse(self, verse: Dict[str, Any]) -> str:
        return f"""
## 📖 Daily Verse

> {verse['text']}

**Reference**: {verse['reference']}  
**Translation**: {verse['translation']}

---"""

    def format_teaching(self, teaching: Dict[str, Any]) -> str:
        return f"""
## 🎯 Biblical Teaching: {teaching['topic']}

{teaching['teaching']}

*Generated using {teaching['model_used']} at {teaching['timestamp']}*

---"""

    def format_search_results(self, results: Dict[str, Any]) -> str:
        sources = '\n'.join([
            f"- [{source['title']}]({source['link']})"
            for source in results['online_sources']
        ])
        
        return f"""
## 🔍 Biblical Insights: "{results['query']}"

### AI Analysis
{results['ai_analysis']}

### Online Sources
{sources}

*Generated at {results['timestamp']}*

---"""