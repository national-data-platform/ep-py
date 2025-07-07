"""General dataset update functionality."""

from typing import Dict, Any
from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientDatasetUpdate(APIClientBase):
    """Extension of APIClientBase with general dataset update methods."""

    def update_general_dataset(
        self, dataset_id: str, data: Dict[str, Any], server: str = "local"
    ) -> Dict[str, Any]:
        """
        Update an existing general dataset by making a PUT request.

        Args:
            dataset_id: ID of the dataset to update.
            data: Data for updating the dataset. Can contain:
                - title: Optional human-readable title
                - notes: Optional description or notes
                - tags: Optional list of tags
                - groups: Optional list of groups
                - extras: Optional additional metadata
                - resources: Optional list of resources
            server: Specify 'local' or 'pre_ckan'. Defaults to 'local'.

        Returns:
            Response JSON data indicating success.

        Raises:
            ValueError: If the update fails.
        """
        url = f"{self.base_url}/dataset/{dataset_id}"
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

            if "Dataset not found" in error_detail:
                raise ValueError("Error updating dataset: Not found")
            else:
                raise ValueError(f"Error updating dataset: {error_detail}")

    def patch_general_dataset(
        self, dataset_id: str, data: Dict[str, Any], server: str = "local"
    ) -> Dict[str, Any]:
        """
        Partially update an existing general dataset by making a PATCH request.

        Only updates the fields that are provided, leaving others unchanged.

        Args:
            dataset_id: ID of the dataset to update.
            data: Data for partial update. Can contain:
                - name: Optional unique name for the dataset
                - title: Optional human-readable title
                - owner_org: Optional organization ID
                - notes: Optional description or notes
                - tags: Optional list of tags
                - groups: Optional list of groups
                - extras: Optional additional metadata (merged with existing)
                - resources: Optional list of resources
                - private: Optional whether the dataset is private
                - license_id: Optional license identifier
                - version: Optional version of the dataset
            server: Specify 'local' or 'pre_ckan'. Defaults to 'local'.

        Returns:
            Response JSON data indicating success.

        Raises:
            ValueError: If the update fails.
        """
        url = f"{self.base_url}/dataset/{dataset_id}"
        params = {"server": server}
        try:
            response = self.session.patch(url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)

            if "Dataset not found" in error_detail:
                raise ValueError("Error updating dataset: Not found")
            else:
                raise ValueError(f"Error updating dataset: {error_detail}")
