from typing import Optional


class ResolveInitError(Exception):
    """Error for Resolve Init
    """
    def __init__(self, msg="Init Resolve failed,please check if davinci resolve is running"):
        super().__init__(msg)

class UnsupportSystemError(Exception):
    """Error for system not support
    """
    def __init__(self, msg="Unsupport system!"):
        super().__init__(msg)


class WrapperInitError(Exception):
    """Error for Wrapper Init
    """
    def __init__(self, msg="Init Wrapper failed,please check if the input argument is valid"):
        super().__init__(msg)


class APIVersionError(Exception):
    """Error for API version incompatibility.

    Raised when attempting to use an API that is not compatible with
    the current DaVinci Resolve version.

    Attributes:
        api_name: Name of the incompatible API
        current_version: Current Resolve version string
        constraint: Description of version constraint
        moved_to: New location if API was moved (optional)
    """
    def __init__(
        self,
        api_name: str,
        current_version: str,
        constraint: str,
        moved_to: Optional[str] = None
    ):
        msg = f"API '{api_name}' is not compatible with Resolve version {current_version}. {constraint}"
        if moved_to:
            msg += f" Consider using '{moved_to}' instead."
        super().__init__(msg)
        self.api_name = api_name
        self.current_version = current_version
        self.constraint = constraint
        self.moved_to = moved_to


class APIDeprecationWarning(Warning):
    """Warning for deprecated APIs.

    Emitted when using an API that has been deprecated but still functions.
    The warning message typically suggests an alternative API to use.
    """
    pass