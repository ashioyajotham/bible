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
            handle_interactive_mode(agent)
        elif args.verse:
            verse = agent.get_daily_verse()
            print(verse)
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        sys.exit(1)

def handle_interactive_mode(agent: BibleAgent):
    """Handle interactive mode with command processing"""
    print("\nBible Study AI Agent - Interactive Mode")
    print("Commands: verse, teach, search, export, quit")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'export':
                filename = input("Enter filename (optional): ").strip()
                agent.export_study_session(filename if filename else None)
            elif command == 'teach':
                topic = input("Enter topic: ")
                agent.get_teachings(topic)  # Don't print return value
            elif command == 'verse':
                agent.get_daily_verse()  # Don't print return value
            elif command == 'search':
                query = input("Enter search query: ")
                agent.search_biblical_insights(query)  # Don't print return value
            else:
                handle_command(command, agent)
                
        except Exception as e:
            logging.error(f"Error processing command {command}: {str(e)}")
            print(f"Error: {str(e)}")

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