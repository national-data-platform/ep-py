"""S3 buckets management functionality."""

from typing import Any, Dict, List

from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientS3Buckets(APIClientBase):
    """Extension of APIClientBase with S3 buckets management methods."""

    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        List all S3 buckets.

        Returns:
            List of bucket information dictionaries.

        Raises:
            ValueError: If the request fails.
        """
        url = f"{self.base_url}/s3/buckets/"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise ValueError(f"Error listing S3 buckets: {error_detail}")

    def create_bucket(self, bucket_name: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Create a new S3 bucket.

        Args:
            bucket_name: Name of the bucket to create.
            **kwargs: Additional bucket configuration options.

        Returns:
            Response JSON data with bucket creation details.

        Raises:
            ValueError: If bucket creation fails.
        """
        url = f"{self.base_url}/s3/buckets/"
        data = {"bucket_name": bucket_name, **kwargs}
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise ValueError(f"Error creating S3 bucket: {error_detail}")

    def get_bucket_info(self, bucket_name: str) -> Dict[str, Any]:
        """
        Get information about a specific S3 bucket.

        Args:
            bucket_name: Name of the bucket to get info for.

        Returns:
            Bucket information dictionary.

        Raises:
            ValueError: If the request fails or bucket doesn't exist.
        """
        url = f"{self.base_url}/s3/buckets/{bucket_name}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            if response.status_code == 404:
                raise ValueError(f"S3 bucket '{bucket_name}' not found")
            raise ValueError(f"Error getting S3 bucket info: {error_detail}")

    def delete_bucket(self, bucket_name: str) -> Dict[str, Any]:
        """
        Delete an S3 bucket.

        Args:
            bucket_name: Name of the bucket to delete.

        Returns:
            Response JSON data confirming deletion.

        Raises:
            ValueError: If deletion fails or bucket doesn't exist.
        """
        url = f"{self.base_url}/s3/buckets/{bucket_name}"
        try:
            response = self.session.delete(url)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            if response.status_code == 404:
                raise ValueError(f"S3 bucket '{bucket_name}' not found")
            raise ValueError(f"Error deleting S3 bucket: {error_detail}")
