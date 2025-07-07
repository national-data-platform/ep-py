"""Tests for error cases to complete coverage."""

import pytest
import requests_mock
from requests.exceptions import RequestException

from ndp_ep.api_client import APIClient


class TestErrorCases:
    """Test error cases across different methods."""

    @pytest.fixture
    def client(self):
        """Create a test client instance."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClient(base_url="http://example.com")

    def test_delete_organization_general_error(self, client):
        """Test organization deletion with general error."""
        with requests_mock.Mocker() as m:
            m.delete(
                "http://example.com/organization/test_org",
                json={"detail": "General error occurred"},
                status_code=500,
            )

            with pytest.raises(ValueError, match="General error occurred"):
                client.delete_organization("test_org")

    def test_delete_resource_by_id_not_found(self, client):
        """Test resource deletion by ID when not found."""
        with requests_mock.Mocker() as m:
            m.delete(
                "http://example.com/resource",
                json={"detail": "Resource not found"},
                status_code=404,
            )

            with pytest.raises(ValueError, match="Not found"):
                client.delete_resource_by_id("nonexistent")

    def test_delete_resource_by_name_general_error(self, client):
        """Test resource deletion by name with general error."""
        with requests_mock.Mocker() as m:
            m.delete(
                "http://example.com/resource/test_resource",
                json={"detail": "Database error"},
                status_code=500,
            )

            with pytest.raises(ValueError, match="Database error"):
                client.delete_resource_by_name("test_resource")

    def test_list_organizations_error(self, client):
        """Test list organizations with error."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/organization",
                json={"detail": "Server error"},
                status_code=500,
            )

            with pytest.raises(ValueError, match="Server error"):
                client.list_organizations()

    def test_update_kafka_topic_not_found(self, client):
        """Test Kafka topic update when not found."""
        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/kafka/nonexistent",
                json={"detail": "Kafka dataset not found"},
                status_code=404,
            )

            with pytest.raises(ValueError, match="Not found"):
                client.update_kafka_topic("nonexistent", {})

    def test_update_kafka_topic_general_error(self, client):
        """Test Kafka topic update with general error."""
        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/kafka/kafka123",
                json={"detail": "Update failed"},
                status_code=500,
            )

            with pytest.raises(ValueError, match="Update failed"):
                client.update_kafka_topic("kafka123", {})

    def test_update_s3_resource_not_found(self, client):
        """Test S3 resource update when not found."""
        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/s3/nonexistent",
                json={"detail": "S3 resource not found"},
                status_code=404,
            )

            with pytest.raises(ValueError, match="Not found"):
                client.update_s3_resource("nonexistent", {})

    def test_update_s3_resource_general_error(self, client):
        """Test S3 resource update with general error."""
        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/s3/s3123",
                json={"detail": "S3 update failed"},
                status_code=500,
            )

            with pytest.raises(ValueError, match="S3 update failed"):
                client.update_s3_resource("s3123", {})

    def test_update_url_resource_not_found(self, client):
        """Test URL resource update when not found."""
        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/url/nonexistent",
                json={"detail": "Resource not found"},
                status_code=404,
            )

            with pytest.raises(ValueError, match="Not found"):
                client.update_url_resource("nonexistent", {})

    def test_update_url_resource_invalid_input(self, client):
        """Test URL resource update with invalid input."""
        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/url/url123",
                json={"detail": "Invalid input provided"},
                status_code=400,
            )

            with pytest.raises(ValueError, match="Invalid input provided"):
                client.update_url_resource("url123", {})

    def test_update_url_resource_general_error(self, client):
        """Test URL resource update with general error."""
        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/url/url123",
                json={"detail": "Update failed"},
                status_code=500,
            )

            with pytest.raises(ValueError, match="Update failed"):
                client.update_url_resource("url123", {})

    def test_update_dataset_not_found(self, client):
        """Test dataset update when not found."""
        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/dataset/nonexistent",
                json={"detail": "Dataset not found"},
                status_code=404,
            )

            with pytest.raises(ValueError, match="Not found"):
                client.update_general_dataset("nonexistent", {})

    def test_patch_dataset_not_found(self, client):
        """Test dataset patch when not found."""
        with requests_mock.Mocker() as m:
            m.patch(
                "http://example.com/dataset/nonexistent",
                json={"detail": "Dataset not found"},
                status_code=404,
            )

            with pytest.raises(ValueError, match="Not found"):
                client.patch_general_dataset("nonexistent", {})

    def test_patch_dataset_general_error(self, client):
        """Test dataset patch with general error."""
        with requests_mock.Mocker() as m:
            m.patch(
                "http://example.com/dataset/dataset123",
                json={"detail": "Patch failed"},
                status_code=500,
            )

            with pytest.raises(ValueError, match="Patch failed"):
                client.patch_general_dataset("dataset123", {})

    def test_kafka_details_http_error(self, client):
        """Test Kafka details with HTTP error."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com/status/kafka-details", status_code=500)

            with pytest.raises(
                ValueError, match="Failed to fetch Kafka details"
            ):
                client.get_kafka_details()

    def test_kafka_details_request_exception(self, client):
        """Test Kafka details with request exception."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/status/kafka-details",
                exc=RequestException("Connection error"),
            )

            with pytest.raises(
                ValueError,
                match="An error occurred while fetching Kafka details",
            ):
                client.get_kafka_details()

    def test_system_status_http_error(self, client):
        """Test system status with HTTP error."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com/status/", status_code=500)

            with pytest.raises(
                ValueError, match="Failed to fetch system status"
            ):
                client.get_system_status()

    def test_system_metrics_request_exception(self, client):
        """Test system metrics with request exception."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/status/metrics",
                exc=RequestException("Network error"),
            )

            with pytest.raises(
                ValueError,
                match="An error occurred while fetching system metrics",
            ):
                client.get_system_metrics()

    def test_jupyter_details_http_error(self, client):
        """Test Jupyter details with HTTP error."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com/status/jupyter", status_code=500)

            with pytest.raises(
                ValueError, match="Failed to fetch Jupyter details"
            ):
                client.get_jupyter_details()

    def test_register_s3_invalid_input_error(self, client):
        """Test S3 registration with invalid input error."""
        s3_data = {
            "resource_name": "test_s3",
            "resource_title": "Test S3",
            "owner_org": "test_org",
            "resource_s3": "invalid_s3_url",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/s3",
                json={"detail": "Invalid input format"},
                status_code=400,
            )

            with pytest.raises(ValueError, match="Invalid input format"):
                client.register_s3_link(s3_data)

    def test_register_service_server_not_configured(self, client):
        """Test service registration with server not configured."""
        service_data = {
            "service_name": "test_service",
            "service_title": "Test Service",
            "owner_org": "services",
            "service_url": "http://test.com",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/services",
                json={"detail": "Server is not configured"},
                status_code=400,
            )

            with pytest.raises(
                ValueError, match="Server is not configured or unreachable"
            ):
                client.register_service(service_data)

    def test_register_service_general_error(self, client):
        """Test service registration with general error."""
        service_data = {
            "service_name": "test_service",
            "service_title": "Test Service",
            "owner_org": "services",
            "service_url": "http://test.com",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/services",
                json={"detail": "Unknown error"},
                status_code=500,
            )

            with pytest.raises(ValueError, match="Unknown error"):
                client.register_service(service_data)
