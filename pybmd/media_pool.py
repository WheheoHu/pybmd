from pathlib import Path
from typing import  List

from multimethod import multimethod
from pybmd.folder import Folder
from pybmd.media_pool_item import MediaPoolItem
from pybmd.timeline import Timeline
from pybmd.timeline_item import TimelineItem

from dataclasses import dataclass
from dataclasses import asdict

# TODO clip info for multi version compatible


@dataclass
class ClipInfo():
    """ClipInfo dataclass"""
    media_pool_item: MediaPoolItem
    start_frame: int
    end_frame: int
    media_type: int
    track_index: int
    record_frame: int | float
    
    def to_dict(self):
        return {
            "mediaPoolItem": self.media_pool_item._media_pool_item,
            "startFrame": self.start_frame,
            "endFrame": self.end_frame,
            "mediaType": self.media_type,
            "trackIndex": self.track_index,
            "recordFrame": self.record_frame
        }



@dataclass
class TimelineImportOptions():
    """TimelineImportOptions dataclass"""
    timeline_name: str
    import_source_clips: bool
    source_clips_path: str
    source_clips_folders: List[str]
    interlace_pricessing: bool


# def asdict_inside_list(list: list) -> list:
#     return_list = []
#     for value in list:
#         return_list.append(asdict(value))
#     return return_list


