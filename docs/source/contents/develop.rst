.. _develop:

*****************
Development setup
*****************

This section provides instructions for setting up your environment to contribute to the ``insightvault`` library.  


Preparing Your Environment
==============================================

**1. Clone the Repository**
First, clone the repository from the version control system and navigate to the project directory:  

.. code-block:: bash

   git clone https://github.com/daved01/insightvault.git
   cd insight-vault


**2. Set Up a Virtual Environment**
It is recommended to use a virtual environment to isolate your development dependencies.

Create and activate the virtual environment:

.. code-block:: bash

    python -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate     # On Windows

For more information on managing envirnoments with Pyenv and virtualenv, see my `post <https://deconvoluteai.com/blog/neuralception/pyenvvirtualenv>`_ .


**3. Install the Package in Development Mode**
Install the library in editable mode along with the development dependencies:

.. code-block:: bash

    pip install -e .[dev]

This setup allows you to test changes to the codebase without reinstalling the package.


**4. Verify the Installation**
Ensure the package is installed correctly by running:
    
.. code-block:: bash

    insightvault --help

You should see the CLI help message, confirming the setup is functional.


Running Tests
==============================================

To ensure your changes do not break existing functionality, run the test suite:


.. code-block:: bash
   
    pytest

For detailed test output, use:


.. code-block:: bash
   
    pytest -v

Install pre-commit hooks with:

.. code-block:: bash

    pre-commit install

This will automatically run checks (like formatting and linting) before you commit code.


Code Quality and Formatting
==============================================

The project follows code quality and formatting guidelines. Ensure your changes adhere to these standards:

**Linting:**
Run ruff to check for coding style violations:

.. code-block:: bash

    ruff check insightvault tests

**Formatting:**
Use ruff to format the codebase:

.. code-block:: bash

    ruff format insightvault tests

**Type Checking:**
Run mypy to check type annotations:

.. code-block:: bash

    mypy insightvault


Building the Documentation
==============================================

To update or preview the project documentation, install the documentation dependencies and build the docs:

.. code-block:: bash

    cd docs
    pip install requirements.txt
    make html

The HTML output will be available in the ``docs/_build/html`` directory. Open the ``index.html`` file in a browser to preview it.


Contributing
==============================================

If you plan to contribute to the library, please:

1. Create a new branch.

2. Write tests for any new functionality or changes.

3. Make sure all quality checks pass.

4. If you introduce a new feature, update the documentation.

5. Submit a pull request with a clear description of your changes.

