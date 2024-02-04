class ResolveInitError(Exception):
    """Error for Resolve Init
    """
    def __init__(self, msg="Init Resolve failed,please check if davinci resolve is running"):
        super().__init__(msg)
        
        
class ValueMappingError(Exception):
    """Error for Value Mapping for EnumMapping class
    """
    def __init__(self, msg="Enum Value Mapping Error,please check number of values args is equal to number of enum value"):
        super().__init__(msg)