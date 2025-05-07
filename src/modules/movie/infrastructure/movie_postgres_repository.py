from src.modules.movie.interfaces.movie_repository import MovieRepository
from sqlalchemy.orm import Session
from src.modules.movie.entity.movie import Movie
from src.modules.movie.infrastructure.persistence.models import Movies
from typing import Union,List

class PostgresMovieRepository(MovieRepository):
    def __init__(self,session: Session):
        self.session = Session

    def save(self,movie:Movies)->Movie: 
        self.session.add(movie)
        self.session.commit()

    def get_by_id(self, movie_id: str)-> Union[Movies,None]:
        return self.session.query(Movies).filter(Movies.movie_id == movie_id).first()

    def get_by_movie_name(self, movie_name: str)-> Union[Movies,None]:
        return self.session.query(Movies).filter(Movies.movie_name == movie_name).first()

    def get_all(self)-> Union[List[Movies],None]:
        return self.session.query(Movies).all()

    def update_movie(self,movie_id,reserve_seats,available_seats,movie_status):
        self.session.query(Movies).filter(Movies.movie_id == movie_id).update(
            {Movies.reserve_seats : reserve_seats,
            Movies.available_seats : available_seats,
            Movies.movie_status : movie_status,
            },  # <-- new value
            synchronize_session=False
        )
        return True

    def to_dataclass(self,orm_obj, dataclass_type):
        data = {
            k: v for k, v in vars(orm_obj).items()
            if k in dataclass_type.__dataclass_fields__
        }
        return dataclass_type(**data)

    def to_persistence_model(self,movie:Movie)->Movies:
        return Movies(**movie.__dict__)