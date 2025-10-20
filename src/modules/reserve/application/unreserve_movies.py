
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
from src.core.log_config import logger



def unreserve_movie(unreserve_model:UnReserveModel,user:User,provider:Provider):
    db_session = provider.db_session
    movie_repo:MovieRepository=provider.movie_repository
    reserve_repo:ReserveRepository=provider.reserve_repository
    logger.debug("Starting Unreservation")
    try:
        reserve:Reserve= validate_seats_to_unreserve(unreserve_model.reserve_id,unreserve_model.no_of_seats,reserve_repo)
        updated_reserve,before_reserve_seats=persist_unreserve(reserve,unreserve_model.no_of_seats,reserve_repo)
        movie=update_movie_after_reserve(reserve.movie_id,unreserve_model.no_of_seats,movie_repo)
        logger.debug("Unreservation and update movie seats successful by user: %s", user.username)
        db_session.commit()
        return {
            "username":user.username,
            "movie_name":movie_repo.get_by_id(movie.id).movie_name,
            "before_reserve_seats":before_reserve_seats,
            **vars(updated_reserve)
        }
    except Exception as e:
        db_session.rollback()
        logger.error("An unexpected error occured while unreserving movie")
        raise
    

def validate_seats_to_unreserve(reserve_id:str,no_of_seats:int,reserve_repo):
    raw_reserve = reserve_repo.get_by_id(reserve_id)
    if not raw_reserve:
        raise ReserveNotFoundException("Reservations Not Found")
    
    reserve: Reserve = reserve_repo.to_dataclass(raw_reserve,Reserve)
    if no_of_seats > reserve.user_reserve_seats or no_of_seats == 0 :
        raise InvalidSeatsEnteredException("Invalid Seats Entered")
    return reserve

def persist_unreserve(reserve:Reserve,no_of_seats,reserve_repo):
    before_reserve_seats = reserve.user_reserve_seats
    reserve.user_reserve_seats-=no_of_seats
    if reserve.user_reserve_seats == 0:
        if not reserve_repo.delete_by_id(reserve.id):
            raise FailedToDeleteReserveException(f"Failed to delete Reserve Row with {reserve.id}")
    else:
        reserve.updated_at=datetime.now()
        if not reserve_repo.update_reserve_seats(reserve.id,reserve.user_reserve_seats,reserve.updated_at):
            raise FailedToDeleteReserveException(f"Failed to delete Reserve Row with {reserve.id}")
    return reserve,before_reserve_seats
    

def update_movie_after_reserve(movie_id:str,no_of_seats:int,movie_repo):
    raw_movie:Movie= movie_repo.get_by_id(movie_id)
    if not raw_movie:
        raise MovieNotFoundException("No Such Movie Found")
    movie=movie_repo.from_persistence(raw_movie,Movie)
    movie.reserve_seats -= no_of_seats
    movie.available_seats += no_of_seats
    movie.movie_status = StatusType.AVAILABLE if movie.available_seats > 0 else movie.movie_status
    if not movie_repo.update_movie_seats_and_status(
            movie_id=movie.id,
            reserve_seats=movie.reserve_seats,
            available_seats=movie.available_seats,
            movie_status=movie.movie_status
            ):
        raise FailedToSaveException("Failed to update movie seats and status")
        
    return movie