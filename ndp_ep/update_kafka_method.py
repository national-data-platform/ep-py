"""Kafka topic update functionality."""

from typing import Dict, Any
from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientKafkaUpdate(APIClientBase):
    """Extension of APIClientBase with Kafka topic update method."""

    def update_kafka_topic(
        self, dataset_id: str, data: Dict[str, Any], server: str = "local"
    ) -> Dict[str, Any]:
        """
        Update an existing Kafka topic by making a PUT request.

        Args:
            dataset_id: ID of the dataset to update.
            data: Data for updating the Kafka topic. Can contain:
                - dataset_name: Optional unique name of the dataset
                - dataset_title: Optional title of the dataset
                - owner_org: Optional ID of the organization
                - kafka_topic: Optional Kafka topic name
                - kafka_host: Optional Kafka host
                - kafka_port: Optional Kafka port
                - dataset_description: Optional description
                - extras: Optional additional metadata
                - mapping: Optional mapping information
                - processing: Optional processing information
            server: Specify 'local' or 'pre_ckan'. Defaults to 'local'.

        Returns:
            Response JSON data indicating success.

        Raises:
            ValueError: If the update fails.
        """
        url = f"{self.base_url}/kafka/{dataset_id}"
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

            if "Kafka dataset not found" in error_detail:
                raise ValueError("Error updating Kafka dataset: Not found")
            else:
                raise ValueError(
                    f"Error updating Kafka dataset: {error_detail}"
                )
