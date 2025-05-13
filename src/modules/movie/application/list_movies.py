from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User
from src.modules.movie.entity.movie import Movie
from src.core.provider import Provider



class GetMovies:
    def __init__(self,provider:Provider):
        self.movie_repo=provider.movie_respository

    def execute(self):
        
        raw_movies = self.movie_repo.get_all()
        movies = [self.movie_repo.to_dataclass(movie,Movie) for movie in raw_movies] if raw_movies else []
        return movies
