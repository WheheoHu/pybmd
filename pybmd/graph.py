
from typing import List


class Graph(object):
    """docstring for Graph."""

    def __init__(self, graph):
        self._graph = graph

    def get_num_nodes(self) -> int:
        """Returns the number of nodes in the graph

        Returns:
            int: number of nodes in the graph
        """
        return self._graph.GetNumNodes() 
    
    def set_lut(self,node_index:int,lut_path:str) -> bool:
        """Sets LUT on the node mapping the node index provided
        Args:
            node_index (int): 1 <= nodeIndex <= self.GetNumNodes().
            lut_path (str): The lutPath can be an absolute path, or a relative path (based off custom LUT paths or the master LUT path).

        Returns:
            bool: The operation is successful for valid lut paths that Resolve has already discovered (see Project.RefreshLUTList).
        """
        return self._graph.SetLUT(node_index,lut_path)
    
    def get_lut(self,node_index:str) -> str:
        """Gets relative LUT path based on the node index provided

        Args:
            node_index (str): 1 <= nodeIndex <= total number of nodes.

        Returns:
            str: relative LUT path
        """
        return self._graph.GetLUT(node_index)
    def get_node_label(self,node_index:int) -> str:
        """Returns the label of the node at nodeIndex.

        Args:
            node_index (int):  1 <= nodeIndex <= total number of nodes.

        Returns:
            str: the label of the node at nodeIndex.
        """
        return self._graph.GetNodeLabel(node_index)
    
    def get_tools_in_node(self,node_index:int) -> List[str]:
        """Returns toolsList (list of strings) of the tools used in the node indicated by given nodeIndex (int).

        Args:
            node_index (int): 1 <= nodeIndex <= total number of nodes.

        Returns:
            List[str]: toolsList (list of strings) of the tools used in the node indicated by given nodeIndex (int).
        """
        return self._graph.GetToolsInNode(node_index)
    
    def set_node_enabled(self,node_index:int,is_enable:bool) -> bool:
        """Sets the node at the given nodeIndex (int) to isEnabled (bool).

        Args:
            node_index (int): 1 <= nodeIndex <= self.GetNumNodes().
            is_enable (bool): node is enabled or not

        Returns:
            bool: Return True if the operation is successful.
        """
        return self._graph.SetNodeEnabled(node_index,is_enable)
    
    ##############################################################################################################
    # Add at DR 19.1.0
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
        """
        return self._graph.SetNodeCacheMode(node_index, cache_value)

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

    def apply_grade_from_drx(self, path: str, grade_mode: int = 0) -> bool:
        """Loads a still from given file path and applies grade to graph.

        Args:
            path (str): File path to the DRX file
            grade_mode (int, optional): 0="No keyframes", 1="Source Timecode aligned", 
                2="Start Frames aligned". Defaults to 0.

        Returns:
            bool: True if successful, False otherwise
        """
        return self._graph.ApplyGradeFromDRX(path, grade_mode)

    def apply_arri_cdl_lut(self) -> bool:
        """Applies ARRI CDL and LUT.

        Returns:
            bool: True if successful, False otherwise
        """
        return self._graph.ApplyArriCdlLut()

    def reset_all_grades(self) -> bool:
        """Resets all grades in the graph.

        Returns:
            bool: True if all grades were reset successfully, False otherwise
        """
        return self._graph.ResetAllGrades()