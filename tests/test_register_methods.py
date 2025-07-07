"""Tests for all registration methods (Kafka, S3, URL, Service, Dataset)."""

import pytest
import requests_mock

from ndp_ep.register_kafka_method import APIClientKafkaRegister
from ndp_ep.register_s3_method import APIClientS3Register
from ndp_ep.register_url_method import APIClientURLRegister
from ndp_ep.register_service_method import APIClientServiceRegister
from ndp_ep.register_dataset_method import APIClientDatasetRegister


class TestAPIClientKafkaRegister:
    """Test cases for Kafka registration."""

    @pytest.fixture
    def client(self):
        """Create a test client instance."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientKafkaRegister(base_url="http://example.com")

    def test_register_kafka_topic_success(self, client):
        """Test successful Kafka topic registration."""
        kafka_data = {
            "dataset_name": "test_kafka",
            "dataset_title": "Test Kafka Topic",
            "owner_org": "test_org",
            "kafka_topic": "test_topic",
            "kafka_host": "kafka.example.com",
            "kafka_port": "9092",
        }
        expected_response = {"id": "kafka123"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/kafka",
                json=expected_response,
                status_code=201,
            )

            result = client.register_kafka_topic(kafka_data)

            assert result == expected_response
            assert m.last_request.json() == kafka_data
            assert m.last_request.qs == {"server": ["local"]}

    def test_register_kafka_topic_organization_not_exists(self, client):
        """Test Kafka registration when organization doesn't exist."""
        kafka_data = {
            "dataset_name": "test_kafka",
            "dataset_title": "Test Kafka Topic",
            "owner_org": "nonexistent_org",
            "kafka_topic": "test_topic",
            "kafka_host": "kafka.example.com",
            "kafka_port": "9092",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/kafka",
                json={"detail": "Organization does not exist"},
                status_code=400,
            )

            with pytest.raises(
                ValueError, match="Organization \\(owner_org\\) does not exist"
            ):
                client.register_kafka_topic(kafka_data)


class TestAPIClientS3Register:
    """Test cases for S3 registration."""

    @pytest.fixture
    def client(self):
        """Create a test client instance."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientS3Register(base_url="http://example.com")

    def test_register_s3_link_success(self, client):
        """Test successful S3 link registration."""
        s3_data = {
            "resource_name": "test_s3",
            "resource_title": "Test S3 Resource",
            "owner_org": "test_org",
            "resource_s3": "s3://bucket/file.csv",
        }
        expected_response = {"id": "s3123"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/s3",
                json=expected_response,
                status_code=201,
            )

            result = client.register_s3_link(s3_data)

            assert result == expected_response
            assert m.last_request.json() == s3_data

    def test_register_s3_link_reserved_key_error(self, client):
        """Test S3 registration with reserved key error."""
        s3_data = {
            "resource_name": "reserved_name",
            "resource_title": "Reserved Resource",
            "owner_org": "test_org",
            "resource_s3": "s3://bucket/file.csv",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/s3",
                json={"detail": "Reserved key error"},
                status_code=400,
            )

            with pytest.raises(ValueError, match="Reserved key conflict"):
                client.register_s3_link(s3_data)


class TestAPIClientURLRegister:
    """Test cases for URL registration."""

    @pytest.fixture
    def client(self):
        """Create a test client instance."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientURLRegister(base_url="http://example.com")

    def test_register_url_success(self, client):
        """Test successful URL resource registration."""
        url_data = {
            "resource_name": "test_url",
            "resource_title": "Test URL Resource",
            "owner_org": "test_org",
            "resource_url": "http://example.com/data.csv",
            "file_type": "CSV",
        }
        expected_response = {"id": "url123"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/url",
                json=expected_response,
                status_code=201,
            )

            result = client.register_url(url_data)

            assert result == expected_response
            assert m.last_request.json() == url_data

    def test_register_url_name_already_exists(self, client):
        """Test URL registration when name already exists."""
        url_data = {
            "resource_name": "existing_url",
            "resource_title": "Existing URL Resource",
            "owner_org": "test_org",
            "resource_url": "http://example.com/data.csv",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/url",
                json={"detail": "Group name already exists in database"},
                status_code=400,
            )

            with pytest.raises(ValueError, match="Name already exists"):
                client.register_url(url_data)


class TestAPIClientServiceRegister:
    """Test cases for Service registration."""

    @pytest.fixture
    def client(self):
        """Create a test client instance."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientServiceRegister(base_url="http://example.com")

    def test_register_service_success(self, client):
        """Test successful service registration."""
        service_data = {
            "service_name": "test_service",
            "service_title": "Test Service",
            "owner_org": "services",
            "service_url": "http://api.example.com",
            "service_type": "API",
        }
        expected_response = {"id": "service123"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/services",
                json=expected_response,
                status_code=201,
            )

            result = client.register_service(service_data)

            assert result == expected_response
            assert m.last_request.json() == service_data

    def test_register_service_invalid_owner_org(self, client):
        """Test service registration with invalid owner_org."""
        service_data = {
            "service_name": "test_service",
            "service_title": "Test Service",
            "owner_org": "wrong_org",
            "service_url": "http://api.example.com",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/services",
                json={"detail": "owner_org must be 'services'"},
                status_code=400,
            )

            with pytest.raises(
                ValueError, match="owner_org must be 'services'"
            ):
                client.register_service(service_data)

    def test_register_service_duplicate(self, client):
        """Test service registration with duplicate service."""
        service_data = {
            "service_name": "duplicate_service",
            "service_title": "Duplicate Service",
            "owner_org": "services",
            "service_url": "http://api.example.com",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/services",
                json={"detail": "Duplicate Service"},
                status_code=409,
            )

            with pytest.raises(
                ValueError,
                match="service with the given name or URL already exists",
            ):
                client.register_service(service_data)


class TestAPIClientDatasetRegister:
    """Test cases for general dataset registration."""

    @pytest.fixture
    def client(self):
        """Create a test client instance."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientDatasetRegister(base_url="http://example.com")

    def test_register_general_dataset_success(self, client):
        """Test successful general dataset registration."""
        dataset_data = {
            "name": "test_dataset",
            "title": "Test Dataset",
            "owner_org": "test_org",
            "notes": "A test dataset",
            "tags": ["test", "data"],
        }
        expected_response = {"id": "dataset123"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/dataset",
                json=expected_response,
                status_code=201,
            )

            result = client.register_general_dataset(dataset_data)

            assert result == expected_response
            assert m.last_request.json() == dataset_data

    def test_register_general_dataset_duplicate(self, client):
        """Test general dataset registration with duplicate name."""
        dataset_data = {
            "name": "duplicate_dataset",
            "title": "Duplicate Dataset",
            "owner_org": "test_org",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/dataset",
                json={"detail": "Duplicate Dataset"},
                status_code=409,
            )

            with pytest.raises(
                ValueError, match="dataset with the given name already exists"
            ):
                client.register_general_dataset(dataset_data)

    def test_register_general_dataset_server_error(self, client):
        """Test general dataset registration with server configuration error."""
        dataset_data = {
            "name": "test_dataset",
            "title": "Test Dataset",
            "owner_org": "test_org",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/dataset",
                json={"detail": "Server is not configured"},
                status_code=400,
            )

            with pytest.raises(
                ValueError, match="Server is not configured or unreachable"
            ):
                client.register_general_dataset(dataset_data)
