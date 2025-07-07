"""System status and metrics retrieval functionality."""

from typing import Dict, Any
import requests

from .client_base import APIClientBase


class APIClientSystemStatus(APIClientBase):
    """A class to handle requests for system status and metrics."""

    def get_system_status(self) -> Dict[str, Any]:
        """
        Check system status.

        Check if the CKAN and Keycloak servers are active and reachable.

        Returns:
            System status information.

        Raises:
            ValueError: If the API response contains an error or is unreachable.
        """
        endpoint = f"{self.base_url}/status/"
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise ValueError(
                f"Failed to fetch system status: {http_err}"
            ) from http_err
        except requests.exceptions.RequestException as req_err:
            raise ValueError(
                "An error occurred while fetching system " f"status: {req_err}"
            ) from req_err
        except ValueError as json_err:
            raise ValueError(
                "An error occurred while parsing system " f"status: {json_err}"
            ) from json_err

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Retrieve system metrics.

        Returns detailed system metrics and service status.

        Returns:
            Detailed system metrics and service status.

        Raises:
            ValueError: If the API response contains an error or is unreachable.
        """
        endpoint = f"{self.base_url}/status/metrics"
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise ValueError(
                f"Failed to fetch system metrics: {http_err}"
            ) from http_err
        except requests.exceptions.RequestException as req_err:
            raise ValueError(
                "An error occurred while fetching system "
                f"metrics: {req_err}"
            ) from req_err
        except ValueError as json_err:
            raise ValueError(
                "An error occurred while parsing system "
                f"metrics: {json_err}"
            ) from json_err

    def get_jupyter_details(self) -> Dict[str, Any]:
        """
        Get Jupyter connection details.

        Returns the URL where the JupyterHub is accessible.

        Returns:
            Jupyter connection details.

        Raises:
            ValueError: If the API response contains an error or is unreachable.
        """
        endpoint = f"{self.base_url}/status/jupyter"
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise ValueError(
                f"Failed to fetch Jupyter details: {http_err}"
            ) from http_err
        except requests.exceptions.RequestException as req_err:
            raise ValueError(
                "An error occurred while fetching Jupyter "
                f"details: {req_err}"
            ) from req_err
        except ValueError as json_err:
            raise ValueError(
                "An error occurred while parsing Jupyter "
                f"details: {json_err}"
            ) from json_err
