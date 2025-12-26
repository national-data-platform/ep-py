"""Tests for DataSpaces client wrapper."""

import pytest
from unittest.mock import MagicMock, patch
import sys


class TestDataSpacesClientImport:
    """Test suite for DataSpaces client import handling."""

    def test_import_error_without_dxspaces(self):
        """Test that helpful error is raised when dxspaces not installed."""
        # Temporarily remove dxspaces from modules if present
        dxspaces_modules = [k for k in sys.modules.keys() if "dxspaces" in k]
        saved_modules = {k: sys.modules.pop(k) for k in dxspaces_modules}

        try:
            # Mock import to simulate dxspaces not installed
            with patch.dict(sys.modules, {"dxspaces": None}):
                # Force reimport
                if "ndp_ep.dataspaces" in sys.modules:
                    del sys.modules["ndp_ep.dataspaces"]

                # Import should succeed (lazy import)
                from ndp_ep.dataspaces import DataSpacesClient, DXSPACES_AVAILABLE

                # But instantiation should fail with helpful message
                if not DXSPACES_AVAILABLE:
                    with pytest.raises(ImportError) as exc_info:
                        DataSpacesClient(dspaces_url="http://localhost:8003")

                    assert "pip install ndp-ep[dataspaces]" in str(exc_info.value)
        finally:
            # Restore modules
            sys.modules.update(saved_modules)


class TestDataSpacesClientWithMock:
    """Test suite for DataSpaces client with mocked dxspaces."""

    @pytest.fixture
    def mock_dxspaces(self):
        """Create mock DXSpacesClient."""
        mock_client = MagicMock()
        mock_client.GetVars.return_value = ["var1", "var2"]
        mock_client.GetVarObjs.return_value = [{"name": "var1", "version": 0}]
        mock_client.GetNDArray.return_value = None
        mock_client.Register.return_value = MagicMock(
            namespace="test", parameters={}
        )
        return mock_client

    @pytest.fixture
    def mock_dxspaces_class(self, mock_dxspaces):
        """Patch DXSpacesClient class."""
        with patch("ndp_ep.dataspaces._DXSpacesClient") as mock_class:
            mock_class.return_value = mock_dxspaces
            with patch("ndp_ep.dataspaces.DXSPACES_AVAILABLE", True):
                yield mock_class

    def test_direct_initialization(self, mock_dxspaces_class, mock_dxspaces):
        """Test direct initialization with URL."""
        from ndp_ep.dataspaces import DataSpacesClient

        ds = DataSpacesClient(dspaces_url="http://localhost:8003")

        assert ds.url == "http://localhost:8003"
        mock_dxspaces_class.assert_called_once_with(
            "http://localhost:8003", debug=False
        )

    def test_from_api_client(self, mock_dxspaces_class, mock_dxspaces):
        """Test initialization from APIClient."""
        from ndp_ep.dataspaces import DataSpacesClient

        mock_api_client = MagicMock()
        mock_api_client.get_dspaces_details.return_value = {
            "dspaces_enabled": True,
            "dspaces_url": "http://localhost:8003",
        }

        ds = DataSpacesClient.from_api_client(mock_api_client)

        assert ds.url == "http://localhost:8003"
        mock_api_client.get_dspaces_details.assert_called_once()

    def test_from_api_client_disabled(self, mock_dxspaces_class):
        """Test error when DataSpaces is disabled on server."""
        from ndp_ep.dataspaces import DataSpacesClient

        mock_api_client = MagicMock()
        mock_api_client.get_dspaces_details.return_value = {
            "dspaces_enabled": False,
            "dspaces_url": "",
        }

        with pytest.raises(ValueError) as exc_info:
            DataSpacesClient.from_api_client(mock_api_client)

        assert "not enabled" in str(exc_info.value)

    def test_get_vars(self, mock_dxspaces_class, mock_dxspaces):
        """Test get_vars delegation."""
        from ndp_ep.dataspaces import DataSpacesClient

        ds = DataSpacesClient(dspaces_url="http://localhost:8003")
        result = ds.get_vars()

        assert result == ["var1", "var2"]
        mock_dxspaces.GetVars.assert_called_once()

    def test_get_var_objs(self, mock_dxspaces_class, mock_dxspaces):
        """Test get_var_objs delegation."""
        from ndp_ep.dataspaces import DataSpacesClient

        ds = DataSpacesClient(dspaces_url="http://localhost:8003")
        result = ds.get_var_objs("var1")

        assert result == [{"name": "var1", "version": 0}]
        mock_dxspaces.GetVarObjs.assert_called_once_with("var1")

    def test_get_ndarray(self, mock_dxspaces_class, mock_dxspaces):
        """Test get_ndarray delegation."""
        from ndp_ep.dataspaces import DataSpacesClient

        ds = DataSpacesClient(dspaces_url="http://localhost:8003")
        ds.get_ndarray("var1", version=0, lb=(0, 0), ub=(10, 10))

        mock_dxspaces.GetNDArray.assert_called_once_with(
            "var1", 0, (0, 0), (10, 10), None
        )

    def test_put_ndarray(self, mock_dxspaces_class, mock_dxspaces):
        """Test put_ndarray delegation."""
        from ndp_ep.dataspaces import DataSpacesClient

        ds = DataSpacesClient(dspaces_url="http://localhost:8003")
        mock_arr = MagicMock()
        ds.put_ndarray(mock_arr, "var1", version=0, offset=(0, 0))

        mock_dxspaces.PutNDArray.assert_called_once_with(
            mock_arr, "var1", 0, (0, 0), None
        )

    def test_register(self, mock_dxspaces_class, mock_dxspaces):
        """Test register delegation."""
        from ndp_ep.dataspaces import DataSpacesClient

        ds = DataSpacesClient(dspaces_url="http://localhost:8003")
        result = ds.register("s3", "mydata", {"bucket": "test"})

        mock_dxspaces.Register.assert_called_once_with(
            "s3", "mydata", {"bucket": "test"}
        )
        assert result is not None
