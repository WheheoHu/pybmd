from typing import Protocol, runtime_checkable


@runtime_checkable
class BMDModule(Protocol):
    """Protocol describing the shape of the loaded BMD module."""

    def scriptapp(self, app_name: str, ip: str) -> "ResolveObject": ...


class ResolveObject(Protocol):
    """Protocol describing the DaVinci Resolve object."""

    EXPORT_LUT_17PTCUBE: float
    EXPORT_LUT_33PTCUBE: float
    EXPORT_LUT_65PTCUBE: float
    EXPORT_LUT_PANASONICVLUT: float
    EXPORT_AAF: float
    EXPORT_DRT: float
    EXPORT_EDL: float
    EXPORT_FCP_7_XML: float
    EXPORT_FCPXML_1_8: float
    EXPORT_FCPXML_1_9: float
    EXPORT_FCPXML_1_10: float
    EXPORT_HDR_10_PROFILE_A: float
    EXPORT_HDR_10_PROFILE_B: float
    EXPORT_TEXT_CSV: float
    EXPORT_TEXT_TAB: float
    EXPORT_DOLBY_VISION_VER_2_9: float
    EXPORT_DOLBY_VISION_VER_4_0: float
    EXPORT_DOLBY_VISION_VER_5_1: float
    EXPORT_OTIO: float
    EXPORT_ALE: float
    EXPORT_ALE_CDL: float
    EXPORT_AAF_NEW: float
    EXPORT_AAF_EXISTING: float
    EXPORT_NONE: float
    EXPORT_CDL: float
    EXPORT_SDL: float
    EXPORT_MISSING_CLIPS: float

    CLOUD_SYNC_NONE: float
    CLOUD_SYNC_PROXY_ONLY: float
    CLOUD_SYNC_PROXY_AND_ORIG: float

    CLOUD_SETTING_PROJECT_NAME: float
    CLOUD_SETTING_PROJECT_MEDIA_PATH: float
    CLOUD_SETTING_IS_COLLAB: float
    CLOUD_SETTING_SYNC_MODE: float
    CLOUD_SETTING_IS_CAMERA_ACCESS: float

    AUTO_CAPTION_AUTO: float
    AUTO_CAPTION_DANISH: float
    AUTO_CAPTION_DUTCH: float
    AUTO_CAPTION_ENGLISH: float
    AUTO_CAPTION_FRENCH: float
    AUTO_CAPTION_GERMAN: float
    AUTO_CAPTION_ITALIAN: float
    AUTO_CAPTION_JAPANESE: float
    AUTO_CAPTION_KOREAN: float
    AUTO_CAPTION_NORWEGIAN: float
    AUTO_CAPTION_PORTUGUESE: float
    AUTO_CAPTION_RUSSIAN: float
    AUTO_CAPTION_SPANISH: float
    AUTO_CAPTION_SWEDISH: float
    AUTO_CAPTION_MANDARIN_SIMPLIFIED: float
    AUTO_CAPTION_MANDARIN_TRADITIONAL: float

    AUTO_CAPTION_SUBTITLE_DEFAULT: float
    AUTO_CAPTION_TELETEXT: float
    AUTO_CAPTION_NETFLIX: float

    AUTO_CAPTION_LINE_SINGLE: float
    AUPTO_CAPTION_LINE_DOUBLE: float

    SUBTITLE_LANGUAGE: float
    SUBTITLE_CAPTION_PRESET: float
    SUBTITLE_CHARS_PER_LINE: float
    SUBTITLE_LINE_BREAK: float
    SUBTITLE_GAP: float

    AUDIO_SYNC_WAVEFORM: float
    AUDIO_SYNC_TIMECODE: float
    
    AUDIO_SYNC_MODE: float
    AUDIO_SYNC_CHANNEL_NUMBER: float
    AUDIO_SYNC_RETAIN_EMBEDDED_AUDIO: float
    AUDIO_SYNC_RETAIN_VIDEO_METADATA: float

    MARKER_BLUE: str
    MARKER_CYAN: str
    MARKER_GREEN: str
    MARKER_YELLOW: str
    MARKER_RED: str
    MARKER_PINK: str
    MARKER_PURPLE: str
    MARKER_FUCHSIA: str
    MARKER_ROSE: str
    MARKER_LAVENDER: str
    MARKER_SKY: str
    MARKER_MINT: str
    MARKER_LEMON: str
    MARKER_SAND: str
    MARKER_COCOA: str
    MARKER_CREAM: str
    ###########################################################
    # Add at DR 21.1.0

    # Clone tool checksum types
    CLONE_CHECKSUM_TYPE_NONE: float
    CLONE_CHECKSUM_TYPE_FILESIZE: float
    CLONE_CHECKSUM_TYPE_CRC32: float
    CLONE_CHECKSUM_TYPE_MD5: float
    CLONE_CHECKSUM_TYPE_SHA256: float
    CLONE_CHECKSUM_TYPE_SHA512: float
    CLONE_CHECKSUM_TYPE_XXH_64: float

    # Normalize audio set level modes
    NORMALIZE_AUDIO_SET_LEVEL_RELATIVE: float
    NORMALIZE_AUDIO_SET_LEVEL_INDEPENDENT: float

    # Auto align clips
    AUTO_ALIGN_CLIPS_USING_WAVEFORM: float
    AUTO_ALIGN_CLIPS_USING_TIMECODE: float
    AUTO_ALIGN_CLIPS_WAVEFORM_TRACK_MIX: float
    AUTO_ALIGN_CLIPS_WAVEFORM_TRACK_AUTOMATIC: float

    # Multicam angle sync modes
    MULTICAM_ANGLE_SYNC_IN: float
    MULTICAM_ANGLE_SYNC_OUT: float
    MULTICAM_ANGLE_SYNC_TIMECODE: float
    MULTICAM_ANGLE_SYNC_AUDIO: float
    MULTICAM_ANGLE_SYNC_MARKER: float

    # Audio sync channels
    AUDIO_SYNC_CHANNEL_AUTOMATIC: float
    AUDIO_SYNC_CHANNEL_MIX: float

    # Multicam audio modes
    MULTICAM_AUDIO_ADAPTIVE: float
    MULTICAM_AUDIO_SOURCE: float
    MULTICAM_AUDIO_REFERENCE: float
    MULTICAM_AUDIO_ALL: float

    # Multicam angle name modes
    MULTICAM_ANGLE_NAME_SEQUENTIAL: float
    MULTICAM_ANGLE_NAME_ANGLE: float
    MULTICAM_ANGLE_NAME_CAMERA: float
    MULTICAM_ANGLE_NAME_CLIP: float
    MULTICAM_ANGLE_NAME_FILE: float

    # Multicam same-camera detection modes
    MULTICAM_DETECT_BY_CAMERA_NUMBER: float
    MULTICAM_DETECT_BY_ANGLE: float
    MULTICAM_DETECT_BY_REEL_NUMBER: float
    MULTICAM_DETECT_BY_REEL_NAME: float
    MULTICAM_DETECT_BY_ROLL_CARD: float
    MULTICAM_DETECT_NONE: float

    # Flatten multicam grade options
    FLATTEN_MULTICAM_COPY_GRADE: float
    FLATTEN_MULTICAM_RETAIN_GRADE_FROM_ANGLE: float

    # Multicam smart switch analysis modes
    SMART_SWITCH_ANALYSIS_MODE_NONE: float
    SMART_SWITCH_ANALYSIS_MODE_DETECT_WIDE_ANGLE: float
    SMART_SWITCH_ANALYSIS_MODE_AUDIO_ONLY: float

    # Multicam smart switch wide angle frequencies
    SMART_SWITCH_WIDE_ANGLE_FREQ_LOW: float
    SMART_SWITCH_WIDE_ANGLE_FREQ_MEDIUM: float
    SMART_SWITCH_WIDE_ANGLE_FREQ_HIGH: float

    # Multicam smart switch quality
    SMART_SWITCH_QUALITY_FASTER: float
    SMART_SWITCH_QUALITY_BETTER: float

    ###########################################################
    # Timeline item properties

    # Dynamic zoom ease
    DYNAMIC_ZOOM_EASE_LINEAR: float
    DYNAMIC_ZOOM_EASE_IN: float
    DYNAMIC_ZOOM_EASE_OUT: float
    DYNAMIC_ZOOM_EASE_IN_AND_OUT: float

    # Composite modes
    COMPOSITE_NORMAL: float
    COMPOSITE_ADD: float
    COMPOSITE_SUBTRACT: float
    COMPOSITE_DIFF: float
    COMPOSITE_MULTIPLY: float
    COMPOSITE_SCREEN: float
    COMPOSITE_OVERLAY: float
    COMPOSITE_HARDLIGHT: float
    COMPOSITE_SOFTLIGHT: float
    COMPOSITE_DARKEN: float
    COMPOSITE_LIGHTEN: float
    COMPOSITE_COLOR_DODGE: float
    COMPOSITE_COLOR_BURN: float
    COMPOSITE_EXCLUSION: float
    COMPOSITE_HUE: float
    COMPOSITE_SATURATE: float
    COMPOSITE_COLORIZE: float
    COMPOSITE_LUMA_MASK: float
    COMPOSITE_DIVIDE: float
    COMPOSITE_LINEAR_DODGE: float
    COMPOSITE_LINEAR_BURN: float
    COMPOSITE_LINEAR_LIGHT: float
    COMPOSITE_VIVID_LIGHT: float
    COMPOSITE_PIN_LIGHT: float
    COMPOSITE_HARD_MIX: float
    COMPOSITE_LIGHTER_COLOR: float
    COMPOSITE_DARKER_COLOR: float
    COMPOSITE_FOREGROUND: float
    COMPOSITE_ALPHA: float
    COMPOSITE_INVERTED_ALPHA: float
    COMPOSITE_LUM: float
    COMPOSITE_INVERTED_LUM: float

    # Retime process
    RETIME_USE_PROJECT: float
    RETIME_NEAREST: float
    RETIME_FRAME_BLEND: float
    RETIME_OPTICAL_FLOW: float

    # Motion estimation
    MOTION_EST_USE_PROJECT: float
    MOTION_EST_STANDARD_FASTER: float
    MOTION_EST_STANDARD_BETTER: float
    MOTION_EST_ENHANCED_FASTER: float
    MOTION_EST_ENHANCED_BETTER: float
    MOTION_EST_SPEED_WARP_FASTER: float
    MOTION_EST_SPEED_WARP_BETTER: float
    MOTION_EST_METAL: float

    # Scaling
    SCALE_USE_PROJECT: float
    SCALE_CROP: float
    SCALE_FIT: float
    SCALE_FILL: float
    SCALE_STRETCH: float

    # Resize filter
    RESIZE_FILTER_USE_PROJECT: float
    RESIZE_FILTER_SHARPER: float
    RESIZE_FILTER_SMOOTHER: float
    RESIZE_FILTER_BICUBIC: float
    RESIZE_FILTER_BILINEAR: float
    RESIZE_FILTER_BESSEL: float
    RESIZE_FILTER_BOX: float
    RESIZE_FILTER_CATMULL_ROM: float
    RESIZE_FILTER_CUBIC: float
    RESIZE_FILTER_GAUSSIAN: float
    RESIZE_FILTER_LANCZOS: float
    RESIZE_FILTER_MITCHELL: float
    RESIZE_FILTER_NEAREST_NEIGHBOR: float
    RESIZE_FILTER_QUADRATIC: float
    RESIZE_FILTER_SINC: float
    RESIZE_FILTER_LINEAR: float

    # Dialogue leveler modes
    DIALOGUE_LEVELER_MODE_ALLOW_WIDER_DYNAMICS: float
    DIALOGUE_LEVELER_MODE_OPTIMIZE_MODERATE_LEVELS: float
    DIALOGUE_LEVELER_MODE_MORE_LIFT_FOR_LOW_LEVELS: float
    DIALOGUE_LEVELER_MODE_LIFT_SOFT_WHISPERY_SOURCES: float
