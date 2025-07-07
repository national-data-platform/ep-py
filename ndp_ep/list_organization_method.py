"""Organization listing functionality."""

from typing import List, Optional
from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientOrganizationList(APIClientBase):
    """Extension of APIClientBase with method to list organizations."""

    def list_organizations(
        self, name: Optional[str] = None, server: str = "global"
    ) -> List[str]:
        """
        List all organizations with optional name filtering and server selection.

        Args:
            name: Optional string to filter organizations by name.
            server: The CKAN server to query ('local', 'global', 'pre_ckan').
                   Defaults to 'global'.

        Returns:
            List of organization names.

        Raises:
            ValueError: If the retrieval fails.
        """
        url = f"{self.base_url}/organization"
        params = {"server": server}
        if name:
            params["name"] = name

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise ValueError(f"Error listing organizations: {error_detail}")
