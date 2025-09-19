"""Tests for API version compatibility checking functionality."""

import warnings
from unittest.mock import patch

import pytest
import requests
import requests_mock

from ndp_ep.client_base import APIClientBase
from ndp_ep.version_config import (
    MINIMUM_API_VERSION,
    get_minimum_version,
    is_version_compatible,
    parse_version,
)


class TestVersionConfig:
    """Test cases for version configuration utilities."""

    def test_parse_version_valid(self):
        """Test parsing valid version strings."""
        assert parse_version("1.2.3") == (1, 2, 3)
        assert parse_version("0.1.0") == (0, 1, 0)
        assert parse_version("10.20.30") == (10, 20, 30)

    def test_parse_version_invalid_format(self):
        """Test parsing invalid version strings."""
        with pytest.raises(ValueError, match="Invalid version format"):
            parse_version("1.2")

        with pytest.raises(ValueError, match="Invalid version format"):
            parse_version("1.2.3.4")

        with pytest.raises(ValueError, match="Invalid version format"):
            parse_version("1.a.3")

        with pytest.raises(ValueError, match="Invalid version format"):
            parse_version("")

    def test_is_version_compatible_equal(self):
        """Test version compatibility with equal versions."""
        assert is_version_compatible("1.2.3", "1.2.3") is True

    def test_is_version_compatible_newer(self):
        """Test version compatibility with newer API version."""
        assert is_version_compatible("1.3.0", "1.2.3") is True
        assert is_version_compatible("2.0.0", "1.9.9") is True
        assert is_version_compatible("1.2.4", "1.2.3") is True

    def test_is_version_compatible_older(self):
        """Test version compatibility with older API version."""
        assert is_version_compatible("1.2.2", "1.2.3") is False
        assert is_version_compatible("1.1.9", "1.2.0") is False
        assert is_version_compatible("0.9.9", "1.0.0") is False

    def test_get_minimum_version(self):
        """Test getting minimum version."""
        assert get_minimum_version() == MINIMUM_API_VERSION


