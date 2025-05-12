from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User
from src.modules.reserve.entity.reserve import Reserve




class ListAllReservesService:
    def __init__(self,token,user_repo:UserRepository,token_reop:TokenRepository,reserve_repo:ReserveRepository):
        self.token = token
        self.user_repo = user_repo
        self.token_repo= token_reop
        self.reserve_repo = reserve_repo

    def execute(self):
        username = self.token_repo.validate_and_decode_token(self.token)
        
        user = self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundException("User Not Found")
        user = self.user_repo.to_dataclass(user,User)

        self.is_admin(user.role)

        reserves = self.reserve_repo.get_all()
        reserves = [self.reserve_repo.to_dataclass(reserve,Reserve) for reserve in reserves] if reserves else []
        return reserves

    def is_admin(self,role)->bool:
        if role!="admin":
            raise InvalidMemberTypeException("Access denied. Admin only.")
        return True
