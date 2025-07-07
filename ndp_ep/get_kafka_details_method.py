"""Kafka details retrieval functionality."""

from typing import Dict, Any
import requests

from .client_base import APIClientBase


class APIClientKafkaDetails(APIClientBase):
    """A class to handle requests for Kafka connection details."""

    def get_kafka_details(self) -> Dict[str, Any]:
        """
        Fetch Kafka connection details from the API.

        Returns:
            Kafka connection details including 'kafka_host', 'kafka_port',
            and 'kafka_connection'.

        Raises:
            ValueError: If the API response contains an error or is unreachable.
        """
        endpoint = f"{self.base_url}/status/kafka-details"
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            raise ValueError(
                f"Failed to fetch Kafka details: {http_err}"
            ) from http_err
        except requests.exceptions.RequestException as req_err:
            raise ValueError(
                "An error occurred while fetching Kafka " f"details: {req_err}"
            ) from req_err
        except ValueError as json_err:
            raise ValueError(
                "An error occurred while parsing Kafka " f"details: {json_err}"
            ) from json_err
