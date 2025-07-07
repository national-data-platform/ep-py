"""Resource deletion functionality."""

from typing import Dict, Any
from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientResourceDelete(APIClientBase):
    """Extension of APIClientBase with resource deletion methods."""

    def delete_resource_by_id(
        self, resource_id: str, server: str = "local"
    ) -> Dict[str, Any]:
        """
        Delete a resource by its ID by making a DELETE request.

        Args:
            resource_id: ID of the resource to delete.
            server: Specify 'local' or 'pre_ckan'. Defaults to 'local'.

        Returns:
            Response JSON data indicating success.

        Raises:
            ValueError: If the deletion fails.
        """
        url = f"{self.base_url}/resource"
        params = {"resource_id": resource_id, "server": server}

        try:
            response = self.session.delete(url, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)

            if "Resource not found" in error_detail:
                raise ValueError("Error deleting resource: Not found")
            else:
                raise ValueError(f"Error deleting resource: {error_detail}")

    def delete_resource_by_name(
        self, resource_name: str, server: str = "local"
    ) -> Dict[str, Any]:
        """
        Delete a resource by its name by making a DELETE request.

        Args:
            resource_name: Name of the resource to delete.
            server: Specify 'local' or 'pre_ckan'. Defaults to 'local'.

        Returns:
            Response JSON data indicating success.

        Raises:
            ValueError: If the deletion fails.
        """
        url = f"{self.base_url}/resource/{resource_name}"
        params = {"server": server}

        try:
            response = self.session.delete(url, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)

            if "Resource not found" in error_detail:
                raise ValueError("Error deleting resource: Not found")
            else:
                raise ValueError(f"Error deleting resource: {error_detail}")
