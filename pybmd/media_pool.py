from pathlib import Path
from typing import Dict, Iterable, List
from pybmd.folder import Folder
from pybmd.media_pool_item import MediaPoolItem
from pybmd.timeline import Timeline
from pybmd.timeline_item import TimelineItem

from dataclasses import dataclass
from dataclasses import asdict
from multipledispatch import dispatch


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

    @dispatch(List[MediaPoolItem])
    def append_to_timeline(self, clips: List[MediaPoolItem]) -> List[TimelineItem]: # type: ignore
        timeline_item_list = []
        for timeline_item in self.media_pool.AppendToTimeline([clip.media_pool_item for clip in clips]):
            timeline_item_list.append(TimelineItem(timeline_item))
        return timeline_item_list

    @dispatch(List[ClipInfo])
    def append_to_timeline(self, clips: List[ClipInfo]) -> List[TimelineItem]:
        timeline_item_list = []
        for timeline_item in self.media_pool.AppendToTimeline([asdict(ClipInfo) for ClipInfo in clips]):
            timeline_item_list.append(TimelineItem(timeline_item))
        return timeline_item_list

    def create_empty_timeline(self, name) -> Timeline:
        return Timeline(self.media_pool.CreateEmptyTimeline(name))

    @dispatch(str, Iterable)
    def create_timeline_from_clips(self, name: str, clips: List[MediaPoolItem]) -> Timeline:  # type: ignore
        return Timeline(self.media_pool.CreateTimelineFromClips(name, [clip.media_pool_item for clip in clips]))

    @dispatch(str, List[ClipInfo])
    def create_timeline_from_clips(self, name: str, clip_infos: List[ClipInfo]) -> Timeline:
        return self.media_pool.CreateTimelineFromClips(name, [asdict(ClipInfo) for ClipInfo in clip_infos]) 

    def delete_clip_mattes(self, media_pool_item: MediaPoolItem, paths: List[str]) -> bool:
        return self.media_pool.DeleteClipMattes(media_pool_item, paths)

    def delete_clips(self, clips: List[MediaPoolItem]) -> bool:
        return self.media_pool.DeleteClips([clip.media_pool_item for clip in clips])

    def delete_folders(self, subfolders: List[Folder]) -> bool:
        return self.media_pool.DeleteFolders([folder.folder for folder in subfolders])

    def delete_timelines(self, timelines: List[Timeline]) -> bool:
        return self.media_pool.DeleteTimelines([timeline.timeline for timeline in timelines])

    def export_metadata(self, file_name: str, clips: List[MediaPoolItem]) -> bool:
        return self.media_pool.ExportMetadata(file_name, [clip.media_pool_item for clip in clips])

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

    @dispatch(List[str])
    def import_media(self, file_paths: List[str]) -> List[MediaPoolItem]: # type: ignore
        media_pool_item_list = []
        for media_pool_item in self.media_pool.ImportMedia(file_paths):
            media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return media_pool_item_list

    @dispatch(List[dict])
    def import_media(self, clip_info: List[dict]) -> List[MediaPoolItem]:
        media_pool_item_list = []
        for media_pool_item in self.media_pool.ImportMedia(clip_info):
            media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return media_pool_item_list

    def import_timeline_from_file(self, file_path: str, import_option: TimelineImportOptions) -> Timeline:
        return Timeline(self.media_pool.ImportTimelineFromFile(str(file_path), asdict(import_option)))

    def move_clips(self, clips: List[MediaPoolItem], target_folder: Folder) -> bool:
        return self.media_pool.MoveClips([clip.media_pool_item for clip in clips], target_folder)

    def move_folders(self, folders: List[Folder], target_folder: Folder) -> bool:
        return self.media_pool.MoveFolders([folder.folder for folder in folders], target_folder)

    def relink_clips(self, media_pool_items: List[MediaPoolItem], folder_path: str) -> bool:
        return self.media_pool.RelinkClips([clip.media_pool_item for clip in media_pool_items], str(folder_path))

    def set_current_folder(self, folder: Folder) -> bool:
        return self.media_pool.SetCurrentFolder(folder)

    def unlink_clips(self, media_pool_items: List[MediaPoolItem]) -> bool:
        return self.media_pool.UnlinkClips([clip.media_pool_item for clip in media_pool_items])
