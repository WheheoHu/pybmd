"""Decorator system for DaVinci Resolve API version checking.

This module provides decorators that can be applied to API methods to automatically
check version compatibility at runtime. When a method is decorated, it will:
1. Register the API in the VersionRegistry
2. Check version compatibility before execution
3. Raise APIVersionError if incompatible
4. Warn if deprecated

Example:
    @requires_resolve_version(added_in="20.2.0")
    def set_name(self, name: str) -> bool:
        return self._timeline_item.SetName(name)
"""

import functools
import os
import warnings
from typing import Callable, Optional, TypeVar, cast, Any

import multimethod

from pybmd.version_info import Version, VersionConstraint, APIStatus
from pybmd.version_registry import VersionRegistry
from pybmd.error import APIVersionError, APIDeprecationWarning


F = TypeVar('F', bound=Callable)

# Frames from these files are skipped when attributing a deprecation warning, so the
# warning blames user code instead of multimethod's dispatch machinery. Overloads
# decorated with @multimethod are reached through multimethod.__call__, which would
# otherwise absorb the warning's stacklevel.
_SKIP_FILE_PREFIXES = (os.path.dirname(multimethod.__file__),)


def requires_resolve_version(
    added_in: Optional[str] = None,
    removed_in: Optional[str] = None,
    deprecated_in: Optional[str] = None,
    moved_to: Optional[str] = None,
    notes: Optional[str] = None,
) -> Callable:
    """Decorator to specify DaVinci Resolve version requirements for an API method.

    This decorator automatically:
    - Registers the API in the VersionRegistry
    - Checks version compatibility at runtime before execution
    - Raises APIVersionError if the current Resolve version is incompatible
    - Issues a warning if the API is deprecated but still functional

    Args:
        added_in: Version string when API was added (e.g., "20.0.0" or "20.2")
        removed_in: Version string when API was removed (e.g., "21.0.0")
        deprecated_in: Version string when API was deprecated (e.g., "20.2.0")
        moved_to: New location if API was moved (e.g., "Graph.apply_arri_cdl_lut")
        notes: Additional notes about version compatibility

    Returns:
        Decorator function that wraps the original method

    Raises:
        APIVersionError: If current Resolve version is incompatible with the API

    Warns:
        APIDeprecationWarning: If API is deprecated in current version

    Example:
        Basic usage with minimum version:
        >>> @requires_resolve_version(added_in="20.2.0")
        ... def set_name(self, name: str) -> bool:
        ...     return self._timeline_item.SetName(name)

        API that was moved:
        >>> @requires_resolve_version(
        ...     added_in="18.0.0",
        ...     removed_in="19.0.0",
        ...     moved_to="Graph.set_lut",
        ...     notes="Use get_node_graph().set_lut() instead"
        ... )
        ... def set_lut(self, node_index: int, lut_path: str) -> bool:
        ...     return self._timeline_item.SetLUT(node_index, lut_path)

        Deprecated API:
        >>> @requires_resolve_version(
        ...     added_in="18.0.0",
        ...     deprecated_in="20.0.0",
        ...     moved_to="new_method"
        ... )
        ... def old_method(self):
        ...     pass
    """

    def decorator(func: F) -> F:
        # Create version constraint
        constraint = VersionConstraint(
            added_in=Version.from_string(added_in) if added_in else None,
            removed_in=Version.from_string(removed_in) if removed_in else None,
            deprecated_in=Version.from_string(deprecated_in) if deprecated_in else None,
            moved_to=moved_to,
            notes=notes,
        )

        # Register in central registry
        # Extract class name from qualified name
        class_name = (
            func.__qualname__.rsplit(".", 1)[0] if "." in func.__qualname__ else ""
        )
        api_identifier = (
            f"{class_name}.{func.__name__}" if class_name else func.__name__
        )
        VersionRegistry.register(api_identifier, constraint)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Lazy import to avoid circular dependency
            from pybmd.resolve import RESOLVE_VERSION

            # Get current Resolve version
            if RESOLVE_VERSION is None:
                raise APIVersionError(
                    api_name=func.__name__,
                    current_version="unknown",
                    constraint="Resolve version not initialized. Please create a Resolve instance first.",
                )

            current_version = Version.from_list(RESOLVE_VERSION)

            # Check compatibility
            is_compatible, status, message = constraint.get_status(current_version)

            if not is_compatible:
                raise APIVersionError(
                    api_name=func.__name__,
                    current_version=str(current_version),
                    constraint=message,
                    moved_to=moved_to,
                )

            # Warn if deprecated
            if status == APIStatus.DEPRECATED:
                warnings.warn(
                    f"{func.__name__}: {message}",
                    APIDeprecationWarning,
                    stacklevel=2,
                    skip_file_prefixes=_SKIP_FILE_PREFIXES,
                )

            # Call the original function
            return func(*args, **kwargs)

        # Store constraint as function attribute for inspection
        wrapper_any = cast(Any, wrapper)
        wrapper_any.__version_constraint__ = constraint
        wrapper_any.__api_identifier__ = api_identifier

        return cast(F, wrapper)

    return decorator


