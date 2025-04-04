from pydantic import BaseModel
from ..movie import AvailableType


class MovieResponse(BaseModel):
    movie_name: str
    movie_status : AvailableType
    movie_description : str

class MovieResponseAvailable(MovieResponse):
    available_seats  : int
