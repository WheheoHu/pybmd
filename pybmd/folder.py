from typing import List
from pybmd.media_pool_item import MediaPoolItem


class Folder():
    
    def __init__(self, folder):
        self._folder = folder
    
    def __repr__(self) -> str:
        return f'Folder:{self.get_name()}'
        
    def get_clip_list(self) -> List[MediaPoolItem]:
        """Returns list of MediaPoolItem objects for all clips in this folder."""
        media_pool_item_list = []
        for media_pool_item in self._folder.GetClipList():
            media_pool_item_list.append(MediaPoolItem(media_pool_item))
        return media_pool_item_list

    def get_name(self) -> str:
        """Returns name of this folder."""
        return self._folder.GetName()
    
    def get_sub_folder_list(self) -> List['Folder']:
        """Return a list of sub folders in this folder."""
        folder_list = []
        for folder in self._folder.GetSubFolderList():
            folder_list.append(Folder(folder))
        return folder_list
    
    ###########################################################################
    #Add at DR18.0.0
    def get_is_folder_stale(self) -> bool:
        """Returns true if folder is stale in collaboration mode, false otherwise"""
        return self._folder.GetIsFolderStale()
    
    def get_unique_id(self) -> str:
        """Returns a unique ID for the media pool folder"""
        return self._folder.GetUniqueId()
    
    ###########################################################################
    #Add at DR18.5.0
    def export(self,file_path:str) -> bool:
        """Returns true if export of DRB folder to filePath is successful, false otherwise

        Args:
            file_path (str): file path to export DRB file

        Returns:
            bool: Returns true if export of DRB folder to filePath is successful, false otherwise
        """        
        return self._folder.Export(file_path)   
    ###########################################################################
    #Add at DR18.6.4
    def transcribe_audio(self) -> bool:
        """Transcribes audio of the MediaPoolItems within the folder and nested folders.

        Returns:
            bool: Returns True if successful; False otherwise
        """        
        return self._folder.TranscribeAudio()
    
    def clear_transcription(self) -> bool:
        """Clears audio transcription of the MediaPoolItems within the folder and nested folders.

        Returns:
            bool: Returns True if successful; False otherwise.
        """        
        return self._folder.ClearTranscription()
    
    