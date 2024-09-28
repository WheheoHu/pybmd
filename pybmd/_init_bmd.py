from enum import Enum
import importlib
import sys




def _load_dynamic(module_name, module_path: str):
    """Loads a module dynamically."""
    loader = importlib.machinery.ExtensionFileLoader(module_name, module_path)
    spec = importlib.util.spec_from_loader(name=module_name, loader=loader)
    module = importlib.util.module_from_spec(spec)
    # sys.modules[module_name]=module
    # spec.loader.exec_module(module)
    loader.exec_module(module)
    return module

        
class DEFAULT_LIB_PATH(Enum):
    LIB_Windows = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll"
    LIB_MAC = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    
def _init_bmd_module():
    if sys.platform.startswith("darwin"):
        PYLIB = DEFAULT_LIB_PATH.LIB_MAC.value
    elif sys.platform.startswith("win"):
        PYLIB = DEFAULT_LIB_PATH.LIB_Windows.value
    bmd_module = _load_dynamic(
        module_name='fusionscript', module_path=PYLIB) 
    return bmd_module

_bmd_module_object=_init_bmd_module()


def _init_resolve(davinci_ip:str):
    """init and return Davinci Resolve object
    Args:
        davinci_ip (str, optional): Default value is local (127.0.0.1).
    """
        
    return _bmd_module_object.scriptapp("Resolve", davinci_ip)




_resolve_object = _init_resolve("127.0.0.1")

