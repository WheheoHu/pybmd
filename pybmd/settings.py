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

    ClipStartFrame: int | None = Field(
        default=None,
        ge=0,
        description="Start frame number of the rendered clip, when rendering individual clips",
    )

    TimelineStartTimecode: str | None = Field(
        default=None,
        description='Start timecode of the rendered timeline, e.g. "01:00:00:00"',
    )

    ReplaceExistingFilesInPlace: bool | None = Field(
        default=None,
        description="Whether to overwrite existing files in place instead of creating unique names",
    )

    UseFullExtents: bool | None = Field(
        default=None,
        description="Render the full extents of each clip, ignoring its trimmed in/out points "
        "(DaVinci Resolve 21.0.4+)",
    )

    AddFrameHandles: int | None = Field(
        default=None,
        ge=0,
        description="Number of extra frames rendered before and after each clip "
        "(DaVinci Resolve 21.0.4+)",
    )

    DataBurnIn: str | None = Field(
        default=None,
        description='Data burn-in preset name to apply to the render, or "" for none '
        "(DaVinci Resolve 21.0.4+)",
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
    AUDIO_SYNC_CHANNEL_AUTOMATIC = _resolve.AUDIO_SYNC_CHANNEL_AUTOMATIC
    AUDIO_SYNC_CHANNEL_MIX = _resolve.AUDIO_SYNC_CHANNEL_MIX


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


###################################
# Clone Tool Settings (DR 21.1.0)


class CloneChecksumType(Enum):
    """Checksum types accepted by ``CloneToolSettings.ChecksumType``."""

    NONE = _resolve.CLONE_CHECKSUM_TYPE_NONE
    FILESIZE = _resolve.CLONE_CHECKSUM_TYPE_FILESIZE
    CRC32 = _resolve.CLONE_CHECKSUM_TYPE_CRC32
    MD5 = _resolve.CLONE_CHECKSUM_TYPE_MD5
    SHA256 = _resolve.CLONE_CHECKSUM_TYPE_SHA256
    SHA512 = _resolve.CLONE_CHECKSUM_TYPE_SHA512
    XXH_64 = _resolve.CLONE_CHECKSUM_TYPE_XXH_64


class CloneToolSettings(BaseModel):
    """Settings (``cloneToolSettings``) for ``MediaStorage.set_clone_tool_settings``.

    These settings apply to subsequent ``MediaStorage.start_clone_media`` calls and to
    the Clone Tool in the UI. All fields are optional; only fields explicitly set are
    sent (use ``model_dump(exclude_none=True)``).
    """

    model_config = ConfigDict(use_enum_values=True)

    PreserveFolderName: bool | None = Field(
        default=None, description="Preserve the source folder name (default: False)"
    )
    ChecksumType: CloneChecksumType | None = Field(
        default=None,
        description="Checksum type used to verify the clone (default: MD5)",
    )


class CloneStatus(BaseModel):
    """Status dictionary returned by ``MediaStorage.get_clone_status``."""

    JobStatus: str | None = Field(
        default=None,
        description='Clone job status: "Complete", "Cloning", "InProgress", "Cancelled" '
        'or "Failed". "Complete" when no clone job has been started yet. Kept as a plain '
        "str because DaVinci Resolve reports statuses beyond the documented set",
    )
    CompletionPercentage: float | None = Field(
        default=None, description="Clone progress from 0.0 to 100.0"
    )
    Error: str | None = Field(
        default=None, description='Error message, set when JobStatus is "Failed"'
    )


###################################
# Normalize Audio Options (DR 21.1.0)


class NormalizeAudioSetLevelMode(Enum):
    """Set level modes accepted by ``NormalizeAudioOptions.setLevelMode``."""

    RELATIVE = _resolve.NORMALIZE_AUDIO_SET_LEVEL_RELATIVE
    INDEPENDENT = _resolve.NORMALIZE_AUDIO_SET_LEVEL_INDEPENDENT


class NormalizeAudioOptions(BaseModel):
    """Settings (``normalizeAudioOptions``) for ``Timeline.normalize_audio_level``.

    Note the lowercase/camelCase keys - these are the exact key names DaVinci Resolve
    expects. All fields are optional; only fields explicitly set are sent
    (use ``model_dump(exclude_none=True)``).
    """

    model_config = ConfigDict(use_enum_values=True)

    normalizationMode: str | None = Field(
        default=None,
        description="One of the mode names returned by ``Timeline.get_normalize_audio_modes()`` "
        '(default: "Sample Peak Program")',
    )
    targetLevel: float | None = Field(
        default=None, description="Target level in dBFS, e.g. -9.0"
    )
    targetLoudness: float | None = Field(
        default=None, description="Target loudness in LKFS, e.g. -24.0"
    )
    setLevelMode: NormalizeAudioSetLevelMode | None = Field(
        default=None, description="Set level mode (default: RELATIVE)"
    )


###################################
# Auto Align Options (DR 21.1.0)


class AutoAlignSyncUsing(Enum):
    """Sync modes accepted by ``AutoAlignOptions.SyncUsing``."""

    WAVEFORM = _resolve.AUTO_ALIGN_CLIPS_USING_WAVEFORM
    TIMECODE = _resolve.AUTO_ALIGN_CLIPS_USING_TIMECODE


class AutoAlignWaveformTrack(Enum):
    """Special track values accepted by ``AutoAlignOptions.UseTrack``."""

    MIX = _resolve.AUTO_ALIGN_CLIPS_WAVEFORM_TRACK_MIX
    AUTOMATIC = _resolve.AUTO_ALIGN_CLIPS_WAVEFORM_TRACK_AUTOMATIC


class AutoAlignOptions(BaseModel):
    """Settings (``autoAlignOptions``) for ``Timeline.auto_align_clips``.

    All fields are optional; only fields explicitly set are sent
    (use ``model_dump(exclude_none=True)``).
    """

    model_config = ConfigDict(use_enum_values=True)

    SyncUsing: AutoAlignSyncUsing | None = Field(
        default=None, description="What to sync on (default: TIMECODE)"
    )
    UseTrack: int | AutoAlignWaveformTrack | None = Field(
        default=None,
        description="Audio track index (1, 2, ...) used for waveform comparison, or an "
        "``AutoAlignWaveformTrack`` constant. Only used when SyncUsing is WAVEFORM (default: 1)",
    )


###################################
# Encrypt DCTL Options (DR 21.1.0)


class EncryptDCTLOptions(BaseModel):
    """Settings (``encryptDCTLOptions``) for ``Resolve.encrypt_dctl``.

    All fields are optional; only fields explicitly set are sent
    (use ``model_dump(exclude_none=True)``).
    """

    Name: str | None = Field(
        default=None, description="Output filename. Defaults to the input filename"
    )
    Expiry: str | None = Field(
        default=None,
        description="Expiry date as a valid ISO 8601 string. No expiry when the value is empty",
    )
    OutputFolder: str | None = Field(
        default=None, description="Output folder. Defaults to the user's home folder"
    )


###################################
# Output Blanking (DR 21.1.0)


class OutputBlanking(BaseModel):
    """Blanking dictionary used by ``Timeline`` / ``TimelineItem`` output blanking.

    All fields are optional; only fields explicitly set are sent
    (use ``model_dump(exclude_none=True)``).
    """

    Top: int | None = Field(default=None, ge=0, description="Top blanking in pixels")
    Bottom: int | None = Field(
        default=None, ge=0, description="Bottom blanking in pixels"
    )
    Left: int | None = Field(default=None, ge=0, description="Left blanking in pixels")
    Right: int | None = Field(default=None, ge=0, description="Right blanking in pixels")


###################################
# Fade Info (DR 21.1.0)


class FadeInfo(BaseModel):
    """Fades dictionary used by ``TimelineItem.get_fades`` / ``set_fades``.

    The durations apply to the item's video or audio fader, depending on the type of the
    timeline item. All fields are optional; only fields explicitly set are sent
    (use ``model_dump(exclude_none=True)``).
    """

    FadeIn: int | None = Field(
        default=None, ge=0, description="Fade in duration in frames"
    )
    FadeOut: int | None = Field(
        default=None, ge=0, description="Fade out duration in frames"
    )


###################################
# Speed Options (DR 21.1.0)


class SpeedOptions(BaseModel):
    """Settings (``speedOptions``) for ``TimelineItem.set_speed``.

    All fields are optional; only fields explicitly set are sent
    (use ``model_dump(exclude_none=True)``).
    """

    Percentage: float | None = Field(
        default=None,
        description="Clip speed in percent, e.g. 110.0. 0.0 freezes the frame",
    )
    PitchCorrection: bool | None = Field(
        default=None,
        description="Pitch correction of the linked audio. Defaults to the clip's existing state",
    )
    StretchKeyframesToFit: bool | None = Field(
        default=None, description="Stretch keyframes to fit the new duration (default: False)"
    )
    RippleTimeline: bool | None = Field(
        default=None, description="Ripple the timeline after the change (default: False)"
    )


###################################
# Transition Options (DR 21.1.0)


class TransitionOptions(BaseModel):
    """Settings (``transitionOptions``) for ``TimelineItem.add_transition``.

    All fields are optional; only fields explicitly set are sent
    (use ``model_dump(exclude_none=True)``).
    """

    type: str | None = Field(
        default=None, description='Transition type name, e.g. "Cross Dissolve"'
    )
    category: Literal["simple", "fusion", "ofx", "audio"] | None = Field(
        default=None, description="Transition category"
    )
    position: Literal["start", "end"] | None = Field(
        default=None, description="Edge of the item to attach the transition to"
    )
    alignment: Literal["left", "center", "right"] | None = Field(
        default=None, description="Placement relative to the edge"
    )
    duration: int | None = Field(
        default=None,
        gt=0,
        description="Duration in frames. Automatically calculated when omitted",
    )


###################################
# Multicam Options (DR 21.1.0)


class MulticamAngleSyncMode(Enum):
    """Angle sync modes accepted by ``MulticamOptions.angleSyncMode``."""

    IN = _resolve.MULTICAM_ANGLE_SYNC_IN
    OUT = _resolve.MULTICAM_ANGLE_SYNC_OUT
    TIMECODE = _resolve.MULTICAM_ANGLE_SYNC_TIMECODE
    AUDIO = _resolve.MULTICAM_ANGLE_SYNC_AUDIO
    MARKER = _resolve.MULTICAM_ANGLE_SYNC_MARKER


class MulticamAudioMode(Enum):
    """Audio modes accepted by ``MulticamOptions.multicamAudioMode``."""

    ADAPTIVE = _resolve.MULTICAM_AUDIO_ADAPTIVE
    SOURCE = _resolve.MULTICAM_AUDIO_SOURCE
    REFERENCE = _resolve.MULTICAM_AUDIO_REFERENCE
    ALL = _resolve.MULTICAM_AUDIO_ALL


class MulticamAngleNameMode(Enum):
    """Angle name modes accepted by ``MulticamOptions.angleNameMode``."""

    SEQUENTIAL = _resolve.MULTICAM_ANGLE_NAME_SEQUENTIAL
    ANGLE = _resolve.MULTICAM_ANGLE_NAME_ANGLE
    CAMERA = _resolve.MULTICAM_ANGLE_NAME_CAMERA
    CLIP = _resolve.MULTICAM_ANGLE_NAME_CLIP
    FILE = _resolve.MULTICAM_ANGLE_NAME_FILE


class MulticamDetectSameCameraClipsMode(Enum):
    """Detection modes accepted by ``MulticamOptions.detectSameCameraClipsMode``."""

    BY_CAMERA_NUMBER = _resolve.MULTICAM_DETECT_BY_CAMERA_NUMBER
    BY_ANGLE = _resolve.MULTICAM_DETECT_BY_ANGLE
    BY_REEL_NUMBER = _resolve.MULTICAM_DETECT_BY_REEL_NUMBER
    BY_REEL_NAME = _resolve.MULTICAM_DETECT_BY_REEL_NAME
    BY_ROLL_CARD = _resolve.MULTICAM_DETECT_BY_ROLL_CARD
    NONE = _resolve.MULTICAM_DETECT_NONE


class FlattenMulticamGradeOption(Enum):
    """Grade options accepted by ``TimelineItem.flatten_multicam``."""

    COPY_GRADE = _resolve.FLATTEN_MULTICAM_COPY_GRADE
    RETAIN_GRADE_FROM_ANGLE = _resolve.FLATTEN_MULTICAM_RETAIN_GRADE_FROM_ANGLE


class MulticamOptions(BaseModel):
    """Settings (``multicamOptions``) for ``MediaPool.create_multicam_clip``.

    Note the lowercase/camelCase keys - these are the exact key names DaVinci Resolve
    expects. All fields are optional; only fields explicitly set are sent
    (use ``model_dump(exclude_none=True)``).
    """

    model_config = ConfigDict(use_enum_values=True)

    name: str | None = Field(
        default=None,
        description="Clip name. Auto-generated from the first clip when omitted",
    )
    startTimecode: str | None = Field(
        default=None, description='Start timecode (default: "01:00:00:00")'
    )
    frameRate: float | None = Field(
        default=None,
        gt=0,
        description="Frame rate, e.g. 23.976. Defaults to the project timeline frame rate",
    )
    angleSyncMode: MulticamAngleSyncMode | None = Field(
        default=None, description="What to sync the angles on (default: TIMECODE)"
    )
    channelConfig: int | AudioSyncChannel | None = Field(
        default=None,
        description="Audio channel used for sync (1 - 8), or an ``AudioSyncChannel`` "
        "constant. Only used when angleSyncMode is AUDIO",
    )
    multicamAudioMode: MulticamAudioMode | None = Field(
        default=None, description="Multicam audio mode (default: SOURCE)"
    )
    angleNameMode: MulticamAngleNameMode | None = Field(
        default=None, description="How angles are named (default: SEQUENTIAL)"
    )
    splitAtGaps: bool | None = Field(
        default=None,
        description="Split angles at gaps (default: False). Only used when angleSyncMode is AUDIO",
    )
    useFullClipExtents: bool | None = Field(
        default=None, description="Use the full extents of each clip (default: False)"
    )
    createBinForSourceClips: bool | None = Field(
        default=None, description="Create a bin for the source clips (default: True)"
    )
    detectSameCameraClipsMode: MulticamDetectSameCameraClipsMode | None = Field(
        default=None, description="How to detect clips from the same camera (default: NONE)"
    )


###################################
# Multicam Smart Switch Settings (DR 21.1.0)


class SmartSwitchAnalysisMode(Enum):
    """Analysis modes accepted by ``SmartSwitchSettings.analysisMode``."""

    NONE = _resolve.SMART_SWITCH_ANALYSIS_MODE_NONE
    DETECT_WIDE_ANGLE = _resolve.SMART_SWITCH_ANALYSIS_MODE_DETECT_WIDE_ANGLE
    AUDIO_ONLY = _resolve.SMART_SWITCH_ANALYSIS_MODE_AUDIO_ONLY


class SmartSwitchWideAngleFrequency(Enum):
    """Wide angle frequencies accepted by ``SmartSwitchSettings.wideAngleFrequency``."""

    LOW = _resolve.SMART_SWITCH_WIDE_ANGLE_FREQ_LOW
    MEDIUM = _resolve.SMART_SWITCH_WIDE_ANGLE_FREQ_MEDIUM
    HIGH = _resolve.SMART_SWITCH_WIDE_ANGLE_FREQ_HIGH


class SmartSwitchQuality(Enum):
    """Quality settings accepted by ``SmartSwitchSettings.quality``."""

    FASTER = _resolve.SMART_SWITCH_QUALITY_FASTER
    BETTER = _resolve.SMART_SWITCH_QUALITY_BETTER


class SmartSwitchSettings(BaseModel):
    """Settings (``smartSwitchSettings``) for ``TimelineItem.perform_multicam_smart_switch``.

    Note the camelCase keys - these are the exact key names DaVinci Resolve expects.
    All fields are optional; only fields explicitly set are sent
    (use ``model_dump(exclude_none=True)``).
    """

    model_config = ConfigDict(use_enum_values=True)

    minEditDuration: float | None = Field(
        default=None,
        ge=0.5,
        le=10.0,
        description="Minimum edit duration in seconds, 0.5 to 10.0 (default: 1.0)",
    )
    editChangeDelay: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0,
        description="Edit change delay in seconds, 0.0 to 2.0 (default: 0.3)",
    )
    isAutoDetectWideAngle: bool | None = Field(
        default=None,
        description="Auto-detect the wide angle from analysis (default: True)",
    )
    analysisMode: SmartSwitchAnalysisMode | None = Field(
        default=None, description="Analysis mode. Overrides isAutoDetectWideAngle"
    )
    wideAngleID: str | None = Field(
        default=None,
        description='Wide angle name, or "None" to disable. Used when isAutoDetectWideAngle is False',
    )
    wideAngleFrequency: SmartSwitchWideAngleFrequency | None = Field(
        default=None, description="Wide angle frequency (default: MEDIUM)"
    )
    isUseWideAngleForIntroOutro: bool | None = Field(
        default=None,
        description="Use the wide angle for intro and outro (default: True)",
    )
    isUseWideAngleForSilence: bool | None = Field(
        default=None, description="Use the wide angle for silence (default: True)"
    )
    switchOnVideoOnly: bool | None = Field(
        default=None,
        description="Switch on video only (default: False). Not supported in adaptive or "
        "source audio mode",
    )
    quality: SmartSwitchQuality | None = Field(
        default=None, description="Analysis quality (default: BETTER)"
    )


