from typing import List
from pybmd.gallery_still_album import GalleryStillAlbum


class Gallery():
    """docstring for Gallery."""

    def __init__(self, gallery):
        self._gallery = gallery

    def get_album_name(self, gallert_still_album: GalleryStillAlbum) -> str:
        """return the album name of the GalleryStillAlbum object"""
        return self._gallery.GetAlbumName(gallert_still_album)

    def get_current_still_album(self) -> GalleryStillAlbum:
        """return the current GalleryStillAlbum object"""
        return GalleryStillAlbum(self._gallery.GetCurrentStillAlbum())

    def get_gallery_still_albums(self) -> List[GalleryStillAlbum]:
        """return a list of GalleryStillAlbum objects"""
        gallery_still_album_list = []
        for gallery_still_album in self._gallery.GetGalleryStillAlbums():
            gallery_still_album_list.append(
                GalleryStillAlbum(gallery_still_album))
        return gallery_still_album_list

    def set_album_name(self, gallert_still_album: GalleryStillAlbum, album_name: str) -> bool:
        """set the album name of the GalleryStillAlbum object

        Args:
            gallert_still_album (GalleryStillAlbum): gallery still album object
            album_name (str): name of the album

        Returns:
            bool: ture if successful, false otherwise
        """
        return self._gallery.SetAlbumName(gallert_still_album, album_name)

    def set_current_still_album(self, gallery_still_album: GalleryStillAlbum) -> bool:
        """set the current GalleryStillAlbum object

        Args:
            gallery_still_album (GalleryStillAlbum): gallery still album object to set as current

        Returns:
            bool: true if successful, false otherwise
        """        
        return self._gallery.SetCurrentStillAlbum(gallery_still_album)
