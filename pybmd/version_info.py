"""Version checking system for DaVinci Resolve API compatibility.

This module provides classes for representing versions, API status, and version constraints
to ensure API calls are compatible with the current DaVinci Resolve version.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


@dataclass(frozen=True)
class Version:
    """Represents a DaVinci Resolve version.

    Attributes:
        major: Major version number
        minor: Minor version number
        patch: Patch version number (default: 0)

    Example:
        >>> v1 = Version(20, 2, 0)
        >>> v2 = Version(20, 1, 0)
        >>> v1 > v2
        True
        >>> str(v1)
        '20.2.0'
    """

    major: int
    minor: int
    patch: int = 0

    def __str__(self) -> str:
        """Returns version string in format 'major.minor.patch'."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other: "Version") -> bool:
        """Check if this version is less than another version."""
        return (self.major, self.minor, self.patch) < (
            other.major,
            other.minor,
            other.patch,
        )

    def __le__(self, other: "Version") -> bool:
        """Check if this version is less than or equal to another version."""
        return self < other or self == other

    def __gt__(self, other: "Version") -> bool:
        """Check if this version is greater than another version."""
        return not self <= other

    def __ge__(self, other: "Version") -> bool:
        """Check if this version is greater than or equal to another version."""
        return not self < other

    @classmethod
    def from_string(cls, version_str: str) -> "Version":
        """Parse version string like '20.1.0' or '19.0'.

        Args:
            version_str: Version string in format 'major.minor' or 'major.minor.patch'

        Returns:
            Version object

        Example:
            >>> Version.from_string("20.2.0")
            Version(major=20, minor=2, patch=0)
            >>> Version.from_string("19.1")
            Version(major=19, minor=1, patch=0)
        """
        parts = version_str.split(".")
        if len(parts) < 2:
            raise ValueError(f"Invalid version string: {version_str}")
        return cls(
            major=int(parts[0]),
            minor=int(parts[1]),
            patch=int(parts[2]) if len(parts) > 2 else 0,
        )

    @classmethod
    def from_list(cls, version_list: list) -> "Version":
        """Parse version from Resolve's GetVersion() format.

        Args:
            version_list: List in format [major, minor, patch, build, suffix]

        Returns:
            Version object

        Example:
            >>> Version.from_list([20, 2, 0, 12345, ""])
            Version(major=20, minor=2, patch=0)
        """
        return cls(
            major=version_list[0],
            minor=version_list[1],
            patch=version_list[2] if len(version_list) > 2 else 0,
        )


class APIStatus(Enum):
    """Status of an API in a specific version.

    Attributes:
        ADDED: API was added in this version
        REMOVED: API was removed in this version
        DEPRECATED: API is deprecated (still works, but discouraged)
        MOVED: API was moved to different class/module
        NON_FUNCTIONAL: API exists but doesn't work properly
    """

    ADDED = "added"
    REMOVED = "removed"
    DEPRECATED = "deprecated"
    MOVED = "moved"
    NON_FUNCTIONAL = "non_functional"


@dataclass
class VersionConstraint:
    """Defines version constraints for an API.

    Attributes:
        added_in: First version where API exists
        removed_in: Version where API was removed
        deprecated_in: Version where API was deprecated
        moved_to: Where API was moved (if applicable)
        notes: Additional information

    Example:
        >>> constraint = VersionConstraint(
        ...     added_in=Version(20, 0, 0),
        ...     deprecated_in=Version(20, 2, 0),
        ...     moved_to="Graph.set_lut"
        ... )
        >>> current = Version(20, 1, 0)
        >>> constraint.is_compatible(current)
        True
    """

    added_in: Optional[Version] = None
    removed_in: Optional[Version] = None
    deprecated_in: Optional[Version] = None
    moved_to: Optional[str] = None
    notes: Optional[str] = None

    def is_compatible(self, current_version: Version) -> bool:
        """Check if current version is compatible with this API.

        Args:
            current_version: The current DaVinci Resolve version

        Returns:
            True if API is compatible, False otherwise

        Example:
            >>> constraint = VersionConstraint(added_in=Version(20, 0, 0))
            >>> constraint.is_compatible(Version(20, 1, 0))
            True
            >>> constraint.is_compatible(Version(19, 0, 0))
            False
        """
        # Must be added before or at current version
        if self.added_in and current_version < self.added_in:
            return False

        # Must not be removed before current version
        if self.removed_in and current_version >= self.removed_in:
            return False

        return True

    def get_status(self, current_version: Version) -> Tuple[bool, APIStatus, str]:
        """Get detailed status of API compatibility.

        Args:
            current_version: The current DaVinci Resolve version

        Returns:
            Tuple of (is_compatible, status, message)

        Example:
            >>> constraint = VersionConstraint(
            ...     added_in=Version(20, 0, 0),
            ...     removed_in=Version(21, 0, 0),
            ...     moved_to="Graph.method"
            ... )
            >>> is_ok, status, msg = constraint.get_status(Version(19, 0, 0))
            >>> is_ok
            False
            >>> status
            <APIStatus.ADDED: 'added'>
        """
        # Check if not yet added
        if self.added_in and current_version < self.added_in:
            return (
                False,
                APIStatus.ADDED,
                f"API not available. Added in version {self.added_in}",
            )

        # Check if removed
        if self.removed_in and current_version >= self.removed_in:
            msg = f"API removed in version {self.removed_in}"
            if self.moved_to:
                msg += f". Moved to {self.moved_to}"
            return (False, APIStatus.REMOVED, msg)

        # Check if deprecated
        if self.deprecated_in and current_version >= self.deprecated_in:
            msg = f"API deprecated since version {self.deprecated_in}"
            if self.moved_to:
                msg += f". Use {self.moved_to} instead"
            return (True, APIStatus.DEPRECATED, msg)

        return (True, APIStatus.ADDED, "API available")
