from colorama import init, Fore, Style
from typing import Dict, Any


init()

class ConsoleFormatter:
    def format_verse(self, verse: Dict[str, Any]) -> str:
        return (
            f"{Fore.CYAN}📖 Daily Verse{Style.RESET_ALL}\n"
            f"{Fore.YELLOW}>{Style.RESET_ALL} {verse['text']}\n\n"
            f"{Fore.GREEN}Reference{Style.RESET_ALL}: {verse['reference']}\n"
            f"{Fore.GREEN}Translation{Style.RESET_ALL}: {verse['translation']}\n"
        )

    def format_teaching(self, teaching: Dict[str, Any]) -> str:
        if not teaching or 'teaching' not in teaching:
            return f"{Fore.RED}No teaching content available{Style.RESET_ALL}"

        return (
            f"\n{Fore.CYAN}🎯 Biblical Teaching: {teaching['topic']}{Style.RESET_ALL}\n\n"
            f"{teaching['teaching']}\n\n"
            f"{Fore.BLUE}Generated using {teaching['model_used']} "
            f"at {teaching['timestamp']}{Style.RESET_ALL}\n"
        )

    def format_search_results(self, results: Dict[str, Any]) -> str:
        # Convert markdown headers to colored console output
        analysis = results['ai_analysis'].replace('## ', f"\n{Fore.CYAN}")
        analysis = analysis.replace('### ', f"\n{Fore.GREEN}")
        
        online_sources = "\n".join([
            f"{Fore.YELLOW}• {source['title']}{Style.RESET_ALL}\n  {Fore.BLUE}{source['link']}{Style.RESET_ALL}"
            for source in results['online_sources']
        ])

        return f"""
{Fore.CYAN}🔍 Biblical Search: "{results['query']}"{Style.RESET_ALL}

{analysis}{Style.RESET_ALL}

{Fore.GREEN}Related Sources:{Style.RESET_ALL}
{online_sources}

{Fore.BLUE}Generated at {results['timestamp']}{Style.RESET_ALL}
"""