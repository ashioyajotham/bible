# Bible Study AI Agent 🤖📚

An intelligent agent system for biblical study and analysis, combining modern AI with scriptural wisdom.

## 🌟 Key Features

- **Interactive Study Mode**: Engage in dynamic Bible study sessions with natural language interactions
- **Intelligent Search**: Advanced biblical search with theological analysis and cross-references
- **Daily Verses**: AI-curated daily verses with contextual insights
- **Spiritual Reflections**: Generate meaningful reflections on biblical passages
- **Teaching Generation**: Get in-depth teachings on biblical topics
- **Multi-Model Support**: Leverages both Google's Gemini and Hugging Face models
- **Export Capabilities**: Save study sessions in beautifully formatted Markdown
- **Smart Model Selection**: Automatic model selection based on task requirements

## 🏗️ Architecture

```mermaid
graph TB
    User([User]) --> CLI[Command Line Interface]
    CLI --> BA[Bible Agent]
    
    subgraph "Core Components"
        BA --> MS[Model Selector]
        BA --> SA[Search Agent]
        BA --> SS[Study Session]
        
        MS --> GM[Gemini Model]
        MS --> HF[HuggingFace Model]
        
        SA --> SP[Serper Service]
        SA --> MA[Model Analysis]
    end
    
    subgraph "Features"
        BA --> VS[Verse Service]
        BA --> TS[Teaching Service]
        BA --> RS[Reflection Service]
        BA --> AS[Analysis Service]
    end
    
    subgraph "Utils & Formatting"
        BA --> CF[Console Formatter]
        BA --> MF[Markdown Formatter]
        SS --> EX[Export System]
    end
```

## 🔧 Technical Components

- **Agent System**
  - `BibleAgent`: Core orchestrator for all functionalities
  - `SearchAgent`: Handles biblical search and analysis
  - `ModelSelector`: Smart model selection based on task
  
- **Models & Services**
  - Google Gemini Integration
  - HuggingFace Models Support
  - Serper API Integration
  - ESV Bible API Integration

- **Session Management**
  - Study Session Tracking
  - Progress Persistence
  - Export Capabilities

## 🚀 Getting Started

1. **Clone the repository**
```bash
git clone https://github.com/ashioyajotham/bible-study-ai.git
cd bible-study-ai
```

2. **Set up environment**
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

3. **Configure API keys**
Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_key
SERPER_API_KEY=your_serper_key
ESV_API_KEY=your_esv_key
HF_API_KEY=your_huggingface_key
```

4. **Run the application**
```bash
python src/main.py --interactive
```

## 💻 Usage Examples

### Interactive Mode
```bash
python src/main.py -i
```

### Get Daily Verse
```bash
python src/main.py --verse
```

### Search Biblical Topics
```bash
python src/main.py --search "love your neighbor"
```

### Generate Teaching
```bash
python src/main.py --teach "forgiveness"
```

## 🔍 Command Reference

- `search (s)`: Search and analyze biblical topics
- `teach (t)`: Get biblical teaching on a topic
- `verse (v)`: Get daily verse with reflection
- `reflect (r)`: Reflect on recent study
- `analyze (a)`: Analyze biblical passage
- `export (e)`: Export study session
- `help (h)`: Show help message
- `quit (q)`: Exit application

## 🛠️ Development

The project uses a modular architecture with clear separation of concerns:

- `src/agent/`: Core agent implementations
- `src/models/`: Data models and structures
- `src/services/`: External service integrations
- `src/utils/`: Helper utilities and formatters

## 📜 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## ⚠️ Note

This is an AI assistant tool meant to aid in Bible study, not replace traditional study methods or spiritual guidance.