
from os import path
from typing import TYPE_CHECKING, List

from pybmd.media_pool_item import MediaPoolItem
if TYPE_CHECKING:
    from pybmd.resolve import Resolve

from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class Item_Info():
    """Item Info"""
    media: str
    start_frame: int
    end_frame: int


class MediaStorage:
    """MediaStorage."""

    def __init__(self, media_storage):
        self._media_storage = media_storage

    def add_clip_mattes_to_media_pool(self, media_pool_item: MediaPoolItem, paths: List[str], stero_eye: str = None) -> bool:
        """Adds specified media files as mattes for the specified MediaPoolItem

        Args:
            media_pool_item (MediaPoolItem): MediaPoolItem to add mattes to
            paths (List[str]): file paths to add as mattes
            stero_eye (str, optional): specifying which eye to add the matte to for stereo clips ("left" or "right"). Defaults to None.

        Returns:
            bool: True if success, False if fail
        """
        return self._media_storage.AddClipMattesToMediaPool(media_pool_item, paths, stero_eye)

    def add_item_list_to_meida_pool(self, items: List[str] | List[Item_Info]) -> List[MediaPoolItem]:
        """Adds specified file/folder paths from Media Storage into current Media Pool folder. 

        Args:
            items (List[str]): an array of file/folder paths
            items (List[Item_Info]): an array of Item_info
        Returns:
            List[MediaPoolItem]: a list of MediaPoolItem objects created from the added items
        """
        # media_pool_item_list = []
        # for media_pool_item in self.media_storage.AddItemListToMeidaPool(item_path_list):
        #     media_pool_item_list.append(MediaPoolItem(media_pool_item))
        # return media_pool_item_list
        if type(items[0]) is str:
            return [MediaPoolItem(media_pool_item) for media_pool_item in self._media_storage.AddItemListToMediaPool(items)]
        elif type(items[0]) is Item_Info:
            temp_list=[asdict(item_info) for item_info in items]
            return [MediaPoolItem(media_pool_item) for media_pool_item in self._media_storage.AddItemListToMediaPool(temp_list)]

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
        return [MediaPoolItem(media_pool_item) for media_pool_item in self._media_storage.AddTimelineMattesToMediaPool(paths)]

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
