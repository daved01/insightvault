.. InsightVault documentation master file, created by
   sphinx-quickstart on Sat Dec 21 15:07:57 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

InsightVault documentation
==========================

InsightVault is a framework for building AI applications that run locally.

# TODO: Add better explanation of what the app is about



To get started, run

.. code-block:: bash

   pip install insightvault

Then you can use the three apps for your needs like this.

The `SummarizerApp` is used to summarize text.

.. code-block:: python

   from insightvault import SummarizerApp

   # Initialization
   summarizer_app = SummarizerApp()

   # Summarization (synchronous)
   summary = summarizer_app.summarize(text="This is a very long text...")


The search and chat apps use a database we must populate first. This database is shared between the two apps.

.. code-block:: python

   from insightvault import SearchApp, ChatApp

   # Initialize one or more apps
   search_app = SearchApp()
   chat_app = ChatApp()

   # Summarization (synchronous)
   summary = summarizer_app.summarize(text="This is a very long text...")

   # Chat (synchronous)
   chat_response = chat_app.query("Given what we have talked about before, why is the earth flat?")


Note that all methods shown above also have an async method with an `async_` prefix.

Before we can query our documents we have to add them to the database.


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
   contents/api/insightvault


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`