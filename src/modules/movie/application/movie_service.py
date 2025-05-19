import uuid
from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.movie.exceptions import DuplicateMovieException,MovieNotFoundException
from src.modules.movie.entity.movie import Movie
from datetime import datetime
from src.entrypoints.api.movie.models import MovieAddModel
from src.modules.movie.entity.movie import Movie
from src.core.provider import Provider
from src.core.log_config import logger
from src.entrypoints.api.movie.models import MovieAddModel



def create_movie_service(movie_model:MovieAddModel,hall_settings,provider:Provider):
    movie_repo:MovieRepository=provider.movie_repository
    try:
        check_duplicate_movie(movie_model.movie_name,movie_repo)
        movie = Movie(
            id=str(uuid.uuid4()),
            movie_name=movie_model.movie_name,
            movie_description=movie_model.movie_description,
            movie_status=movie_model.movie_status,
            total_seats=hall_settings.seat_capacity,
            reserve_seats=0,
            available_seats=hall_settings.seat_capacity,
            created_at=datetime.now()
        )

        movie_data = movie_repo.to_persistence(movie)
        movie_repo.save(movie_data)
        logger.info("Movie created successfully: %s", movie.movie_name)
        return movie
    except Exception as e:
        logger.error("Unexpected error while creating movie: %s", movie_model.movie_name)
        raise
    

def list_movies(provider:Provider):
    movie_repo:MovieRepository=provider.movie_repository
    try:
        movies = movie_repo.get_all()
        return movies
    except Exception as e:
        logger.error("An unexpected error occured while fetching list of movies")
        raise

def get_available_movies(provider:Provider):
    movie_repo:MovieRepository = provider.movie_repository
    logger.debug("Starting to Get Available Movies")
    try:
        movies = movie_repo.get_all_available()
        return movies
    except Exception as e:
        logger.error("Error occured while getting available movies")
        raise


def get_movie_by_id(movie_id,provider:Provider):
    movie_repo:MovieRepository=provider.movie_repository
    try:
        raw_movie=movie_repo.get_by_id(movie_id)
        if not raw_movie:
            raise MovieNotFoundException(f"No Such movie with id {movie_id} ")
        movie=movie_repo.from_persistence(raw_movie,Movie)
        return movie
    except Exception as e:
        logger.error("An unexpected error occured during getting movie by id")
        raise

def check_duplicate_movie(movie_name: str,movie_repo:MovieRepository):
    movie = movie_repo.get_by_movie_name(movie_name)
    if movie:
        logger.warning("Attempt to create a duplicate movie: %s",movie_name)
        raise DuplicateMovieException("Movie already Exist")


    
    
    
    

