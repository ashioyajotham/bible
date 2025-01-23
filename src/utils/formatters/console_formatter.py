from colorama import init, Fore, Style, Back
from typing import Dict, Any, List
import textwrap
from datetime import datetime

init()

class ConsoleFormatter:
    def __init__(self):
        init()  # Initialize colorama
        
    def _create_header(self, title: str) -> str:
        """Create standardized header"""
        return f"""
{Fore.CYAN}╔{'═' * 70}╗
║ {title.center(68)} ║
╚{'═' * 70}╝{Style.RESET_ALL}"""

    def _create_section_title(self, title: str, icon: str) -> str:
        """Create standardized section title"""
        return f"""\n{Fore.YELLOW}┌{'─' * 68}┐
│ {Back.BLUE}{Fore.WHITE} {icon} {title.upper()} {Style.RESET_ALL}{Fore.YELLOW}
└{'─' * 68}┘{Style.RESET_ALL}\n"""

    def format_teaching(self, data: Dict) -> str:
        """Format biblical teaching with enhanced styling"""
        header = self._create_header("BIBLICAL TEACHING")
        topic = self._create_section_title(data['query'], "📚")
        
        sections = [
            ("🔍 Key Insights", data['insights']),
            ("📖 Scripture References", data.get('references', [])),
            ("💡 Application", data.get('application', '')),
            ("🙏 Prayer Focus", data.get('prayer', ''))
        ]
        
        content = self._format_sections(sections)
        sources = self._format_sources(data['sources'])
        footer = self._create_footer(f"Generated at {datetime.fromisoformat(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        return f"{header}{topic}{content}\n{sources}\n{footer}"

    def format_verse(self, data: Dict) -> str:
        """Format verse with devotional"""
        header = self._create_header("DAILY VERSE & DEVOTIONAL")
        verse_section = self._create_section_title(data['reference'], "📖")
        
        verse_text = f"{Fore.GREEN}{data['text']}{Style.RESET_ALL}"
        devotional = self._format_section("🙏 Daily Devotional", data['devotional'])
        footer = self._create_footer(f"Translation: {data['translation']}")
        
        return f"{header}{verse_section}{verse_text}\n{devotional}\n{footer}"

    def format_reflection(self, data: Dict) -> str:
        """Format reflection with context awareness"""
        header = self._create_header("SPIRITUAL REFLECTION")
        context = self._create_section_title(f"Reflecting on: {data['context_type']}", "💭")
        
        sections = [
            ("🤔 Insights", data['insights']),
            ("🔄 Personal Application", data['application']),
            ("🙏 Prayer Focus", data['prayer'])
        ]
        
        content = self._format_sections(sections)
        footer = self._create_footer("May these insights deepen your faith journey")
        
        return f"{header}{context}{content}\n{footer}"

    def format_welcome(self) -> str:
        """Format welcome message with all commands"""
        commands = {
            'teach (t)': 'Get biblical teaching and analysis',
            'verse (v)': 'Get daily verse with devotional',
            'reflect (r)': 'Reflect on recent study',
            'export (e)': 'Export study session',
            'help (h)': 'Show this help message',
            'exit (q)': 'Exit application'
        }

        header = self._create_header("BIBLE STUDY ASSISTANT")
        command_list = "\n".join(
            f"{Fore.YELLOW}{cmd:<15}{Style.RESET_ALL} - {desc}"
            for cmd, desc in commands.items()
        )
        
        return f"{header}\n\nAvailable Commands:\n{command_list}"

    def format_export_success(self, filepath: str) -> str:
        """Format export success message"""
        header = self._create_header("EXPORT SUCCESS")
        content = f"""
{Fore.GREEN}✅ Study session exported successfully!{Style.RESET_ALL}

{Fore.YELLOW}📁 Location:{Style.RESET_ALL} {filepath}

{Fore.BLUE}Open the file to view your study session in Markdown format.{Style.RESET_ALL}"""
        
        return f"{header}\n{content}"

    # Helper methods
    def _format_sections(self, sections: List[tuple]) -> str:
        """Format multiple content sections"""
        formatted = []
        for icon_title, content in sections:
            if content:  # Only include non-empty sections
                section = f"\n{Fore.MAGENTA}{icon_title}:{Style.RESET_ALL}\n"
                section += self._format_content_sections(content)
                formatted.append(section)
        return '\n'.join(formatted)

    def _format_content_sections(self, content: str) -> str:
        """Format content with borders and proper wrapping"""
        if isinstance(content, list):
            content = '\n'.join(f"• {item}" for item in content)
        
        parts = content.split('\n\n')
        formatted = []
        
        for part in parts:
            wrapped = textwrap.fill(part.strip(), width=65)
            bordered = '\n'.join(f"{Fore.GREEN}│{Style.RESET_ALL} {line}" 
                               for line in wrapped.split('\n'))
            formatted.append(bordered)

        return '\n\n'.join(formatted)

    def _format_sources(self, sources: List[Dict]) -> str:
        """Format source references with enhanced styling"""
        formatted_sources = []
        for i, source in enumerate(sources, 1):
            source_text = (
                f"{Fore.YELLOW}Source {i}:{Style.RESET_ALL}\n"
                f"{Fore.CYAN}Title:{Style.RESET_ALL} {source.get('title', 'N/A')}\n"
                f"{Fore.CYAN}Link: {Style.RESET_ALL}{source.get('link', 'N/A')}\n"
                f"{Fore.CYAN}Summary:{Style.RESET_ALL} {textwrap.fill(source.get('snippet', 'N/A'), width=65)}"
            )
            formatted_sources.append(source_text)
        
        return "\n\n".join(formatted_sources)

    def _format_section(self, title: str, content: str) -> str:
        """Format a single section with title and content"""
        section_title = f"\n{Fore.MAGENTA}{title}:{Style.RESET_ALL}\n"
        wrapped_content = textwrap.fill(content.strip(), width=65)
        bordered_content = '\n'.join(f"{Fore.GREEN}│{Style.RESET_ALL} {line}" 
                                   for line in wrapped_content.split('\n'))
        return f"{section_title}{bordered_content}"

    def _create_footer(self, text: str) -> str:
        """Create standardized footer"""
        return f"""
{Fore.CYAN}╔{'═' * 70}╗
║ {text.center(68)} ║
╚{'═' * 70}╝{Style.RESET_ALL}"""