
import importlib.machinery
from os import path


from pybmd.media_storage import MediaStorage
from pybmd.project_manager import ProjectManager


def load_dynamic(module, module_path: path):
    loader = importlib.machinery.ExtensionFileLoader(module, module_path)
    module = loader.load_module()
    return module


class Bmd:

    PYLIB = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    APP_NAME = 'Resolve'
    IP_ADDRESS = '127.0.0.1'

    local_davinci = None

    def __init__(self,resolve_ip=IP_ADDRESS):
        self.local_davinci = self.init_davinci(resolve_ip=resolve_ip)
        #TODO finish timeline export properties
        self.EXPORT_AAF = self.local_davinci.EXPORT_AAF
        self.EXPORT_AAF_NEW = self.local_davinci.EXPORT_AAF_NEW
        self.EXPORT_DRT=self.local_davinci.EXPORT_DRT
    def init_davinci(self, davinci_ip):
        """init and return Davinci Resolve object

        Args:
            davinci_ip (str, optional): Defaults to LOCATION.

        """
        bmd_module = load_dynamic(
            module='fusionscript', module_path=self.PYLIB)
        return bmd_module.scriptapp(self.APP_NAME, davinci_ip)

    def get_local_davinci(self):
        return self.local_davinci

    def delete_layout_preset(self, preset_name: str) -> bool:
        """Deletes preset named preset_name.

        Args:
            preset_name (string)

        Returns:
            bool: result
        """
        return self.local_davinci.DeleteLayoutPreset(preset_name)

    def export_layout_preset(self, preset_name: str, preset_file_path: path) -> bool:
        """Exports preset named preset_name to path preset_file_path.

        Args:
            preset_name (str): 
            preset_file_path (str): 

        Returns:
            bool: result
        """
        return self.local_davinci.ExportLayoutPreset(preset_name, str(preset_file_path))

    def fusion(self):
        """Returns the Fusion object. Starting point for Fusion scripts."""
        # if I find more info about fusion I will finish this function
        return self.local_davinci.Fusion()

    def get_current_page(self) -> str:
        """Returns the page currently displayed in the main window

        Returns:
            str: Returned value can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver", None).
        """
        return self.local_davinci.GetCurrentPage()

    def get_media_stroage(self) -> MediaStorage:
        """Returns the MediaStorage  object to query and act on media locations.

        Returns:
            MediaStorage: 
        """
        return MediaStorage(self.local_davinci)

    def get_prodect_name(self) -> str:
        """Returns product name.

        Returns:
            str: product name
        """
        return self.local_davinci.GetProdectName()

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
        return self.local_davinci.GetVersion()

    def get_version_string(self) -> str:
        """Returns product version in "major.minor.patch[suffix].build" format.

        Returns:
            str: product version string
        """
        return self.local_davinci.GetVersionString()

    def import_layout_preset(self, preset_file_path: path, preset_name: str) -> bool:
        """Imports preset from path 'preset_file_path'. 
            The optional argument 'preset_name' specifies how the preset shall be named.
            If not specified, the preset is named based on the filename.
        """
        return self.local_davinci.ImportLayoutPreset(str(preset_file_path), preset_name)

    def load_layout_preset(self, preset_name: str) -> bool:
        """Loads UI layout from saved preset named preset_name.

        Args:
            preset_name (str): 

        Returns:
            bool
        """
        return self.local_davinci.LoadLayoutPreset(preset_name)

    def open_page(self, page_name: str) -> bool:
        """Switches to indicated page in DaVinci Resolve. 

        Args:
            page_name (str): Input can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver").

        Returns:
            bool
        """
        return self.local_davinci.OpenPage(page_name)

    def quit(self):
        """Quits the Resolve App."""
        self.local_davinci.Quit()

    def save_layout_preset(self, preset_name: str) -> bool:
        """Saves current UI layout as a preset named preset_name.

        Args:
            preset_name (str)

        Returns:
            bool
        """
        return self.local_davinci.SaveLayoutPreset(preset_name)

    def update_layout_preset(self, preset_name: str) -> bool:
        """Overwrites preset named 'preset_name' with current UI layout.

        Args:
            preset_name (str)

        Returns:
            bool
        """
        return self.local_davinci.UpdateLayoutPreset(preset_name)
