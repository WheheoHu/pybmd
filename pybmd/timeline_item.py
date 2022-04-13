

import string
from dataclasses import dataclass
from dataclasses import asdict
from os import path
from typing import List
from pybmd.fusion_comp import FusionComp
from pybmd.media_pool_item import MediaPoolItem

from enum import Enum

class VersionType(Enum):
    """Docstring for VersionType."""
    LOCAL = 0
    REMOTE = 1


@dataclass
class CDL_Map():
    """Docstring for CDL_Map."""
    NodeIndex: str
    Slope: str
    Offset: str
    Power: str
    Saturation: str


class TimelineItem():
    """docstring for TimelineItem."""

    def __init__(self, timeline_item):
        self.timeline_item = timeline_item

    def get_markers(self) -> dict:
        return self.timeline_item.GetMarkers()

    def add_flag(self, color: str) -> bool:
        return self.timeline_item.AddFlag(color)

    def add_fusion_comp(self) -> FusionComp:
        return FusionComp(self.timeline_item.AddFusionComp())

    def add_marker(self, frame_id: str, color: str, name: str, note: str, duration: str, custom_data: str) -> bool:
        return self.timeline_item.AddMarker(frame_id, color, name, note, duration, custom_data)

    def add_take(self, media_pool_item: MediaPoolItem, start_frame: int, end_frame: int) -> bool:
        return self.timeline_item.AddTake(media_pool_item, start_frame, end_frame)

    def add_version(self, version_name: str, version_type: VersionType) -> bool:
        return self.timeline_item.AddVersion(version_name, version_type.value)

    def clear_clip_color(self) -> bool:
        return self.timeline_item.ClearClipColor()

    def clear_flags(self, color) -> bool:
        return self.timeline_item.ClearFlags(color)

    def copy_grades(self, target_timeline_items: List['TimelineItem']) -> bool:
        timeline_item_list = []
        for timeline_item in target_timeline_items:
            timeline_item_list.append(timeline_item.timeline_item)
        return self.timeline_item.CopyGrades(timeline_item_list)

    def delete_fusion_comp_by_name(self, comp_name: str) -> bool:
        return self.timeline_item.DeleteFusionCompByName(comp_name)

    def delet_marker_at_frame(self, fram_num: int) -> bool:
        return self.timeline_item.DeletMarkerAtFrame(fram_num)

    def delete_marker_by_custom_data(self, custom_data) -> bool:
        return self.timeline_item.DeleteMarkerByCustomData(custom_data)

    def delete_marker_by_color(self, color: str) -> bool:
        return self.timeline_item.DeleteMarkerByColor(color)

    def delete_take_by_index(self, index: int) -> bool:
        return self.timeline_item.DeleteTakeByIndex(index)

    def delet_version_by_name(self, version_name: str, version_type: VersionType) -> bool:
        return self.timeline_item.DeletVersionByName(version_name, version_type.value)

    def export_fusion_comp(self, path: str, comp_index: int) -> bool:
        return self.timeline_item.ExportFusionComp(str(path), comp_index)

    def finalize_take(self) -> bool:
        return self.timeline_item.FinalizeTake()

    def get_clip_color(self) -> str:
        return self.timeline_item.GetClipColor()

    def get_current_version(self) -> dict:
        return self.timeline_item.GetCurrentVersion()

    def get_duration(self) -> int:
        return self.timeline_item.GetDuration()

    def get_end(self) -> int:
        return self.timeline_item.GetEnd()

    def get_flag_list(self) -> list:
        return self.timeline_item.GetFlagList()

    def get_fusion_comp_by_index(self, comp_index) -> FusionComp:
        return FusionComp(self.timeline_item.GetFusionCompByIndex(comp_index))

    def get_fusion_comp_by_name(self, comp_name) -> FusionComp:
        return FusionComp(self.timeline_item.GetFusionCompByName(comp_name))

    def get_fusion_comp_count(self) -> int:
        return self.timeline_item.GetFusionCompCount()

    def get_fusion_comp_name_list(self) -> list:
        return self.timeline_item.GetFusionCompNameList()

    def get_left_offset(self) -> int:
        return self.timeline_item.GetLeftOffset()

    def get_marker_by_custom_data(self, custom_data: str) -> dict:
        return self.timeline_item.GetMarkerByCustomData(custom_data)

    def get_marker_custom_data(self, frame_id: int) -> str:
        return self.timeline_item.GetMarkerCustomData(frame_id)

    def get_media_pool_item(self,) -> MediaPoolItem:
        return MediaPoolItem(self.timeline_item.GetMediaPoolItem())

    def get_name(self) -> str:
        return self.timeline_item.GetName()

    def get_property(self, property_key):
        # if no key is specified, the method returns a dictionary(python) or table(lua) for all supported keys
        return self.timeline_item.GetProperty(property_key)

    def get_right_offset(self) -> int:
        return self.timeline_item.GetRightOffset()

    def get_selected_take_index(self) -> int:
        return self.timeline_item.GetSelectedTakeIndex()

    def get_start(self) -> int:
        return self.timeline_item.GetStart()

    def get_stereo_convergence_values(self) -> dict:
        return self.timeline_item.GetStereoConvergenceValues()

    def get_stereo_left_floating_window_params(self) -> dict:
        return self.timeline_item.GetStereoLeftFloatingWindowParams()

    def get_stereo_right_floating_window_params(self) -> dict:
        return self.timeline_item.GetStereoRightFloatingWindowParams()

    def get_take_by_index(self, index) -> dict:
        return self.timeline_item.GetTakeByIndex(index)

    def get_takes_count(self) -> int:
        return self.timeline_item.GetTakesCount()

    def get_version_name_list(self, version_type: VersionType) -> list:
        return self.timeline_item.GetVersionNameList(version_type.value)

    def import_fusion_comp(self, path: str) -> FusionComp:
        return FusionComp(self.timeline_item.ImportFusionComp(str(path)))

    def load_fusion_comp_by_name(self, comp_name: str) -> FusionComp:
        return FusionComp(self.timeline_item.LoadFusionCompByName(comp_name))

    def load_version_by_name(self, version_name: str, version_type: VersionType) -> bool:
        return self.timeline_item.LoadVersionByName(version_name, version_type.value)

    def rename_fusion_comp_by_name(self, old_name: str, new_name: str) -> bool:
        return self.timeline_item.RenameFusionCompByName(old_name, new_name)

    def rename_version_by_name(self, old_name: str, new_name: str) -> bool:
        return self.timeline_item.RenameVersionByName(old_name, new_name)

    def select_take_by_index(self, index: int) -> bool:
        return self.timeline_item.SelectTakeByIndex(index)

    def set_cdl(self, cdl_map: CDL_Map) -> bool:
        return self.timeline_item.SetCdl(asdict(cdl_map))

    def set_clip_color(self, color_name) -> bool:
        return self.timeline_item.SetClipColor(color_name)

    def set_lut(self, node_index: int, lutpath: str) -> bool:
        return self.timeline_item.SetLUT(node_index, str(lutpath))
    
    ####################################################################################################################
    #add in davinci resolve 17.4.6
    def get_num_node(self) -> int:
        return self.timeline_item.GetNumNode()
    
    def get_lut(self,node_index) -> str:
        return self.timeline_item.GetLUT(node_index)
    
    
    ##########################################################################################################################
