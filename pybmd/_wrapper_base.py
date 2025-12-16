from pybmd.error import WrapperInitError


class WrapperBase(object):
    """base class for all wrapper classes."""

    def __init__(self, _resolve_object):
        super(WrapperBase, self).__init__()
        if _resolve_object is None:
            raise WrapperInitError("_resolve_object cannot be None")
        self._resolve_object = _resolve_object
