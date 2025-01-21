import os
import argparse
import sys
import logging

# Set TensorFlow logging before any imports
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from datetime import datetime
from agent.bible_agent import BibleAgent
from utils.helpers import setup_logging, create_export_filename

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
                print("Unknown command. Available commands: verse, teach, search, quit")
                
        except Exception as e:
            logging.error(f"Error processing command {command}: {str(e)}")
            print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()