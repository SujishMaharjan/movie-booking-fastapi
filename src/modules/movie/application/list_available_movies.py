from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.movie.entity.movie import Movie

class GetAvailableMovies:
    def __init__(self,movie_repo: MovieRepository):
        self.movie_repo = movie_repo

    def exeute(self):
        raw_movies = self.movie_repo.get_all_available()
        movies = [self.movie_repo.to_dataclass(movie,Movie) for movie in raw_movies] if raw_movies else []
        return movies