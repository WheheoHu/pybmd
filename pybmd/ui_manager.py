from pybmd._wrapper_base import WrapperBase


class UI_Manager(WrapperBase):
    """docstring for UI_Manager."""

    def __init__(self, ui_manager):
        super(UI_Manager, self).__init__(ui_manager)
        self._ui_manager = self._resolve_object