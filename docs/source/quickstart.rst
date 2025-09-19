Quick Start Guide
=================

This guide will help you get started with the ndp-ep library in just a few minutes.

🎯 Recommended: Interactive Tutorial
------------------------------------

**For the best learning experience, start with our interactive tutorial:**

.. raw:: html

   <p>
   <a href="https://colab.research.google.com/github/sci-ndp/ndp-ep-py/blob/main/docs/source/tutorials/getting_started.ipynb" target="_blank">
   <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
   </a>
   <a href="https://mybinder.org/v2/gh/sci-ndp/ndp-ep-py/main?filepath=docs%2Fsource%2Ftutorials%2Fgetting_started.ipynb" target="_blank">
   <img src="https://mybinder.org/badge_logo.svg" alt="Binder"/>
   </a>
   </p>

The interactive tutorial covers:

* **🔐 Secure Authentication Setup** - Learn to configure authentication safely
* **🏢 Organization Management** - Create and manage data containers
* **🔍 Dataset Search** - Simple and advanced search techniques
* **📊 Resource Registration** - Register URL, S3, and Kafka resources
* **🛡️ Error Handling** - Best practices for robust applications
* **🎯 Complete Workflows** - End-to-end real-world examples

.. note::
   The tutorial works completely in your browser and includes live, runnable code examples with real API interactions.

Basic Setup
-----------

1. **Install the library**:

   .. code-block:: bash

      pip install ndp-ep

2. **Get your API token**:
   
   - Visit https://nationaldataplatform.org/
   - Register for an account
   - Navigate to your profile to find your API token

3. **Import and initialize**:

   .. code-block:: python

      from ndp_ep import APIClient

      # Option 1: Using API token (recommended)
      client = APIClient(
          base_url="http://155.101.6.191:8003",
          token="your-api-token-here"
      )

      # Option 2: Using username/password
      client = APIClient(
          base_url="http://155.101.6.191:8003",
          username="your-username",
          password="your-password"
      )

.. tip::
   For a step-by-step guide on secure authentication setup, see our :doc:`tutorials/getting_started` notebook or the :doc:`authentication` guide.

First Steps
-----------

List Available Organizations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # List all organizations
   organizations = client.list_organizations()
   print("Available organizations:", organizations)

   # List organizations on a specific server
   local_orgs = client.list_organizations(server="local")
   global_orgs = client.list_organizations(server="global")

Search for Datasets
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Simple search
   results = client.search_datasets(
       terms=["climate", "weather"],
       server="global"
   )
   
   print(f"Found {len(results)} datasets")
   for dataset in results[:3]:  # Show first 3 results
       print(f"- {dataset.get('title', 'No title')}")

Check System Status
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Check if the system is healthy
   status = client.get_system_status()
   print("System status:", status)

   # Get detailed metrics
   metrics = client.get_system_metrics()
   print("System metrics:", metrics)

Creating Your First Organization
---------------------------------

.. code-block:: python

   # Define organization data
   org_data = {
       "name": "my_research_org",  # Must be lowercase, no spaces
       "title": "My Research Organization",
       "description": "An organization for my research projects"
   }

   try:
       # Create the organization
       result = client.register_organization(org_data)
       print(f"✓ Organization created with ID: {result['id']}")
   except ValueError as e:
       print(f"✗ Error creating organization: {e}")

.. note::
   For comprehensive organization management examples, check out the :doc:`tutorials/getting_started` notebook or the :doc:`user_guide/organizations` guide.

Registering Your First Dataset
-------------------------------

URL Resource
~~~~~~~~~~~~

.. code-block:: python

   url_data = {
       "resource_name": "climate_data_csv",
       "resource_title": "Climate Data CSV File",
       "owner_org": "my_research_org",  # Use your organization name
       "resource_url": "https://example.com/climate_data.csv",
       "file_type": "CSV",
       "notes": "Monthly climate data from weather stations"
   }

   try:
       result = client.register_url(url_data)
       print(f"✓ URL resource registered with ID: {result['id']}")
   except ValueError as e:
       print(f"✗ Error: {e}")

S3 Resource
~~~~~~~~~~~

.. code-block:: python

   s3_data = {
       "resource_name": "large_dataset_s3",
       "resource_title": "Large Dataset in S3",
       "owner_org": "my_research_org",
       "resource_s3": "s3://my-bucket/large-dataset.parquet",
       "notes": "Large dataset stored in S3 bucket"
   }

   try:
       result = client.register_s3_link(s3_data)
       print(f"✓ S3 resource registered with ID: {result['id']}")
   except ValueError as e:
       print(f"✗ Error: {e}")

Kafka Topic
~~~~~~~~~~~

.. code-block:: python

   kafka_data = {
       "dataset_name": "sensor_stream",
       "dataset_title": "Real-time Sensor Data Stream",
       "owner_org": "my_research_org",
       "kafka_topic": "sensor-data-topic",
       "kafka_host": "kafka.example.com",
       "kafka_port": "9092",
       "dataset_description": "Live sensor data from IoT devices"
   }

   try:
       result = client.register_kafka_topic(kafka_data)
       print(f"✓ Kafka topic registered with ID: {result['id']}")
   except ValueError as e:
       print(f"✗ Error: {e}")

