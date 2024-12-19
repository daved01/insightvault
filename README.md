# Insight Vault

 Python application for running local RAG (Retrieval-Augmented Generation) pipelines.

## Features

- Local document storage using Chroma DB
- Local LLM inference using LLAMA
- Local embeddings using HuggingFace models
- CLI interface with interactive mode
- REST API using FastAPI

## Installation

```bash
pip install -e .
```

## Usage

```bash
insightvault <command> <args>
```

## Development

1. Clone the repository

```bash
git clone https://github.com/daved01/insightvault.git
```

2. Install the dependencies

```bash
pip install -e ".[dev]"
```

3. Run the tests

```bash
pytest
```

Checks

```bash
mypy insightvault
ruff check . --fix
ruff format .
```

## Publishing
