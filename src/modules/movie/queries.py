from src.db_schemas.user import Movies
from src.core.extensions import db_dependency
from src.core.extensions import db_dependency as db



def get_all_movies_from_db(db):
    return db.query(Movies).all()

def get_movie_by_movie_name(movie_name):
    return db.query(Movies).filter(Movies.movie_name == movie_name).all()

def save_movie_to_db(data):
    db.add(data)
    db.commit()
    return get_movie_by_movie_name(data.username)

def get_all_movies_available_from_db():
    movies = db.query(Movies).filter(Movies.movie_status == "Available").all()
    return movies

def is_movie_available_to_reserve():
    