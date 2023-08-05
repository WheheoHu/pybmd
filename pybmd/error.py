class ResolveInitError(Exception):
    """Error Class for init Resolve Object

    """
    def __init__(self, msg="Init Resolve failed,please check if davinci resolve is running"):
        super().__init__(msg)