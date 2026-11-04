from typing import TYPE_CHECKING, Optional

from pybmd._wrapper_base import WrapperBase
from pybmd.decorators import requires_resolve_version
from pybmd.fusion_comp import FusionComp

if TYPE_CHECKING:
    from pybmd.settings import EffectInfo


class Effect(WrapperBase):
    """A Fusion, OFX or audio effect applied to a TimelineItem or PhotoAlbumItem.

    Effect objects are returned by ``add_effect`` and ``get_effects`` on
    :class:`~pybmd.timeline_item.TimelineItem` and
    :class:`~pybmd.photo_album_item.PhotoAlbumItem`.

    Version:
        Added in DaVinci Resolve 21.1.2
    """

    def __init__(self, effect):
        super(Effect, self).__init__(effect)
        self._effect = self._object

    def __repr__(self) -> str:
        info = self._effect.GetInfo() or {}
        return f"Effect: {info.get('name')}"

    ##############################################################################################################################
    # Add at DR 21.1.2

    @requires_resolve_version(added_in="21.1.2")
    def get_info(self) -> Optional["EffectInfo"]:
        """Returns information about the effect.

        Returns:
            EffectInfo | None: ``category``, ``id`` and ``name`` of the effect, None if
                no information was returned

        Raises:
            APIVersionError: If Resolve version < 21.1.2

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        from pybmd.settings import EffectInfo

        info = self._effect.GetInfo()
        if not info:
            return None
        return EffectInfo(**info)

    @requires_resolve_version(added_in="21.1.2")
    def get_is_enabled(self) -> bool:
        """Returns whether the effect is enabled.

        Returns:
            bool: True if the effect is enabled, False otherwise

        Raises:
            APIVersionError: If Resolve version < 21.1.2

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._effect.GetIsEnabled()

    @requires_resolve_version(added_in="21.1.2")
    def set_is_enabled(self, enabled: bool) -> bool:
        """Enables or disables the effect.

        Args:
            enabled (bool): True to enable the effect, False to disable it

        Returns:
            bool: True if successful, False otherwise

        Raises:
            APIVersionError: If Resolve version < 21.1.2

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._effect.SetIsEnabled(enabled)

    @requires_resolve_version(added_in="21.1.2")
    def get_fusion_comp(self) -> Optional[FusionComp]:
        """Returns the Fusion composition of this effect.

        Returns:
            FusionComp | None: the Fusion composition, None if this is not a Fusion effect

        Raises:
            APIVersionError: If Resolve version < 21.1.2

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        fusion_comp = self._effect.GetFusionComp()
        if fusion_comp is None:
            return None
        return FusionComp(fusion_comp)

    @requires_resolve_version(added_in="21.1.2")
    def get_index(self) -> Optional[int]:
        """Returns the 1-based index of the effect among the item's effects of the same
        category.

        Returns:
            int | None: the index, None if the effect is no longer applied

        Raises:
            APIVersionError: If Resolve version < 21.1.2

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._effect.GetIndex()

    @requires_resolve_version(added_in="21.1.2")
    def set_index(self, index: int) -> bool:
        """Moves the effect to the given 1-based index among the item's effects of the
        same category, which changes the order they are applied in.

        Args:
            index (int): new 1-based index

        Returns:
            bool: True if successful, False otherwise

        Raises:
            APIVersionError: If Resolve version < 21.1.2

        Version:
            Added in DaVinci Resolve 21.1.2
        """
        return self._effect.SetIndex(index)
