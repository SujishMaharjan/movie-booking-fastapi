import uuid
from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.user.exceptions import UserNotFoundException
from src.modules.user.entity.user import User
from src.modules.movie.exceptions import DuplicateMovieException
from src.modules.movie.entity.movie import Movie
from datetime import datetime
from src.config.settings import HallSettings
from src.api.entrypoint.movie.models import MovieAddModel
from src.modules.movie.entity.movie import Movie
from src.modules.user.exceptions import InvalidMemberTypeException

class CreateMovie:
    def __init__(
        self, 
        user_repository: UserRepository, 
        token_repository: TokenRepository,
        movie_repository: MovieRepository
    ):
        self.user_repo = user_repository
        self.token_repo = token_repository
        self.movie_repo= movie_repository
        

    def execute(self, token,movie_model:MovieAddModel,hall_settings:HallSettings):
        username=self.token_repo.validate_and_decode_token(token)
        user = self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundException("User Not Found")
        
        user = self.user_repo.to_dataclass(user,User)
        self.is_admin(user.role)
        self.check_duplicate_movie(movie_model.movie_name)

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

        movie_data = self.user_repo.to_persistence_model(movie)
        self.user_repository.save(movie_data)
        return movie
        

    def check_duplicate_movie(self, movie_name: str) -> bool:
        movie = self.movie_repo.get_by_movie_name(movie_name)
        if movie:
            raise DuplicateMovieException("Movie already Exist")
        return False
    
    def is_admin(self,role):
        if role!="admin":
            raise InvalidMemberTypeException("Access denied. Admin only.")
        return True
    

