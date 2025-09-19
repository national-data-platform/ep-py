"""
Version configuration for API compatibility checking.

This file contains the minimum required API version for full functionality.
Update this version when new features require newer API versions.
"""

# Minimum required API version for full library functionality
# Format: "major.minor.patch"
MINIMUM_API_VERSION = "0.2.0"


# Version comparison helper functions
def parse_version(version_str: str) -> tuple:
    """
    Parse version string into tuple for comparison.

    Args:
        version_str: Version string in format "major.minor.patch"

    Returns:
        Tuple of integers (major, minor, patch)

    Raises:
        ValueError: If version string format is invalid
    """
    try:
        parts = version_str.split(".")
        if len(parts) != 3:
            raise ValueError(f"Invalid version format: {version_str}")
        return tuple(int(part) for part in parts)
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid version format: {version_str}") from e


def is_version_compatible(
    api_version: str, min_version: str = MINIMUM_API_VERSION
) -> bool:
    """
    Check if API version is compatible with minimum required version.

    Args:
        api_version: Current API version string
        min_version: Minimum required version string

    Returns:
        True if API version >= minimum version, False otherwise

    Raises:
        ValueError: If version strings are invalid
    """
    api_tuple = parse_version(api_version)
    min_tuple = parse_version(min_version)
    return api_tuple >= min_tuple


def get_minimum_version() -> str:
    """
    Get the minimum required API version.

    Returns:
        Minimum required API version string
    """
    return MINIMUM_API_VERSION
