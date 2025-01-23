import pytest
from datetime import datetime
from src.agent.bible_agent import BibleAgent
from src.models.verse import Verse
from src.utils.formatters.console_formatter import ConsoleFormatter

@pytest.fixture
def bible_agent():
    return BibleAgent()

@pytest.fixture
def sample_teaching_data():
    return {
        "query": "love",
        "insights": "Biblical insights about love...",
        "references": ["John 3:16", "1 Corinthians 13:4-7"],
        "application": "How to apply love...",
        "prayer": "Prayer points about love...",
        "sources": [{"title": "Source 1", "link": "http://example.com"}],
        "timestamp": datetime.now().isoformat()
    }

class TestBibleAgent:
    def test_initialization(self, bible_agent):
        """Test agent initialization"""
        assert hasattr(bible_agent, 'model_manager')
        assert hasattr(bible_agent, 'console_formatter')
        assert hasattr(bible_agent, 'current_session')
        assert hasattr(bible_agent, 'search_agent')

    def test_process_teach_command(self, bible_agent, monkeypatch):
        """Test teaching command processing"""
        # Mock user input
        monkeypatch.setattr('builtins.input', lambda _: "forgiveness")
        
        # Mock search agent
        def mock_search(*args):
            return {
                "insights": "Test insights",
                "sources": []
            }
        monkeypatch.setattr(bible_agent.search_agent, 'search_and_analyze', mock_search)
        
        result = bible_agent.process_command("teach")
        assert result is not None
        assert "query" in result
        assert result["query"] == "forgiveness"

    def test_process_verse_command(self, bible_agent, monkeypatch):
        """Test verse command processing"""
        # Mock verse fetching
        mock_verse = Verse(
            text="Test verse text",
            reference="John 3:16",
            translation="ESV",
            category="wisdom"
        )
        monkeypatch.setattr(bible_agent, 'get_daily_verse', lambda: mock_verse)
        
        result = bible_agent.process_command("verse")
        assert result is not None
        assert "text" in result
        assert "reference" in result
        assert "devotional" in result

    def test_process_reflect_command(self, bible_agent, sample_teaching_data):
        """Test reflection command processing"""
        # Add teaching to session
        bible_agent.current_session.add_teaching(sample_teaching_data)
        
        result = bible_agent.process_command("reflect")
        assert result is not None
        assert "context_type" in result
        assert "insights" in result
        assert "application" in result
        assert "prayer" in result

    def test_process_export_command(self, bible_agent, sample_teaching_data, tmp_path):
        """Test export command processing"""
        # Add content to session
        bible_agent.current_session.add_teaching(sample_teaching_data)
        
        # Set temporary export directory
        bible_agent.export_dir = tmp_path
        
        result = bible_agent.process_command("export")
        assert result is not None
        assert tmp_path.joinpath(result).exists()

    def test_error_handling(self, bible_agent):
        """Test error handling in command processing"""
        result = bible_agent.process_command("invalid_command")
        assert result is None

    def test_session_management(self, bible_agent, sample_teaching_data):
        """Test session management"""
        bible_agent.current_session.add_teaching(sample_teaching_data)
        assert len(bible_agent.current_session.teachings) == 1
        
        content = bible_agent.current_session.get_latest_content()
        assert content is not None
        assert content['type'] == 'teaching'
        