###################################
# Project Settings Preset Info (DR 21.1.0)


class ProjectSettingsPresetInfo(BaseModel):
    """One entry of the list returned by ``Project.get_project_settings_preset_list``."""

    Name: str | None = Field(default=None, description="Preset name")
    Width: int | None = Field(default=None, description="Resolution width, e.g. 1920")
    Height: int | None = Field(default=None, description="Resolution height, e.g. 1080")


###################################
# Project Attributes (DR 21.0.3)


class ProjectAttributes(BaseModel):
    """One value of the dict returned by
    ``ProjectManager.get_project_attributes_in_current_folder``."""

    lastModifiedDate: str | None = Field(
        default=None,
        description='Last modified date in ISO 8601 format, e.g. "2024-06-15T09:30:00+05:30"',
    )
    creationDate: str | None = Field(
        default=None,
        description='Creation date in ISO 8601 format, e.g. "2024-06-15T09:30:00+05:30"',
    )
    notes: str | None = Field(default=None, description="Project notes")
    liveCollaborationMode: str | None = Field(
        default=None, description='"multi_user" or "single_user"'
    )


###################################
# Transcription (DR 21.1.0)


class TranscriptionWord(BaseModel):
    """A single word of a ``TranscriptionSegment``."""

    start: str | None = Field(default=None, description="Start timecode")
    end: str | None = Field(default=None, description="End timecode")
    text: str | None = Field(
        default=None, description='Word text. "(...)" denotes silence'
    )


