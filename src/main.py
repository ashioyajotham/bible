import os
import argparse
import sys
import logging

from typing import Optional

# Set TensorFlow logging before any imports
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from datetime import datetime
from agent.bible_agent import BibleAgent
from utils.helpers import setup_logging, create_export_filename

def get_command_map():
    """Get mapping of commands and their shortcuts"""
    return {
        # Main commands and their shortcuts
        'search': {'s', 'find', 'lookup'},
        'teach': {'t', 'learn', 'study'},
        'verse': {'v', 'daily', 'dv'},
        'reflect': {'r', 'meditate', 'think'},
        'export': {'e', 'save', 'backup'},
        'help': {'h', '?'},
        'exit': {'q', 'quit', 'bye'}
    }

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
    parser = argparse.ArgumentParser(description="Bible Study AI Agent")
    
    # Interactive mode
    parser.add_argument('--interactive', '-i', 
                       action='store_true', 
                       help='Start interactive mode')
    
    # Daily verse
    parser.add_argument('--verse', '-v', 
                       action='store_true', 
                       help='Get daily verse')
    
    # Teachings
    parser.add_argument('--teach', '-t',
                          help='Get teachings on a topic')
    
    # Search
    parser.add_argument('--search', '-s',
                            help='Search for biblical insights')
    
    # Debug mode
    parser.add_argument('--debug', '-d', 
                       action='store_true', 
                       help='Enable debug logging')
    
    args = parser.parse_args()

    # Setup logging based on debug flag
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(level=log_level)
    
    try:
        logging.debug("Initializing Bible Agent")
        agent = BibleAgent()
        if args.interactive:
            handle_interactive_mode()
        elif args.verse:
            verse = agent.get_daily_verse()
            print(verse)
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        sys.exit(1)

def handle_interactive_mode():
    """Handle interactive mode with full command set"""
    try:
        agent = BibleAgent()
        
        commands = {
            'search (s)': 'Search and analyze biblical topics',
            'teach (t)': 'Get biblical teaching on a topic',
            'verse (v)': 'Get daily verse with reflection',
            'reflect (r)': 'Reflect on recent study',
            'analyze (a)': 'Analyze biblical passage',
            'export (e)': 'Export study session',
            'help (h)': 'Show this help message',
            'quit (q)': 'Exit application'
        }
        
        print(agent.console_formatter.format_welcome(commands))
        
        while True:
            command = input("\nEnter command (h for help): ").strip().lower()
            agent.process_command(command)
            
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