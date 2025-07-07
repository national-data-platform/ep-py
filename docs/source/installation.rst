Installation Guide
==================

Requirements
------------

* Python 3.8 or higher
* requests >= 2.25.0
* urllib3 >= 1.26.0

Installing from PyPI
---------------------

The easiest way to install ndp-ep is from PyPI using pip:

.. code-block:: bash

   pip install ndp-ep

Installing from Source
-----------------------

You can also install directly from the GitHub repository:

.. code-block:: bash

   pip install git+https://github.com/sci-ndp/ndp-ep-py.git

For development purposes, clone the repository and install in editable mode:

.. code-block:: bash

   git clone https://github.com/sci-ndp/ndp-ep-py.git
   cd ndp-ep-py
   pip install -e .

Development Installation
------------------------

If you want to contribute to the project, install the development dependencies:

.. code-block:: bash

   git clone https://github.com/sci-ndp/ndp-ep-py.git
   cd ndp-ep-py
   
   # Create virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install package and development dependencies
   pip install -e .
   pip install -r requirements-dev.txt

Verifying Installation
----------------------

After installation, you can verify that the library is working correctly:

.. code-block:: python

   import ndp_ep
   print(ndp_ep.__version__)
   
   # Basic connection test (replace with actual API URL)
   from ndp_ep import APIClient
   
   try:
       client = APIClient(base_url="http://155.101.6.191:8003")
       print("✓ Connection successful")
   except Exception as e:
       print(f"✗ Connection failed: {e}")

Docker Installation
-------------------

If you prefer using Docker, you can create a container with the library pre-installed:

.. code-block:: dockerfile

   FROM python:3.11-slim
   
   WORKDIR /app
   
   # Install ndp-ep
   RUN pip install ndp-ep
   
   # Copy your scripts
   COPY . .
   
   CMD ["python", "your_script.py"]

Jupyter Notebook Installation
-----------------------------

For interactive development and tutorials, install Jupyter:

.. code-block:: bash

   pip install ndp-ep jupyter
   
   # Start Jupyter
   jupyter notebook

Then create a new notebook and test the installation:

.. code-block:: python

   import ndp_ep
   from ndp_ep import APIClient
   
   print(f"ndp-ep version: {ndp_ep.__version__}")

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**ImportError: No module named 'ndp_ep'**

Make sure you have installed the package correctly:

.. code-block:: bash

   pip list | grep ndp-ep

**Connection Errors**

If you encounter connection errors, check:

1. Network connectivity to the API endpoint
2. Firewall settings
3. API endpoint URL (ensure it's correct and accessible)

**Authentication Issues**

For authentication problems:

1. Verify your API token is valid
2. Check token expiration
3. Ensure proper permissions for your account

Getting Help
~~~~~~~~~~~~

If you encounter issues not covered here:

1. Check the `GitHub Issues <https://github.com/sci-ndp/ndp-ep-py/issues>`_
2. Review the API documentation
3. Create a new issue with:
   - Python version
   - ndp-ep version
   - Complete error message
   - Minimal code example reproducing the issue

Virtual Environment Recommendations
-----------------------------------

It's strongly recommended to use a virtual environment:

**Using venv (Python 3.3+):**

.. code-block:: bash

   python -m venv ndp-env
   source ndp-env/bin/activate  # On Windows: ndp-env\Scripts\activate
   pip install ndp-ep

**Using conda:**

.. code-block:: bash

   conda create -n ndp-env python=3.11
   conda activate ndp-env
   pip install ndp-ep

**Using pipenv:**

.. code-block:: bash

   pipenv install ndp-ep
   pipenv shell