class TranscriptionSegment(BaseModel):
    """A single segment of a ``Transcription``."""

    start: str | None = Field(
        default=None, description='Start timecode, e.g. "01:00:02:05"'
    )
    end: str | None = Field(default=None, description='End timecode, e.g. "01:00:04:10"')
    text: str | None = Field(
        default=None,
        description='Concatenated text of all words in the segment. "(...)" denotes silence',
    )
    speaker: str | None = Field(
        default=None,
        description="Speaker name if speaker detection was used, None otherwise",
    )
    words: list[TranscriptionWord] = Field(
        default_factory=list, description="Words of this segment"
    )


class Transcription(BaseModel):
    """Transcription data returned by ``MediaPoolItem.get_transcription``."""

    language: str | None = Field(
        default=None, description="Transcription language code"
    )
    segments: list[TranscriptionSegment] = Field(
        default_factory=list, description="Transcription segments"
    )


###################################
# Timeline Item Properties (DR 21.1.0)


class DynamicZoomEase(Enum):
    """Ease modes accepted by ``TimelineItemProperties.DynamicZoomEase``."""

    LINEAR = _resolve.DYNAMIC_ZOOM_EASE_LINEAR
    IN = _resolve.DYNAMIC_ZOOM_EASE_IN
    OUT = _resolve.DYNAMIC_ZOOM_EASE_OUT
    IN_AND_OUT = _resolve.DYNAMIC_ZOOM_EASE_IN_AND_OUT


