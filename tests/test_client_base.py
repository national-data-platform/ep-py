"""Tests for the base API client functionality."""

import pytest
import requests
import requests_mock

from ndp_ep.client_base import APIClientBase


class TestAPIClientBase:
    """Test cases for APIClientBase class."""

    def test_ensure_protocol_adds_http_when_missing(self):
        """Test that _ensure_protocol adds http:// when missing."""
        url = "example.com"
        result = APIClientBase._ensure_protocol(url)
        assert result == "http://example.com"

    def test_ensure_protocol_keeps_existing_protocol(self):
        """Test that _ensure_protocol keeps existing protocol."""
        url = "https://example.com"
        result = APIClientBase._ensure_protocol(url)
        assert result == "https://example.com"

    def test_init_with_token(self):
        """Test initialization with token."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            client = APIClientBase(
                base_url="http://example.com", token="test-token"
            )
            assert client.token == "test-token"
            assert (
                client.session.headers["Authorization"] == "Bearer test-token"
            )

    def test_init_with_username_password(self):
        """Test initialization with username and password."""
        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/token",
                json={"access_token": "retrieved-token"},
                status_code=200,
            )
            client = APIClientBase(
                base_url="http://example.com", username="user", password="pass"
            )
            assert client.token == "retrieved-token"
            assert (
                client.session.headers["Authorization"]
                == "Bearer retrieved-token"
            )

    def test_init_with_both_token_and_credentials_raises_error(self):
        """Test that providing both token and credentials raises ValueError."""
        with pytest.raises(ValueError, match="Provide either a token"):
            APIClientBase(
                base_url="http://example.com",
                token="test-token",
                username="user",
                password="pass",
            )

    def test_init_without_auth_checks_api_availability(self):
        """Test initialization without auth checks API availability."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            client = APIClientBase(base_url="http://example.com")
            assert client.token is None

    def test_check_api_availability_connection_error(self):
        """Test _check_api_availability with connection error."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com", exc=requests.exceptions.ConnectionError
            )
            with pytest.raises(ValueError, match="Failed to connect"):
                APIClientBase(base_url="http://example.com")

    def test_check_api_availability_http_error(self):
        """Test _check_api_availability with HTTP error."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=500)
            with pytest.raises(
                ValueError, match="API connection check failed"
            ):
                APIClientBase(base_url="http://example.com")

    def test_check_api_availability_request_exception(self):
        """Test _check_api_availability with general request exception."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com",
                exc=requests.exceptions.RequestException("Test error"),
            )
            with pytest.raises(
                ValueError, match="An error occurred while attempting"
            ):
                APIClientBase(base_url="http://example.com")

    def test_get_token_success(self):
        """Test successful token retrieval."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            m.post(
                "http://example.com/token",
                json={"access_token": "new-token"},
                status_code=200,
            )
            client = APIClientBase(base_url="http://example.com")
            client.get_token("user", "pass")
            assert client.token == "new-token"
            assert (
                client.session.headers["Authorization"] == "Bearer new-token"
            )

    def test_get_token_no_access_token_in_response(self):
        """Test token retrieval when no access token in response."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            m.post("http://example.com/token", json={}, status_code=200)
            client = APIClientBase(base_url="http://example.com")
            with pytest.raises(ValueError, match="No access token received"):
                client.get_token("user", "pass")

    def test_get_token_connection_error(self):
        """Test token retrieval with connection error."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            m.post(
                "http://example.com/token",
                exc=requests.exceptions.ConnectionError,
            )
            client = APIClientBase(base_url="http://example.com")
            with pytest.raises(ValueError, match="Failed to connect"):
                client.get_token("user", "pass")

    def test_get_token_unauthorized(self):
        """Test token retrieval with 401 unauthorized."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            m.post("http://example.com/token", status_code=401)
            client = APIClientBase(base_url="http://example.com")
            with pytest.raises(
                ValueError, match="Invalid username or password"
            ):
                client.get_token("user", "pass")

    def test_get_token_http_error(self):
        """Test token retrieval with general HTTP error."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            m.post("http://example.com/token", status_code=500)
            client = APIClientBase(base_url="http://example.com")
            with pytest.raises(ValueError, match="HTTP error occurred"):
                client.get_token("user", "pass")

    def test_get_token_request_exception(self):
        """Test token retrieval with general request exception."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            m.post(
                "http://example.com/token",
                exc=requests.exceptions.RequestException("Test error"),
            )
            client = APIClientBase(base_url="http://example.com")
            with pytest.raises(
                ValueError, match="An error occurred while attempting"
            ):
                client.get_token("user", "pass")

    def test_base_url_strips_trailing_slash(self):
        """Test that base_url strips trailing slash."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            client = APIClientBase(base_url="http://example.com/")
            assert client.base_url == "http://example.com"
