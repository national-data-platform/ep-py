"""Base class for the API client."""

import requests
from typing import Optional
from urllib.parse import urlparse


class APIClientBase:
    """Base class for the API client."""

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """
        Initialize the API client.

        Args:
            base_url: Base URL of the API.
            token: Access token for authentication.
            username: Username for authentication.
            password: Password for authentication.

        Raises:
            ValueError: If invalid authentication combination is provided
                       or if API is not reachable.
        """
        self.base_url = self._ensure_protocol(base_url).rstrip("/")
        self.session = requests.Session()

        # Initialize token to None by default
        self.token: Optional[str] = None

        # Validate input combinations
        if token and (username or password):
            raise ValueError(
                "Provide either a token or username/password, not both."
            )

        # Initialize with token if provided
        if token:
            self.token = token
            self.session.headers.update(
                {"Authorization": f"Bearer {self.token}"}
            )
        # Fallback to username/password authentication
        elif username and password:
            self.get_token(username, password)
        # Check API availability if no authentication details are provided
        else:
            self._check_api_availability()

    @staticmethod
    def _ensure_protocol(url: str) -> str:
        """
        Ensure the URL contains a valid protocol.

        If missing, prepend 'http://'.

        Args:
            url: The URL to validate.

        Returns:
            The URL with a protocol.
        """
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            return f"http://{url}"
        return url

    def _check_api_availability(self) -> None:
        """
        Check if the API is reachable.

        Makes a GET request to the base URL.

        Raises:
            ValueError: If the connection fails or response is not 200.
        """
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise ValueError(
                f"Failed to connect to the API at {self.base_url}. "
                "Please check if the URL is correct and reachable."
            )
        except requests.exceptions.HTTPError as http_err:
            raise ValueError(
                "API connection check failed with "
                f"status code {response.status_code}: {http_err}"
            )
        except requests.exceptions.RequestException as req_err:
            raise ValueError(
                "An error occurred while attempting to connect "
                f"to the API: {req_err}"
            )

    def get_token(self, username: str, password: str) -> None:
        """
        Obtain authentication token.

        Args:
            username: Username for authentication.
            password: Password for authentication.

        Raises:
            ValueError: If authentication fails or connection error occurs.
        """
        url = f"{self.base_url}/token"
        try:
            response = self.session.post(
                url, data={"username": username, "password": password}
            )
            response.raise_for_status()
            token_data = response.json()
            self.token = token_data.get("access_token")
            if not self.token:
                raise ValueError(
                    "Authentication failed: No access token received."
                )
            # Update session headers with the token
            self.session.headers.update(
                {"Authorization": f"Bearer {self.token}"}
            )
        except requests.exceptions.ConnectionError:
            raise ValueError(
                f"Failed to connect to the API at {self.base_url}. "
                "Please check if the URL is correct and reachable."
            )
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                raise ValueError(
                    "Authentication failed: Invalid username or password."
                ) from http_err
            else:
                raise ValueError(
                    f"HTTP error occurred: {http_err}"
                ) from http_err
        except requests.exceptions.RequestException as req_err:
            raise ValueError(
                "An error occurred while attempting to obtain "
                f"the token: {req_err}"
            ) from req_err
