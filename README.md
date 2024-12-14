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

## Publishing

``bash

# Install build tools

pip install build twine

# Build the package

python -m build

# Check the distribution

twine check dist/*

# Test upload to TestPyPI (optional)

twine upload --repository testpypi dist/*

# Upload to PyPI

twine upload dist/*

```
