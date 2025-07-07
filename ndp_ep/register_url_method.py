"""URL resource registration functionality."""

from typing import Dict, Any
from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientURLRegister(APIClientBase):
    """Extension of APIClientBase with URL resource registration method."""

    def register_url(
        self, data: Dict[str, Any], server: str = "local"
    ) -> Dict[str, Any]:
        """
        Register a new URL resource by making a POST request.

        Args:
            data: Data for the URL resource. Should contain:
                - resource_name: The unique name of the resource
                - resource_title: The title of the resource
                - owner_org: The ID of the organization
                - resource_url: The URL of the resource
                - file_type: Optional file type (stream, CSV, TXT, JSON, NetCDF)
                - notes: Optional additional notes
                - extras: Optional additional metadata
                - mapping: Optional mapping information
                - processing: Optional processing information
            server: Specify 'local' or 'pre_ckan'. Defaults to 'local'.

        Returns:
            Response JSON data with the resource ID.

        Raises:
            ValueError: If the registration fails.
        """
        url = f"{self.base_url}/url"
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
            if "Organization does not exist" in error_detail:
                raise ValueError(
                    "Error creating URL resource: Organization "
                    "(owner_org) does not exist."
                )
            elif "Group name already exists in database" in error_detail:
                raise ValueError(
                    "Error creating URL resource: Name already exists."
                )
            else:
                raise ValueError(
                    f"Error creating URL resource: {error_detail}"
                )
