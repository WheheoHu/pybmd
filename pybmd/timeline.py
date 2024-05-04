from enum import Enum
from os import path
from typing import List

from pybmd.gallery_still import GalleryStill
from pybmd.settings import AutoCaptionSettings
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


class TrackType(Enum):
    """docstring for TrackTpye."""
    AUDIO_TRACK = 'audio'
    VIDEO_TRACK = 'video'
    SUBTITLE_TRACK = 'subtitle'


class OptionalSubTrackType(Enum):
    """OptionalSubTrackType is required for TrackType is AUDIO_TRACK"""
    MONO = "mono"
    STEREO = "stereo"
    FP1 = "5.1"
    FP1_FILM = "5.1film"
    SP1 = "7.1"
    SP1_FILM = "7.1film"
    ADAPTIVE_1 = "adaptive1"
    ADAPTIVE_2 = "adaptive2"
    ADAPTIVE_3 = "adaptive3"
    ADAPTIVE_4 = "adaptive4"
    ADAPTIVE_5 = "adaptive5"
    ADAPTIVE_6 = "adaptive6"
    ADAPTIVE_7 = "adaptive7"
    ADAPTIVE_8 = "adaptive8"
    ADAPTIVE_9 = "adaptive9"
    ADAPTIVE_10 = "adaptive10"
    ADAPTIVE_11 = "adaptive11"
    ADAPTIVE_12 = "adaptive12"
    ADAPTIVE_13 = "adaptive13"
    ADAPTIVE_14 = "adaptive14"
    ADAPTIVE_15 = "adaptive15"
    ADAPTIVE_16 = "adaptive16"
    ADAPTIVE_17 = "adaptive17"
    ADAPTIVE_18 = "adaptive18"
    ADAPTIVE_19 = "adaptive19"
    ADAPTIVE_20 = "adaptive20"
    ADAPTIVE_21 = "adaptive21"
    ADAPTIVE_22 = "adaptive22"
    ADAPTIVE_23 = "adaptive23"
    ADAPTIVE_24 = "adaptive24"


def timeline_item_class_list_transfer(timeline_item_list: List[TimelineItem]) -> list:
    timeline_item_trans_list = []

    for timeline_item in timeline_item_list:
        timeline_item_trans_list.append(timeline_item.timeline_item)

    return timeline_item_trans_list


