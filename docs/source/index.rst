NDP EP Python Client Library
=============================

**ndp-ep** is a Python client library for interacting with the National Data Platform (NDP) EP API.

🚀 Quick Start
--------------

**Try our interactive tutorials first!**

.. raw:: html

   <p>
   <a href="https://colab.research.google.com/github/sci-ndp/ndp-ep-py/blob/main/docs/source/tutorials/getting_started.ipynb" target="_blank">
   <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
   </a>
   <a href="https://mybinder.org/v2/gh/sci-ndp/ndp-ep-py/main?filepath=docs%2Fsource%2Ftutorials%2Fgetting_started.ipynb" target="_blank">
   <img src="https://mybinder.org/badge_logo.svg" alt="Binder"/>
   </a>
   </p>

The tutorial includes:

* 🔧 **Client setup and authentication** - Secure token configuration
* 🏢 **Working with organizations** - Create and manage data containers
* 🔍 **Searching datasets** - Simple and advanced search techniques  
* 📊 **Registering resources** - URL, S3, and Kafka topic registration
* 🛡️ **Error handling** - Best practices for robust applications
* 🎯 **Complete workflows** - End-to-end examples

Install and Basic Usage
-----------------------

Install the library:

.. code-block:: bash

   pip install ndp-ep

Basic usage:

.. code-block:: python

   from ndp_ep import APIClient

   # Initialize client with token
   client = APIClient(
       base_url="http://155.101.6.191:8003",
       token="your-access-token"
   )

   # List organizations
   organizations = client.list_organizations()
   print(organizations)

   # Search datasets
   results = client.search_datasets(
       terms=["climate", "temperature"],
       server="global"
   )

Features
--------

* **Complete API Coverage**: Support for all API endpoints including Kafka topics, S3 resources, URL resources, organizations, and services
* **Authentication**: Token-based and username/password authentication  
* **Search Functionality**: Advanced search capabilities across datasets and resources
* **Error Handling**: Comprehensive error handling with meaningful error messages
* **Type Hints**: Full type hint support for better IDE integration
* **Testing**: Extensive test coverage (>89%) with unit and integration tests

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart
   authentication

.. toctree::
   :maxdepth: 2
   :caption: Interactive Tutorials
   
   tutorials/getting_started
   tutorials/bulk_resource_management

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   user_guide/organizations

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api_reference

Learning Path
-------------

For the best learning experience, we recommend this path:

1. **📓 Start with the Interactive Tutorial** (:doc:`tutorials/getting_started`)
   
   * Run it in `Google Colab <https://colab.research.google.com/github/sci-ndp/ndp-ep-py/blob/main/docs/source/tutorials/getting_started.ipynb>`_ or `Binder <https://mybinder.org/v2/gh/sci-ndp/ndp-ep-py/main?filepath=docs%2Fsource%2Ftutorials%2Fgetting_started.ipynb>`_
   * Hands-on experience with live examples
   * Learn authentication and basic operations

2. **🔐 Set up Authentication** (:doc:`authentication`)
   
   * Get your API token
   * Configure secure authentication
   * Learn best practices

3. **🏢 Master Organizations** (:doc:`user_guide/organizations`)
   
   * Create and manage organizations
   * Learn naming conventions
   * Understand data organization

4. **📋 Explore the API Reference** (:doc:`api_reference`)
   
   * Complete method documentation
   * Advanced features and options
   * Error handling details

Advanced Tutorials
------------------

Ready for more? Explore advanced patterns and real-world scenarios:

**🚀 Bulk Resource Management** (:doc:`tutorials/bulk_resource_management`)

.. raw:: html

   <p>
   <a href="https://colab.research.google.com/github/sci-ndp/ndp-ep-py/blob/main/docs/source/tutorials/bulk_resource_management.ipynb" target="_blank">
   <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
   </a>
   <a href="https://mybinder.org/v2/gh/sci-ndp/ndp-ep-py/main?filepath=docs%2Fsource%2Ftutorials%2Fbulk_resource_management.ipynb" target="_blank">
   <img src="https://mybinder.org/badge_logo.svg" alt="Binder"/>
   </a>
   </p>

* Learn bulk operations, progress tracking, and complete cleanup workflows
* Create and manage hundreds of resources efficiently  
* Perfect for data migration, system setup, and testing environments
* Includes comprehensive error handling and performance monitoring

Quick Examples
--------------

**Search for datasets:**

.. code-block:: python

   # Simple search
   results = client.search_datasets(["climate"], server="global")
   
   # Advanced search with filters
   results = client.advanced_search({
       "search_term": "temperature,precipitation", 
       "filter_list": ["format:CSV"],
       "server": "global"
   })

**Create an organization:**

.. code-block:: python

   org_data = {
       "name": "my_research_lab",
       "title": "My Research Laboratory",
       "description": "Climate research data repository"
   }
   result = client.register_organization(org_data)

**Register a dataset:**

.. code-block:: python

   # URL resource
   url_data = {
       "resource_name": "climate_data_csv",
       "resource_title": "Climate Data",
       "owner_org": "my_research_lab",
       "resource_url": "https://example.com/climate.csv",
       "file_type": "CSV"
   }
   result = client.register_url(url_data)
   
   # S3 resource
   s3_data = {
       "resource_name": "large_dataset", 
       "resource_title": "Large Climate Dataset",
       "owner_org": "my_research_lab",
       "resource_s3": "s3://my-bucket/climate-data.parquet"
   }
   result = client.register_s3_link(s3_data)

**Bulk operations:**

.. code-block:: python

   # Create multiple services efficiently
   for i in range(1, 101):
       service_data = {
           "service_name": f"test_service_{i:03d}",
           "service_title": f"Test Service {i:03d}",
           "owner_org": "services",
           "service_url": f"https://api.example.com/service_{i:03d}",
           "service_type": "REST API"
       }
       result = client.register_service(service_data)
   
   # With progress tracking and cleanup
   # See the bulk management tutorial for complete examples

Community and Support
---------------------

* **📚 Documentation**: Complete guides and API reference
* **💻 GitHub**: `Source code and issues <https://github.com/sci-ndp/ndp-ep-py>`_
* **📦 PyPI**: `Package distribution <https://pypi.org/project/ndp-ep/>`_
* **🎓 Tutorials**: Interactive learning with live examples

Contributing
------------

We welcome contributions! See our `GitHub repository <https://github.com/sci-ndp/ndp-ep-py>`_ for:

* **🐛 Bug reports and feature requests** - Use GitHub Issues
* **🔧 Development setup** - Complete development guide  
* **🧪 Testing** - Comprehensive test suite
* **📝 Documentation** - Help improve our docs

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`