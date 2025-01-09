import argparse
import sys
import logging
from datetime import datetime
from agent.bible_agent import BibleAgent
from utils.helpers import setup_logging, create_export_filename

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Bible Study AI Agent")
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    parser.add_argument('--verse', action='store_true', help='Get daily verse')
    args = parser.parse_args()
    
    try:
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
            elif command == 'verse':
                verse = agent.get_daily_verse()
                print(f"\nDaily Verse:\n{verse}")
            elif command == 'teach':
                topic = input("Enter topic: ")
                teachings = agent.get_teachings(topic)
                print(f"\nTeachings about {topic}:\n{teachings}")
            elif command == 'search':
                query = input("Enter search query: ")
                insights = agent.search_biblical_insights(query)
                print(f"\nInsights for {query}:\n{insights}")
            elif command == 'export':
                filename = create_export_filename("scripture_study")
                print(f"Export functionality to be implemented: {filename}")
            else:
                print("Unknown command. Available commands: verse, teach, search, export, quit")
                
        except Exception as e:
            logging.error(f"Error processing command {command}: {str(e)}")
            print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()