from typing import List

from pybmd.ui_manager import UI_Manager
from . import _init_bmd


class UI_Dispather(object):
    """docstring for UI_Dispather."""
    def __init__(self,ui_manager:UI_Manager):
        self._ui_dispather = _init_bmd._bmd_module_object.UIDispatcher(ui_manager._ui_manager)
        
    def add_window(self, id:str,children:List):
        setattr(self,id,children)