.. tip::
   The :doc:`tutorials/getting_started` notebook includes working examples of all resource types with detailed explanations.

Advanced Search Example
-----------------------

.. code-block:: python

   # Advanced search with filters
   search_data = {
       "search_term": "climate,temperature,precipitation",
       "filter_list": [
           "format:CSV",
           "owner_org:research"
       ],
       "server": "global"
   }

   results = client.advanced_search(search_data)
   
   print(f"Advanced search found {len(results)} datasets")
   for dataset in results:
       print(f"- {dataset.get('title')}")
       print(f"  Organization: {dataset.get('organization', {}).get('title')}")
       print(f"  Resources: {len(dataset.get('resources', []))}")

Working with Services
---------------------

.. code-block:: python

   service_data = {
       "service_name": "weather_api",
       "service_title": "Weather Data API",
       "owner_org": "services",  # Must be 'services' for service registration
       "service_url": "https://api.weather.example.com",
       "service_type": "REST API",
       "notes": "RESTful API for weather data access",
       "health_check_url": "https://api.weather.example.com/health",
       "documentation_url": "https://docs.weather.example.com"
   }

   try:
       result = client.register_service(service_data)
       print(f"✓ Service registered with ID: {result['id']}")
   except ValueError as e:
       print(f"✗ Error: {e}")

Error Handling Best Practices
------------------------------

.. code-block:: python

   def safe_api_call(func, *args, **kwargs):
       """Wrapper for safe API calls with error handling."""
       try:
           return func(*args, **kwargs)
       except ValueError as e:
           print(f"API Error: {e}")
           return None
       except Exception as e:
           print(f"Unexpected error: {e}")
           return None

   # Example usage
   organizations = safe_api_call(client.list_organizations)
   if organizations:
       print(f"Found {len(organizations)} organizations")

Complete Example: Data Management Workflow
------------------------------------------

.. code-block:: python

   from ndp_ep import APIClient

   def main():
       # Initialize client
       client = APIClient(
           base_url="http://155.101.6.191:8003",
           token="your-token-here"
       )

       # 1. Check system health
       print("1. Checking system status...")
       status = client.get_system_status()
       print(f"   System is {'healthy' if status else 'not responding'}")

       # 2. List existing organizations
       print("\n2. Listing organizations...")
       orgs = client.list_organizations()
       print(f"   Found {len(orgs)} organizations")

       # 3. Search for existing datasets
       print("\n3. Searching for climate datasets...")
       results = client.search_datasets(["climate"], server="global")
       print(f"   Found {len(results)} climate-related datasets")

       # 4. Create organization (if needed)
       org_name = "demo_organization"
       if org_name not in orgs:
           print(f"\n4. Creating organization '{org_name}'...")
           org_data = {
               "name": org_name,
               "title": "Demo Organization",
               "description": "Demonstration organization for testing"
           }
           try:
               org_result = client.register_organization(org_data)
               print(f"   ✓ Organization created: {org_result['id']}")
           except ValueError as e:
               print(f"   ✗ Failed to create organization: {e}")

       # 5. Register a sample dataset
       print("\n5. Registering sample dataset...")
       dataset_data = {
           "resource_name": "sample_weather_data",
           "resource_title": "Sample Weather Data",
           "owner_org": org_name,
           "resource_url": "https://example.com/weather.csv",
           "file_type": "CSV",
           "notes": "Sample weather data for demonstration"
       }
       try:
           dataset_result = client.register_url(dataset_data)
           print(f"   ✓ Dataset registered: {dataset_result['id']}")
       except ValueError as e:
           print(f"   ✗ Failed to register dataset: {e}")

       print("\n✓ Workflow completed successfully!")

   if __name__ == "__main__":
       main()

Next Steps
----------

Now that you've seen the basics, explore more advanced features:

**📓 Interactive Learning:**
- **:doc:`tutorials/getting_started`** - Complete hands-on tutorial with live examples
- Run in `Google Colab <https://colab.research.google.com/github/sci-ndp/ndp-ep-py/blob/main/docs/source/tutorials/getting_started.ipynb>`_ or `Binder <https://mybinder.org/v2/gh/sci-ndp/ndp-ep-py/main?filepath=docs%2Fsource%2Ftutorials%2Fgetting_started.ipynb>`_

**📖 Detailed Guides:**
- **:doc:`authentication`** - Comprehensive authentication setup and security
- **:doc:`user_guide/organizations`** - Advanced organization management
- **:doc:`api_reference`** - Complete API documentation with all methods

**🔧 Development:**
- Explore our `GitHub repository <https://github.com/sci-ndp/ndp-ep-py>`_
- Check out the test suite for more usage examples
- Contribute to the project