class CompositeMode(Enum):
    """Composite modes accepted by ``TimelineItemProperties.CompositeMode``."""

    NORMAL = _resolve.COMPOSITE_NORMAL
    ADD = _resolve.COMPOSITE_ADD
    SUBTRACT = _resolve.COMPOSITE_SUBTRACT
    DIFF = _resolve.COMPOSITE_DIFF
    MULTIPLY = _resolve.COMPOSITE_MULTIPLY
    SCREEN = _resolve.COMPOSITE_SCREEN
    OVERLAY = _resolve.COMPOSITE_OVERLAY
    HARDLIGHT = _resolve.COMPOSITE_HARDLIGHT
    SOFTLIGHT = _resolve.COMPOSITE_SOFTLIGHT
    DARKEN = _resolve.COMPOSITE_DARKEN
    LIGHTEN = _resolve.COMPOSITE_LIGHTEN
    COLOR_DODGE = _resolve.COMPOSITE_COLOR_DODGE
    COLOR_BURN = _resolve.COMPOSITE_COLOR_BURN
    EXCLUSION = _resolve.COMPOSITE_EXCLUSION
    HUE = _resolve.COMPOSITE_HUE
    SATURATE = _resolve.COMPOSITE_SATURATE
    COLORIZE = _resolve.COMPOSITE_COLORIZE
    LUMA_MASK = _resolve.COMPOSITE_LUMA_MASK
    DIVIDE = _resolve.COMPOSITE_DIVIDE
    LINEAR_DODGE = _resolve.COMPOSITE_LINEAR_DODGE
    LINEAR_BURN = _resolve.COMPOSITE_LINEAR_BURN
    LINEAR_LIGHT = _resolve.COMPOSITE_LINEAR_LIGHT
    VIVID_LIGHT = _resolve.COMPOSITE_VIVID_LIGHT
    PIN_LIGHT = _resolve.COMPOSITE_PIN_LIGHT
    HARD_MIX = _resolve.COMPOSITE_HARD_MIX
    LIGHTER_COLOR = _resolve.COMPOSITE_LIGHTER_COLOR
    DARKER_COLOR = _resolve.COMPOSITE_DARKER_COLOR
    FOREGROUND = _resolve.COMPOSITE_FOREGROUND
    ALPHA = _resolve.COMPOSITE_ALPHA
    INVERTED_ALPHA = _resolve.COMPOSITE_INVERTED_ALPHA
    LUM = _resolve.COMPOSITE_LUM
    INVERTED_LUM = _resolve.COMPOSITE_INVERTED_LUM


