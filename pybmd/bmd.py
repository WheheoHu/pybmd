
from enum import Enum
import importlib.machinery
import importlib.util
from os import path
import sys
import subprocess
import platform
import psutil 

from pybmd.error import *
from pybmd.media_storage import MediaStorage
from pybmd.project_manager import ProjectManager


def load_dynamic(module_name, module_path: str):
    """Loads a module dynamically."""
    loader = importlib.machinery.ExtensionFileLoader(module_name, module_path)
    spec = importlib.util.spec_from_loader(name=module_name, loader=loader)
    module = importlib.util.module_from_spec(spec)
    # sys.modules[module_name]=module
    # spec.loader.exec_module(module)

    return module
def is_process_running(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return True
    return False

def start_local_resolve():
    app_name_mac = "Resolve"
    app_name_win = "Resolve.exe"
    try:
        if is_process_running(app_name_mac) or is_process_running(app_name_win):
            print(f"Davinci Resolve is already running.")
        else:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', '-a', '/Applications/DaVinci Resolve/DaVinci Resolve.app'])
                print("Opened DaVinci Resolve successfully on macOS!")
            elif platform.system() == 'Windows':  # Windows
                resolve_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
                subprocess.Popen(resolve_path)
                print("Opened DaVinci Resolve successfully on Windows!")
            else:
                print("Unsupported operating system.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

class Default_LIB_PATH(Enum):
    LIB_Windows = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll"
    LIB_MAC = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"


class Bmd:
    """Bmd class. Init Davinci Resolve Object
        Base for everything
    """

    if sys.platform.startswith("darwin"):
        PYLIB = Default_LIB_PATH.LIB_MAC.value
    elif sys.platform.startswith("win"):
        PYLIB = Default_LIB_PATH.LIB_Windows.value
    APP_NAME = 'Resolve'


    local_davinci = None

    def __init__(self, resolve_ip:str='127.0.0.1',auto_start:bool=False):
        """Init Davinci Resolve Object

        Args:
            resolve_ip (str, optional): davinci resolve ip. Defaults to 127.0.0.1.
            auto_start (bool, optional): pen davinci automatically if it's not running, if you want to open davinci manually, change arg to false. Defaults to True.

        Raises:
            ResolveInitError: davinci resolve init failed.you need to check if davinci resolve is running.
        """
        self.local_davinci = self.init_davinci(davinci_ip=resolve_ip,auto_start=auto_start)
        if self.local_davinci is None:
            raise ResolveInitError

        # timeline exportType can be one of the following constants:
        self.EXPORT_AAF = self.local_davinci.EXPORT_AAF
        self.EXPORT_DRT = self.local_davinci.EXPORT_DRT
        self.EXPORT_EDL = self.local_davinci.EXPORT_EDL
        self.EXPORT_FCP_7_XML = self.local_davinci.EXPORT_FCP_7_XML

        # Remove at DR 18.1.3
        # self.EXPORT_FCPXML_1_3 = self.local_davinci.EXPORT_FCPXML_1_3
        # self.EXPORT_FCPXML_1_4 = self.local_davinci.EXPORT_FCPXML_1_4
        # self.EXPORT_FCPXML_1_5 = self.local_davinci.EXPORT_FCPXML_1_5
        # self.EXPORT_FCPXML_1_6 = self.local_davinci.EXPORT_FCPXML_1_6
        # self.EXPORT_FCPXML_1_7 = self.local_davinci.EXPORT_FCPXML_1_7
        self.EXPORT_FCPXML_1_8 = self.local_davinci.EXPORT_FCPXML_1_8

        # Add at DR 18.0.0
        self.EXPORT_FCPXML_1_9 = self.local_davinci.EXPORT_FCPXML_1_9
        self.EXPORT_FCPXML_1_10 = self.local_davinci.EXPORT_FCPXML_1_10

        self.EXPORT_HDR_10_PROFILE_A = self.local_davinci.EXPORT_HDR_10_PROFILE_A
        self.EXPORT_HDR_10_PROFILE_B = self.local_davinci.EXPORT_HDR_10_PROFILE_B
        self.EXPORT_TEXT_CSV = self.local_davinci.EXPORT_TEXT_CSV
        self.EXPORT_TEXT_TAB = self.local_davinci.EXPORT_TEXT_TAB
        self.EXPORT_DOLBY_VISION_VER_2_9 = self.local_davinci.EXPORT_DOLBY_VISION_VER_2_9
        self.EXPORT_DOLBY_VISION_VER_4_0 = self.local_davinci.EXPORT_DOLBY_VISION_VER_4_0

        # Add at DR 18.1.3
        self.EXPORT_DOLBY_VISION_VER_5_1 = self.local_davinci.EXPORT_DOLBY_VISION_VER_5_1

        # Add at DR 18.5.0
        self.EXPORT_OTIO = self.local_davinci.EXPORT_OTIO

        # timeline exportSubtype can be one of the following enums:
        # for exportType is EXPORT_AAF:
        self.EXPORT_AAF_NEW = self.local_davinci.EXPORT_AAF_NEW
        self.EXPORT_AAF_EXISTING = self.local_davinci.EXPORT_AAF_EXISTING
        # for exportType is EXPORT_EDL:
        self.EXPORT_NONE = self.local_davinci.EXPORT_NONE
        self.EXPORT_CDL = self.local_davinci.EXPORT_CDL
        self.EXPORT_SDL = self.local_davinci.EXPORT_SDL
        self.EXPORT_MISSING_CLIPS = self.local_davinci.EXPORT_MISSING_CLIPS
        
        
        self.CLOUD_SETTING_PROJECT_NAME=self.local_davinci.CLOUD_SETTING_PROJECT_NAME
        self.CLOUD_SETTING_PROJECT_MEDIA_PATH=self.local_davinci.CLOUD_SETTING_PROJECT_MEDIA_PATH
        self.CLOUD_SETTING_IS_COLLAB=self.local_davinci.CLOUD_SETTING_IS_COLLAB
        self.CLOUD_SETTING_SYNC_MODE=self.local_davinci.CLOUD_SETTING_SYNC_MODE
        self.CLOUD_SETTING_IS_CAMERA_ACCESS=self.local_davinci.CLOUD_SETTING_IS_CAMERA_ACCESS
        
        self.CLOUD_SYNC_NONE=self.local_davinci.CLOUD_SYNC_NONE
        self.CLOUD_SYNC_PROXY_ONLY=self.local_davinci.CLOUD_SYNC_PROXY_ONLY
        self.CLOUD_SYNC_PROXY_AND_ORIG=self.local_davinci.CLOUD_SYNC_PROXY_AND_ORIG
        
        
        self.SUBTITLE_LANGUAGE=self.local_davinci.SUBTITLE_LANGUAGE
        self.SUBTITLE_CAPTION_PRESET=self.local_davinci.SUBTITLE_CAPTION_PRESET
        self.SUBTITLE_CHARS_PER_LINE=self.local_davinci.SUBTITLE_CHARS_PER_LINE
        self.SUBTITLE_LINE_BREAK=self.local_davinci.SUBTITLE_LINE_BREAK
        self.SUBTITLE_GAP=self.local_davinci.SUBTITLE_GAP
        
        
        self.AUTO_CAPTION_AUTO=self.local_davinci.AUTO_CAPTION_AUTO
        self.AUTO_CAPTION_DANISH=self.local_davinci.AUTO_CAPTION_DANISH
        self.AUTO_CAPTION_DUTCH=self.local_davinci.AUTO_CAPTION_DUTCH
        self.AUTO_CAPTION_ENGLISH=self.local_davinci.AUTO_CAPTION_ENGLISH
        self.AUTO_CAPTION_FRENCH=self.local_davinci.AUTO_CAPTION_FRENCH
        self.AUTO_CAPTION_GERMAN=self.local_davinci.AUTO_CAPTION_GERMAN
        self.AUTO_CAPTION_ITALIAN=self.local_davinci.AUTO_CAPTION_ITALIAN
        self.AUTO_CAPTION_JAPANESE=self.local_davinci.AUTO_CAPTION_JAPANESE
        self.AUTO_CAPTION_KOREAN=self.local_davinci.AUTO_CAPTION_KOREAN
        self.AUTO_CAPTION_MANDARIN_SIMPLIFIED=self.local_davinci.AUTO_CAPTION_MANDARIN_SIMPLIFIED
        self.AUTO_CAPTION_MANDARIN_TRADITIONAL=self.local_davinci.AUTO_CAPTION_MANDARIN_TRADITIONAL
        self.AUTO_CAPTION_NORWEGIAN=self.local_davinci.AUTO_CAPTION_NORWEGIAN
        self.AUTO_CAPTION_PORTUGUESE=self.local_davinci.AUTO_CAPTION_PORTUGUESE
        self.AUTO_CAPTION_RUSSIAN=self.local_davinci.AUTO_CAPTION_RUSSIAN
        self.AUTO_CAPTION_SPANISH=self.local_davinci.AUTO_CAPTION_SPANISH
        self.AUTO_CAPTION_SWEDISH=self.local_davinci.AUTO_CAPTION_SWEDISH
        
        
        
        self.AUTO_CAPTION_SUBTITLE_DEFAULT=self.local_davinci.AUTO_CAPTION_SUBTITLE_DEFAULT
        self.AUTO_CAPTION_TELETEXT=self.local_davinci.AUTO_CAPTION_TELETEXT
        self.AUTO_CAPTION_NETFLIX=self.local_davinci.AUTO_CAPTION_NETFLIX
        
       
        self.AUTO_CAPTION_LINE_SINGLE=self.local_davinci.AUTO_CAPTION_LINE_SINGLE
        self.AUTO_CAPTION_LINE_DOUBLE=self.local_davinci.AUTO_CAPTION_LINE_DOUBLE
        
        global RESOLVE_VERSION
        RESOLVE_VERSION=self.local_davinci.GetVersion()
        
    def init_davinci(self, davinci_ip,auto_start):
        """init and return Davinci Resolve object

        Args:
            davinci_ip (str, optional): Default value is local (127.0.0.1).

        """
        if(auto_start):
            start_local_resolve()
            
        bmd_module = load_dynamic(
            module_name='fusionscript', module_path=self.PYLIB)
        return bmd_module.scriptapp(self.APP_NAME, davinci_ip)

    def get_local_davinci(self):
        """Returns the local Davinci Resolve object."""
        return self.local_davinci

    def delete_layout_preset(self, preset_name: str) -> bool:
        """Deletes preset named preset_name.

        Args:
            preset_name (string)

        Returns:
            bool: result
        """
        return self.local_davinci.DeleteLayoutPreset(preset_name)  # type: ignore

    def export_layout_preset(self, preset_name: str, preset_file_path: str) -> bool:
        """Exports preset named preset_name to path preset_file_path.

        Args:
            preset_name (str): 
            preset_file_path (str): 

        Returns:
            bool: result
        """
        return self.local_davinci.ExportLayoutPreset(preset_name, str(preset_file_path))  # type: ignore

    def fusion(self):
        """Returns the Fusion object. Starting point for Fusion scripts."""
        # if I find more info about fusion I will finish this function
        return self.local_davinci.Fusion()  # type: ignore

    def get_current_page(self) -> str:
        """Returns the page currently displayed in the main window

        Returns:
            str: Returned value can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver", None).
        """
        return self.local_davinci.GetCurrentPage()  # type: ignore

    def get_media_storage(self) -> MediaStorage:
        """Returns the MediaStorage  object to query and act on media locations.

        Returns:
            MediaStorage: 
        """
        return MediaStorage(self.local_davinci)

    def get_product_name(self) -> str:
        """Returns product name.

        Returns:
            str: product name
        """
        return self.local_davinci.GetProductName()  # type: ignore

    def get_project_manager(self) -> ProjectManager:
        """Returns the ProjectManager object for currently open database.

        Returns:
            ProjectManager: 
        """
        return ProjectManager(self.local_davinci)

    def get_version(self) -> list:
        """Returns list of product version fields in [major, minor, patch, build, suffix] format.

        Returns:
            list: list of product version fields
        """
        return self.local_davinci.GetVersion()  # type: ignore

    def get_version_string(self) -> str:
        """Returns product version in "major.minor.patch[suffix].build" format.

        Returns:
            str: product version string
        """
        return self.local_davinci.GetVersionString()  # type: ignore

    def import_layout_preset(self, preset_file_path: str, preset_name: str) -> bool:
        """Imports preset from path 'preset_file_path'. 
            The optional argument 'preset_name' specifies how the preset shall be named.
            If not specified, the preset is named based on the filename.
        """
        return self.local_davinci.ImportLayoutPreset(str(preset_file_path), preset_name)  # type: ignore

    def load_layout_preset(self, preset_name: str) -> bool:
        """Loads UI layout from saved preset named preset_name.

        Args:
            preset_name (str): 

        Returns:
            bool
        """
        return self.local_davinci.LoadLayoutPreset(preset_name)  # type: ignore

    def open_page(self, page_name: str) -> bool:
        """Switches to indicated page in DaVinci Resolve. 

        Args:
            page_name (str): Input can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver").

        Returns:
            bool
        """
        return self.local_davinci.OpenPage(page_name)  # type: ignore

    def quit(self):
        """Quits the Resolve App."""
        self.local_davinci.Quit()  # type: ignore

    def save_layout_preset(self, preset_name: str) -> bool:
        """Saves current UI layout as a preset named preset_name.

        Args:
            preset_name (str)

        Returns:
            bool
        """
        return self.local_davinci.SaveLayoutPreset(preset_name)  # type: ignore

    def update_layout_preset(self, preset_name: str) -> bool:
        """Overwrites preset named 'preset_name' with current UI layout.

        Args:
            preset_name (str)

        Returns:
            bool
        """
        return self.local_davinci.UpdateLayoutPreset(preset_name)  # type: ignore

    ##############################################################################################################################
    # Add at DR18.6.0 
    
    def import_render_preset(self, preset_path: str) -> bool:
        """Import a preset from presetPath (string) and set it as current preset for rendering.

        Args:
            preset_path (str): path of preset file

        Returns:
            bool: Returns True if succssful, False otherwise.
        """
        return self.bmd.ImportRenderPreset(preset_path)

    def export_render_preset(self, preset_name: str, export_path: str) -> bool:
        """Export a preset to a given path (string) if presetName(string) exists.

        Args:
            preset_name (str): export preset name   
            export_path (str): export path

        Returns:
            bool: Returns True if succssful, False otherwise.
        """
        return self.bmd.ExportRenderPreset(preset_name, export_path)

    def import_burn_in_preset(self, preset_path: str) -> bool:
        """Import a data burn in preset from a given presetPath (string)

        Args:
            preset_path (str): path of preset

        Returns:
            bool: Returns True if succssful, False otherwise.
        """
        return self.bmd.ImportBurnInPreset(preset_path)

    def export_burn_in_preset(self, preset_name: str, export_path: str) -> bool:
        """Export a data burn in preset to a given path (string) if presetName (string) exists.

        Args:   
            preset_name (str): name of export preset
            export_path (str): path to export

        Returns:
            bool: Returns True if succssful, False otherwise.
        """
        return self.bmd.ExportBurnInPreset(preset_name, export_path)
