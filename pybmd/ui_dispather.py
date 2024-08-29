from typing import List


class UI_Dispather(object):
    """docstring for UI_Dispather."""
    def __init__(self, ui_dispather):
        self._ui_dispather = ui_dispather
        
    def add_window(self, id:str,children:List):
        setattr(self,id,children)