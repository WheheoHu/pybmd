from enum import Enum
from typing import Any, ClassVar, Literal
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_serializer,
    SerializerFunctionWrapHandler,
)
from pybmd._init_bmd import _resolve_object as _resolve


class RenderSetting(BaseModel):
    """RenderSetting Object to store render setting."""

    TargetDir: str = Field(..., description="Target directory for rendered output")
    CustomName: str = Field(..., description="Custom name for the rendered file")

    SelectAllFrames: bool = Field(
        default=True, description="Whether to render all frames or use MarkIn/MarkOut"
    )
    MarkIn: int = Field(default=0, ge=0, description="Start frame for rendering")
    MarkOut: int = Field(default=0, ge=0, description="End frame for rendering")

    UniqueFilenameStyle: Literal[0, 1] = Field(
        default=0, description="Filename uniqueness style: 0 for prefix, 1 for suffix"
    )
    ExportVideo: bool = Field(default=True, description="Whether to export video")
    ExportAudio: bool = Field(default=True, description="Whether to export audio")
    FormatWidth: int = Field(
        default=1920, gt=0, description="Output video width in pixels"
    )
    FormatHeight: int = Field(
        default=1080, gt=0, description="Output video height in pixels"
    )
    FrameRate: float = Field(default=29.97, gt=0, description="Output video frame rate")

    PixelAspectRatio: str = Field(
        default="square",
        description='Pixel aspect ratio (SD: "16_9" or "4_3", other: "square" or "cinemascope")',
    )

    VideoQuality: int | Literal["Least", "Low", "Medium", "High", "Best"] = Field(
        default=0,
        description="Video quality: 0 for automatic, 1+ for bit rate, or quality level string",
    )

    AudioCodec: str = Field(default="aac", description="Audio codec to use")
    AudioBitDepth: int = Field(default=24, gt=0, description="Audio bit depth in bits")
    AudioSampleRate: int = Field(
        default=48000, gt=0, description="Audio sample rate in Hz"
    )

    ColorSpaceTag: str = Field(
        default="Same as Project",
        description="Color space tag (e.g., 'Same as Project', 'AstroDesign')",
    )

    GammaTag: str = Field(
        default="Same as Project",
        description="Gamma tag (e.g., 'Same as Project', 'ACEScct')",
    )
    ExportAlpha: bool = Field(
        default=False, description="Whether to export alpha channel"
    )

    EncodingProfile: str = Field(
        default="Main10",
        description="Encoding profile (e.g., 'Main10'). Only for H.264 and H.265",
    )

    MultiPassEncode: bool = Field(
        default=True, description="Whether to use multi-pass encoding. Only for H.264"
    )

    AlphaMode: Literal[0, 1] = Field(
        default=0,
        description="Alpha mode: 0 for Premultiplied, 1 for Straight. Only if ExportAlpha is True",
    )

    NetworkOptimization: bool = Field(
        default=True,
        description="Network optimization. Only supported by QuickTime and MP4 formats",
    )

    ExportSubtitle: bool = Field(
        default=False,
        description="Whether to export subtitles (DaVinci Resolve 20.2.0+)",
    )

    SubtitleFormat: Literal["BurnIn", "EmbeddedCaptions", "SeparateFile"] = Field(
        default="BurnIn", description="Subtitle format type"
    )

    @field_validator("VideoQuality")
    @classmethod
    def validate_video_quality(cls, v: Any) -> Any:
        """Validate VideoQuality value."""
        if isinstance(v, int) and v < 0:
            raise ValueError("VideoQuality integer value must be >= 0")
        if isinstance(v, str) and v not in ["Least", "Low", "Medium", "High", "Best"]:
            raise ValueError(
                "VideoQuality string must be one of: Least, Low, Medium, High, Best"
            )
        return v

    @field_validator("MarkOut")
    @classmethod
    def validate_mark_out(cls, v: int, info) -> int:
        """Validate that MarkOut is >= MarkIn when provided."""
        if info.data.get("MarkIn") is not None and v > 0 and v < info.data["MarkIn"]:
            raise ValueError("MarkOut must be >= MarkIn")
        return v


