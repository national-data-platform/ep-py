"""URL resource update functionality."""

from typing import Dict, Any
from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientURLUpdate(APIClientBase):
    """Extension of APIClientBase with URL resource update method."""

    def update_url_resource(
        self, resource_id: str, data: Dict[str, Any], server: str = "local"
    ) -> Dict[str, Any]:
        """
        Update an existing URL resource by making a PUT request.

        Args:
            resource_id: ID of the resource to update.
            data: Data for updating the URL resource. Can contain:
                - resource_name: Optional unique name of the resource
                - resource_title: Optional title of the resource
                - owner_org: Optional ID of the organization
                - resource_url: Optional URL of the resource
                - file_type: Optional file type (stream, CSV, TXT, JSON, NetCDF)
                - notes: Optional additional notes
                - extras: Optional additional metadata
                - mapping: Optional mapping information
                - processing: Optional processing information
            server: Specify 'local' or 'pre_ckan'. Defaults to 'local'.

        Returns:
            Response JSON data indicating success.

        Raises:
            ValueError: If the update fails.
        """
        url = f"{self.base_url}/url/{resource_id}"
        params = {"server": server}
        try:
            response = self.session.put(url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)

            if "Resource not found" in error_detail:
                raise ValueError("Error updating URL resource: Not found")
            elif "Reserved key error" in error_detail:
                raise ValueError(
                    f"Error updating URL resource: {error_detail}"
                )
            elif "Invalid input" in error_detail:
                raise ValueError(
                    f"Error updating URL resource: {error_detail}"
                )
            else:
                raise ValueError(
                    f"Error updating URL resource: {error_detail}"
                )
