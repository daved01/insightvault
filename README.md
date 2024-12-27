# Insight Vault

<p align="center">
 <a href="https://www.python.org/downloads/release/python-312/"><img src="https://img.shields.io/badge/python-3.12-green.svg" alt="Python 3.12"></a>
 <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
  <a href="https://pypi.org/project/insightvault"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/insightvault?color=blue"></a>
 <img src="https://github.com/daved01/insightvault/actions/workflows/quality-checks.yml/badge.svg" alt="GitHub CI">
</p>

**Insight Vault** is a local, privacy-focused library for building LLM-based applications. It allows you to store, search, and summarize text completely offline.

With **Insight Vault**, you can:

- **Search** your local knowledge base.
- **Chat** with your documents interactively.
- **Summarize** large sets of information into concise outputs.

All data stays **on your machine**, with no external API calls required.

## 🚀 **Features**

- **Local Inference** — Uses LLAMA for local LLM inference.
- **Local Embeddings** — Embeddings are created using SentenceTransformers.
- **Privacy-first RAG** — Store and query documents locally with ChromaDB.
- **Interactive CLI** — Intuitive CLI interface for searching, managing, and summarizing.

## 📦 **Dependencies**

The following dependencies are required to run **Insight Vault**:

- [**Ollama**](https://ollama.com/) — For local LLM inference.
- [**ChromaDB**](https://docs.trychroma.com/) — Local document storage and vector database.
- [**SentenceTransformers**](https://www.sbert.net/) — Embeddings for better document search and query matching.

## 🔥 **Installation**

To install **Insight Vault**, you can use the following command:

```bash
pip install insightvault
```

## ⚙️ **Usage**

Insight Vault can be used via a simple CLI interface or as a Python library.

If you want to use the `chat` or `summarize` commands, you need to make sure that Ollama is running first.

### CLI

**Adding Documents**

```bash
insightvault manage add-file <path_to_document>
```

This command will add a file from the specified path to the local document database. You can also directly add text. The `manage` command is also used to list all documents, and to delete all documents.

**Searching Documents**

```bash
insightvault search "Explain RAG pipelines"
```

This will search your indexed documents for the query “Explain RAG pipelines” and return the most relevant results.

**Chat**

```bash
insightvault chat "Explain RAG pipelines"
```

This uses RAG which means it takes in a natural language query and returns a response in natural language based on the most relevant documents you have indexed.

**Summarizing Documents**

```bash
insightvault summarize "Explain RAG pipelines"
```

Summarizes the text you provide. The flag `--file` can be used to summarize a file.

### Library

Insightvault provides three apps as part of the library:

- `RAGApp` — For RAG pipelines.
- `SearchApp` — For searching indexed documents.
- `SummarizerApp` — For summarizing text.

For example, to use the `SummarizerApp`, you can do the following:

```python
from insightvault import SummarizerApp

app = SummarizerApp()
await app.summarize("This is a loooong test")
```

See the [API Documentation](TODO!) for more information.

## 🛠️ **Development**

If you want to contribute to Insight Vault or run it locally for development, follow these steps.

1. Clone the Repository

```bash
git clone https://github.com/daved01/insightvault.git
cd insightvault
```

2. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

This installs all required libraries for development, testing, and quality checks.

3. Run Tests

```bash
pytest tests
```

This runs all the unit and integration tests to ensure everything is working properly.

4. Run Quality Checks

We use ruff, mypy, and pre-commit hooks to ensure high code quality.

```bash
# Type checking with mypy
mypy insightvault

# Linting and formatting with ruff
ruff check . --fix
ruff format .
```

Pre-commit Hooks

To automatically check for secrets, format code, and run linters before every commit, set up pre-commit hooks as follows:

```bash
pre-commit install
```

This will install the hooks and run them automatically before each commit.

---

## 📤 **Publishing**

To publish a new version of Insight Vault to PyPI:

1. Update the version in pyproject.toml.
2. Build the package:

```bash
python -m build
```

3. Publish the package:

```bash
twine upload dist/*
```

---

## 💡 **Contributing**

We welcome contributions of all kinds. Whether it’s bug fixes, new features, or improving the documentation. Please open an issue or submit a pull request.
