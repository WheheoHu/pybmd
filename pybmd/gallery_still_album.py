from os import path
from typing import List
from pybmd.gallery_still import GalleryStill

from enum import Enum


class StillFormats(Enum):
    """Docstring for StillFormats."""
    DPX = "dpx"
    CIN = "cin"
    TIF = "tif"
    JPG = "jpg"
    PNG = "png"
    PPM = "ppm"
    BMP = "bmp"
    XPM = "xpm"


def get_gallery_still_list_from_class_list(list: List[GalleryStill]):
    return_list = []
    for ele in list:
        return_list.append(ele.gallery_still)
    return return_list


class GalleryStillAlbum():
    """docstring for GalleryStillAlbum."""

    def __init__(self, gallery_still_album):
        self.gallery_still_album = gallery_still_album

    def delete_stills(self, gallery_stills: List[GalleryStill]) -> bool:

        gallery_still_list = get_gallery_still_list_from_class_list(
            gallery_stills)
        return self.gallery_still_album.DeleteStills(gallery_still_list)

    def export_stills(self, gallery_stills: List[GalleryStill], folder_path: str, file_prefix: str, format: StillFormats) -> bool:
        gallery_still_list = get_gallery_still_list_from_class_list(
            gallery_stills)
        return self.gallery_still_album.ExportStills(gallery_still_list, str(folder_path), file_prefix, format.value)

    def get_label(self, gallery_still: GalleryStill) -> str:
        return self.gallery_still_album.GetLabel(gallery_still)

    def get_stills(self) -> List[GalleryStill]:
        gallery_still_list = []
        for gallery_still in self.gallery_still_album.GetStills():
            gallery_still_list.append(GalleryStill(gallery_still))
        return gallery_still_list

    def set_label(self, gallery_still: GalleryStill, label: str) -> bool:
        return self.gallery_still_album.SetLabel(gallery_still, label)

