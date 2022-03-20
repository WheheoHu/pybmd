from os import path
from pathlib import Path
from typing import Dict, List
from pybmd.folder import Folder
from pybmd.media_pool_item import MediaPoolItem
from pybmd.timeline import Timeline
from pybmd.timeline_item import TimelineItem

from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class ClipInfo():
    """Docstring for ClipInfo."""
    media_pool_item: MediaPoolItem
    start_frame: int
    end_frame: int
    media_type: int


@dataclass
class TimelineImportOptions():
    """Docstring for TimelineImportOptions."""
    timeline_name: str
    import_source_clips: str
    source_clips_path: str
    source_flips_folders: str
    interlace_pricessing: bool


def asdict_inside_list(list: list) -> list:
    return_list = []
    for value in list:
        return_list.append(asdict(value))
    return return_list


class MediaPool():
    """docstring for MediaPool."""

    def __init__(self, media_pool):
        self.media_pool = media_pool

    def add_sub_folder(self, folder: Folder, name: str) -> Folder:
        return Folder(self.media_pool.AddSubFolder(folder, name))
    
    #BUG fix clips list input
    def append_to_timeline(self, clips: List[MediaPoolItem]) -> List[TimelineItem]:
        timeline_item_list = []
        for timeline_item in self.media_pool.AppendToTimeline(clips):
            timeline_item_list.append(TimelineItem(timeline_item))
        return timeline_item_list

    def append_to_timeline(self, clip_infos: List[ClipInfo]) -> List[TimelineItem]:
        timeline_item_list = []
        for timeline_item in self.media_pool.AppendToTimeline(asdict_inside_list(clip_infos)):
            timeline_item_list.append(TimelineItem(timeline_item))
        return timeline_item_list

    def create_empty_timeline(self, name) -> Timeline:
        return Timeline(self.media_pool.CreateEmptyTimeline(name))

    #BUG fix clips list input   
    def create_timeline_from_clips(self, name: str, clips: List[MediaPoolItem]) -> Timeline:
        return Timeline(self.media_pool.CreateTimelineFromClips(name, clips))

    def create_timeline_from_clips(self, name: str, clip_infos: List[ClipInfo]) -> Timeline:
        return self.media_pool.CreateTimelineFromClips(name, asdict_inside_list(clip_infos))

    def delete_clip_mattes(self, media_pool_item: MediaPoolItem, paths: List[str]) -> bool:
        return self.media_pool.DeleteClipMattes(media_pool_item, paths)

    #BUG fix clips list input
    def delete_clips(self, clips: List[MediaPoolItem]) -> bool:
        return self.media_pool.DeleteClips(clips)

    #BUG fix folder list input
    def delete_folders(self, subfolders: List[Folder]) -> bool:
        return self.media_pool.DeleteFolders(subfolders)

    #BUG fix timeline list input
    def delete_timelines(self, timelines: List[Timeline]) -> bool:
        return self.media_pool.DeleteTimelines(timelines)

    #BUG fix clips list input
    def export_metadata(self, file_name: str, clips: List[MediaPoolItem]) -> bool:
        return self.media_pool.ExportMetadata(file_name, clips)

    def get_clip_matte_list(self, media_pool_item) -> List[Path]:
        path_list = []
        for str_path in self.media_pool.GetClipMatteList(media_pool_item):
            path_list.append(Path(str_path))
        return path_list

    def get_current_folder(self) -> Folder:
        return Folder(self.media_pool.GetCurrentFolder())

    def get_root_folder(self) -> Folder:
        return Folder(self.media_pool.GetRootFolder())

    def get_timeline_matte_list(self, folder: Folder) -> List[MediaPoolItem]:
        media_pool_item_list = []
        for media_pool_item in self.media_pool.GetTimelineMatteList(folder):
            media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return media_pool_item_list

    def import_media(self, file_paths: List[str]) -> List[MediaPoolItem]:
        media_pool_item_list = []
        for media_pool_item in self.media_pool.ImportMedia(file_paths):
            media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return media_pool_item_list

    def import_media(self, clip_info: List[dict]) -> List[MediaPoolItem]:
        media_pool_item_list = []
        for media_pool_item in self.media_pool.ImportMedia(clip_info):
            media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return media_pool_item_list

    def import_timeline_from_file(self, file_path: path, import_option: TimelineImportOptions) -> Timeline:
        return Timeline(self.media_pool.ImportTimelineFromFile(str(file_path), asdict(import_option)))

    #BUG fix clips list input
    def move_clips(self, clips: List[MediaPoolItem], target_folder: Folder) -> bool:
        return self.media_pool.MoveClips(clips, target_folder)

    #BUG fix folder list input
    def move_folders(self, folders: List[Folder], target_folder: Folder) -> bool:
        return self.media_pool.MoveFolders(folders, target_folder)

    #BUG fix clips list input
    def relink_clips(self, media_pool_items: List[MediaPoolItem], folder_path: path) -> bool:
        return self.media_pool.RelinkClips(media_pool_items, str(folder_path))

    def set_current_folder(self, folder: Folder) -> bool:
        return self.media_pool.SetCurrentFolder(folder)

    #BUG fix clips list input
    def unlink_clips(self, media_pool_items: List[MediaPoolItem]) -> bool:
        return self.media_pool.UnlinkClips(media_pool_items)
