from colorama import init, Fore, Style
from typing import Dict, Any

init()

class ConsoleFormatter:
    def format_verse(self, verse: Dict[str, Any]) -> str:
        return f"{Fore.CYAN}📖 Daily Verse{Style.RESET_ALL}\n{Fore.YELLOW}>{Style.RESET_ALL} {verse['text']}\n\n{Fore.GREEN}Reference{Style.RESET_ALL}: {verse['reference']}\n{Fore.GREEN}Translation{Style.RESET_ALL}: {verse['translation']}\n"

    def format_teaching(self, teaching: Dict[str, Any]) -> str:
        content = teaching['teaching']
        sections = content.split('\n\n')
        formatted_sections = []
        
        for section in sections:
            if '**' in section:
                title = section.split('**')[1]
                formatted_sections.append(f"{Fore.CYAN}{title}{Style.RESET_ALL}")
                content = section.split('\n', 1)[1] if '\n' in section else ''
                if content:
                    formatted_sections.append(content)
            else:
                formatted_sections.append(section)

        return f"{Fore.GREEN}🎯 Biblical Teaching: {teaching['topic']}{Style.RESET_ALL}\n\n{Fore.WHITE}{chr(10).join(formatted_sections)}{Style.RESET_ALL}\n\n{Fore.BLUE}Generated using {teaching['model_used']} at {teaching['timestamp']}{Style.RESET_ALL}"

    def format_search_results(self, results: Dict[str, Any]) -> str:
        online_sources = "\n".join([
            f"{Fore.YELLOW}• {source['title']}{Style.RESET_ALL}\n  {Fore.BLUE}{source['link']}{Style.RESET_ALL}"
            for source in results['online_sources']
        ])

        return f"""
{Fore.CYAN}🔍 Biblical Search: "{results['query']}"{Style.RESET_ALL}

{Fore.GREEN}AI Analysis:{Style.RESET_ALL}
{results['ai_analysis']}

{Fore.GREEN}Related Sources:{Style.RESET_ALL}
{online_sources}

{Fore.BLUE}Generated at {results['timestamp']}{Style.RESET_ALL}
"""