from enum import Enum

from pybmd.error import ResolveInitError


from ._init_bmd import _resolve_object as _resolve


if _resolve is None:
    raise ResolveInitError


class LUT_Export_Type(Enum):
    CUBE_17PT=_resolve.EXPORT_LUT_17PTCUBE
    CUBE_33PT=_resolve.EXPORT_LUT_33PTCUBE
    CUBE_65PT=_resolve.EXPORT_LUT_65PTCUBE
    VLUT_PS=_resolve.EXPORT_LUT_PANASONICVLUT
    

class Timeline_Export_Type(Enum):
    EXPORT_AAF = _resolve.EXPORT_AAF
    EXPORT_DRT = _resolve.EXPORT_DRT
    EXPORT_EDL = _resolve.EXPORT_EDL
    EXPORT_FCP_7_XML = _resolve.EXPORT_FCP_7_XML
    # Remove at DR 18.1.3
    # EXPORT_FCPXML_1_3 = local_davinci.EXPORT_FCPXML_1_3
    # EXPORT_FCPXML_1_4 = local_davinci.EXPORT_FCPXML_1_4
    # EXPORT_FCPXML_1_5 = local_davinci.EXPORT_FCPXML_1_5
    # EXPORT_FCPXML_1_6 = local_davinci.EXPORT_FCPXML_1_6
    # EXPORT_FCPXML_1_7 = local_davinci.EXPORT_FCPXML_1_7
    EXPORT_FCPXML_1_8 = _resolve.EXPORT_FCPXML_1_8
    # Add at DR 18.0.0
    EXPORT_FCPXML_1_9 = _resolve.EXPORT_FCPXML_1_9
    EXPORT_FCPXML_1_10 = _resolve.EXPORT_FCPXML_1_10
    EXPORT_HDR_10_PROFILE_A = _resolve.EXPORT_HDR_10_PROFILE_A
    EXPORT_HDR_10_PROFILE_B = _resolve.EXPORT_HDR_10_PROFILE_B
    EXPORT_TEXT_CSV = _resolve.EXPORT_TEXT_CSV
    EXPORT_TEXT_TAB = _resolve.EXPORT_TEXT_TAB
    EXPORT_DOLBY_VISION_VER_2_9 = _resolve.EXPORT_DOLBY_VISION_VER_2_9
    EXPORT_DOLBY_VISION_VER_4_0 = _resolve.EXPORT_DOLBY_VISION_VER_4_0
    # Add at DR 18.1.3
    EXPORT_DOLBY_VISION_VER_5_1 = _resolve.EXPORT_DOLBY_VISION_VER_5_1
    # Add at DR 18.5.0
    EXPORT_OTIO = _resolve.EXPORT_OTIO
    # Add at DR 19.0.0
    EXPORT_ALE = _resolve.EXPORT_ALE
    EXPORT_ALE_CDL = _resolve.EXPORT_ALE_CDL
    
    
class Timeline_Export_Subtype(Enum):
     # timeline exportSubtype can be one of the following enums:
    # for exportType is EXPORT_AAF:
    EXPORT_AAF_NEW = _resolve.EXPORT_AAF_NEW
    EXPORT_AAF_EXISTING = _resolve.EXPORT_AAF_EXISTING
    # for exportType is EXPORT_EDL:
    EXPORT_NONE = _resolve.EXPORT_NONE
    EXPORT_CDL = _resolve.EXPORT_CDL
    EXPORT_SDL = _resolve.EXPORT_SDL
    EXPORT_MISSING_CLIPS = _resolve.EXPORT_MISSING_CLIPS
    
