from pathlib import Path
from typing import TYPE_CHECKING, List

from multimethod import multimethod
from pybmd._wrapper_base import WrapperBase
from pybmd.decorators import requires_resolve_version
from pybmd.folder import Folder
from pybmd.media_pool_item import MediaPoolItem

from pybmd.timeline import Timeline
from pybmd.timeline_item import TimelineItem

from dataclasses import dataclass
from dataclasses import asdict

if TYPE_CHECKING:
    from pybmd.settings import AudioSyncSetting, MulticamOptions
# TODO clip info for multi version compatible


@dataclass
class ClipInfo:
    """ClipInfo dataclass

    One entry of the ``clipInfo`` list taken by ``MediaPool.append_to_timeline`` and
    ``MediaPool.create_timeline_from_clips``. Only ``media_pool_item`` is required -
    every field left at ``None`` is omitted from the dict handed to DaVinci Resolve, so
    Resolve applies its own default (the whole clip, both video and audio, appended after
    the last clip).

    Args:
        media_pool_item (MediaPoolItem): clip to place
        start_frame (int, optional): first source frame. Defaults to None.
        end_frame (int, optional): last source frame. Defaults to None.
        media_type (int, optional): 1 - video only, 2 - audio only; None for both.
            Defaults to None.
        track_index (int, optional): target track. Defaults to None.
        record_frame (int | float, optional): timeline frame to place the clip at.
            Defaults to None.
    """

    media_pool_item: MediaPoolItem
    start_frame: int | None = None
    end_frame: int | None = None
    media_type: int | None = None
    track_index: int | None = None
    record_frame: int | float | None = None

    def to_dict(self) -> dict:
        clip_info: dict = {"mediaPoolItem": self.media_pool_item._media_pool_item}
        optional_keys = {
            "startFrame": self.start_frame,
            "endFrame": self.end_frame,
            "mediaType": self.media_type,
            "trackIndex": self.track_index,
            "recordFrame": self.record_frame,
        }
        clip_info.update(
            {key: value for key, value in optional_keys.items() if value is not None}
        )
        return clip_info


@dataclass
class ImportClipInfo:
    """ImportClipInfo dataclass

    One entry of the ``clipInfo`` list taken by ``MediaPool.import_media``. Used to
    import an image sequence as a single MediaPoolItem.
    """

    file_path: str
    start_index: int | None = None
    end_index: int | None = None

    def to_dict(self) -> dict:
        clip_info: dict = {"FilePath": self.file_path}
        if self.start_index is not None:
            clip_info["StartIndex"] = self.start_index
        if self.end_index is not None:
            clip_info["EndIndex"] = self.end_index
        return clip_info


@dataclass
class TimelineImportOptions:
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


