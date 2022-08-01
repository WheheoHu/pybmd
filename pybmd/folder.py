from typing import List
from pybmd.media_pool_item import MediaPoolItem


class Folder():
    
    def __init__(self, folder):
        self.folder = folder
        
    def get_clip_list(self) -> List[MediaPoolItem]:
        """Returns list of MediaPoolItem objects for all clips in this folder."""
        media_pool_item_list = []
        for media_pool_item in self.folder.GetClipList():
            media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return media_pool_item_list

    def get_name(self) -> str:
        """Returns name of this folder."""
        return self.folder.GetName()
    
    def get_sub_folder_list(self) -> List['Folder']:
        """Return a list of sub folders in this folder."""
        folder_list = []
        for folder in self.folder.GetSubFolderList():
            folder_list.append(Folder(folder))
        return folder_list
    
    ###########################################################################
    #Add at DR18.0.0
    def get_is_folder_stale(self) -> bool:
        """Returns true if folder is stale in collaboration mode, false otherwise"""
        return self.folder.GetIsFolderStale()
    
    def get_unique_id(self) -> str:
        """Returns a unique ID for the media pool folder"""
        return self.folder.GetUniqueId()
    
    ###########################################################################
    
    