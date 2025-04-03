from pydantic import BaseModel
from .user import MemberType 
from .movie import AvailableType


class UserResponse(BaseModel):
    name : str
    username: str
    permission: MemberType


class MovieResponse(BaseModel):
    movie_name: str
    movie_status : AvailableType
    movie_description : str

class MovieResponseAvailable(MovieResponse):
    available_seats  : int


class ReserveResponse(BaseModel):
    username: str
    movie_name: str
    user_reserve_seats: int
    # message: Optional[str] = None

class UnReserveResponse(BaseModel):
    username: str
    movie_name: str
    before_reserve_seats: int
    update_reserve_seats: int