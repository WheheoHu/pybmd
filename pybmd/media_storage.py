from typing import TYPE_CHECKING, List, cast

from pydantic import BaseModel, ConfigDict, Field

from pybmd._wrapper_base import WrapperBase
from pybmd.decorators import (
    requires_resolve_version,
    warn_deprecated_calling_convention,
)
from pybmd.media_pool_item import MediaPoolItem

if TYPE_CHECKING:
    from pybmd.settings import CloneStatus, CloneToolSettings


class Item_Info(BaseModel):
    """Item Info

    ``start_frame`` / ``end_frame`` are serialized as the ``startFrame`` / ``endFrame``
    keys DaVinci Resolve expects, so dump this model with ``model_dump(by_alias=True)``.
    Both the snake_case field names and the Resolve key names are accepted on init.
    """

    model_config = ConfigDict(populate_by_name=True)

    media: str
    start_frame: int = Field(
        ...,
        alias="startFrame",
        description="Start frame of the media item",
        ge=0,
    )
    end_frame: int = Field(
        ...,
        alias="endFrame",
        description="End frame of the media item",
        ge=0,
    )


class MediaStorage(WrapperBase):
    """MediaStorage."""

    def __init__(self, media_storage):
        super(MediaStorage, self).__init__(media_storage)
        self._media_storage = self._object

    def add_clip_mattes_to_media_pool(
        self, media_pool_item: MediaPoolItem, paths: List[str], stereo_eye: str
    ) -> bool:
        """Adds specified media files as mattes for the specified MediaPoolItem

        Args:
            media_pool_item (MediaPoolItem): MediaPoolItem to add mattes to
            paths (List[str]): file paths to add as mattes
            stereo_eye (str, optional): specifying which eye to add the matte to for stereo clips ("left" or "right"). Defaults to None.

        Returns:
            bool: True if success, False if fail
        """
        return self._media_storage.AddClipMattesToMediaPool(
            media_pool_item._media_pool_item, paths, stereo_eye
        )

    def add_item_list_to_media_pool(
        self, items: List[str] | List[Item_Info]
    ) -> List[MediaPoolItem]:
        """Adds specified file/folder paths from Media Storage into current Media Pool folder.

        Args:
            items (List[str]): an array of file/folder paths
            items (List[Item_Info]): an array of Item_info
        Returns:
            List[MediaPoolItem]: a list of MediaPoolItem objects created from the added items

        Deprecated:
            Passing a list of plain paths is a deprecated calling convention since DaVinci
            Resolve 21.1.0. Pass a list of :class:`Item_Info` instead.
        """
        if all(isinstance(item, str) for item in items):
            warn_deprecated_calling_convention(
                "MediaStorage.add_item_list_to_media_pool([path, ...])",
                deprecated_in="21.1.0",
                moved_to="add_item_list_to_media_pool([Item_Info(media=path), ...])",
            )
            return [
                MediaPoolItem(media_pool_item)
                for media_pool_item in self._media_storage.AddItemListToMediaPool(items)
            ]
        elif all(isinstance(item, Item_Info) for item in items):
            item_info_list = cast(List[Item_Info], items)
            temp_list = [
                item_info.model_dump(by_alias=True) for item_info in item_info_list
            ]
            return [
                MediaPoolItem(media_pool_item)
                for media_pool_item in self._media_storage.AddItemListToMediaPool(
                    temp_list
                )
            ]
        else:
            raise ValueError("Invalid item type. Must be List[str] or List[Item_Info].")

    def add_timeline_mattes_to_media_pool(self, paths) -> List[MediaPoolItem]:
        """Adds specified media files as timeline mattes in current media pool folder.

        Args:
            paths (_type_): one or more file/folder paths.

        Returns:
            List[MediaPoolItem]:a list of created MediaPoolItem
        """

        # media_pool_item_list = []
        # for media_pool_item in self.media_storage.AddTimelineMattesToMediaPool(paths):
        #     media_pool_item_list.append(MediaPoolItem(media_pool_item))
        # return media_pool_item_list
        return [
            MediaPoolItem(media_pool_item)
            for media_pool_item in self._media_storage.AddTimelineMattesToMediaPool(
                paths
            )
        ]

    def get_file_list(self, folder_path: str) -> List[str]:
        """Returns list of media and file listings in the given absolute folder path.

        Args:
            folder_path (str): absolute folder path

        Returns:
            List[str]: file listings in the given absolute folder path NOTE:media listings may be logically consolidated entries
        """
        return self._media_storage.GetFileList(str(folder_path))

    def get_mounted_volume_list(self) -> List[str]:
        """Returns list of folder paths corresponding to mounted volumes displayed in Resolve’s Media Storage."""
        return self._media_storage.GetMountedVolumeList()

    def get_sub_folder_list(self, folder_path: str) -> List[str]:
        """Returns list of folder paths in the given absolute folder path."""
        return self._media_storage.GetSubFolderList(str(folder_path))

    def reveal_in_storage(self, path: str) -> bool:
        """Expands and displays given file/folder path in Resolve’s Media Storage."""
        return self._media_storage.RevealInStorage(str(path))

    ##########################################################################################################################
    # Add at DR 21.1.0

    @requires_resolve_version(added_in="21.1.0")
    def start_clone_media(self, source_dir: str, target_dirs: str | List[str]) -> bool:
        """Starts cloning media from 'source_dir' to 'target_dirs'.

        Use :meth:`set_clone_tool_settings` to configure ``PreserveFolderName`` and
        ``ChecksumType`` beforehand.

        Note:
            Every target folder has to exist already - DaVinci Resolve returns False
            instead of creating it.

        Args:
            source_dir (str): source folder path
            target_dirs (str | List[str]): one target folder path, or a list of them

        Returns:
            bool: Returns True if the clone job was started, False otherwise

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        if isinstance(target_dirs, str):
            targets = str(target_dirs)
        else:
            targets = [str(target_dir) for target_dir in target_dirs]
        return self._media_storage.StartCloneMedia(str(source_dir), targets)

    @requires_resolve_version(added_in="21.1.0")
    def stop_clone_media(self) -> bool:
        """Stops the clone job currently in progress, started via :meth:`start_clone_media`.

        Returns:
            bool: Returns True if successful, False if no clone job is in progress

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._media_storage.StopCloneMedia()

    @requires_resolve_version(added_in="21.1.0")
    def get_clone_status(self) -> "CloneStatus | dict":
        """Returns the status of the current (or most recently started) clone job.

        Returns:
            CloneStatus | dict: Clone job status, an empty dict if no status was returned.
                ``JobStatus`` is "Complete" when no clone job has been started yet.
                Refer to 'Clone Tool Settings' section for details.

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        from pybmd.settings import CloneStatus

        clone_status = self._media_storage.GetCloneStatus()
        if not clone_status:
            return {}
        return CloneStatus(**clone_status)

    @requires_resolve_version(added_in="21.1.0")
    def set_clone_tool_settings(
        self, clone_tool_settings: "CloneToolSettings | dict | None" = None
    ) -> bool:
        """Sets the options used by subsequent :meth:`start_clone_media` calls, and by
        the Clone Tool in the UI.

        Args:
            clone_tool_settings (CloneToolSettings | dict, optional): Clone tool
                settings. Resets to defaults when omitted. Refer to
                'Clone Tool Settings' section for details. Defaults to None.

        Returns:
            bool: Returns True if successful, False otherwise

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        if clone_tool_settings is None:
            settings_dict: dict = {}
        elif isinstance(clone_tool_settings, dict):
            settings_dict = clone_tool_settings
        else:
            settings_dict = clone_tool_settings.model_dump(exclude_none=True)
        return self._media_storage.SetCloneToolSettings(settings_dict)
