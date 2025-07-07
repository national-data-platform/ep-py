Working with Organizations
===========================

Organizations are the primary containers for datasets and resources in NDP EP. This guide covers how to create, manage, and work with organizations effectively.

What are Organizations?
------------------------

Organizations in NDP EP serve as:

- **Data containers**: Group related datasets and resources
- **Access control**: Manage permissions and visibility  
- **Collaboration units**: Teams can share and collaborate on data
- **Metadata organization**: Categorize data by department, project, or theme

Listing Organizations
---------------------

Before creating new organizations, it's helpful to see what already exists:

.. code-block:: python

   from ndp_ep import APIClient

   client = APIClient(
       base_url="http://155.101.6.191:8003",
       token="your-token"
   )

   # List all organizations from global server
   organizations = client.list_organizations(server="global")
   print(f"Found {len(organizations)} organizations")
   
   for org in organizations:
       print(f"- {org}")

Server Options
~~~~~~~~~~~~~~

Organizations can be listed from different servers:

.. code-block:: python

   # Local server
   local_orgs = client.list_organizations(server="local")
   
   # Global server (default)
   global_orgs = client.list_organizations(server="global")
   
   # Pre-production server
   pre_orgs = client.list_organizations(server="pre_ckan")

Filtering by Name
~~~~~~~~~~~~~~~~~

You can filter organizations by name:

.. code-block:: python

   # Find organizations with "research" in the name
   research_orgs = client.list_organizations(name="research", server="global")
   
   # Find organizations starting with "climate"
   climate_orgs = client.list_organizations(name="climate", server="global")

Creating Organizations
----------------------

Basic Organization Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   org_data = {
       "name": "my_research_lab",           # Required: unique, lowercase, no spaces
       "title": "My Research Laboratory",   # Required: human-readable name
       "description": "A research lab focusing on climate data analysis"  # Optional
   }

   try:
       result = client.register_organization(org_data, server="local")
       print(f"✅ Organization created with ID: {result['id']}")
       print(f"📝 Message: {result['message']}")
   except ValueError as e:
       print(f"❌ Error creating organization: {e}")

Naming Guidelines
~~~~~~~~~~~~~~~~~

**Organization Name Requirements:**

- Must be unique across the server
- Use lowercase letters, numbers, and underscores only
- No spaces or special characters
- Should be descriptive but concise
- Cannot be changed after creation

**Good Examples:**

.. code-block:: python

   # Good organization names
   good_names = [
       "climate_research_center",
       "university_data_lab", 
       "weather_monitoring_dept",
       "ocean_science_institute",
       "ai_research_group"
   ]

**Bad Examples:**

.. code-block:: python

   # Avoid these patterns
   bad_names = [
       "Climate Research Center",  # Contains spaces and capitals
       "my-org",                  # Contains hyphens
       "org@university.edu",      # Contains special characters
       "123",                     # Too generic
       "a"                        # Too short
   ]

Advanced Organization Management
--------------------------------

Creating Organizations with Rich Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   comprehensive_org = {
       "name": "comprehensive_climate_hub",
       "title": "Comprehensive Climate Data Hub",
       "description": """
       A collaborative platform for climate researchers worldwide.
       
       This organization hosts datasets from:
       - Temperature monitoring stations
       - Precipitation measurement networks  
       - Satellite imagery and remote sensing data
       - Climate model outputs and projections
       
       Contact: climate-data@university.edu
       """
   }

   result = client.register_organization(comprehensive_org, server="local")

Organization Hierarchies
~~~~~~~~~~~~~~~~~~~~~~~~~

While NDP EP doesn't support nested organizations directly, you can use naming conventions to create logical hierarchies:

.. code-block:: python

   # University structure
   university_orgs = [
       {
           "name": "university_main",
           "title": "University Main Campus",
           "description": "Main university data repository"
       },
       {
           "name": "university_physics_dept", 
           "title": "University Physics Department",
           "description": "Physics department research data"
       },
       {
           "name": "university_climate_lab",
           "title": "University Climate Research Lab", 
           "description": "Climate lab within physics department"
       }
   ]

   for org in university_orgs:
       try:
           result = client.register_organization(org, server="local")
           print(f"✅ Created: {org['title']}")
       except ValueError as e:
           print(f"❌ Failed to create {org['title']}: {e}")

