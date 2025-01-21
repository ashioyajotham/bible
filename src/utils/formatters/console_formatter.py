from colorama import init, Fore, Style
from typing import Dict, Any


init()

class ConsoleFormatter:
    def format_verse(self, verse_data: Dict) -> str:
        """Format verse display with colors and structure"""
        return (
            f"\n{Fore.CYAN}📖 Daily Verse{Style.RESET_ALL}\n"
            f"\n{Fore.GREEN}{verse_data['text']}{Style.RESET_ALL}\n"
            f"\n{Fore.YELLOW}— {verse_data['reference']} ({verse_data['translation']}){Style.RESET_ALL}\n"
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

    def format_search_results(self, search_data: Dict[str, Any]) -> str:
        if not search_data or 'results' not in search_data:
            return f"{Fore.RED}No search results available{Style.RESET_ALL}"

        output = [
            f"\n{Fore.CYAN}🔍 Biblical Search: {search_data['query']}{Style.RESET_ALL}\n"
        ]

        for idx, result in enumerate(search_data['results'], 1):
            output.extend([
                f"\n{Fore.GREEN}{idx}. {result.get('title', 'No title')}{Style.RESET_ALL}",
                f"{Fore.YELLOW}>{Style.RESET_ALL} {result.get('snippet', 'No description')}",
                f"{Fore.BLUE}{result.get('link', '')}{Style.RESET_ALL}\n"
            ])

        return "\n".join(output)

    def format_analysis(self, analysis: Dict[str, Any]) -> str:
        if not analysis or 'analysis' not in analysis:
            return f"{Fore.RED}No analysis available{Style.RESET_ALL}"

        return (
            f"\n{Fore.CYAN}📚 Biblical Analysis{Style.RESET_ALL}\n\n"
            f"{Fore.YELLOW}Passage:{Style.RESET_ALL}\n{analysis['passage']}\n\n"
            f"{Fore.GREEN}Analysis:{Style.RESET_ALL}\n{analysis['analysis']}\n\n"
            f"{Fore.BLUE}Generated using {analysis['model_used']} "
            f"at {analysis['timestamp']}{Style.RESET_ALL}\n"
        )