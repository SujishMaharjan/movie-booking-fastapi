from src.db_schemas.movie import Movies
from src.modules.movie.exceptions import *
from src.modules.movie.queries import *
from src.api.entrypoint.movie.responses import *
from src.core.log_config import logger
from src.api.entrypoint.movie.models import MovieAddModel





def get_movies():
    movies = get_all_movies_from_db()
    if not movies:
        raise MovieNotFoundException
    all_movie_response = [AllMovieResponse(**movie.model_dump()) for movie in movies]
    return all_movie_response




def check_duplicate_movie(movie_name):
    movie = get_movie_by_movie_name(movie_name)
    if movie:
        logger.warning("Trying to create duplicate movie")
        raise DuplicateMovieException(
            f"Movie with Moviename {movie_name} already exists"
        )
    else:
        return None
    

def persist_movie_to_db(model: MovieAddModel):
    data = model.model_dump()
    movie = save_movie_to_db(db,data)
    if not movie:
         logger.error("Failed to save user in database")
         raise FailedToSaveMovieException(
              f"An Unexpected error occured while creating user with username {data.username}"
         )
    return MovieAddResponse(**movie)

def get_all_movies_available():
    movies = get_all_movies_available_from_db()
    if not movies:
        raise MovieNotFoundException
    available_movies = [MovieResponseAvailable(**vars(movie)) for movie in movies]
    return available_movies

def is_movie_available_to_reserve(movie_name,no_of_seats) -> bool:
    movie: Movies = get_movie_by_movie_name(movie_name)
    if not movie:
        raise MovieNotFoundException
    if movie.available_seats < no_of_seats:
        raise InvalidSeatsEnteredException
    return True
    
def update_movie_after_reserve(movie,no_of_seats):
    movie.reserve_seats += no_of_seats
    movie.available_seats -= no_of_seats
    if movie.available_seats == 0:
        movie.movie_status = "Fully Reserved"
    db.commit()
    db.refresh(movie)
    return True

def update_movie_after_unreserve(movie,no_of_seats):
    movie.reserve_seats -= no_of_seats
    movie.available_seats += no_of_seats
    if movie.available_seats != 0:
        movie.movie_status = "Available"
    db.commit()
    db.refresh(movie)
    return True
