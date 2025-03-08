from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.box import Box, ROUNDED, HEAVY, DOUBLE
from rich.markdown import Markdown
from rich.align import Align
from rich.layout import Layout
from typing import Dict, Any, List
import textwrap
from datetime import datetime

class ConsoleFormatter:
    def __init__(self):
        self.console = Console()
        self.ascii_title = """
  ____  _ _     _        _____ _             _         _         _     _              _   
 |  _ \(_) |__ | | ___  / ____| |_ _   _  __| |_   _  / \   __ _(_)___| |_ __ _ _ __ | |_ 
 | |_) | | '_ \| |/ _ \ \___ \| __| | | |/ _` | | | |/ _ \ / _` | / __| __/ _` | '_ \| __|
 |  _ <| | |_) | |  __/  ___) | |_| |_| | (_| | |_| / ___ \ (_| | \__ \ || (_| | | | | |_ 
 |_| \_\_|_.__/|_|\___| |____/ \__|\__,_|\__,_|\__, /_/   \_\__, |_|___/\__\__,_|_| |_|\__|
                                               |___/        |___/                         
 """
        
    def _create_header(self, title: str) -> Panel:
        """Create standardized header panel"""
        return Panel(
            Text(title, style="bold cyan", justify="center"),
            box=DOUBLE,
            border_style="cyan",
            expand=True
        )

    def _create_section_title(self, title: str, icon: str) -> Panel:
        """Create standardized section title"""
        return Panel(
            Text(f"{icon} {title.upper()}", style="white on blue"),
            box=ROUNDED,
            border_style="yellow",
            padding=(0, 2),
            expand=True
        )

    def format_teaching(self, data: Dict) -> str:
        """Format biblical teaching with enhanced styling"""
        # Capture rich output as string
        with self.console.capture() as capture:
            self.console.print(self._create_header("BIBLICAL TEACHING"))
            self.console.print(self._create_section_title(data['query'], "📚"))
            
            # Key Insights
            self.console.print(Panel(
                Text(data['insights'], style="green"),
                title="🔍 Key Insights",
                title_align="left",
                box=ROUNDED,
                border_style="magenta",
                padding=(1, 2),
                expand=True
            ))
            
            # Scripture References
            if references := data.get('references', []):
                refs_table = Table(box=Box.ROUNDED, show_header=False, expand=True, border_style="blue")
                refs_table.add_column("References")
                for ref in references:
                    refs_table.add_row(f"• {ref}")
                self.console.print(Panel(
                    refs_table,
                    title="📖 Scripture References",
                    title_align="left",
                    box=ROUNDED,
                    border_style="blue",
                    padding=(1, 2),
                    expand=True
                ))
            
            # Application
            if application := data.get('application', ''):
                self.console.print(Panel(
                    Text(application, style="yellow"),
                    title="💡 Application",
                    title_align="left",
                    box=ROUNDED,
                    border_style="yellow",
                    padding=(1, 2),
                    expand=True
                ))
            
            # Prayer Focus
            if prayer := data.get('prayer', ''):
                self.console.print(Panel(
                    Text(prayer, style="cyan"),
                    title="🙏 Prayer Focus",
                    title_align="left",
                    box=ROUNDED,
                    border_style="cyan",
                    padding=(1, 2),
                    expand=True
                ))
            
            # Sources
            if sources := data.get('sources', []):
                sources_table = Table(box=Box.ROUNDED, expand=True, border_style="dim white")
                sources_table.add_column("Title", style="cyan")
                sources_table.add_column("Link", style="blue underline")
                
                for source in sources:
                    sources_table.add_row(
                        textwrap.shorten(source.get('title', 'N/A'), width=40),
                        source.get('link', 'N/A')
                    )
                
                self.console.print(Panel(
                    sources_table,
                    title="📚 Sources",
                    title_align="left",
                    box=ROUNDED,
                    border_style="dim white",
                    padding=(1, 2),
                    expand=True
                ))
            
            # Footer
            timestamp = datetime.fromisoformat(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            self.console.print(Panel(
                Text(f"Generated at {timestamp}", style="dim", justify="center"),
                box=DOUBLE,
                border_style="cyan",
                expand=True
            ))
            
        return capture.get()

    def format_verse(self, data: Dict) -> str:
        """Format verse with devotional"""
        with self.console.capture() as capture:
            self.console.print(self._create_header("DAILY VERSE & DEVOTIONAL"))
            self.console.print(self._create_section_title(data['reference'], "📖"))
            
            # Verse text
            self.console.print(Panel(
                Text(data['text'], style="green italic"),
                border_style="green",
                box=ROUNDED,
                padding=(1, 2),
                expand=True
            ))
            
            # Translation & reference footer
            self.console.print(Text(
                f"— {data['reference']} ({data['translation']})",
                style="blue",
                justify="right"
            ))
            
            # Devotional
            if devotional := data.get('devotional', ''):
                self.console.print(Panel(
                    Markdown(devotional),
                    title="🙏 Daily Devotional",
                    title_align="left",
                    border_style="cyan",
                    box=ROUNDED,
                    padding=(1, 2),
                    expand=True
                ))
            
        return capture.get()

    def format_reflection(self, data: Dict) -> str:
        """Format reflection with context awareness"""
        with self.console.capture() as capture:
            self.console.print(self._create_header("SPIRITUAL REFLECTION"))
            self.console.print(self._create_section_title(f"Reflecting on: {data['context_type']}", "💭"))
            
            # Insights
            self.console.print(Panel(
                Text(data['insights'], style="green"),
                title="🤔 Insights",
                title_align="left",
                border_style="magenta",
                box=ROUNDED,
                padding=(1, 2),
                expand=True
            ))
            
            # Application
            self.console.print(Panel(
                Text(data['application'], style="yellow"),
                title="🔄 Personal Application",
                title_align="left",
                border_style="yellow",
                box=ROUNDED,
                padding=(1, 2),
                expand=True
            ))
            
            # Prayer Focus
            self.console.print(Panel(
                Text(data['prayer'], style="cyan"),
                title="🙏 Prayer Focus",
                title_align="left",
                border_style="cyan",
                box=ROUNDED,
                padding=(1, 2),
                expand=True
            ))
            
            # Footer
            self.console.print(Panel(
                Text("May these insights deepen your faith journey", style="italic", justify="center"),
                box=DOUBLE,
                border_style="cyan",
                expand=True
            ))
            
        return capture.get()

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

        with self.console.capture() as capture:
            # ASCII art title with gradient color
            title_text = Text(self.ascii_title)
            title_text.stylize("bold cyan")
            self.console.print(title_text)
            
            self.console.print(Panel(
                Text("BIBLE STUDY ASSISTANT", style="white on blue", justify="center"),
                box=DOUBLE,
                border_style="cyan",
                expand=True
            ))
            
            # Commands table
            command_table = Table(box=ROUNDED, expand=True, show_header=False)
            command_table.add_column("Command", style="yellow bold")
            command_table.add_column("Description")
            
            for cmd, desc in commands.items():
                command_table.add_row(cmd, desc)
            
            self.console.print(Panel(
                command_table,
                title="Available Commands",
                title_align="left",
                border_style="green",
                box=ROUNDED,
                padding=(1, 2),
                expand=True
            ))
            
            self.console.print(Text("\n🙏 Begin your spiritual journey with any command above...", style="italic cyan"))
            
        return capture.get()

    def format_export_success(self, filepath: str) -> str:
        """Format export success message"""
        with self.console.capture() as capture:
            self.console.print(self._create_header("EXPORT SUCCESS"))
            
            layout = Layout()
            layout.split(
                Layout(name="upper"),
                Layout(name="lower")
            )
            
            layout["upper"].update(Panel(
                Text("✅ Study session exported successfully!", style="bold green", justify="center"),
                box=ROUNDED,
                border_style="green",
                padding=(1, 2)
            ))
            
            layout["lower"].update(Panel(
                Text(f"📁 Location: {filepath}\n\nOpen the file to view your study session in Markdown format.",
                     justify="left"),
                box=ROUNDED,
                border_style="blue",
                padding=(1, 2)
            ))
            
            self.console.print(layout)
            
        return capture.get()

    def format_search_results(self, results: Dict[str, Any]) -> str:
        """Format search results with enhanced styling"""
        with self.console.capture() as capture:
            self.console.print(self._create_header("BIBLICAL SEARCH RESULTS"))
            self.console.print(self._create_section_title(f"Query: {results['query']}", "🔍"))
            
            # Insights
            self.console.print(Panel(
                Markdown(results['insights']),
                title="📝 Theological Insights",
                title_align="left",
                border_style="magenta",
                box=ROUNDED,
                padding=(1, 2),
                expand=True
            ))
            
            # Sources
            if sources := results.get('sources', []):
                sources_table = Table(box=ROUNDED, expand=True)
                sources_table.add_column("Title", style="cyan")
                sources_table.add_column("Source", style="blue")
                
                for source in sources:
                    sources_table.add_row(
                        textwrap.shorten(source.get('title', 'N/A'), width=40),
                        textwrap.shorten(source.get('link', 'N/A'), width=50)
                    )
                
                self.console.print(Panel(
                    sources_table,
                    title="📚 Reference Sources",
                    title_align="left",
                    border_style="blue",
                    box=ROUNDED,
                    padding=(1, 2),
                    expand=True
                ))
                
        return capture.get()

    def format_analysis(self, data: Dict[str, Any]) -> str:
        """Format passage analysis"""
        with self.console.capture() as capture:
            self.console.print(self._create_header("BIBLICAL PASSAGE ANALYSIS"))
            
            # Passage
            passage_panel = Panel(
                Text(data['passage'], style="green italic"),
                title="📜 Passage",
                title_align="left",
                box=ROUNDED,
                border_style="green",
                padding=(1, 2),
                expand=True
            )
            self.console.print(passage_panel)
            
            # Analysis
            analysis_panel = Panel(
                Markdown(data['analysis']),
                title="🔍 Analysis",
                title_align="left",
                box=ROUNDED,
                border_style="magenta",
                padding=(1, 2),
                expand=True
            )
            self.console.print(analysis_panel)
            
        return capture.get()