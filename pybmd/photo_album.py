from typing import List, Optional

from pybmd._wrapper_base import WrapperBase
from pybmd.decorators import requires_resolve_version
from pybmd.gallery_still import GalleryStill
from pybmd.graph import Graph
from pybmd.media_pool_item import MediaPoolItem
from pybmd.photo_album_item import PhotoAlbumItem


class PhotoAlbum(WrapperBase):
    """A photo album: an ordered set of photos graded together.

    The photo counterpart of :class:`~pybmd.timeline.Timeline`. Photo albums are
    enumerated through ``Project.get_photo_album_count`` / ``get_photo_album_by_index``
    and created through ``MediaPool.create_empty_photo_album`` /
    ``create_photo_album_from_photos``.

    Version:
        Added in DaVinci Resolve 21.1.2
    """

    def __init__(self, photo_album):
        super(PhotoAlbum, self).__init__(photo_album)
        self._photo_album = self._object

    def __repr__(self) -> str:
        return f"Photo Album: {self._photo_album.GetName()}"

    ##############################################################################################################################
    # Add at DR 21.1.2

    @requires_resolve_version(added_in="21.1.2")
    def get_name(self) -> str:
        """Returns the photo album name.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album.GetName()

    @requires_resolve_version(added_in="21.1.2")
    def set_name(self, photo_album_name: str) -> bool:
        """Renames the photo album. The name must be unique.

        Args:
            photo_album_name (str): new name

        Returns:
            bool: True if successful, False otherwise

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album.SetName(photo_album_name)

    @requires_resolve_version(added_in="21.1.2")
    def get_unique_id(self) -> str:
        """Returns a unique ID for the photo album.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album.GetUniqueId()

    @requires_resolve_version(added_in="21.1.2")
    def get_photo_list(self) -> List[PhotoAlbumItem]:
        """Returns the photos in the photo album.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return [PhotoAlbumItem(item) for item in self._photo_album.GetPhotoList() or []]

    @requires_resolve_version(added_in="21.1.2")
    def get_current_item(self) -> Optional[PhotoAlbumItem]:
        """Returns the current photo of the photo album.

        Returns:
            PhotoAlbumItem | None: the current photo, None if there is none

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        item = self._photo_album.GetCurrentItem()
        if item is None:
            return None
        return PhotoAlbumItem(item)

    @requires_resolve_version(added_in="21.1.2")
    def delete_photos(self, photo_album_items: List[PhotoAlbumItem]) -> bool:
        """Deletes the given photos from the photo album.

        Args:
            photo_album_items (List[PhotoAlbumItem]): photos to delete

        Returns:
            bool: True if successful, False otherwise

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album.DeletePhotos(
            [item._photo_album_item for item in photo_album_items]
        )

    @requires_resolve_version(added_in="21.1.2")
    def get_node_graph(self) -> Graph:
        """Returns the photo album's node graph.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return Graph(self._photo_album.GetNodeGraph())

    @requires_resolve_version(added_in="21.1.2")
    def get_media_pool_item(self) -> Optional[MediaPoolItem]:
        """Returns the media pool item of the photo album.

        Returns:
            MediaPoolItem | None: the media pool item, None if there is none

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        media_pool_item = self._photo_album.GetMediaPoolItem()
        if media_pool_item is None:
            return None
        return MediaPoolItem(media_pool_item)

    @requires_resolve_version(added_in="21.1.2")
    def grab_still(self) -> GalleryStill:
        """Grabs a still from the current photo.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return GalleryStill(self._photo_album.GrabStill())

    @requires_resolve_version(added_in="21.1.2")
    def grab_all_stills(self) -> List[GalleryStill]:
        """Grabs a still from every photo in the photo album.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return [GalleryStill(still) for still in self._photo_album.GrabAllStills() or []]
