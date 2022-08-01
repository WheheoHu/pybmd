from enum import Enum
from os import path
from typing import List

from pybmd.gallery_still import GalleryStill
from pybmd.timeline_item import TimelineItem


from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class ImportOptions():
    """Docstring for ImportOptions."""

    # specifies a filesystem path to search for source clips if the media is inaccessible
    # in their original path and if "ignoreFileExtensionsWhenMatching" is True
    sourceClipsPath: str = ""

    # list of Media Pool folder objects to search for source clips if the media is not present in current folder
    sourceClipsFolders: str = ""

    autoImportSourceClipsIntoMediaPool: bool = True
    ignoreFileExtensionsWhenMatching: bool = False
    linkToSourceCameraFiles: bool = False
    useSizingInfo: bool = False
    importMultiChannelAudioTracksAsLinkedGroups: bool = False
    insertAdditionalTracks: bool = True
    insertWithOffset: str = "00:00:00:00"


class TrackTpye(Enum):
    """docstring for TrackTpye."""
    AUDIO_TRACK = 'audio'
    VIDEO_TRACK = 'video'
    SUBTITLE_TRACK = 'subtitle'


def timeline_item_class_list_transfer(timeline_item_list: List[TimelineItem]) -> list:
    timeline_item_trans_list = []

    for timeline_item in timeline_item_list:
        timeline_item_trans_list.append(timeline_item.timeline_item)

    return timeline_item_trans_list


