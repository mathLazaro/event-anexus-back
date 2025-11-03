class BusinessException(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message


class NotFoundException(BusinessException):
    def __init__(self, message="Resource not found", *args):
        super().__init__(message, *args)


class ForbiddenException(BusinessException):
    def __init__(self, message="Forbidden access", *args):
        super().__init__(message, *args)


class BadRequestException(BusinessException):
    def __init__(self, message="Bad request", details=[], *args):
        super().__init__(message, *args)
        self.details = details
