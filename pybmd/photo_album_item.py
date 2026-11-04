from dataclasses import asdict
from typing import TYPE_CHECKING, Dict, List, Optional

from pybmd._wrapper_base import WrapperBase
from pybmd.color_group import ColorGroup
from pybmd.decorators import requires_resolve_version
from pybmd.effect import Effect
from pybmd.fusion_comp import FusionComp
from pybmd.graph import Graph
from pybmd.media_pool_item import MediaPoolItem

if TYPE_CHECKING:
    from pybmd.export_type import LUT_Export_Type
    from pybmd.settings import (
        ExportFrameOptions,
        ExportFrameResult,
        PhotoAlbumItemProperties,
    )
    from pybmd.timeline_item import CDL_Map


class PhotoAlbumItem(WrapperBase):
    """A photo in a photo album, with its color grades, flags and Fusion compositions.

    The photo album counterpart of :class:`~pybmd.timeline_item.TimelineItem`.
    Photo albums only support remote color versions, so the version methods take no
    version type.

    Version:
        Added in DaVinci Resolve 21.1.2
    """

    def __init__(self, photo_album_item):
        super(PhotoAlbumItem, self).__init__(photo_album_item)
        self._photo_album_item = self._object

    def __repr__(self) -> str:
        return f"Photo Album Item: {self._photo_album_item.GetName()}"

    ##############################################################################################################################
    # Add at DR 21.1.2

    # --- Name and identity ---

    @requires_resolve_version(added_in="21.1.2")
    def get_name(self) -> str:
        """Returns the item name.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.GetName()

    @requires_resolve_version(added_in="21.1.2")
    def set_name(self, name: str) -> bool:
        """Sets the item name.

        Args:
            name (str): new name

        Returns:
            bool: True if successful, False otherwise

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.SetName(name)

    @requires_resolve_version(added_in="21.1.2")
    def get_unique_id(self) -> str:
        """Returns a unique ID for the photo album item.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.GetUniqueId()

    @requires_resolve_version(added_in="21.1.2")
    def get_media_pool_item(self) -> Optional[MediaPoolItem]:
        """Returns the media pool item of the photo, if one exists.

        Returns:
            MediaPoolItem | None: the media pool item, None if there is none

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        media_pool_item = self._photo_album_item.GetMediaPoolItem()
        if media_pool_item is None:
            return None
        return MediaPoolItem(media_pool_item)

    # --- Fusion compositions ---

    @requires_resolve_version(added_in="21.1.2")
    def get_fusion_comp_count(self) -> int:
        """Returns the number of Fusion compositions of the item.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.GetFusionCompCount()

    @requires_resolve_version(added_in="21.1.2")
    def get_fusion_comp_name_list(self) -> List[str]:
        """Returns the names of the item's Fusion compositions.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.GetFusionCompNameList()

    @requires_resolve_version(added_in="21.1.2")
    def get_fusion_comp_by_index(self, comp_index: int) -> Optional[FusionComp]:
        """Returns the Fusion composition at the given index.

        Args:
            comp_index (int): 1 <= comp_index <= get_fusion_comp_count()

        Returns:
            FusionComp | None: the Fusion composition, None if there is none

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        fusion_comp = self._photo_album_item.GetFusionCompByIndex(comp_index)
        if fusion_comp is None:
            return None
        return FusionComp(fusion_comp)

    @requires_resolve_version(added_in="21.1.2")
    def get_fusion_comp_by_name(self, comp_name: str) -> Optional[FusionComp]:
        """Returns the Fusion composition with the given name.

        Args:
            comp_name (str): composition name

        Returns:
            FusionComp | None: the Fusion composition, None if there is none

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        fusion_comp = self._photo_album_item.GetFusionCompByName(comp_name)
        if fusion_comp is None:
            return None
        return FusionComp(fusion_comp)

    @requires_resolve_version(added_in="21.1.2")
    def add_fusion_comp(self) -> FusionComp:
        """Adds a new Fusion composition to the item.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return FusionComp(self._photo_album_item.AddFusionComp())

    @requires_resolve_version(added_in="21.1.2")
    def delete_fusion_comp_by_name(self, comp_name: str) -> bool:
        """Deletes the named Fusion composition.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.DeleteFusionCompByName(comp_name)

    @requires_resolve_version(added_in="21.1.2")
    def load_fusion_comp_by_name(self, comp_name: str) -> FusionComp:
        """Loads the named Fusion composition as the active composition.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return FusionComp(self._photo_album_item.LoadFusionCompByName(comp_name))

    @requires_resolve_version(added_in="21.1.2")
    def rename_fusion_comp_by_name(self, old_name: str, new_name: str) -> bool:
        """Renames the Fusion composition named old_name.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.RenameFusionCompByName(old_name, new_name)

    @requires_resolve_version(added_in="21.1.2")
    def import_fusion_comp(self, path: str) -> FusionComp:
        """Imports a Fusion composition from the given file path as a new composition
        of the item.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return FusionComp(self._photo_album_item.ImportFusionComp(str(path)))

    @requires_resolve_version(added_in="21.1.2")
    def export_fusion_comp(self, path: str, comp_index: int) -> bool:
        """Exports the Fusion composition at comp_index to the given path.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.ExportFusionComp(str(path), comp_index)

    # --- Flags, color and ratings ---

    @requires_resolve_version(added_in="21.1.2")
    def add_flag(self, color: str) -> bool:
        """Adds a flag with the given color, e.g. "Blue".

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.AddFlag(color)

    @requires_resolve_version(added_in="21.1.2")
    def get_flag_list(self) -> List[str]:
        """Returns the flag colors assigned to the item.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.GetFlagList()

    @requires_resolve_version(added_in="21.1.2")
    def clear_flags(self, color: str = "All") -> bool:
        """Clears the flags of the given color. "All" clears every flag.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.ClearFlags(color)

    @requires_resolve_version(added_in="21.1.2")
    def get_clip_color(self) -> str:
        """Returns the item color, an empty string if none is set.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.GetClipColor()

    @requires_resolve_version(added_in="21.1.2")
    def set_clip_color(self, color_name: str) -> bool:
        """Sets the item color, e.g. "Orange".

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.SetClipColor(color_name)

    @requires_resolve_version(added_in="21.1.2")
    def clear_clip_color(self) -> bool:
        """Clears the item color.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.ClearClipColor()

    @requires_resolve_version(added_in="21.1.2")
    def get_ratings(self) -> int:
        """Returns the photo rating in stars, 0 to 5.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.GetRatings()

    @requires_resolve_version(added_in="21.1.2")
    def set_ratings(self, stars: int) -> bool:
        """Sets the photo rating in stars, 0 to 5.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.SetRatings(stars)

    # --- Color grading ---

    @requires_resolve_version(added_in="21.1.2")
    def copy_grades(self, target_photo_album_items: List["PhotoAlbumItem"]) -> bool:
        """Copies the current node stack layer grade to the same layer of each target
        item.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.CopyGrades(
            [item._photo_album_item for item in target_photo_album_items]
        )

    @requires_resolve_version(added_in="21.1.2")
    def get_current_version(self) -> Dict:
        """Returns the current color version, ``{"versionName": str, "versionType": 1}``.
        Photo albums only support remote versions.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.GetCurrentVersion()

    @requires_resolve_version(added_in="21.1.2")
    def add_version(self, version_name: str) -> bool:
        """Adds a new (remote) color version.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.AddVersion(version_name)

    @requires_resolve_version(added_in="21.1.2")
    def get_version_name_list(self) -> List[str]:
        """Returns the names of all (remote) color versions.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.GetVersionNameList()

    @requires_resolve_version(added_in="21.1.2")
    def load_version_by_name(self, version_name: str) -> bool:
        """Loads the named color version as the active version.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.LoadVersionByName(version_name)

    @requires_resolve_version(added_in="21.1.2")
    def rename_version_by_name(self, old_name: str, new_name: str) -> bool:
        """Renames the color version named old_name.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.RenameVersionByName(old_name, new_name)

    @requires_resolve_version(added_in="21.1.2")
    def delete_version_by_name(self, version_name: str) -> bool:
        """Deletes the named color version.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.DeleteVersionByName(version_name)

    @requires_resolve_version(added_in="21.1.2")
    def set_cdl(self, cdl_map: "CDL_Map | dict") -> bool:
        """Sets CDL values on a node.

        Args:
            cdl_map (CDL_Map | dict): ``NodeIndex``, ``Slope``, ``Offset``, ``Power`` and
                ``Saturation``

        Returns:
            bool: True if successful, False otherwise

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        cdl_dict = cdl_map if isinstance(cdl_map, dict) else asdict(cdl_map)
        return self._photo_album_item.SetCDL(cdl_dict)

    @requires_resolve_version(added_in="21.1.2")
    def get_node_graph(self, layer_index: Optional[int] = None) -> Graph:
        """Returns the photo's node graph.

        Args:
            layer_index (int, optional): 1 <= layer_index <= the project's
                "nodeStackLayers" setting. Returns the first layer when omitted.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        if layer_index is None:
            return Graph(self._photo_album_item.GetNodeGraph())
        return Graph(self._photo_album_item.GetNodeGraph(layer_index))

    @requires_resolve_version(added_in="21.1.2")
    def reset_all_node_colors(self) -> bool:
        """Resets the color of every node in the active version of the photo.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.ResetAllNodeColors()

    @requires_resolve_version(added_in="21.1.2")
    def export_lut(self, export_type: "LUT_Export_Type", path: str) -> bool:
        """Exports a LUT of the size given by export_type to the given path.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.ExportLUT(export_type.value, str(path))

    @requires_resolve_version(added_in="21.1.2")
    def get_color_group(self) -> Optional[ColorGroup]:
        """Returns the photo's color group, None if it is in none.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        color_group = self._photo_album_item.GetColorGroup()
        if color_group is None:
            return None
        return ColorGroup(color_group)

    @requires_resolve_version(added_in="21.1.2")
    def assign_to_color_group(self, color_group: ColorGroup) -> bool:
        """Assigns the photo to the given color group of the current project.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.AssignToColorGroup(color_group._object)

    @requires_resolve_version(added_in="21.1.2")
    def remove_from_color_group(self) -> bool:
        """Removes the photo from its color group.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.RemoveFromColorGroup()

    @requires_resolve_version(added_in="21.1.2")
    def load_burn_in_preset(self, preset_name: str) -> bool:
        """Loads the named user data burn-in preset for the photo.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.LoadBurnInPreset(preset_name)

    # --- Effects ---

    @requires_resolve_version(added_in="21.1.2")
    def add_effect(self, category: str, effect_id: str) -> Optional[Effect]:
        """Applies an effect to the photo.

        Args:
            category (str): "fusion" or "ofx"
            effect_id (str): effect id, see ``Resolve.get_effects_list("photo")``

        Returns:
            Effect | None: the applied effect, None on failure

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        effect = self._photo_album_item.AddEffect(category, effect_id)
        if effect is None:
            return None
        return Effect(effect)

    @requires_resolve_version(added_in="21.1.2")
    def get_effects(self, category: str) -> List[Effect]:
        """Returns the effects of the given category ("fusion" or "ofx") applied to
        the photo.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return [Effect(effect) for effect in self._photo_album_item.GetEffects(category) or []]

    @requires_resolve_version(added_in="21.1.2")
    def delete_effects(self, effects: List[Effect]) -> bool:
        """Removes the given effects from the photo.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.DeleteEffects([effect._effect for effect in effects])

    # --- Export and properties ---

    @requires_resolve_version(added_in="21.1.2")
    def export_frame(
        self, export_frame_options: "ExportFrameOptions | dict | None" = None
    ) -> "ExportFrameResult | dict":
        """Exports the photo as a still image.

        Args:
            export_frame_options (ExportFrameOptions | dict, optional): output options.
                Returns a base64 encoded JPEG when omitted. Defaults to None.

        Returns:
            ExportFrameResult | dict: the export result, an empty dict if nothing was
                returned. Use ``ExportFrameResult.decode_data()`` for the image bytes.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        from pybmd.settings import ExportFrameResult

        if export_frame_options is None:
            result = self._photo_album_item.ExportFrame()
        else:
            if not isinstance(export_frame_options, dict):
                export_frame_options = export_frame_options.model_dump(exclude_none=True)
            result = self._photo_album_item.ExportFrame(export_frame_options)
        if not result:
            return {}
        return ExportFrameResult(**result)

    @requires_resolve_version(added_in="21.1.2")
    def get_properties(self) -> Dict:
        """Returns all photo properties (source transform, cropping and looks).

        Refer to ``settings.PhotoAlbumItemProperties`` for the keys.

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._photo_album_item.GetProperties()

    @requires_resolve_version(added_in="21.1.2")
    def set_properties(self, properties: "PhotoAlbumItemProperties | dict") -> bool:
        """Sets photo properties (source transform, cropping and looks).

        DaVinci Resolve validates every key and value first, so either all properties
        are set or none is.

        Args:
            properties (PhotoAlbumItemProperties | dict): properties to set

        Returns:
            bool: True if successful, False otherwise

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        if not isinstance(properties, dict):
            properties = properties.model_dump(exclude_none=True)
        return self._photo_album_item.SetProperties(properties)
