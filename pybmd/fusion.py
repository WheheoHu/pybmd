from typing import Any, Dict
from pybmd.ui_manager import UI_Manager


class Fusion(object):
    """docstring for Fusion."""
    def __init__(self, fusion_obj):
        self._fusion = fusion_obj
        self._ui_manager=UI_Manager(self._fusion.UIManager) 
        
        
    @property
    def ui_manager(self) -> UI_Manager:
        return self._ui_manager
    

        
    def set_pref(self, pref_name:str, pref_value) -> bool:  
        return self._fusion.SetPrefs(pref_name, pref_value)

    def set_prefs(self, prefs_dict:dict[str,Any]) -> bool:# -> Any:
        return self._fusion.SetPrefs(prefs_dict)
    
    def get_prefs(self, pref_name:str="")->Dict|Any :
        return self._fusion.GetPrefs(pref_name)
    
    def load_prefs( self, file_name:str="") -> bool:  
        return self._fusion.LoadPrefs(file_name)
    
    def save_prefs(self,file_name:str=None) -> bool:  
        return self._fusion.SavePrefs(file_name)

    
    
    
