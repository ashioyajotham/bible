from colorama import init, Fore, Style, Back
from typing import Dict, Any
import textwrap
from datetime import datetime

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

    def format_search_results(self, search_data: Dict) -> str:
        """Format search results with rich styling and longer snippets"""
        # Create styled header
        header = f"""
{Fore.CYAN}╔{'═' * 60}╗
║{' ' * 25}SEARCH RESULTS{' ' * 24}║
╚{'═' * 60}╝{Style.RESET_ALL}"""

        # Format query
        query = f"\n{Fore.YELLOW}🔍 Query: {search_data['query'].upper()}{Style.RESET_ALL}\n"

        # Process results
        results = []
        for idx, result in enumerate(search_data['results'], 1):
            # Format each result with more detailed content
            result_block = f"""
{Fore.GREEN}Result #{idx}{Style.RESET_ALL}
{Fore.BLUE}{'─' * 60}{Style.RESET_ALL}
{Fore.CYAN}Title:{Style.RESET_ALL} {result.get('title', 'No title')}

{Fore.CYAN}Summary:{Style.RESET_ALL}
{textwrap.fill(result.get('snippet', 'No description'), width=70)}

{Fore.CYAN}Key Points:{Style.RESET_ALL}
{textwrap.fill(result.get('description', result.get('snippet', '')), width=70)}

{Fore.BLUE}Source:{Style.RESET_ALL} {result.get('link', 'No link available')}
"""
            results.append(result_block)

        # Join results with decorative separator
        separator = f"\n{Fore.BLUE}• {'═' * 58} •{Style.RESET_ALL}\n"
        formatted_results = separator.join(results)

        # Add footer with timestamp
        footer = f"""
{Fore.CYAN}╔{'═' * 60}╗
║{' ' * 15}Search completed at {datetime.now().strftime('%H:%M:%S')}{' ' * 15}║
╚{'═' * 60}╝{Style.RESET_ALL}"""

        return f"{header}{query}\n{formatted_results}\n{footer}"

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