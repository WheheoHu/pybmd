"""Central registry for API version constraints.

This module provides a singleton registry that stores version constraints
for all APIs in the pybmd library. Decorators automatically register APIs,
and the registry can be queried to check compatibility.
"""

from typing import Dict, Optional, Tuple

from pybmd.version_info import Version, VersionConstraint


class VersionRegistry:
    """Central registry for API version constraints.

    This class maintains a registry of all APIs and their version requirements.
    APIs are automatically registered when decorated with @requires_resolve_version.

    Example:
        >>> from pybmd.version_info import Version, VersionConstraint
        >>> constraint = VersionConstraint(added_in=Version(20, 0, 0))
        >>> VersionRegistry.register("TimelineItem.set_name", constraint)
        >>> VersionRegistry.get_constraint("TimelineItem.set_name")
        VersionConstraint(added_in=Version(major=20, minor=0, patch=0), ...)
    """

    _registry: Dict[str, VersionConstraint] = {}

    @classmethod
    def register(cls, api_identifier: str, constraint: VersionConstraint) -> None:
        """Register an API with its version constraints.

        Args:
            api_identifier: Full API identifier (e.g., "TimelineItem.set_name")
            constraint: Version constraint object defining compatibility rules

        Example:
            >>> from pybmd.version_info import Version, VersionConstraint
            >>> constraint = VersionConstraint(
            ...     added_in=Version(20, 2, 0),
            ...     notes="Added subtitle export support"
            ... )
            >>> VersionRegistry.register("Timeline.export_subtitle", constraint)
        """
        cls._registry[api_identifier] = constraint

    @classmethod
    def get_constraint(cls, api_identifier: str) -> Optional[VersionConstraint]:
        """Get version constraint for an API.

        Args:
            api_identifier: Full API identifier (e.g., "TimelineItem.set_name")

        Returns:
            VersionConstraint if API is registered, None otherwise

        Example:
            >>> constraint = VersionRegistry.get_constraint("TimelineItem.set_name")
            >>> if constraint:
            ...     print(f"Added in: {constraint.added_in}")
            Added in: 20.2.0
        """
        return cls._registry.get(api_identifier)

    @classmethod
    def list_apis(cls, current_version: Version) -> Dict[str, Tuple[bool, str]]:
        """List all APIs and their compatibility with current version.

        Args:
            current_version: The current DaVinci Resolve version

        Returns:
            Dictionary mapping API identifiers to (is_compatible, status_message) tuples

        Example:
            >>> from pybmd.version_info import Version
            >>> current = Version(20, 1, 0)
            >>> apis = VersionRegistry.list_apis(current)
            >>> for api_id, (is_ok, msg) in apis.items():
            ...     if not is_ok:
            ...         print(f"{api_id}: {msg}")
            TimelineItem.set_name: API not available. Added in version 20.2.0
        """
        result = {}
        for api_id, constraint in cls._registry.items():
            is_compat, status, msg = constraint.get_status(current_version)
            result[api_id] = (is_compat, msg)
        return result

    @classmethod
    def clear(cls) -> None:
        """Clear all registered APIs.

        This method is primarily useful for testing purposes.

        Example:
            >>> VersionRegistry.clear()
            >>> len(VersionRegistry._registry)
            0
        """
        cls._registry.clear()

    @classmethod
    def get_all_registered(cls) -> Dict[str, VersionConstraint]:
        """Get all registered APIs and their constraints.

        Returns:
            Dictionary mapping API identifiers to their version constraints

        Example:
            >>> all_apis = VersionRegistry.get_all_registered()
            >>> len(all_apis)
            42
        """
        return cls._registry.copy()
