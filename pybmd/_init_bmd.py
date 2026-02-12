from typing import cast
from enum import Enum

import importlib.util
import importlib.machinery

import os
import sys

from pybmd._resolve_types import BMDModule, ResolveObject
from pybmd.error import UnsupportSystemError, ResolveInitError


def _load_dynamic(module_name, module_path: str):
    """Loads a module dynamically."""
    loader = importlib.machinery.ExtensionFileLoader(module_name, module_path)
    if (
        spec := importlib.util.spec_from_loader(name=module_name, loader=loader)
    ) is None:
        raise ResolveInitError(
            f"Failed to create module spec for {module_name} at {module_path}"
        )
    module = importlib.util.module_from_spec(spec)

    loader.exec_module(module)
    return module


class DEFAULT_LIB_PATH(Enum):
    LIB_Windows = (
        "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll"
    )
    LIB_MAC = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    LIB_LINUX = "/opt/resolve/Developer/Scripting/Modules/"


def _init_bmd_module():
    if sys.platform.startswith("darwin"):
        PYLIB = DEFAULT_LIB_PATH.LIB_MAC.value
    elif sys.platform.startswith("win"):
        # For virtual environments (e.g., created by uv), set PYTHON3HOME
        # so that embedded DLLs (e.g., fusionscript.dll) can locate the correct Python installation.
        if sys.base_prefix != sys.prefix:
            os.environ["PYTHON3HOME"] = sys.base_exec_prefix
        PYLIB = DEFAULT_LIB_PATH.LIB_Windows.value
    elif sys.platform.startswith("linux"):
        PYLIB = DEFAULT_LIB_PATH.LIB_LINUX.value
    else:
        raise UnsupportSystemError()
    bmd_module = _load_dynamic(module_name="fusionscript", module_path=PYLIB)
    return cast("BMDModule", bmd_module)


_bmd_module_object: BMDModule | None = None
_resolve_object: ResolveObject | None = None


def _init_resolve(davinci_ip: str = "127.0.0.1"):
    """init and return Davinci Resolve object
    Args:
        davinci_ip (str, optional): Default value is local (127.0.0.1).
    """
    global _bmd_module_object
    if not _bmd_module_object:
        raise ResolveInitError(
            "BMD module is not initialized. Ensure that _init_bmd_module() is called first."
        )
    return _bmd_module_object.scriptapp("Resolve", davinci_ip)


def is_resolve_initialized() -> bool:
    """Check if the Resolve object has been initialized.

    Returns:
        True if Resolve() has been instantiated and is ready to use

    Example:
        >>> from pybmd._init_bmd import is_resolve_initialized
        >>> is_resolve_initialized()
        False
        >>> from pybmd import Resolve
        >>> resolve = Resolve()
        >>> is_resolve_initialized()
        True
    """
    global _resolve_object
    return _resolve_object is not None
