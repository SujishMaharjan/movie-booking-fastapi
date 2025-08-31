from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.movie.exceptions import InvalidInputEnteredException
from src.modules.user.entity.user import User
from src.modules.movie.entity.movie import Movie
from src.core.provider import Provider



class GetMovieById:
    def __init__(self,provider:Provider):
        self.movie_repo:MovieRepository=provider.movie_repository

    def execute(self,movie_id):
        raw_movie=self.movie_repo.get_by_id(movie_id)
        if not raw_movie:
            raise InvalidInputEnteredException(f"No Such movie with id {movie_id} ")
        movie=self.movie_repo.to_dataclass(raw_movie,Movie)
        return movie
    