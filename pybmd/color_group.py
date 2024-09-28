from typing import List,TYPE_CHECKING

from pybmd.graph import Graph
if TYPE_CHECKING:
    from pybmd.timeline import Timeline
    from pybmd.timeline_item import TimelineItem


class ColorGroup(object):
    """docstring for ColorGroup."""

    def __init__(self, color_group):
        super(ColorGroup, self).__init__()
        self._color_group = color_group

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

    def get_clips_in_timeline(self, timeline: 'Timeline') -> List['TimelineItem']:
        """Returns a list of TimelineItem that are in colorGroup in the given Timeline. 

        Args:
            timeline (Timeline): Timeline is Current Timeline by default.

        Returns:
            List[TimelineItem]: a list of TimelineItem that are in colorGroup in the given Timeline.
        """
        return self._color_group.GetClipsInTimeline(timeline._timeline)

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