def warn_deprecated_calling_convention(
    api_name: str,
    deprecated_in: str,
    moved_to: Optional[str] = None,
    stacklevel: int = 3,
) -> None:
    """Warn that the *calling convention* used to reach an API is deprecated.

    Some DaVinci Resolve APIs did not get deprecated as a whole - only one of their
    calling conventions did (e.g. ``SetMetadata(metadataType, metadataValue)`` versus
    ``SetMetadata({metadata})``). Which convention was used is only known at call time,
    so those wrappers call this helper on the legacy path instead of being decorated
    with :func:`requires_resolve_version`. No constraint is registered in the
    VersionRegistry, because the method itself stays fully supported.

    Nothing is warned when the running Resolve version is older than 'deprecated_in',
    or when no Resolve instance has been created yet.

    Args:
        api_name: Legacy convention identifier, e.g.
            "MediaPoolItem.set_metadata(metadata_type, metadata_value)"
        deprecated_in: Version string the convention was deprecated in (e.g. "21.1.0")
        moved_to: Convention to use instead (e.g. "set_metadata({metadata})")
        stacklevel: Stack level the warning points at. The default of 3 blames the
            caller of the wrapper method.

    Warns:
        APIDeprecationWarning: If the running Resolve version deprecates the convention
    """
    # Lazy import to avoid circular dependency
    from pybmd.resolve import RESOLVE_VERSION

    if RESOLVE_VERSION is None:
        return

    if Version.from_list(RESOLVE_VERSION) < Version.from_string(deprecated_in):
        return

    message = f"{api_name}: API deprecated since version {deprecated_in}"
    if moved_to:
        message += f". Use {moved_to} instead"
    warnings.warn(
        message,
        APIDeprecationWarning,
        stacklevel=stacklevel,
        skip_file_prefixes=_SKIP_FILE_PREFIXES,
    )


def minimum_resolve_version(version_str: str) -> Callable:
    """Simplified decorator for APIs that only need minimum version.

    This is a convenience decorator that wraps requires_resolve_version
    with only the added_in parameter.

    Args:
        version_str: Minimum version string (e.g., "20.0.0")

    Returns:
        Decorator function

    Example:
        >>> @minimum_resolve_version("20.0.0")
        ... def link_full_resolution_media(self, file_path: str) -> bool:
        ...     return self._media_pool_item.LinkProxyMedia(file_path)
    """
    return requires_resolve_version(added_in=version_str)


def version_range(min_version: str, max_version: str) -> Callable:
    """Decorator for APIs available only in a specific version range.

    This is useful for APIs that were added in one version and removed
    in a later version, typically because they were replaced or refactored.

    Args:
        min_version: Minimum version (inclusive)
        max_version: Maximum version (exclusive)

    Returns:
        Decorator function

    Example:
        >>> @version_range("18.0.0", "19.0.0")
        ... def old_api_method(self):
        ...     '''This API only worked in DR 18.x'''
        ...     pass
    """
    return requires_resolve_version(added_in=min_version, removed_in=max_version)
