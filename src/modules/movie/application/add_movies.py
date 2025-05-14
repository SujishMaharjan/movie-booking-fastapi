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
from src.entrypoints.api.movie.models import MovieAddModel
from src.modules.movie.entity.movie import Movie
from src.modules.user.exceptions import InvalidMemberTypeException
from src.core.provider import Provider
from src.core.log_config import logger

class CreateMovie:
    def __init__(self,provider:Provider):
        self.movie_repo:MovieRepository=provider.movie_repository

    def execute(self,movie_model:MovieAddModel,hall_settings:HallSettings):
        try:
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

            movie_data = self.movie_repo.to_persistence_model(movie)
            self.movie_repo.save(movie_data)
            logger.info("Movie created successfully: %s", movie.movie_name)
            return movie
        except Exception as e:
            logger.error("Unexpected error while creating movie: %s", movie_model.movie_name)
            raise

        
    def check_duplicate_movie(self, movie_name: str) -> bool:
        movie = self.movie_repo.get_by_movie_name(movie_name)
        if movie:
            logger.warning("Attempt to create a duplicate movie: %s",movie_name)
            raise DuplicateMovieException("Movie already Exist")
    
    
    

