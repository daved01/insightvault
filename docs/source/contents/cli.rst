.. _cli:

***************
Using the CLI
***************

The package includes a Command-Line Interface (CLI) designed primarily for debugging, quick testing, and simple integrations. It allows you to explore functionality, manage the vector database, and even integrate ``insightvault`` into a CI/CD pipeline.  

    **Note:** The CLI is optimized for simplicity, not performance. It is slower by design compared to using the Python package directly, as it initializes components on every command.

To get started, display the available commands and their descriptions by running:

.. code-block:: bash

    insightvault --help

Command: manage
=========================

The manage command allows you to interact with the vector database used by the SearchApp and ChatApp. You can add, view, or clear documents stored in the database.

**Adding Documents**

You can add documents in two ways:

1.	From a text file:

.. code-block:: bash

    insightvault manage add-file <path-to-file>

This splits the input file into chunks, generates embeddings for each chunk, and ingests them into the database.

2.	From raw text:

.. code-block:: bash

    insightvault manage add-text "<text>"

This creates and ingests a document directly from the provided string.


**Listing Documents**

To view the documents stored in the database:

.. code-block:: bash

    insightvault manage list


**Clearing the Database**

To delete all documents and reset the database:

.. code-block:: bash

    insightvault manage delete-all


Command: summarize
=========================

The summarize command uses the ``SummarizerApp`` to generate concise summaries of text. This command does not use the vector database.

**Summarizing Raw Text**

Provide a string to summarize directly:

.. code-block:: bash
    
    insightvault summarize "This is a very long string which we must summarize."


**Summarizing a Text File**

Provide the path to a text file for summarization:

.. code-block:: bash
    
    insightvault summarize --file "./data/my-file.txt"


Command: search
=========================

The search command performs semantic searches on the document chunks in the vector database.

**Example Search**

Run a query to retrieve the most relevant documents:

.. code-block:: bash
    
    insightvault search "Why is the sky blue?"


The results include the names of the best-matching documents, with the maximum number of results configurable in your ``config.yaml``.


Command: chat
=========================

The chat command provides an interactive session for chatting with the documents stored in the vector database. It leverages Retrieval-Augmented Generation (RAG) to generate context-aware responses.

**Starting a Chat**

Ask a question and receive a response based on your documents:

.. code-block:: bash
    
    insightvault chat "What is Rayleigh scattering?"


**Important:** The CLI chat does not preserve history between commands. For persistent conversations and enhanced features, consider building custom apps as described in :ref:`building_apps`.


Notes
=========================
	
1.	Performance:
The CLI initializes components on each invocation, making it slower than direct programmatic use. For production-grade performance, use the Python package.

2.	Shared Database:
The manage, search, and chat commands operate on the same shared database, which is accessible across multiple CLI sessions.

3.	Debugging and Prototyping:
The CLI is ideal for debugging and quickly testing new ideas but is not recommended for latency-critical or high-volume use cases.
