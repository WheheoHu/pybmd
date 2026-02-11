from enum import Enum

import importlib.util
import importlib.machinery

import os
import sys

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
    return bmd_module


_bmd_module_object = None


def _init_resolve(davinci_ip: str = "127.0.0.1"):
    """init and return Davinci Resolve object
    Args:
        davinci_ip (str, optional): Default value is local (127.0.0.1).
    """

    return _bmd_module_object.scriptapp("Resolve", davinci_ip)  # ty:ignore[unresolved-attribute]


_resolve_object = None
