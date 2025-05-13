from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.movie.entity.movie import Movie
from src.core.provider import Provider

class GetAvailableMovies:
    def __init__(self,provider: Provider):
        self.movie_repo:MovieRepository = provider.movie_repository

    def exeute(self):
        raw_movies = self.movie_repo.get_all_available()
        movies = [self.movie_repo.to_dataclass(movie,Movie) for movie in raw_movies] if raw_movies else []
        return movies