class MediaPool():
    """ MediaPool Object """

    def __init__(self, media_pool):
        self._media_pool = media_pool

    def add_sub_folder(self, folder: Folder, name: str) -> Folder:
        """add sub folder to folder

        Args:
            folder (Folder): folder to add sub folder to 
            name (str): name of new sub folder

        Returns:
            Folder: folder object of new sub folder
        """
        return Folder(self._media_pool.AddSubFolder(folder._folder, name))

    @multimethod
    def append_to_timeline(self, clips: List['MediaPoolItem']) -> List[TimelineItem]:
        """append clips to current timeline

        Args:
            clips (List[MediaPoolItem]|List[ClipInfo]): clips to append to current timeline

        Returns:
            List[TimelineItem]: timeline items of appended clips at timeline
        """

        temp_list = self._media_pool.AppendToTimeline(
                [clip._media_pool_item for clip in clips])
        return [TimelineItem(timeline_item) for timeline_item in temp_list]
    
    @multimethod
    def append_to_timeline(self, clip_info_list: List['ClipInfo']) -> List['TimelineItem']:
        temp_list = self._media_pool.AppendToTimeline(
                [clip_info.to_dict() for clip_info in clip_info_list])
        return [TimelineItem(timeline_item) for timeline_item in temp_list]
    

    def create_empty_timeline(self, name) -> Timeline:
        """create empty timeline"""
        return Timeline(self._media_pool.CreateEmptyTimeline(name))

    # @dispatch(str, Iterable)
    # type: ignore
    def create_timeline_from_clips(self, name: str, clips) -> Timeline:
        """create new timeline from clips with name

        Args:
            name (str): new timeline name
            clips (_type_): clips to create timeline from

        Returns:
            Timeline: new timeline object
        """
        if type(clips[0]) is MediaPoolItem:
            return Timeline(self._media_pool.CreateTimelineFromClips(name, [clip.media_pool_item for clip in clips]))
        elif type(clips[0]) is ClipInfo:
            return Timeline(self._media_pool.CreateTimelineFromClips(name, [asdict(ClipInfo) for clip in clips]))

    # @dispatch(str, List[ClipInfo])
    # def create_timeline_from_clips(self, name: str, clip_infos: List[ClipInfo]) -> Timeline:
    #     return self.media_pool.CreateTimelineFromClips(name, [asdict(ClipInfo) for ClipInfo in clip_infos])

    def delete_clip_mattes(self, media_pool_item: MediaPoolItem, paths: List[str]) -> bool:
        """Delete mattes based on their file paths for specified media pool item

        Args:
            media_pool_item (MediaPoolItem): meida pool item to delete mattes for
            paths (List[str]): matte file paths to delete

        Returns:
            bool: true if successful, false if not
        """
        return self._media_pool.DeleteClipMattes(media_pool_item, paths)

    def delete_clips(self, clips: List[MediaPoolItem]) -> bool:
        """Delete clips from media pool"""
        return self._media_pool.DeleteClips([clip._media_pool_item for clip in clips])

    def delete_folders(self, subfolders: List[Folder]) -> bool:
        """delete folders from media pool"""
        return self._media_pool.DeleteFolders([folder._folder for folder in subfolders])

    def delete_timelines(self, timelines: List[Timeline]) -> bool:
        """delete timelines from media pool

        Args:
            timelines (List[Timeline]): list of timelines to delete

        Returns:
            bool: true if successful, false if not
        """
        return self._media_pool.DeleteTimelines([timeline._timeline for timeline in timelines])

    def export_metadata(self, file_name: str, clips: List[MediaPoolItem]) -> bool:
        """export metadata to csv file

        Args:
            file_name (str): export metadata csv file name
            clips (List[MediaPoolItem]): clips to export metadata for If no clips are specified, all clips from media pool will be used.

        Returns:
            bool: True if successful, False if not
        """
        return self._media_pool.ExportMetadata(file_name, [clip._media_pool_item for clip in clips])

    def get_clip_matte_list(self, media_pool_item) -> List[Path]:
        """get list of clip mattes for specified media pool item"""
        path_list = []
        for str_path in self._media_pool.GetClipMatteList(media_pool_item):
            path_list.append(Path(str_path))
        return path_list

    def get_current_folder(self) -> Folder:
        """get current folder

        Returns:
            Folder: current folder object
        """
        return Folder(self._media_pool.GetCurrentFolder())

    def get_root_folder(self) -> Folder:
        """return root folder object of media pool

        Returns:    
            Folder: root folder object
        """
        return Folder(self._media_pool.GetRootFolder())

    def get_timeline_matte_list(self, folder: Folder) -> List[MediaPoolItem]:
        """Get mattes in specified Folder

        Args:
            folder (Folder): folder to get mattes for

        Returns:
            List[MediaPoolItem]: list of media pool items that are mattes
        """
        media_pool_item_list = []
        for media_pool_item in self._media_pool.GetTimelineMatteList(folder._folder):
            media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return media_pool_item_list

    # @dispatch(List[str])
    # type: ignore
    def import_media(self, file_paths: List[str]) -> List[MediaPoolItem]:
        """Imports specified file/folder paths into current Media Pool folder. 


        Args:
            file_paths (List[str]): Input is an array of file/folder paths. 

        Returns:
            List[MediaPoolItem]: Returns a list of the MediaPoolItem created.
        """
        # media_pool_item_list = []
        # for media_pool_item in self.media_pool.ImportMedia(file_paths):
        #     media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return [MediaPoolItem(media_pool_item) for media_pool_item in self._media_pool.ImportMedia(file_paths)]

    # @dispatch(List[dict])
    # def import_media(self, clip_info: List[dict]) -> List[MediaPoolItem]:
    #     media_pool_item_list = []
    #     for media_pool_item in self.media_pool.ImportMedia(clip_info):
    #         media_pool_item_list.append(MediaPoolItem(media_pool_item))
    #     return media_pool_item_list

    def import_timeline_from_file(self, file_path: str, import_option: TimelineImportOptions) -> Timeline:
        """create new timeline from file and import options

        Args:
            file_path (str): timeline file path
            import_option (TimelineImportOptions): timelineimportoptions object

        Returns:
            Timeline: timeline object
        """
        return Timeline(self._media_pool.ImportTimelineFromFile(str(file_path), asdict(import_option)))

    def move_clips(self, clips: List[MediaPoolItem], target_folder: Folder) -> bool:
        """Moves specified clips to target Folder 

        Args:
            clips (List[MediaPoolItem]): list of clips to move  
            target_folder (Folder): target folder to move clips to

        Returns:
            bool: true if successful, false if not
        """
        return self._media_pool.MoveClips([clip._media_pool_item for clip in clips], target_folder._folder)

    def move_folders(self, folders: List[Folder], target_folder: Folder) -> bool:
        """move folders to target folder


        Args:
            folders (List[Folder]): folders to move
            target_folder (Folder): target folder to move folders to

        Returns:
            bool: true if successful, false if not
        """
        return self._media_pool.MoveFolders([folder._folder for folder in folders], target_folder._folder)

    def relink_clips(self, media_pool_items: List[MediaPoolItem], folder_path: str) -> bool:
        """Update the folder location of specified media pool clips with the specified folderpath

        Args:
            media_pool_items (List[MediaPoolItem]): clips to relink
            folder_path (str): folder path to relink clips to

        Returns:
            bool: True if successful, False if not
        """
        return self._media_pool.RelinkClips([clip._media_pool_item for clip in media_pool_items], str(folder_path))

    def set_current_folder(self, folder: Folder) -> bool:
        """set current folder"""
        return self._media_pool.SetCurrentFolder(folder._folder)

    def unlink_clips(self, media_pool_items: List[MediaPoolItem]) -> bool:
        """Unlink specified media pool clips"""
        return self._media_pool.UnlinkClips([clip._media_pool_item for clip in media_pool_items])

    ##########################################################################################################################
    # Add at DR18.0.0
    def refresh_folders(self) -> bool:
        """Updates the folders in collaboration mode"""
        return self._media_pool.RefreshFolders()

    def get_unique_id(self) -> str:
        """get unique id of media pool object"""
        return self._media_pool.GetUniqueId()

    ##########################################################################################################################
    # Add at DR18.5.0 Beta

    def import_folder_from_file(self, file_path: str, source_clips_path: str) -> bool:
        """Returns true if import from given DRB filePath is successful, false otherwise

        Args:
            file_path (str): file path to DRB file
            source_clips_path (str): sourceClipsPath is a tring that specifies a filesystem path to search for source clips if the media is inaccessible in their original path, empty by default

        Returns:
            bool: Returns true if import from given DRB filePath is successful, false otherwise
        """
        return self._media_pool.ImportFolderFromFile(file_path, source_clips_path)

    ##########################################################################################################################
    # Add at DR18.6.4
    def create_stereo_clip(self, left_media_pool_item: MediaPoolItem, right_media_pool_item: MediaPoolItem) -> MediaPoolItem:
        """Takes in two existing media pool items and creates a new 3D stereoscopic media pool entry replacing the input media in the media pool.

        Args:
            left_media_pool_item (MediaPoolItem): left media pool item
            right_media_pool_item (MediaPoolItem): right media pool item

        Returns:
            MediaPoolItem: 3D stereoscopic media pool entry
        """
        return MediaPoolItem(self._media_pool.CreateStereoClip(left_media_pool_item._media_pool_item, right_media_pool_item._media_pool_item))
    
    ##########################################################################################################################
    # Add at DR19.0.2
    def get_selected_clips(self) -> List[MediaPoolItem]:
        """Returns the current selected MediaPoolItems

        Returns:
            List[MediaPoolItem]: current selected MediaPoolItems
        """
        media_pool_items = list()
        for mp_item in self._media_pool.GetSelectedClips():
            media_pool_items.append(MediaPoolItem(mp_item))
        return media_pool_items
    

    def set_selected_clip(self,media_pool_item:MediaPoolItem) -> bool:
        """Sets the selected MediaPoolItem to the given MediaPoolItem

        Args:
            media_pool_item (MediaPoolItem): selected MediaPoolItem

        Returns:
            bool: Returns true if successful, false if not
        """
        return self._media_pool.SetSelectedClip(media_pool_item._media_pool_item)