class RetimeProcess(Enum):
    """Retime processes accepted by ``TimelineItemProperties.RetimeProcess``."""

    USE_PROJECT = _resolve.RETIME_USE_PROJECT
    NEAREST = _resolve.RETIME_NEAREST
    FRAME_BLEND = _resolve.RETIME_FRAME_BLEND
    OPTICAL_FLOW = _resolve.RETIME_OPTICAL_FLOW


class MotionEstimation(Enum):
    """Motion estimation modes accepted by ``TimelineItemProperties.MotionEstimation``."""

    USE_PROJECT = _resolve.MOTION_EST_USE_PROJECT
    STANDARD_FASTER = _resolve.MOTION_EST_STANDARD_FASTER
    STANDARD_BETTER = _resolve.MOTION_EST_STANDARD_BETTER
    ENHANCED_FASTER = _resolve.MOTION_EST_ENHANCED_FASTER
    ENHANCED_BETTER = _resolve.MOTION_EST_ENHANCED_BETTER
    SPEED_WARP_FASTER = _resolve.MOTION_EST_SPEED_WARP_FASTER
    SPEED_WARP_BETTER = _resolve.MOTION_EST_SPEED_WARP_BETTER

    ## Add at DR 21.1.0
    METAL = _resolve.MOTION_EST_METAL