Deleting Organizations
----------------------

.. warning::
   Deleting an organization will also remove all associated datasets and resources. This operation cannot be undone.

Basic Deletion
~~~~~~~~~~~~~~

.. code-block:: python

   try:
       result = client.delete_organization("old_organization", server="local")
       print(f"✅ Organization deleted successfully")
   except ValueError as e:
       if "not found" in str(e).lower():
           print("❌ Organization not found")
       else:
           print(f"❌ Error deleting organization: {e}")

Safe Deletion with Confirmation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def safe_delete_organization(client, org_name, server="local"):
       """Safely delete an organization with confirmation."""
       
       # First, check if organization exists
       try:
           orgs = client.list_organizations(server=server)
           if org_name not in orgs:
               print(f"❌ Organization '{org_name}' not found")
               return False
       except Exception as e:
           print(f"❌ Error checking organization: {e}")
           return False
       
       # Get user confirmation
       confirmation = input(f"⚠️  Delete organization '{org_name}'? (yes/no): ")
       if confirmation.lower() != 'yes':
           print("🚫 Deletion cancelled")
           return False
       
       # Perform deletion
       try:
           result = client.delete_organization(org_name, server=server)
           print(f"✅ Organization '{org_name}' deleted successfully")
           return True
       except ValueError as e:
           print(f"❌ Error deleting organization: {e}")
           return False

   # Usage
   safe_delete_organization(client, "test_organization")

Best Practices
--------------

Naming Conventions
~~~~~~~~~~~~~~~~~~

**Use consistent prefixes:**

.. code-block:: python

   # By department
   department_orgs = [
       "dept_physics",
       "dept_chemistry", 
       "dept_biology"
   ]

   # By project
   project_orgs = [
       "proj_climate_2024",
       "proj_ocean_monitoring",
       "proj_ai_weather"
   ]

   # By data type
   data_type_orgs = [
       "data_sensors",
       "data_satellites",
       "data_models"
   ]

Organization Planning
~~~~~~~~~~~~~~~~~~~~~

Before creating organizations, consider:

1. **Purpose and scope**: What will this organization contain?
2. **Longevity**: Is this temporary or permanent?
3. **Collaboration**: Who will have access?
4. **Naming strategy**: How does it fit with existing organizations?
5. **Data governance**: What are the data management policies?

Bulk Operations
~~~~~~~~~~~~~~~

For creating multiple organizations:

.. code-block:: python

   def create_organizations_batch(client, org_configs, server="local"):
       """Create multiple organizations with error handling."""
       
       results = []
       
       for config in org_configs:
           try:
               result = client.register_organization(config, server=server)
               results.append({
                   "name": config["name"],
                   "status": "success",
                   "id": result["id"]
               })
               print(f"✅ Created: {config['title']}")
               
           except ValueError as e:
               results.append({
                   "name": config["name"], 
                   "status": "failed",
                   "error": str(e)
               })
               print(f"❌ Failed: {config['title']} - {e}")
       
       return results

   # Example usage
   research_organizations = [
       {
           "name": "marine_biology_lab",
           "title": "Marine Biology Laboratory",
           "description": "Research on marine ecosystems"
       },
       {
           "name": "atmospheric_science_dept",
           "title": "Atmospheric Science Department", 
           "description": "Weather and climate research"
       },
       {
           "name": "geophysics_institute",
           "title": "Geophysics Research Institute",
           "description": "Earth science and seismic monitoring"
       }
   ]

   # Create all organizations
   results = create_organizations_batch(client, research_organizations)
   
   # Summary
   successful = [r for r in results if r["status"] == "success"]
   failed = [r for r in results if r["status"] == "failed"]
   
   print(f"\n📊 Summary: {len(successful)} created, {len(failed)} failed")

Error Handling
~~~~~~~~~~~~~~

Common organization-related errors and how to handle them:

