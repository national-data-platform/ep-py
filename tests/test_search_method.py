"""Tests for search functionality."""

import pytest
import requests_mock

from ndp_ep.search_method import APIClientSearch


class TestAPIClientSearch:
    """Test cases for APIClientSearch class."""

    @pytest.fixture
    def client(self):
        """Create a test client instance."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com", status_code=200)
            return APIClientSearch(base_url="http://example.com")

    def test_search_datasets_success(self, client):
        """Test successful dataset search."""
        expected_response = [
            {"id": "123", "name": "test_dataset", "title": "Test Dataset"}
        ]

        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/search",
                json=expected_response,
                status_code=200,
            )

            result = client.search_datasets(
                terms=["climate", "temperature"], server="global"
            )

            assert result == expected_response
            # Verify the request was made with correct parameters
            assert m.last_request.qs == {
                "terms": ["climate", "temperature"],
                "server": ["global"],
            }

    def test_search_datasets_with_keys(self, client):
        """Test dataset search with keys specified."""
        expected_response = []

        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/search",
                json=expected_response,
                status_code=200,
            )

            result = client.search_datasets(
                terms=["climate", "temperature"],
                keys=["title", None],
                server="local",
            )

            assert result == expected_response
            # Verify the request was made with correct parameters
            expected_params = {
                "terms": ["climate", "temperature"],
                "keys": ["title", "null"],
                "server": ["local"],
            }
            assert m.last_request.qs == expected_params

    def test_search_datasets_keys_length_mismatch(self, client):
        """Test search with mismatched terms and keys length."""
        with pytest.raises(ValueError, match="number of terms must match"):
            client.search_datasets(
                terms=["climate", "temperature"],
                keys=["title"],  # Only one key for two terms
            )

    def test_search_datasets_http_error(self, client):
        """Test search with HTTP error response."""
        error_response = {"detail": "Search failed"}

        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/search",
                json=error_response,
                status_code=400,
            )

            with pytest.raises(
                ValueError, match="Error searching for datasets: Search failed"
            ):
                client.search_datasets(terms=["test"])

    def test_search_datasets_http_error_no_detail(self, client):
        """Test search with HTTP error and no detail in response."""
        with requests_mock.Mocker() as m:
            m.get(
                "http://example.com/search",
                status_code=500,
                text="Internal Server Error",
            )

            with pytest.raises(
                ValueError, match="Error searching for datasets"
            ):
                client.search_datasets(terms=["test"])

    def test_advanced_search_success(self, client):
        """Test successful advanced search."""
        search_data = {
            "dataset_name": "climate_data",
            "resource_url": "http://example.com/data",
            "server": "local",
        }
        expected_response = [
            {"id": "456", "name": "climate_data", "title": "Climate Data"}
        ]

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/search",
                json=expected_response,
                status_code=200,
            )

            result = client.advanced_search(search_data)

            assert result == expected_response
            # Verify the request was made with correct JSON data
            assert m.last_request.json() == search_data

    def test_advanced_search_with_filter_list(self, client):
        """Test advanced search with filter list."""
        search_data = {
            "search_term": "climate,temperature",
            "filter_list": ["format:CSV", "owner_org:research"],
            "server": "global",
        }
        expected_response = []

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/search",
                json=expected_response,
                status_code=200,
            )

            result = client.advanced_search(search_data)

            assert result == expected_response
            assert m.last_request.json() == search_data

    def test_advanced_search_http_error(self, client):
        """Test advanced search with HTTP error response."""
        search_data = {"dataset_name": "test"}
        error_response = {"detail": "Advanced search failed"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/search",
                json=error_response,
                status_code=400,
            )

            with pytest.raises(
                ValueError,
                match="Error in advanced search: Advanced search failed",
            ):
                client.advanced_search(search_data)

    def test_advanced_search_http_error_no_detail(self, client):
        """Test advanced search with HTTP error and no detail in response."""
        search_data = {"dataset_name": "test"}

        with requests_mock.Mocker() as m:
            m.post(
                "http://example.com/search",
                status_code=500,
                text="Internal Server Error",
            )

            with pytest.raises(ValueError, match="Error in advanced search"):
                client.advanced_search(search_data)

    def test_search_datasets_default_server(self, client):
        """Test that search_datasets uses global as default server."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com/search", json=[], status_code=200)

            client.search_datasets(terms=["test"])

            assert m.last_request.qs == {
                "terms": ["test"],
                "server": ["global"],
            }

    def test_search_datasets_empty_terms(self, client):
        """Test search with empty terms list."""
        with requests_mock.Mocker() as m:
            m.get("http://example.com/search", json=[], status_code=200)

            result = client.search_datasets(terms=[])

            assert result == []
            # When terms is empty, requests doesn't include it in query string
            assert m.last_request.qs == {"server": ["global"]}
