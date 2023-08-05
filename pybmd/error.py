class ResolveInitError(Exception):
    """Error for Resolve Init
    """
    def __init__(self, msg="Init Resolve failed,please check if davinci resolve is running"):
        super().__init__(msg)