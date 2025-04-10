from src.db_schemas.reserve import Reservations
from src.core.extensions import db_dependency as db


def get_reserve_from_db(id):
    reserve = db.query(Reservations).filter((Reservations.id == id)).first()
    return reserve

def get_reserve_from_db_by_userid_movie_id(movie_id)
    reserve = db.query(Reservations).filter((Reservations.movie_id == movie_id)).first()
    return reserve

def check_user_reserve_this_movie_before(user_id,movie_id):
    # reserve = db.query(Reservations).filter((Reservations.user_id == user_id) & (Reservations.movie_id == movie_id)).first()
    # return reserve
    reserve = db.query(Reservations).filter((Reservations.user_id == user_id) & (Reservations.movie_id == movie_id)).first()
    return reserve

# def update_reserve_in_db():
#     db.commit()
#     return get_reserve_from_db()
    


def save_reserve_to_db(data):
    db.add(data)
    db.commit()
    return get_reserve_from_db(data.id)


def get_reserve_from_db_by_user_id(user_id):
    reserve = db.query(Reservations).filter(Reservations.user_id == user_id).all()
    return reserve
    