class TestAPIVersionChecking:
    """Test cases for API version checking in client initialization."""

    @pytest.fixture
    def mock_api_base(self):
        """Mock the base API URL for testing."""
        return "http://example.com"

    def test_version_check_compatible_version(self, mock_api_base):
        """Test version check with compatible API version."""
        with requests_mock.Mocker() as m:
            # Mock initial connection check
            m.get(mock_api_base, status_code=200)
            # Mock status endpoint with compatible version
            m.get(
                f"{mock_api_base}/status/",
                json={"version": "1.0.0"},
                status_code=200,
            )

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                client = APIClientBase(
                    base_url=mock_api_base, token="test-token"
                )

                assert client.api_version == "1.0.0"
                assert len(w) == 0  # No warnings should be issued

    def test_version_check_incompatible_version(self, mock_api_base):
        """Test version check with incompatible API version."""
        with requests_mock.Mocker() as m:
            # Mock initial connection check
            m.get(mock_api_base, status_code=200)
            # Mock status endpoint with older version
            m.get(
                f"{mock_api_base}/status/",
                json={"version": "0.0.1"},
                status_code=200,
            )

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                client = APIClientBase(
                    base_url=mock_api_base, token="test-token"
                )

                assert client.api_version == "0.0.1"
                assert len(w) == 1
                assert issubclass(w[0].category, UserWarning)
                assert "API version compatibility warning" in str(w[0].message)
                assert "0.0.1" in str(w[0].message)
                assert MINIMUM_API_VERSION in str(w[0].message)

    def test_version_check_missing_version_field(self, mock_api_base):
        """Test version check when version field is missing from status."""
        with requests_mock.Mocker() as m:
            # Mock initial connection check
            m.get(mock_api_base, status_code=200)
            # Mock status endpoint without version info
            m.get(
                f"{mock_api_base}/status/",
                json={"status": "healthy"},
                status_code=200,
            )

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                client = APIClientBase(
                    base_url=mock_api_base, token="test-token"
                )

                assert client.api_version is None
                assert len(w) == 1
                assert issubclass(w[0].category, UserWarning)
                assert "Could not determine API version" in str(w[0].message)

    def test_version_check_alternative_version_fields(self, mock_api_base):
        """Test version check with alternative version field names."""
        test_cases = [
            {"api_version": "1.1.0"},
            {"app_version": "1.2.0"},
        ]

        for version_data in test_cases:
            with requests_mock.Mocker() as m:
                # Mock initial connection check
                m.get(mock_api_base, status_code=200)
                # Mock status endpoint with alternative version field
                m.get(
                    f"{mock_api_base}/status/",
                    json=version_data,
                    status_code=200,
                )

                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    client = APIClientBase(
                        base_url=mock_api_base, token="test-token"
                    )

                    expected_version = list(version_data.values())[0]
                    assert client.api_version == expected_version
                    assert len(w) == 0  # Compatible versions

    def test_version_check_network_error(self, mock_api_base):
        """Test version check when status endpoint is unreachable."""
        with requests_mock.Mocker() as m:
            # Mock initial connection check
            m.get(mock_api_base, status_code=200)
            # Mock status endpoint with network error
            m.get(
                f"{mock_api_base}/status/",
                exc=requests.exceptions.ConnectionError,
            )

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                # Should not raise exception, just silently handle error
                client = APIClientBase(
                    base_url=mock_api_base, token="test-token"
                )

                assert client.api_version is None
                assert len(w) == 0  # Network errors are handled silently

    def test_version_check_http_error(self, mock_api_base):
        """Test version check when status endpoint returns HTTP error."""
        with requests_mock.Mocker() as m:
            # Mock initial connection check
            m.get(mock_api_base, status_code=200)
            # Mock status endpoint with HTTP error
            m.get(f"{mock_api_base}/status/", status_code=500)

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                # Should not raise exception, just silently handle error
                client = APIClientBase(
                    base_url=mock_api_base, token="test-token"
                )

                assert client.api_version is None
                assert len(w) == 0  # HTTP errors are handled silently

    def test_version_check_invalid_json(self, mock_api_base):
        """Test version check when status endpoint returns invalid JSON."""
        with requests_mock.Mocker() as m:
            # Mock initial connection check
            m.get(mock_api_base, status_code=200)
            # Mock status endpoint with invalid JSON
            m.get(f"{mock_api_base}/status/", text="invalid json")

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                # Should not raise exception, just silently handle error
                client = APIClientBase(
                    base_url=mock_api_base, token="test-token"
                )

                assert client.api_version is None
                assert len(w) == 0  # JSON errors are handled silently

    def test_version_check_with_username_password(self, mock_api_base):
        """Test version check when using username/password authentication."""
        with requests_mock.Mocker() as m:
            # Mock initial connection check
            m.get(mock_api_base, status_code=200)
            # Mock token endpoint
            m.post(
                f"{mock_api_base}/token",
                json={"access_token": "test-token"},
                status_code=200,
            )
            # Mock status endpoint
            m.get(
                f"{mock_api_base}/status/",
                json={"version": "1.0.0"},
                status_code=200,
            )

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                client = APIClientBase(
                    base_url=mock_api_base, username="user", password="pass"
                )

                assert client.api_version == "1.0.0"
                assert len(w) == 0

    def test_no_version_check_without_auth(self, mock_api_base):
        """Test that version check is not performed without authentication."""
        with requests_mock.Mocker() as m:
            # Mock initial connection check only
            m.get(mock_api_base, status_code=200)

            client = APIClientBase(base_url=mock_api_base)

            assert client.api_version is None
            assert client.token is None
            # Status endpoint should not have been called
            assert (
                len(
                    [req for req in m.request_history if "/status/" in req.url]
                )
                == 0
            )

    @patch("ndp_ep.version_config.MINIMUM_API_VERSION", "2.0.0")
    def test_version_check_with_different_minimum(self, mock_api_base):
        """Test version check with different minimum version."""
        with requests_mock.Mocker() as m:
            # Mock initial connection check
            m.get(mock_api_base, status_code=200)
            # Mock status endpoint with version below new minimum
            m.get(
                f"{mock_api_base}/status/",
                json={"version": "1.5.0"},
                status_code=200,
            )

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                client = APIClientBase(
                    base_url=mock_api_base, token="test-token"
                )

                assert client.api_version == "1.5.0"
                assert len(w) == 1
                assert "2.0.0" in str(w[0].message)
