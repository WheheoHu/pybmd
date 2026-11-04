from typing import List, Optional, TYPE_CHECKING
from pybmd._wrapper_base import WrapperBase
from pybmd.decorators import requires_resolve_version
from pybmd.graph import Graph

if TYPE_CHECKING:
    from pybmd.photo_album import PhotoAlbum
    from pybmd.photo_album_item import PhotoAlbumItem
    from pybmd.timeline import Timeline
    from pybmd.timeline_item import TimelineItem


class ColorGroup(WrapperBase):
    """docstring for ColorGroup."""

    def __init__(self, color_group):
        super(ColorGroup, self).__init__(color_group)
        self._color_group = self._object

    def get_name(self) -> str:
        """Returns the name (string) of the ColorGroup.

        Returns:
            str: name of the ColorGroup.
        """
        return self._color_group.GetName()

    def set_name(self, group_name: str) -> bool:
        """Renames ColorGroup to groupName (string).

        Args:
            group_name (str): color group name

        Returns:
            bool: Returns True if successful, False otherwise.
        """
        return self._color_group.SetName(group_name)

    def get_clips_in_timeline(self, timeline: "Timeline") -> List["TimelineItem"]:
        """Returns a list of TimelineItem that are in colorGroup in the given Timeline.

        Args:
            timeline (Timeline): Timeline is Current Timeline by default.

        Returns:
            List[TimelineItem]: a list of TimelineItem that are in colorGroup in the given Timeline.
        """
        # Imported here: timeline_item imports color_group, so a module-level import
        # would be circular. It used to be imported for type checking only, which made
        # this method raise NameError.
        from pybmd.timeline_item import TimelineItem

        timeline_item_list = [
            TimelineItem(ti_item)
            for ti_item in self._color_group.GetClipsInTimeline(timeline._timeline)
        ]
        return timeline_item_list

    def get_pre_clip_node_graph(self) -> Graph:
        """Returns the ColorGroup Pre-clip graph.

        Returns:
            Graph: ColorGroup Pre-clip graph
        """
        return Graph(self._color_group.GetPreClipNodeGraph())

    def get_post_clip_node_graph(self) -> Graph:
        """Returns the ColorGroup Post-clip graph.

        Returns:
            Graph: ColorGroup Post-clip graph
        """
        return Graph(self._color_group.GetPostClipNodeGraph())

    ##############################################################################################################
    # Add at DR 21.1.2

    @requires_resolve_version(added_in="21.1.2")
    def get_photos_in_photo_album(
        self, photo_album: Optional["PhotoAlbum"] = None
    ) -> List["PhotoAlbumItem"]:
        """Returns the photos of the given photo album that are in this ColorGroup.

        Args:
            photo_album (PhotoAlbum, optional): photo album to look in. Uses the current
                photo album when omitted. Defaults to None.

        Returns:
            List[PhotoAlbumItem]: photos in this ColorGroup

        Raises:
            APIVersionError: If Resolve version < 21.1.2

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        from pybmd.photo_album_item import PhotoAlbumItem

        if photo_album is None:
            photos = self._color_group.GetPhotosInPhotoAlbum()
        else:
            photos = self._color_group.GetPhotosInPhotoAlbum(photo_album._photo_album)
        return [PhotoAlbumItem(photo) for photo in photos or []]
