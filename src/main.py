import argparse
import sys
import logging
from datetime import datetime
from agent.bible_agent import BibleAgent
from utils.helpers import setup_logging, create_export_filename

def main():
    parser = argparse.ArgumentParser(description="Bible Study AI Agent")
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    parser.add_argument('--verse', action='store_true', help='Get daily verse')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
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