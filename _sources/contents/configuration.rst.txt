.. _configuration:

*****************
Configuration
*****************

InsightVault provides a flexible configuration system through a YAML file, allowing you to customize key settings for the framework.


Default Configuration
===================================

Below is an example configuration file, ``config.yaml``:


.. code-block:: yaml

    database:
        max_num_results: 8      # Number of docs returned from the db using ANN
        result_threshold: 0.95  # Similarity threshold below which results are not returned
        path: "./data/db"       # Path for the database

    splitter:
        chunk_size: 1024
        chunk_overlap: 256

    llm:
        model: "llama3"

    embedding:
        model: "all-MiniLM-L6-v2"


Setting Up the Configuration
===================================

Place the config.yaml file in the root of your project directory. For instance, if your project is called myapp, the directory structure should look like this:

.. code-block:: bash

    myapp/
    ├── __init__.py
    ├── main.py
    ├── config.yaml

Alternatively, you can specify a custom path to the configuration file when initializing the package.

.. code-block:: python
    from insightvault import SearchApp

    # Specify the path to your configuration file
    search_app = SearchApp(config_path="path/to/config.yaml")

**Tip:** If no configuration file is provided, InsightVault will use default values.