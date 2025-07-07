API Reference
=============

This section provides detailed documentation for all classes and methods in the ndp-ep library.

.. currentmodule:: ndp_ep

Main Client
-----------

.. autoclass:: APIClient
   :members:
   :inherited-members:
   :show-inheritance:

The main APIClient class provides access to all NDP EP functionality.

Example usage::

    from ndp_ep import APIClient
    
    client = APIClient(
        base_url="http://155.101.6.191:8003",
        token="your-token"
    )

Base Classes
------------

.. autoclass:: APIClientBase
   :members:
   :show-inheritance:

Organization Management
-----------------------

.. autoclass:: ndp_ep.register_organization_method.APIClientOrganizationRegister
   :members:
   :show-inheritance:

.. autoclass:: ndp_ep.list_organization_method.APIClientOrganizationList
   :members:
   :show-inheritance:

.. autoclass:: ndp_ep.delete_organization_method.APIClientOrganizationDelete
   :members:
   :show-inheritance:

Resource Registration
---------------------

.. autoclass:: ndp_ep.register_kafka_method.APIClientKafkaRegister
   :members:
   :show-inheritance:

.. autoclass:: ndp_ep.register_s3_method.APIClientS3Register
   :members:
   :show-inheritance:

.. autoclass:: ndp_ep.register_url_method.APIClientURLRegister
   :members:
   :show-inheritance:

.. autoclass:: ndp_ep.register_service_method.APIClientServiceRegister
   :members:
   :show-inheritance:

.. autoclass:: ndp_ep.register_dataset_method.APIClientDatasetRegister
   :members:
   :show-inheritance:

Resource Updates
----------------

.. autoclass:: ndp_ep.update_kafka_method.APIClientKafkaUpdate
   :members:
   :show-inheritance:

.. autoclass:: ndp_ep.update_s3_method.APIClientS3Update
   :members:
   :show-inheritance:

.. autoclass:: ndp_ep.update_url_method.APIClientURLUpdate
   :members:
   :show-inheritance:

.. autoclass:: ndp_ep.update_dataset_method.APIClientDatasetUpdate
   :members:
   :show-inheritance:

Search Functionality
--------------------

.. autoclass:: ndp_ep.search_method.APIClientSearch
   :members:
   :show-inheritance:

System Information
------------------

.. autoclass:: ndp_ep.get_kafka_details_method.APIClientKafkaDetails
   :members:
   :show-inheritance:

.. autoclass:: ndp_ep.get_system_status_method.APIClientSystemStatus
   :members:
   :show-inheritance:

Constants and Version
---------------------

.. autodata:: ndp_ep.__version__

.. autodata:: ndp_ep.__description__

Common Parameters
-----------------

Server Options
~~~~~~~~~~~~~~

Most methods accept a ``server`` parameter with these options:

- ``"local"``: Local CKAN instance
- ``"global"``: Global CKAN instance (default for searches)
- ``"pre_ckan"``: Pre-production CKAN instance

Authentication
~~~~~~~~~~~~~~

The client supports two authentication methods:

**Token-based (recommended)**::

    client = APIClient(base_url="...", token="your-token")

**Username/Password**::

    client = APIClient(base_url="...", username="user", password="pass")

Error Handling
--------------

All methods may raise ``ValueError`` with descriptive error messages for:

- Authentication failures
- Network connectivity issues  
- API validation errors
- Resource not found errors
- Server configuration errors

Example error handling::

    try:
        result = client.register_organization(org_data)
    except ValueError as e:
        if "already exists" in str(e):
            print("Organization name is taken")
        elif "Authentication failed" in str(e):
            print("Check your credentials")
        else:
            print(f"API error: {e}")