from pybmd._wrapper_base import WrapperBase


class FusionComp(WrapperBase):
    """Fusion Composite Object"""
    def __init__(self, fusion_comp):
        super(FusionComp, self).__init__(fusion_comp)
        self._fusion_comp = self._resolve_object
        
    

    