class Scaling(Enum):
    """Scaling modes accepted by ``TimelineItemProperties.Scaling``."""

    USE_PROJECT = _resolve.SCALE_USE_PROJECT
    CROP = _resolve.SCALE_CROP
    FIT = _resolve.SCALE_FIT
    FILL = _resolve.SCALE_FILL
    STRETCH = _resolve.SCALE_STRETCH


class ResizeFilter(Enum):
    """Resize filters accepted by ``TimelineItemProperties.ResizeFilter``."""

    USE_PROJECT = _resolve.RESIZE_FILTER_USE_PROJECT
    SHARPER = _resolve.RESIZE_FILTER_SHARPER
    SMOOTHER = _resolve.RESIZE_FILTER_SMOOTHER
    BICUBIC = _resolve.RESIZE_FILTER_BICUBIC
    BILINEAR = _resolve.RESIZE_FILTER_BILINEAR
    BESSEL = _resolve.RESIZE_FILTER_BESSEL
    BOX = _resolve.RESIZE_FILTER_BOX
    CATMULL_ROM = _resolve.RESIZE_FILTER_CATMULL_ROM
    CUBIC = _resolve.RESIZE_FILTER_CUBIC
    GAUSSIAN = _resolve.RESIZE_FILTER_GAUSSIAN
    LANCZOS = _resolve.RESIZE_FILTER_LANCZOS
    MITCHELL = _resolve.RESIZE_FILTER_MITCHELL
    NEAREST_NEIGHBOR = _resolve.RESIZE_FILTER_NEAREST_NEIGHBOR
    QUADRATIC = _resolve.RESIZE_FILTER_QUADRATIC
    SINC = _resolve.RESIZE_FILTER_SINC
    LINEAR = _resolve.RESIZE_FILTER_LINEAR


