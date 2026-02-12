import subprocess
import platform
from typing import TYPE_CHECKING, List, Tuple
import psutil

from pybmd.error import ResolveInitError
from pybmd.media_storage import MediaStorage
from pybmd.project_manager import ProjectManager
from pybmd.fusion import Fusion
from pybmd.version_info import Version
from pybmd.version_registry import VersionRegistry
from pybmd.decorators import minimum_resolve_version

if TYPE_CHECKING:
    from pybmd.settings import KeyframeMode

from . import _init_bmd


def _is_process_running(process_name):
    for process in psutil.process_iter(["pid", "name"]):
        if process.info["name"] == process_name:
            return True
    return False


def _start_local_resolve():
    app_name_mac = "Resolve"
    app_name_win = "Resolve.exe"
    try:
        if _is_process_running(app_name_mac) or _is_process_running(app_name_win):
            print("Davinci Resolve is already running.")
        else:
            if platform.system() == "Darwin":  # macOS
                subprocess.run(
                    ["open", "-a", "/Applications/DaVinci Resolve/DaVinci Resolve.app"]
                )
                print("Opened DaVinci Resolve successfully on macOS!")
            elif platform.system() == "Windows":  # Windows
                resolve_path = (
                    r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
                )
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

    def _initialize_resolve(self, resolve_ip: str):
        """Initialize the Resolve connection.

        Args:
            resolve_ip: IP address of the DaVinci Resolve instance

        Returns:
            Resolve object

        Raises:
            ResolveInitError: If initialization fails
        """
        _init_bmd._bmd_module_object = _init_bmd._init_bmd_module()
        resolve_obj = _init_bmd._init_resolve(davinci_ip=resolve_ip)

        if resolve_obj is None:
            raise ResolveInitError

        return resolve_obj

    def __init__(self, resolve_ip: str = "127.0.0.1", auto_start: bool = False):
        """Init Davinci Resolve Object

        Args:
            resolve_ip (str, optional): davinci resolve ip. Defaults to 127.0.0.1.
            auto_start (bool, optional): open davinci automatically if it's not running, if you want to open davinci manually, change arg to false. Defaults to True.

        Raises:
            ResolveInitError: davinci resolve init failed.you need to check if davinci resolve is running.
        """

        if auto_start:
            _start_local_resolve()

        self._resolve = self._initialize_resolve(resolve_ip)
        self._version = self._resolve.GetVersion()

        # Populate the global _resolve_object so other modules can access constants
        _init_bmd._resolve_object = self._resolve

        global RESOLVE_VERSION
        RESOLVE_VERSION = self._version

    def delete_layout_preset(self, preset_name: str) -> bool:
        """Deletes preset named preset_name.

        Args:
            preset_name (string)

        Returns:
            bool: result
        """
        return self._resolve.DeleteLayoutPreset(preset_name)

    def export_layout_preset(self, preset_name: str, preset_file_path: str) -> bool:
        """Exports preset named preset_name to path preset_file_path.

        Args:
            preset_name (str):
            preset_file_path (str):

        Returns:
            bool: result
        """
        return self._resolve.ExportLayoutPreset(preset_name, str(preset_file_path))

    @property
    def fusion(self) -> Fusion:
        """Returns the Fusion object."""
        return Fusion(self._resolve.Fusion())

    def get_current_page(self) -> str:
        """Returns the page currently displayed in the main window

        Returns:
            str: Returned value can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver", None).
        """
        return self._resolve.GetCurrentPage()

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
        return self._resolve.GetProductName()

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
        return self._resolve.GetVersion()

    def get_version_string(self) -> str:
        """Returns product version in "major.minor.patch[suffix].build" format.

        Returns:
            str: product version string
        """
        return self._resolve.GetVersionString()

    def get_version_info(self) -> Version:
        """Returns structured version information.

        Returns:
            Version: Version object with major, minor, patch components

        Example:
            >>> resolve = Resolve()
            >>> version = resolve.get_version_info()
            >>> print(f"Running Resolve {version}")
            Running Resolve 20.2.0
            >>> version.major
            20
        """
        return Version.from_list(self._version)

    def is_version_at_least(self, version_str: str) -> bool:
        """Check if current Resolve version is at least the specified version.

        Args:
            version_str: Version string like "20.0.0" or "19.1"

        Returns:
            bool: True if current version >= specified version

        Example:
            >>> resolve = Resolve()
            >>> resolve.is_version_at_least("20.0.0")
            True
            >>> resolve.is_version_at_least("21.0.0")
            False
        """
        required = Version.from_string(version_str)
        current = self.get_version_info()
        return current >= required

    def check_api_compatibility(self, api_name: str) -> Tuple[bool, str]:
        """Check if an API is compatible with current Resolve version.

        Args:
            api_name: Full API identifier (e.g., "TimelineItem.set_name")

        Returns:
            Tuple of (is_compatible, status_message)

        Example:
            >>> resolve = Resolve()
            >>> is_ok, msg = resolve.check_api_compatibility("TimelineItem.set_name")
            >>> print(f"TimelineItem.set_name: {msg}")
            TimelineItem.set_name: API available
        """
        constraint = VersionRegistry.get_constraint(api_name)
        if constraint is None:
            return (True, "No version constraints defined")

        current = self.get_version_info()
        is_compat, _, message = constraint.get_status(current)
        return (is_compat, message)

    def list_incompatible_apis(self) -> List[Tuple[str, str]]:
        """List all APIs incompatible with current Resolve version.

        Returns:
            List of (api_name, reason) tuples

        Example:
            >>> resolve = Resolve()
            >>> incompatible = resolve.list_incompatible_apis()
            >>> for api_name, reason in incompatible:
            ...     print(f"❌ {api_name}: {reason}")
        """
        current = self.get_version_info()
        incompatible = []

        for api_id, constraint in VersionRegistry.get_all_registered().items():
            is_compat, _, message = constraint.get_status(current)
            if not is_compat:
                incompatible.append((api_id, message))

        return incompatible

    def import_layout_preset(self, preset_file_path: str, preset_name: str) -> bool:
        """Imports preset from path 'preset_file_path'.
        The optional argument 'preset_name' specifies how the preset shall be named.
        If not specified, the preset is named based on the filename.
        """
        return self._resolve.ImportLayoutPreset(str(preset_file_path), preset_name)

    def load_layout_preset(self, preset_name: str) -> bool:
        """Loads UI layout from saved preset named preset_name.

        Args:
            preset_name (str):

        Returns:
            bool
        """
        return self._resolve.LoadLayoutPreset(preset_name)

    def open_page(self, page_name: str) -> bool:
        """Switches to indicated page in DaVinci Resolve.

        Args:
            page_name (str): Input can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver").

        Returns:
            bool
        """
        return self._resolve.OpenPage(page_name)

    def quit(self):
        """Quits the Resolve App."""
        self._resolve.Quit()

    def save_layout_preset(self, preset_name: str) -> bool:
        """Saves current UI layout as a preset named preset_name.

        Args:
            preset_name (str)

        Returns:
            bool
        """
        return self._resolve.SaveLayoutPreset(preset_name)

    def update_layout_preset(self, preset_name: str) -> bool:
        """Overwrites preset named 'preset_name' with current UI layout.

        Args:
            preset_name (str)

        Returns:
            bool
        """
        return self._resolve.UpdateLayoutPreset(preset_name)

    ##############################################################################################################################
    # Add at DR18.6.0
    @minimum_resolve_version("18.6.0")
    def import_render_preset(self, preset_path: str) -> bool:
        """Import a preset from presetPath (string) and set it as current preset for rendering.

        Args:
            preset_path (str): path of preset file

        Returns:
            bool: Returns True if successful, False otherwise.
        """
        return self._resolve.ImportRenderPreset(preset_path)

    @minimum_resolve_version("18.6.0")
    def export_render_preset(self, preset_name: str, export_path: str) -> bool:
        """Export a preset to a given path (string) if presetName(string) exists.

        Args:
            preset_name (str): export preset name
            export_path (str): export path

        Returns:
            bool: Returns True if successful, False otherwise.
        """
        return self._resolve.ExportRenderPreset(preset_name, export_path)

    @minimum_resolve_version("18.6.0")
    def import_burn_in_preset(self, preset_path: str) -> bool:
        """Import a data burn in preset from a given presetPath (string)

        Args:
            preset_path (str): path of preset

        Returns:
            bool: Returns True if successful, False otherwise.
        """
        return self._resolve.ImportBurnInPreset(preset_path)

    @minimum_resolve_version("18.6.0")
    def export_burn_in_preset(self, preset_name: str, export_path: str) -> bool:
        """Export a data burn in preset to a given path (string) if presetName (string) exists.

        Args:
            preset_name (str): name of export preset
            export_path (str): path to export

        Returns:
            bool: Returns True if successful, False otherwise.
        """
        return self._resolve.ExportBurnInPreset(preset_name, export_path)

    ##############################################################################################################################
    # Add at DR 19.0.0
    @minimum_resolve_version("19.0.0")
    def get_keyframe_mode(self) -> int:
        """Refer to section 'Keyframe Mode information' for details.

        Returns:
            int: currently set keyframe mode
        """
        return self._resolve.GetKeyframeMode()

    @minimum_resolve_version("19.0.0")
    def set_keyframe_mode(self, key_frame_mode: "KeyframeMode") -> bool:
        """Refer to section 'Keyframe Mode information' below for details.

        Args:
            key_frame_mode (KeyframeModeInformation): key frame mode

        Returns:
            bool: Returns True when 'keyframeMode'(enum) is successfully set.
        """
        return self._resolve.SetKeyframeMode(key_frame_mode.value)

    @minimum_resolve_version("20.3.0")
    def get_fairlight_presets(self) -> list:
        """Returns a list of Fairlight preset names.

        Returns:
            list: List of Fairlight preset names available in the system.
        """
        return self._resolve.GetFairlightPresets()
