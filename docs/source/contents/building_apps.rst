.. _building_apps:

***************
Building Apps
***************

Once the package is installed, you can start building applications using InsightVault. 
This section demonstrates how to utilize the three main apps: ``SearchApp``, ``ChatApp``, and ``SummarizerApp``.

    **Note:** 
    InsightVault caches the weights for the LLM and the embedding model. These weights are eagerly downloaded when you initialize an app if they are not already available locally. This ensures minimal latency during runtime.


Search App
=====================================

The ``SearchApp`` enables semantic search over your database. It returns a list of documents relevant to your query based on their content.  

**Example Usage:**

.. code-block:: python
    
    from insightvault import Document, SearchApp

    # Initialize the SearchApp
    search_app = SearchApp()

    # Add documents to the database
    documents = [
        Document(
            title="Sky Science", 
            content="The sky is blue because of Rayleigh scattering.",
            metadata={"source": "A book"}),
        Document(
             title="Sky Science", 
            content="The ocean reflects the sky's color, which is why it appears blue.",
            metadata={"source": "A book"})
    ]
    search_app.add_documents(documents)

    # Perform a synchronous search
    results = search_app.query("Why is the sky blue?")
    print(results)

    # Perform an asynchronous search
    results = await search_app.async_query("Why is the sky blue?")
    print(results)

**Tip:** Ensure you populate the database with your documents before performing a search. The methods ``add_documents()`` and ``delete_documents()`` allow you to manage the document database.


Chat App
=====================================

The ChatApp facilitates an interactive chat experience with your data. It maintains chat history, enabling contextual conversations.

**Example Usage:**

.. code-block:: python

    from insightvault import ChatApp, Document

    # Initialize the ChatApp
    chat_app = ChatApp()

    # Add documents to the database (shared with SearchApp)
    documents = [
        Document(
            title="More Science",
            content="The earth revolves around the sun.",
            metadata={"another key": "We can add whatever we want"}
        )
    ]
    chat_app.add_documents(documents)

    # Ask a question
    response = chat_app.query("What does the earth revolve around?")
    print(response)

    # Perform an asynchronous query
    response = await chat_app.async_query("What does the earth revolve around?")
    print(response)

    # Clear the chat history
    chat_app.clear()

**Note:** Currently, ``clear()`` clears the entire chat history.


Summarizer App
=====================================

The SummarizerApp enables concise summarization of lengthy text documents. Unlike the SearchApp and ChatApp, the SummarizerApp does not require a shared database.

**Example Usage:**

.. code-block:: python

    from insightvault import SummarizerApp

    # Initialize the SummarizerApp
    summarizer_app = SummarizerApp()

    # Summarize text (synchronous)
    summary = summarizer_app.summarize(text="This is a very long text about the history of the universe...")
    print(summary)

    # Summarize text (asynchronous)
    summary = await summarizer_app.async_summarize(text="This is a very long text about the history of the universe...")
    print(summary)


Key Notes for All Apps
=====================================

**1.	Synchronous vs. Asynchronous Methods:**

All apps offer synchronous methods (e.g., search, query, summarize) and their asynchronous equivalents with the prefix async_ (e.g., async_search, async_query, async_summarize).

**2.	Database Management:**

- The SearchApp and ChatApp share a document database.

- Use the ``add_documents()`` method to populate the database and ``delete_documents()`` to remove entries.

**3.	Cached Models:**

- The LLM and embedding model weights are cached for efficiency.

- On first use, the package will download the required weights if they are not already available.

This comprehensive toolkit empowers you to build robust AI-powered applications with ease.
