from ..database.models import Users,Movies,Reservations
from fastapi.responses import JSONResponse
from ..model import schemas


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
    

    
