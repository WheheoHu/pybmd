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