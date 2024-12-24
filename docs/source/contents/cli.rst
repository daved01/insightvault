.. _cli:

***************
Using the CLI
***************

The package comes with a CLI which allows you to test out the functionality, manage the vector database, or integrate `insightvault` with a CI/CD setup.

To get started, you can view the interactive help:

.. code-block:: bash

    insightvault --help

Command ``manage``
==========================

The ``manage`` commands let you interact with the vector database. The database is used by the ``SearchApp`` and the ``ChatApp``.

You can add ``txt`` files like this.

.. code-block:: bash
    
    insightvault manage add-file <path-to-file>

This creates a ``Document`` of the input, splits it into chunks, and ingests these chunks into the database with the created embeddings of the chunks.

You can also directly add text as a string.

.. code-block:: bash
    
    insightvault manage add-text <text>

To view which documents are in the database, you can use this.

.. code-block:: bash
    
    insightvault manage list

Finally, to clear the database, run:

.. code-block:: bash
    
    insightvault manage delete-all



Command ``summarize``
==========================

This uses the ``SummarizerApp`` to summarize the input. Consequently, this does not use the database.


.. code-block:: bash
    
    insightvault summarize "This is a very long string which we must summarize."

You can also provide the path to a ``txt``  file like this.

.. code-block:: bash
    
    insightvault summarize --file "./data/my-file.txt"


Command ``search``
==========================

You an search through the document chunks in the database with semantic search.

.. code-block:: bash
    
    insightvault search <query>

This will return the document name of the best matches (there is a fixed limit for how many you can set in the config file).


Commant ``chat``
==========================

This commands provides an interactive chat that allows you to chat with your documents in the database. This is using retrieval-augmented generation [TODO: Add link]().

.. code-block:: bash
    
    insightvault chat <question>

Please note that because the app restarts on every commands, this does not preserve a chat history. For this and other features, you can :ref:`building_apps` use the package to create your own apps as described next.
