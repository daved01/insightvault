import uuid
from pathlib import Path

import click

from insightvault import __version__

from ..models.document import Document
from .rag import RAGApp
from .search import SearchApp
from .summarizer import SummarizerApp


@click.group()
@click.version_option(__version__)
def cli() -> None:
    """InsightVault - Local RAG Pipeline Runner."""
    pass


def _add_document_to_app(filepath: str, app_name: str, app_class: type) -> None:
    """Helper function to add a document to an app"""
    app = app_class(name=app_name)

    # Read file content
    path = Path(filepath)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Create and add document
    doc = Document(
        title=path.name,
        content=content,
        metadata={"title": path.name, "source": str(path)},
    )

    app.add_documents([doc])


def _add_text_to_app(text: str, app_name: str, app_class: type) -> None:
    """Helper function to add text to an app"""
    app = app_class(name=app_name)
    doc = Document(
        title="Direct Input",
        content=text,
        metadata={"title": "Direct Input", "type": "direct_input"},
    )
    app.add_documents([doc])


def _list_documents_with_app(app_name: str, app_class: type) -> None:
    """Helper function to list document titles using an app"""
    app = app_class(name=app_name)
    documents: list[Document] = app.list_documents()

    if not documents:
        click.echo("No documents found in database.")
        return

    click.echo("\nDocuments in database:")
    for i, doc in enumerate(documents, 1):
        click.echo(f"{i}. {doc.metadata.get('title', 'Untitled')} (ID: {doc.id})")


def _delete_all_documents_with_app(app_name: str, app_class: type) -> None:
    """Helper function to delete all documents using an app"""
    app = app_class(name=app_name)
    app.delete_all_documents()
    click.echo("All documents deleted from the database!")


@cli.group()
def search() -> None:
    """Search operations using the database"""
    pass


@search.command(name="add-file")
@click.argument("filepath", type=click.Path(exists=True))
def search_add_document(filepath: str) -> None:
    """Add a document in the filepath to the search database"""
    _add_document_to_app(filepath, "insightvault.search", SearchApp)


@search.command(name="add-text")
@click.argument("text")
def search_add_text(text: str) -> None:
    """Add a text to the search database"""
    _add_text_to_app(text, "insightvault.search", SearchApp)


@search.command(name="query")
@click.argument("query_text")
def search_search_documents(query_text: str) -> None:
    """Search documents in the database"""
    app = SearchApp(name="insightvault.search")
    results: list[str] = app.query(query_text)

    if not results:
        click.echo("No results found.")
        return

    click.echo("\nSearch results:")
    for i, result in enumerate(results, 1):
        click.echo(f"{i}. {result}")


@search.command(name="list")
def search_list_documents() -> None:
    """List all documents in the search database"""
    _list_documents_with_app("insightvault.search", SearchApp)


@search.command("delete-all")
def search_delete_all():
    """Delete all documents from the search database"""
    _delete_all_documents_with_app("search", SearchApp)


@cli.group()
def chat() -> None:
    """Chat operations using the database"""
    pass


@chat.command(name="add-file")
@click.argument("filepath", type=click.Path(exists=True))
def chat_add_document(filepath: str) -> None:
    """Add a document in the filepath to the RAG database"""
    _add_document_to_app(filepath, "insightvault.rag", RAGApp)


@chat.command(name="add-text")
@click.argument("text")
def chat_add_text(text: str) -> None:
    """Add a text to the RAG database"""
    _add_text_to_app(text, "insightvault.rag", RAGApp)


@chat.command(name="query")
@click.argument("query_text")
def chat_search_documents(query_text: str) -> None:
    """Search documents in the database and return a chat response"""
    app = RAGApp(name="insightvault.rag")
    results: str = app.query(query_text)

    if not results:
        click.echo("No results found.")
        return

    click.echo("\nChat response:")
    # TODO: Implement chat response
    click.echo(results)


@chat.command(name="list")
def chat_list_documents() -> None:
    """List all documents in the RAG database"""
    _list_documents_with_app("insightvault.rag", RAGApp)


@chat.command("delete-all")
def chat_delete_all():
    """Delete all documents from the RAG database"""
    _delete_all_documents_with_app("rag", RAGApp)


@cli.group()
def summarize() -> None:
    """Summarization operations"""
    pass


@summarize.command(name="text")
@click.argument("text")
def summarize_text(text: str) -> None:
    """Summarize the provided text"""
    app = SummarizerApp(name="insightvault.summarizer")

    # Create a temporary document for summarization
    doc = Document(
        id=str(uuid.uuid4()),
        content=text,
        title="Direct Input",
        metadata={"type": "direct_input"},
    )

    summary = app.summarize([doc])
    click.echo("\nSummary:")
    click.echo(summary)


@summarize.command(name="file")
@click.argument("filepath", type=click.Path(exists=True))
def summarize_file(filepath: str) -> None:
    """Summarize the content of a file"""
    app = SummarizerApp(name="insightvault.summarizer")

    # Read file content
    path = Path(filepath)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Create document for summarization
    doc = Document(
        id=str(uuid.uuid4()),
        content=content,
        metadata={"title": path.name, "source": str(path)},
    )

    summary = app.summarize([doc])
    click.echo("\nSummary:")
    click.echo(summary)


def main() -> None:
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
