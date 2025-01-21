from colorama import init, Fore, Style, Back
from typing import Dict, Any, List
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
        """Format biblical teaching with rich styling"""
        # Create fancy header with double borders
        header = f"""
{Fore.CYAN}╔{'═' * 70}╗
║ {'BIBLICAL TEACHINGS'.center(68)} ║
╚{'═' * 70}╝{Style.RESET_ALL}"""

        # Format topic with emoji and highlighting
        topic = f"""\n{Fore.YELLOW}┌{'─' * 68}┐
│ {Back.BLUE}{Fore.WHITE} 📚 Topic: {teaching_data['topic'].upper()} {Style.RESET_ALL}{Fore.YELLOW}
└{'─' * 68}┘{Style.RESET_ALL}\n"""

        # Process content into sections
        content_parts = teaching_data['teaching'].split('\n\n')
        formatted_content = []
        
        for part in content_parts:
            # Format each paragraph with proper wrapping and styling
            wrapped = textwrap.fill(part.strip(), width=65)
            # Add subtle left border for content
            wrapped = '\n'.join(f"{Fore.BLUE}│{Style.RESET_ALL} {line}" 
                              for line in wrapped.split('\n'))
            formatted_content.append(wrapped)

        # Join with decorative separators
        separator = f"\n{Fore.CYAN}├{'─' * 68}┤{Style.RESET_ALL}\n"
        content = separator.join(formatted_content)

        # Add styled footer
        footer = f"""
{Fore.CYAN}╔{'═' * 70}╗
║ {f'Generated by {teaching_data["model_used"]}'.center(68)} ║
╚{'═' * 70}╝{Style.RESET_ALL}
"""

        return f"{header}{topic}\n{content}\n{footer}"

    def format_search_results(self, data: Dict) -> str:
        """Format complete search results"""
        # ...existing formatting code...
        # Updated to match new data structure

    def _format_sources(self, sources: List[Dict]) -> str:
        """Format source references"""
        return "\n\n".join(
            f"Source {i+1}:\n"
            f"Title: {source.get('title', 'N/A')}\n"
            f"Link: {source.get('link', 'N/A')}"
            for i, source in enumerate(sources)
        )

    def format_reflection(self, reflection_data: Dict) -> str:
        """Format spiritual reflection"""
        header = self._create_header("SPIRITUAL REFLECTION")
        
        content = (
            f"{Fore.YELLOW}💭 Personal Application{Style.RESET_ALL}\n"
            f"{textwrap.fill(reflection_data['application'], width=70)}\n\n"
            f"{Fore.YELLOW}🙏 Prayer Points{Style.RESET_ALL}\n"
            f"{textwrap.fill(reflection_data['prayer_points'], width=70)}\n\n"
            f"{Fore.YELLOW}📖 Meditation Verses{Style.RESET_ALL}\n"
            f"{textwrap.fill(reflection_data['meditation_verses'], width=70)}"
        )
        
        footer = self._create_footer("May these insights guide your walk")
        return f"{header}\n\n{content}\n\n{footer}"

    def format_analysis(self, analysis_data: Dict) -> str:
        """Format passage analysis with rich styling"""
        header = f"""
{Fore.CYAN}╔{'═' * 60}╗
║{' ' * 24}PASSAGE ANALYSIS{' ' * 23}║
╚{'═' * 60}╝{Style.RESET_ALL}"""

        passage = f"\n{Fore.YELLOW}📜 Passage: {analysis_data['passage']}{Style.RESET_ALL}\n"
        
        content = textwrap.fill(analysis_data['analysis'], width=70)
        
        footer = f"""
{Fore.CYAN}╔{'═' * 60}╗
║{' ' * 15}Analyzed using {analysis_data['model_used']}{' ' * 15}║
╚{'═' * 60}╝{Style.RESET_ALL}"""

        return f"{header}{passage}\n{content}\n{footer}"

    def format_export_success(self, filepath: str) -> str:
        """Format export success message"""
        return f"""
{Fore.CYAN}╔{'═' * 60}╗
║{' ' * 26}EXPORT SUCCESS{' ' * 22}║
╚{'═' * 60}╝{Style.RESET_ALL}

{Fore.GREEN}✅ Study session exported successfully!{Style.RESET_ALL}

{Fore.YELLOW}📁 Location:{Style.RESET_ALL} {filepath}

{Fore.BLUE}Open the file to view your study session in Markdown format.{Style.RESET_ALL}"""

    def format_help(self) -> str:
        """Format help message with commands and shortcuts"""
        commands = {
            'search (s)': 'Search biblical content and get analysis',
            'teach (t)': 'Get biblical teaching on a topic',
            'verse (v)': 'Get daily verse with reflection',
            'reflect (r)': 'Reflect on recent search/study',
            'export (e)': 'Export study session',
            'help (h)': 'Show this help message',
            'exit (q)': 'Exit the application'
        }
        
        header = f"""
{Fore.CYAN}╔{'═' * 70}╗
║ {'AVAILABLE COMMANDS'.center(68)} ║
╚{'═' * 70}╝{Style.RESET_ALL}"""

        content = []
        for cmd, desc in commands.items():
            content.append(f"{Fore.YELLOW}{cmd:<15}{Style.RESET_ALL} - {desc}")

        return f"{header}\n\n" + "\n".join(content)

    def format_welcome(self, commands: Dict[str, str]) -> str:
        """Format welcome message with all commands"""
        header = f"""
{Fore.CYAN}╔{'═' * 70}╗
║ {'BIBLE STUDY ASSISTANT'.center(68)} ║
╚{'═' * 70}╝{Style.RESET_ALL}"""

        command_list = "\n".join(
            f"{Fore.YELLOW}{cmd:<15}{Style.RESET_ALL} - {desc}"
            for cmd, desc in commands.items()
        )
        
        return f"{header}\n\nAvailable Commands:\n{command_list}"