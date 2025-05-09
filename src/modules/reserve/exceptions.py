from src.core.exceptions import (
    BaseApiException,
    NotFoundException,
    DuplicateResourceException,
    FailedToSaveException,
    NotAvailableException
)

class ReserveNotFoundException(NotFoundException): ...

class DuplicateReserveException(DuplicateResourceException): ...

class FailedToSaveReserveException(FailedToSaveException): ...

class FailedToUnReserveExpection(BaseApiException): ...

class MovieNotAvailableException(NotAvailableException):...

