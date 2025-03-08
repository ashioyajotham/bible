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

    def format_study_session(self, content: Dict[str, Any]) -> str:
        output = [
            "# 📚 Bible Study Session\n",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        ]

        if 'verse' in content:
            output.extend([
                "## 📖 Daily Verse\n\n",
                f"> {content['verse']['text']}\n\n",
                f"**Reference**: {content['verse']['reference']}  \n",
                f"**Translation**: {content['verse']['translation']}\n\n"
            ])

        if 'teaching' in content:
            output.extend([
                f"## 🎯 Biblical Teaching: {content['teaching']['topic']}\n\n",
                f"{content['teaching']['teaching']}\n\n"
            ])

        if 'search_results' in content:
            output.extend([
                f"## 🔍 Biblical Insights: {content['search_results']['query']}\n\n",
                "### Analysis\n",
                f"{content['search_results']['ai_analysis']}\n\n",
                "### Sources\n",
                *[f"- [{source['title']}]({source['link']})\n" 
                  for source in content['search_results']['online_sources']]
            ])

        return "".join(output)