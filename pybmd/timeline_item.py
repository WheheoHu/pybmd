from dataclasses import dataclass
from dataclasses import asdict
from os import path
from typing import List
from pybmd.fusion_comp import FusionComp
from pybmd.media_pool_item import MediaPoolItem

from enum import Enum


class VersionType(Enum):
    """VersionType."""
    LOCAL = 0
    REMOTE = 1


@dataclass
class CDL_Map():
    """CDL_Map"""
    NodeIndex: str
    Slope: str
    Offset: str
    Power: str
    Saturation: str


@dataclass
class MagicMask_Mode():
    """MagicMask_Mode."""
    Forward = "F"
    Backward = "B"
    Bidirection = "BI"


class TimelineItem():
    """TimelineItem Object"""

    def __init__(self, timeline_item):
        self.timeline_item = timeline_item

    def __repr__(self) -> str:
        return f'Timeline Item:f{self.get_name()}'

    def get_markers(self) -> dict:
        """Returns a dict (frameId -> {information}) of all markers and dicts with their information.
            Example: a value of {96.0: {'color': 'Green', 'duration': 1.0, 'note': '', 'name': 'Marker 1', 'customData': ''}, ...}
            indicates a single green marker at clip offset 96
        """
        return self.timeline_item.GetMarkers()

    def add_flag(self, color: str) -> bool:
        """Adds a flag with given color (string)."""
        return self.timeline_item.AddFlag(color)

    def add_fusion_comp(self) -> FusionComp:
        """Adds a new Fusion composition associated with the timeline item."""
        return FusionComp(self.timeline_item.AddFusionComp())

    def add_marker(self, frame_id: str, color: str, name: str, note: str, duration: str, custom_data: str) -> bool:
        """Creates a new marker at given frameId position and with given marker information. 

        Args:
            frame_id (str): frame position of the marker
            color (str): color of the marker
            name (str): name of the marker
            note (str): note of the marker
            duration (str): duration of the marker
            custom_data (str): custom data of the marker helps to attach user specific data to the marker.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline_item.AddMarker(frame_id, color, name, note, duration, custom_data)

    def add_take(self, media_pool_item: MediaPoolItem, start_frame: int, end_frame: int) -> bool:
        """Adds mediaPoolItem as a new take. Initializes a take selector for the timeline item if needed. By default, the full clip extents is added. 

        Args:
            media_pool_item (MediaPoolItem): MeidaPoolItem object to add as a new take.
            start_frame (int): start frame of the take.
            end_frame (int): end frame of the take.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline_item.AddTake(media_pool_item, start_frame, end_frame)

    def add_version(self, version_name: str, version_type: VersionType) -> bool:
        """Adds a new color version for a video clip based on versionType

        Args:
            version_name (str): version name
            version_type (VersionType): version type object

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline_item.AddVersion(version_name, version_type.value)

    def clear_clip_color(self) -> bool:
        """Clears the item color."""
        return self.timeline_item.ClearClipColor()

    def clear_flags(self, color) -> bool:
        """Clears all flags of a given color.if color is empty, all flags are cleared."""
        return self.timeline_item.ClearFlags(color)

    def copy_grades(self, target_timeline_items: List['TimelineItem']) -> bool:
        """
        Copies the current grade to all the items in tgtTimelineItems list. 
        Returns True on success and False if any error occurred.
        """
        timeline_item_list = []
        for timeline_item in target_timeline_items:
            timeline_item_list.append(timeline_item.timeline_item)
        return self.timeline_item.CopyGrades(timeline_item_list)

    def delete_fusion_comp_by_name(self, comp_name: str) -> bool:
        """Deletes the named Fusion composition."""
        return self.timeline_item.DeleteFusionCompByName(comp_name)

    def delet_marker_at_frame(self, fram_num: int) -> bool:
        """Delete marker at frameNum from the timeline item."""
        return self.timeline_item.DeletMarkerAtFrame(fram_num)

    def delete_marker_by_custom_data(self, custom_data) -> bool:
        """Delete first matching marker with specified customData."""
        return self.timeline_item.DeleteMarkerByCustomData(custom_data)

    def delete_marker_by_color(self, color: str) -> bool:
        """
        Delete all markers of the specified color from the timeline item. 
        "All" as argument deletes all color markers.
        """
        return self.timeline_item.DeleteMarkerByColor(color)

    def delete_take_by_index(self, index: int) -> bool:
        """Deletes a take by index, 1 <= idx <= number of takes."""
        return self.timeline_item.DeleteTakeByIndex(index)

    def delete_version_by_name(self, version_name: str, version_type: VersionType) -> bool:
        """Deletes a color version by name and versionType 

        Args:
            version_name (str): version name to delete
            version_type (VersionType): VersionType object

        Returns:
            bool: true if successful, false otherwise.
        """
        return self.timeline_item.DeleteVersionByName(version_name, version_type.value)

    def export_fusion_comp(self, path: str, comp_index: int) -> bool:
        """Exports the Fusion composition based on given compIndex to the path provided."""
        return self.timeline_item.ExportFusionComp(str(path), comp_index)

    def finalize_take(self) -> bool:
        """Finalizes take selection."""
        return self.timeline_item.FinalizeTake()

    def get_clip_color(self) -> str:
        """Returns the item color."""
        return self.timeline_item.GetClipColor()

    def get_current_version(self) -> dict:
        """returns the current version of the timeline item"""
        return self.timeline_item.GetCurrentVersion()

    def get_duration(self) -> int:
        """Returns the item duration."""
        return self.timeline_item.GetDuration()

    def get_end(self) -> int:
        """Returns the end frame position on the timeline."""
        return self.timeline_item.GetEnd()

    def get_flag_list(self) -> list:
        """Returns the end frame position on the timeline."""
        return self.timeline_item.GetFlagList()

    def get_fusion_comp_by_index(self, comp_index) -> FusionComp:
        """
        Returns the Fusion composition object based on given compIndex. 
        1 <= compIndex <= timelineItem.get_fusion_comp_count()
        """
        return FusionComp(self.timeline_item.GetFusionCompByIndex(comp_index))

    def get_fusion_comp_by_name(self, comp_name) -> FusionComp:
        """Returns the Fusion composition object based on given comp_name."""
        return FusionComp(self.timeline_item.GetFusionCompByName(comp_name))

    def get_fusion_comp_count(self) -> int:
        """Returns number of Fusion compositions associated with the timeline item."""
        return self.timeline_item.GetFusionCompCount()

    def get_fusion_comp_name_list(self) -> list:
        """Returns a list of Fusion composition names associated with the timeline item."""
        return self.timeline_item.GetFusionCompNameList()

    def get_left_offset(self) -> int:
        """Returns the maximum extension by frame for clip from left side."""
        return self.timeline_item.GetLeftOffset()

    def get_marker_by_custom_data(self, custom_data: str) -> dict:
        """Returns marker {information} for the first matching marker with specified customData."""
        return self.timeline_item.GetMarkerByCustomData(custom_data)

    def get_marker_custom_data(self, frame_id: int) -> str:
        """Returns customData string for the marker at given frameId position."""
        return self.timeline_item.GetMarkerCustomData(frame_id)

    def get_media_pool_item(self) -> MediaPoolItem:
        """Returns the media pool item corresponding to the timeline item if one exists.

        Returns:
            MediaPoolItem: meida pool item object
        """
        return MediaPoolItem(self.timeline_item.GetMediaPoolItem())

    def get_name(self) -> str:
        """Returns the item name."""
        return self.timeline_item.GetName()

    def get_property(self, property_key):
        """returns the value of the specified key.

        if no key is specified, the method returns a dictionary(python) or table(lua) for all supported keys
        """
        return self.timeline_item.GetProperty(property_key)

    def get_right_offset(self) -> int:
        """Returns the maximum extension by frame for clip from right side."""
        return self.timeline_item.GetRightOffset()

    def get_selected_take_index(self) -> int:
        """Returns the index of the currently selected take, or 0 if the clip is not a take selector."""
        return self.timeline_item.GetSelectedTakeIndex()

    def get_start(self) -> int:
        """Returns the start frame position on the timeline."""
        return self.timeline_item.GetStart()

    def get_stereo_convergence_values(self) -> dict:
        """Returns a dict (offset -> value) of keyframe offsets and respective convergence values."""
        return self.timeline_item.GetStereoConvergenceValues()

    def get_stereo_left_floating_window_params(self) -> dict:
        """For the LEFT eye -> returns a dict (offset -> dict) of keyframe offsets and respective floating window params. 
        Value at particular offset includes the left, right, top and bottom floating window values."""
        return self.timeline_item.GetStereoLeftFloatingWindowParams()

    def get_stereo_right_floating_window_params(self) -> dict:
        """For the RIGHT eye -> returns a dict (offset -> dict) of keyframe offsets and respective floating window params. 
        Value at particular offset includes the left, right, top and bottom floating window values."""
        return self.timeline_item.GetStereoRightFloatingWindowParams()

    def get_take_by_index(self, index) -> dict:
        """Returns a dict (keys "startFrame", "endFrame" and "mediaPoolItem") with take info for specified index."""
        return self.timeline_item.GetTakeByIndex(index)

    def get_takes_count(self) -> int:
        """Returns the number of takes in take selector, or 0 if the clip is not a take selector."""
        return self.timeline_item.GetTakesCount()

    def get_version_name_list(self, version_type: VersionType) -> list:
        """Returns a list of all color versions for the given versionType.

        Args:
            version_type (VersionType): VersionType object

        Returns:
            list: list of version names
        """
        return self.timeline_item.GetVersionNameList(version_type.value)

    def import_fusion_comp(self, path: str) -> FusionComp:
        """Imports a Fusion composition from given file path by creating and adding a new composition for the item.

        Args:
            path (str): path to the Fusion composition file

        Returns:
            FusionComp: Fusion composition object
        """
        return FusionComp(self.timeline_item.ImportFusionComp(str(path)))

    def load_fusion_comp_by_name(self, comp_name: str) -> FusionComp:
        """Loads the named Fusion composition as the active composition."""
        return FusionComp(self.timeline_item.LoadFusionCompByName(comp_name))

    def load_version_by_name(self, version_name: str, version_type: VersionType) -> bool:
        """Loads a named color version as the active version.

        Args:
            version_name (str): version name to load    
            version_type (VersionType): VersionType object

        Returns:
            bool: True if successful, False otherwise
        """
        return self.timeline_item.LoadVersionByName(version_name, version_type.value)

    def rename_fusion_comp_by_name(self, old_name: str, new_name: str) -> bool:
        """Renames the Fusion composition identified by oldName."""
        return self.timeline_item.RenameFusionCompByName(old_name, new_name)

    def rename_version_by_name(self, old_name: str, new_name: str, version_type: VersionType) -> bool:
        """Renames the color version identified by oldName and versionType """
        return self.timeline_item.RenameVersionByName(old_name, new_name, version_type.value)

    def select_take_by_index(self, index: int) -> bool:
        """Selects a take by index, 1 <= idx <= number of takes."""
        return self.timeline_item.SelectTakeByIndex(index)

    def set_cdl(self, cdl_map: CDL_Map) -> bool:
        """Sets the color correction lookup (CDL) for the timeline item.

        Args:
            cdl_map (CDL_Map): CDL_Map object

        Returns:
            bool: True if successful, False otherwise
        """
        return self.timeline_item.SetCdl(asdict(cdl_map))

    def set_clip_color(self, color_name: str) -> bool:
        """Sets the item color based on the colorName (string)."""
        return self.timeline_item.SetClipColor(color_name)

    def set_lut(self, node_index: int, lutpath: str) -> bool:
        """Sets LUT on the node mapping the nodeIndex provided

        Args:
            node_index (int): 1 <= nodeIndex <= total number of nodes.
            lutpath (str): can be an absolute path, or a relative path (based off custom LUT paths or the master LUT path).

        Returns:
            bool: True if successful, False otherwise
        """
        return self.timeline_item.SetLUT(node_index, str(lutpath))

    ####################################################################################################################
    # add in davinci resolve 17.4.6

    def get_num_node(self) -> int:
        """Returns the number of nodes in the current graph for the timeline item"""
        return self.timeline_item.GetNumNode()

    def get_lut(self, node_index: int) -> str:
        """Gets relative LUT path based on the node index provided

        Args:
            node_index (int): 1 <= nodeIndex <= total number of nodes.

        Returns:
            str: lut path
        """
        return self.timeline_item.GetLUT(node_index)

    ##########################################################################################################################
    # Add at DR18.0.0

    def update_sidecar(self) -> bool:
        """Updates sidecar file for BRAW clips or RMD file for R3D clips."""
        return self.timeline_item.UpdateSidecar()

    def get_unique_id(self) -> str:
        """Returns a unique ID for the timeline item"""
        return self.timeline_item.GetUniqueId()

    ##########################################################################################################################
    # Add at DR18.5.0 Beta

    def apply_arri_cdl_lut(self) -> bool:
        """Applies ARRI CDL and LUT.

        Returns:
            bool: Returns True if successful, False otherwise.
        """
        return self.timeline_item.ApplyArriCdlLut()

    def set_clip_enabled(self, bool_value: bool) -> bool:
        """Sets clip enabled based on argument.

        Args:
            bool_value (bool): Sets clip enabled based on argument.

        Returns:
            bool: True for clip is enabled
        """
        return self.timeline_item.SetClipEnabled(bool_value)

    def get_clip_enabled(self) -> bool:
        """Gets clip enabled status.

        Returns:
            bool: clip enabled status 
        """
        return self.timeline_item.GetClipEnabled()

    def load_burn_in_preset(self, preset_name: str) -> bool:
        """Loads user defined data burn in preset for clip when supplied presetName (string). Returns true if successful.

        Args:
            preset_name (str): burn-in preset name

        Returns:
            bool: Returns true if successful
        """
        return self.timeline_item.LoadBurnInPreset(preset_name)

    def get_node_label(self, node_index: int) -> str:
        """Returns the label of the node at nodeIndex.

        Args:
            node_index (int): node index

        Returns:
            str: node label
        """
        return self.timeline_item.GetNodeLabel(node_index)

    ##############################################################################################################################
    # Add at DR18.5.0
    
    def create_magic_mask(self, mode: MagicMask_Mode) -> bool:
        """Returns True if magic mask was created successfully, False otherwise. 

        Args:
            mode (MagicMask_Mode): mode 

        Returns:
            bool: Returns True if magic mask was created successfully, False otherwise.
        """
        return self.timeline_item.CreateMagicMask(mode.value)
    
    def regenerate_magic_mask(self) -> bool:
        """Returns True if magic mask was regenerated successfully, False otherwise.

        Returns:
            bool: Returns True if magic mask was regenerated successfully, False otherwise.
        """
        return self.timeline_item.RegenerateMagicMask()
    
    def stabilize(self) -> bool:
        """Returns True if stabilization was successful, False otherwise

        Returns:
            bool: Returns True if stabilization was successful, False otherwise
        """
        return self.timeline_item.Stabilize()
    
    def smart_reframe(self) -> bool:
        """Performs Smart Reframe. 

        Returns:
            bool: _descriReturns True if successful, False otherwise.
        """
        return self.timeline_item.SmartReframe()