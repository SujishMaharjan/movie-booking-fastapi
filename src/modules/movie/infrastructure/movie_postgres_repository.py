from src.modules.movie.interfaces.movie_repository import MovieRepository
from sqlalchemy.orm import Session
from src.modules.movie.entity.movie import Movie, StatusType
from src.modules.movie.infrastructure.persistence.models import Movies
from typing import Union,List
from sqlalchemy.exc import SQLAlchemyError
from src.core.exceptions import DatabaseException
from src.core.log_config import logger


class PostgresMovieRepository(MovieRepository):
    def __init__(self,session: Session):
        self.session = session

    def save(self,movie:Movies): 
        try:
            self.session.add(movie)
            self.session.commit()
            logger.debug("Movie saved successfully in database %s", movie.movie_name)
        except SQLAlchemyError as e:
            logger.error("Failed to save movie in database: %s",str(e))
            raise DatabaseException("An unexpected error while saving movie in database") from e

    def get_by_id(self, movie_id: str)-> Union[Movies,None]:
        try:
            return self.session.query(Movies).filter(Movies.id == movie_id).first()
        except SQLAlchemyError as e:
            logger.error("Database Error during get_by_id: %s",str(e))
            raise DatabaseException("Failed to fetch movie by movie_id from database") from e
            

    def get_by_movie_name(self, movie_name: str)-> Union[Movies,None]:
        try:
            return self.session.query(Movies).filter(Movies.movie_name == movie_name).first()
        except SQLAlchemyError as e:
            logger.error("Database Error during get_by_movie_name: %s",str(e))
            raise DatabaseException("Failed to fetch movie by movie_name from database") from e
            
    

    def get_all(self)-> Union[List[Movies],None]:
        try:
            return self.session.query(Movies).all()
        except SQLAlchemyError as e:
            logger.error("Database Error during getting all movies: %s",str(e))
            raise DatabaseException("Failed to fetch list of movie from database") from e
            
    
    
    def get_all_available(self)-> Union[List[Movies],None]:
        try:
            return self.session.query(Movies).filter(Movies.movie_status == StatusType.AVAILABLE).all()
        except SQLAlchemyError as e:
            logger.error("Database error during getting all available movies: %s", str(e))
            raise DatabaseException("Failed to fetch available movies from database") from e

    def update_movie_seats_and_status(self,movie_id,reserve_seats,available_seats,movie_status):
        try:
            result=self.session.query(Movies).filter(Movies.id == movie_id).update(
                {Movies.reserve_seats : reserve_seats,
                Movies.available_seats : available_seats,
                Movies.movie_status : movie_status,
                },  # <-- new value
                synchronize_session=False
            )
            return True
        except SQLAlchemyError as e:
            logger.error("Database error while updating movie_seats and status in database:%s",str(e))
            raise DatabaseException("Failed to update movie_seats and status in database") from e

    def to_dataclass(self,orm_obj, dataclass_type):
        try:
            data = {
                k: v for k, v in vars(orm_obj).items()
                if k in dataclass_type.__dataclass_fields__
            }
            return dataclass_type(**data)
        except Exception as e:
            logger.exception("Failed to convert database model to entity/domain model")
            raise 

    def to_persistence_model(self,movie:Movie)->Movies:
        try:
            return Movies(**vars(movie))
        except Exception as e:
            logger.exception("Failed to convert to persistence model")
            raise