class DialogueLevelerMode(Enum):
    """Modes accepted by ``TimelineItemProperties.AudioDialogueLevelerMode``."""

    ALLOW_WIDER_DYNAMICS = _resolve.DIALOGUE_LEVELER_MODE_ALLOW_WIDER_DYNAMICS
    OPTIMIZE_MODERATE_LEVELS = _resolve.DIALOGUE_LEVELER_MODE_OPTIMIZE_MODERATE_LEVELS
    MORE_LIFT_FOR_LOW_LEVELS = _resolve.DIALOGUE_LEVELER_MODE_MORE_LIFT_FOR_LOW_LEVELS
    LIFT_SOFT_WHISPERY_SOURCES = _resolve.DIALOGUE_LEVELER_MODE_LIFT_SOFT_WHISPERY_SOURCES


# ``TimelineItemProperties`` has fields whose names are identical to the enums that type
# them (``CompositeMode``, ``Scaling``, ...). Inside a class body the field assignment
# happens before its annotation is evaluated, and pydantic also resolves annotations
# against the class namespace, so the bare enum name would resolve to the field itself.
# These private aliases give the annotations an unshadowed name to bind to.
_DynamicZoomEase = DynamicZoomEase
_CompositeMode = CompositeMode
_RetimeProcess = RetimeProcess
_MotionEstimation = MotionEstimation
_Scaling = Scaling
_ResizeFilter = ResizeFilter


