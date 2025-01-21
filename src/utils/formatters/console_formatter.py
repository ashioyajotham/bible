from colorama import init, Fore, Style, Back
from typing import Dict, Any
import textwrap

init()

class ConsoleFormatter:
    def format_verse(self, verse_data: Dict) -> str:
        """Format verse display with colors and structure"""
        return (
            f"\n{Fore.CYAN}📖 Daily Verse{Style.RESET_ALL}\n"
            f"\n{Fore.GREEN}{verse_data['text']}{Style.RESET_ALL}\n"
            f"\n{Fore.YELLOW}— {verse_data['reference']} ({verse_data['translation']}){Style.RESET_ALL}\n"
        )

    def format_teaching(self, teaching_data: Dict) -> str:
        # Create styled header
        header = f"""
{Fore.CYAN}╔{'═' * 60}╗
║{' ' * 24}BIBLICAL TEACHING{' ' * 23}║
╚{'═' * 60}╝{Style.RESET_ALL}"""

        # Format topic
        topic = f"\n{Fore.YELLOW}📚 Topic: {teaching_data['topic'].upper()}{Style.RESET_ALL}\n"

        # Process and format content with proper wrapping
        content = teaching_data['teaching']
        wrapped_content = []
        
        # Split content into paragraphs
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            # Wrap text to 70 characters
            wrapped = textwrap.fill(para.strip(), width=70)
            # Add proper indentation and styling
            wrapped = f"{Fore.WHITE}{wrapped}{Style.RESET_ALL}"
            wrapped_content.append(wrapped)

        # Join paragraphs with decorative separators
        separator = f"\n{Fore.BLUE}• ─────────────────────── •{Style.RESET_ALL}\n"
        formatted_content = separator.join(wrapped_content)

        # Add footer with metadata
        footer = f"""
{Fore.CYAN}╔{'═' * 60}╗
║{' ' * 15}Generated using {teaching_data['model_used']}{' ' * 15}║
╚{'═' * 60}╝{Style.RESET_ALL}"""

        # Combine all elements
        return f"{header}{topic}\n{formatted_content}\n{footer}"

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