class Timeline():
    """docstring for Timeline."""

    def __init__(self, timeline):
        self.timeline = timeline

    def add_marker(self, frame_id: str, color: str, name: str, note: str, duration: str, custom_data: str) -> bool:
        return self.timeline.AddMarker(frame_id, color, name, note, duration, custom_data)

    def apply_grade_from_drx(self, path: str, grade_mode: int, timeline_items: List[TimelineItem]) -> bool:
        return self.timeline.ApplyGradeFromDRX(str(path), grade_mode, timeline_items)

    def create_compound_clip(self, timeline_items: List[TimelineItem], clipinfo: dict) -> TimelineItem:
        return TimelineItem(timeline_item=self.timeline.CreateCompoundClip(timeline_item_class_list_transfer(timeline_items), clipinfo))

    def create_fusion_clip(self, timeline_items: List[TimelineItem]) -> TimelineItem:
        return TimelineItem(timeline_item=self.timeline.CreateFusionClip(timeline_item_class_list_transfer(timeline_items)))

    def delete_marker_at_frame(self, frame_num: int) -> bool:
        return self.timeline.DeleteMarkerAtFrame(frame_num)

    def delete_marker_by_custom_data(self, custom_data: str) -> bool:
        return self.timeline.DeleteMarkerByCustomData(custom_data)

    def delete_marker_by_color(self, color: str) -> bool:
        return self.timeline.DeleteMarkerByColor(color)

    def duplicate_timeline(self, timeline_name: str):
        return Timeline(timeline=self.timeline.DuplicateTimeline(timeline_name))

    def export(self, file_name: str, export_type, export_subtype=None) -> bool:
        # file_name should be a path, not a file name.
        # eg. file_path=os.path.join(os.path.expanduser("~"), "Desktop/Temp/sampleExp.drt")
        #     timeline.export(file_path,LOCAL_RESOLVE.EXPORT_DRT)
        return self.timeline.Export(file_name, export_type, export_subtype)

    def get_current_clip_thumbnail_image(self) -> dict:
        return self.timeline.GetCurrentClipThumbnailImage()

    def get_current_timecode(self) -> str:
        return self.timeline.GetCurrentTimecode()

    def get_current_video_item(self) -> TimelineItem:
        return TimelineItem(self.timeline.GetCurrentVideoItem())

    def get_end_frame(self) -> int:
        return self.timeline.GetEndFrame()

    def get_item_list_in_track(self, track_type: TrackTpye, index: int) -> List[TimelineItem]:
        timeline_items_list = []
        for timeline_item in self.timeline.GetItemListInTrack(
                track_type.value, index):
            timeline_items_list.append(TimelineItem(timeline_item))
        return timeline_items_list

    def get_marker_by_custom_data(self, custom_data: str) -> dict:
        return self.timeline.GetMarkerByCustomData(custom_data)

    def get_marker_custom_data(self, frame_id: int) -> str:
        return self.timeline.GetMarkerCustomData(frame_id)

    def get_markers(self) -> dict:
        return self.timeline.GetMarkers()

    def get_name(self) -> str:
        return self.timeline.GetName()

    def get_setting(self, setting_name: str) -> str:
        return self.timeline.GetSetting(setting_name)

    def get_start_frame(self) -> int:
        return self.timeline.GetStartFrame()

    def get_track_count(self, track_type: TrackTpye) -> int:
        return self.timeline.GetTrackCount(track_type.value)

    def get_track_name(self, track_type: TrackTpye, track_index: int) -> str:
        return self.timeline.GetTrackName(track_type.value, track_index)

    def grab_all_stills(self, still_frame_source: int) -> List[GalleryStill]:
        gallery_stills_list = []
        for gallery_still in self.timeline.GrabAllStills(still_frame_source):
            gallery_stills_list.append(gallery_still)
        return gallery_stills_list

    def grab_still(self) -> GalleryStill:
        return GalleryStill(self.timeline.GrabStill())

    # TODO test this
    def import_into_timeline(self, file_path: str, import_options: ImportOptions) -> bool:
        return self.timeline.ImportIntoTimeline(file_path, asdict(import_options))

    def insert_fusion_generator_into_timeline(self, generator_name: str) -> TimelineItem:
        return TimelineItem(self.timeline.InsertFusionGeneratorIntoTimeline(generator_name))

    def insert_fusion_title_into_timeline(self, title_name: str) -> TimelineItem:
        return TimelineItem(self.timeline.InsertFusionTitleIntoTimeline(title_name))

    def insert_generator_into_timeline(self, generator_name: str) -> TimelineItem:
        return TimelineItem(self.timeline.InsertGeneratorIntoTimeline(generator_name))

    def insert_oFX_generator_into_timeline(self, generator_name: str) -> TimelineItem:
        return TimelineItem(self.timeline.InsertOFXGeneratorIntoTimeline(generator_name))

    def insert_title_into_timeline(self, title_name: str) -> TimelineItem:
        return TimelineItem(self.timeline.InsertTitleIntoTimeline(title_name))

    def set_current_timecode(self, tiemcode: str) -> bool:
        return self.timeline.SetCurrentTimecode(tiemcode)

    def set_name(self, timeline_name) -> bool:
        return self.timeline.SetName(timeline_name)

    # TODO setting_name to data class
    def set_setting(self, setting_name: str, setting_value: str) -> bool:
        return self.timeline.SetSetting(setting_name, setting_value)

    def set_track_name(self, track_type: TrackTpye, track_index: int, name: str) -> bool:
        return self.timeline.SetTrackName(track_type.value, track_index, name)

    def update_marker_custom_data(self, frame_id: int, custom_data: str) -> bool:
        return self.timeline.UpdateMarkerCustomData(frame_id, custom_data)

    #######################################################################################################################
    # Add at DR18.0.0
    
    def set_start_timecode(self, timecode: str) -> bool:
        return self.timeline.SetStartTimecode(timecode)

    def get_start_timecode(self) -> str:
        return self.timeline.GetStartTimecode()
    
    def insert_fusion_composition_into_timeline(self) -> TimelineItem:
        return TimelineItem(self.timeline.InsertFusionCompositionIntoTimeline())
    
    def get_unique_id(self) -> str:
        return self.timeline.GetUniqueId()
    
    #######################################################################################################################