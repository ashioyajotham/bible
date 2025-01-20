from .base_formatter import BaseFormatter
from typing import Dict, Any
from colorama import init, Fore, Style

init()  # Initialize colorama for Windows

class ConsoleFormatter(BaseFormatter):
    def format_verse(self, verse: Dict[str, Any]) -> str:
        return f"""
{Fore.CYAN}📖 Daily Verse{Style.RESET_ALL}
{Fore.YELLOW}>{Style.RESET_ALL} {verse['text']}

{Fore.GREEN}Reference{Style.RESET_ALL}: {verse['reference']}
{Fore.GREEN}Translation{Style.RESET_ALL}: {verse['translation']}
"""

    def format_teaching(self, teaching: Dict[str, Any]) -> str:
        return f"""
{Fore.CYAN}🎯 Biblical Teaching: {teaching['topic']}{Style.RESET_ALL}

{teaching['teaching']}

{Fore.BLUE}Generated using {teaching['model_used']} at {teaching['timestamp']}{Style.RESET_ALL}
"""

    def format_search_results(self, results: Dict[str, Any]) -> str:
        sources = "\n".join([f"{Fore.YELLOW}•{Style.RESET_ALL} {r['title']}" 
                           for r in results['online_sources']])
        
        return f"""
{Fore.CYAN}🔍 Biblical Insights: "{results['query']}"{Style.RESET_ALL}

{Fore.GREEN}AI Analysis:{Style.RESET_ALL}
{results['ai_analysis']}

{Fore.GREEN}Online Sources:{Style.RESET_ALL}
{sources}

{Fore.BLUE}Generated at {results['timestamp']}{Style.RESET_ALL}
"""
    from .base_formatter import BaseFormatter
from typing import Dict, Any
from colorama import init, Fore, Style

init()  # Initialize colorama for Windows

class ConsoleFormatter(BaseFormatter):
    def format_verse(self, verse: Dict[str, Any]) -> str:
        return f"""
{Fore.CYAN}📖 Daily Verse{Style.RESET_ALL}
{Fore.YELLOW}>{Style.RESET_ALL} {verse['text']}

{Fore.GREEN}Reference{Style.RESET_ALL}: {verse['reference']}
{Fore.GREEN}Translation{Style.RESET_ALL}: {verse['translation']}
"""

    def format_teaching(self, teaching: Dict[str, Any]) -> str:
        return f"""
{Fore.CYAN}🎯 Biblical Teaching: {teaching['topic']}{Style.RESET_ALL}

{teaching['teaching']}

{Fore.BLUE}Generated using {teaching['model_used']} at {teaching['timestamp']}{Style.RESET_ALL}
"""

    def format_search_results(self, results: Dict[str, Any]) -> str:
        sources = "\n".join([f"{Fore.YELLOW}•{Style.RESET_ALL} {r['title']}" 
                           for r in results['online_sources']])
        
        return f"""
{Fore.CYAN}🔍 Biblical Insights: "{results['query']}"{Style.RESET_ALL}

{Fore.GREEN}AI Analysis:{Style.RESET_ALL}
{results['ai_analysis']}

{Fore.GREEN}Online Sources:{Style.RESET_ALL}
{sources}

{Fore.BLUE}Generated at {results['timestamp']}{Style.RESET_ALL}
"""