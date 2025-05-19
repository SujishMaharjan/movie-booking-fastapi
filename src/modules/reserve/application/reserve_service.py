from src.modules.auth.application.ports.token_repository import TokenRepository
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User
from src.modules.reserve.entity.reserve import Reserve
from src.core.provider import Provider




class ListAllReservesService:
    def __init__(self,provider:Provider):
        self.reserve_repo:ReserveRepository = provider.reserve_repository

    def execute(self):
        reserves = self.reserve_repo.get_all()
        reserves = [self.reserve_repo.to_dataclass(reserve,Reserve) for reserve in reserves] if reserves else []
        return reserves

