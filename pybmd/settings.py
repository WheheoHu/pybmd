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

if not _resolve:
    raise ImportError("DaVinci Resolve object is not initialized.")


class RenderSetting(BaseModel):
    """RenderSetting Object to store render setting.

    All fields are optional. Only fields explicitly set by the user are forwarded
    to DaVinci Resolve (see ``Project.set_render_settings``); unset fields keep
    their current value in DR. No preset defaults are baked into the model.
    """

    TargetDir: str | None = Field(
        default=None, description="Target directory for rendered output"
    )
    CustomName: str | None = Field(
        default=None, description="Custom name for the rendered file"
    )

    SelectAllFrames: bool | None = Field(
        default=None, description="Whether to render all frames or use MarkIn/MarkOut"
    )
    MarkIn: int | None = Field(default=None, ge=0, description="Start frame for rendering")
    MarkOut: int | None = Field(default=None, ge=0, description="End frame for rendering")

    UniqueFilenameStyle: Literal[0, 1] | None = Field(
        default=None, description="Filename uniqueness style: 0 for prefix, 1 for suffix"
    )
    ExportVideo: bool | None = Field(default=None, description="Whether to export video")
    ExportAudio: bool | None = Field(default=None, description="Whether to export audio")
    FormatWidth: int | None = Field(default=None, gt=0, description="Output video width in pixels")
    FormatHeight: int | None = Field(default=None, gt=0, description="Output video height in pixels")
    FrameRate: float | None = Field(default=None, gt=0, description="Output video frame rate")

    PixelAspectRatio: str | None = Field(
        default=None,
        description='Pixel aspect ratio (SD: "16_9" or "4_3", other: "square" or "cinemascope")',
    )

    VideoQuality: int | Literal["Least", "Low", "Medium", "High", "Best"] | None = Field(
        default=None,
        description="Video quality: 0 for automatic, 1+ for bit rate, or quality level string",
    )

    AudioCodec: str | None = Field(default=None, description="Audio codec to use")
    AudioBitDepth: int | None = Field(default=None, gt=0, description="Audio bit depth in bits")
    AudioSampleRate: int | None = Field(default=None, gt=0, description="Audio sample rate in Hz")

    ColorSpaceTag: str | None = Field(
        default=None,
        description="Color space tag (e.g., 'Same as Project', 'AstroDesign')",
    )

    GammaTag: str | None = Field(
        default=None,
        description="Gamma tag (e.g., 'Same as Project', 'ACEScct')",
    )
    ExportAlpha: bool | None = Field(default=None, description="Whether to export alpha channel")

    EncodingProfile: str | None = Field(
        default=None,
        description="Encoding profile (e.g., 'Main10'). Only for H.264 and H.265",
    )

    MultiPassEncode: bool | None = Field(
        default=None, description="Whether to use multi-pass encoding. Only for H.264"
    )

    AlphaMode: Literal[0, 1] | None = Field(
        default=None,
        description="Alpha mode: 0 for Premultiplied, 1 for Straight. Only if ExportAlpha is True",
    )

    NetworkOptimization: bool | None = Field(
        default=None,
        description="Network optimization. Only supported by QuickTime and MP4 formats",
    )

    ExportSubtitle: bool | None = Field(
        default=None, description="Whether to export subtitles (DaVinci Resolve 20.2.0+)"
    )

    SubtitleFormat: Literal["BurnIn", "EmbeddedCaptions", "SeparateFile"] | None = Field(
        default=None, description="Subtitle format type"
    )

    @field_validator("VideoQuality")
    @classmethod
    def validate_video_quality(cls, v: Any) -> Any:
        """Validate VideoQuality value."""
        if v is None:
            return v
        if isinstance(v, int) and v < 0:
            raise ValueError("VideoQuality integer value must be >= 0")
        if isinstance(v, str) and v not in ["Least", "Low", "Medium", "High", "Best"]:
            raise ValueError(
                "VideoQuality string must be one of: Least, Low, Medium, High, Best"
            )
        return v

    @field_validator("MarkOut")
    @classmethod
    def validate_mark_out(cls, v: int | None, info) -> int | None:
        """Validate that MarkOut is >= MarkIn when both provided."""
        if v is None:
            return v
        mark_in = info.data.get("MarkIn")
        if mark_in is not None and v > 0 and v < mark_in:
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


