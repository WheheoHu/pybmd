


class MediaPoolItem():
    """docstring for MediaPoolItem."""

    def __init__(self, media_pool_item):
        self.media_pool_item = media_pool_item

    def add_flag(self, color: str) -> bool:
        return self.media_pool_item.AddFlag(color)

    def add_marker(self, frame_id: int, color: str, name: str, note: str, duration: int, custom_data: str) -> bool:
        return self.media_pool_item.AddMarker(frame_id, color, name, note, duration, custom_data)

    def clear_clip_color(self) -> bool:
        return self.media_pool_item.ClearClipColor()

    def clear_flag_color(self, color: str) -> bool:
        return self.media_pool_item.ClearFlagColor(color)

    def delete_marker_at_frame(self, frame_num: int) -> bool:
        return self.media_pool_item.DeleteMarkerAtFrame(frame_num)

    def delete_marker_by_custom_data(self, custom_data: str) -> bool:
        return self.media_pool_item.DeleteMarkerByCustomData(custom_data)

    def delete_marker_by_color(self, color: str) -> bool:
        return self.media_pool_item.DeleteMarkerByColor(color)

    def get_clip_color(self) -> str:
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
