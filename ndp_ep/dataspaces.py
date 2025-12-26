"""
DataSpaces client wrapper for ep-py.

This module provides a thin wrapper around dxspaces.DXSpacesClient that
integrates with ep-api for service discovery. Install with:

    pip install ndp-ep[dataspaces]

Example usage:
    from ndp_ep import APIClient
    from ndp_ep.dataspaces import DataSpacesClient, TimeDirection

    # Option 1: Discover dspaces URL from ep-api
    api_client = APIClient(base_url="http://localhost:8001/demo")
    ds = DataSpacesClient.from_api_client(api_client)

    # Option 2: Direct connection with known URL
    ds = DataSpacesClient(dspaces_url="http://localhost:8003")

    # Use dxspaces functionality
    vars = ds.get_vars()
    arr = ds.get_ndarray("myvar", version=0, lb=(0, 0), ub=(10, 10))

    # Query array from registered datasets (requires api_client)
    results = ds.query_array(
        source="my_source",
        var_name="Rad",
        lb=(0, 0),
        ub=(100, 100),
        dataset_name="my_dataset",
        owner_org="my_org",
        timestamp=datetime.now(),
        time_direction=TimeDirection.PAST
    )
"""

from datetime import datetime
from enum import Enum
import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from dateutil import parser

# Lazy import check for dxspaces
try:
    from dxspaces import DXSpacesClient as _DXSpacesClient
    DXSPACES_AVAILABLE = True
except ImportError:
    _DXSpacesClient = None
    DXSPACES_AVAILABLE = False

if TYPE_CHECKING:
    from .api_client import APIClient


class TimeDirection(Enum):
    """Direction for time-based queries."""
    FUTURE = 1
    PAST = 2

    def __str__(self):
        if self == TimeDirection.FUTURE:
            return ">"
        else:
            return "<"


class StagingFailure(Exception):
    """Exception raised when staged data cannot be retrieved."""
    pass


_EXCLUDED_EXTRAS = ['staging_handle', 'staging_socket']


def _check_dxspaces_installed():
    """Raise ImportError with helpful message if dxspaces not installed."""
    if not DXSPACES_AVAILABLE:
        raise ImportError(
            "The 'dxspaces' package is required for DataSpaces functionality. "
            "Install it with: pip install ndp-ep[dataspaces]"
        )


def _time_arg_to_str(arg) -> str:
    """Convert a time argument to ISO format string."""
    if isinstance(arg, str):
        time = parser.isoparse(arg)
    elif isinstance(arg, datetime):
        time = arg
    else:
        raise ValueError("timestamp must be a datetime or a parseable datetime string")
    return time.strftime('%Y-%m-%dT%H:%M:%S')


def _get_query_time_string(**kwargs) -> Optional[str]:
    """Build a time query string from keyword arguments."""
    if 'timestamp' in kwargs:
        tstamp_str = _time_arg_to_str(kwargs['timestamp'])
        tstamp_direction = TimeDirection.FUTURE
        if 'time_direction' in kwargs:
            if not isinstance(kwargs['time_direction'], TimeDirection):
                raise ValueError("time_direction should be FUTURE or PAST")
            tstamp_direction = kwargs['time_direction']
        return f'{tstamp_direction}{tstamp_str}'
    time_string = None
    if 'start_time' in kwargs:
        time_string = _time_arg_to_str(kwargs['start_time']) + '/'
    if 'end_time' in kwargs:
        end_time_string = _time_arg_to_str(kwargs['end_time'])
        if time_string:
            time_string = time_string + end_time_string
        else:
            time_string = '/' + end_time_string
    return time_string


def _normalize_extras(extras: Any) -> Dict[str, Any]:
    """Normalize CKAN-style extras into a dict.

    ep-api / CKAN responses sometimes encode extras as either:
    - a dict: {"source": "...", "staging_handle": "...", ...}
    - a list of {"key": ..., "value": ...} dicts
    """
    if extras is None:
        return {}
    if isinstance(extras, dict):
        return extras
    if isinstance(extras, list):
        normalized: Dict[str, Any] = {}
        for item in extras:
            if not isinstance(item, dict):
                continue
            if "key" in item and "value" in item:
                normalized[item["key"]] = item["value"]
        return normalized
    return {}


