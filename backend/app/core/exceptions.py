class ClinexaException(Exception):
    """
    Base exception for all Clinexa AI application exceptions.
    """

    def __init__(
        self,
        message: str,
        error_code: str = "CLINEXA_ERROR",
        status_code: int = 500
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code

        super().__init__(message)


class ResourceNotFoundException(ClinexaException):
    """
    Raised when a requested resource does not exist.
    """

    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            error_code="RESOURCE_NOT_FOUND",
            status_code=404
        )


class BadRequestException(ClinexaException):
    """
    Raised when the request is invalid.
    """

    def __init__(self, message: str = "Invalid request"):
        super().__init__(
            message=message,
            error_code="BAD_REQUEST",
            status_code=400
        )


class ResourceAlreadyExistsException(ClinexaException):
    """
    Raised when a resource already exists.
    """

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            message=message,
            error_code="RESOURCE_ALREADY_EXISTS",
            status_code=409
        )