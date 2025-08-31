from src.core.exceptions import (
    BaseApiException,
    NotFoundException,
    DuplicateResourceException,
    FailedToSaveException,
    InvalidInputEnteredException
)

class MovieNotFoundException(NotFoundException): ...

class DuplicateMovieException(DuplicateResourceException): ...

class FailedToSaveMovieException(FailedToSaveException): ...

class InvalidSeatsEnteredException(InvalidInputEnteredException): ...

class FailedToUpdateMovieException(FailedToSaveException): ...