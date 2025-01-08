# README.md

# Scripture AI Agent

## Overview
The Scripture AI Agent is a Python-based application designed to provide users with daily Bible verses, teachings of Jesus Christ, and insightful summaries from online sources. The agent leverages the capabilities of GPT-4 and the Serper API to enhance user experience and deliver relevant content.

## Features
- **Daily Verses**: Fetches and displays daily Bible verses.
- **Teachings of Jesus**: Provides insights into the teachings of Jesus Christ.
- **Online Insights**: Searches for additional insights and summaries from the web.
- **GPT-4 Integration**: Utilizes GPT-4 for generating responses and enhancing user interaction.

## Project Structure
```
scripture-ai-agent
├── src
│   ├── main.py
│   ├── agent
│   │   ├── __init__.py
│   │   ├── bible_agent.py
│   │   └── search_agent.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── gpt_service.py
│   │   └── serper_service.py
│   ├── models
│   │   ├── __init__.py
│   │   └── verse.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── config
│   └── settings.py
├── requirements.txt
├── .env
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd scripture-ai-agent
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Configuration
- Update the `.env` file with your API keys and other sensitive information.
- Modify `config/settings.py` for any additional configuration settings.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.