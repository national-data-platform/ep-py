"""Tests for additional methods to improve coverage."""

import pytest
import requests_mock

from ndp_ep.delete_organization_method import APIClientOrganizationDelete
from ndp_ep.delete_resource_method import APIClientResourceDelete
from ndp_ep.list_organization_method import APIClientOrganizationList
from ndp_ep.update_kafka_method import APIClientKafkaUpdate
from ndp_ep.update_s3_method import APIClientS3Update
from ndp_ep.update_url_method import APIClientURLUpdate
from ndp_ep.update_dataset_method import APIClientDatasetUpdate
from ndp_ep.get_kafka_details_method import APIClientKafkaDetails
from ndp_ep.get_system_status_method import APIClientSystemStatus


class TestDeleteMethods:
    """Test deletion methods."""

    @pytest.fixture
    def delete_org_client(self):
        """Create delete organization client."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientOrganizationDelete(base_url="http://example.com")

    @pytest.fixture
    def delete_resource_client(self):
        """Create delete resource client."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientResourceDelete(base_url="http://example.com")

    def test_delete_organization_success(self, delete_org_client):
        """Test successful organization deletion."""
        with requests_mock.Mocker() as m:
            m.delete(
                "http://example.com/organization/test_org",
                json={"message": "Organization deleted successfully"},
                status_code=200,
            )

            result = delete_org_client.delete_organization("test_org")
            assert "deleted successfully" in result["message"]

    def test_delete_organization_not_found(self, delete_org_client):
        """Test organization deletion when not found."""
        with requests_mock.Mocker() as m:
            m.delete(
                "http://example.com/organization/nonexistent",
                json={"detail": "Organization not found"},
                status_code=404,
            )

            with pytest.raises(ValueError, match="Not found"):
                delete_org_client.delete_organization("nonexistent")

    def test_delete_resource_by_id_success(self, delete_resource_client):
        """Test successful resource deletion by ID."""
        with requests_mock.Mocker() as m:
            m.delete(
                "http://example.com/resource",
                json={"message": "Resource deleted successfully"},
                status_code=200,
            )

            result = delete_resource_client.delete_resource_by_id(
                "resource123"
            )
            assert "deleted successfully" in result["message"]

    def test_delete_resource_by_name_success(self, delete_resource_client):
        """Test successful resource deletion by name."""
        with requests_mock.Mocker() as m:
            m.delete(
                "http://example.com/resource/test_resource",
                json={"message": "Resource deleted successfully"},
                status_code=200,
            )

            result = delete_resource_client.delete_resource_by_name(
                "test_resource"
            )
            assert "deleted successfully" in result["message"]


class TestListMethods:
    """Test listing methods."""

    @pytest.fixture
    def list_client(self):
        """Create list client."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientOrganizationList(base_url="http://example.com")

    def test_list_organizations_with_name_filter(self, list_client):
        """Test listing organizations with name filter."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/organization",
                json=["test_org"],
                status_code=200,
            )

            result = list_client.list_organizations(name="test")
            assert result == ["test_org"]
            assert m.last_request.qs == {
                "server": ["global"],
                "name": ["test"],
            }


class TestUpdateMethods:
    """Test update methods."""

    @pytest.fixture
    def update_kafka_client(self):
        """Create update Kafka client."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientKafkaUpdate(base_url="http://example.com")

    @pytest.fixture
    def update_s3_client(self):
        """Create update S3 client."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientS3Update(base_url="http://example.com")

    @pytest.fixture
    def update_url_client(self):
        """Create update URL client."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientURLUpdate(base_url="http://example.com")

    @pytest.fixture
    def update_dataset_client(self):
        """Create update dataset client."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientDatasetUpdate(base_url="http://example.com")

    def test_update_kafka_topic_success(self, update_kafka_client):
        """Test successful Kafka topic update."""
        update_data = {"dataset_title": "Updated Title"}

        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/kafka/kafka123",
                json={"message": "Kafka dataset updated successfully"},
                status_code=200,
            )

            result = update_kafka_client.update_kafka_topic(
                "kafka123", update_data
            )
            assert "updated successfully" in result["message"]

    def test_update_s3_resource_success(self, update_s3_client):
        """Test successful S3 resource update."""
        update_data = {"resource_title": "Updated S3 Title"}

        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/s3/s3123",
                json={"message": "S3 resource updated successfully"},
                status_code=200,
            )

            result = update_s3_client.update_s3_resource("s3123", update_data)
            assert "updated successfully" in result["message"]

    def test_update_url_resource_success(self, update_url_client):
        """Test successful URL resource update."""
        update_data = {"resource_title": "Updated URL Title"}

        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/url/url123",
                json={"message": "Resource updated successfully"},
                status_code=200,
            )

            result = update_url_client.update_url_resource(
                "url123", update_data
            )
            assert "updated successfully" in result["message"]

    def test_update_url_resource_reserved_key_error(self, update_url_client):
        """Test URL resource update with reserved key error."""
        update_data = {"resource_name": "reserved_name"}

        with requests_mock.Mocker() as m:
            m.put(
                "http://example.com/url/url123",
                json={"detail": "Reserved key error"},
                status_code=400,
            )

            with pytest.raises(ValueError, match="Reserved key error"):
                update_url_client.update_url_resource("url123", update_data)

    def test_patch_general_dataset_success(self, update_dataset_client):
        """Test successful dataset patch."""
        patch_data = {"notes": "Updated notes"}

        with requests_mock.Mocker() as m:
            m.patch(
                "http://example.com/dataset/dataset123",
                json={"message": "Dataset updated successfully"},
                status_code=200,
            )

            result = update_dataset_client.patch_general_dataset(
                "dataset123", patch_data
            )
            assert "updated successfully" in result["message"]


class TestSystemMethods:
    """Test system information methods."""

    @pytest.fixture
    def kafka_client(self):
        """Create Kafka details client."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientKafkaDetails(base_url="http://example.com")

    @pytest.fixture
    def system_client(self):
        """Create system status client."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientSystemStatus(base_url="http://example.com")

    def test_get_kafka_details_success(self, kafka_client):
        """Test successful Kafka details retrieval."""
        expected_details = {
            "kafka_host": "kafka.example.com",
            "kafka_port": 9092,
            "kafka_connection": "active",
        }

        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/status/kafka-details",
                json=expected_details,
                status_code=200,
            )

            result = kafka_client.get_kafka_details()
            assert result == expected_details

    def test_get_system_status_success(self, system_client):
        """Test successful system status retrieval."""
        expected_status = {"status": "healthy", "services": {"ckan": "up"}}

        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/status/",
                json=expected_status,
                status_code=200,
            )

            result = system_client.get_system_status()
            assert result == expected_status

    def test_get_system_metrics_success(self, system_client):
        """Test successful system metrics retrieval."""
        expected_metrics = {"cpu_usage": 45.2, "memory_usage": 67.8}

        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/status/metrics",
                json=expected_metrics,
                status_code=200,
            )

            result = system_client.get_system_metrics()
            assert result == expected_metrics

    def test_get_jupyter_details_success(self, system_client):
        """Test successful Jupyter details retrieval."""
        expected_details = {"jupyter_url": "http://jupyter.example.com"}

        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/status/jupyter",
                json=expected_details,
                status_code=200,
            )

            result = system_client.get_jupyter_details()
            assert result == expected_details
