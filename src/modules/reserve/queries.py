from src.db_schemas.reserve import Reservations
# from src.core.extensions import db_dependency as db


def get_reserve_from_db(db,reserve_id):
    reserve = db.query(Reservations).filter((Reservations.reserve_id == reserve_id)).first()
    return reserve

def get_reserve_from_db_by_userid_movie_id(db,movie_id):
    reserve = db.query(Reservations).filter((Reservations.movie_id == movie_id)).first()
    return reserve

def check_user_reserve_this_movie_before(db,user_id,movie_id):
    # reserve = db.query(Reservations).filter((Reservations.user_id == user_id) & (Reservations.movie_id == movie_id)).first()
    # return reserve
    reserve = db.query(Reservations).filter((Reservations.user_id == user_id) & (Reservations.movie_id == movie_id)).first()
    return reserve

# def update_reserve_in_db():
#     db.commit()
#     return get_reserve_from_db()
    


def add_reserve_to_db(db,data):
    db.add(data)
    # return True
    db.flush()
    return get_reserve_from_db(db,data.reserve_id).reserve_id

def update_reserve_seat_in_db(db,reserve_id,update_reserve_seats):
    db.query(Reservations).filter(Reservations.reserve_id == reserve_id).update(
        {Reservations.user_reserve_seats: update_reserve_seats},  # <-- new value
        synchronize_session=False
    )
    # return True
    return reserve_id



def get_reserve_from_db_by_user_id(db,user_id):
    reserve = db.query(Reservations).filter(Reservations.user_id == user_id).all()
    return reserve

def get_all_reserves_from_db(db):
    return db.query(Reservations).all()
    
