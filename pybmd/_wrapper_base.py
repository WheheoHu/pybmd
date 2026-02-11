from pybmd.error import WrapperInitError


class WrapperBase(object):
    """base class for all wrapper classes."""

    def __init__(self, _object):
        super(WrapperBase, self).__init__()
        if _object is None:
            raise WrapperInitError("davinci resolve object cannot be None")
        self._object = _object
