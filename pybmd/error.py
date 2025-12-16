class ResolveInitError(Exception):
    """Error for Resolve Init
    """
    def __init__(self, msg="Init Resolve failed,please check if davinci resolve is running"):
        super().__init__(msg)
        
class UnsupportSystemError(Exception):
    """Error for system not support
    """
    def __init__(self, msg="Unsupport system!"):
        super().__init__(msg)
        

class WrapperInitError(Exception):
    """Error for Wrapper Init
    """
    def __init__(self, msg="Init Wrapper failed,please check if the input argument is valid"):
        super().__init__(msg)