from pybmd._wrapper_base import WrapperBase


class GalleryStill(WrapperBase):
    """GalleryStill Object"""

    def __init__(self, gallery_still):
        super(GalleryStill, self).__init__(gallery_still)
        self._gallery_still = self._resolve_object
