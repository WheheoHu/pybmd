from enum import Enum
from typing import TYPE_CHECKING, List
from pybmd._wrapper_base import WrapperBase
from pybmd.decorators import requires_resolve_version
from pybmd.media_pool_item import MediaPoolItem

if TYPE_CHECKING:
    from pybmd.settings import MotionDeblurSettings, MarkerColor


class Folder(WrapperBase):
    
    def __init__(self, folder):
        super(Folder, self).__init__(folder)
        self._folder = self._object
    
    def __repr__(self) -> str:
        return f'Folder: {self.get_name()}'
        
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
    def transcribe_audio(self, use_speaker_detection: bool | None = None) -> bool:
        """Transcribes audio of the MediaPoolItems within the folder and nested folders.

        Args:
            use_speaker_detection (bool, optional): Whether to use speaker detection
                when transcribing. If None, the project's setting is used. Defaults to None.

        Returns:
            bool: Returns True if successful; False otherwise
        """
        if use_speaker_detection is None:
            return self._folder.TranscribeAudio()
        return self._folder.TranscribeAudio(use_speaker_detection)

    def clear_transcription(self) -> bool:
        """Clears audio transcription of the MediaPoolItems within the folder and nested folders.

        Returns:
            bool: Returns True if successful; False otherwise.
        """
        return self._folder.ClearTranscription()

    ###########################################################################
    # Add at DR 21.0.2

    @requires_resolve_version(added_in="21.0.2")
    def perform_audio_classification(self) -> bool:
        """Analyzes and classifies the audio of the MediaPoolItems within the folder and nested folders.

        Studio-only. Refer to DaVinci Resolve's "Studio and AI Scripting APIs"
        prerequisites; returns False if requirements are not met.

        Returns:
            bool: Returns True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.0.2

        Version:
            Added in DaVinci Resolve 21.0.2
        """
        return self._folder.PerformAudioClassification()

    @requires_resolve_version(added_in="21.0.2")
    def clear_audio_classification(self) -> bool:
        """Clears audio classification of the MediaPoolItems within the folder and nested folders.

        Studio-only. Refer to DaVinci Resolve's "Studio and AI Scripting APIs"
        prerequisites; returns False if requirements are not met.

        Returns:
            bool: Returns True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.0.2

        Version:
            Added in DaVinci Resolve 21.0.2
        """
        return self._folder.ClearAudioClassification()

    @requires_resolve_version(added_in="21.0.2")
    def remove_motion_blur(
        self, deblur_option: "MotionDeblurSettings | dict"
    ) -> List[List[MediaPoolItem]]:
        """Applies motion deblur on the MediaPoolItems in the folder.

        Studio-only. Refer to DaVinci Resolve's "Studio and AI Scripting APIs"
        prerequisites.

        Args:
            deblur_option (MotionDeblurSettings | dict): Motion deblur settings.
                A ``MotionDeblurSettings`` model or a raw dict.

        Returns:
            List[List[MediaPoolItem]]: A list of ``[original, newly_created]``
                MediaPoolItem pairs.

        Raises:
            APIVersionError: If Resolve version < 21.0.2

        Version:
            Added in DaVinci Resolve 21.0.2
        """
        if isinstance(deblur_option, dict):
            option_dict = deblur_option
        else:
            option_dict = deblur_option.model_dump(exclude_none=True)
        result = self._folder.RemoveMotionBlur(option_dict)
        if not result:
            return []
        return [
            [MediaPoolItem(pair[0]), MediaPoolItem(pair[1])] for pair in result
        ]

    @requires_resolve_version(added_in="21.0.2")
    def analyze_for_intellisearch(
        self, identify_faces: bool, is_better_mode: bool
    ) -> bool:
        """Performs Intellisearch analysis on all MediaPoolItems in the folder.

        Studio-only. Refer to DaVinci Resolve's "Studio and AI Scripting APIs"
        prerequisites (AI IntelliSearch Faster/Better Extras); returns False if
        requirements are not met.

        Args:
            identify_faces (bool): Whether to identify faces.
            is_better_mode (bool): Whether to use Better mode (else Faster mode).

        Returns:
            bool: Returns True if required packages are installed and analysis is successful.

        Raises:
            APIVersionError: If Resolve version < 21.0.2

        Version:
            Added in DaVinci Resolve 21.0.2
        """
        return self._folder.AnalyzeForIntellisearch(identify_faces, is_better_mode)

    @requires_resolve_version(added_in="21.0.2")
    def analyze_for_slate(self, marker_color: "MarkerColor | str") -> bool:
        """Performs Slate analysis on all MediaPoolItems in the folder using the current settings and specified marker color.

        Studio-only. Refer to DaVinci Resolve's "Studio and AI Scripting APIs"
        prerequisites (AI Slate ID Extras); returns False if requirements are not met.

        Args:
            marker_color (MarkerColor | str): Marker color to use. A ``MarkerColor``
                enum member or the underlying color string.

        Returns:
            bool: Returns True if required packages are installed and analysis is successful.

        Raises:
            APIVersionError: If Resolve version < 21.0.2

        Version:
            Added in DaVinci Resolve 21.0.2
        """
        color = marker_color.value if isinstance(marker_color, Enum) else marker_color
        return self._folder.AnalyzeForSlate(color)
    
    