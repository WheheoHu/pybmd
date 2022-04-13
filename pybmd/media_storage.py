
from os import path
from typing import TYPE_CHECKING, List

from pybmd.media_pool_item import MediaPoolItem
if TYPE_CHECKING:
    from pybmd.bmd import Bmd


class MediaStorage:
    """docstring for MediaStorage."""

    media_storage = None

    def __init__(self, _local_davinci: 'Bmd.local_davinci'):
        """davinci media storage

        Args:
            _local_davinci (Bmd.local_davinci): davinci object
        """
        self.media_storage = _local_davinci.GetMediaStorage()

    def add_clip_mattes_to_media_pool(self, media_pool_item: MediaPoolItem, paths: List[str], stero_eye: str = None) -> bool:
        return self.media_storage.AddClipMattesToMediaPool(media_pool_item, paths, stero_eye)

    def add_item_list_to_meida_pool(self, item_path_list: List[str]) -> List[MediaPoolItem]:
        media_pool_item_list = []
        for media_pool_item in self.media_storage.AddItemListToMeidaPool(item_path_list):
            media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return media_pool_item_list

    def add_timeline_mattes_to_media_pool(self, paths) -> List[MediaPoolItem]:
        media_pool_item_list = []
        for media_pool_item in self.media_storage.AddTimelineMattesToMediaPool(paths):
            media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return media_pool_item_list

    def get_file_list(self, folder_list: str) -> List[str]:
        return self.media_storage.GetFileList(str(folder_list))

    def get_mounted_volume_list(self) -> List[str]:
        return self.media_storage.GetMountedVolumeList()

    def get_sub_folder_list(self, folder_path: str) -> List[str]:
        return self.media_storage.GetSubFolderList(str(folder_path))

    def reveal_in_storage(self, path: str) -> bool:
        return self.media_storage.RevealInStorage(str(path))
