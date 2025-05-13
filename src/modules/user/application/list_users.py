from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User
from src.core.provider import Provider


class ListUser:
    def __init__(self,provider:Provider):
        self.user_repo:UserRepository = provider.user_repository
    
    def execute(self):
        users = self.user_repo.get_all()
        users = [self.user_repo.to_dataclass(user,User) for user in users] if users else []
        return users
        
 

    





