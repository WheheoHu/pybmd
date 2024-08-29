from os import path
from typing import List
from pybmd.gallery_still import GalleryStill

from enum import Enum


class StillFormat(Enum):
    """StillFormats"""
    DPX = "dpx"
    CIN = "cin"
    TIF = "tif"
    JPG = "jpg"
    PNG = "png"
    PPM = "ppm"
    BMP = "bmp"
    XPM = "xpm"


class GalleryStillAlbum():
    """docstring for GalleryStillAlbum."""

    def __init__(self, gallery_still_album):
        self._gallery_still_album = gallery_still_album

    def delete_stills(self, gallery_stills: List[GalleryStill]) -> bool:
        """Delete the given gallery stills from the album."""
        gallery_still_list = [still._gallery_still for still in gallery_stills]
        return self._gallery_still_album.DeleteStills(gallery_still_list)

    def export_stills(self, gallery_stills: List[GalleryStill], folder_path: str, file_prefix: str, format: StillFormat) -> bool:
        """Exports list of GalleryStill objects 'galleryStill' to directory 'folderPath', with filename prefix 'filePrefix', using file format 'format' 

        Args:
            gallery_stills (List[GalleryStill]): a list of GalleryStill objects to export
            folder_path (str): folder path to export to
            file_prefix (str): filename prefix for exported files
            format (StillFormats): StillFormat Object to use for export format
        Returns:
            bool: function returns true if export was successful, false otherwise
        """
        gallery_still_list = [still._gallery_still for still in gallery_stills]
        return self._gallery_still_album.ExportStills(gallery_still_list, str(folder_path), file_prefix, format.value)

    def get_label(self, gallery_still: GalleryStill) -> str:
        """Returns label of given gallery still."""
        return self._gallery_still_album.GetLabel(gallery_still._gallery_still)

    def get_stills(self) -> List[GalleryStill]:
        """Returns list of GalleryStill objects in this album."""
        gallery_still_list = []
        for gallery_still in self._gallery_still_album.GetStills():
            gallery_still_list.append(GalleryStill(gallery_still))
        return gallery_still_list

    def set_label(self, gallery_still: GalleryStill, label: str) -> bool:
        """sets label of given gallery still.

        Args:
            gallery_still (GalleryStill): gallery still to set label on
            label (str): label to set on gallery still

        Returns:
            bool: ture if successful, false otherwise
        """        
        return self._gallery_still_album.SetLabel(gallery_still, label)

