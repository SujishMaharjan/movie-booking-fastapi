from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User
from src.modules.movie.entity.movie import Movie



class GetMovies:
    def __init__(self,token:str,user_repo:UserRepository,token_repo:TokenRepository,movie_repo:MovieRepository):
        self.token=token
        self.user_repo=user_repo
        self.token_repo= token_repo
        self.movie_repo=movie_repo

    def execute(self):
        username = self.token_repo.validate_and_decode_token(self.token)

        user = self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundException("User Not Found")
        
        user = self.user_repo.to_dataclass(user,User)
        self.is_admin(user.role)
        raw_movies = self.movie_repo.get_all()
        movies = [self.movie_repo.to_dataclass(movie,Movie) for movie in raw_movies] if raw_movies else []

        return movies
    
    def is_admin(self,role)->bool:
        if role!="admin":
            raise InvalidMemberTypeException("Access denied. Admin only.")
        return True