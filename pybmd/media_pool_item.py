


class MediaPoolItem():
    """docstring for MediaPoolItem."""

    def __init__(self, media_pool_item):
        self.media_pool_item = media_pool_item

    def add_flag(self, color: str) -> bool:
        """Add a flag to the clip."""
        return self.media_pool_item.AddFlag(color)

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
        return self.media_pool_item.AddMarker(frame_id, color, name, note, duration, custom_data)

    def clear_clip_color(self) -> bool:
        """clear clip color.

        :return: bool
        """        
        return self.media_pool_item.ClearClipColor()

    def clear_flag_color(self, color: str) -> bool:
        """Clears the flag of the given color if one exists. An "All" argument is supported and clears all flags.

        :param color: color of the flag to clear
        :type color: str
        :return: true if success, false if fail
        :rtype: bool
        """       
        return self.media_pool_item.ClearFlagColor(color)

    def delete_marker_at_frame(self, frame_num: int) -> bool:
        """Delete marker at frame number from the media pool item.

        :param frame_num: frame number of the marker to delete
        :type frame_num: int
        :return: true if success, false if fail
        :rtype: bool
        """
        return self.media_pool_item.DeleteMarkerAtFrame(frame_num)

    def delete_marker_by_custom_data(self, custom_data: str) -> bool:
        """Delete first matching marker with specified customData.

        Args:
            custom_data (str): custom data

        Returns:
            bool: true if success, false if fail
        """
        return self.media_pool_item.DeleteMarkerByCustomData(custom_data)

    def delete_marker_by_color(self, color: str) -> bool:
        """delete all markers with the given color.

        Args:
            color (str): color of the marker to delete

        Returns:
            bool: true if success, false if fail
        """
        return self.media_pool_item.DeleteMarkerByColor(color)

    def get_clip_color(self) -> str:
        """get clip color.

        Returns:
            str: color name
        """
        return self.media_pool_item.GetClipColor()

    # property_name as data class
    def get_clip_property(self, property_name: str = "") -> str:
        return self.media_pool_item.GetClipProperty(property_name)

    def get_flag_list(self) -> list:
        return self.media_pool_item.GetFlagList()

    def get_marker_by_custom_data(self, custom_data: str) -> dict:
        return self.media_pool_item.GetMarkerByCustomData(custom_data)

    def get_marker_custom_data(self, freamid: int) -> str:
        return self.media_pool_item.GetMarkerCustomData(freamid)

    def get_markers(self) -> dict:
        return self.media_pool_item.GetMarkers()

    def get_media_id(self) -> str:
        return self.media_pool_item.GetMediaId()

    # TODO metadata_type as data class
    def get_metadata(self, metadata_type: str = "") -> str:
        return self.media_pool_item.GetMetadata(metadata_type)

    def get_name(self) -> str:
        return self.media_pool_item.GetName()

    def link_proxy_media(self, proxy_media_file_path: str) -> bool:  
        # 'proxy_media_file_path' should be absolute clip path.
        return self.media_pool_item.LinkProxyMedia(str(proxy_media_file_path))

    def replace_clip(self, file_path: str) -> bool:
        return self.media_pool_item.ReplaceClip(str(file_path))

    def set_clip_color(self, color_name: str) -> bool:
        return self.media_pool_item.SetClipColor(color_name)

    
    def set_clip_property(self, property_type: str, property_value: str) -> bool:
        return self.media_pool_item.SetClipProperty(property_type, property_value)
    
    # TODO metadata_type as data class
    def set_metadata(self, metadata_type: str, metadata_value: str) -> bool:
        return self.media_pool_item.SetMetadata(metadata_type, metadata_value)

    def unlink_proxy_media(self) -> bool:
        return self.media_pool_item.UnlinkProxyMedia()

    def updata_marker_custom_data(self, frame_id:int, custom_data:str) -> bool:
        return self.media_pool_item.UpdataMarkerCustomData(frame_id, custom_data)
    
    ###############################################################################
    #Add at DR18.0.0
    
    def get_unique_id(self) -> str:
        return self.media_pool_item.GetUniqueId()
    
    ################################################################################