class TimelineItemProperties(BaseModel):
    """Inspector properties used by ``TimelineItem.get_properties`` / ``set_properties``.

    Field names are the exact property keys DaVinci Resolve expects. All fields are
    optional; only fields explicitly set are sent (use ``model_dump(exclude_none=True)``).
    Values beyond the accepted range are clipped by DaVinci Resolve.

    ``Pan``, ``Tilt``, ``AnchorPointX``, ``AnchorPointY``, ``CropLeft``, ``CropRight``,
    ``CropTop`` and ``CropBottom`` are bounded by the clip's width/height, so they carry
    no static range constraint.
    """

    model_config = ConfigDict(use_enum_values=True)

    # --- Transform ---
    TransformEnabled: bool | None = Field(
        default=None, description="Enable/disable the Transform filter section (DR 21.1.0+)"
    )
    Pan: float | None = Field(default=None, description="-4.0*width to 4.0*width")
    Tilt: float | None = Field(default=None, description="-4.0*height to 4.0*height")
    ZoomX: float | None = Field(default=None, ge=0.0, le=100.0, description="0.0 to 100.0")
    ZoomY: float | None = Field(default=None, ge=0.0, le=100.0, description="0.0 to 100.0")
    ZoomGang: bool | None = Field(default=None, description="Gang ZoomX and ZoomY")
    RotationAngle: float | None = Field(
        default=None, ge=-360.0, le=360.0, description="-360.0 to 360.0"
    )
    AnchorPointX: float | None = Field(
        default=None, description="-4.0*width to 4.0*width"
    )
    AnchorPointY: float | None = Field(
        default=None, description="-4.0*height to 4.0*height"
    )
    Pitch: float | None = Field(default=None, ge=-1.5, le=1.5, description="-1.5 to 1.5")
    Yaw: float | None = Field(default=None, ge=-1.5, le=1.5, description="-1.5 to 1.5")
    FlipX: bool | None = Field(default=None, description="Flip horizontally")
    FlipY: bool | None = Field(default=None, description="Flip vertically")

    # --- Cropping ---
    CroppingEnabled: bool | None = Field(
        default=None, description="Enable/disable the Cropping filter section (DR 21.1.0+)"
    )
    CropLeft: float | None = Field(default=None, ge=0.0, description="0.0 to width")
    CropRight: float | None = Field(default=None, ge=0.0, description="0.0 to width")
    CropTop: float | None = Field(default=None, ge=0.0, description="0.0 to height")
    CropBottom: float | None = Field(default=None, ge=0.0, description="0.0 to height")
    CropSoftness: float | None = Field(
        default=None, ge=-100.0, le=100.0, description="-100.0 to 100.0"
    )
    CropRetain: bool | None = Field(
        default=None, description='The "Retain Image Position" checkbox'
    )

    # --- Dynamic Zoom ---
    DynamicZoomEnabled: bool | None = Field(
        default=None,
        description="Enable/disable the Dynamic Zoom filter section (DR 21.1.0+)",
    )
    DynamicZoomEase: _DynamicZoomEase | None = Field(
        default=None, description="Dynamic zoom ease mode"
    )

    # --- Composite ---
    CompositeEnabled: bool | None = Field(
        default=None, description="Enable/disable the Composite filter section (DR 21.1.0+)"
    )
    CompositeMode: _CompositeMode | None = Field(default=None, description="Composite mode")
    Opacity: float | None = Field(
        default=None, ge=0.0, le=100.0, description="0.0 to 100.0"
    )

    # --- Lens Correction ---
    LensCorrectionEnabled: bool | None = Field(
        default=None,
        description="Enable/disable the Lens Correction filter section (DR 21.1.0+)",
    )
    Distortion: float | None = Field(
        default=None, ge=-1.0, le=1.0, description="-1.0 to 1.0"
    )

    # --- Retime and Scaling ---
    RetimeAndScalingEnabled: bool | None = Field(
        default=None,
        description="Enable/disable the Retime and Scaling filter section (DR 21.1.0+)",
    )
    RetimeProcess: _RetimeProcess | None = Field(default=None, description="Retime process")
    MotionEstimation: _MotionEstimation | None = Field(
        default=None, description="Motion estimation mode"
    )
    Scaling: _Scaling | None = Field(default=None, description="Scaling mode")
    ResizeFilter: _ResizeFilter | None = Field(default=None, description="Resize filter")

    # --- Audio (DR 21.1.0+) ---
    AudioVolumeEnabled: bool | None = Field(
        default=None, description="Enable/disable the audio volume filter"
    )
    AudioVolume: float | None = Field(
        default=None, ge=-100.0, le=30.0, description="-100.0 to 30.0 dB"
    )
    AudioPanEnabled: bool | None = Field(
        default=None, description="Enable/disable the audio pan filter"
    )
    AudioPan: float | None = Field(
        default=None, ge=-100.0, le=100.0, description="-100.0 to 100.0"
    )
    AudioPitchEnabled: bool | None = Field(
        default=None, description="Enable/disable the audio pitch filter"
    )
    AudioPitchSemiTones: float | None = Field(
        default=None, ge=-24.0, le=24.0, description="-24.0 to 24.0"
    )
    AudioPitchCents: float | None = Field(
        default=None, ge=-100.0, le=100.0, description="-100.0 to 100.0"
    )

    # --- Voice Isolation (DR 21.1.0+, active timeline only) ---
    AudioVoiceIsolationEnabled: bool | None = Field(
        default=None, description="Enable/disable Voice Isolation"
    )
    AudioVoiceIsolationAmount: int | None = Field(
        default=None, ge=0, le=100, description="Isolation strength, 0 to 100"
    )

    # --- Dialogue Leveler (DR 21.1.0+, active timeline only) ---
    AudioDialogueLevelerEnabled: bool | None = Field(
        default=None, description="Enable/disable the Dialogue Leveler"
    )
    AudioDialogueLevelerMode: DialogueLevelerMode | None = Field(
        default=None, description="Dialogue Leveler mode"
    )
    AudioDialogueLevelerReduceLoudDialogue: bool | None = Field(
        default=None, description="Reduce loud dialogue"
    )
    AudioDialogueLevelerLiftSoftDialogue: bool | None = Field(
        default=None, description="Lift soft dialogue"
    )
    AudioDialogueLevelerBackgroundReduction: bool | None = Field(
        default=None, description="Enable background reduction"
    )
    AudioDialogueLevelerOutputGain: float | None = Field(
        default=None, ge=0.0, le=6.0, description="0.0 to 6.0 dB"
    )
