"""Unified API Client combining all functionality."""

from .register_kafka_method import APIClientKafkaRegister
from .register_organization_method import APIClientOrganizationRegister
from .register_s3_method import APIClientS3Register
from .register_url_method import APIClientURLRegister
from .register_service_method import APIClientServiceRegister
from .register_dataset_method import APIClientDatasetRegister
from .list_organization_method import APIClientOrganizationList
from .search_method import APIClientSearch
from .update_kafka_method import APIClientKafkaUpdate
from .update_s3_method import APIClientS3Update
from .update_url_method import APIClientURLUpdate
from .update_dataset_method import APIClientDatasetUpdate
from .delete_organization_method import APIClientOrganizationDelete
from .delete_resource_method import APIClientResourceDelete
from .get_kafka_details_method import APIClientKafkaDetails
from .get_system_status_method import APIClientSystemStatus


class APIClient(
    APIClientKafkaRegister,
    APIClientOrganizationRegister,
    APIClientS3Register,
    APIClientURLRegister,
    APIClientServiceRegister,
    APIClientDatasetRegister,
    APIClientOrganizationList,
    APIClientSearch,
    APIClientKafkaUpdate,
    APIClientS3Update,
    APIClientURLUpdate,
    APIClientDatasetUpdate,
    APIClientOrganizationDelete,
    APIClientResourceDelete,
    APIClientKafkaDetails,
    APIClientSystemStatus,
):
    """
    Unified API Client with comprehensive functionality.

    This class combines all the individual API client mixins to provide
    a complete interface for interacting with the NDP EP API.

    Features:
    - Organization management (create, list, delete)
    - Resource registration (Kafka, S3, URL, Services, General datasets)
    - Resource updates (Kafka, S3, URL, General datasets)
    - Resource deletion (by ID and name)
    - Search functionality (simple and advanced)
    - System information (status, metrics, Kafka details, Jupyter details)
    - Authentication (token-based and username/password)

    Example:
        >>> client = APIClient(
        ...     base_url="https://api.example.com",
        ...     token="your-token"
        ... )
        >>> organizations = client.list_organizations()
        >>> results = client.search_datasets(["climate"], server="global")
    """

    pass
