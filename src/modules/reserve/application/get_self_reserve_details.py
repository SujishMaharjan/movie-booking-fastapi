from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User,UserRole
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from src.modules.reserve.exceptions import UserHasNoReservationException
from src.modules.reserve.entity.reserve import Reserve



class GetUserReserveOwn:
    def __init__(self,token:str,user_repo:UserRepository,token_repo:TokenRepository,reserve_repo:ReserveRepository):
        self.token=token
        self.user_repo= user_repo
        self.token_repo = token_repo
        self.reserve_repo = reserve_repo
    
    def execute(self):
        username = self.token_repo.validate_and_decode_token(self.token)
        user = self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundException("User Not Found")
        user:User = self.user_repo.to_dataclass(user,User)
        self.is_member(user.role)

        reserve= self.reserve_repo.get_by_user_id(user.id)
        if not reserve:
            raise UserHasNoReservationException(f"{username} has not reserved any movie")

        reserve = self.user_repo.to_dataclass(reserve,Reserve)
        return reserve
        
    def is_member(self,role)->bool:
        if role==UserRole.ADMIN:
            raise InvalidMemberTypeException("Access denied. Member only.")
        return True
