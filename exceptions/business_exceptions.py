class BusinessException(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
        self.message = message


class NotFoundException(BusinessException):  # 404
    def __init__(self, message="Resource not found", *args):
        super().__init__(message, *args)


class ForbiddenException(BusinessException):  # 403
    def __init__(self, message="Forbidden access", *args):
        super().__init__(message, *args)


class BadRequestException(BusinessException):  # 400
    def __init__(self, message="Bad request", details=[], *args):
        super().__init__(message, *args)
        self.details = details


class UnauthorizedException(BusinessException):  # 401
    def __init__(self, message="Unauthorized access", *args):
        super().__init__(message, *args)
