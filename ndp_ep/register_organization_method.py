"""Organization registration functionality."""

from typing import Dict, Any
from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientOrganizationRegister(APIClientBase):
    """Extension of APIClientBase with organization registration method."""

    def register_organization(
        self, data: Dict[str, Any], server: str = "local"
    ) -> Dict[str, Any]:
        """
        Register a new organization by making a POST request.

        Args:
            data: Data for the organization. Should contain:
                - name: The unique name of the organization
                - title: The title of the organization
                - description: Optional description of the organization
            server: CKAN instance ("local" or "pre_ckan").
                   Defaults to "local".

        Returns:
            Response JSON data with the organization ID and message.

        Raises:
            ValueError: If the registration fails or name already exists.
        """
        url = f"{self.base_url}/organization"
        params = {"server": server}
        try:
            response = self.session.post(url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            # Retrieve the error detail if available, otherwise use the
            # error message
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)

            # Specific error for organization name existence
            if "Group name already exists in database" in error_detail:
                raise ValueError(
                    "Error creating organization: Organization name "
                    "already exists"
                )
            else:
                raise ValueError(
                    f"Error creating organization: {error_detail}"
                )
