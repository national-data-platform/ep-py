# ndp-ep

[![CI](https://github.com/sci-ndp/ndp-ep-py/workflows/CI/badge.svg)](https://github.com/sci-ndp/ndp-ep-py/actions)
[![codecov](https://codecov.io/gh/sci-ndp/ndp-ep-py/branch/main/graph/badge.svg)](https://codecov.io/gh/sci-ndp/ndp-ep-py)
[![PyPI version](https://badge.fury.io/py/ndp-ep.svg)](https://badge.fury.io/py/ndp-ep)
[![Python versions](https://img.shields.io/pypi/pyversions/ndp-ep.svg)](https://pypi.org/project/ndp-ep/)

A Python client library for interacting with the NDP EP API. This library provides a simple and intuitive interface for managing datasets, organizations, resources, and services through the API.

## Features

- **Complete API Coverage**: Support for all API endpoints including Kafka topics, S3 resources, URL resources, organizations, and services
- **Authentication**: Token-based and username/password authentication
- **Search Functionality**: Advanced search capabilities across datasets and resources
- **Error Handling**: Comprehensive error handling with meaningful error messages
- **Type Hints**: Full type hint support for better IDE integration
- **Testing**: Extensive test coverage (>70%) with unit and integration tests

## Installation

```bash
pip install ndp-ep
```

## Quick Start

```python
from ndp_ep import APIClient

# Initialize client with token
client = APIClient(
    base_url="https://your-api-endpoint.com",
    token="your-access-token"
)

# Or with username/password
client = APIClient(
    base_url="https://your-api-endpoint.com",
    username="your-username",
    password="your-password"
)

# List organizations
organizations = client.list_organizations()
print(organizations)

# Search datasets
results = client.search_datasets(
    terms=["climate", "temperature"],
    server="global"
)

# Register a new organization
org_data = {
    "name": "my_organization",
    "title": "My Organization",
    "description": "A sample organization"
}
response = client.register_organization(org_data)

# Register a service
service_data = {
    "service_name": "user_auth_api",
    "service_title": "User Authentication API",
    "owner_org": "services",
    "service_url": "https://api.example.com/auth",
    "service_type": "API",
    "notes": "RESTful API for user authentication"
}
response = client.register_service(service_data)
```

## API Coverage

### Authentication
- Token-based authentication
- Username/password authentication

### Organizations
- `list_organizations()` - List all organizations
- `register_organization()` - Create new organization
- `delete_organization()` - Delete organization

### Datasets and Resources
- `search_datasets()` - Search datasets with advanced filters
- `advanced_search()` - Advanced search with POST method
- `register_url()` - Register URL resources
- `register_s3_link()` - Register S3 resources
- `register_kafka_topic()` - Register Kafka topics
- `register_general_dataset()` - Register general datasets
- `update_url_resource()` - Update URL resources
- `update_s3_resource()` - Update S3 resources
- `update_kafka_topic()` - Update Kafka topics
- `update_general_dataset()` - Update general datasets (PUT)
- `patch_general_dataset()` - Partially update general datasets (PATCH)
- `delete_resource_by_id()` - Delete resource by ID
- `delete_resource_by_name()` - Delete resource by name

### Services
- `register_service()` - Register new services

### System Information
- `get_kafka_details()` - Get Kafka connection details
- `get_system_status()` - Check system status
- `get_system_metrics()` - Get system metrics
- `get_jupyter_details()` - Get Jupyter connection details

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/sci-ndp/ndp-ep-py.git
cd ndp-ep-py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .
pip install -r requirements-dev.txt
```

### Running tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ndp_ep --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
```

### Code formatting and linting

```bash
# Format code
black ndp_ep tests

# Lint code
flake8 ndp_ep

# Type checking
mypy ndp_ep
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass and coverage is maintained
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v0.1.0
- Initial release
- Complete API coverage for all endpoints
- Authentication support (token and username/password)
- Search functionality
- Resource management (URL, S3, Kafka)
- Organization management
- Comprehensive testing suite