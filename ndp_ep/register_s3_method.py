"""S3 link registration functionality."""

from typing import Dict, Any
from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientS3Register(APIClientBase):
    """Extension of APIClientBase with S3 link registration method."""

    def register_s3_link(
        self, data: Dict[str, Any], server: str = "local"
    ) -> Dict[str, Any]:
        """
        Register a new S3 link by making a POST request.

        Args:
            data: Data for the S3 link. Should contain:
                - resource_name: The unique name of the resource
                - resource_title: The title of the resource
                - owner_org: The ID of the organization
                - resource_s3: The S3 URL of the resource
                - notes: Optional additional notes
                - extras: Optional additional metadata
            server: Specify 'local' or 'pre_ckan'. Defaults to 'local'.

        Returns:
            Response JSON data with the link ID.

        Raises:
            ValueError: If the registration fails or organization
                       does not exist.
        """
        url = f"{self.base_url}/s3"
        params = {"server": server}
        try:
            response = self.session.post(url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            # Extract error details from response JSON
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)

            # Specific error for organization existence
            if "Organization does not exist" in error_detail:
                raise ValueError(
                    "Error creating S3 resource: Organization "
                    "(owner_org) does not exist"
                )
            # Reserved key conflict
            elif "Reserved key error" in error_detail:
                raise ValueError(
                    "Error creating S3 resource: Reserved key conflict."
                )
            # Invalid input handling
            elif "Invalid input" in error_detail:
                raise ValueError(f"Error creating S3 resource: {error_detail}")
            else:
                raise ValueError(f"Error creating S3 resource: {error_detail}")