class BaseIndexSetting(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    _field_to_index: ClassVar[dict[str, Enum]]

    @model_serializer(mode="wrap")
    def ser_model(self, handler: SerializerFunctionWrapHandler) -> dict[float, Any]:
        data = handler(self)
        return {
            self._field_to_index[field_name].value: (
                value.value if isinstance(value, Enum) else value
            )
            for field_name, value in data.items()
        }


class CloudSyncMode(Enum):
    NONE = _resolve.CLOUD_SYNC_NONE
    PROXY_ONLY = _resolve.CLOUD_SYNC_PROXY_ONLY
    PROXY_AND_ORIG = _resolve.CLOUD_SYNC_PROXY_AND_ORIG


class CloudProjectSettingIndex(Enum):
    """Docstring for CloudProjectSettingEnum."""

    PROJECT_NAME = _resolve.CLOUD_SETTING_PROJECT_NAME
    PROJECT_MEDIA_PATH = _resolve.CLOUD_SETTING_PROJECT_MEDIA_PATH
    IS_COLLAB = _resolve.CLOUD_SETTING_IS_COLLAB
    SYNC_MODE = _resolve.CLOUD_SETTING_SYNC_MODE
    IS_CAMERA_ACCESS = _resolve.CLOUD_SETTING_IS_CAMERA_ACCESS


class CloudProjectsSetting(BaseIndexSetting):
    project_name: str = ""
    project_media_path: str = ""
    is_collab: bool = False
    sync_mode: CloudSyncMode = CloudSyncMode.PROXY_ONLY
    is_camera_access: bool = False

    model_config = ConfigDict(use_enum_values=True)

    _field_to_index: ClassVar[dict[str, CloudProjectSettingIndex]] = {
        "project_name": CloudProjectSettingIndex.PROJECT_NAME,
        "project_media_path": CloudProjectSettingIndex.PROJECT_MEDIA_PATH,
        "is_collab": CloudProjectSettingIndex.IS_COLLAB,
        "sync_mode": CloudProjectSettingIndex.SYNC_MODE,
        "is_camera_access": CloudProjectSettingIndex.IS_CAMERA_ACCESS,
    }


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
    SUBTITLE_DEFAULT = _resolve.AUTO_CAPTION_SUBTITLE_DEFAULT
    TELETEXT = _resolve.AUTO_CAPTION_TELETEXT
    NETFLIX = _resolve.AUTO_CAPTION_NETFLIX


class LineBreakTypes(Enum):
    LINE_SINGLE = _resolve.AUTO_CAPTION_LINE_SINGLE
    LINE_DOUBLE = _resolve.AUPTO_CAPTION_LINE_DOUBLE


class AutoCaptionSettingsIndex(Enum):
    LANGUAGE = _resolve.SUBTITLE_LANGUAGE
    CAPTION_PRESET = _resolve.SUBTITLE_CAPTION_PRESET
    CHARS_PER_LINE = _resolve.SUBTITLE_CHARS_PER_LINE
    LINE_BREAK = _resolve.SUBTITLE_LINE_BREAK
    GAP = _resolve.SUBTITLE_GAP


class AutoCaptionSettings(BaseIndexSetting):
    subtitle_language: LanguageID = LanguageID.AUTO
    subtitle_caption_preset: PresetType = PresetType.SUBTITLE_DEFAULT
    subtitle_chars_per_line: int = 42
    subtitle_line_break: LineBreakTypes = LineBreakTypes.LINE_SINGLE
    subtitle_gap: int = 0
    _field_to_index: ClassVar[dict[str, AutoCaptionSettingsIndex]] = {
        "subtitle_language": AutoCaptionSettingsIndex.LANGUAGE,
        "subtitle_caption_preset": AutoCaptionSettingsIndex.CAPTION_PRESET,
        "subtitle_chars_per_line": AutoCaptionSettingsIndex.CHARS_PER_LINE,
        "subtitle_line_break": AutoCaptionSettingsIndex.LINE_BREAK,
        "subtitle_gap": AutoCaptionSettingsIndex.GAP,
    }


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


#################################
# Audio Sync Settings


class AudioSyncMode(Enum):
    AUDIO_SYNC_WAVEFORM = _resolve.AUDIO_SYNC_WAVEFORM
    AUDIO_SYNC_TIMECODE = _resolve.AUDIO_SYNC_TIMECODE


class AudioSyncChannel(Enum):
    AUDIO_SYNC_CHANNEL_AUTOMATIC = -1
    AUDIO_SYNC_CHANNEL_MIX = -2


class AudioSyncSettingIndex(Enum):
    AUDIO_SYNC_MODE = _resolve.AUDIO_SYNC_MODE
    AUDIO_SYNC_CHANNEL_NUMBER = _resolve.AUDIO_SYNC_CHANNEL_NUMBER
    AUDIO_SYNC_RETAIN_EMBEDDED_AUDIO = _resolve.AUDIO_SYNC_RETAIN_EMBEDDED_AUDIO
    AUDIO_SYNC_RETAIN_VIDEO_METADATA = _resolve.AUDIO_SYNC_RETAIN_VIDEO_METADATA


class AudioSyncSetting(BaseIndexSetting):
    _audioSyncMode: AudioSyncMode = AudioSyncMode.AUDIO_SYNC_TIMECODE
    _channelNumber: int = 1
    _retainEmbeddedAudio: bool = False
    _retainVideoMetadata: bool = False
    _field_to_index: ClassVar[dict[str, AudioSyncSettingIndex]] = {
        "_audioSyncMode": AudioSyncSettingIndex.AUDIO_SYNC_MODE,
        "_channelNumber": AudioSyncSettingIndex.AUDIO_SYNC_CHANNEL_NUMBER,
        "_retainEmbeddedAudio": AudioSyncSettingIndex.AUDIO_SYNC_RETAIN_EMBEDDED_AUDIO,
        "_retainVideoMetadata": AudioSyncSettingIndex.AUDIO_SYNC_RETAIN_VIDEO_METADATA,
    }
