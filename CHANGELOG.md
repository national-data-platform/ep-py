# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-07-03

### Added
- Initial release of ndp-ep Python client library
- Complete API coverage for all NDP EP endpoints
- Authentication support (token-based and username/password)
- Organization management (create, list, delete)
- Resource registration for multiple types:
  - Kafka topics
  - S3 resources  
  - URL resources
  - Services
  - General datasets
- Resource update functionality (PUT and PATCH operations)
- Resource deletion (by ID and name)
- Search functionality (simple and advanced)
- System information retrieval:
  - System status and health checks
  - System metrics
  - Kafka connection details
  - Jupyter connection details
- Comprehensive error handling with meaningful error messages
- Type hints throughout the codebase
- Extensive test suite with 89% code coverage
- CI/CD pipeline with GitHub Actions
- Automatic PyPI publishing on main branch
- Complete documentation and examples

### Technical Details
- Python 3.8+ support
- Built with requests library for HTTP operations
- Follows PEP 8 coding standards
- Modular architecture with mixin classes
- Comprehensive error handling and validation
- Mock-based testing with requests-mock
- Coverage reporting with pytest-cov
- Code formatting with black
- Linting with flake8
- Type checking with mypy

### API Endpoints Covered
- `/token` - Authentication
- `/organization` - Organization management
- `/kafka` - Kafka topic management
- `/s3` - S3 resource management
- `/url` - URL resource management
- `/services` - Service registration
- `/dataset` - General dataset management
- `/search` - Search functionality
- `/status/*` - System information
- `/resource` - Resource deletion

### Dependencies
- requests >= 2.25.0
- urllib3 >= 1.26.0

### Development Dependencies
- pytest >= 7.0.0
- pytest-cov >= 4.0.0
- pytest-mock >= 3.10.0
- requests-mock >= 1.9.0
- black >= 22.0.0
- flake8 >= 5.0.0
- mypy >= 1.0.0
- twine >= 4.0.0
- build >= 0.10.0
