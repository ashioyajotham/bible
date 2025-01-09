# Scripture AI Agent

An autonomous AI agent for biblical study and research, powered by multiple LLMs and equipped with self-learning capabilities.

## Agent Architecture

This system implements a true autonomous agent with:

- **Self-Directed Goals**: Dynamically adjusts objectives based on context
- **Memory Systems**: Short-term and long-term memory for learning
- **Planning Module**: Strategic action planning with fallback mechanisms
- **Learning Component**: Adapts strategies based on experience
- **Tool Integration**: Dynamic selection of LLMs and search capabilities
- **State Management**: Tracks agent state and confidence levels
- **Reflection System**: Continuous self-evaluation and improvement

### Core Components

```mermaid
graph TD
    A[User Input] --> B[Agent Core]
    B --> C[Goal System]
    B --> D[Memory System]
    B --> E[Planning Module]
    B --> F[Learning System]
    C --> G[Tool Selection]
    G --> H[LLM Models]
    G --> I[Search Tools]

## Overview
The Scripture AI Agent is a Python-based application designed to provide users with daily Bible verses, teachings of Jesus Christ, and insightful summaries from online sources. The agent leverages the capabilities of GPT-4 and the Serper API to enhance user experience and deliver relevant content.

## Features
- **Daily Verses**: Fetches and displays daily Bible verses.
- **Teachings of Jesus**: Provides insights into the teachings of Jesus Christ.
- **Online Insights**: Searches for additional insights and summaries from the web.
- **GPT-4 Integration**: Utilizes GPT-4 for generating responses and enhancing user interaction.

## Project Structure
```
scripture-ai-agent/
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── bible_agent.py
│   │   └── search_agent.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── serper_service.py
│   │   └── llm/
│   │       ├── __init__.py
│   │       ├── base_llm.py
│   │       ├── gemini_llm.py
│   │       └── hf_llm.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── verse.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── requirements.txt
├── setup.py
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/ashioyajotham/bible.git

   ```
2. Navigate to the project directory:
   ```
   cd bible
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py

# Interactive Mode
python src/main.py --interactive

# Get Daily Verse
python src/main.py --verse

# Search Biblical Insights
python src/main.py --search "faith"

Arguments:
  --interactive, -i  Run the agent in interactive mode
  --verse, -v        Get the daily Bible verse
  --search, -s       Search for biblical insights
```
Alternatively, you can use the agent in your Python code:

```python
from bible import BibleAgent

agent = BibleAgent()

# Get daily verse with reflection
verse = agent.get_daily_verse()
reflection = agent.generate_reflection(verse)

# Search biblical insights
insights = agent.search_biblical_insights("faith and works")

# Interactive mode
agent.start_interactive_session()
```

## Configuration
- Update the `.env` file with your API keys and other sensitive information.
- Modify `config/settings.py` for any additional configuration settings.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
