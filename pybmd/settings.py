from enum import Enum, EnumType, auto
from dataclasses import dataclass
from typing import Any, TypedDict, Unpack

from pybmd.error import ResolveInitError

from pybmd._init_bmd import _resolve_object as _resolve


if _resolve is None:
    raise ResolveInitError


class SettingParameter(object):
    """docstring for SettingParamater."""

    def __init__(self, parameter_index: float, parameter_value: Any):
        super(SettingParameter, self).__init__()
        self.__parameter_index = parameter_index
        self.__parameter_value = parameter_value

    @property
    def parameter_index(self):
        return self.__parameter_index

    @property
    def parameter_value(self):
        return self.__parameter_value


@dataclass
class RenderSetting():
    """RenderSetting Object to store render setting."""
    SelectAllFrames: bool
    MarkIn: int
    MarkOut: int
    TargetDir: str
    CustomName: str
    UniqueFilenameStyle: int  # 0 for prefix, 1 for suffix
    ExportVideo: bool
    ExportAudio: bool
    FormatWidth: int
    FormatHeight: int
    FrameRate: float

    # (for SD resolution: "16_9" or "4_3") (other resolutions: "square" or "cinemascope")
    PixelAspectRatio: str

    #  possible values for current codec (if applicable):
    #  0(int) - will set quality to automatic
    # [1 -> MAX] (int) - will set input bit rate
    # ["Least", "Low", "Medium", "High", "Best"] (String) - will set input quality level
    VideoQuality: Any

    AudioCodec: str
    AudioBitDepth: int
    AudioSampleRate: int

    # example: "Same as Project", "AstroDesign"
    ColorSpaceTag: str

    # example: "Same as Project", "ACEScct"
    GammaTag: str
    ExportAlpha: bool

    # (example: "Main10"). Can only be set for H.264 and H.265.
    EncodingProfile: str

    # Can onlt be set for H.264.
    MultiPassEncode: bool

    # 0 - Premultipled, 1 - Straight. Can only be set if "ExportAlpha" is true.
    AlphaMode: int

    # Only supported by QuickTime and MP4 formats.
    NetworkOptimization: bool


class CloudSyncMode(Enum):
    """Docstring for CloudSyncMode."""
    NONE: float = _resolve.CLOUD_SYNC_NONE
    PROXY_ONLY: float = _resolve.CLOUD_SYNC_PROXY_ONLY
    PROXY_AND_ORIG: float = _resolve.CLOUD_SYNC_PROXY_AND_ORIG


class CloudProjectSettingEnum(Enum):
    """Docstring for CloudProjectSettingEnum."""

    PROJECT_NAME: str = _resolve.CLOUD_SETTING_PROJECT_NAME
    PROJECT_MEDIA_PATH: str = _resolve.CLOUD_SETTING_PROJECT_MEDIA_PATH
    IS_COLLAB: bool = _resolve.CLOUD_SETTING_IS_COLLAB
    SYNC_MODE: float = _resolve.CLOUD_SETTING_SYNC_MODE
    IS_CAMERA_ACCESS: bool = _resolve.CLOUD_SETTING_IS_CAMERA_ACCESS


