.. _building_apps:

***************
Building Apps
***************

Once the package is installed, you can start building apps with it. This section shows in more detail how the three apps can be used.

Note that the app caches weights for the LLM and the embedding model. The weights are eagerly downloadeed if they cannot be found when you initialize an app. This is to minimize the latency in a deployed scenario.


Search App
=================

The ``SearchApp`` allows you to perform a semantic search over your database. This returns a list of document names which contain text relevant to the query.


.. code-block:: bash

    from insightvault import SearchApp

    search_app = SearchApp()

    # Perform a search
    results = search_app.search("Why is the sky blue?")

    # Async search
    results = await search_app.async_search("Why is the sky blue?")

As you can see, there is a synchronous and an asynchronous method availabe. This is the case for all app methods.


Chat App
=================

The ``ChatApp`` allows you to perform an interactive chat with your data. This app also keeps your chat history.

# TODO: Add clearing chat history

.. code-block:: bash

    from insightvault import ChatApp

    chat_app = ChatApp()

    # Ask a qustion
    results = chat_app.query("Why is the sky blue?")

    # Async method
    results = await chat_app.async_query("Why is the sky blue?")

    # Clear the chat history
    chat_app.clear()


Summarizer App
=================


.. code-block:: bash

    pip install insightvault