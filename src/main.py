import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import logging
from dotenv import load_dotenv

from agent.bible_agent import BibleAgent
from agent.search_agent import SearchAgent
from utils.helpers import setup_logging, create_export_filename
from config.settings import Config

def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scripture AI Agent CLI")
    parser.add_argument('--verse', help='Get daily verse')
    parser.add_argument('--teach', help='Get teachings about topic')
    parser.add_argument('--search', help='Search biblical insights')
    parser.add_argument('--export', help='Export results to file')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    return parser

def handle_interactive_mode(bible_agent: BibleAgent, search_agent: SearchAgent):
    print("\nScripture AI Agent Interactive Mode")
    print("Commands: verse, teach, search, export, quit")
    
    while True:
        command = input("\nEnter command: ").strip().lower()
        
        try:
            if command == 'quit':
                break
            elif command == 'verse':
                verse = bible_agent.get_daily_verse()
                print(f"\nDaily Verse:\n{verse}")
            elif command == 'teach':
                topic = input("Enter topic: ")
                teachings = bible_agent.get_teachings(topic)
                print(f"\nTeachings about {topic}:\n{teachings}")
            elif command == 'search':
                query = input("Enter search query: ")
                insights = search_agent.search_insights(query)
                print(f"\nInsights for {query}:\n{insights}")
            elif command == 'export':
                filename = create_export_filename("scripture_study")
                # Implementation for export functionality
        except Exception as e:
            logging.error(f"Error processing command {command}: {str(e)}")
            print(f"Error: {str(e)}")

def main():
    # Setup
    load_dotenv()
    setup_logging()
    parser = setup_args()
    args = parser.parse_args()

    try:
        bible_agent = BibleAgent()
        search_agent = SearchAgent()

        if args.interactive:
            handle_interactive_mode(bible_agent, search_agent)
        else:
            if args.verse:
                verse = bible_agent.get_daily_verse()
                print(verse)
            
            if args.teach:
                teachings = bible_agent.get_teachings(args.teach)
                print(teachings)
                
            if args.search:
                insights = search_agent.search_insights(args.search)
                print(insights)
                
            if args.export:
                # Implementation for export functionality
                pass

    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()