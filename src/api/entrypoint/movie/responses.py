from pydantic import BaseModel
from src.api.entrypoint.movie.models import AvailableType

class AllMovieResponse(BaseModel):
    movie_name: str
    movie_status : AvailableType

    
class MovieAddResponse(BaseModel):
    movie_name: str
    movie_status : AvailableType
    movie_description : str

class MovieResponseAvailable(MovieAddResponse):
    available_seats  : int
