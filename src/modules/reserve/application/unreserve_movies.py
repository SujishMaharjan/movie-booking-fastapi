import uuid
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User,UserRole
from src.modules.movie.entity.movie import Movie,StatusType
from src.modules.reserve.entity.reserve import Reserve
from src.modules.movie.exceptions import MovieNotFoundException,InvalidSeatsEnteredException
from src.modules.reserve.exceptions import ReserveNotFoundException
from src.entrypoints.api.reserve.models import AddReserveModel
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from datetime import datetime
from src.modules.reserve.exceptions import FailedToSaveException, MovieNotAvailableException


class MovieUnreserveService:
    def __init__(self,token:str,user_repo:UserRepository,token_repo:TokenRepository,movie_repo:MovieRepository,reserve_repo:ReserveRepository):
        self.token=token
        self.user_repo=user_repo
        self.token_repo=token_repo
        self.movie_repo=movie_repo
        self.reserve_repo=reserve_repo

    def execute(self,reserve_model:AddReserveModel):
        username = self.token_repo.validate_and_decode_token(self.token)
        user = self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundException("User Not Found")
        
        user:User = self.user_repo.to_dataclass(user,User)
        self.is_member(user.role)
        movie:Movie = self.validate_movie_and_seat_to_reserve(reserve_model.movie_id,reserve_model.no_of_seats)
        updated_movie=self.update_movie_before_reserve(movie,reserve_model.no_of_seats)
        updated_reserve,before_reserve_seats=self.create_or_update_reserve(user.id,movie.id,reserve_model.no_of_seats)
        return {
            "username":user.username,
            "movie_name":movie.movie_name,
            "before_reserve_seats":before_reserve_seats,
            **updated_reserve.__dict__
        }