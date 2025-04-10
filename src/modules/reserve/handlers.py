from src.db_schemas.movie import Movies
from src.modules.reserve.exceptions import *
from src.modules.movie.exceptions import FailedToUpdateMovieException,MovieNotFoundException
from src.modules.reserve.handlers import *
from src.modules.reserve.queries import *
from src.modules.movie.queries import get_movie_by_movie_name
from src.modules.movie.handlers import update_movie_after_reserve,update_movie_after_unreserve
from src.api.entrypoint.movie.responses import *
from src.core.log_config import logger
from src.api.entrypoint.reserve.models import AddReserveModel
from src.api.entrypoint.reserve.responses import ReserveUpdateResponse
from src.core.extensions import db_dependency as db





def persist_reserve_to_db(model,current_user):
    
    movie = get_movie_by_movie_name(model.movie_name)
    if not movie:
        raise MovieNotFoundException("Movie not found")

    reserve = check_user_reserve_this_movie_before(current_user.user_id, movie.movie_id)
    before_reserve_seats = reserve.user_reserve_seats if reserve else 0

    try:
        if reserve:
            reserve.user_reserve_seats += model.no_of_seats
        else:
            new_reserve = Reservations(
                user_id=current_user.user_id,
                movie_id=movie.movie_id,
                user_reserve_seats=model.no_of_seats
            )
            db.add(new_reserve)

        db.commit()
    except Exception as e:
        db.rollback()
        raise FailedToSaveReserveException("Failed to reserve") from e

    # Update movie after reserve
    if not update_movie_after_reserve(movie, model.no_of_seats):
        raise FailedToUpdateMovieException("Failed to update movie seat count")

    return ReserveUpdateResponse(**model.dict(), before_reserve_seats=before_reserve_seats)



def persist_unreserve_to_db(model,current_user):
    
    movie = get_movie_by_movie_name(model.movie_name)
    if not movie:
        raise MovieNotFoundException("Movie not found")

    reserve = get_reserve_from_db_by_userid_movie_id(current_user.user_id, movie.movie_id)
    if not reserve:
        raise ReserveNotFoundException("No reservation found for this user and movie")

    before_reserve_seats = reserve.user_reserve_seats

    try:
        reserve.user_reserve_seats -= model.no_of_seats

        if reserve.user_reserve_seats <= 0:
            db.delete(reserve)

        db.commit()

    except Exception as e:
        db.rollback()
        raise FailedToUnReserveExpection("Failed to unreserve") from e

    if not update_movie_after_unreserve(movie, model.no_of_seats):
        # incase if failed to update movie, it should rollback the reserve commit
        db.rollback()
        raise FailedToUnReserveExpection("Failed to update movie seat count so rollback previous reserve commit")

    return ReserveUpdateResponse(**model.dict(), before_reserve_seats=before_reserve_seats)



    


def check_valid_movie_entered(current_user,movie_name)
    
    movie_id = get_movie_by_movie_name(movie_name).movie_id
    reserve = get_reserve_from_db_by_userid_movie_id(current_user.user_id,movie_id)
    return reserve

def check_valid_seats_entered_to_unreserve(reserve, no_of_seats):
    
    if no_of_seats > reserve.user_reserve_seats:
        logger.warning("Invalid Seat entered")

        return False
    return True


def list_reserves_by_user(current_user):
    reserves = get_reserve_from_db_by_user_id(current_user.user_id)
    if not reserves:
        return []
    reserves_response= [{"username":current_user.username,
                         "movie_name":get_movie_by_movie_name(reserve.movie_id).movie_name,
                         "user_reserve_seats":reserve.user_reserve_seats
                         }
                        for reserve in reserves]
    return reserves_response