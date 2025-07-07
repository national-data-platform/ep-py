"""Service registration functionality."""

from typing import Dict, Any
from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientServiceRegister(APIClientBase):
    """Extension of APIClientBase with service registration method."""

    def register_service(
        self, data: Dict[str, Any], server: str = "local"
    ) -> Dict[str, Any]:
        """
        Register a new service by making a POST request.

        Args:
            data: Data for the service. Should contain:
                - service_name: Unique name for the service
                - service_title: Display title for the service
                - owner_org: Organization ID (must be 'services')
                - service_url: URL where the service is accessible
                - service_type: Optional type of service (API, Web Service, etc.)
                - notes: Optional description of the service
                - extras: Optional additional metadata
                - health_check_url: Optional URL for health check endpoint
                - documentation_url: Optional URL to service documentation
            server: Specify 'local' or 'pre_ckan'. Defaults to 'local'.

        Returns:
            Response JSON data with the service ID.

        Raises:
            ValueError: If the registration fails.
        """
        url = f"{self.base_url}/services"
        params = {"server": server}

        try:
            response = self.session.post(url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            # Extract error details if available
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)

            # Custom handling for common errors
            if "owner_org must be 'services'" in error_detail:
                raise ValueError(
                    "Error creating service: owner_org must be 'services' "
                    "for service registration"
                )
            elif "Server is not configured" in error_detail:
                raise ValueError(
                    "Error creating service: Server is not configured "
                    "or unreachable"
                )
            elif "Duplicate Service" in error_detail:
                raise ValueError(
                    "Error creating service: A service with the given "
                    "name or URL already exists"
                )
            else:
                raise ValueError(f"Error creating service: {error_detail}")
