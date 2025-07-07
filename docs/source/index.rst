NDP EP Python Client Library
=============================

**ndp-ep** is a Python client library for interacting with the National Data Platform (NDP) EP API.

Features
--------

* **Complete API Coverage**: Support for all API endpoints including Kafka topics, S3 resources, URL resources, organizations, and services
* **Authentication**: Token-based and username/password authentication  
* **Search Functionality**: Advanced search capabilities across datasets and resources
* **Error Handling**: Comprehensive error handling with meaningful error messages
* **Type Hints**: Full type hint support for better IDE integration
* **Testing**: Extensive test coverage (>89%) with unit and integration tests

Quick Start
-----------

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
   :caption: User Guide

   user_guide/organizations

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api_reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`