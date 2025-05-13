from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User
from src.core.provider import Provider

class GetUser:
    def __init__(self,provider:Provider):
        self.user_repo:UserRepository = provider.user_repository
    
    def execute(self,user_id:int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"No user with such id{user_id}")
        breakpoint()
        user = self.user_repo.to_dataclass(user,User)
        return user
    
