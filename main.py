import os
import argparse
import sys
import logging
from rich.console import Console

from typing import Optional

# Set TensorFlow logging before any imports
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from datetime import datetime
from agent.bible_agent import BibleAgent
from utils.helpers import setup_logging, create_export_filename

def get_command_map():
    return {
        'teach': {'t'},  # Primary teaching command
        'verse': {'v', 'daily'},
        'reflect': {'r', 'meditate'},
        'export': {'e', 'save'},
        'help': {'h', '?'},
        'exit': {'q', 'quit', 'bye'}
    }

def show_help():
    """Display available commands"""
    commands = {
        'teach (t)': 'Get biblical teaching and analysis',
        'verse (v)': 'Get daily verse with devotional',
        'reflect (r)': 'Reflect on recent study',
        'export (e)': 'Export study session',
        'help (h)': 'Show this help message',
        'exit (q)': 'Exit application'
    }
    return commands

def resolve_command(input_cmd: str) -> Optional[str]:
    """Resolve command aliases to main command"""
    cmd_map = get_command_map()
    input_cmd = input_cmd.lower().strip()
    
    # Direct command match
    if input_cmd in cmd_map:
        return input_cmd
        
    # Check aliases
    for main_cmd, aliases in cmd_map.items():
        if input_cmd in aliases:
            return main_cmd
            
    return None

def main():
    """Main entry point with enhanced error handling"""
    console = Console()
    
    # Add command-line flag to control verbosity
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging with debug output")
    args, unknown = parser.parse_known_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)
    
    if not args.verbose:
        console.print("[bold yellow]Running in delightful mode. For deeper insights, try '--verbose'.[/bold yellow]")
        console.rule("[bold blue]Welcome to Biblia - Your Spiritual Companion[/bold blue]")
    else:
        console.print("[bold magenta]Verbose mode enabled. Brace for the deep technical insight![/bold magenta]")
    
    try:
        agent = BibleAgent()
        if not agent._models:
            raise Exception("Model system failed to initialize")
            
        # Show the welcome message with creative styling
        print(agent.console_formatter.format_welcome())
        
        while True:
            try:
                command = input("\nEnter command (h for help): ").strip()
                resolved_cmd = resolve_command(command)
                
                if resolved_cmd:
                    result = agent.process_command(resolved_cmd)
                    if result is None:
                        console.print("[bold red]Command failed. Please check the logs and try again.[/bold red]")
                else:
                    console.print("[bold red]Unknown command. Type 'h' for help.[/bold red]")
            except KeyboardInterrupt:
                console.print("\n\n[bold green]👋 Goodbye! God bless your spiritual journey.[/bold green]")
                sys.exit(0)
    except KeyboardInterrupt:
        console.print("\n\n[bold green]👋 Goodbye! God bless your spiritual journey.[/bold green]")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        print(f"Critical error: {str(e)}")
        raise

def handle_interactive_mode():
    """Handle interactive mode with full command set"""
    console = Console()
    try:
        agent = BibleAgent()
        
        commands = {
            'teach (t)': 'Get biblical teaching and analysis',
            'verse (v)': 'Get daily verse with devotional',
            'reflect (r)': 'Reflect on recent study',
            'analyze (a)': 'Analyze biblical passage',
            'export (e)': 'Export study session',
            'help (h)': 'Show this help message',
            'quit (q)': 'Exit application'
        }
        
        print(agent.console_formatter.format_welcome(commands))
        
        while True:
            try:
                command = input("\nEnter command (h for help): ").strip().lower()
                agent.process_command(command)
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                console.print("\n\n[bold green]👋 Goodbye! God bless your spiritual journey.[/bold green]")
                sys.exit(0)
            
    except KeyboardInterrupt:
        console.print("\n\n[bold green]👋 Goodbye! God bless your spiritual journey.[/bold green]")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        raise

def handle_command(command: str, agent: BibleAgent) -> None:
    try:
        if command == "search":
            query = input("Enter search query: ")
            results = agent.search_with_analysis(query)
            
        elif command == "reflect":
            topic = input("Enter topic for reflection: ")
            reflection = agent.generate_reflection(topic)
            
        elif command == "analyze":
            passage = input("Enter biblical passage: ")
            analysis = agent.analyze_passage(passage)
            
    except Exception as e:
        logging.error(f"Error processing command {command}: {str(e)}")

if __name__ == '__main__':
    main()