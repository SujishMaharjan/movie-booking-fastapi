from src.db_schemas.movie import Movies
from src.modules.reserve.exceptions import *
from src.modules.movie.exceptions import (FailedToUpdateMovieException,
                                          MovieNotFoundException,
                                          InvalidSeatsEnteredException)
from src.modules.reserve.handlers import *
from src.modules.user.queries import get_user_from_db_by_id
from src.modules.reserve.queries import *
from src.modules.movie.queries import get_movie_by_movie_name,get_movie_available_by_movie_name,get_movie_from_db_by_id
from src.modules.movie.handlers import (
    update_movie_after_reserve,
    update_movie_after_unreserve,
)
from src.api.entrypoint.movie.responses import *
from src.core.log_config import logger
from src.api.entrypoint.reserve.models import AddReserveModel
from src.api.entrypoint.reserve.responses import ReserveResponse
from src.core.extensions import db_dependency as db



def reserve_movie(db,reserve:Reservations,current_user,movie,no_of_seats):
    if reserve:
            update_reserve_seats =reserve.user_reserve_seats +no_of_seats
            reserve_id =  update_reserve_seat_in_db(db,reserve.reserve_id,update_reserve_seats=update_reserve_seats)     
    else:
        new_reserve = Reservations(
            user_id=current_user.user_id,
            movie_id=movie.movie_id,
            user_reserve_seats=no_of_seats
        )
        reserve_id= add_reserve_to_db(db,new_reserve)
    return reserve_id


def unreserve_movie(db,reserve:Reservations,no_of_seats):
    if reserve:
            update_reserve_seats =reserve.user_reserve_seats -no_of_seats
            reserve_id =  update_reserve_seat_in_db(db,reserve.reserve_id,update_reserve_seats=update_reserve_seats)
    return reserve_id


def persist_reserve_to_db(db,model,current_user):
    movie = get_movie_by_movie_name(db,model.movie_name)
    if not movie:
        raise MovieNotFoundException("Movie not found")
    reserve = check_user_reserve_this_movie_before(db,current_user.user_id, movie.movie_id)
    before_reserve_seats = reserve.user_reserve_seats if reserve else 0
    try:
    
        success = update_movie_after_reserve(db,movie, model.no_of_seats)
        reserve_id= reserve_movie(db,reserve,current_user,movie,model.no_of_seats)
        if not success or not bool(reserve_id):
            raise FailedToSaveReserveException("Failed to reserve movie.")

        # commit only after both update_movie and reserve
        db.commit()
        return ReserveResponse(reserve_id = reserve_id,
                               username= current_user.username,
                               movie_name=model.movie_name,
                               before_reserve_seats=before_reserve_seats,
                               user_reserve_seats=before_reserve_seats+model.no_of_seats
                               )
    except Exception as e:
        db.rollback()
        raise FailedToSaveReserveException(str(e))
    

def persist_unreserve_to_db(db,movie,no_of_seats,reserve:Reservations,current_user):
    before_reserve_seats = reserve.user_reserve_seats

    try:
        delete_success = False
        user_reserve_seats = before_reserve_seats - no_of_seats
        if user_reserve_seats == 0:
            db.delete(reserve)
            delete_success = True
        else:
            reserve_id = unreserve_movie(db,reserve,no_of_seats)

        success = update_movie_after_unreserve(db,movie,no_of_seats)

        if not ((delete_success or bool(reserve_id)) and success): 
            raise FailedToSaveReserveException("Failed to Unreserve Movie")

        db.commit()
        return ReserveResponse(reserve_id = reserve.reserve_id,
                               username= current_user.username,
                               movie_name=movie.movie_name,
                               before_reserve_seats=before_reserve_seats,
                               user_reserve_seats=user_reserve_seats
                               )


    except Exception as e:
        db.rollback()
        raise FailedToUnReserveExpection("Failed to unreserve") from e


def check_valid_movie_entered(db,current_user,movie_name):
    # breakpoint()
    try:
        movie = get_movie_by_movie_name(db,movie_name)

        if not movie:
            raise ReserveNotFoundException(f"User with {current_user.username} has not reserved movie {movie_name}")
        reserve = check_user_reserve_this_movie_before(db,current_user.user_id,movie.movie_id)
        if not reserve:
            raise ReserveNotFoundException(f"User with {current_user.username} has not reserved movie {movie_name}")
    except Exception as e:
        raise ReserveNotFoundException(str(e))

    return reserve,movie

def check_valid_seats_entered_to_unreserve(reserve, no_of_seats):
    if no_of_seats > reserve.user_reserve_seats or no_of_seats == 0:
        logger.warning("Invalid Seat entered")
        raise InvalidSeatsEnteredException("Invalid Seats Entered")
    return True

def list_out_all_reserves(db):
    reserves = get_all_reserves_from_db(db)
    if not reserves:
        return []
    reserve_response = [{"reserve_id":reserve.reserve_id,
                         "username":get_user_from_db_by_id(db,reserve.user_id).username,
                         "movie_name":get_movie_from_db_by_id(db,reserve.movie_id).movie_name
                        #  "user_reserve_seats":reserve.user_reserve_seats
                         }
                        for reserve in reserves]
    return reserve_response

def list_reserves_by_user(current_user):
    reserves = get_reserve_from_db_by_user_id(db,current_user.user_id)
    if not reserves:
        return []
    reserves_response= [{"username":current_user.username,
                         "movie_name":get_movie_by_movie_name(db,reserve.movie_id).movie_name,
                         "user_reserve_seats":reserve.user_reserve_seats
                         }
                        for reserve in reserves]
    return reserves_response


def is_movie_available_to_reserve(db,movie_name,no_of_seats) -> bool:
    # breakpoint()
    movie = get_movie_available_by_movie_name(db,movie_name)
    if not movie:
        raise MovieNotFoundException("No Such Movie Available")
    if no_of_seats > movie.available_seats or no_of_seats == 0 :
        raise InvalidSeatsEnteredException("Please Enter Valid Seats")
    return True
    