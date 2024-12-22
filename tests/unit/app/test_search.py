from unittest.mock import Mock, patch

import pytest

from insightvault.app.search import SearchApp
from insightvault.models.document import Document


class TestSearchApp:
    @pytest.fixture
    def search_app(
        self, mock_db_service, mock_splitter_service, mock_embedding_service
    ):
        """Create a search app with mocked services"""
        with (
            patch("insightvault.app.base.ChromaDatabaseService") as mock_db_class,
            patch("insightvault.app.base.SplitterService") as mock_splitter_class,
            patch("insightvault.app.base.EmbeddingService") as mock_embedding_class,
        ):
            mock_db_class.return_value = mock_db_service
            mock_splitter_class.return_value = mock_splitter_service
            mock_embedding_class.return_value = mock_embedding_service

            app = SearchApp()
            return app

    @pytest.mark.asyncio
    async def test_async_query_returns_sorted_unique_titles(self, search_app):
        """Test that query returns sorted unique document titles"""
        # Setup mock responses
        await search_app.init_base()
        search_app.embedder.embed.return_value = [[0.1, 0.2, 0.3]]
        search_app.db.query.return_value = [
            Document(title="Doc B", content="Content B"),
            Document(title="Doc A", content="Content A"),
            Document(title="Doc B", content="Duplicate title"),  # Duplicate title
        ]

        result = await search_app.async_query("test query")

        # Verify embeddings were generated
        search_app.embedder.embed.assert_called_once_with(["test query"])

        # Verify database was queried with embeddings
        search_app.db.query.assert_called_once_with([0.1, 0.2, 0.3])

        # Verify results are unique and sorted
        assert result == ["Doc A", "Doc B"]

    def test_sync_query_calls_async_version(self, search_app):
        """Test that sync query method properly calls async version"""
        with patch("asyncio.get_event_loop") as mock_loop:
            mock_loop.return_value.run_until_complete = Mock()

            search_app.query("test query")

            mock_loop.return_value.run_until_complete.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_query_with_no_results(self, search_app):
        """Test query behavior when no results are found"""
        await search_app.init_base()
        search_app.embedder.embed.return_value = [[0.1, 0.2, 0.3]]
        search_app.db.query.return_value = []

        result = await search_app.async_query("test query")

        assert result == []

    @pytest.mark.asyncio
    async def test_async_query_preserves_query_text(self, search_app):
        """Test that query text is preserved in embedding call"""
        complex_query = "What is the meaning of life?"
        await search_app.init_base()
        search_app.embedder.embed.return_value = [[0.1, 0.2, 0.3]]
        search_app.db.query.return_value = []

        await search_app.async_query(complex_query)

        search_app.embedder.embed.assert_called_once_with([complex_query])

    @pytest.mark.asyncio
    async def test_async_query_initializes_base(self, search_app):
        """Test that query initializes base app"""
        await search_app.init_base()
        search_app.embedder.embed.return_value = [[0.1, 0.2, 0.3]]
        search_app.db.query.return_value = []

        await search_app.async_query("test query")

        # Verify init_base was called
        search_app.embedder.get_client.assert_called()