def _get_data_from_staging(
    staging_handle: str,
    var_name: str,
    staging_socket: str,
    lb: Tuple[int, ...],
    ub: Tuple[int, ...],
    timestamp: str = None,
    staging_parameters: str = None,
    **kwargs
):
    """Retrieve data from DataSpaces staging.
    
    Parameters
    ----------
    staging_handle : str
        The namespace for DataSpaces queries (e.g., "ds_reg")
    var_name : str
        The variable name to retrieve
    staging_socket : str
        URL of the DataSpaces API
    lb : Tuple[int, ...]
        Lower bounds of the array slice
    ub : Tuple[int, ...]
        Upper bounds of the array slice
    timestamp : str, optional
        ISO timestamp string
    staging_parameters : str, optional
        JSON string with additional parameters (e.g., '{"id": "5"}')
    """
    # staging_handle is the namespace (e.g., "ds_reg")
    namespace = staging_handle
    
    # Build the variable name with parameters
    # Format: "var_name:Rad,id:5,url:..."
    name = f'var_name:{var_name}'
    
    if staging_parameters:
        try:
            params = json.loads(staging_parameters)
            for key, value in params.items():
                name = f'{name},{key}:{value}'
        except json.JSONDecodeError:
            pass
    
    client = _DXSpacesClient(staging_socket)
    data = client.GetNDArray(name=name, version=0, lb=lb, ub=ub, namespace=namespace)
    if data is None:
        raise StagingFailure(f"Registered data not found in staging. namespace={namespace}, name={name}")
    
    ts = parser.isoparse(timestamp) if timestamp else None
    return (data, ts)


def query_array(
    api_client: "APIClient",
    source: str,
    var_name: str,
    lb: Tuple[int, ...],
    ub: Tuple[int, ...],
    dataset_name: Optional[str] = None,
    dataset_title: Optional[str] = None,
    owner_org: Optional[str] = None,
    **kwargs
) -> List[Tuple]:
    """
    Download a subset of an array within a dataset previously registered as external data.

    This standalone function searches for datasets with the given source identifier that have
    staging metadata, then retrieves the requested array subset from DataSpaces.

    Parameters
    ----------
    api_client : APIClient
        An authenticated ep-py APIClient instance for searching datasets.
    source : str
        The name of the external source (stored in extras).
    var_name : str
        The name of the array variable to access.
    lb : Tuple[int, ...]
        The lower-bounds of array indices to access.
    ub : Tuple[int, ...]
        The upper-bounds of array indices to access.
    dataset_name : str, optional
        The name of the dataset.
    dataset_title : str, optional
        The title of the dataset.
    owner_org : str, optional
        The ID of the organization.
    timestamp : str or datetime, optional
        Find a result nearest in time to the given timestamp.
    time_direction : TimeDirection, optional
        Either `TimeDirection.FUTURE` or `TimeDirection.PAST`. If the former,
        and `timestamp` is given, then "nearest in time" looks forward in time;
        if the latter, backwards. Default behavior is forward-looking.
    start_time : str or datetime, optional
        The start of a time interval.
    end_time : str or datetime, optional
        The end of a time interval.

    Returns
    -------
    List[Tuple[NDArray, datetime, dict]]
        A list of tuples, one per matching dataset. Each tuple consists of:
        - The matching array subset
        - The timestamp of the dataset (or None)
        - A metadata dict for the dataset (extras without staging fields)

    Raises
    ------
    StagingFailure
        If the staged data cannot be retrieved.

    Example
    -------
    >>> from ndp_ep import APIClient
    >>> from ndp_ep.dataspaces import query_array, TimeDirection
    >>> client = APIClient(base_url="http://localhost:8001", token="...")
    >>> results = query_array(
    ...     api_client=client,
    ...     source="my_source",
    ...     var_name="Rad",
    ...     lb=(0, 0),
    ...     ub=(100, 100),
    ...     timestamp=datetime.now(),
    ...     time_direction=TimeDirection.PAST
    ... )
    """
    _check_dxspaces_installed()

    if len(lb) != len(ub):
        raise ValueError("lb and ub must have the same length")

    time_string = _get_query_time_string(**kwargs)
    filter_list = [f'source:{source}']

    # Build search payload
    search_data = {
        "filter_list": filter_list,
    }
    if dataset_name:
        search_data["dataset_name"] = dataset_name
    if dataset_title:
        search_data["dataset_title"] = dataset_title
    if owner_org:
        search_data["owner_org"] = owner_org
    if time_string:
        search_data["timestamp"] = time_string

    # Allow callers to specify which catalog backend to query
    server = kwargs.get("server")
    if server:
        search_data["server"] = server

    search_results = api_client.advanced_search(search_data)
    # Some catalog backends store timestamps but do not index them under a
    # top-level 'timestamp' field for search filtering. In that case, a
    # timestamp-constrained query can incorrectly return zero datasets.
    # Retry without the timestamp constraint to still allow staging fetch.
    if not search_results and "timestamp" in search_data:
        retry_data = dict(search_data)
        del retry_data["timestamp"]
        search_results = api_client.advanced_search(retry_data)

    results = []
    for result in search_results:
        extras = _normalize_extras(result.get('extras'))
        if extras:
            if 'staging_handle' in extras and 'staging_socket' in extras:
                data, timestamp_dt = _get_data_from_staging(
                    lb=lb,
                    ub=ub,
                    var_name=var_name,
                    **extras
                )
                # Remove staging fields from returned extras
                cleaned_extras = {
                    k: v for k, v in extras.items()
                    if k not in _EXCLUDED_EXTRAS
                }
                results.append((data, timestamp_dt, cleaned_extras))

    return results


