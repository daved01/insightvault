.. InsightVault documentation master file, created by
   sphinx-quickstart on Sat Dec 21 15:07:57 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
==========================

InsightVault is a framework for building AI applications that run locally, providing tools for semantic search, text summarization, and Retrieval-Augmented Generation (RAG)-based chat. 

With InsightVault, developers can easily create on-premise FastAPI services or similar interfaces to enable advanced natural language processing workflows. Whether you need to perform quick document searches, generate concise summaries, or interact through intelligent chat systems, InsightVault has you covered.

To get started, install the package using:

.. code-block:: bash

   pip install insightvault

**Using the SummarizerApp**

The SummarizerApp simplifies text summarization:


.. code-block:: python

   from insightvault import SummarizerApp

   # Initialize the summarizer
   summarizer_app = SummarizerApp()

   # Generate a summary
   summary = summarizer_app.summarize(text="This is a very long text...")
   print(summary)


**Using the Search and Chat Apps**

The SearchApp and ChatApp rely on a shared database. Populate the database before querying:

.. code-block:: python

   from insightvault import SearchApp, ChatApp, Document

   # Initialize the apps
   search_app = SearchApp()
   chat_app = ChatApp()

   # Add documents to the database (example)
   documents = [
      Document(
         content= "The earth is flat.",
         title="The Truth Teller",
         metadata={"source": "the internet"}
      )
   ]

   search_app.add_documents(documents)

   # Perform a search
   search_results = search_app.query("What shape is the earth?")
   print(search_results)

   # Chat interaction
   chat_response = chat_app.query("Given what we have talked about before, why is the earth flat?")
   print(chat_response)


Note: All synchronous methods (e.g., summarize, search, query) have asynchronous counterparts with the prefix ``async_``. For example, use ``async_summarize()`` for asynchronous summarization.


Table of contents
=========================

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   contents/installation


.. toctree::
   :maxdepth: 2
   :caption: Usage guide

   contents/configuration
   contents/building_apps
   contents/cli


.. toctree::
   :maxdepth: 2
   :caption: Developer guide

   contents/develop
   contents/api_reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`