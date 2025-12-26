"""DataSpaces details retrieval functionality."""

from typing import Any, Dict

import requests

from .client_base import APIClientBase


class APIClientDSpacesDetails(APIClientBase):
    """A class to handle requests for DataSpaces connection details."""

    def get_dspaces_details(self) -> Dict[str, Any]:
        """
        Fetch DataSpaces connection details from the API.

        Returns:
            DataSpaces connection details including 'dspaces_enabled'
            and 'dspaces_url'.

        Raises:
            ValueError: If the API response contains an error or is unreachable.
        """
        endpoint = f"{self.base_url}/status/dspaces-details"
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise ValueError(
                f"Failed to fetch DataSpaces details: {http_err}"
            ) from http_err
        except requests.exceptions.RequestException as req_err:
            raise ValueError(
                "An error occurred while fetching DataSpaces "
                f"details: {req_err}"
            ) from req_err
        except ValueError as json_err:
            raise ValueError(
                "An error occurred while parsing DataSpaces "
                f"details: {json_err}"
            ) from json_err
