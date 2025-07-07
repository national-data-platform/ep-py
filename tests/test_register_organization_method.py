"""Tests for organization registration functionality."""

import pytest
import requests_mock

from ndp_ep.register_organization_method import APIClientOrganizationRegister


class TestAPIClientOrganizationRegister:
    """Test cases for APIClientOrganizationRegister class."""

    @pytest.fixture
    def client(self):
        """Create a test client instance."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientOrganizationRegister(base_url="http://example.com")

    def test_register_organization_success(self, client):
        """Test successful organization registration."""
        org_data = {
            "name": "test_org",
            "title": "Test Organization",
            "description": "A test organization",
        }
        expected_response = {
            "id": "12345",
            "message": "Organization created successfully",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/organization",
                json=expected_response,
                status_code=201,
            )

            result = client.register_organization(org_data)

            assert result == expected_response
            # Verify the request was made with correct data and params
            assert m.last_request.json() == org_data
            assert m.last_request.qs == {"server": ["local"]}

    def test_register_organization_with_pre_ckan_server(self, client):
        """Test organization registration with pre_ckan server."""
        org_data = {"name": "test_org", "title": "Test Organization"}
        expected_response = {
            "id": "67890",
            "message": "Organization created successfully",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/organization",
                json=expected_response,
                status_code=201,
            )

            result = client.register_organization(org_data, server="pre_ckan")

            assert result == expected_response
            assert m.last_request.qs == {"server": ["pre_ckan"]}

    def test_register_organization_name_already_exists(self, client):
        """Test organization registration when name already exists."""
        org_data = {"name": "existing_org", "title": "Existing Organization"}
        error_response = {"detail": "Group name already exists in database"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/organization",
                json=error_response,
                status_code=400,
            )

            with pytest.raises(
                ValueError, match="Organization name already exists"
            ):
                client.register_organization(org_data)

    def test_register_organization_http_error_with_detail(self, client):
        """Test organization registration with HTTP error and detail."""
        org_data = {"name": "test_org", "title": "Test Organization"}
        error_response = {"detail": "Invalid organization data"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/organization",
                json=error_response,
                status_code=400,
            )

            with pytest.raises(
                ValueError,
                match="Error creating organization: Invalid organization data",
            ):
                client.register_organization(org_data)

    def test_register_organization_http_error_no_detail(self, client):
        """Test organization registration with HTTP error and no detail."""
        org_data = {"name": "test_org", "title": "Test Organization"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/organization",
                status_code=500,
                text="Internal Server Error",
            )

            with pytest.raises(
                ValueError, match="Error creating organization"
            ):
                client.register_organization(org_data)

    def test_register_organization_invalid_json_response(self, client):
        """Test organization registration with invalid JSON response."""
        org_data = {"name": "test_org", "title": "Test Organization"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/organization",
                text="Invalid JSON",
                status_code=400,
            )

            with pytest.raises(
                ValueError, match="Error creating organization"
            ):
                client.register_organization(org_data)

    def test_register_organization_minimal_data(self, client):
        """Test organization registration with minimal required data."""
        org_data = {"name": "minimal_org", "title": "Minimal Organization"}
        expected_response = {
            "id": "minimal123",
            "message": "Organization created successfully",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/organization",
                json=expected_response,
                status_code=201,
            )

            result = client.register_organization(org_data)

            assert result == expected_response
            assert m.last_request.json() == org_data

    def test_register_organization_with_optional_description(self, client):
        """Test organization registration with optional description."""
        org_data = {
            "name": "described_org",
            "title": "Described Organization",
            "description": "This organization has a description",
        }
        expected_response = {
            "id": "described123",
            "message": "Organization created successfully",
        }

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/organization",
                json=expected_response,
                status_code=201,
            )

            result = client.register_organization(org_data)

            assert result == expected_response
            assert m.last_request.json() == org_data

    def test_register_organization_default_server(self, client):
        """Test that register_organization uses local as default server."""
        org_data = {"name": "default_org", "title": "Default Organization"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/organization",
                json={"id": "123", "message": "Success"},
                status_code=201,
            )

            client.register_organization(org_data)

            assert m.last_request.qs == {"server": ["local"]}
