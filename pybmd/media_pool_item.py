from multimethod import multimethod


class MediaPoolItem():
    """docstring for MediaPoolItem."""

    def __init__(self, media_pool_item):
        self._media_pool_item = media_pool_item

    def __repr__(self) -> str:
        return f'Media Pool Item:{self.get_name()}'

    def add_flag(self, color: str) -> bool:
        """Add a flag to the clip."""
        return self._media_pool_item.AddFlag(color)

    def add_marker(self, frame_id: int, color: str, name: str, note: str, duration: int, custom_data: str) -> bool:
        """add a marker to the clip.

        Args:
            frame_id (int): postion of the marker
            color (str): color of the marker
            name (str): name of the marker
            note (str): maker note
            duration (int): maker duration
            custom_data (str): optional data help to attach to the marker


        Returns:
            bool: true if success, false if fail
        """
        return self._media_pool_item.AddMarker(frame_id, color, name, note, duration, custom_data)

    def clear_clip_color(self) -> bool:
        """clear clip color.

        :return: bool
        """
        return self._media_pool_item.ClearClipColor()

    def clear_flag_color(self, color: str) -> bool:
        """Clears the flag of the given color if one exists. An "All" argument is supported and clears all flags.

        :param color: color of the flag to clear
        :type color: str
        :return: true if success, false if fail
        :rtype: bool
        """
        return self._media_pool_item.ClearFlagColor(color)

    def delete_marker_at_frame(self, frame_num: int) -> bool:
        """Delete marker at frame number from the media pool item.

        :param frame_num: frame number of the marker to delete
        :type frame_num: int
        :return: true if success, false if fail
        :rtype: bool
        """
        return self._media_pool_item.DeleteMarkerAtFrame(frame_num)

    def delete_marker_by_custom_data(self, custom_data: str) -> bool:
        """Delete first matching marker with specified customData.

        Args:
            custom_data (str): custom data

        Returns:
            bool: true if success, false if fail
        """
        return self._media_pool_item.DeleteMarkerByCustomData(custom_data)

    def delete_marker_by_color(self, color: str) -> bool:
        """delete all markers with the given color.

        Args:
            color (str): color of the marker to delete

        Returns:
            bool: true if success, false if fail
        """
        return self._media_pool_item.DeleteMarkerByColor(color)

    def get_clip_color(self) -> str:
        """get clip color.

        Returns:
            str: color name
        """
        return self._media_pool_item.GetClipColor()

    # TODO property_name as data class
    def get_clip_property(self, property_name: str = "") -> str:
        """return clip property based on the property name.

        Args:
            property_name (str, optional): clip property . Defaults to "".

        Returns:
            str: property value,if property is empty, return a dict of all clip properties.
        """
        return self._media_pool_item.GetClipProperty(property_name)

    def get_flag_list(self) -> list:
        """get flag list.

        Returns:
            list: flag colors assigned to the item.
        """
        return self._media_pool_item.GetFlagList()

    def get_marker_by_custom_data(self, custom_data: str) -> dict:
        """return maker infomation of fist marker matching the custom data.

        Args:
            custom_data (str): specific custom data

        Returns:
            dict: maker info
        """
        return self._media_pool_item.GetMarkerByCustomData(custom_data)

    def get_marker_custom_data(self, freamid: int) -> str:
        """return marker custom data.

        Args:
            freamid (int): frame id of the marker

        Returns:
            str: custom data of the marker
        """
        return self._media_pool_item.GetMarkerCustomData(freamid)

    def get_markers(self) -> dict:
        """return a dict of all markers and dict of marker info.

        Returns:
            dict: maker position and info
        """
        return self._media_pool_item.GetMarkers()

    def get_media_id(self) -> str:
        """return media id for the clip."""
        return self._media_pool_item.GetMediaId()

    # TODO metadata_type as data class
    def get_metadata(self, metadata_type: str = "") -> str:
        """return metadata value of the key metadata_type.

        Args:
            metadata_type (str, optional): metadata type. Defaults to "".

        Returns:
            str: metadata value If no argument is specified, a dict of all set metadata properties is returned.
        """
        return self._media_pool_item.GetMetadata(metadata_type)

    def get_name(self) -> str:
        """return name of the clip."""
        return self._media_pool_item.GetName()

    def link_proxy_media(self, proxy_media_file_path: str) -> bool:
        """Links proxy media located at path specified by arg 'proxyMediaFilePath' with the current clip. 

        Args:
            proxy_media_file_path (str): should be absolute clip path.

        Returns:
            bool: true if success, false if fail
        """
        return self._media_pool_item.LinkProxyMedia(str(proxy_media_file_path))

    def replace_clip(self, file_path: str) -> bool:
        """Replaces the underlying asset and metadata of MediaPoolItem with the specified absolute clip path."""
        return self._media_pool_item.ReplaceClip(str(file_path))

    def set_clip_color(self, color_name: str) -> bool:
        """set clip color with the given color name.

        Args:
            color_name (str): color name

        Returns:
            bool: true if success, false if fail
        """
        return self._media_pool_item.SetClipColor(color_name)

    def set_clip_property(self, property_type: str, property_value: str) -> bool:
        """set clip property with the given property type and value.

        Args:
            property_type (str): property type
            property_value (str): property value

        Returns:
            bool: true if success, false if fail
        """
        return self._media_pool_item.SetClipProperty(property_type, property_value)

    # TODO metadata_type as data class
    def set_metadata(self, metadata_type: str, metadata_value: str) -> bool:
        """set metadata with the given metadata type and value.

        Args:
            metadata_type (str): metadata type
            metadata_value (str): metadata value

        Returns:
            bool: true if success, false if fail
        """
        return self._media_pool_item.SetMetadata(metadata_type, metadata_value)

    def unlink_proxy_media(self) -> bool:
        """Unlinks proxy media from the current clip."""
        return self._media_pool_item.UnlinkProxyMedia()

    def updata_marker_custom_data(self, frame_id: int, custom_data: str) -> bool:
        """update marker custom data.

        Args:
            frame_id (int): maker frame id
            custom_data (str): maker custom data

        Returns:
            bool: true if success, false if fail
        """
        return self._media_pool_item.UpdataMarkerCustomData(frame_id, custom_data)

    ###############################################################################
    # Add at DR18.0.0

    # TODO Add version check
    def get_unique_id(self) -> str:
        """return unique id of the clip."""
        return self._media_pool_item.GetUniqueId()

    ##############################################################################################################################
    # Add at DR18.5.0

    def transcribe_audio(self) -> bool:
        """Transcribes audio of the MediaPoolItem. 

        Returns:
            bool: Returns True if successful; False otherwise
        """
        return self._media_pool_item.TranscribeAudio()

    def clear_transcription(self) -> bool:
        """Clears audio transcription of the MediaPoolItem. 

        Returns:
            bool: Returns True if successful; False otherwise.
        """
        return self._media_pool_item.ClearTranscription()

    ##############################################################################################################################
    # Add at DR 19.0.0

    def get_audio_mapping(self) -> str:
        """Returns a string with MediaPoolItem's audio mapping information. Check 'Audio Mapping' section for more information.

        Returns:
            str: json formatted string
        """
        return self._media_pool_item.GetAudioMapping()

    ##############################################################################################################################
    # Add at DR 19.0.2

    def get_third_party_metadata(self, metadata_type: str = None) -> str | dict:
        """Returns the third party metadata value for the key 'metadataType'.

        Args:
            metadata_type (str, optional): If no argument is specified, a dict of all set third parth metadata properties is returned. Defaults to None.

        Returns:
            str | dict: third party metadata value
        """
        return self._media_pool_item.GetThirdPartyMetadata(metadata_type)

    @multimethod
    def set_third_party_metadata(self, metadata_type: str, metadata_value: str) -> bool:
        """Sets/Add the given third party metadata to metadata_value (string). 

        Args:
            metadata_type (str): metadata type
            metadata_value (str): metadata value

        Returns:
            bool: Returns True if successful.
        """
        return self._media_pool_item.SetThirdPartyMetadata(metadata_type, metadata_value)
    
    @multimethod
    def set_third_party_metadata(self, metadata_dict: dict) -> bool:
        """Sets/Add the given third party metadata to metadata_value (string). 
        
        Args:
            metadata_dict (dict): metadata dict 
        
        Returns:
            bool: Returns True if successful.
        """
        return self._media_pool_item.SetThirdPartyMetadata(metadata_dict)
    
    