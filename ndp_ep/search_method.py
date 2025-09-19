"""Search functionality for datasets."""

from typing import Any, Dict, List, Optional

from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientSearch(APIClientBase):
    """Extension of APIClientBase with search functionality for datasets."""

    def search_datasets(
        self,
        terms: List[str],
        keys: Optional[List[Optional[str]]] = None,
        server: str = "global",
    ) -> List[Dict[str, Any]]:
        """
        Search datasets by a list of terms with optional key specifications.

        Args:
            terms: A list of terms to search for in the datasets.
            keys: An optional list specifying the keys for each term.
                  Use None for a global search for the corresponding term.
            server: Specify the server to search on: 'local', 'global' or
                   'pre-ckan'.

        Returns:
            List of matching datasets.

        Raises:
            ValueError: If the search fails or validation fails.
        """
        # Ensure terms and keys lengths match, if keys are provided
        if keys is not None:
            if len(keys) != len(terms):
                raise ValueError(
                    "The number of terms must match the number of keys, "
                    "or keys must be omitted."
                )
            # Convert Python None to JSON null for the API
            processed_keys = [
                key if key is not None else "null" for key in keys
            ]
        else:
            processed_keys = None

        url = f"{self.base_url}/search"
        # Prepare the payload including optional keys
        payload = {"terms": terms, "server": server}
        if processed_keys:
            payload["keys"] = processed_keys

        try:
            response = self.session.get(url, params=payload)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            # Extract detailed error message from the API response if available
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise ValueError(f"Error searching for datasets: {error_detail}")

    def advanced_search(
        self, search_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Perform an advanced search using the POST /search endpoint.

        Args:
            search_data: A dict matching the 'SearchRequest' model,
                for example::

                    {
                        "dataset_name": "...",
                        "resource_url": "...",
                        "search_term": "...",
                        "filter_list": [...],
                        "server": "local"
                    }

        Returns:
            A list of matching datasets.

        Raises:
            ValueError: If the search or validation fails.
        """
        url = f"{self.base_url}/search"

        try:
            response = self.session.post(url, json=search_data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            error_detail = ""
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)
            raise ValueError(f"Error in advanced search: {error_detail}")
