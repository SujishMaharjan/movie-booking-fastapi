from src.modules.movie.infrastructure.persistence.models import Movies
from src.modules.movie.exceptions import *
from src.modules.movie.queries import *
from src.api.entrypoint.movie.responses import *
from src.core.log_config import logger
from src.api.entrypoint.movie.models import MovieAddModel





def get_all_movies(db_session):
    movies = get_all_movies_from_db(db_session)
    if not movies:
        return []
    # breakpoint()
    all_movie_response = [AllMovieResponse(**movie.__dict__) for movie in movies]
    return all_movie_response




def check_duplicate_movie(db_session,movie_name):
    movie = get_movie_by_movie_name(db_session,movie_name)
    if movie:
        logger.warning("Trying to create duplicate movie")
        raise DuplicateMovieException(
            f"Movie with Moviename {movie_name} already exists"
        )
    else:
        return None
    

def persist_movie_to_db(db_session,model: MovieAddModel):
    data = Movies(**model.model_dump())
    movie = save_movie_to_db(db_session,data)
    # breakpoint()
    if not movie:
         logger.error("Failed to save user in database")
         raise FailedToSaveMovieException(
              f"An Unexpected error occured while creating user with username {data.username}"
         )
    
    return MovieAddResponse(**movie.__dict__)

def get_all_movies_available(db_session):
    movies = get_all_movies_available_from_db(db_session)
    if not movies:
        return []
    available_movies = [MovieResponseAvailable(**movie.__dict__) for movie in movies]
    return available_movies

# def is_movie_available_to_reserve(db_session,movie_name,no_of_seats) -> bool:
#     breakpoint()
#     movie = get_movie_available_by_movie_name(db_session,movie_name)
#     if not movie:
#         raise MovieNotFoundException
#     if movie.available_seats < no_of_seats:
#         raise InvalidSeatsEnteredException
#     return True
    
def update_movie_after_reserve(db_session,movie:Movies,no_of_seats):
    update_reserve_seats = movie.reserve_seats +no_of_seats
    update_available_seats =movie.available_seats -no_of_seats
    if update_available_seats == 0:
        movie_status = "Fully Reserved"
    else:
        movie_status = movie.movie_status
    return bool(update_movie_after_reserve_or_unreserve_in_db(db_session,movie.movie_id,update_reserve_seats,update_available_seats,movie_status))
    


    # movie.reserve_seats += no_of_seats
    # movie.available_seats -= no_of_seats
    # if movie.available_seats == 0:
    #     movie.movie_status = "Fully Reserved"
    # db_session.commit()
    # db_session.refresh(movie)
    # return True

def update_movie_after_unreserve(db_session,movie:Movies,no_of_seats):
    update_reserve_seats = movie.reserve_seats -no_of_seats
    update_available_seats =movie.available_seats +no_of_seats
    if update_available_seats != 0:
        movie_status = "Available"
    else:
        movie_status = movie.movie_status
    return bool(update_movie_after_reserve_or_unreserve_in_db(db_session,movie.movie_id,update_reserve_seats,update_available_seats,movie_status))
    


# def update_movie_after_unreserve(db_session,movie,no_of_seats):
#     movie.reserve_seats -= no_of_seats
#     movie.available_seats += no_of_seats
#     if movie.available_seats != 0:
#         movie.movie_status = "Available"
#     db_session.commit()
#     db_session.refresh(movie)
#     return True


def get_movie_by_id(db_session,movie_id):
    movie = get_movie_from_db_by_id(db_session,movie_id)
    if not movie:
        raise MovieNotFoundException("No such Id")
    return movie