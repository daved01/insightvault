from pathlib import Path

import click

from insightvault import __version__

from ..models.document import Document
from .base import BaseApp
from .rag import RAGApp
from .search import SearchApp
from .summarizer import SummarizerApp


@click.group()
@click.version_option(__version__)
def cli() -> None:
    """InsightVault - Local RAG Pipeline Runner."""
    pass


@cli.group()
def manage() -> None:
    """Manage documents in the databases"""
    pass


@manage.command(name="add-file")
@click.argument("filepath", type=click.Path(exists=True))
def manage_add_file(filepath: str) -> None:
    """Add a document from a file to the specified database"""
    app = BaseApp(name="insightvault.base")

    path = Path(filepath)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    doc = Document(
        title=path.name,
        content=content,
        metadata={"title": path.name, "source": str(path)},
    )

    app.add_documents([doc])


@manage.command(name="add-text")
@click.argument("text")
def manage_add_text(text: str) -> None:
    """Add text to the specified database"""
    app = BaseApp(name="insightvault.base")
    doc = Document(
        title="Direct Input",
        content=text,
        metadata={"title": "Direct Input", "type": "direct_input"},
    )
    app.add_documents([doc])


@manage.command(name="list")
def manage_list_documents() -> None:
    """List all documents in the specified database"""
    app = BaseApp(name="insightvault.base")
    documents: list[Document] | None = app.list_documents()

    if not documents:
        click.echo("No documents found in database.")
        return

    click.echo("\nDocuments in database:")
    for i, doc in enumerate(documents, 1):
        click.echo(f"{i}. {doc.metadata.get('title', 'Untitled')} (ID: {doc.id})")


@manage.command(name="delete-all")
def manage_delete_all() -> None:
    """Delete all documents from the specified database"""
    app = BaseApp(name="insightvault.base")
    app.delete_all_documents()
    click.echo("All documents deleted from the database!")


@cli.group()
def search() -> None:
    """Search operations using the database"""
    pass


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


@cli.group()
def chat() -> None:
    """Chat operations using the database"""
    pass


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
    click.echo(results)


@cli.group()
def summarize() -> None:
    """Summarization operations"""
    pass


@summarize.command(name="text")
@click.argument("text")
def summarize_text(text: str) -> None:
    """Summarize the provided text"""
    app = SummarizerApp(name="insightvault.summarizer")

    summary = app.summarize(text)
    click.echo("\nSummary:")
    click.echo(summary)


@summarize.command(name="file")
@click.argument("filepath", type=click.Path(exists=True))
def summarize_file(filepath: str) -> None:
    """Summarize the content of a file"""
    app = SummarizerApp(name="insightvault.summarizer")

    path = Path(filepath)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    summary = app.summarize(content)
    click.echo("\nSummary:")
    click.echo(summary)


def main() -> None:
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
