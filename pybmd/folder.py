from typing import List
from pybmd.media_pool_item import MediaPoolItem


class Folder():
    """docstring for Folder."""
    def __init__(self, folder):
        self.folder = folder
        
    def get_clip_list(self) -> List[MediaPoolItem]:
        media_pool_item_list = []
        for media_pool_item in self.folder.GetClipList():
            media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return media_pool_item_list

    def get_name(self) -> str:
        return self.folder.GetName()
    
    def get_sub_folder_list(self) -> List['Folder']:
        folder_list = []
        for folder in self.folder.GetSubFolderList():
            folder_list.append(Folder(folder))
        return folder_list
    
    ###########################################################################
    #Add at DR18.0.0
    def get_is_folder_stale(self) -> bool:
        return self.folder.GetIsFolderStale()
    
    def get_unique_id(self) -> str:
        return self.folder.GetUniqueId()
    
    ###########################################################################
    
    