class MediaPool(WrapperBase):
    """MediaPool Object"""

    def __init__(self, media_pool):
        super(MediaPool, self).__init__(media_pool)
        self._media_pool = self._object

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
    @requires_resolve_version(
        deprecated_in="21.1.0",
        moved_to="MediaPool.append_to_timeline([ClipInfo])",
        notes="Deprecated calling convention since DR 21.1.0. Pass a list of ClipInfo instead",
    )
    def append_to_timeline(self, clips: List["MediaPoolItem"]) -> List[TimelineItem]:
        """append clips to current timeline

        Args:
            clips (List[MediaPoolItem]|List[ClipInfo]): clips to append to current timeline

        Returns:
            List[TimelineItem]: timeline items of appended clips at timeline

        Deprecated:
            Passing a list of MediaPoolItem is a deprecated calling convention since
            DaVinci Resolve 21.1.0. Pass a list of :class:`ClipInfo` instead.
        """

        temp_list = self._media_pool.AppendToTimeline(
            [clip._media_pool_item for clip in clips]
        )
        return [TimelineItem(timeline_item) for timeline_item in temp_list]

    @multimethod
    def append_to_timeline(  # noqa: F811
        self, clip_info_list: List["ClipInfo"]
    ) -> List["TimelineItem"]:
        temp_list = self._media_pool.AppendToTimeline(
            [clip_info.to_dict() for clip_info in clip_info_list]
        )
        return [TimelineItem(timeline_item) for timeline_item in temp_list]

    def create_empty_timeline(self, name) -> Timeline:
        """create empty timeline"""
        return Timeline(self._media_pool.CreateEmptyTimeline(name))

    @multimethod
    @requires_resolve_version(
        deprecated_in="21.1.0",
        moved_to="MediaPool.create_timeline_from_clips(name, [ClipInfo])",
        notes="Deprecated calling convention since DR 21.1.0. Pass a list of ClipInfo instead",
    )
    def create_timeline_from_clips(
        self, name: str, clips: List["MediaPoolItem"]
    ) -> Timeline:
        """create new timeline from clips with name

        Args:
            name (str): new timeline name
            clips (List[MediaPoolItem]): clips to create timeline from

        Returns:
            Timeline: new timeline object

        Deprecated:
            Deprecated calling convention since DaVinci Resolve 21.1.0, use
            ``create_timeline_from_clips(name, [ClipInfo(...), ...])`` instead.
        """
        return Timeline(
            self._media_pool.CreateTimelineFromClips(
                name, [clip._media_pool_item for clip in clips]
            )
        )

    @multimethod
    def create_timeline_from_clips(  # noqa: F811
        self, name: str, clip_info_list: List["ClipInfo"]
    ) -> Timeline:
        """create new timeline from ClipInfo list with name

        Args:
            name (str): new timeline name
            clip_info_list (List[ClipInfo]): clip infos to create timeline from

        Returns:
            Timeline: new timeline object
        """
        return Timeline(
            self._media_pool.CreateTimelineFromClips(
                name, [clip_info.to_dict() for clip_info in clip_info_list]
            )
        )

    def delete_clip_mattes(
        self, media_pool_item: MediaPoolItem, paths: List[str]
    ) -> bool:
        """Delete mattes based on their file paths for specified media pool item

        Args:
            media_pool_item (MediaPoolItem): media pool item to delete mattes for
            paths (List[str]): matte file paths to delete

        Returns:
            bool: true if successful, false if not
        """
        return self._media_pool.DeleteClipMattes(
            media_pool_item._media_pool_item, paths
        )

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
        return self._media_pool.DeleteTimelines(
            [timeline._timeline for timeline in timelines]
        )

    def export_metadata(
        self, file_name: str, clips: List[MediaPoolItem] | None = None
    ) -> bool:
        """export metadata to csv file

        Args:
            file_name (str): export metadata csv file name
            clips (List[MediaPoolItem]): clips to export metadata for If no clips are specified, all clips from media pool will be used.

        Returns:
            bool: True if successful, False if not
        """
        if not clips:
            return self._media_pool.ExportMetadata(file_name)

        return self._media_pool.ExportMetadata(
            file_name, [clip._media_pool_item for clip in clips]
        )

    def get_clip_matte_list(self, media_pool_item: MediaPoolItem) -> List[Path]:
        """get list of clip mattes for specified media pool item"""
        path_list = []
        for str_path in self._media_pool.GetClipMatteList(
            media_pool_item._media_pool_item
        ):
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

    @multimethod
    @requires_resolve_version(
        deprecated_in="21.1.0",
        moved_to="MediaPool.import_media([ImportClipInfo])",
        notes="Deprecated calling convention since DR 21.1.0. Pass a list of ImportClipInfo instead",
    )
    def import_media(self, file_paths: List[str]) -> List[MediaPoolItem]:
        """Imports specified file/folder paths into current Media Pool folder.


        Args:
            file_paths (List[str]): Input is an array of file/folder paths.

        Returns:
            List[MediaPoolItem]: Returns a list of the MediaPoolItem created.

        Deprecated:
            Deprecated calling convention since DaVinci Resolve 21.1.0, use
            ``import_media([ImportClipInfo(file_path=path), ...])`` instead.
        """
        media_pool_items = self._media_pool.ImportMedia(file_paths)
        if not media_pool_items:
            return []
        return [
            MediaPoolItem(media_pool_item) for media_pool_item in media_pool_items
        ]

    @multimethod
    def import_media(  # noqa: F811
        self, clip_info_list: List["ImportClipInfo"]
    ) -> List[MediaPoolItem]:
        """Imports file path(s) into current Media Pool folder as specified in the
        ImportClipInfo list.

        Each ImportClipInfo gets imported as one MediaPoolItem unless
        'Show Individual Frames' is turned on.

        Args:
            clip_info_list (List[ImportClipInfo]): clip infos to import, e.g.
                ``[ImportClipInfo("file_%03d.dpx", 1, 100)]`` imports
                "file_[001-100].dpx".

        Returns:
            List[MediaPoolItem]: Returns a list of the MediaPoolItem created. Empty when
                DaVinci Resolve imported nothing.

        Note:
            DaVinci Resolve only accepts this calling convention for image sequences,
            i.e. entries carrying ``start_index`` / ``end_index``. Single media files
            import nothing and yield an empty list - pass their paths as strings instead.
        """
        media_pool_items = self._media_pool.ImportMedia(
            [clip_info.to_dict() for clip_info in clip_info_list]
        )
        if not media_pool_items:
            return []
        return [
            MediaPoolItem(media_pool_item) for media_pool_item in media_pool_items
        ]

    @multimethod
    def import_media(self, clip_info_list: List[dict]) -> List[MediaPoolItem]:  # noqa: F811
        """Imports file path(s) into current Media Pool folder as specified in the
        clipInfo dict list.

        Args:
            clip_info_list (List[dict]): dicts of "FilePath" (str), "StartIndex" (int)
                and "EndIndex" (int), e.g.
                ``[{"FilePath": "file_%03d.dpx", "StartIndex": 1, "EndIndex": 100}]``.

        Returns:
            List[MediaPoolItem]: Returns a list of the MediaPoolItem created. Empty when
                DaVinci Resolve imported nothing.

        Note:
            DaVinci Resolve only accepts this calling convention for image sequences,
            i.e. dicts carrying "StartIndex" / "EndIndex". Single media files import
            nothing and yield an empty list - pass their paths as strings instead.
        """
        media_pool_items = self._media_pool.ImportMedia(clip_info_list)
        if not media_pool_items:
            return []
        return [
            MediaPoolItem(media_pool_item) for media_pool_item in media_pool_items
        ]

    def import_timeline_from_file(
        self, file_path: str, import_option: TimelineImportOptions
    ) -> Timeline:
        """create new timeline from file and import options

        Args:
            file_path (str): timeline file path
            import_option (TimelineImportOptions): timelineimportoptions object

        Returns:
            Timeline: timeline object
        """
        return Timeline(
            self._media_pool.ImportTimelineFromFile(
                str(file_path), asdict(import_option)
            )
        )

    def move_clips(self, clips: List[MediaPoolItem], target_folder: Folder) -> bool:
        """Moves specified clips to target Folder

        Args:
            clips (List[MediaPoolItem]): list of clips to move
            target_folder (Folder): target folder to move clips to

        Returns:
            bool: true if successful, false if not
        """
        return self._media_pool.MoveClips(
            [clip._media_pool_item for clip in clips], target_folder._folder
        )

    def move_folders(self, folders: List[Folder], target_folder: Folder) -> bool:
        """move folders to target folder


        Args:
            folders (List[Folder]): folders to move
            target_folder (Folder): target folder to move folders to

        Returns:
            bool: true if successful, false if not
        """
        return self._media_pool.MoveFolders(
            [folder._folder for folder in folders], target_folder._folder
        )

    def relink_clips(
        self, media_pool_items: List[MediaPoolItem], folder_path: str
    ) -> bool:
        """Update the folder location of specified media pool clips with the specified folderpath

        Args:
            media_pool_items (List[MediaPoolItem]): clips to relink
            folder_path (str): folder path to relink clips to

        Returns:
            bool: True if successful, False if not
        """
        return self._media_pool.RelinkClips(
            [clip._media_pool_item for clip in media_pool_items], str(folder_path)
        )

    def set_current_folder(self, folder: Folder) -> bool:
        """set current folder"""
        return self._media_pool.SetCurrentFolder(folder._folder)

    def unlink_clips(self, media_pool_items: List[MediaPoolItem]) -> bool:
        """Unlink specified media pool clips"""
        return self._media_pool.UnlinkClips(
            [clip._media_pool_item for clip in media_pool_items]
        )

    ##########################################################################################################################
    # Add at DR18.0.0
    @requires_resolve_version(added_in="18.0.0")
    def refresh_folders(self) -> bool:
        """Updates the folders in collaboration mode

        Returns:
            bool: True if successful

        Raises:
            APIVersionError: If Resolve version < 18.0.0

        Version:
            Added in DaVinci Resolve 18.0.0
        """
        return self._media_pool.RefreshFolders()

    def get_unique_id(self) -> str:
        """get unique id of media pool object"""
        return self._media_pool.GetUniqueId()

    ##########################################################################################################################
    # Add at DR18.5.0 Beta

    @requires_resolve_version(added_in="18.5.0")
    def import_folder_from_file(self, file_path: str, source_clips_path: str) -> bool:
        """Returns true if import from given DRB filePath is successful, false otherwise

        Args:
            file_path (str): file path to DRB file
            source_clips_path (str): sourceClipsPath is a tring that specifies a filesystem path to search for source clips if the media is inaccessible in their original path, empty by default

        Returns:
            bool: Returns true if import from given DRB filePath is successful, false otherwise

        Raises:
            APIVersionError: If Resolve version < 18.5.0

        Version:
            Added in DaVinci Resolve 18.5.0 Beta
        """
        return self._media_pool.ImportFolderFromFile(file_path, source_clips_path)

    ##########################################################################################################################
    # Add at DR18.6.4
    @requires_resolve_version(added_in="18.6.4")
    def create_stereo_clip(
        self, left_media_pool_item: MediaPoolItem, right_media_pool_item: MediaPoolItem
    ) -> MediaPoolItem:
        """Takes in two existing media pool items and creates a new 3D stereoscopic media pool entry replacing the input media in the media pool.

        Args:
            left_media_pool_item (MediaPoolItem): left media pool item
            right_media_pool_item (MediaPoolItem): right media pool item

        Returns:
            MediaPoolItem: 3D stereoscopic media pool entry

        Raises:
            APIVersionError: If Resolve version < 18.6.4

        Version:
            Added in DaVinci Resolve 18.6.4
        """
        return MediaPoolItem(
            self._media_pool.CreateStereoClip(
                left_media_pool_item._media_pool_item,
                right_media_pool_item._media_pool_item,
            )
        )

    ##########################################################################################################################
    # Add at DR19.0.2
    @requires_resolve_version(added_in="19.0.2")
    def get_selected_clips(self) -> List[MediaPoolItem]:
        """Returns the current selected MediaPoolItems

        Returns:
            List[MediaPoolItem]: current selected MediaPoolItems

        Raises:
            APIVersionError: If Resolve version < 19.0.2

        Version:
            Added in DaVinci Resolve 19.0.2
        """
        media_pool_items = list()
        for mp_item in self._media_pool.GetSelectedClips():
            media_pool_items.append(MediaPoolItem(mp_item))
        return media_pool_items

    @requires_resolve_version(added_in="19.0.2")
    def set_selected_clip(self, media_pool_item: MediaPoolItem) -> bool:
        """Sets the selected MediaPoolItem to the given MediaPoolItem

        Args:
            media_pool_item (MediaPoolItem): selected MediaPoolItem

        Returns:
            bool: Returns true if successful, false if not
        """
        return self._media_pool.SetSelectedClip(media_pool_item._media_pool_item)

    ##########################################################################################################################
    # Add at DR19.1.0

    @requires_resolve_version(
        added_in="19.1.0", notes="Currently non-functional due to API issues"
    )
    def auto_sync_audio(
        self,
        media_pool_items: List["MediaPoolItem"],
        audio_sync_settings: "AudioSyncSetting",
    ) -> bool:
        """Syncs audio for specified [MediaPoolItems] (list). The list must contain a minimum of two MediaPoolItems - at least one video and one audio clip.
        #BUG NOT WORKING IN DR19.1.X because Resolve's API not working

        Args:
            media_pool_items (List[MediaPoolItem]): _description_
            audio_sync_settings (AudioSyncSetting): _description_

        Returns:
            bool: Returns True if successful. Refer to 'AudioSyncSetting' section for details.

        Raises:
            APIVersionError: If Resolve version < 19.1.0

        Version:
            Added in DaVinci Resolve 19.1.0
        """
        return self._media_pool.AutoSyncAudio(media_pool_items, audio_sync_settings)

    ##########################################################################################################################
    # Add at DR 21.1.0

    @requires_resolve_version(added_in="21.1.0")
    def create_multicam_clip(
        self,
        clips: List["MediaPoolItem"],
        multicam_options: "MulticamOptions | dict",
    ) -> List["MediaPoolItem"]:
        """Creates a multicam clip from the specified [MediaPoolItems] (list).

        Args:
            clips (List[MediaPoolItem]): MediaPoolItems to build the multicam clip from.
            multicam_options (MulticamOptions | dict): Multicam creation options. Refer
                to 'MulticamOptions' section for details.

        Returns:
            List[MediaPoolItem]: The created multicam clip(s). Empty list if creation failed.

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        media_pool_items = [clip._media_pool_item for clip in clips]
        options_dict = (
            multicam_options
            if isinstance(multicam_options, dict)
            else multicam_options.model_dump(exclude_none=True)
        )
        multicam_clips = self._media_pool.CreateMulticamClip(
            media_pool_items, options_dict
        )
        if not multicam_clips:
            return []
        return [MediaPoolItem(multicam_clip) for multicam_clip in multicam_clips]
