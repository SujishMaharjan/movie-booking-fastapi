from pydantic import BaseModel
from src.modules.movie.entity.movie import StatusType
from datetime import datetime

class BaseMovieResponse(BaseModel):
    id:str
    movie_name: str
    movie_status : StatusType

class AllMovieResponse(BaseMovieResponse):...

    
class MovieAddResponse(BaseMovieResponse):
    movie_description : str

class MovieResponseAvailable(MovieAddResponse):
    available_seats  : int

class MovieIdResponse(BaseMovieResponse):
    movie_description : str
    total_seats: int
    reserve_seats: int
    available_seats: int
    created_at: datetime
