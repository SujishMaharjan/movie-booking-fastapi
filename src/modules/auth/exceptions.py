from src.core.exceptions import BaseHttPException
from src.core.exceptions import (
    DuplicateResourceException,
    FailedToSaveException,
    InvalidLoginException,
    InvalidInputException,
    UnauthorizedException
)
from src.core.log_config import logger


class DuplicateUserException(DuplicateResourceException):...
    
class FailedToSaveUserException(FailedToSaveException): ...

class InvalidTokenException(InvalidInputException): ...

class InvalidUserNameException(InvalidLoginException): ...

class InvalidPasswordException(InvalidLoginException): ...

class LoginException(UnauthorizedException): ...

class InvalidMemberTypeException(UnauthorizedException): ...

