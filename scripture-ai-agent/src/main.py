# src/main.py

from agent.bible_agent import BibleAgent
from agent.search_agent import SearchAgent
from services.gpt_service import GptService
from services.serper_service import SerperService

def main():
    bible_agent = BibleAgent()
    search_agent = SearchAgent()
    gpt_service = GptService()
    serper_service = SerperService()

    while True:
        # Example of processing requests
        daily_verse = bible_agent.get_daily_verse()
        teachings = bible_agent.get_teachings()
        insights = search_agent.search_insights("latest teachings")
        summary = search_agent.get_summary(insights)

        # Here you would typically handle the output or further processing
        print(daily_verse)
        print(teachings)
        print(summary)

if __name__ == "__main__":
    main()