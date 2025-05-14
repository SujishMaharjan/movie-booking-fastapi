from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.movie.entity.movie import Movie
from src.core.provider import Provider
from src.core.log_config import logger

class GetAvailableMovies:
    def __init__(self,provider: Provider):
        self.movie_repo:MovieRepository = provider.movie_repository

    def exeute(self):
        logger.debug("Starting to Get Available Movies")
        try:
            raw_movies = self.movie_repo.get_all_available()
            movies = [self.movie_repo.to_dataclass(movie,Movie) for movie in raw_movies] if raw_movies else []
            return movies
        except Exception as e:
            logger.error("Error occured while getting available movies")
            raise