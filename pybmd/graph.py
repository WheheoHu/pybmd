from enum import Enum
from typing import TYPE_CHECKING, List, Literal

from pybmd._wrapper_base import WrapperBase
from pybmd.decorators import (
    require_resolve_version_for_argument,
    requires_resolve_version,
)

if TYPE_CHECKING:
    from pybmd.settings import KeyframeMode

NodeColor = Literal[
    "Orange", "Apricot", "Yellow", "Lime", "Olive", "Green", "Teal", "Navy",
    "Blue", "Purple", "Violet", "Pink", "Tan", "Beige", "Brown", "Chocolate", "",
]
"""Node colors accepted by ``Graph.set_node_color``. An empty string clears the color."""


class Graph(WrapperBase):
    """docstring for Graph."""

    def __init__(self, graph):
        super(Graph, self).__init__(graph)
        self._graph = self._object

    def get_num_nodes(self) -> int:
        """Returns the number of nodes in the graph

        Returns:
            int: number of nodes in the graph
        """
        return self._graph.GetNumNodes()

    def set_lut(self, node_index: int, lut_path: str) -> bool:
        """Sets LUT on the node mapping the node index provided
        Args:
            node_index (int): 1 <= nodeIndex <= self.GetNumNodes().
            lut_path (str): The lutPath can be an absolute path, or a relative path (based off custom LUT paths or the master LUT path).

        Returns:
            bool: The operation is successful for valid lut paths that Resolve has already discovered (see Project.RefreshLUTList).
        """
        return self._graph.SetLUT(node_index, lut_path)

    def get_lut(self, node_index: str) -> str:
        """Gets relative LUT path based on the node index provided

        Args:
            node_index (str): 1 <= nodeIndex <= total number of nodes.

        Returns:
            str: relative LUT path
        """
        return self._graph.GetLUT(node_index)

    def get_node_label(self, node_index: int) -> str:
        """Returns the label of the node at nodeIndex.

        Args:
            node_index (int):  1 <= nodeIndex <= total number of nodes.

        Returns:
            str: the label of the node at nodeIndex.
        """
        return self._graph.GetNodeLabel(node_index)

    def get_tools_in_node(self, node_index: int) -> List[str]:
        """Returns toolsList (list of strings) of the tools used in the node indicated by given nodeIndex (int).

        Args:
            node_index (int): 1 <= nodeIndex <= total number of nodes.

        Returns:
            List[str]: toolsList (list of strings) of the tools used in the node indicated by given nodeIndex (int).
        """
        return self._graph.GetToolsInNode(node_index)

    def set_node_enabled(self, node_index: int, is_enable: bool) -> bool:
        """Sets the node at the given nodeIndex (int) to isEnabled (bool).

        Args:
            node_index (int): 1 <= nodeIndex <= self.GetNumNodes().
            is_enable (bool): node is enabled or not

        Returns:
            bool: Return True if the operation is successful.
        """
        return self._graph.SetNodeEnabled(node_index, is_enable)

    ##############################################################################################################
    # Add at DR 19.1.0
    @requires_resolve_version(added_in="19.1.0")
    def set_node_cache_mode(self, node_index: int, cache_value: int) -> bool:
        """Sets the cache mode type on the node.

        Args:
            node_index (int): 1 <= nodeIndex <= total number of nodes
            cache_value (int): Cache mode value to set
            cache_value is an enumerated integer with one of the following values:
                - resolve.CACHE_AUTO_ENABLED  = -1
                - resolve.CACHE_DISABLED      =  0
                - resolve.CACHE_ENABLED       =  1

        Returns:
            bool: True if successful, False otherwise

        Raises:
            APIVersionError: If Resolve version < 19.1.0

        Version:
            Added in DaVinci Resolve 19.1.0
        """
        return self._graph.SetNodeCacheMode(node_index, cache_value)

    @requires_resolve_version(added_in="19.1.0")
    def get_node_cache_mode(self, node_index: int) -> int:
        """Gets the cache mode type on the node.

        Args:
            node_index (int): 1 <= nodeIndex <= total number of nodes

        Returns:
            int: Cache mode value of the node.cache_value is an enumerated integer with one of the following values:
                - resolve.CACHE_AUTO_ENABLED  = -1
                - resolve.CACHE_DISABLED      =  0
                - resolve.CACHE_ENABLED       =  1
        """
        return self._graph.GetNodeCacheMode(node_index)

    @requires_resolve_version(added_in="19.1.0")
    def apply_grade_from_drx(
        self,
        path: str,
        grade_mode: int = 0,
        apply_to_all_layers: bool = False,
        keyframe_mode: "KeyframeMode | int | None" = None,
    ) -> bool:
        """Loads a still from given file path and applies grade to graph.

        Applying a grade replaces the graph: after a successful call this Graph object
        no longer refers to a valid graph. Call ``get_node_graph()`` again to keep
        working with the new one.

        Args:
            path (str): File path to the DRX file
            grade_mode (int, optional): 0="No keyframes", 1="Source Timecode aligned",
                2="Start Frames aligned". Defaults to 0.
            apply_to_all_layers (bool, optional): Apply the grade to all node-stack
                layers instead of only the active layer. Needs DR 21.1.1+; only sent
                when True. Defaults to False.
            keyframe_mode (KeyframeMode | int, optional): What to apply: all, color only
                or sizing only. Needs DR 21.1.2+; DaVinci Resolve applies everything
                when omitted. Defaults to None.

        Returns:
            bool: True if successful, False otherwise

        Raises:
            APIVersionError: If Resolve version < 19.1.0, or an argument is used on a
                version that predates it

        Version:
            Added in DaVinci Resolve 19.1.0. ``apply_to_all_layers`` added in 21.1.1,
            ``keyframe_mode`` added in 21.1.2.
        """
        if keyframe_mode is not None:
            require_resolve_version_for_argument(
                "Graph.apply_grade_from_drx", "keyframe_mode", "21.1.2"
            )
            if isinstance(keyframe_mode, Enum):
                keyframe_mode = keyframe_mode.value
            return self._graph.ApplyGradeFromDRX(
                path, grade_mode, apply_to_all_layers, keyframe_mode
            )
        if apply_to_all_layers:
            require_resolve_version_for_argument(
                "Graph.apply_grade_from_drx", "apply_to_all_layers", "21.1.1"
            )
            return self._graph.ApplyGradeFromDRX(path, grade_mode, True)
        return self._graph.ApplyGradeFromDRX(path, grade_mode)

    @requires_resolve_version(added_in="19.1.0")
    def apply_arri_cdl_lut(self) -> bool:
        """Applies ARRI CDL and LUT.

        Returns:
            bool: True if successful, False otherwise
        """
        return self._graph.ApplyArriCdlLut()

    @requires_resolve_version(added_in="19.1.0")
    def reset_all_grades(self) -> bool:
        """Resets all grades in the graph.

        Returns:
            bool: True if all grades were reset successfully, False otherwise
        """
        return self._graph.ResetAllGrades()

    ##############################################################################################################
    # Add at DR 21.1.2

    @requires_resolve_version(added_in="21.1.2")
    def set_node_label(self, node_index: int, label: str) -> bool:
        """Sets the label of the node at node_index.

        Args:
            node_index (int): 1 <= node_index <= get_num_nodes()
            label (str): new node label

        Returns:
            bool: True if successful, False otherwise

        Raises:
            APIVersionError: If Resolve version < 21.1.2

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._graph.SetNodeLabel(node_index, label)

    @requires_resolve_version(added_in="21.1.2")
    def get_node_color(self, node_index: int) -> str:
        """Returns the color of the node at node_index.

        Args:
            node_index (int): 1 <= node_index <= get_num_nodes()

        Returns:
            str: the node color, e.g. "Orange", or an empty string if none is set

        Raises:
            APIVersionError: If Resolve version < 21.1.2

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._graph.GetNodeColor(node_index)

    @requires_resolve_version(added_in="21.1.2")
    def set_node_color(self, node_index: int, color_name: "NodeColor | str") -> bool:
        """Sets the color of the node at node_index.

        Args:
            node_index (int): 1 <= node_index <= get_num_nodes()
            color_name (str): one of the clip colors, e.g. "Orange", "Teal" or
                "Chocolate". An empty string clears the color.

        Returns:
            bool: True if successful, False otherwise

        Raises:
            APIVersionError: If Resolve version < 21.1.2

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._graph.SetNodeColor(node_index, color_name)