###################################
# Speech Generation Settings (DR 21.0.2)


class SpeechGenerationSettings(BaseModel):
    """Settings for ``Project.generate_speech``.

    String-keyed dictionary forwarded to DaVinci Resolve. All fields are optional;
    only fields explicitly set are sent (use ``model_dump(exclude_none=True)``).
    """

    TextInput: str | None = Field(
        default=None, description="Text to synthesize (max 350 chars)"
    )
    VoiceModel: str | None = Field(
        default=None, description='Voice model, e.g. "Female 1", "Male 1", "Custom Voice"'
    )
    CustomVoiceFile: str | None = Field(
        default=None, description="Full path of the custom voice file"
    )
    Speed: int | None = Field(default=None, description="Speech speed")
    Variation: int | None = Field(default=None, description="Speech variation")
    Pitch: int | None = Field(default=None, description="Speech pitch")
    GenerationID: int | None = Field(default=None, description="Generation identifier")
    Filename: str | None = Field(default=None, description="Output file name")
    AddToTimeline: bool | None = Field(
        default=None, description="Whether to add the generated clip to the timeline"
    )
    AudioTrack: int | None = Field(
        default=None, description="Audio track index to place the clip on"
    )


###################################
# Motion Deblur Settings (DR 21.0.2)


class MotionDeblurSettings(BaseModel):
    """Settings (``deblurOption``) for ``MediaPoolItem.remove_motion_blur`` and
    ``Folder.remove_motion_blur``.

    String-keyed dictionary forwarded to DaVinci Resolve. All fields are optional;
    only fields explicitly set are sent (use ``model_dump(exclude_none=True)``).
    """

    FileName: str | None = Field(default=None, description="Output file name")
    Format: str | None = Field(
        default=None, description='Container format, e.g. "mov", "mp4"'
    )
    Codec: str | None = Field(
        default=None, description='Codec, e.g. "H264", "ProRes422"'
    )
    EncodingProfile: str | None = Field(
        default=None,
        description='Encoding profile, e.g. "Main10". Only for H.264 and H.265',
    )
    UseExtremeMode: bool | None = Field(default=None, description="Use extreme mode")
    UseMarkInMarkOut: bool | None = Field(
        default=None, description="Only process between mark in and mark out"
    )
    RenderAtSourceRes: bool | None = Field(
        default=None, description="Render at source resolution"
    )
    UseMoreGpuMemory: bool | None = Field(
        default=None, description="Allow using more GPU memory"
    )
    Encoder: str | None = Field(
        default=None, description="Encoder (Native or MainConcept). Only for H.265"
    )


###################################
# Marker Color (DR 21.0.2)


class MarkerColor(Enum):
    """Marker color constants used by ``analyze_for_slate``."""

    BLUE = _resolve.MARKER_BLUE
    CYAN = _resolve.MARKER_CYAN
    GREEN = _resolve.MARKER_GREEN
    YELLOW = _resolve.MARKER_YELLOW
    RED = _resolve.MARKER_RED
    PINK = _resolve.MARKER_PINK
    PURPLE = _resolve.MARKER_PURPLE
    FUCHSIA = _resolve.MARKER_FUCHSIA
    ROSE = _resolve.MARKER_ROSE
    LAVENDER = _resolve.MARKER_LAVENDER
    SKY = _resolve.MARKER_SKY
    MINT = _resolve.MARKER_MINT
    LEMON = _resolve.MARKER_LEMON
    SAND = _resolve.MARKER_SAND
    COCOA = _resolve.MARKER_COCOA
    CREAM = _resolve.MARKER_CREAM
