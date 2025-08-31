from src.core.exceptions import BaseApiException,NotFoundException



class UserNotFoundException(NotFoundException): ...

class InvalidMemberTypeException(BaseApiException): ...