.. code-block:: python

   def handle_organization_errors(client, org_data, server="local"):
       """Demonstrate comprehensive error handling for organizations."""
       
       try:
           result = client.register_organization(org_data, server=server)
           return result
           
       except ValueError as e:
           error_msg = str(e).lower()
           
           if "already exists" in error_msg:
               print(f"❌ Organization name '{org_data['name']}' is already taken")
               # Suggest alternative names
               suggestions = [
                   f"{org_data['name']}_v2",
                   f"{org_data['name']}_new",
                   f"{org_data['name']}_2024"
               ]
               print(f"💡 Suggestions: {', '.join(suggestions)}")
               
           elif "authentication" in error_msg:
               print("❌ Authentication failed. Check your credentials.")
               
           elif "server is not configured" in error_msg:
               print(f"❌ Server '{server}' is not available or configured")
               print("💡 Try using 'local' or 'global' server")
               
           elif "invalid" in error_msg:
               print("❌ Invalid organization data")
               print("💡 Check that 'name' and 'title' are provided and valid")
               
           else:
               print(f"❌ Unexpected error: {e}")
               
           return None

Organization Validation
~~~~~~~~~~~~~~~~~~~~~~~

Validate organization data before creating:

.. code-block:: python

   import re

   def validate_organization_data(org_data):
       """Validate organization data before creation."""
       
       errors = []
       
       # Check required fields
       required_fields = ["name", "title"]
       for field in required_fields:
           if field not in org_data or not org_data[field]:
               errors.append(f"Missing required field: {field}")
       
       # Validate organization name
       if "name" in org_data:
           name = org_data["name"]
           
           # Check name format
           if not re.match(r'^[a-z0-9_]+, name):
               errors.append("Name must contain only lowercase letters, numbers, and underscores")
           
           # Check length
           if len(name) < 3:
               errors.append("Name must be at least 3 characters long")
           elif len(name) > 50:
               errors.append("Name must be less than 50 characters")
           
           # Check for reserved words
           reserved_words = ["admin", "api", "www", "test", "system"]
           if name in reserved_words:
               errors.append(f"Name '{name}' is reserved")
       
       # Validate title
       if "title" in org_data:
           title = org_data["title"]
           if len(title) < 3:
               errors.append("Title must be at least 3 characters long")
           elif len(title) > 100:
               errors.append("Title must be less than 100 characters")
       
       return errors

   # Usage example
   def create_validated_organization(client, org_data, server="local"):
       """Create organization with validation."""
       
       # Validate data
       errors = validate_organization_data(org_data)
       if errors:
           print("❌ Validation errors:")
           for error in errors:
               print(f"   - {error}")
           return None
       
       # Create organization
       return handle_organization_errors(client, org_data, server)

   # Example
   org_data = {
       "name": "validated_org_123",
       "title": "Validated Organization",
       "description": "This organization has been validated"
   }

   result = create_validated_organization(client, org_data)

Monitoring and Maintenance
--------------------------

Organization Audit
~~~~~~~~~~~~~~~~~~

Regularly audit your organizations:

.. code-block:: python

   def audit_organizations(client, servers=["local", "global"]):
       """Audit organizations across multiple servers."""
       
       print("🔍 Organization Audit Report")
       print("=" * 50)
       
       total_orgs = 0
       
       for server in servers:
           try:
               orgs = client.list_organizations(server=server)
               total_orgs += len(orgs)
               
               print(f"\n📊 Server: {server}")
               print(f"   Organizations: {len(orgs)}")
               
               # Analyze naming patterns
               prefixes = {}
               for org in orgs:
                   prefix = org.split('_')[0] if '_' in org else org[:5]
                   prefixes[prefix] = prefixes.get(prefix, 0) + 1
               
               print("   Top prefixes:")
               for prefix, count in sorted(prefixes.items(), 
                                         key=lambda x: x[1], reverse=True)[:5]:
                   print(f"     {prefix}: {count} organizations")
                   
           except Exception as e:
               print(f"❌ Error auditing {server}: {e}")
       
       print(f"\n📈 Total organizations across all servers: {total_orgs}")

   # Run audit
   audit_organizations(client)

Organization Health Check
~~~~~~~~~~~~~~~~~~~~~~~~~

Monitor organization health and usage:

.. code-block:: python

   def check_organization_health(client, org_name, server="local"):
       """Check the health and usage of an organization."""
       
       print(f"🏥 Health Check for '{org_name}'")
       print("-" * 40)
       
       # Check if organization exists
       try:
           orgs = client.list_organizations(server=server)
           if org_name not in orgs:
               print("❌ Organization not found")
               return False
           
           print("✅ Organization exists")
           
       except Exception as e:
           print(f"❌ Error checking organization: {e}")
           return False
       
       # Check for associated datasets (via search)
       try:
           # Search for datasets belonging to this organization
           search_results = client.advanced_search({
               "filter_list": [f"owner_org:{org_name}"],
               "server": server
           })
           
           dataset_count = len(search_results)
           print(f"📊 Associated datasets: {dataset_count}")
           
           if dataset_count == 0:
               print("⚠️  No datasets found - organization might be unused")
           else:
               print("✅ Organization is actively used")
               
               # Show sample datasets
               print("\n📋 Sample datasets:")
               for i, dataset in enumerate(search_results[:3]):
                   title = dataset.get('title', dataset.get('name', 'Untitled'))
                   resource_count = len(dataset.get('resources', []))
                   print(f"   {i+1}. {title} ({resource_count} resources)")
           
       except Exception as e:
           print(f"⚠️  Could not check datasets: {e}")
       
       return True

   # Example usage
   check_organization_health(client, "my_research_lab")

Migration and Backup
~~~~~~~~~~~~~~~~~~~~

Tools for organization migration:

.. code-block:: python

   def export_organization_config(client, org_name, server="local"):
       """Export organization configuration for backup or migration."""
       
       try:
           # Get organization list to verify existence
           orgs = client.list_organizations(server=server)
           if org_name not in orgs:
               print(f"❌ Organization '{org_name}' not found")
               return None
           
           # Create export data
           export_data = {
               "name": org_name,
               "server": server,
               "export_date": "2024-01-01",  # You'd use actual date
               "datasets": []
           }
           
           # Get associated datasets
           try:
               search_results = client.advanced_search({
                   "filter_list": [f"owner_org:{org_name}"],
                   "server": server
               })
               
               for dataset in search_results:
                   dataset_info = {
                       "id": dataset.get("id"),
                       "name": dataset.get("name"),
                       "title": dataset.get("title"),
                       "resources": len(dataset.get("resources", []))
                   }
                   export_data["datasets"].append(dataset_info)
                   
           except Exception as e:
               print(f"⚠️  Could not export datasets: {e}")
           
           return export_data
           
       except Exception as e:
           print(f"❌ Export failed: {e}")
           return None

   # Usage
   backup_data = export_organization_config(client, "my_research_lab")
   if backup_data:
       print(f"✅ Exported config for {backup_data['name']}")
       print(f"📊 Contains {len(backup_data['datasets'])} datasets")

Troubleshooting
---------------

Common Issues and Solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue: "Organization name already exists"**

Solution: Check existing organizations and choose a unique name:

.. code-block:: python

   def find_available_name(client, base_name, server="local"):
       """Find an available organization name based on a base name."""
       
       try:
           existing_orgs = client.list_organizations(server=server)
           
           # Try the base name first
           if base_name not in existing_orgs:
               return base_name
           
           # Try variations
           for i in range(2, 101):  # Try up to 100 variations
               variation = f"{base_name}_{i}"
               if variation not in existing_orgs:
                   return variation
           
           # If all variations are taken, suggest timestamp-based name
           import time
           timestamp_name = f"{base_name}_{int(time.time())}"
           return timestamp_name
           
       except Exception as e:
           print(f"Error finding available name: {e}")
           return None

   # Usage
   available_name = find_available_name(client, "research_lab")
   print(f"💡 Suggested name: {available_name}")

**Issue: "Server is not configured"**

Solution: Try different servers:

.. code-block:: python

   def find_working_server(client):
       """Find which servers are available."""
       
       servers = ["local", "global", "pre_ckan"]
       working_servers = []
       
       for server in servers:
           try:
               orgs = client.list_organizations(server=server)
               working_servers.append(server)
               print(f"✅ {server}: {len(orgs)} organizations")
           except Exception as e:
               print(f"❌ {server}: {e}")
       
       return working_servers

   # Check which servers work
   available_servers = find_working_server(client)
   print(f"\n💡 Available servers: {available_servers}")

Summary
-------

Organizations are fundamental to organizing your data in NDP EP. Key points to remember:

1. **Plan your organization structure** before creating
2. **Use consistent naming conventions** for better organization
3. **Validate data** before creation to avoid errors  
4. **Handle errors gracefully** with proper exception handling
5. **Monitor and audit** your organizations regularly
6. **Be careful with deletion** as it's irreversible

With proper organization management, you can create a well-structured, maintainable data platform that scales with your needs.