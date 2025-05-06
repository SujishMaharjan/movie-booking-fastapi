from abc import ABC, abstractmethod
from src.modules.user.entity.user import User
from typing import Union

class UserRepository(ABC):

    
    def save(self, user: User)-> User: ...

    def get_by_id(self, user_id: int)-> Union[User,None]: ...

    def get_by_username(self, username: str)-> Union[User,None]: ...

    def get_by_email(self, email: str)-> Union[User,None]: ...

    def get_by_phone(self, phone: str)-> Union[User,None]: ...

    def username_exists(self, username: str)->bool:...

    