"""Tests for DataSpaces details method in ep-py client."""

import pytest
import requests
import requests_mock

from ndp_ep import APIClient


class TestGetDSpacesDetails:
    """Test suite for get_dspaces_details method."""

    @pytest.fixture
    def client(self):
        """Create APIClient instance for testing."""
        return APIClient(base_url="http://localhost:8001")

    def test_get_dspaces_details_success(self, client):
        """Test successful retrieval of DataSpaces details."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://localhost:8001/status/dspaces-details",
                json={
                    "dspaces_enabled": True,
                    "dspaces_url": "http://localhost:8003",
                },
            )

            result = client.get_dspaces_details()

            assert result["dspaces_enabled"] is True
            assert result["dspaces_url"] == "http://localhost:8003"

    def test_get_dspaces_details_disabled(self, client):
        """Test DataSpaces details when disabled."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://localhost:8001/status/dspaces-details",
                json={
                    "dspaces_enabled": False,
                    "dspaces_url": "",
                },
            )

            result = client.get_dspaces_details()

            assert result["dspaces_enabled"] is False
            assert result["dspaces_url"] == ""

    def test_get_dspaces_details_http_error(self, client):
        """Test handling of HTTP errors."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://localhost:8001/status/dspaces-details",
                status_code=500,
                json={"detail": "Internal server error"},
            )

            with pytest.raises(ValueError) as exc_info:
                client.get_dspaces_details()

            assert "Failed to fetch DataSpaces details" in str(exc_info.value)

    def test_get_dspaces_details_connection_error(self, client):
        """Test handling of connection errors."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://localhost:8001/status/dspaces-details",
                exc=requests.exceptions.ConnectionError,
            )

            with pytest.raises(ValueError) as exc_info:
                client.get_dspaces_details()

            assert "An error occurred while fetching DataSpaces" in str(
                exc_info.value
            )
