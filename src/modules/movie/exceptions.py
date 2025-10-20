from src.core.exceptions import (
    BaseApiException,
    NotFoundException,
    DuplicateResourceException,
    FailedToSaveException,
    InvalidInputException
)

class MovieNotFoundException(NotFoundException): ...

class DuplicateMovieException(DuplicateResourceException): ...

class FailedToSaveMovieException(FailedToSaveException): ...

class InvalidSeatsEnteredException(InvalidInputException): ...

class FailedToUpdateMovieException(FailedToSaveException): ...