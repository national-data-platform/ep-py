"""General dataset registration functionality."""

from typing import Dict, Any
from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientDatasetRegister(APIClientBase):
    """Extension of APIClientBase with general dataset registration method."""

    def register_general_dataset(
        self, data: Dict[str, Any], server: str = "local"
    ) -> Dict[str, Any]:
        """
        Register a new general dataset by making a POST request.

        Args:
            data: Data for the general dataset. Should contain:
                - name: Unique name for the dataset (lowercase, no spaces)
                - title: Human-readable title of the dataset
                - owner_org: Organization ID that owns this dataset
                - notes: Optional description or notes about the dataset
                - tags: Optional list of tags for categorizing the dataset
                - groups: Optional list of groups for the dataset
                - extras: Optional additional metadata as key-value pairs
                - resources: Optional list of resources associated with dataset
                - private: Optional whether the dataset is private (default: false)
                - license_id: Optional license identifier for the dataset
                - version: Optional version of the dataset
            server: Specify 'local' or 'pre_ckan'. Defaults to 'local'.

        Returns:
            Response JSON data with the dataset ID.

        Raises:
            ValueError: If the registration fails.
        """
        url = f"{self.base_url}/dataset"
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
            if "Server is not configured" in error_detail:
                raise ValueError(
                    "Error creating dataset: Server is not configured "
                    "or unreachable"
                )
            elif "Duplicate Dataset" in error_detail:
                raise ValueError(
                    "Error creating dataset: A dataset with the given "
                    "name already exists"
                )
            else:
                raise ValueError(f"Error creating dataset: {error_detail}")