class Timeline():
    """Timeline Object"""

    def __init__(self, timeline):
        self.timeline = timeline

    def __repr__(self) -> str:
        return f'Timeline: {self.get_name()}'

    def add_marker(self, frame_id: str, color: str, name: str, note: str, duration: str, custom_data: str) -> bool:
        """Creates a new marker at given frameId position and with given marker information. 

        Args:
            frame_id (str): frame position of the marker.
            color (str): color of the marker.
            name (str): name of the marker.
            note (str): note of the marker.
            duration (str): duration of the marker.
            custom_data (str): custom data of the marker.helps to attach user specific data to the marker.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline.AddMarker(frame_id, color, name, note, duration, custom_data)

    def apply_grade_from_drx(self, path: str, grade_mode: int, timeline_items: List[TimelineItem]) -> bool:
        """Loads a still from given file path (string) and applies grade to Timeline Items with gradeMode (int)

        Args:
            path (str): still file path.
            grade_mode (int): 0 - "No keyframes", 1 - "Source Timecode aligned", 2 - "Start Frames aligned".
            timeline_items (List[TimelineItem]): timeline items to apply grade to.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline.ApplyGradeFromDRX(str(path), grade_mode, timeline_items)

    def create_compound_clip(self, timeline_items: List[TimelineItem], clipinfo: dict) -> TimelineItem:
        """Creates a compound clip of input TimelineItems with an optional clipInfo map

        Args:
            timeline_items (List[TimelineItem]): TimelineItems to create compound clip from.
            clipinfo (dict): {"startTimecode" : "00:00:00:00", "name" : "Compound Clip 1"}. 

        Returns:
            TimelineItem: created timeline item.
        """
        return TimelineItem(timeline_item=self.timeline.CreateCompoundClip(timeline_item_class_list_transfer(timeline_items), clipinfo))

    def create_fusion_clip(self, timeline_items: List[TimelineItem]) -> TimelineItem:
        """Creates a Fusion clip of input timeline items.

        Args:
            timeline_items (List[TimelineItem]): timeline items to create fusion clip from.

        Returns:
            TimelineItem: created timeline item.
        """
        return TimelineItem(timeline_item=self.timeline.CreateFusionClip(timeline_item_class_list_transfer(timeline_items)))

    def delete_marker_at_frame(self, frame_num: int) -> bool:
        """Deletes the timeline marker at the given frame number."""
        return self.timeline.DeleteMarkerAtFrame(frame_num)

    def delete_marker_by_custom_data(self, custom_data: str) -> bool:
        """Delete first matching marker with specified custom_data."""
        return self.timeline.DeleteMarkerByCustomData(custom_data)

    def delete_marker_by_color(self, color: str) -> bool:
        """Deletes all timeline markers of the specified color. 
        An "All" argument is supported and deletes all timeline markers.
        """
        return self.timeline.DeleteMarkerByColor(color)

    def duplicate_timeline(self, timeline_name: str):
        """Duplicates the timeline and returns the created timeline, 
        with the (optional) timelineName, on success.
        """
        return Timeline(timeline=self.timeline.DuplicateTimeline(timeline_name))

    def export(self, file_name: str, export_type, export_subtype=None) -> bool:
        """Exports timeline to 'fileName' as per input exportType & exportSubtype format.
        # file_name should be a path, not a file name.
        # eg. file_path=os.path.join(os.path.expanduser("~"), "Desktop/Temp/sampleExp.drt")
        #     timeline.export(file_path,LOCAL_RESOLVE.EXPORT_DRT)
        """
        return self.timeline.Export(file_name, export_type, export_subtype)

    def get_current_clip_thumbnail_image(self) -> dict:
        """Returns a dict (keys "width", "height", "format" and "data") with data containing raw thumbnail image data 
        (RGB 8-bit image data encoded in base64 format) for current media in the Color Page.
        """
        return self.timeline.GetCurrentClipThumbnailImage()

    def get_current_timecode(self) -> str:
        """Returns a string timecode representation for the current playhead position, 
        while on Cut, Edit, Color, Fairlight and Deliver pages.
        """
        return self.timeline.GetCurrentTimecode()

    def get_current_video_item(self) -> TimelineItem:
        """Returns the current video timeline item."""
        return TimelineItem(self.timeline.GetCurrentVideoItem())

    def get_end_frame(self) -> int:
        """Returns the frame number at the end of timeline."""
        return self.timeline.GetEndFrame()

    def get_item_list_in_track(self, track_type: TrackType, index: int) -> List[TimelineItem]:
        """Returns a list of timeline items on that track.

        Args:
            track_type (TrackTpye): track type.
            index (int): track index.

        Returns:
            List[TimelineItem]: timeline items on that track.
        """
        timeline_items_list = []
        for timeline_item in self.timeline.GetItemListInTrack(
                track_type.value, index):
            timeline_items_list.append(TimelineItem(timeline_item))
        return timeline_items_list

    def get_marker_by_custom_data(self, custom_data: str) -> dict:
        """Returns marker {information} for the first matching marker with specified customData."""
        return self.timeline.GetMarkerByCustomData(custom_data)

    def get_marker_custom_data(self, frame_id: int) -> str:
        """Returns customData string for the marker at given frameId position."""
        return self.timeline.GetMarkerCustomData(frame_id)

    def get_markers(self) -> dict:
        """Returns a dict (frameId -> {information}) of all markers and dicts with their information.
        Example: a value of {96.0: {'color': 'Green', 'duration': 1.0, 'note': '', 'name': 'Marker 1', 'customData': ''}, ...} 
        indicates a single green marker at timeline offset 96
        """
        return self.timeline.GetMarkers()

    def get_name(self) -> str:
        """Returns the name of the timeline."""
        return self.timeline.GetName()

    def get_setting(self, setting_name: str = "") -> str:
        """Returns value of timeline setting (indicated by settingName : string)."""
        return self.timeline.GetSetting(setting_name)

    def get_start_frame(self) -> int:
        """Returns the frame number at the start of timeline."""
        return self.timeline.GetStartFrame()

    def get_track_count(self, track_type: TrackType) -> int:
        """Returns the number of tracks for the given trackType ("audio", "video" or "subtitle")."""
        return self.timeline.GetTrackCount(track_type.value)

    def get_track_name(self, track_type: TrackType, track_index: int) -> str:
        """Returns the track name for track indicated by trackType ("audio", "video" or "subtitle") and trackIndex.

        Args:
            track_type (TrackTpye): Track type.
            track_index (int):  1 <= trackIndex <= GetTrackCount(trackType)

        Returns:
            str: track name.
        """

        return self.timeline.GetTrackName(track_type.value, track_index)

    def grab_all_stills(self, still_frame_source: int) -> List[GalleryStill]:
        """Grabs stills from all the clips of the timeline and returns a list of GalleryStill objects.

        Args:
            still_frame_source (int): 1 - First frame, 2 - Middle frame

        Returns:
            List[GalleryStill]: List of GalleryStill objects containing grabbed stills.
        """

        return [GalleryStill(gallery_still) for gallery_still in self.timeline.GrabAllStills(still_frame_source)]

    def grab_still(self) -> GalleryStill:
        """Grabs still from the current video clip. Returns a GalleryStill object."""
        return GalleryStill(self.timeline.GrabStill())

    # TODO test this
    def import_into_timeline(self, file_path: str, import_options: ImportOptions) -> bool:
        """Imports timeline items from an AAF file and optional importOptions dict into the timeline,

        Args:
            file_path (str): file path.
            import_options (ImportOptions): ImportOptions object.

        Returns:
            bool: true if successful, false otherwise.
        """
        return self.timeline.ImportIntoTimeline(file_path, asdict(import_options))

    def insert_fusion_generator_into_timeline(self, generator_name: str) -> TimelineItem:
        """Inserts a Fusion generator (indicated by generatorName : string) into the timeline."""
        return TimelineItem(self.timeline.InsertFusionGeneratorIntoTimeline(generator_name))

    def insert_fusion_title_into_timeline(self, title_name: str) -> TimelineItem:
        """Inserts a Fusion title (indicated by titleName : string) into the timeline."""
        return TimelineItem(self.timeline.InsertFusionTitleIntoTimeline(title_name))

    def insert_generator_into_timeline(self, generator_name: str) -> TimelineItem:
        """Inserts a generator (indicated by generatorName : string) into the timeline."""
        return TimelineItem(self.timeline.InsertGeneratorIntoTimeline(generator_name))

    def insert_oFX_generator_into_timeline(self, generator_name: str) -> TimelineItem:
        """Inserts an OFX generator (indicated by generatorName : string) into the timeline."""
        return TimelineItem(self.timeline.InsertOFXGeneratorIntoTimeline(generator_name))

    def insert_title_into_timeline(self, title_name: str) -> TimelineItem:
        """Inserts a title (indicated by titleName : string) into the timeline."""
        return TimelineItem(self.timeline.InsertTitleIntoTimeline(title_name))

    def set_current_timecode(self, tiemcode: str) -> bool:
        """Sets current playhead position from input timecode for Cut, Edit, Color, Fairlight and Deliver pages."""
        return self.timeline.SetCurrentTimecode(tiemcode)

    def set_name(self, timeline_name) -> bool:
        """Sets the timeline name if timelineName (string) is unique. Returns True if successful."""
        return self.timeline.SetName(timeline_name)

    # TODO setting_name to data class
    def set_setting(self, setting_name: str, setting_value: str) -> bool:
        """Sets timeline setting 

        Args:
            setting_name (str): Setting name.   
            setting_value (str): Setting value. 

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline.SetSetting(setting_name, setting_value)

    def set_track_name(self, track_type: TrackType, track_index: int, name: str) -> bool:
        """Sets the track name (string) for track indicated by trackType and trackIndex. 

        Args:
            track_type (TrackTpye):TrackType object.
            track_index (int): 1 <= trackIndex <= GetTrackCount(trackType).
            name (str): track name.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline.SetTrackName(track_type.value, track_index, name)

    def update_marker_custom_data(self, frame_id: int, custom_data: str) -> bool:
        """Updates customData (string) for the marker at given frameId position. 
        CustomData is not exposed via UI and is useful for scripting developer to attach any user specific data to markers.
        """
        return self.timeline.UpdateMarkerCustomData(frame_id, custom_data)

    #######################################################################################################################
    # Add at DR18.0.0

    def set_start_timecode(self, timecode: str) -> bool:
        """Set the start timecode of the timeline to the string 'timecode'. Returns true when the change is successful, false otherwise."""
        return self.timeline.SetStartTimecode(timecode)

    def get_start_timecode(self) -> str:
        """Returns the start timecode for the timeline."""
        return self.timeline.GetStartTimecode()

    def insert_fusion_composition_into_timeline(self) -> TimelineItem:
        """Inserts a Fusion composition into the timeline.Returns a TimelineItem object."""
        return TimelineItem(self.timeline.InsertFusionCompositionIntoTimeline())

    def get_unique_id(self) -> str:
        """Returns a unique ID for the timeline"""
        return self.timeline.GetUniqueId()

    ##############################################################################################################################
    # Add at DR18.5.0
    def add_track(self, track_type: TrackType, optional_sub_track_type: OptionalSubTrackType) -> bool:
        """Adds track of trackType ("video", "subtitle", "audio").
        Second argument optionalSubTrackType is required for "audio"

        Args:
            track_type (TrackType): track type
            optional_sub_track_type (OptionalSubTrackType): Second argument optionalSubTrackType is required for "audio"

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline.AddTrack(track_type.value, optional_sub_track_type.value)

    def delete_track(self, track_type: TrackType, track_index: int) -> bool:
        """Deletes track of trackType ("video", "subtitle", "audio") and given trackIndex. 


        Args:
            track_type (TrackType): track type
            track_index (int): track index.1 <= track_index <= get_track_count(track_type).

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline.DeleteTrack(track_type.value, track_index)

    def set_track_enable(self, track_type: TrackType, track_index: int, is_enable: bool) -> bool:
        """Enables/Disables track with given trackType and trackIndex



        Args:
            track_type (TrackType): trackType is one of {"audio", "video", "subtitle"}
            track_index (int): 1 <= trackIndex < GetTrackCount(trackType).
            is_enable (bool): enable state

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline.SetTrackEnable(track_type.value, track_index, is_enable)

    def get_is_track_enabled(self, track_type, track_index) -> bool:
        """

        Args:
            track_type (_type_): trackType is one of {"audio", "video", "subtitle"}
            track_index (_type_): 1 <= trackIndex <= GetTrackCount(trackType).

        Returns:
            bool: Returns True if track with given trackType and trackIndex is enabled and False otherwise.
        """
        return self.timeline.GetIsTrackEnabled(track_type, track_index)

    def set_track_lock(self, track_type: TrackType, track_index: int, is_locked: bool) -> bool:
        """Locks/Unlocks track with given trackType and trackIndex

        Args:
            track_type (TrackType): trackType is one of {"audio", "video", "subtitle"}
            track_index (int): 1 <= trackIndex <= GetTrackCount(trackType).
            is_locked (bool):  lock state

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline.SetTrackLock(track_type, track_index, is_locked)

    def get_is_track_locked(self, track_type: TrackType, track_index: int) -> bool:
        """Returns True if track with given trackType and trackIndex is locked and False otherwise.


        Args:
            track_type (TrackType): trackType is one of {"audio", "video", "subtitle"}
            track_index (int): 1 <= trackIndex <= GetTrackCount(trackType).

        Returns:
            bool: Returns True if track with given trackType and trackIndex is locked and False otherwise.
        """
        return self.timeline.GetIsTrackLocked(track_type, track_index)

    def delete_clips(self, timeline_items: List[TimelineItem], ripple_delete: bool = False) -> bool:
        """Deletes specified TimelineItems from the timeline

        Args:
            timeline_items (List[TimelineItem]): specified TimelineItems
            ripple_delete (bool): performing ripple delete if the second argument is True.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline.DeleteClips([timeline_item.timeline_item for timeline_item in timeline_items], ripple_delete)

    def set_clips_linked(self, timeline_items: List[TimelineItem], is_linked: bool) -> bool:
        """Links or unlinks the specified TimelineItems depending on second argument.

        Args:
            timeline_items (List[TimelineItem]): specified TimelineItems
            is_linked (bool): Links or unlinks the specified TimelineItems

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.timeline.SetClipsLinked([timeline_item.timeline_item for timeline_item in timeline_items], is_linked)

    def create_subtitles_from_audio(self,auto_caption_settings:AutoCaptionSettings) -> bool:
        #Modified at DR 18.6.4
        """Creates subtitles from audio for the timeline. 

        Returns:
            bool: Returns True on success, False otherwise.
        """
        return self.timeline.CreateSubtitlesFromAudio(auto_caption_settings.asdict())
    
    def detect_scene_cuts(self) -> bool:
        """Detects and makes scene cuts along the timeline. 

        Returns:
            bool: Returns True if successful, False otherwise.
        """
        return self.timeline.DetectSceneCuts()  
    
    ##############################################################################################################################
    # Add at DR18.6.4
    def convert_timeline_to_stereo(self) -> bool:
        """Converts timeline to stereo.

        Returns:
            bool: Returns True if successful; False otherwise.
        """        
        return self.timeline.ConvertTimelineToStereo()
    