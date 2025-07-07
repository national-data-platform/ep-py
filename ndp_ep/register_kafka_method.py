"""Kafka topic registration functionality."""

from typing import Dict, Any
from requests.exceptions import HTTPError

from .client_base import APIClientBase


class APIClientKafkaRegister(APIClientBase):
    """Extension of APIClientBase with Kafka topic registration method."""

    def register_kafka_topic(
        self, data: Dict[str, Any], server: str = "local"
    ) -> Dict[str, Any]:
        """
        Register a new Kafka topic by making a POST request.

        Args:
            data: Data for the Kafka topic. Should contain:
                - dataset_name: The unique name of the dataset
                - dataset_title: The title of the dataset
                - owner_org: The ID of the organization
                - kafka_topic: The Kafka topic name
                - kafka_host: The Kafka host
                - kafka_port: The Kafka port
                - dataset_description: Optional description
                - extras: Optional additional metadata
                - mapping: Optional mapping information
                - processing: Optional processing information
            server: Specify 'local' or 'pre_ckan'. Defaults to 'local'.

        Returns:
            Response JSON data with the topic ID.

        Raises:
            ValueError: If the registration fails.
        """
        url = f"{self.base_url}/kafka"
        params = {"server": server}  # Send server as a query parameter

        try:
            response = self.session.post(url, json=data, params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            try:
                error_detail = response.json().get("detail", str(e))
            except Exception:
                error_detail = str(e)

            if "Organization does not exist" in error_detail:
                raise ValueError(
                    "Error creating Kafka dataset: Organization "
                    "(owner_org) does not exist"
                )
            else:
                raise ValueError(
                    f"Error creating Kafka dataset: {error_detail}"
                )
