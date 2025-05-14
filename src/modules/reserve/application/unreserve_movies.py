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
from src.entrypoints.api.reserve.models import UnReserveModel
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from datetime import datetime
from src.modules.reserve.exceptions import FailedToSaveException, MovieNotAvailableException,ReserveNotFoundException,FailedToDeleteReserveException
from src.core.provider import Provider

class MovieUnreserveService:
    def __init__(self,provider:Provider):
        self.movie_repo:MovieRepository=provider.movie_repository
        self.reserve_repo:ReserveRepository=provider.reserve_repository

    def execute(self,unreserve_model:UnReserveModel,user):
        reserve:Reserve= self.validate_seats_to_unreserve(unreserve_model.reserve_id,unreserve_model.no_of_seats)
        updated_reserve,before_reserve_seats=self.persist_unreserve(reserve,unreserve_model.no_of_seats)
        movie=self.update_movie_after_reserve(reserve.movie_id,unreserve_model.no_of_seats)
        return {
            "username":user.username,
            "movie_name":self.movie_repo.get_by_id(movie.id).movie_name,
            "before_reserve_seats":before_reserve_seats,
            **updated_reserve.__dict__
        }
    
    def is_member(self,role)->bool:
        if role!=UserRole.MEMBER:
            raise InvalidMemberTypeException("Access denied. Member only.")
        return True
    

    def validate_seats_to_unreserve(self,reserve_id:str,no_of_seats:int):
        raw_reserve = self.reserve_repo.get_by_id(reserve_id)
        if not raw_reserve:
            raise ReserveNotFoundException("Reservations Not Found")
        
        reserve: Reserve = self.reserve_repo.to_dataclass(raw_reserve,Reserve)
        if no_of_seats > reserve.user_reserve_seats or no_of_seats == 0 :
            raise InvalidSeatsEnteredException("Invalid Seats Entered")
        return reserve
    
    def persist_unreserve(self,reserve:Reserve,no_of_seats):
        before_reserve_seats = reserve.user_reserve_seats
        reserve.user_reserve_seats-=no_of_seats
        if reserve.user_reserve_seats == 0:
            if not self.reserve_repo.delete_by_id(reserve.id):
                raise FailedToDeleteReserveException(f"Failed to delete Reserve Row with {reserve.id}")
        else:
            reserve.updated_at=datetime.now()
            if not self.reserve_repo.update_reserve_seats(reserve.id,reserve.user_reserve_seats,reserve.updated_at):
                raise FailedToDeleteReserveException(f"Failed to delete Reserve Row with {reserve.id}")
        return reserve,before_reserve_seats
        
    
    def update_movie_after_reserve(self,movie_id:str,no_of_seats:int):
        raw_movie:Movie= self.movie_repo.get_by_id(movie_id)
        if not raw_movie:
            raise MovieNotFoundException("No Such Movie Found")
        movie=self.movie_repo.to_dataclass(raw_movie,Movie)
        movie.reserve_seats -= no_of_seats
        movie.available_seats += no_of_seats
        movie.movie_status = StatusType.AVAILABLE if movie.available_seats > 0 else movie.movie_status
        if not self.movie_repo.update_movie_seats_and_status(
                movie_id=movie.id,
                reserve_seats=movie.reserve_seats,
                available_seats=movie.available_seats,
                movie_status=movie.movie_status
                ):
            raise FailedToSaveException("Failed to update movie seats and status")
            
        return movie