class CloudProjectsSetting():
    """Setting for CloudProject"""

    def __init__(self,
                 cloud_setting_project_name: str = _resolve.CLOUD_SETTING_PROJECT_NAME,
                 cloud_setting_project_media_path: str = _resolve.CLOUD_SETTING_PROJECT_MEDIA_PATH,
                 cloud_setting_is_collab: bool = _resolve.CLOUD_SETTING_IS_COLLAB,
                 cloud_setting_sync_mode: CloudSyncMode = _resolve.CLOUD_SETTING_SYNC_MODE,
                 cloud_setting_is_camera_access: bool = _resolve.CLOUD_SETTING_IS_CAMERA_ACCESS):
        """Initialize CloudProjectsSetting.

        Args:
            cloud_setting_project_name (str, optional): project name for Cloud Project. Defaults to "".
            cloud_setting_project_media_path (str, optional): media path for Cloud Project. Defaults to "".
            cloud_setting_is_collab (bool, optional): collabration mode. Defaults to False.
            cloud_setting_sync_mode (CloudSyncMode, optional): sync mode. Defaults to CloudSyncMode.PROXY_ONLY.
            cloud_setting_is_camera_access (bool, optional): camera access mode. Defaults to False.

        Examples:
            >>> from pybmd.settings import CloudProjectsSetting,CloudSyncMode
            >>> settings=CloudProjectsSetting()
            >>> print(settings.asdict())
            {0.0: '', 1.0: '', 2.0: False, 3.0: 1.0, 4.0: False}
            >>> settings.cloud_setting_sync_mode=CloudSyncMode.PROXY_AND_ORIG
            >>> print(settings.asdict()) 
            {0.0: '', 1.0: '', 2.0: False, 3.0: 2.0, 4.0: False}
        """
        self.__cloud_setting_project_name = SettingParameter(
            0.0, cloud_setting_project_name)
        self.__cloud_setting_project_media_path = SettingParameter(
            1.0, cloud_setting_project_media_path)
        self.__cloud_setting_is_collab = SettingParameter(
            2.0, cloud_setting_is_collab)
        self.__cloud_setting_sync_mode = SettingParameter(
            3.0, cloud_setting_sync_mode.value)
        self.__cloud_setting_is_camera_access = SettingParameter(
            4.0, cloud_setting_is_camera_access)

    @property
    def cloud_setting_project_name(self) -> str:
        return self.__cloud_setting_project_name.parameter_value

    @cloud_setting_project_name.setter
    def cloud_setting_project_name(self, value: str) -> None:
        self.__cloud_setting_project_name = SettingParameter(
            0.0, value)

    @property
    def cloud_setting_project_media_path(self) -> str:
        return self.__cloud_setting_project_media_path.parameter_value

    @cloud_setting_project_media_path.setter
    def cloud_setting_project_media_path(self, value: str) -> None:
        self.__cloud_setting_project_media_path = SettingParameter(
            1.0, value)

    @property
    def cloud_setting_is_collab(self) -> bool:
        return self.__cloud_setting_is_collab.parameter_value

    @cloud_setting_is_collab.setter
    def cloud_setting_is_collab(self, value: bool) -> None:
        self.__cloud_setting_is_collab = SettingParameter(
            2.0, value)

    @property
    def cloud_setting_sync_mode(self) -> CloudSyncMode:
        return self.__cloud_setting_sync_mode.parameter_value

    @cloud_setting_sync_mode.setter
    def cloud_setting_sync_mode(self, value: CloudSyncMode) -> None:
        self.__cloud_setting_sync_mode = SettingParameter(
            3.0, value.value)

    @property
    def cloud_setting_is_camera_access(self) -> bool:
        return self.__cloud_setting_is_camera_access.parameter_value

    @cloud_setting_is_camera_access.setter
    def cloud_setting_is_camera_access(self, value: bool) -> None:
        self.__cloud_setting_is_camera_access = SettingParameter(
            4.0, value)

    def asdict(self):
        return {self.__cloud_setting_project_name.parameter_index: self.__cloud_setting_project_name.parameter_value,
                self.__cloud_setting_project_media_path.parameter_index: self.__cloud_setting_project_media_path.parameter_value,
                self.__cloud_setting_is_collab.parameter_index: self.__cloud_setting_is_collab.parameter_value,
                self.__cloud_setting_sync_mode.parameter_index: self.__cloud_setting_sync_mode.parameter_value,
                self.__cloud_setting_is_camera_access.parameter_index: self.__cloud_setting_is_camera_access.parameter_value}


class LanguageID(Enum):
    """Docstring for LanguageID."""
    AUTO = _resolve.AUTO_CAPTION_AUTO
    DANISH = _resolve.AUTO_CAPTION_DANISH
    DUTCH = _resolve.AUTO_CAPTION_DUTCH
    ENGLISH = _resolve.AUTO_CAPTION_ENGLISH
    FRENCH = _resolve.AUTO_CAPTION_FRENCH
    GERMAN = _resolve.AUTO_CAPTION_GERMAN
    ITALIAN = _resolve.AUTO_CAPTION_ITALIAN
    JAPANESE = _resolve.AUTO_CAPTION_JAPANESE
    KOREAN = _resolve.AUTO_CAPTION_KOREAN
    MANDARIN_SIMPLIFIED = _resolve.AUTO_CAPTION_MANDARIN_SIMPLIFIED
    MANDARIN_TRADITIONAL = _resolve.AUTO_CAPTION_MANDARIN_TRADITIONAL
    NORWEGIAN = _resolve.AUTO_CAPTION_NORWEGIAN
    PORTUGUESE = _resolve.AUTO_CAPTION_PORTUGUESE
    RUSSIAN = _resolve.AUTO_CAPTION_RUSSIAN
    SPANISH = _resolve.AUTO_CAPTION_SPANISH
    SWEDISH = _resolve.AUTO_CAPTION_SWEDISH


#######################################
# AUTO CAPTION SETTINGS

class PresetType(Enum):
    """Docstring for PresetType."""
    SUBTITLE_DEFAULT = _resolve.AUTO_CAPTION_SUBTITLE_DEFAULT
    TELETEXT = _resolve.AUTO_CAPTION_TELETEXT
    NETFLIX = _resolve.AUTO_CAPTION_NETFLIX


class LineBreakTypes(Enum):
    """Docstring for LineBreakTypes."""
    LINE_SINGLE = _resolve.AUTO_CAPTION_LINE_SINGLE
    LINE_DOUBLE = _resolve.AUPTO_CAPTION_LINE_DOUBLE


