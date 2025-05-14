from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User,UserRole
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from src.modules.reserve.exceptions import UserHasNoReservationException
from src.modules.reserve.entity.reserve import Reserve
from src.core.provider import Provider



class GetUserReserveOwn:
    def __init__(self,provider:Provider):
        self.user_repo:UserRepository = provider.reserve_repository
    
    def execute(self,user:User):
        raw_reserve= self.reserve_repo.get_by_user_id(user.id)
        if not raw_reserve:
            raise UserHasNoReservationException(f"{user.username} has not reserved any movie")

        reserve = self.user_repo.to_dataclass(raw_reserve,Reserve)
        return reserve
        