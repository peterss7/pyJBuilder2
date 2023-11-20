class MethodResult:
    def __init__(self, success=True, data=None, error_message=None) -> None:
        self.success = success
        self.data = data
        self.error_message=error_message
    
    @classmethod
    def success(cls, data=None):
        return cls(success=True, data=data)
    
    @classmethod
    def failure(cls, error_message, data=None):
        return cls(success=False, error_message = error_message, data=data)     