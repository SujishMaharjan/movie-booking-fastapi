from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User

class GetUserOwn:
    def __init__(self,token:str,user_repo:UserRepository,token_repo:TokenRepository):
        self.token=token
        self.user_repo= user_repo
        self.token_repo = token_repo
    
    def execute(self):
        payload = self.token_repo.validate_and_decode_token(self.token)
        username = payload.get("sub")
        user = self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundException("User Not Found")
        user = self.user_repo.to_dataclass(user,User)
        self.is_member(user.role)

        user = self.user_repo.get_by_id(user.id)
        user = self.user_repo.to_dataclass(user,User)
        return user
        
    def is_Member(self,role)->bool:
        if role!="admin":
            raise InvalidMemberTypeException("Access denied. Member only.")
        return True
