Authentication Guide
====================

The ndp-ep library supports multiple authentication methods to connect to the NDP EP API. This guide covers all available options and best practices.

Getting Your Credentials
-------------------------

Before you can authenticate, you need to obtain credentials from the National Data Platform:

1. Visit https://nationaldataplatform.org/
2. Create an account or log in to your existing account
3. Navigate to your user profile or settings
4. Find the API token section
5. Generate or copy your API token

.. note::
   Keep your API token secure and never share it publicly or commit it to version control.

Authentication Methods
----------------------

Token-Based Authentication (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The preferred method for authentication is using an API token:

.. code-block:: python

   from ndp_ep import APIClient

   client = APIClient(
       base_url="http://155.101.6.191:8003",
       token="your-api-token-here"
   )

**Advantages:**
- More secure than username/password
- Can be easily rotated
- Doesn't require storing passwords
- Better for automated scripts

Username/Password Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also authenticate using your username and password:

.. code-block:: python

   from ndp_ep import APIClient

   client = APIClient(
       base_url="http://155.101.6.191:8003",
       username="your-username",
       password="your-password"
   )

**When to use:**
- For interactive sessions
- When tokens are not available
- For testing purposes

.. warning::
   Username/password authentication requires the client to obtain a token from the server on initialization. This adds a network call during setup.

Environment Variables (Best Practice)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For production applications, store credentials in environment variables:

.. code-block:: python

   import os
   from ndp_ep import APIClient

   client = APIClient(
       base_url=os.getenv("NDP_API_URL", "http://155.101.6.191:8003"),
       token=os.getenv("NDP_API_TOKEN")
   )

Set your environment variables:

.. code-block:: bash

   # Linux/macOS
   export NDP_API_URL="http://155.101.6.191:8003"
   export NDP_API_TOKEN="your-token-here"

   # Windows
   set NDP_API_URL=http://155.101.6.191:8003
   set NDP_API_TOKEN=your-token-here

Using .env Files
~~~~~~~~~~~~~~~~

For local development, use a `.env` file with python-dotenv:

.. code-block:: bash

   pip install python-dotenv

Create a `.env` file:

.. code-block:: text

   NDP_API_URL=http://155.101.6.191:8003
   NDP_API_TOKEN=your-token-here

Load in your Python code:

.. code-block:: python

   import os
   from dotenv import load_dotenv
   from ndp_ep import APIClient

   # Load environment variables from .env file
   load_dotenv()

   client = APIClient(
       base_url=os.getenv("NDP_API_URL"),
       token=os.getenv("NDP_API_TOKEN")
   )

No Authentication (Limited Access)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some endpoints may work without authentication:

.. code-block:: python

   from ndp_ep import APIClient

   # This will work for public read-only endpoints
   client = APIClient(base_url="http://155.101.6.191:8003")

   # You can still perform searches and view public data
   results = client.search_datasets(["climate"], server="global")

Security Best Practices
------------------------

Token Management
~~~~~~~~~~~~~~~~

1. **Rotate tokens regularly**: Change your API tokens periodically
2. **Use different tokens for different environments**: Separate tokens for dev, staging, and production
3. **Revoke unused tokens**: Remove tokens that are no longer needed
4. **Monitor token usage**: Check for unauthorized access

Secure Storage
~~~~~~~~~~~~~~

.. code-block:: python

   # ✅ Good: Using environment variables
   token = os.getenv("NDP_API_TOKEN")
   
   # ✅ Good: Using secure configuration management
   from your_config_manager import get_secret
   token = get_secret("ndp_api_token")
   
   # ❌ Bad: Hardcoding in source code
   token = "abc123def456"  # Never do this!
   
   # ❌ Bad: Storing in plain text files
   with open("token.txt") as f:
       token = f.read()  # Avoid this

Network Security
~~~~~~~~~~~~~~~~

1. **Use HTTPS in production**: Always use secure connections
2. **Validate certificates**: Don't disable SSL verification
3. **Use VPNs for sensitive data**: Consider additional network security
4. **Monitor API access**: Log and monitor API usage

Error Handling
--------------

Handle authentication errors gracefully:

.. code-block:: python

   from ndp_ep import APIClient

   def create_authenticated_client():
       """Create an authenticated client with error handling."""
       try:
           client = APIClient(
               base_url=os.getenv("NDP_API_URL"),
               token=os.getenv("NDP_API_TOKEN")
           )
           
           # Test the connection
           status = client.get_system_status()
           print("✅ Authentication successful")
           return client
           
       except ValueError as e:
           if "Invalid username or password" in str(e):
               print("❌ Authentication failed: Invalid credentials")
           elif "No access token received" in str(e):
               print("❌ Authentication failed: No token received")
           else:
               print(f"❌ Authentication error: {e}")
           return None
           
       except ConnectionError:
           print("❌ Network error: Could not connect to API")
           return None
           
       except Exception as e:
           print(f"❌ Unexpected error: {e}")
           return None

   # Usage
   client = create_authenticated_client()
   if client:
       # Proceed with API operations
       pass

Troubleshooting
---------------

Common Authentication Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**"Authentication failed: Invalid username or password"**

- Check your username and password are correct
- Verify your account is active on the NDP platform
- Try logging in to the web interface first

**"Failed to connect to the API"**

- Check the API URL is correct and accessible
- Verify network connectivity
- Check firewall settings

**"No access token received"**

- The server response didn't include a token
- Check if your account has API access enabled
- Contact support if the issue persists

**Token-related errors**

- Verify the token is valid and not expired
- Check the token has the correct permissions
- Try generating a new token

Testing Authentication
~~~~~~~~~~~~~~~~~~~~~~

You can test your authentication setup:

.. code-block:: python

   def test_authentication():
       """Test different authentication methods."""
       
       # Test 1: Token authentication
       try:
           client = APIClient(
               base_url="http://155.101.6.191:8003",
               token=os.getenv("NDP_API_TOKEN")
           )
           client.get_system_status()
           print("✅ Token authentication: SUCCESS")
       except Exception as e:
           print(f"❌ Token authentication: FAILED - {e}")
       
       # Test 2: Search without authentication
       try:
           client = APIClient(base_url="http://155.101.6.191:8003")
           results = client.search_datasets(["test"], server="global")
           print(f"✅ Public access: SUCCESS - Found {len(results)} results")
       except Exception as e:
           print(f"❌ Public access: FAILED - {e}")

   test_authentication()

Configuration Examples
----------------------

Development Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # config/development.py
   import os
   from ndp_ep import APIClient

   def get_dev_client():
       return APIClient(
           base_url="http://155.101.6.191:8003",
           token=os.getenv("NDP_DEV_TOKEN")
       )

Production Configuration
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # config/production.py
   import os
   from ndp_ep import APIClient

   def get_prod_client():
       return APIClient(
           base_url=os.getenv("NDP_PROD_URL"),
           token=os.getenv("NDP_PROD_TOKEN")
       )

Docker Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: dockerfile

   FROM python:3.11-slim

   WORKDIR /app

   # Install dependencies
   RUN pip install ndp-ep

   # Environment variables will be passed at runtime
   ENV NDP_API_URL=""
   ENV NDP_API_TOKEN=""

   COPY app.py .

   CMD ["python", "app.py"]

Run with environment variables:

.. code-block:: bash

   docker run -e NDP_API_URL="http://155.101.6.191:8003" \
              -e NDP_API_TOKEN="your-token" \
              your-app:latest