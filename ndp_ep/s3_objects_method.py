"""S3 objects management functionality."""

from typing import Any, Dict, List, Optional, Union

from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientS3Objects(APIClientBase):
    """Extension of APIClientBase with S3 objects management methods."""

    def list_objects(
        self, bucket_name: str, prefix: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List objects in an S3 bucket.

        Args:
            bucket_name: Name of the bucket to list objects from.
            prefix: Optional prefix to filter objects.

        Returns:
            List of object information dictionaries.

        Raises:
            ValueError: If the request fails.
        """
        url = f"{self.base_url}/s3/objects/{bucket_name}"
        params = {}
        if prefix:
            params["prefix"] = prefix

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise ValueError(f"Error listing S3 objects: {error_detail}")

    def upload_object(
        self,
        bucket_name: str,
        object_key: str,
        file_data: Union[bytes, Any],
        content_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload an object to an S3 bucket.

        Args:
            bucket_name: Name of the bucket to upload to.
            object_key: Key/name for the object in the bucket.
            file_data: Binary file data to upload.
            content_type: Optional content type for the object.

        Returns:
            Response JSON data with upload details.

        Raises:
            ValueError: If upload fails.
        """
        url = f"{self.base_url}/s3/objects/{bucket_name}"
        files: Dict[str, Any] = {"file": (object_key, file_data, content_type)}
        data = {"object_key": object_key}

        try:
            response = self.session.post(url, files=files, data=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise ValueError(f"Error uploading S3 object: {error_detail}")

    def download_object(self, bucket_name: str, object_key: str) -> bytes:
        """
        Download an object from an S3 bucket.

        Args:
            bucket_name: Name of the bucket containing the object.
            object_key: Key/name of the object to download.

        Returns:
            Binary content of the object.

        Raises:
            ValueError: If download fails or object doesn't exist.
        """
        url = f"{self.base_url}/s3/objects/{bucket_name}/{object_key}"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.content
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            if response.status_code == 404:
                raise ValueError(
                    f"S3 object '{object_key}' not found in bucket "
                    f"'{bucket_name}'"
                )
            raise ValueError(f"Error downloading S3 object: {error_detail}")

    def delete_object(
        self, bucket_name: str, object_key: str
    ) -> Dict[str, Any]:
        """
        Delete an object from an S3 bucket.

        Args:
            bucket_name: Name of the bucket containing the object.
            object_key: Key/name of the object to delete.

        Returns:
            Response JSON data confirming deletion.

        Raises:
            ValueError: If deletion fails or object doesn't exist.
        """
        url = f"{self.base_url}/s3/objects/{bucket_name}/{object_key}"

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
                raise ValueError(
                    f"S3 object '{object_key}' not found in bucket "
                    f"'{bucket_name}'"
                )
            raise ValueError(f"Error deleting S3 object: {error_detail}")

    def get_object_metadata(
        self, bucket_name: str, object_key: str
    ) -> Dict[str, Any]:
        """
        Get metadata for an S3 object.

        Args:
            bucket_name: Name of the bucket containing the object.
            object_key: Key/name of the object.

        Returns:
            Object metadata dictionary.

        Raises:
            ValueError: If the request fails or object doesn't exist.
        """
        url = f"{self.base_url}/s3/objects/{bucket_name}/{object_key}/metadata"

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
                raise ValueError(
                    f"S3 object '{object_key}' not found in bucket "
                    f"'{bucket_name}'"
                )
            raise ValueError(
                f"Error getting S3 object metadata: {error_detail}"
            )

    def generate_presigned_upload_url(
        self,
        bucket_name: str,
        object_key: str,
        expiration: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate a presigned URL for uploading an object.

        Args:
            bucket_name: Name of the bucket to upload to.
            object_key: Key/name for the object.
            expiration: Optional expiration time in seconds.

        Returns:
            Dictionary containing the presigned URL and form fields.

        Raises:
            ValueError: If URL generation fails.
        """
        url = (
            f"{self.base_url}/s3/objects/{bucket_name}/{object_key}/"
            "presigned-upload"
        )
        data = {}
        if expiration:
            data["expiration"] = expiration

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise ValueError(
                f"Error generating presigned upload URL: {error_detail}"
            )

    def generate_presigned_download_url(
        self,
        bucket_name: str,
        object_key: str,
        expiration: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate a presigned URL for downloading an object.

        Args:
            bucket_name: Name of the bucket containing the object.
            object_key: Key/name of the object.
            expiration: Optional expiration time in seconds.

        Returns:
            Dictionary containing the presigned URL.

        Raises:
            ValueError: If URL generation fails.
        """
        url = (
            f"{self.base_url}/s3/objects/{bucket_name}/{object_key}/"
            "presigned-download"
        )
        data = {}
        if expiration:
            data["expiration"] = expiration

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise ValueError(
                f"Error generating presigned download URL: {error_detail}"
            )
