import uuid
from pathlib import Path

import click

from insightvault import __version__

from ..models.document import Document
from .rag import RAGApp
from .summarizer import SummarizerApp


@click.group()
@click.version_option(__version__)
def cli() -> None:
    """InsightVault - Local RAG Pipeline Runner."""
    pass


@cli.group()
def query() -> None:
    """Query operations for RAG"""
    pass


@query.command(name="add-file")
@click.argument("filepath", type=click.Path(exists=True))
def add_document(filepath: str) -> None:
    """Add a document in the filepath to the RAG database"""
    app = RAGApp(name="insightvault.rag")

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


@query.command(name="add-text")
@click.argument("text")
def add_text(text: str) -> None:
    """Add a text to the RAG database"""
    app = RAGApp(name="insightvault.rag")
    doc = Document(
        title="Direct Input",
        content=text,
        metadata={"title": "Direct Input", "type": "direct_input"},
    )
    app.add_documents([doc])


@query.command(name="search")
@click.argument("query_text")
def search_documents(query_text: str) -> None:
    """Search documents in the RAG database"""
    app = RAGApp(name="insightvault.rag")
    results = app.query(query_text)

    if not results:
        click.echo("No results found.")
        return

    click.echo("\nSearch results:")
    for i, doc in enumerate(results, 1):
        click.echo(f"\n{i}. {doc.metadata.get('title', 'Untitled')}")
        click.echo(f"Content: {doc.content[:200]}...")


@query.command(name="list")
def list_documents() -> None:
    """List all documents in the database"""
    app = RAGApp(name="insightvault.rag")
    documents = app.list_documents()

    if not documents:
        click.echo("No documents found in database.")
        return

    click.echo("\nDocuments in database:")
    for i, doc in enumerate(documents, 1):
        click.echo(f"{i}. {doc.metadata.get('title', 'Untitled')} (ID: {doc.id})")


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