class AutoCaptionSettingsEnum(Enum):
    """Docstring for MyEnum."""
    LANGUAGE = _resolve.SUBTITLE_LANGUAGE
    CAPTION_PRESET = _resolve.SUBTITLE_CAPTION_PRESET
    CHARS_PER_LINE = _resolve.SUBTITLE_CHARS_PER_LINE
    LINE_BREAK = _resolve.SUBTITLE_LINE_BREAK
    GAP = _resolve.SUBTITLE_GAP


class AutoCaptionSettings():
    """Setting object for AutoCaptionSettings
    Args:
        subtitle_language: LanguageID
        subtitle_caption_preset: PresetType
        subtitle_chars_per_line: int
        subtitle_line_break: LineBreakTypes
        subtitle_gap: int

    Examples:
    >>> from pybmd.settings import AutoCaptionSettings, LanguageID
    >>> settings=AutoCaptionSettings()
    >>> print(settings.asdict())
    >>> settings.subtitle_language=LanguageID.ENGLISH
    >>> print(settings.asdict())
    """

    def __init__(self,
                 subtitle_language: LanguageID = LanguageID.AUTO,
                 subtitle_caption_preset: PresetType = PresetType.SUBTITLE_DEFAULT,
                 subtitle_chars_per_line: int = 42,
                 subtitle_line_break: LineBreakTypes = LineBreakTypes.LINE_SINGLE,
                 subtitle_gap: int = 0):
        self.__subtitle_language = SettingParameter(
            0.0, subtitle_language.value)
        self.__subtitle_caption_preset = SettingParameter(
            1.0, subtitle_caption_preset.value)
        self.__subtitle_chars_per_line = SettingParameter(
            2.0, subtitle_chars_per_line)
        self.__subtitle_line_break = SettingParameter(
            3.0, subtitle_line_break.value)
        self.__subtitle_gap = SettingParameter(4.0, subtitle_gap)

    @property
    def subtitle_language(self):
        return self.__subtitle_language.parameter_value

    @subtitle_language.setter
    def subtitle_language(self, language: LanguageID):
        self.__subtitle_language = SettingParameter(
            0.0, language.value)

    @property
    def subtitle_caption_preset(self):
        return self.__subtitle_caption_preset.parameter_value

    @subtitle_caption_preset.setter
    def subtitle_caption_preset(self, preset: PresetType):
        self.__subtitle_caption_preset = SettingParameter(
            1.0, preset.value)

    @property
    def subtitle_chars_per_line(self):
        return self.__subtitle_chars_per_line.parameter_value

    @subtitle_chars_per_line.setter
    def subtitle_chars_per_line(self, value: int):
        self.__subtitle_chars_per_line = SettingParameter(
            2.0, value)

    @property
    def subtitle_line_break(self):
        return self.__subtitle_line_break.parameter_value

    @subtitle_line_break.setter
    def subtitle_line_break(self, line_break_type: LineBreakTypes):
        self.__subtitle_line_break = SettingParameter(
            3.0, line_break_type.value)

    @property
    def subtitle_gap(self):
        return self.__subtitle_gap.parameter_value

    @subtitle_gap.setter
    def subtitle_gap(self, value: int):
        self.__subtitle_gap = SettingParameter(4.0, value)

    def asdict(self) -> dict[float, Any]:
        """return dict of setting parameters

        Returns:
            dict[float, Any]: returned dict
        """
        return {self.__subtitle_language.parameter_index: self.__subtitle_language.parameter_value,
                self.__subtitle_caption_preset.parameter_index: self.__subtitle_caption_preset.parameter_value,
                self.__subtitle_chars_per_line.parameter_index: self.__subtitle_chars_per_line.parameter_value,
                self.__subtitle_line_break.parameter_index: self.__subtitle_line_break.parameter_value,
                self.__subtitle_gap.parameter_index: self.__subtitle_gap.parameter_value}


class KeyframeMode(Enum):
    """Docstring for KeyframeModeInformation."""
    KEYFRAME_MODE_ALL = 0
    KEYFRAME_MODE_COLOR = 1
    KEYFRAME_MODE_SIZING = 2


###################################
# Project and Clip properties

class CloudSyncState(Enum):
    """Docstring for CloudSyncState."""
    CLOUD_SYNC_DEFAULT = -1
    CLOUD_SYNC_DOWNLOAD_IN_QUEUE = 0
    CLOUD_SYNC_DOWNLOAD_IN_PROGRESS = 1
    CLOUD_SYNC_DOWNLOAD_SUCCESS = 2
    CLOUD_SYNC_DOWNLOAD_FAIL = 3
    CLOUD_SYNC_DOWNLOAD_NOT_FOUND = 4

    CLOUD_SYNC_UPLOAD_IN_QUEUE = 5
    CLOUD_SYNC_UPLOAD_IN_PROGRESS = 6
    CLOUD_SYNC_UPLOAD_SUCCESS = 7
    CLOUD_SYNC_UPLOAD_FAIL = 8
    CLOUD_SYNC_UPLOAD_NOT_FOUND = 9
    
    ## Add at DR 19.0.1
    CLOUD_SYNC_SUCCESS = 10
