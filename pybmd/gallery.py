from typing import List
from pybmd.gallery_still_album import GalleryStillAlbum


class Gallery():
    """docstring for Gallery."""

    def __init__(self, gallery):
        self.gallery = gallery

    def get_album_name(self, gallert_still_album: GalleryStillAlbum) -> str:
        return self.gallery.GetAlbumName(gallert_still_album)

    def get_current_still_album(self) -> GalleryStillAlbum:
        return GalleryStillAlbum(self.gallery.GetCurrentStillAlbum())

    def get_gallery_still_albums(self) -> List[GalleryStillAlbum]:
        gallery_still_album_list = []
        for gallery_still_album in self.gallery.GetGalleryStillAlbums():
            gallery_still_album_list.append(
                GalleryStillAlbum(gallery_still_album))
        return gallery_still_album_list

    def set_album_name(self, gallert_still_album: GalleryStillAlbum, album_name: str) -> bool:
        return self.gallery.SetAlbumName(gallert_still_album, album_name)

    def set_current_still_album(self, gallery_still_album: GalleryStillAlbum) -> bool:
        return self.gallery.SetCurrentStillAlbum(gallery_still_album)
