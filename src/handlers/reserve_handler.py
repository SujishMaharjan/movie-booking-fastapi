from ..database.models import Users,Movies,Reservations
from fastapi.responses import JSONResponse
from ..handlers.user_handler import check_user_member_type
from ..handlers.movie_handler import check_movie_available
from ..log import logger
from ..model.responses.reserve import ReserveResponse,UnReserveResponse
from ..exceptions import (
    MemberTypeError,
    MovieNotAvailableError,
    InvalidSeatsEnteredError,
    FailedToReserveError,
    MovieNotReserveByUserError
)

def check_same_username_with_same_movie(db,username,movie_name):
    user_id = db.query(Users).filter(Users.username == username).first().user_id
    movie_id = db.query(Movies).filter(Movies.movie_name == movie_name).first().movie_id
    # breakpoint()
    reserve = db.query(Reservations).filter((Reservations.user_id == user_id) & (Reservations.movie_id == movie_id)).first()
    return reserve

def check_valid_seats_to_reserve(db,reserve):
    available_seats = db.query(Movies).filter(Movies.movie_name == reserve.movie_name).first().available_seats
    if reserve.no_of_seats > available_seats:
        return False
    return True
        

def add_reservation(db, reserve, current_user):
    db_reserve = check_same_username_with_same_movie(db,current_user.username,reserve.movie_name)
    if not db_reserve:
        reserve_data = {}
        reserve_data["user_id"] = current_user.user_id
        reserve_data["movie_id"] = db.query(Movies).filter(Movies.movie_name == reserve.movie_name).first().movie_id
        reserve_data["user_reserve_seats"] = reserve.no_of_seats
        reserve_data = Reservations(**reserve_data)
        db.add(reserve_data)
        db.commit()
        reserve_success = True
    else:
        db_reserve.user_reserve_seats += reserve.no_of_seats
        db.commit()
        db.refresh(db_reserve)
        reserve_success = True
    if not reserve_success:
        return JSONResponse(content={'detail':"Failed to reserve"})
    movie = db.query(Movies).filter(Movies.movie_name == reserve.movie_name).first()
    # breakpoint()
    movie.reserve_seats += reserve.no_of_seats
    movie.available_seats -= reserve.no_of_seats
    if movie.available_seats == 0:
        movie.movie_status = "Fully Reserved"
    db.commit()
    db.refresh(movie)
    return True
    
        

def get_all_reserves(db,current_user):
    reserves = db.query(Reservations).filter(Reservations.user_id == current_user.user_id).all()
    reserves_response= [{"username":current_user.username,
                         "movie_name":db.query(Movies).filter(Movies.movie_id == reserve.movie_id).first().movie_name,
                         "user_reserve_seats":reserve.user_reserve_seats
                         }
                        for reserve in reserves]
    return reserves_response


def get_reserve_from_db(db,current_user,movie_name):
    movie_id = movie_id = db.query(Movies).filter(Movies.movie_name == movie_name).first().movie_id
    reserve = db.query(Reservations).filter((Reservations.user_id == current_user.user_id) & (Reservations.movie_id == movie_id)).first()
    return reserve
    
    
def check_valid_seats_to_unreserve(db,reserve,no_of_seats):
    if no_of_seats > reserve.user_reserve_seats:
        return False
    return True
    

def unreserve_seats(db,db_reserve,no_of_seats,current_user):

    db_reserve.user_reserve_seats -= no_of_seats
    movie = db.query(Movies).filter(Movies.movie_id == db_reserve.movie_id).first()
    if db_reserve.user_reserve_seats == 0:
        db.delete(db_reserve)
    
    db.commit()
    unreserve_success = True
    if not unreserve_success:
        return JSONResponse(content={'detail':"Failed to unreserve"})
    # breakpoint()
    movie.reserve_seats -= no_of_seats
    movie.available_seats += no_of_seats
    if movie.available_seats != 0:
        movie.movie_status = "Available"
    db.commit()
    db.refresh(movie) 
    return True


def add_reserve(db,reserve,current_user):
    if not check_user_member_type(current_user,"member"):
        raise MemberTypeError
    if not check_movie_available(db,reserve.movie_name):
        raise MovieNotAvailableError
    if not check_valid_seats_to_reserve(db,reserve):
        raise InvalidSeatsEnteredError
    if not add_reservation(db,reserve,current_user):
        raise FailedToReserveError
    
    logger.info(f"{reserve.movie_name} reserved by {current_user.username}")
    # breakpoint()
    return ReserveResponse(
        username=current_user.username,
        movie_name=reserve.movie_name,
        user_reserved_seats=reserve.no_of_seats
        )


def unreserve_movie(db,unreserve,current_user):
    if not check_user_member_type(current_user,"member"):
        raise MemberTypeError
    db_reserve = get_reserve_from_db(db,current_user,unreserve.movie_name)
    if not db_reserve:
        raise MovieNotReserveByUserError(detail=f"No Reservations done in {unreserve.movie_name} found by {current_user.username}")
    before_reserve_seats = db_reserve.user_reserve_seats
    if not check_valid_seats_to_unreserve(db,db_reserve,unreserve.no_of_seats):
        JSONResponse(content={'detail':f"Invalid seats entered, Reserved  Seats: {db_reserve.user_reserve_seats}"})
    if not unreserve_seats(db,db_reserve,unreserve.no_of_seats,current_user):
        return JSONResponse(content={'detail':"Error in reserving movies"})
    logger.info(f"{unreserve.movie_name} reserved by {current_user.username}")

    unreserve_response_dict={
        "username":current_user.username,
        "movie_name":unreserve.movie_name,
        "before_reserve_seats":before_reserve_seats,
        "update_reserve_seats":db_reserve.user_reserve_seats
    }
    
    return UnReserveResponse(**unreserve_response_dict)
    




    
