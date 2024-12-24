.. _configuration:

*****************
Configuration
*****************

To begin development for the library, follow the instructions below to set up your environment.

# TODO: Add once we have a config file!

You can configure the app with a config file ``config.yaml`` like this.


.. code-block:: yaml

    splitter:
        chunk_size: 1024
        chunk_overlap: 256

    llm:
        model: "llama3"

    embedding:
        model: "all-MiniLM-L6-v2"

Place this file into the root of your project. For example, if you are developing an app ``myapp``, place the ``config.yaml`` next to you where you are initializing the package, or provide the path to the config file.

.. code-block:: bash

    myapp/
    ├── __init__.py
    ├── main.py
    ├── config.yaml

