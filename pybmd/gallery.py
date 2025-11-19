from typing import List, Optional
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

    def set_album_name(self, gallery_still_album: GalleryStillAlbum, album_name: str) -> bool:
        """set the album name of the GalleryStillAlbum object

        Args:
            gallert_still_album (GalleryStillAlbum): gallery still album object
            album_name (str): name of the album

        Returns:
            bool: ture if successful, false otherwise
        """
        return self._gallery.SetAlbumName(gallery_still_album._gallery_still_album, album_name)

    def set_current_still_album(self, gallery_still_album: GalleryStillAlbum) -> bool:
        """set the current GalleryStillAlbum object

        Args:
            gallery_still_album (GalleryStillAlbum): gallery still album object to set as current

        Returns:
            bool: true if successful, false otherwise
        """        
        if gallery_still_album is None:
            return False
        return self._gallery.SetCurrentStillAlbum(gallery_still_album._gallery_still_album)
    ##############################################################################################################
    # Add at DR 19.1.0
    def get_gallery_power_grade_albums(self) -> List[GalleryStillAlbum]:
        """Returns the gallery PowerGrade albums.

        Returns:
            List[GalleryStillAlbum]: List of gallery PowerGrade album objects
        """
        power_grade_albums = []
        for album in self._gallery.GetGalleryPowerGradeAlbums():
            power_grade_albums.append(GalleryStillAlbum(album))
        return power_grade_albums

    def create_gallery_still_album(self) -> Optional[GalleryStillAlbum]:
        """Creates a new Still album.

        Returns:
            Optional[GalleryStillAlbum]: New gallery still album object if successful, None otherwise
        """
        album = self._gallery.CreateGalleryStillAlbum()
        return GalleryStillAlbum(album) if album else None

    def create_gallery_power_grade_album(self) -> Optional[GalleryStillAlbum]:
        """Creates a new PowerGrade album.

        Returns:
            Optional[GalleryStillAlbum]: New gallery PowerGrade album object if successful, None otherwise
        """
        album = self._gallery.CreateGalleryPowerGradeAlbum()
        return GalleryStillAlbum(album) if album else None
