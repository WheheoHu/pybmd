from dataclasses import dataclass
from dataclasses import asdict
from os import path
from typing import List, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from pybmd.export_type import LUT_Export_Type

from pybmd.color_group import ColorGroup

from pybmd.fusion_comp import FusionComp
from pybmd.graph import Graph
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
        self._timeline_item = timeline_item

    def __repr__(self) -> str:
        return f'Timeline Item:f{self.get_name()}'

    def get_markers(self) -> dict:
        """Returns a dict (frameId -> {information}) of all markers and dicts with their information.
            Example: a value of {96.0: {'color': 'Green', 'duration': 1.0, 'note': '', 'name': 'Marker 1', 'customData': ''}, ...}
            indicates a single green marker at clip offset 96
        """
        return self._timeline_item.GetMarkers()

    def add_flag(self, color: str) -> bool:
        """Adds a flag with given color (string)."""
        return self._timeline_item.AddFlag(color)

    def add_fusion_comp(self) -> 'FusionComp':
        """Adds a new Fusion composition associated with the timeline item."""
        return FusionComp(self._timeline_item.AddFusionComp())

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
        return self._timeline_item.AddMarker(frame_id, color, name, note, duration, custom_data)

    def add_take(self, media_pool_item: MediaPoolItem, start_frame: int, end_frame: int) -> bool:
        """Adds mediaPoolItem as a new take. Initializes a take selector for the timeline item if needed. By default, the full clip extents is added. 

        Args:
            media_pool_item (MediaPoolItem): MeidaPoolItem object to add as a new take.
            start_frame (int): start frame of the take.
            end_frame (int): end frame of the take.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._timeline_item.AddTake(media_pool_item._media_pool_item, start_frame, end_frame)

    def add_version(self, version_name: str, version_type: VersionType) -> bool:
        """Adds a new color version for a video clip based on versionType

        Args:
            version_name (str): version name
            version_type (VersionType): version type object

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._timeline_item.AddVersion(version_name, version_type.value)

    def clear_clip_color(self) -> bool:
        """Clears the item color."""
        return self._timeline_item.ClearClipColor()

    def clear_flags(self, color) -> bool:
        """Clears all flags of a given color.if color is empty, all flags are cleared."""
        return self._timeline_item.ClearFlags(color)

    def copy_grades(self, target_timeline_items: List['TimelineItem']) -> bool:
        """
        Copies the current node stack layer grade to the same layer for each item in target_timeline_items. 
        Returns True if successful.
        """
        timeline_item_list = []
        for timeline_item in target_timeline_items:
            timeline_item_list.append(timeline_item._timeline_item)
        return self._timeline_item.CopyGrades(timeline_item_list)

    def delete_fusion_comp_by_name(self, comp_name: str) -> bool:
        """Deletes the named Fusion composition."""
        return self._timeline_item.DeleteFusionCompByName(comp_name)

    def delet_marker_at_frame(self, fram_num: int) -> bool:
        """Delete marker at frameNum from the timeline item."""
        return self._timeline_item.DeletMarkerAtFrame(fram_num)

    def delete_marker_by_custom_data(self, custom_data) -> bool:
        """Delete first matching marker with specified customData."""
        return self._timeline_item.DeleteMarkerByCustomData(custom_data)

    def delete_marker_by_color(self, color: str) -> bool:
        """
        Delete all markers of the specified color from the timeline item. 
        "All" as argument deletes all color markers.
        """
        return self._timeline_item.DeleteMarkerByColor(color)

    def delete_take_by_index(self, index: int) -> bool:
        """Deletes a take by index, 1 <= idx <= number of takes."""
        return self._timeline_item.DeleteTakeByIndex(index)

    def delete_version_by_name(self, version_name: str, version_type: VersionType) -> bool:
        """Deletes a color version by name and versionType 

        Args:
            version_name (str): version name to delete
            version_type (VersionType): VersionType object

        Returns:
            bool: true if successful, false otherwise.
        """
        return self._timeline_item.DeleteVersionByName(version_name, version_type.value)

    def export_fusion_comp(self, path: str, comp_index: int) -> bool:
        """Exports the Fusion composition based on given compIndex to the path provided."""
        return self._timeline_item.ExportFusionComp(str(path), comp_index)

    def finalize_take(self) -> bool:
        """Finalizes take selection."""
        return self._timeline_item.FinalizeTake()

    def get_clip_color(self) -> str:
        """Returns the item color."""
        return self._timeline_item.GetClipColor()

    def get_current_version(self) -> dict:
        """returns the current version of the timeline item"""
        return self._timeline_item.GetCurrentVersion()

    def get_duration(self, subframe_precision: bool = False) -> int | float:
        # Change at 19.0.2
        """Returns the item duration."""
        return self._timeline_item.GetDuration(subframe_precision)

    def get_end(self,subframe_precision: bool = False) -> int | float:
        # Change at 19.0.2
        """Returns the end frame position on the timeline."""
        return self._timeline_item.GetEnd(subframe_precision)

    def get_flag_list(self) -> list:
        """Returns the end frame position on the timeline."""
        return self._timeline_item.GetFlagList()

    def get_fusion_comp_by_index(self, comp_index: int) -> "FusionComp":
        """
        Returns the Fusion composition object based on given compIndex. 
        1 <= compIndex <= timelineItem.get_fusion_comp_count()
        """
        return FusionComp(self._timeline_item.GetFusionCompByIndex(comp_index))

    def get_fusion_comp_by_name(self, comp_name: str) -> "FusionComp":
        """Returns the Fusion composition object based on given comp_name."""
        return FusionComp(self._timeline_item.GetFusionCompByName(comp_name))

    def get_fusion_comp_count(self) -> int:
        """Returns number of Fusion compositions associated with the timeline item."""
        return self._timeline_item.GetFusionCompCount()

    def get_fusion_comp_name_list(self) -> list:
        """Returns a list of Fusion composition names associated with the timeline item."""
        return self._timeline_item.GetFusionCompNameList()

    def get_left_offset(self,subframe_precision:bool=False) -> int | float:
        ### Change at 19.0.2
        """Returns the maximum extension by frame for clip from left side."""
        return self._timeline_item.GetLeftOffset(subframe_precision)

    def get_marker_by_custom_data(self, custom_data: str) -> dict:
        """Returns marker {information} for the first matching marker with specified customData."""
        return self._timeline_item.GetMarkerByCustomData(custom_data)

    def get_marker_custom_data(self, frame_id: int) -> str:
        """Returns customData string for the marker at given frameId position."""
        return self._timeline_item.GetMarkerCustomData(frame_id)

    def get_media_pool_item(self) -> "MediaPoolItem":
        """Returns the media pool item corresponding to the timeline item if one exists.

        Returns:
            MediaPoolItem: meida pool item object
        """
        return MediaPoolItem(self._timeline_item.GetMediaPoolItem())

    def get_name(self) -> str:
        """Returns the item name."""
        return self._timeline_item.GetName()

    def get_property(self, property_key):
        """returns the value of the specified key.

        if no key is specified, the method returns a dictionary(python) or table(lua) for all supported keys
        """
        return self._timeline_item.GetProperty(property_key)

    def get_right_offset(self,subframe_precision:bool=False) -> int | float:
        ### Change at 19.0.2
        """Returns the maximum extension by frame for clip from right side."""
        return self._timeline_item.GetRightOffset(subframe_precision)

    def get_selected_take_index(self) -> int:
        """Returns the index of the currently selected take, or 0 if the clip is not a take selector."""
        return self._timeline_item.GetSelectedTakeIndex()

    def get_start(self,subframe_precision:bool=False) -> int | float:
        ### Change at 19.0.2
        """Returns the start frame position on the timeline."""
        return self._timeline_item.GetStart(subframe_precision)

    def get_stereo_convergence_values(self) -> dict:
        """Returns a dict (offset -> value) of keyframe offsets and respective convergence values."""
        return self._timeline_item.GetStereoConvergenceValues()

    def get_stereo_left_floating_window_params(self) -> dict:
        """For the LEFT eye -> returns a dict (offset -> dict) of keyframe offsets and respective floating window params. 
        Value at particular offset includes the left, right, top and bottom floating window values."""
        return self._timeline_item.GetStereoLeftFloatingWindowParams()

    def get_stereo_right_floating_window_params(self) -> dict:
        """For the RIGHT eye -> returns a dict (offset -> dict) of keyframe offsets and respective floating window params. 
        Value at particular offset includes the left, right, top and bottom floating window values."""
        return self._timeline_item.GetStereoRightFloatingWindowParams()

    def get_take_by_index(self, index) -> dict:
        """Returns a dict (keys "startFrame", "endFrame" and "mediaPoolItem") with take info for specified index."""
        return self._timeline_item.GetTakeByIndex(index)

    def get_takes_count(self) -> int:
        """Returns the number of takes in take selector, or 0 if the clip is not a take selector."""
        return self._timeline_item.GetTakesCount()

    def get_version_name_list(self, version_type: VersionType) -> list:
        """Returns a list of all color versions for the given versionType.

        Args:
            version_type (VersionType): VersionType object

        Returns:
            list: list of version names
        """
        return self._timeline_item.GetVersionNameList(version_type.value)

    def import_fusion_comp(self, path: str) -> "FusionComp":
        """Imports a Fusion composition from given file path by creating and adding a new composition for the item.

        Args:
            path (str): path to the Fusion composition file

        Returns:
            FusionComp: Fusion composition object
        """
        return FusionComp(self._timeline_item.ImportFusionComp(str(path)))

    def load_fusion_comp_by_name(self, comp_name: str) -> "FusionComp":
        """Loads the named Fusion composition as the active composition."""
        return FusionComp(self._timeline_item.LoadFusionCompByName(comp_name))

    def load_version_by_name(self, version_name: str, version_type: VersionType) -> bool:
        """Loads a named color version as the active version.

        Args:
            version_name (str): version name to load    
            version_type (VersionType): VersionType object

        Returns:
            bool: True if successful, False otherwise
        """
        return self._timeline_item.LoadVersionByName(version_name, version_type.value)

    def rename_fusion_comp_by_name(self, old_name: str, new_name: str) -> bool:
        """Renames the Fusion composition identified by oldName."""
        return self._timeline_item.RenameFusionCompByName(old_name, new_name)

    def rename_version_by_name(self, old_name: str, new_name: str, version_type: VersionType) -> bool:
        """Renames the color version identified by oldName and versionType """
        return self._timeline_item.RenameVersionByName(old_name, new_name, version_type.value)

    def select_take_by_index(self, index: int) -> bool:
        """Selects a take by index, 1 <= idx <= number of takes."""
        return self._timeline_item.SelectTakeByIndex(index)

    def set_cdl(self, cdl_map: CDL_Map) -> bool:
        """Sets the color correction lookup (CDL) for the timeline item.

        Args:
            cdl_map (CDL_Map): CDL_Map object

        Returns:
            bool: True if successful, False otherwise
        """
        return self._timeline_item.SetCdl(asdict(cdl_map))

    def set_clip_color(self, color_name: str) -> bool:
        """Sets the item color based on the colorName (string)."""
        return self._timeline_item.SetClipColor(color_name)

    # Remove at DR 19.0.0
    # def set_lut(self, node_index: int, lutpath: str) -> bool:
    #     """Sets LUT on the node mapping the nodeIndex provided

    #     Args:
    #         node_index (int): 1 <= nodeIndex <= total number of nodes.
    #         lutpath (str): can be an absolute path, or a relative path (based off custom LUT paths or the master LUT path).

    #     Returns:
    #         bool: True if successful, False otherwise
    #     """
    #     return self._timeline_item.SetLUT(node_index, str(lutpath))

    ####################################################################################################################
    # add in davinci resolve 17.4.6

    # Remove at DR 19.0.0
    # def get_num_node(self) -> int:
    #     """Returns the number of nodes in the current graph for the timeline item"""
    #     return self._timeline_item.GetNumNode()

    # Remove at DR 19.0.0
    # def get_lut(self, node_index: int) -> str:
    #     """Gets relative LUT path based on the node index provided

    #     Args:
    #         node_index (int): 1 <= nodeIndex <= total number of nodes.

    #     Returns:
    #         str: lut path
    #     """
    #     return self._timeline_item.GetLUT(node_index)

    ##########################################################################################################################
    # Add at DR18.0.0

    def update_sidecar(self) -> bool:
        """Updates sidecar file for BRAW clips or RMD file for R3D clips."""
        return self._timeline_item.UpdateSidecar()

    def get_unique_id(self) -> str:
        """Returns a unique ID for the timeline item"""
        return self._timeline_item.GetUniqueId()

    ##########################################################################################################################
    # Add at DR18.5.0 Beta

    def apply_arri_cdl_lut(self) -> bool:
        """Applies ARRI CDL and LUT.

        Returns:
            bool: Returns True if successful, False otherwise.
        """
        return self._timeline_item.ApplyArriCdlLut()

    def set_clip_enabled(self, bool_value: bool) -> bool:
        """Sets clip enabled based on argument.

        Args:
            bool_value (bool): Sets clip enabled based on argument.

        Returns:
            bool: True for clip is enabled
        """
        return self._timeline_item.SetClipEnabled(bool_value)

    def get_clip_enabled(self) -> bool:
        """Gets clip enabled status.

        Returns:
            bool: clip enabled status 
        """
        return self._timeline_item.GetClipEnabled()

    def load_burn_in_preset(self, preset_name: str) -> bool:
        """Loads user defined data burn in preset for clip when supplied presetName (string). Returns true if successful.

        Args:
            preset_name (str): burn-in preset name

        Returns:
            bool: Returns true if successful
        """
        return self._timeline_item.LoadBurnInPreset(preset_name)

    # Remove at DR 19.0.0
    # def get_node_label(self, node_index: int) -> str:
    #     """Returns the label of the node at nodeIndex.

    #     Args:
    #         node_index (int): node index

    #     Returns:
    #         str: node label
    #     """
    #     return self._timeline_item.GetNodeLabel(node_index)

    ##############################################################################################################################
    # Add at DR18.5.0

    def create_magic_mask(self, mode: MagicMask_Mode) -> bool:
        """Returns True if magic mask was created successfully, False otherwise. 

        Args:
            mode (MagicMask_Mode): mode 

        Returns:
            bool: Returns True if magic mask was created successfully, False otherwise.
        """
        return self._timeline_item.CreateMagicMask(mode.value)

    def regenerate_magic_mask(self) -> bool:
        """Returns True if magic mask was regenerated successfully, False otherwise.

        Returns:
            bool: Returns True if magic mask was regenerated successfully, False otherwise.
        """
        return self._timeline_item.RegenerateMagicMask()

    def stabilize(self) -> bool:
        """Returns True if stabilization was successful, False otherwise

        Returns:
            bool: Returns True if stabilization was successful, False otherwise
        """
        return self._timeline_item.Stabilize()

    def smart_reframe(self) -> bool:
        """Performs Smart Reframe. 

        Returns:
            bool: _descriReturns True if successful, False otherwise.
        """
        return self._timeline_item.SmartReframe()

    ##############################################################################################################################
    # Add at DR 19.0.0

    def get_node_graph(self, layer_index: int) -> "Graph":
        """Returns the clip's node graph object 

        Args:
            layer_index (int):  1 <= layer_index <= project.GetSetting("nodeStackLayers").

        Returns:
            Graph: The clip's node graph object at layer_index. Returns the first layer if layer_index is skipped.
        """
        return Graph(self._timeline_item.GetNodeGraph(layer_index))

    def get_color_group(self) -> "ColorGroup":
        """Returns the clip's color group if one exists.

        Returns:
            ColorGroup: the clip's color group
        """
        return ColorGroup(self._timeline_item.GetColorGroup())

    def assign_to_color_group(self, color_group: ColorGroup) -> bool:
        """Returns True if TiItem to successfully assigned to given ColorGroup. 

        Args:
            color_group (ColorGroup): ColorGroup must be an existing group in the current project.

        Returns:
            bool: Returns True if TiItem to successfully assigned to given ColorGroup. 
        """
        return self._timeline_item.AssignToColorGroup(color_group)

    def remove_from_color_group(self) -> bool:
        """Returns True if the TiItem is successfully removed from the ColorGroup it is in.

        Returns:
            bool: Returns True if the TiItem is successfully removed from the ColorGroup it is in.
        """
        return self._timeline_item.RemoveFromColorGroup()

    def export_LUT(self, export_type: "LUT_Export_Type", export_path: str) -> bool:
        """ Exports LUTs from tiItem 

        Args:
            export_type (LUT_Export_Type): export lut type
            export_path (str): Saves generated LUT in the provided 'path' (string). 'path' should include the intended file name.If an empty or incorrect extension is provided, the appropriate extension (.cube/.vlt) will be appended at the end of the path.

        Returns:
            bool: Returns True if successful, False otherwise.
        """

        return self._timeline_item.ExportLUT(export_type.value, export_path)

    def get_linked_items(self) -> List["TimelineItem"]:
        """ Returns a list of linked timeline items.

        Returns:
            List[TimelineItem]: a list of linked timeline items.
        """
        timeline_item_list = list()
        for value in self._timeline_item.GetLinkedItems():
            timeline_item_list.append(TimelineItem(value))
        return timeline_item_list

    def get_track_type_and_index(self) -> Tuple[str, int]:
        """Returns a list of two values that correspond to the TimelineItem's trackType (string) and trackIndex (int) respectively.

        Returns:
            Tuple[str,int]: trackType is one of {"audio", "video", "subtitle"},1 <= trackIndex <= Timeline.GetTrackCount(trackType)

        """
        return tuple(self._timeline_item.GetTrackTypeAndIndex())

    ##############################################################################################################################
    # Add at DR 19.0.1

    def get_source_audio_channel_mapping(self) -> str:
        """Returns a string with TimelineItem's audio mapping information.

        Returns:
            str: json formatted string
        """
        return self._timeline_item.GetSourceAudioChannelMapping()
    
    ##############################################################################################################################
    # Add at DR 19.0.2
    
    def get_source_end_frame(self) -> int:
        """Returns the end frame position of the media pool clip in the timeline clip.

        Returns:
            int: end frame position of the media pool clip
        """
        return self._timeline_item.GetSourceEndFrame()
    
    def get_source_end_time(self) -> float:
        """Returns the end time position of the media pool clip in the timeline clip.

        Returns:
            float: end time position of the media pool clip
        """
        return self._timeline_item.GetSourceEndTime()
    
    def get_source_start_frame(self) -> int:
        """Returns the start frame position of the media pool clip in the timeline clip.
        
        Returns:
            int: start frame position of the media pool clip
        """
        return self._timeline_item.GetSourceStartFrame()
    
    def get_source_start_time(self) -> float:
        """Returns the start time position of the media pool clip in the timeline clip.
        
        Returns:
            float: start time position of the media pool clip
        """
        return self._timeline_item.GetSourceStartTime()