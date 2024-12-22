from unittest.mock import AsyncMock, Mock, patch

import pytest
from click.testing import CliRunner

from insightvault.app.cli import cli
from insightvault.models.document import Document


class TestCLI:
    @pytest.fixture
    def runner(self):
        """Create a CLI runner"""
        return CliRunner()

    @pytest.fixture
    def mock_base_app(self):
        """Create a mock base app"""
        with patch("insightvault.app.cli.BaseApp") as mock:
            app_instance = mock.return_value
            app_instance.add_documents = Mock()
            app_instance.list_documents = Mock()
            app_instance.delete_all_documents = Mock()
            yield mock

    @pytest.fixture
    def mock_search_app(self):
        """Create a mock search app"""
        with patch("insightvault.app.cli.SearchApp") as mock:
            app_instance = mock.return_value
            app_instance.query = Mock(return_value=["Result 1", "Result 2"])
            yield mock

    @pytest.fixture
    def mock_rag_app(self):
        """Create a mock RAG app"""
        with patch("insightvault.app.cli.RAGApp") as mock:
            app_instance = mock.return_value
            app_instance.query = Mock(return_value="Generated chat response")
            yield mock

    @pytest.fixture
    def mock_summarizer_app(self):
        """Create a mock summarizer app"""
        with patch("insightvault.app.cli.SummarizerApp") as mock:
            app_instance = mock.return_value
            app_instance.summarize = Mock(return_value="Summarized text")
            yield mock

    def test_manage_add_file(self, runner, mock_base_app, tmp_path):
        """Test adding a file through CLI"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content")

        mock_base_app.return_value.init = AsyncMock()
        mock_base_app.return_value.add_documents = AsyncMock()

        result = runner.invoke(cli, ["manage", "add-file", str(test_file)])

        assert result.exit_code == 0
        mock_base_app.return_value.add_documents.assert_called_once()
        doc = mock_base_app.return_value.add_documents.call_args[0][0][0]
        assert doc.title == "test.txt"
        assert doc.content == "Test content"
        assert doc.metadata["source"] == str(test_file)

    def test_manage_add_text(self, runner, mock_base_app):
        """Test adding text through CLI"""
        mock_base_app.return_value.init = AsyncMock()
        mock_base_app.return_value.add_documents = AsyncMock()

        result = runner.invoke(cli, ["manage", "add-text", "Test content"])

        assert result.exit_code == 0
        mock_base_app.return_value.add_documents.assert_called_once()
        doc = mock_base_app.return_value.add_documents.call_args[0][0][0]
        assert doc.title == "Direct Input"
        assert doc.content == "Test content"
        assert doc.metadata["type"] == "direct_input"

    def test_manage_list_documents(self, runner, mock_base_app):
        """Test listing documents through CLI"""
        mock_base_app.return_value.list_documents.return_value = [
            Document(
                id="1",
                title="Doc 1",
                content="Content 1",
                metadata={"title": "Doc 1"},
            ),
            Document(
                id="2",
                title="Doc 2",
                content="Content 2",
                metadata={"title": "Doc 2"},
            ),
        ]

        result = runner.invoke(cli, ["manage", "list"])

        assert result.exit_code == 0
        assert "1. Doc 1 (ID: 1)" in result.output
        assert "2. Doc 2 (ID: 2)" in result.output

    def test_manage_list_documents_empty(self, runner, mock_base_app):
        """Test listing documents when none exist"""
        mock_base_app.return_value.list_documents.return_value = []

        result = runner.invoke(cli, ["manage", "list"])

        assert result.exit_code == 0
        assert "No documents found in database." in result.output

    def test_manage_delete_all(self, runner, mock_base_app):
        """Test deleting all documents through CLI"""
        result = runner.invoke(cli, ["manage", "delete-all"])

        assert result.exit_code == 0
        mock_base_app.return_value.delete_all_documents.assert_called_once()
        assert "All documents deleted" in result.output

    def test_search_query(self, runner, mock_search_app):
        """Test search query through CLI"""
        mock_search_app.return_value.init = AsyncMock()
        result = runner.invoke(cli, ["search", "test query"])

        assert result.exit_code == 0
        mock_search_app.return_value.query.assert_called_once_with("test query")
        assert "1. Result 1" in result.output
        assert "2. Result 2" in result.output

    def test_search_query_no_results(self, runner, mock_search_app):
        """Test search query with no results"""
        mock_search_app.return_value.init = AsyncMock()
        mock_search_app.return_value.query.return_value = []

        result = runner.invoke(cli, ["search", "test query"])

        assert result.exit_code == 0
        assert "No results found." in result.output

    def test_chat_query(self, runner, mock_rag_app):
        """Test chat query through CLI"""
        mock_rag_app.return_value.init = AsyncMock()
        result = runner.invoke(cli, ["chat", "test question"])

        assert result.exit_code == 0
        mock_rag_app.return_value.query.assert_called_once_with("test question")
        assert "Chat response" in result.output

    def test_summarize_text(self, runner, mock_summarizer_app):
        """Test text summarization through CLI"""
        mock_summarizer_app.return_value.init = AsyncMock()
        result = runner.invoke(cli, ["summarize", "Text to summarize"])

        assert result.exit_code == 0
        mock_summarizer_app.return_value.summarize.assert_called_once_with(
            "Text to summarize"
        )
        assert "Summarized text" in result.output

    def test_summarize_file(self, runner, mock_summarizer_app, tmp_path):
        """Test file summarization through CLI"""
        mock_summarizer_app.return_value.init = AsyncMock()
        test_file = tmp_path / "test.txt"
        test_file.write_text("Content to summarize")

        result = runner.invoke(cli, ["summarize", "--file", str(test_file)])

        assert result.exit_code == 0
        mock_summarizer_app.return_value.summarize.assert_called_once_with(
            "Content to summarize"
        )
        assert "Summarized text" in result.output

    def test_invalid_command(self, runner):
        """Test invalid command handling"""
        result = runner.invoke(cli, ["invalid"])
        expected_exit_code = 2
        assert result.exit_code == expected_exit_code
        assert "No such command" in result.output
