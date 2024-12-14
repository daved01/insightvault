import click
from typing import Optional

@click.group()
def cli() -> None:
    """InsightVault - Local RAG Pipeline Runner"""
    pass

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--collection', '-c', help='Collection name', default='default')
def add(file_path: str, collection: str) -> None:
    """Add a document to the database"""
    click.echo(f"Adding document from {file_path} to collection {collection}")

@cli.command()
@click.argument('query')
@click.option('--collection', '-c', help='Collection name', default='default')
@click.option('--k', help='Number of results', default=5)
def query(query: str, collection: str, k: int) -> None:
    """Query the database"""
    click.echo(f"Querying '{query}' in collection {collection}")

if __name__ == '__main__':
    cli() 