class DataSpacesClient:
    """
    A thin wrapper around dxspaces.DXSpacesClient for ep-py integration.

    This class provides service discovery from ep-api and delegates all
    array operations to the underlying DXSpacesClient from dxspaces.

    Parameters
    ----------
    dspaces_url : str
        URL of the DataSpaces API (e.g., "http://localhost:8003")
    debug : bool, optional
        Enable debug output from dxspaces (default: False)
    """

    def __init__(self, dspaces_url: str, debug: bool = False, api_client: Optional["APIClient"] = None):
        _check_dxspaces_installed()
        self._url = dspaces_url
        self._debug = debug
        self._client = _DXSpacesClient(dspaces_url, debug=debug)
        self._api_client = api_client

    @classmethod
    def from_api_client(
        cls,
        api_client: "APIClient",
        debug: bool = False,
    ) -> "DataSpacesClient":
        """
        Create a DataSpacesClient by discovering the URL from ep-api.

        Parameters
        ----------
        api_client : APIClient
            An authenticated ep-py APIClient instance
        debug : bool, optional
            Enable debug output from dxspaces (default: False)

        Returns
        -------
        DataSpacesClient
            A configured DataSpacesClient instance

        Raises
        ------
        ValueError
            If DataSpaces is not enabled on the ep-api server
        """
        details = api_client.get_dspaces_details()
        if not details.get("dspaces_enabled"):
            raise ValueError(
                "DataSpaces is not enabled on this EP API server. "
                "Contact the server administrator to enable it."
            )
        dspaces_url = details.get("dspaces_url")
        if not dspaces_url:
            raise ValueError(
                "DataSpaces URL not configured on this EP API server."
            )
        return cls(dspaces_url=dspaces_url, debug=debug, api_client=api_client)

    @property
    def api_client(self) -> Optional["APIClient"]:
        """Return the associated APIClient, if any."""
        return self._api_client

    @property
    def url(self) -> str:
        """Return the DataSpaces API URL."""
        return self._url

    @property
    def client(self) -> "_DXSpacesClient":
        """Return the underlying dxspaces client for advanced usage."""
        return self._client

    # -------------------------------------------------------------------------
    # Delegated methods to dxspaces.DXSpacesClient
    # -------------------------------------------------------------------------

    def get_vars(self) -> List[str]:
        """
        Get list of variable names stored in DataSpaces.

        Returns
        -------
        List[str]
            List of variable names
        """
        return self._client.GetVars()

    def get_var_objs(self, name: str) -> List[Dict[str, Any]]:
        """
        Get objects for a specific variable.

        Parameters
        ----------
        name : str
            Variable name

        Returns
        -------
        List[Dict[str, Any]]
            List of object metadata for the variable
        """
        return self._client.GetVarObjs(name)

    def get_ndarray(
        self,
        name: str,
        version: int,
        lb: Tuple[int, ...],
        ub: Tuple[int, ...],
        namespace: Optional[str] = None,
    ):
        """
        Get a numpy ndarray from DataSpaces.

        Parameters
        ----------
        name : str
            Variable name
        version : int
            Version number
        lb : Tuple[int, ...]
            Lower bounds of the bounding box
        ub : Tuple[int, ...]
            Upper bounds of the bounding box
        namespace : str, optional
            Namespace for the variable

        Returns
        -------
        numpy.ndarray or None
            The requested array data, or None if not found
        """
        return self._client.GetNDArray(name, version, lb, ub, namespace)

    def put_ndarray(
        self,
        arr,
        name: str,
        version: int,
        offset: Tuple[int, ...],
        namespace: Optional[str] = None,
    ) -> None:
        """
        Store a numpy ndarray in DataSpaces.

        Parameters
        ----------
        arr : numpy.ndarray
            The array to store
        name : str
            Variable name
        version : int
            Version number
        offset : Tuple[int, ...]
            Offset for placement in the global array
        namespace : str, optional
            Namespace for the variable
        """
        self._client.PutNDArray(arr, name, version, offset, namespace)

    def register(
        self,
        type: str,
        name: str,
        data: Dict[str, Any],
    ):
        """
        Register an external data source.

        Parameters
        ----------
        type : str
            Type of the data source
        name : str
            Name for the registration
        data : Dict[str, Any]
            Registration data/parameters

        Returns
        -------
        RegistryHandle or None
            Handle for the registered data source
        """
        return self._client.Register(type, name, data)

    def query_array(
        self,
        source: str,
        var_name: str,
        lb: Tuple[int, ...],
        ub: Tuple[int, ...],
        dataset_name: Optional[str] = None,
        dataset_title: Optional[str] = None,
        owner_org: Optional[str] = None,
        **kwargs
    ) -> List[Tuple]:
        """
        Download a subset of an array within a dataset previously registered as external data.

        This method searches for datasets with the given source identifier that have
        staging metadata, then retrieves the requested array subset from DataSpaces.

        Parameters
        ----------
        source : str
            The name of the external source (stored in extras).
        var_name : str
            The name of the array variable to access.
        lb : Tuple[int, ...]
            The lower-bounds of array indices to access.
        ub : Tuple[int, ...]
            The upper-bounds of array indices to access.
        dataset_name : str, optional
            The name of the dataset.
        dataset_title : str, optional
            The title of the dataset.
        owner_org : str, optional
            The ID of the organization.
        timestamp : str or datetime, optional
            Find a result nearest in time to the given timestamp.
        time_direction : TimeDirection, optional
            Either `TimeDirection.FUTURE` or `TimeDirection.PAST`. If the former,
            and `timestamp` is given, then "nearest in time" looks forward in time;
            if the latter, backwards. Default behavior is forward-looking.
        start_time : str or datetime, optional
            The start of a time interval.
        end_time : str or datetime, optional
            The end of a time interval.

        Returns
        -------
        List[Tuple[NDArray, datetime, dict]]
            A list of tuples, one per matching dataset. Each tuple consists of:
            - The matching array subset
            - The timestamp of the dataset (or None)
            - A metadata dict for the dataset (extras without staging fields)

        Raises
        ------
        ValueError
            If no APIClient is associated with this DataSpacesClient.
        StagingFailure
            If the staged data cannot be retrieved.
        """
        if self._api_client is None:
            raise ValueError(
                "query_array requires an APIClient. Create the DataSpacesClient "
                "using from_api_client() or pass api_client to the constructor."
            )

        if len(lb) != len(ub):
            raise ValueError("lb and ub must have the same length")

        time_string = _get_query_time_string(**kwargs)
        filter_list = [f'source:{source}']

        # Build search payload
        search_data = {
            "filter_list": filter_list,
        }
        if dataset_name:
            search_data["dataset_name"] = dataset_name
        if dataset_title:
            search_data["dataset_title"] = dataset_title
        if owner_org:
            search_data["owner_org"] = owner_org
        if time_string:
            search_data["timestamp"] = time_string

        search_results = self._api_client.advanced_search(search_data)

        results = []
        for result in search_results:
            if 'extras' in result:
                extras = result['extras']
                if 'staging_handle' in extras and 'staging_socket' in extras:
                    data, timestamp = _get_data_from_staging(
                        lb=lb,
                        ub=ub,
                        var_name=var_name,
                        **extras
                    )
                    # Remove staging fields from returned extras
                    cleaned_extras = {
                        k: v for k, v in extras.items()
                        if k not in _EXCLUDED_EXTRAS
                    }
                    results.append((data, timestamp, cleaned_extras))

        return results
