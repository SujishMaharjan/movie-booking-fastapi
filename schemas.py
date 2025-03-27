from pydantic import BaseModel
from enum import StrEnum
from typing import Optional


class MemberType(StrEnum):
    admin = "admin"
    member = "member"

class AvailableType(StrEnum):
    available = "Available"
    unavailable = "Unavailable"
    fully_reserved = "Fully Reserved"



class UsersBase(BaseModel):
    name: str
    date_of_birth : str
    email : str
    username : str
    password : str
    permission : MemberType
    disabled : Optional[bool] = True
    user_id : Optional[str] = None

class UserResponse(BaseModel):
    name : str
    username: str
    permission: MemberType
    # message: str

class MovieBase(BaseModel):
    movie_name: str
    movie_status : AvailableType
    movie_description : str
    total_seats : Optional[int] = 200
    booked_seats : Optional[int] = 0
    available_seats : Optional[int] = 200
    movie_id : Optional[str] = None

class MovieResponse(BaseModel):
    movie_name: str
    movie_status : AvailableType
    movie_description : str

class ReserveBase(BaseModel):
    username: str
    movie_name: str
    no_of_seats: int
    reserve_id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    username: str | None = None