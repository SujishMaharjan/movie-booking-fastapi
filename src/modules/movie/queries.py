from src.db_schemas.movie import Movies
from src.core.extensions import db_dependency
from src.core.extensions import db_dependency as db



def get_all_movies_from_db(db):
    return db.query(Movies).all()

def get_movie_by_movie_name(db,movie_name):
    return db.query(Movies).filter(Movies.movie_name == movie_name).first()

def save_movie_to_db(db,data):
    db.add(data)
    db.commit()
    return get_movie_by_movie_name(db,data.movie_name)

def get_all_movies_available_from_db(db):
    movies = db.query(Movies).filter(Movies.movie_status == "Available").all()
    return movies

def get_movie_from_db_by_id(db,movie_id):
    return db.query(Movies).filter(Movies.movie_id == movie_id).first()