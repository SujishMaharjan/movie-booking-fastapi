from models import Users,Movies,Reservations
from fastapi.responses import JSONResponse
from model import schemas

def check_same_username_with_same_movie(db,username,movie_name):
    user_id = db.query(Users).filter(Users.username == username).first().user_id
    movie_id = db.query(Movies).filter(Movies.movie_name == movie_name).first().movie_id
    breakpoint()
    reserve = db.query(Reservations).filter((Reservations.user_id == user_id) & (Reservations.movie_id == movie_id)).first()

    return reserve

def check_valid_seats_to_reserve(db,reserve):
    available_seats = db.query(Movies).filter(Movies.movie_name == reserve.movie_name).first().available_seats
    if reserve.no_of_seats > available_seats:
        return JSONResponse(content={'detail':f"Invalid seats entered,Available Seats: {available_seats}"})

def add_reservation(db, reserve, current_user):
    # breakpoint()
    db_reserve = check_same_username_with_same_movie(db,current_user.username,reserve.movie_name)
    breakpoint()
    reserve_success =  False
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