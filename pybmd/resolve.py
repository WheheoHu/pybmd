import subprocess
import platform
from typing import TYPE_CHECKING
import psutil

from pybmd.error import *
from pybmd.media_storage import MediaStorage
from pybmd.project_manager import ProjectManager
from pybmd.fusion import Fusion
if TYPE_CHECKING:
    from pybmd.settings import KeyframeMode

from . import _init_bmd

def _is_process_running(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return True
    return False


def _start_local_resolve():
    app_name_mac = "Resolve"
    app_name_win = "Resolve.exe"
    try:
        if _is_process_running(app_name_mac) or _is_process_running(app_name_win):
            print(f"Davinci Resolve is already running.")
        else:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(
                    ['open', '-a', '/Applications/DaVinci Resolve/DaVinci Resolve.app'])
                print("Opened DaVinci Resolve successfully on macOS!")
            elif platform.system() == 'Windows':  # Windows
                resolve_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
                subprocess.Popen(resolve_path)
                print("Opened DaVinci Resolve successfully on Windows!")
            else:
                print("Unsupported operating system.")

    except Exception as e:
        print(f"An error occurred: {e}")
            



RESOLVE_VERSION = None




class Resolve:
    """Resolve class. Init Davinci Resolve Object
        Base for everything
    """

    def __init__(self, resolve_ip: str = '127.0.0.1', auto_start: bool = False):
        """Init Davinci Resolve Object

        Args:
            resolve_ip (str, optional): davinci resolve ip. Defaults to 127.0.0.1.
            auto_start (bool, optional): pen davinci automatically if it's not running, if you want to open davinci manually, change arg to false. Defaults to True.

        Raises:
            ResolveInitError: davinci resolve init failed.you need to check if davinci resolve is running.
        """
        

        if (auto_start):
            _start_local_resolve()
        
        _init_bmd._bmd_module_object=_init_bmd._init_bmd_module()
        _init_bmd._resolve_object =_init_bmd._init_resolve(
            davinci_ip=resolve_ip)
        
        self._resolve =_init_bmd._resolve_object
        
        if self._resolve is None:
            raise ResolveInitError

        global RESOLVE_VERSION
        RESOLVE_VERSION = self._resolve.GetVersion()




    def delete_layout_preset(self, preset_name: str) -> bool:
        """Deletes preset named preset_name.

        Args:
            preset_name (string)

        Returns:
            bool: result
        """
        return self._resolve.DeleteLayoutPreset(preset_name)  # type: ignore

    def export_layout_preset(self, preset_name: str, preset_file_path: str) -> bool:
        """Exports preset named preset_name to path preset_file_path.

        Args:
            preset_name (str): 
            preset_file_path (str): 

        Returns:
            bool: result
        """
        return self._resolve.ExportLayoutPreset(preset_name, str(preset_file_path))  # type: ignore

    @property
    def fusion(self) -> Fusion:
        """Returns the Fusion object."""
        return Fusion(self._resolve.Fusion())

    def get_current_page(self) -> str:
        """Returns the page currently displayed in the main window

        Returns:
            str: Returned value can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver", None).
        """
        return self._resolve.GetCurrentPage()  # type: ignore

    def get_media_storage(self) -> MediaStorage:
        """Returns the MediaStorage  object to query and act on media locations.

        Returns:
            MediaStorage: 
        """
        return MediaStorage(self._resolve.GetMediaStorage())

    def get_product_name(self) -> str:
        """Returns product name.

        Returns:
            str: product name
        """
        return self._resolve.GetProductName()  # type: ignore

    def get_project_manager(self) -> ProjectManager:
        """Returns the ProjectManager object for currently open database.

        Returns:
            ProjectManager: 
        """
        return ProjectManager(self._resolve.GetProjectManager())

    def get_version(self) -> list:
        """Returns list of product version fields in [major, minor, patch, build, suffix] format.

        Returns:
            list: list of product version fields
        """
        return self._resolve.GetVersion()  # type: ignore

    def get_version_string(self) -> str:
        """Returns product version in "major.minor.patch[suffix].build" format.

        Returns:
            str: product version string
        """
        return self._resolve.GetVersionString()  # type: ignore

    def import_layout_preset(self, preset_file_path: str, preset_name: str) -> bool:
        """Imports preset from path 'preset_file_path'. 
            The optional argument 'preset_name' specifies how the preset shall be named.
            If not specified, the preset is named based on the filename.
        """
        return self._resolve.ImportLayoutPreset(str(preset_file_path), preset_name)  # type: ignore

    def load_layout_preset(self, preset_name: str) -> bool:
        """Loads UI layout from saved preset named preset_name.

        Args:
            preset_name (str): 

        Returns:
            bool
        """
        return self._resolve.LoadLayoutPreset(preset_name)  # type: ignore

    def open_page(self, page_name: str) -> bool:
        """Switches to indicated page in DaVinci Resolve. 

        Args:
            page_name (str): Input can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver").

        Returns:
            bool
        """
        return self._resolve.OpenPage(page_name)  # type: ignore

    def quit(self):
        """Quits the Resolve App."""
        self._resolve.Quit()  # type: ignore

    def save_layout_preset(self, preset_name: str) -> bool:
        """Saves current UI layout as a preset named preset_name.

        Args:
            preset_name (str)

        Returns:
            bool
        """
        return self._resolve.SaveLayoutPreset(preset_name)  # type: ignore

    def update_layout_preset(self, preset_name: str) -> bool:
        """Overwrites preset named 'preset_name' with current UI layout.

        Args:
            preset_name (str)

        Returns:
            bool
        """
        return self._resolve.UpdateLayoutPreset(preset_name)  # type: ignore


    ##############################################################################################################################
    # Add at DR18.6.0

    def import_render_preset(self, preset_path: str) -> bool:
        """Import a preset from presetPath (string) and set it as current preset for rendering.

        Args:
            preset_path (str): path of preset file

        Returns:
            bool: Returns True if succssful, False otherwise.
        """
        return self._resolve.ImportRenderPreset(preset_path)

    def export_render_preset(self, preset_name: str, export_path: str) -> bool:
        """Export a preset to a given path (string) if presetName(string) exists.

        Args:
            preset_name (str): export preset name   
            export_path (str): export path

        Returns:
            bool: Returns True if succssful, False otherwise.
        """
        return self._resolve.ExportRenderPreset(preset_name, export_path)

    def import_burn_in_preset(self, preset_path: str) -> bool:
        """Import a data burn in preset from a given presetPath (string)

        Args:
            preset_path (str): path of preset

        Returns:
            bool: Returns True if succssful, False otherwise.
        """
        return self._resolve.ImportBurnInPreset(preset_path)

    def export_burn_in_preset(self, preset_name: str, export_path: str) -> bool:
        """Export a data burn in preset to a given path (string) if presetName (string) exists.

        Args:   
            preset_name (str): name of export preset
            export_path (str): path to export

        Returns:
            bool: Returns True if succssful, False otherwise.
        """
        return self._resolve.ExportBurnInPreset(preset_name, export_path)

    ##############################################################################################################################
    # Add at DR 19.0.0
    def get_keyframe_mode(self) -> int:
        """Refer to section 'Keyframe Mode information' for details.

        Returns:
            int: currently set keyframe mode
        """
        return self._resolve.GetKeyframeMode()

    def set_keyframe_mode(self, key_frame_mode: "KeyframeMode") -> bool:
        """ Refer to section 'Keyframe Mode information' below for details.

        Args:
            key_frame_mode (KeyframeModeInformation): key frame mode

        Returns:
            bool: Returns True when 'keyframeMode'(enum) is successfully set.
        """
        return self._resolve.SetKeyframeMode(key_frame_mode.value)
