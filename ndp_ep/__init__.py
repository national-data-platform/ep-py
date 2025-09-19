"""
NDP EP Python Client Library.

A Python client library for interacting with the NDP EP API.
This library provides a simple and intuitive interface for managing
datasets, organizations, resources, and services through the API.
"""

from .api_client import APIClient
from .client_base import APIClientBase
from .delete_organization_method import APIClientOrganizationDelete
from .delete_resource_method import APIClientResourceDelete
from .get_kafka_details_method import APIClientKafkaDetails
from .get_system_status_method import APIClientSystemStatus
from .list_organization_method import APIClientOrganizationList
from .register_dataset_method import APIClientDatasetRegister
from .register_kafka_method import APIClientKafkaRegister
from .register_organization_method import APIClientOrganizationRegister
from .register_s3_method import APIClientS3Register
from .register_service_method import APIClientServiceRegister
from .register_url_method import APIClientURLRegister
from .search_method import APIClientSearch
from .update_dataset_method import APIClientDatasetUpdate
from .update_kafka_method import APIClientKafkaUpdate
from .update_s3_method import APIClientS3Update
from .update_url_method import APIClientURLUpdate

__version__ = "0.1.1"
__description__ = "Python client library for NDP EP API"

# Main exports
__all__ = [
    "APIClient",
    "APIClientBase",
    "__version__",
    "__description__",
]

# Default client for backward compatibility
Client = APIClient
